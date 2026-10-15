# 🏙️ Mahalla Muammolari Platformasi (Telegram Bot)

Ushbu loyiha fuqarolarga o'z hududlaridagi (mahalla, tuman, viloyat) kommunal, ekologik va ijtimoiy muammolarni GPS orqali belgilab, mas'ul xodimlarga (adminlarga) yuborish imkonini beruvchi platformadir.

## 🚀 Asosiy Imkoniyatlar

- **🌐 Ko'p tilli interfeys:** O'zbekcha (🇺🇿), Ruscha (🇷🇺) va Inglizcha (🇺🇸).
- **📍 To'liq Hududlar Bazasi:** O'zbekistonning barcha 14 ta viloyat/shaharlari va 200+ tumanlari qamrab olingan.
- **📸 Ko'p Rasmli Tizim:** Bitta murojaatga cheksiz miqdorda rasm biriktirish imkoniyati.
- **🗺️ GPS Integratsiya:** Admin panelda muammo joylashgan nuqtani bevosita Google Maps/Xarita orqali ko'rish.
- **👨‍💻 Admin Panel (Advanced):**
  - Murojaatlarni sahifalab (Pagination) ko'rish.
  - Har bir murojaatga alohida matnli javob yozish va statusni o'zgartirish (*Done, Process, Yangi*).
  - Barcha ma'lumotlarni yagona **Excel** jadvaliga eksport qilish.
- **📢 Broadcast:** Botning barcha foydalanuvchilariga e'lon yuborish tizimi.
- **🏆 Reyting va Gamifikatsiya:** Ballar tizimi orqali faol fuqarolarni rag'batlantirish.
- **⏰ Eslatmalar:** 48 soat davomida ko'rilmagan murojaatlar haqida adminni ogohlantiruvchi avtomat tizim.

## 🛠️ Texnologiyalar

- **Python 3.x** - Dasturlash tili
- **Aiogram 3.x** - Telegram Bot Framework (asinx, FSM, FilterLari)
- **SQLite3** - Lokal ma'lumotlar bazasi (foydalanuvchilar, murojaatlar)
- **Pandas & Openpyxl** - Excel export uchun
- **Logging** - Xatolarni kuzatib borish va debug qilish

## 📦 O'rnatish

### 1. Loyihani yuklab oling:
```bash
git clone https://github.com/SolijonSolayev/Mahalla-Muammolari-Platformasi.git
cd Mahalla-Muammolari-Platformasi
```

### 2. Virtual muhit yarating (ixtiyoriy lekin tavsiya etiladi):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kerakli kutubxonalarni o'rnating:
```bash
pip install -r requirements.txt
```

### 4. TOKEN va Admin IDs'ni sozlang:
`main.py` yoki .env faylida quyidagi muhit o'zgaruvchilarini to'ldiring (Botxona standartlariga mos):

```text
BOT_TOKEN=your_bot_token_here
DATA_DIR=./data
ADMIN_IDS=12345678  # agar bir nechta bo'lsa: 12345,67890
```

## 🏃 Ishga tushirish

Botni ishga tushirish uchun:

```bash
python main.py
```

Agar hammasi to'g'ri bo'lsa, terminalda quyidagi xabar ko'rinishi mumkin:
```
Bot ishga tushmoqda... (long polling)
```

## 📋 Foydalanish Ko'rsatmasi

### 👥 Oddiy Foydalanuvchi Uchun:

1. **Botni Boshlash:** `/start` buyrug'i yoki botga ulanish
2. **Tili Tanlash:** Uz 🇺🇿, Ru 🇷🇺 yoki En 🇺🇸 ni tanlang
3. **Murojaat Yuborish:**
   - "📢 Muammo yuborish" tugmasini bosing
   - Viloyatni tanlang
   - Tumanni tanlang
   - Kategoriyani tanlang (Yo'llar, Kommunal, Ekologiya, Boshqa)
   - Ustuvorlik darajasini tanlang (Yuqori, O'rta, Past)
   - Muammo haqida to'liq ta'rif yozing
   - Rasm(lar) yuklang (bitta yoki bir nechta)
   - GPS lokatsiyasini yuboring
   - ✅ Murojaat qabul qilindi!

4. **Murojaatlarim:** O'zingizning yuborgan murojaatlaringizni ko'ring
5. **Statistika:** O'zingizning ballingizni va umumiy statistikani ko'ring
6. **Tilni O'zgartirish:** Istalgan vaqtda tili o'zgartirish mumkin

### 🔧 Admin Uchun:

1. **Admin Panel Kirish:** "👨‍💻 Admin Panel" tugmasini bosing
2. **Murojaatlarni Boshqarish:**
   - "📚 Murojaatlar" - barcha murojaatlarni sahifalar bo'yicha ko'ring
   - Murojaat ID'ni bosing - detalyni ko'ring
   - Rasm(lar)ni ko'ring va GPS lokatsiyani Google Maps'da ko'ring
   - **Status o'zgartirish:**
     - 🟡 Ko'rilmoqda (Yangi → Process)
     - ✅ Hal etildi (Process → Done)
   - **Javob Yozish:** Foydalanuvchiga matnli javob yuboring

3. **Broadcast Yuborish:**
   - "📣 Broadcast" tugmasini bosing
   - Barcha foydalanuvchilarga yuborish uchun xabar yozing
   - Avtomatik barcha faol foydalanuvchilarga tarqatiladi

4. **Statistika Eksporti:**
   - "📥 Excel Export" tugmasini bosing
   - Barcha murojaatlar va ma'lumotlar Excel jadvaliga chiqadi

## 🗄️ Ma'lumotlar Bazasi Strukturasi

### `users` Jadvali:
```
- user_id (INTEGER PRIMARY KEY): Foydalanuvchi Telegram ID
- lang (TEXT): Tili (uz, ru, en)
- points (INTEGER): Reyting ballari
- joined_at (DATETIME): Ro'yhatga olingan vaqt
```

### `reports` Jadvali:
```
- id (INTEGER PRIMARY KEY): Murojaat ID
- user_id (INTEGER): Foydalanuvchi ID
- category (TEXT): Kategoriya (Yo'llar, Kommunal, Ekologiya, Boshqa)
- priority (TEXT): Ustuvorlik (Yuqori, O'rta, Past)
- province (TEXT): Viloyat nomi
- district (TEXT): Tuman nomi
- description (TEXT): Muammo ta'rifi
- photos (TEXT): Rasm file ID'lari (JSON)
- latitude (REAL): GPS kenglik
- longitude (REAL): GPS uzunlik
- status (TEXT): Holati (Yangi, Process, Done)
- admin_reply (TEXT): Admin javob matni
- created_at (DATETIME): Murojaat vaqti
- lang (TEXT): Murojaat tili
```

## 💡 Kod Strukturasi

### 🔑 Asosiy Funksiyalar:

#### **Database Operatsiyalari** (45-58 qatorlar):
```python
def db_query(query, params=(), fetch=False, fetchall=False, get_id=False):
    # Ma'lumotlar bazasiga query yuborish
    # fetch=True → bitta qator
    # fetchall=True → barcha qatorlar
    # get_id=True → oxirgi insert ID qaytarish
```

#### **Foydalanuvchi Sessiyasi** (73-85 qatorlar):
```python
class Form(StatesGroup):
    # FSM (Finite State Machine) murojaat yaratish uchun
    region, district, cat, priority, desc, photo, loc

class AdminAction(StatesGroup):
    # Admin operatsiyalari uchun
    waiting_reply_text, report_id, broadcast_msg
```

#### **Murojaat Yaratish Jarayoni** (183-264 qatorlar):
- **183-191:** Viloyat tanlash
- **192-201:** Tuman tanlash
- **202-209:** Kategoriya tanlash
- **210-217:** Ustuvorlik tanlash
- **218-223:** Ta'rif yozish
- **224-243:** Rasm(lar) yuklash
- **244-264:** GPS lokatsiya va bazaga yozyuvchi

#### **Admin PANEL** (266-410 qatorlar):
- **267-274:** Admin asosiy menyusi
- **276-293:** Murojaatlar ro'yxati (sahifalar)
- **294-310:** Murojaat detalyasi
- **311-327:** Javob yozish va yuborish
- **328-337:** Status o'zgartirish
- **350-365:** Broadcast yuborish
- **374-379:** Excel eksport

#### **Eslatma Tizimi** (396-405 qatorlar):
```python
async def reminder_loop():
    # 48+ soat davomida ko'rilmagan murojaatlar haqida eslatma
    # Har 12 soatda tekshiradi
```

## 🎨 Keyboard Designi

Platforma 3 xil klaviaturadan foydalanadi:

### 1. **Til Tanlash Inline Keyboard:**
```
[Uz 🇺🇿] [Ru 🇷🇺] [En 🇺🇸]
```

### 2. **Asosiy Menyu (Reply Keyboard):**
```
[📢 Muammo yuborish] [🗺 Xarita]
[📋 Murojaatlarim] [❓ Qo'llanma]
[📊 Statistika] [🌐 Til]
[👨‍💻 Admin Panel] (faqat adminlarga)
```

### 3. **Admin Panel Inline Keyboard:**
```
[📚 Murojaatlar]
[📣 Broadcast]
[📥 Excel Export]
```

## 🔒 Xavfsizlik

- **Admin ID Tekshirish:** Faqat `ADMIN_IDS` ro'yxatidagi foydalanuvchilar admin amallarini amalga oshira oladi
- **Xato Xavfsizligi:** Barcha ma'lumotlar bazasi operatsiyalari `try-except` blokida himoya qilingan
- **Lokatsiya:** GPS koordinatalari faqat admin panelda ko'rinadi

## 📞 Texnik Ma'lumotlar

### Ayogram Filterlari:
- `Command("start")` - Komanda filter
- `F.data.startswith()` - Callback data filter
- `F.photo` - Media filter
- `F.location` - Lokatsiya filter

### FSM (Finite State Machine):
Bot har bir foydalanuvchi uchun alohida sessiyani boshqaradi, bu esa multi-user-multi-step jarayonlarni ishonchli bilan amalga oshirish imkoniyatini beradi.

### Async/Await:
Barcha uzun amallar asinxroniy bajariladi, bu esa ko'p foydalanuvchilar bilan ishlashni tezlashtiradi.

## 🐛 Debug Mode

Xatolarni ko'rish uchun logging shunga qarab yoqilgan:
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 📊 Namuna Ma'lumotlari

Platformada O'zbekistonning **14 ta viloyati** va **200+ tumani** mavjud:
- **Viloyatlar:** Toshkent, Andijon, Farg'ona, Namangan, Samarqand, Buxoro, Qashqadaryo, Surxondaryo, Jizzax, Sirdaryo, Navoiy, Xorazm, Qoraqalpog'iston

## 🚀 Keyingi Qadamlar (Takmillash Rejalari)

- [ ] Telegram WebApp bilan GPS qabul qilish
- [ ] Rasm kompressiyasi
- [ ] Qo'shimcha statistika va grafiklar
- [ ] Email bildirishnomalar
- [ ] Multi-language translation API integratsiyasi
- [ ] Analytics Dashboard

## 🚢 Deploy to Botxona (5 qadam)

Quyidagi 5 qadam orqali loyihani Botxona platformasiga oson va tez joylashtiring:

1. .env faylini yarating.
   - `.env.example` faylidan nusxa olib `.env` deb nomlang.
   - `.env` ichida BOT_TOKEN va DATA_DIR qiymatlarini to'ldiring:
     - `BOT_TOKEN=YOUR_TELEGRAM_TOKEN`
     - `DATA_DIR=./data` (yoki konteyner uchun `/app/data`)
   - (ixtiyoriy) ADMIN_IDS va boshqalarni to'ldiring.

2. GitHub-ga commit qiling yoki ZIP tayyorlang.
   - `git add .env.example requirements.txt` va boshqa o'zgartirishlarni commit qilib `git push` qiling; yoki butun loyihani ZIP qiling.

3. Botxona paneliga yuklang.
   - Panelda `Deploy from GitHub` yoki `Upload ZIP` funksiyasini tanlang.
   - Agar GitHub ulanmagan bo'lsa, ZIP faylni yuklang.

4. Paneldagi muhit o'zgaruvchilarini to'ldiring.
   - BOT_TOKEN = (sizning token)
   - DATA_DIR = ./data
   - (ixtiyoriy) ADMIN_IDS, TELEGRAM_API_URL, WEBHOOK_URL, WEBHOOK_PATH, WEBHOOK_SECRET, PORT
   - Start komandasi: `python main.py`

5. Ishga tushirib test qiling.
   - Panelda Deploy/Start bosing.
   - Botga `/start` yuboring — javob bo'lsa hammasi yaxshi.
   - Murojaat yuboring va DATA_DIR ichida `mahalla_platform.db` paydo bo'lganini tekshiring.

## 📝 Litsenziya

Bu loyiha ochiq manba (Open Source) loyihasining. Istalgan maqsadda foydalanish mumkin.

## 👤 Muallif

- **SolijonSolayev** - GitHub: [@SolijonSolayev](https://github.com/SolijonSolayev)

## 📧 Bog'lanish

Savollar yoki masalalar bo'lsa, GitHub Issues bo'limiga murojaat qiling yoki bevosita murojaat faylini oching.

---

**Muvaffaqiyali foydalanish!** 🎉
