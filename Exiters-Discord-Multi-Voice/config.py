"""Application configuration and first-run setup."""

from __future__ import annotations

import getpass
import io
import logging
import os
import re
import secrets
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


logger = logging.getLogger(__name__)
PROJECT_DIR = Path(__file__).resolve().parent
ENV_FILE = PROJECT_DIR / ".env"


def _env_int(name: str, default: int) -> int:
    """Read an integer environment variable, falling back when invalid."""
    value = os.getenv(name)
    if value is None or not value.strip():
        return default

    try:
        return int(value)
    except ValueError:
        logger.warning("Giá trị %s không hợp lệ; dùng mặc định %d", name, default)
        return default


def _env_bool(name: str, default: bool) -> bool:
    """Read a boolean environment variable, falling back when invalid."""
    value = os.getenv(name)
    if value is None or not value.strip():
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False

    logger.warning("Giá trị %s không hợp lệ; dùng mặc định %s", name, default)
    return default


def first_run_setup() -> None:
    """Create the local environment file when running initially in interactive mode."""
    # If .env already exists or password is provided via environment, skip
    if ENV_FILE.exists() or os.getenv("DASHBOARD_PASSWORD"):
        return

    password = ""
    is_interactive = bool(sys.stdin and hasattr(sys.stdin, "isatty") and sys.stdin.isatty())
    if is_interactive:
        try:
            password = getpass.getpass("Đặt mật khẩu dashboard (nhấn Enter để dùng mặc định 'admin123'): ").strip()
        except (EOFError, io.UnsupportedOperation):
            password = ""

    if not password:
        password = os.getenv("DASHBOARD_PASSWORD", "admin123")

    jwt_secret = os.getenv("JWT_SECRET") or secrets.token_hex(32)
    try:
        ENV_FILE.write_text(
            f"DASHBOARD_PASSWORD={password}\nJWT_SECRET={jwt_secret}\n",
            encoding="utf-8",
        )
        logger.info("Đã tạo file cấu hình môi trường lần đầu tại %s", ENV_FILE)
    except OSError as exc:
        logger.warning("Không thể ghi file .env: %s", exc)


@dataclass
class AppConfig:
    """Typed application settings loaded from the project environment file."""

    host: str = "0.0.0.0"
    port: int = 7860
    password: str = ""
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 72
    tokens_file: str = "tokens.txt"
    enable_tunnel: bool = False
    cloudflared_path: str = "/usr/local/bin/cloudflared"
    auto_start: bool = False
    channel_ids: list[int] = field(default_factory=list)
    keep_alive_url: str = ""

    def __post_init__(self) -> None:
        """Load environment values after constructing the configuration."""
        self.reload()

    def reload(self) -> None:
        """Re-read ``.env`` and update all configuration attributes."""
        if ENV_FILE.exists():
            load_dotenv(dotenv_path=ENV_FILE, override=True)
        else:
            load_dotenv(override=False)

        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = _env_int("PORT", 7860)
        self.password = os.getenv("DASHBOARD_PASSWORD", "").strip()
        if not self.password:
            self.password = "admin123"

        self.jwt_secret = os.getenv("JWT_SECRET", "").strip()
        if not self.jwt_secret:
            self.jwt_secret = secrets.token_hex(32)

        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_expire_hours = _env_int("JWT_EXPIRE_HOURS", 72)
        self.tokens_file = os.getenv("TOKENS_FILE", "tokens.txt")

        # Disable tunnel by default if running in cloud or if cloudflared binary is not found
        has_cloudflared = bool(shutil.which("cloudflared") or shutil.which("cloudflared.exe"))
        is_cloud_env = bool(
            os.getenv("RENDER")
            or os.getenv("KOYEB")
            or os.getenv("SPACE_ID")
            or os.getenv("RAILWAY_ENVIRONMENT")
        )
        default_tunnel = has_cloudflared and not is_cloud_env
        self.enable_tunnel = _env_bool("ENABLE_TUNNEL", default_tunnel)
        self.cloudflared_path = os.getenv(
            "CLOUDFLARED_PATH", "/usr/local/bin/cloudflared"
        )

        self.auto_start = _env_bool("AUTO_START", False)
        channel_ids_str = os.getenv("CHANNEL_IDS", os.getenv("VOICE_CHANNEL_ID", ""))
        self.channel_ids = [
            int(c.strip())
            for c in re.split(r"[\s,;]+", channel_ids_str)
            if c.strip().isdigit()
        ]
        self.keep_alive_url = (
            os.getenv("KEEP_ALIVE_URL")
            or os.getenv("RENDER_EXTERNAL_URL")
            or ""
        ).strip()


first_run_setup()
config = AppConfig()
