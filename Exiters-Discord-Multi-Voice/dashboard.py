"""Dashboard startup entrypoint (replaces self-bot.py)."""

from __future__ import annotations

import asyncio
import os
import socket
import sys
import time
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from config import config, first_run_setup
from core.api import router as api_router
from core.auth import auth_middleware
from core.engine import bot_manager
from core.logger import app_logger, log_handler
from core.tunnel import tunnel_manager
from core.web import dashboard_route, websocket_endpoint

BANNER = """
 ███╗   ███╗ ██████╗ ██╗
 ████╗ ████║██╔════╝ ██║
 ██╔████╔██║██║  ███╗██║
 ██║╚██╔╝██║██║   ██║██║
 ██║ ╚═╝ ██║╚██████╔╝███████╗
 ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ 
"""


def get_local_ip() -> str:
    """Returns the machine's LAN IP (not the loopback address)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not send actual data; only lets the OS select the interface and source IP
        sock.connect(("8.8.8.8", 80))
        return str(sock.getsockname()[0])
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


_shutdown_done = False


async def shutdown() -> None:
    """Stops the bot and tunnel; cleanup runs only once."""
    global _shutdown_done
    if _shutdown_done:
        return
    _shutdown_done = True

    await bot_manager.stop_all()
    await tunnel_manager.stop()
    print("System has stopped.")
    sys.stdout.flush()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Cleanup when uvicorn shuts down (Ctrl+C or SIGTERM)."""
    yield
    await shutdown()


def create_app() -> FastAPI:
    """Creates the FastAPI app with middleware and all routes."""
    app = FastAPI(title="kwishtt", lifespan=lifespan)
    app.middleware("http")(auth_middleware)

    @app.get("/health")
    @app.get("/ping")
    async def direct_health() -> dict[str, Any]:
        """Direct health check route for cloud host uptime monitors."""
        return {
            "status": "ok",
            "uptime": round(time.time() - bot_manager.start_timestamp, 1),
            "bots_online": sum(1 for b in bot_manager.bots if b.is_ready()),
            "bots_in_voice": sum(1 for b in bot_manager.bots if b.is_in_voice),
        }

    app.include_router(api_router)
    app.add_api_websocket_route("/ws", websocket_endpoint)
    app.add_api_route(
        "/", dashboard_route, methods=["GET"], response_class=HTMLResponse
    )
    return app


def print_banner(lan_ip: str, tunnel_url: str | None) -> None:
    """Prints the banner and access links to the terminal."""
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)
    print()
    print(" Dashboard is running!")
    print()
    print(f" Web URL      : http://{lan_ip}:{config.port}")
    print(f" Password     : {config.password}")
    if tunnel_url:
        print(f" Remote Access: {tunnel_url}")
    print()
    print(" Press Ctrl+C to stop the system.")
    sys.stdout.flush()


async def _keep_alive_loop(url: str) -> None:
    """Pings the health endpoint every 10 minutes to prevent free hosting spindown."""
    health_url = url.rstrip("/") + "/health"
    app_logger.info("Keep-alive pinger started for: %s", health_url)
    import urllib.request
    while True:
        await asyncio.sleep(600)  # Ping every 10 minutes
        try:
            req = urllib.request.Request(
                health_url,
                headers={"User-Agent": "Dashboard-KeepAlive/1.0"}
            )
            await asyncio.to_thread(lambda: urllib.request.urlopen(req, timeout=10).read())
            app_logger.debug("Keep-alive ping sent successfully to %s", health_url)
        except Exception as exc:
            app_logger.debug("Keep-alive ping error: %s", exc)


async def main() -> None:
    """Starts the dashboard: config, tunnel, web server, and cleanup on shutdown."""
    first_run_setup()
    config.reload()

    # Load tokens from the file to preserve data between sessions
    bot_manager.tokens_file = config.tokens_file
    bot_manager.load_tokens()

    loop = asyncio.get_running_loop()
    log_handler.set_loop(loop)

    app = create_app()
    lan_ip = get_local_ip()

    try:
        tunnel_url: str | None = None
        if config.enable_tunnel:
            tunnel_url = await tunnel_manager.start(config.port)
            if tunnel_url is None:
                app_logger.warning("Failed to start Cloudflare Tunnel.")
        else:
            app_logger.info("Cloudflare Tunnel is disabled in the configuration.")

        print_banner(lan_ip, tunnel_url)

        # Start keep-alive pinger if URL is configured
        if config.keep_alive_url:
            asyncio.create_task(_keep_alive_loop(config.keep_alive_url))

        # Auto-start bots if configured via AUTO_START
        if config.auto_start and config.channel_ids and bot_manager.tokens:
            app_logger.info(
                "AUTO_START enabled: Starting %d tokens for channels %s...",
                len(bot_manager.tokens),
                config.channel_ids,
            )
            task = asyncio.create_task(
                bot_manager.start_normal(config.channel_ids, delay=5.0)
            )
            bot_manager._start_task = task

        # uvicorn.run() sẽ tạo event loop mới, không gọi được trong async main;
        # dùng Server.serve() để chạy cùng loop với bot_manager/tunnel.
        server = uvicorn.Server(
            uvicorn.Config(
                app,
                host=config.host,
                port=config.port,
                log_level="warning",
            )
        )
        await server.serve()
    finally:
        # Safety net if uvicorn exits without running lifespan shutdown
        await shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Ctrl+C falls outside main (for example, during startup) -> exit cleanly
        pass
