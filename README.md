# 🤖 SecureShare Bot (Telegram Uploader) | ربات امن‌رسان (آپلودر تلگرام)

A powerful Telegram file uploader bot with secure sharing and automatic cleanup | ربات آپلودر تلگرام با قابلیت اشتراک‌گذاری امن و پاکسازی خودکار

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/PTB-20.0%2B-blue)](https://python-telegram-bot.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 📌 English Description

### What is SecureShare Bot?
SecureShare Bot is a professional Telegram uploader bot that allows admins to upload files and share them through unique links. It includes features like mandatory channel membership verification and automatic file deletion for enhanced security.

### Features
- 🔒 Secure file uploading and sharing through unique links
- 📤 Professional file uploader for Telegram channels
- ✅ Channel membership verification
- 📊 File engagement tracking (likes, dislikes, downloads)
- ⏱️ Automatic file cleanup after 30 seconds
- 💾 Automatic database backup to Discord
- 👮 Admin-only upload capability
- 📁 Supports multiple file types (documents, videos, photos, audio)
- 🔄 Auto-delete feature for better security

### Requirements
- Python 3.9 or higher
- python-telegram-bot library
- SQLite3
- Additional dependencies listed in requirements.txt

### Installation
1. Clone the repository:
```bash
git clone https://github.com/mohsenakhavan/secureshare-bot.git
cd secureshare-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
- Set your Telegram Bot Token
- Add admin user IDs
- Configure required channel usernames
- Set Discord webhook URL for backups

4. Run the bot:
```bash
python main.py
```

### Usage
1. Admin uploads any file to the bot
2. Bot generates a unique sharing link
3. Users must join required channels to access files
4. Files are automatically deleted after 30 seconds
5. Users can interact with files through likes/dislikes

### Configuration
Edit the following variables in the code:
```python
TOKEN = 'YOUR-BOT-TOKEN'
OWNER_IDS = [your_telegram_id]
DISCORD_WEBHOOK_URL = 'YOUR-DISCORD-WEBHOOK'
REQUIRED_CHANNELS = ['@channel1', '@channel2']
```

---

## 📌 توضیحات فارسی

### ربات امن‌رسان چیست؟
ربات امن‌رسان یک ربات آپلودر حرفه‌ای تلگرام است که به ادمین‌ها اجازه می‌دهد فایل‌های خود را آپلود کرده و از طریق لینک‌های یکتا به اشتراک بگذارند. این ربات شامل ویژگی‌هایی مانند تأیید عضویت اجباری در کانال و حذف خودکار فایل‌ها برای امنیت بیشتر است.

### ویژگی‌ها
- 🔒 آپلود و اشتراک‌گذاری امن فایل از طریق لینک‌های یکتا
- 📤 آپلودر حرفه‌ای فایل برای کانال‌های تلگرام
- ✅ بررسی عضویت اجباری در کانال‌های مورد نیاز
- 📊 پیگیری تعاملات فایل (لایک، دیسلایک، دانلود)
- ⏱️ پاکسازی خودکار فایل‌ها پس از ۳۰ ثانیه
- 💾 پشتیبان‌گیری خودکار از پایگاه داده در دیسکورد
- 👮 قابلیت آپلود فایل فقط برای ادمین‌ها
- 📁 پشتیبانی از انواع فایل (سند، ویدیو، عکس، صوت)
- 🔄 قابلیت حذف خودکار برای امنیت بیشتر

### پیش‌نیازها
- پایتون ۳.۹ یا بالاتر
- کتابخانه python-telegram-bot
- SQLite3
- سایر وابستگی‌های ذکر شده در requirements.txt

### نصب و راه‌اندازی
1. کلون کردن مخزن:
```bash
git clone https://github.com/mohsenakhavan/secureshare-bot.git
cd secureshare-bot
```

2. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

3. پیکربندی ربات:
- تنظیم توکن ربات تلگرام
- افزودن شناسه‌های کاربری ادمین‌ها
- تنظیم نام‌کاربری کانال‌های مورد نیاز
- تنظیم وبهوک دیسکورد برای پشتیبان‌گیری

4. اجرای ربات:
```bash
python main.py
```

### نحوه استفاده
1. ادمین فایل را در ربات آپلود می‌کند
2. ربات یک لینک یکتا برای اشتراک‌گذاری تولید می‌کند
3. کاربران باید عضو کانال‌های مورد نیاز باشند
4. فایل‌ها پس از ۳۰ ثانیه به طور خودکار حذف می‌شوند
5. کاربران می‌توانند با لایک/دیسلایک با فایل‌ها تعامل کنند

### پیکربندی
متغیرهای زیر را در کد ویرایش کنید:
```python
TOKEN = 'توکن-ربات-شما'
OWNER_IDS = [شناسه_تلگرام_شما]
DISCORD_WEBHOOK_URL = 'وبهوک-دیسکورد-شما'
REQUIRED_CHANNELS = ['@کانال1', '@کانال2']
```

## 🔍 Keywords
- Telegram File Uploader Bot
- Telegram File Share Bot
- Secure File Sharing
- Channel Membership Bot
- Auto-delete Telegram Files
- ربات آپلودر تلگرام
- ربات آپلودر فایل
- آپلودر کانال تلگرام
- ربات اشتراک فایل تلگرام
- اشتراک‌گذاری امن فایل
- ربات عضویت اجباری کانال
- حذف خودکار فایل تلگرام
- آپلودر اتوماتیک تلگرام
- ربات آپلود فایل تلگرام

## 📄 License | مجوز
MIT License - feel free to use and modify | مجوز MIT - استفاده و تغییر آزاد

## 🤝 Contributing | مشارکت
Contributions, issues, and feature requests are welcome! | مشارکت‌ها، گزارش مشکلات و درخواست‌های ویژگی‌های جدید پذیرفته می‌شوند!

## ⭐ Support | حمایت
If you find this project helpful, please give it a star! | اگر این پروژه برایتان مفید است، لطفاً به آن ستاره دهید!

## 📱 Contact | تماس
For questions and support, join our Telegram channel | برای پرسش و پشتیبانی، به کانال تلگرام ما بپیوندید: [@securexweb](https://t.me/securexweb)
