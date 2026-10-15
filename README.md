# 🏙️ Mahalla Muammolari Platformasi (Telegram Bot)

Ushbu loyiha fuqarolarga o'z hududlaridagi (mahalla, tuman, viloyat) kommunal, ekologik va ijtimoiy muammolarni GPS orqali belgilab, mas'ul xodimlarga (adminlarga) yuborish imkonini beruvchi Telegram boti hisoblanadi.

---

## 🔐 Muhim — Botxona (talablar)

- Token faqat muhit o'zgaruvchisidan o'qilishi kerak: BOT_TOKEN. Kod ichida token saqlanmadi.
- Ma'lumotlar (SQLite DB, eksportlar, fayllar) faqat DATA_DIR papkasida yoziladi. DEFAULT: `./data`.
- TELEGRAM_API_URL ixtiyoriy — Botxona o'z proksisini ishlatadi, siz odatda bu qiymatni o'zgartirmaysiz.
- Long polling (getUpdates) default — webhook ishlatilmasa long polling ishlaydi.

---

## 🚀 Asosiy xususiyatlar

- Ko'p tilli: uz/ru/en
- Foydalanuvchilardan rasm va GPS qabul qilish
- Admin panel: murojaatlarni ko'rish, status o'zgartirish, javob yuborish
- Broadcast va Excel eksport (export fayli DATA_DIR ichida yaratiladi)
- Eslatma tizimi: 48+ soat davomida ko'rilmagan murojaatlar haqida adminlarga ogohlantirish

---

## 🧰 Fayllar va strukturasi

- `main.py` — botning kirish nuqtasi. Token va sozlamalar muhit o'zgaruvchilaridan olinadi.
- `requirements.txt` — pinlangan kutubxonalar (aiogram, pandas, python-dotenv).
- `.env.example` — barcha muhit o'zgaruvchilari va qisqacha izohlar.
- `.gitignore` — .env, data/, DB va eksport fayllarini kamaytiradi.
- `tests/smoke_test.py` — lokal smoke-test: DATA_DIR va DB jadvallari yaratilganligini tekshiradi.

---

## 🛠️ O'rnatish va lokal ishga tushirish (qadam‑qadam)

1) Repo klonlash:

```bash
git clone https://github.com/SolijonSolayev/Mahalla-Muammolari-Platformasi.git
cd Mahalla-Muammolari-Platformasi
```

2) Virtual muhit (tavsiya):

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
# Windows:
# venv\Scripts\activate
```

3) Kutubxonalarni o'rnatish:

```bash
pip install -r requirements.txt
```

4) .env faylini yaratish va to'ldirish:

```bash
cp .env.example .env
# yoki Windows PowerShell:
# copy .env.example .env
```

Keyin `.env` ichini to'ldiring (minimal):

```
BOT_TOKEN=your_bot_token_here
DATA_DIR=./data
ADMIN_IDS=12345678         # agar bir nechta bo'lsa vergul bilan ajrating
# TELEGRAM_API_URL= (ixtiyoriy)
```

.env faylida saqlangan tokenni hech qachon jamoat repo-ga qo'ymang.

5) Smoke-testni ishga tushirish (lokal tekshiruv):

```bash
python tests/smoke_test.py
```

Agar hammasi to'g'ri bo'lsa, skript chiqishi `OK: Kerakli jadvallar mavjud.` bo'ladi.

6) Botni ishga tushirish:

```bash
python main.py
```

Terminalda `Bot ishga tushmoqda... (long polling)` chiqishini ko'rasiz.

---

## 📦 Export va saqlash

- Excel eksport (`platform_data.xlsx`) endi `DATA_DIR` ichida yaratiladi.
- SQLite DB fayli nomi: `mahalla_platform.db` va u ham `DATA_DIR` ichida joylashadi.
- `.gitignore` yordamida bu fayllar repoga tushmaydi.

---

## ⚙️ Muhit o'zgaruvchilari (.env.example)

Muxtasar:

- BOT_TOKEN — (majburiy) Telegram Bot token
- DATA_DIR — (majburiy) ma'lumotlar uchun papka (yazish huquqi bo'lishi kerak)
- ADMIN_IDS — (ixtiyoriy) admin telegram id lar; vergul bilan ajrating
- TELEGRAM_API_URL — (ixtiyoriy) agar maxsus API kerak bo'lsa
- WEBHOOK_* — (ixtiyoriy) webhook orqali ishlash kerak bo'lsa

---

## 📌 Deploy (Botxona uchun tez 5 qadam)

1. `.env` yarating va to'ldiring (BOT_TOKEN va DATA_DIR zarur).
2. GitHub-ga push qiling yoki loyihani ZIP qilib tayyorlang.
3. Botxona paneliga loyihani yuklang (`Deploy from GitHub` yoki `Upload ZIP`).
4. Panelda Environment (muqovat) sozlamalariga BOT_TOKEN va DATA_DIR ni qo'ying; start komandasi: `python main.py`.
5. Deploy qiling va test qiling: botga `/start` yuboring, muammo yuborib DB fayli va eksportning `DATA_DIR` ichida paydo bo'lishini tekshiring.

---

## 🧪 Test va tekshirish

- `tests/smoke_test.py` — DB va jadvallarning mavjudligini tekshiradi.
- Agar `BOT_TOKEN` test uchun yo'q bo'lsa, skript test token bilan ishlaydi (lokal test uchun).

---

## 🔒 Xavfsizlik eslatmalari

- Hech qachon haqiqiy BOT_TOKEN ni `main.py` yoki boshqa kod fayllariga yozmang — faqat `.env` yoki hosting panelidagi muhit o'zgaruvchilariga kiriting.
- `DATA_DIR` ichidagi fayllar `.gitignore` orqali repoga tushmaydi.

---

## 👤 Muallif

- **SolijonSolayev** — GitHub: https://github.com/SolijonSolayev

---
