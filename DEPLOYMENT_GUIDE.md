# 🚀 24/7 Free Hosting Guide (কিভাবে ফ্রিতে ২৪/৭ হোস্ট করবেন)

এই গাইডটিতে স্টেপ-বাই-স্টেপ দেখানো হয়েছে কিভাবে এই Discord Multi-Voice Bot এবং Web Dashboard ফ্রিতে ২৪/৭ অনলাইনে রাখবেন, যাতে আপনার টোকেনগুলো সবসময় ভয়েস চ্যানেলে অনলাইনে থাকে।

---

## 🌟 অপশন ১: Koyeb (সবচেয়ে সেরা ও সহজ — ২৪/৭ স্লিপ ছাড়া চলবে)
> **কেন Koyeb?**
> - কোনো ক্রেডিট কার্ড ছাড়াই ফ্রিতে চালানো যায়।
> - Render-এর মতো ১৫ মিনিট পর ঘুমিয়ে (sleep) যায় না; ২৪/৭ একটানা চলতে থাকে।
> - অটোমেটিক HTTPS ডোমেইন লিঙ্ক পাওয়া যায়।

### Koyeb-এ হোস্ট করার স্টেপসমূহ:
1. **GitHub-এ প্রজেক্ট আপলোড করুন:**
   - GitHub-এ একটি নতুন Repository তৈরি করুন (Private রাখতে পারেন)।
   - আপনার এই পুরো ফোল্ডারটি GitHub রিপোজিটরিতে পুশ / আপলোড করুন।
2. **Koyeb অ্যাকাউন্ট তৈরি করুন:**
   - [koyeb.com](https://www.koyeb.com)-এ যান এবং GitHub দিয়ে Sign Up করুন।
3. **Create Service:**
   - ড্যাশবোর্ডে গিয়ে **"Create App"** অথবা **"Create Service"** বাটনে ক্লিক করুন।
   - Deployment Method হিসেবে **"GitHub"** সিলেক্ট করুন এবং আপনার রিপোজিটরি সিলেক্ট করুন।
   - Builder হিসেবে **"Dockerfile"** অথবা **"Buildpack"** সিলেক্ট করুন (Dockerfile সিলেক্ট করা সবচেয়ে ভালো)।
4. **Environment Variables সেট করুন:**
   - **Environment Variables** সেকশনে নিচের ভেরিয়েবলগুলো যুক্ত করুন:
     - `DASHBOARD_PASSWORD`: আপনার ড্যাশবোর্ড লগইন পাসওয়ার্ড (যেমন: `mysecret123`)
     - `AUTO_START`: `true` (যাতে সার্ভার চালু হওয়ামাত্রই নিজে নিজে টোকেনগুলো ভয়েস চ্যানেলে ঢুকে পড়ে)
     - `CHANNEL_IDS`: আপনার Discord Voice Channel ID (যেমন: `123456789012345678`)
     - `TOKENS`: আপনার টোকেনগুলো কমা দিয়ে আলাদা করে দিতে পারেন (অথবা পরে ড্যাশবোর্ড থেকেও যুক্ত করতে পারবেন)
5. **Deploy বাটনে ক্লিক করুন:**
   - **"Deploy"** বাটনে ক্লিক করুন। ২-৩ মিনিটের মধ্যে অ্যাপটি বিল্ড হয়ে লাইভ হয়ে যাবে!
   - Koyeb আপনাকে একটি পাবলিক URL দিবে (যেমন: `https://xxxx-yourname.koyeb.app`)।
   - ব্রাউজারে সেই URL ওপেন করে আপনার পাসওয়ার্ড দিয়ে লগইন করুন এবং টোকেনগুলো লাইভ কন্ট্রোল করুন!

---

## 🌟 অপশন ২: Hugging Face Spaces (২৪/৭ ফ্রি ডকার — 16GB RAM)
> **কেন Hugging Face?**
> - ২ কোর CPU, ১৬ জিবি র‍্যাম সম্পূর্ণ ফ্রি!
> - কখনো স্লিপ মোডে যায় না, সবসময় ২৪/৭ অনলাইনে থাকে।

### Hugging Face Spaces-এ হোস্ট করার স্টেপসমূহ:
1. [huggingface.co](https://huggingface.co)-এ একটি ফ্রি অ্যাকাউন্ট খুলুন।
2. উপরে আপনার প্রোফাইল থেকে **"New Space"**-এ ক্লিক করুন।
3. Space Settings:
   - **Space Name:** যে কোনো নাম দিন (যেমন: `discord-multi-voice`)
   - **License:** `mit` বা `apache-2.0`
   - **Space SDK:** **Docker** নির্বাচন করুন
   - **Docker Template:** **Blank** নির্বাচন করুন
   - **Space Hardware:** Free (2 vCPU, 16GB RAM)
   - Privacy: **Private** বা **Public** (টোকেনের নিরাপত্তার জন্য Private রাখা ভালো)
4. **ফাইল আপলোড করুন:**
   - Space তৈরি হলে **"Files"** ট্যাবে গিয়ে আপনার এই প্রজেক্টের ফাইলগুলো ড্র্যাগ & ড্রপ করে আপলোড করে দিন (অথবা Git দিয়ে পুশ করুন)।
5. **Settings -> Variables and Secrets:**
   - `DASHBOARD_PASSWORD`: আপনার পছন্দের পাসওয়ার্ড
   - `AUTO_START`: `true`
   - `CHANNEL_IDS`: ভয়েস চ্যানেল আইডি
   - `TOKENS`: আপনার ডিসকর্ড টোকেনগুলো
6. Space অটোমেটিক বিল্ড শুরু হবে এবং Running স্ট্যাটাস দেখাবে। আপনি Hugging Face-এর লিঙ্ক দিয়েই ড্যাশবোর্ড ব্যবহার করতে পারবেন!

---

## 🌟 অপশন ৩: Render.com (ফ্রি ওয়েব সার্ভিস)
> **মনে রাখবেন:** Render Free Tier-এ ১৫ মিনিট ট্রাফিক না থাকলে স্লিপ মোডে যায়। তবে আমরা এতে **Keep-Alive Pinger** যুক্ত করে দিয়েছি, তাই এটি ২৪/৭ অনলাইনে রাখা সম্ভব।

### Render-এ হোস্ট করার স্টেপসমূহ:
1. GitHub-এ কোড পুশ করুন।
2. [render.com](https://render.com)-এ যান এবং GitHub দিয়ে লগইন করুন।
3. **New +** -> **Web Service** সিলেক্ট করুন।
4. আপনার রিপোজিটরি কানেক্ট করুন।
5. সেটিংস:
   - **Environment:** `Python` বা `Docker`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python dashboard.py`
   - **Plan:** Free
6. Environment Variables-এ যোগ করুন:
   - `DASHBOARD_PASSWORD`: আপনার পাসওয়ার্ড
   - `AUTO_START`: `true`
   - `CHANNEL_IDS`: আপনার ভয়েস চ্যানেল আইডি
7. **Keep-Alive চালু করা:**
   - রেন্ডার আপনাকে যে URL দিবে (যেমন: `https://your-bot.onrender.com`), সেটি কপি করুন।
   - [cron-job.org](https://cron-job.org) অথবা [uptimerobot.com](https://uptimerobot.com)-এ একটি ফ্রি অ্যাকাউন্ট খুলুন।
   - সেখানে একটি মনিটর বানিয়ে আপনার লিঙ্ক দিন: `https://your-bot.onrender.com/health` এবং প্রতি ৫ মিনিট পর পর পিং দিতে সেট করুন।
   - এর ফলে Render কখনোই স্লিপে যাবে না এবং আপনার টোকেন ২৪/৭ ভয়েস চ্যানেলে থাকবে!

---

## 🔧 প্রয়োজনীয় Environment Variables তালিকা:

| Variable | ডিফল্ট | বিবরণ |
| :--- | :--- | :--- |
| `DASHBOARD_PASSWORD` | `admin123` | ড্যাশবোর্ডে লগইন করার পাসওয়ার্ড |
| `AUTO_START` | `false` | `true` দিলে সার্ভার চালু হতেই স্বয়ংক্রিয়ভাবে ভয়েসে কানেক্ট হবে |
| `CHANNEL_IDS` | *(খালি)* | ভয়েস চ্যানেলের আইডি (একাধিক হলে কমা দিয়ে লিখুন) |
| `TOKENS` | *(খালি)* | ডিসকর্ড টোকেনগুলো (কমা অথবা নতুন লাইনে দিন) |
| `PORT` | `8080` | হোস্টিং প্রোভাইডার অটোমেটিক সেট করে নেয় |
| `KEEP_ALIVE_URL` | *(খালি)* | সেলফ-পিংয়ের জন্য আপনার অ্যাপ্লিকেশনের URL |

---

## 🖥️ লোকাল কম্পিউটারে রান করার নিয়ম:
1. `Exiters-Discord-Multi-Voice` ফোল্ডারে থাকা `run.bat` ফাইলটিতে ডাবল ক্লিক করুন।
2. ব্রাউজারে `http://localhost:8080` ওপেন করে লগইন করুন (ডিফল্ট পাসওয়ার্ড: `admin123`)।
3. ড্যাশবোর্ড থেকে টোকেন সেভ করুন এবং এক ক্লিকে START বাটনে চাপুন!
