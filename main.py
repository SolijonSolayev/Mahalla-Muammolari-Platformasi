import logging
import asyncio
import sqlite3
import json
from datetime import datetime, timedelta
import pandas as pd
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton, 
    ReplyKeyboardRemove, FSInputFile, WebAppInfo, InputMediaPhoto
)

# --- KONFIGURATSIYA ---
TOKEN = "8507163454:AAFXvQv8qfVdVKkmLZibABetauMh1L9AE7A"
ADMIN_IDS = [6266750005]  
WEB_APP_URL = "https://google.com/maps"

# O'zbekistonning barcha viloyat va tumanlari (To'liq ro'yxat)
REGIONS = {
    "Toshkent sh.": ["Yunusobod", "Chilonzor", "Mirzo Ulug'bek", "Yashnobod", "Olmazor", "Sergeli", "Uchtepa", "Bektemir", "Mirobod", "Shayxontohur", "Yakkasaroy", "Yangihayot"],
    "Toshkent vil.": ["Nurafshon sh.", "Olmaliq sh.", "Angren sh.", "Chirchiq sh.", "Bekobod sh.", "Akkurgan", "Bekobod t.", "Bo'stonliq", "Bo'ka", "Zangiota", "Qibray", "Quyi Chirchiq", "Parkent", "Pskent", "O'rta Chirchiq", "Chinoz", "Yuqori Chirchiq", "Yangiyo'l t.", "Toshkent t."],
    "Andijon": ["Andijon sh.", "Xonobod sh.", "Andijon t.", "Asaka", "Baliqchi", "Bo'ston", "Buloqboshi", "Jalaquduq", "Izboskan", "Qo'rg'ontepa", "Marhamat", "Oltinko'l", "Paxtaobod", "Ulughnor", "Shahrixon", "Xo'jaobod"],
    "Farg'ona": ["Farg'ona sh.", "Marg'ilon sh.", "Qo'qon sh.", "Quvasoy sh.", "Oltiariq", "Bag'dod", "Beshariq", "Buvayda", "Dang'ara", "Yozyovon", "Quva", "Rishton", "So'x", "Toshloq", "O'zbekiston", "Uchko'prik", "Farg'ona t.", "Furqat"],
    "Namangan": ["Namangan sh.", "Chust", "Pop", "Uychi", "Uchqo'rg'on", "Norin", "Mingbuloq", "Kosonsoy", "Namangan t.", "Yangiqo'rg'on", "To'raqo'rg'on", "Davlatobod", "Yangi Namangan"],
    "Samarqand": ["Samarqand sh.", "Kattaqo'rg'on sh.", "Oqdaryo", "Bulung'ur", "Jomboy", "Ishtixon", "Kattaqo'rg'on t.", "Narpay", "Payariq", "Pastdarg'om", "Paxtachi", "Samarqand t.", "Nurobod", "Urgut", "Toyloq", "Qo'shrabot"],
    "Buxoro": ["Buxoro sh.", "Kogon sh.", "Buxoro t.", "Vobkent", "Gijduvon", "Jondor", "Kogon t.", "Qorako'l", "Qorovulbozor", "Olot", "Peshku", "Romitan", "Shofirkon"],
    "Qashqadaryo": ["Qarshi sh.", "Shahrisabz sh.", "G'uzor", "Dehqonobod", "Qamashi", "Karshi t.", "Koson", "Kasbi", "Kitob", "Muborak", "Nishon", "Chiroqchi", "Shahrisabz t.", "Yakkabog'", "Ko'kdala"],
    "Surxondaryo": ["Termiz sh.", "Angor", "Boysun", "Denov", "Jarqo'rg'on", "Qiziriq", "Qumqo'rg'on", "Muzrabot", "Oltinsoy", "Sariosiyo", "Termiz t.", "Uzun", "Sherobod", "Sho'rchi"],
    "Jizzax": ["Jizzax sh.", "Arnasoy", "Baxmal", "Do'stlik", "Sh.Rashidov", "Zafarobod", "Zarbdor", "Zamin", "Mirzacho'l", "Paxtakor", "Forish", "Yangiobod"],
    "Sirdaryo": ["Guliston sh.", "Yangiyer sh.", "Shirin sh.", "Boyovut", "Guliston t.", "Sardoba", "Mirzaobod", "Oqoltin", "Sayhunobod", "Sirdaryo t.", "Xovos"],
    "Navoiy": ["Navoiy sh.", "Zarafshon sh.", "Karmana", "Konimex", "Qiziltepa", "Navbahor", "Nurota", "Tomdi", "Uchquduq", "Xatirchi"],
    "Xorazm": ["Urganch sh.", "Xiva sh.", "Bog'ot", "Gurlan", "Qo'shko'pir", "Shovot", "Tuproqqala", "Xazorasp", "Xonqa", "Xiva t.", "Yangiarik", "Yangibozor", "Urganch t."],
    "Qoraqalpog'iston": ["Nukus sh.", "Amudaryo", "Beruniy", "Kegeyli", "Qonliko'l", "Qorao'zak", "Qo'ng'irot", "Mo'ynoq", "Nukus t.", "Taxtako'pir", "To'rtko'l", "Xo'jayli", "Chimboy", "Shumanay", "Ellikqala", "Taxiatosh", "Bo'zatov"]
}

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- BAZA FUNKSIYALARI ---
def db_query(query, params=(), fetch=False, fetchall=False, get_id=False):
    try:
        with sqlite3.connect('mahalla_platform.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch: return cursor.fetchone()
            if fetchall: return cursor.fetchall()
            if get_id: 
                conn.commit()
                return cursor.lastrowid
            conn.commit()
    except Exception as e:
        logger.error(f"Database Error: {e}")
        return None

def init_db():
    db_query('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY, lang TEXT DEFAULT 'uz', points INTEGER DEFAULT 0, joined_at DATETIME
    )''')
    db_query('''CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, category TEXT, priority TEXT,
        province TEXT, district TEXT, description TEXT, photos TEXT, latitude REAL, longitude REAL,
        status TEXT DEFAULT 'Yangi', admin_reply TEXT DEFAULT 'Javob berilmadi', created_at DATETIME, lang TEXT
    )''')

init_db()

# --- STATES ---
class Form(StatesGroup):
    region = State()
    district = State()
    cat = State()
    priority = State()
    desc = State()
    photo = State()
    loc = State()

class AdminAction(StatesGroup):
    waiting_reply_text = State()
    report_id = State()
    broadcast_msg = State()

# --- TARJIMALAR ---
TEXTS = {
    'uz': {
        'start': "Xush kelibsiz! Tilni tanlang:",
        'guide': "📖 **Bot qo'llanmasi:**\n\n1️⃣ **Muammo yuborish** tugmasini bosing.\n2️⃣ Viloyat va tumaningizni tanlang.\n3️⃣ Kamida 1 ta rasm yuklang va muammoni ta'riflang.\n4️⃣ GPS lokatsiyani yuboring.\n\n🎁 **Reyting:** Faollik uchun ballar yig'ing!",
        'main_menu': "Asosiy menyu",
        'btn_report': "📢 Muammo yuborish",
        'btn_help': "❓ Qo'llanma",
        'btn_stats': "📊 Statistika/Reyting",
        'btn_my_reports': "📋 Murojaatlarim",
        'btn_admin': "👨‍💻 Admin Panel",
        'btn_lang': "🌐 Tilni o'zgartirish",
        'ask_reg': "Viloyatni tanlang:",
        'ask_dist': "Tumanni tanlang:",
        'ask_cat': "Kategoriyani tanlang:",
        'ask_pri': "Ustuvorlik darajasi:",
        'ask_desc': "Muammo haqida yozing:",
        'ask_photo': "Rasm yuboring. Tugatgach '✅ Bo'ldi' ni bosing:",
        'ask_loc': "📍 GPS joylashuvni yuboring:",
        'confirm': "✅ Murojaat qabul qilindi! ID: #{}",
        'status_upd': "Sizning #{} murojaatingiz statusi: {}",
        'priority_high': "🔴 Yuqori", 'priority_med': "🟡 O'rta", 'priority_low': "🟢 Past"
    },
    'ru': {
        'start': "Добро пожаловать! Выберите язык:",
        'guide': "📖 **Инструкция:**\n1. Нажмите '📢 Сообщить'.\n2. Выберите регион и фото.\n3. Отправьте GPS локацию.",
        'main_menu': "Главное меню",
        'btn_report': "📢 Сообщить о проблеме",
        'btn_help': "❓ Помощь",
        'btn_stats': "📊 Статистика",
        'btn_my_reports': "📋 Мои заявки",
        'btn_admin': "👨‍💻 Админ Панель",
        'btn_lang': "🌐 Сменить язык",
        'ask_reg': "Выберите область:",
        'ask_dist': "Выберите район:",
        'priority_high': "🔴 Высокий", 'priority_med': "🟡 Средний", 'priority_low': "🟢 Низкий",
        'confirm': "✅ Принято! ID: #{}",
    },
    'en': {
        'start': "Welcome! Choose language:",
        'guide': "📖 **Guide:**\n1. Click 'Report'.\n2. Send photo and region.\n3. Send GPS location.",
        'main_menu': "Main Menu",
        'btn_report': "📢 Report a Problem",
        'btn_help': "❓ Guide",
        'btn_stats': "📊 Stats/Rating",
        'btn_my_reports': "📋 My Reports",
        'btn_admin': "👨‍💻 Admin Panel",
        'btn_lang': "🌐 Language",
        'ask_reg': "Select Province:",
        'ask_dist': "Select District:",
        'ask_pri': "Priority level:",
        'confirm': "✅ Report accepted! ID: #{}",
        'priority_high': "🔴 High", 'priority_med': "🟡 Medium", 'priority_low': "🟢 Low"
    }
}

# --- KEYBOARDS ---
def get_lang_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Uz 🇺🇿", callback_data="l_uz"),
         InlineKeyboardButton(text="Ru 🇷🇺", callback_data="l_ru"),
         InlineKeyboardButton(text="En 🇺🇸", callback_data="l_en")]
    ])

def get_main_kb(uid, lang):
    is_admin = uid in ADMIN_IDS
    kb = [
        [KeyboardButton(text=TEXTS[lang]['btn_report'])],
        [KeyboardButton(text="🗺 Xarita", web_app=WebAppInfo(url=WEB_APP_URL))],
        [KeyboardButton(text=TEXTS[lang]['btn_my_reports']), KeyboardButton(text=TEXTS[lang]['btn_help'])],
        [KeyboardButton(text=TEXTS[lang]['btn_stats']), KeyboardButton(text=TEXTS[lang]['btn_lang'])]
    ]
    if is_admin: kb.append([KeyboardButton(text=TEXTS[lang]['btn_admin'])])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

bot = Bot(token=TOKEN)
dp = Dispatcher()

def g_lang(uid):
    res = db_query("SELECT lang FROM users WHERE user_id = ?", (uid,), fetch=True)
    return res[0] if res else 'uz'

# --- START ---
@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    db_query("INSERT OR IGNORE INTO users (user_id, joined_at) VALUES (?, ?)", (m.from_user.id, datetime.now()))
    await m.answer(TEXTS['uz']['start'], reply_markup=get_lang_kb())

@dp.callback_query(F.data.startswith("l_"))
async def set_lang(c: types.CallbackQuery):
    lang = c.data.split("_")[1]
    db_query("UPDATE users SET lang = ? WHERE user_id = ?", (lang, c.from_user.id))
    await c.message.delete()
    await c.message.answer(TEXTS[lang].get('guide', 'Guide'), parse_mode="Markdown", reply_markup=get_main_kb(c.from_user.id, lang))

# --- MUROJAAT JARAYONI ---
@dp.message(F.text.in_([TEXTS['uz']['btn_report'], TEXTS['ru']['btn_report'], TEXTS['en']['btn_report']]))
async def report_start(m: types.Message, state: FSMContext):
    l = g_lang(m.from_user.id)
    keys = list(REGIONS.keys())
    # Hududlar menyusi
    kb_btns = [[KeyboardButton(text=keys[i]), KeyboardButton(text=keys[i+1])] if i+1<len(keys) else [KeyboardButton(text=keys[i])] for i in range(0, len(keys), 2)]
    await state.set_state(Form.region)
    await m.answer(TEXTS[l]['ask_reg'], reply_markup=ReplyKeyboardMarkup(keyboard=kb_btns, resize_keyboard=True))

@dp.message(Form.region)
async def f_region(m: types.Message, state: FSMContext):
    if m.text not in REGIONS: return
    await state.update_data(region=m.text)
    dists = REGIONS[m.text]
    # Tumanlar menyusi
    kb_btns = [[KeyboardButton(text=dists[i]), KeyboardButton(text=dists[i+1])] if i+1<len(dists) else [KeyboardButton(text=dists[i])] for i in range(0, len(dists), 2)]
    await state.set_state(Form.district)
    await m.answer(TEXTS[g_lang(m.from_user.id)]['ask_dist'], reply_markup=ReplyKeyboardMarkup(keyboard=kb_btns, resize_keyboard=True))

@dp.message(Form.district)
async def f_district(m: types.Message, state: FSMContext):
    await state.update_data(district=m.text)
    l = g_lang(m.from_user.id)
    cats = ["Roads", "Utility", "Eco", "Other"] if l == 'en' else ["Yo'llar", "Kommunal", "Ekologiya", "Boshqa"]
    await state.set_state(Form.cat)
    await m.answer(TEXTS[l]['ask_cat'], reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=x)] for x in cats], resize_keyboard=True))

@dp.message(Form.cat)
async def f_cat(m: types.Message, state: FSMContext):
    await state.update_data(cat=m.text)
    l = g_lang(m.from_user.id)
    kb = [[KeyboardButton(text=TEXTS[l]['priority_high'])], [KeyboardButton(text=TEXTS[l]['priority_med'])], [KeyboardButton(text=TEXTS[l]['priority_low'])]]
    await state.set_state(Form.priority)
    await m.answer(TEXTS[l]['ask_pri'], reply_markup=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(Form.priority)
async def f_pri(m: types.Message, state: FSMContext):
    await state.update_data(priority=m.text)
    await state.set_state(Form.desc)
    await m.answer(TEXTS[g_lang(m.from_user.id)]['ask_desc'], reply_markup=ReplyKeyboardRemove())

@dp.message(Form.desc)
async def f_desc(m: types.Message, state: FSMContext):
    await state.update_data(desc=m.text, photos=[])
    await state.set_state(Form.photo)
    await m.answer(TEXTS[g_lang(m.from_user.id)]['ask_photo'])

@dp.message(Form.photo, F.photo)
async def f_photo(m: types.Message, state: FSMContext):
    data = await state.get_data()
    pts = data.get('photos', [])
    pts.append(m.photo[-1].file_id)
    await state.update_data(photos=pts)
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="✅ Bo'ldi")]], resize_keyboard=True)
    await m.answer(f"📸 {len(pts)} ta rasm qo'shildi. Davom eting yoki tugating.", reply_markup=kb)

@dp.message(Form.photo, F.text == "✅ Bo'ldi")
async def f_photo_done(m: types.Message, state: FSMContext):
    await state.set_state(Form.loc)
    await m.answer(TEXTS[g_lang(m.from_user.id)]['ask_loc'], reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📍 GPS", request_location=True)]], resize_keyboard=True))

@dp.message(Form.loc, F.location)
async def f_loc(m: types.Message, state: FSMContext):
    d = await state.get_data()
    uid, l = m.from_user.id, g_lang(m.from_user.id)
    rid = db_query('''INSERT INTO reports 
        (user_id, category, priority, province, district, description, photos, latitude, longitude, created_at, lang) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
        (uid, d['cat'], d['priority'], d['region'], d['district'], d['desc'], json.dumps(d['photos']), 
         m.location.latitude, m.location.longitude, datetime.now(), l), get_id=True)
    
    db_query("UPDATE users SET points = points + 5 WHERE user_id = ?", (uid,))
    await m.answer(TEXTS[l]['confirm'].format(rid), reply_markup=get_main_kb(uid, l))
    
    # Adminga
    for adm in ADMIN_IDS:
        try:
            if d['photos']: await bot.send_media_group(adm, [InputMediaPhoto(media=p) for p in d['photos']])
            await bot.send_message(adm, f"🆕 #{rid} | {d['priority']}\n📍 {d['region']}, {d['district']}\n📁 {d['cat']}\n📝 {d['desc']}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⚙️ Boshqarish", callback_data=f"view_{rid}")]]))
        except: pass
    await state.clear()

# --- ADMIN PANEL (MUHIM: BU QISM ISHLAYDI) ---
@dp.message(F.text.in_([TEXTS['uz']['btn_admin'], TEXTS['ru'].get('btn_admin', 'Admin'), TEXTS['en'].get('btn_admin', 'Admin')]))
async def admin_main(m: types.Message):
    if m.from_user.id not in ADMIN_IDS: return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Murojaatlar", callback_data="adm_reports_0")],
        [InlineKeyboardButton(text="📣 Broadcast", callback_data="adm_broadcast")],
        [InlineKeyboardButton(text="📥 Excel Export", callback_data="adm_export")]
    ])
    await m.answer("🔧 Admin boshqaruv paneli:", reply_markup=kb)

@dp.callback_query(F.data.startswith("adm_reports_"))
async def adm_view_list(c: types.CallbackQuery):
    offset = int(c.data.split("_")[2])
    reps = db_query("SELECT id, category, priority FROM reports ORDER BY id DESC LIMIT 5 OFFSET ?", (offset,), fetchall=True)
    if not reps:
        if offset == 0: await c.message.edit_text("Murojaatlar yo'q.")
        else: await c.answer("Boshqa murojaat yo'q.")
        return

    btns = [[InlineKeyboardButton(text=f"#{r[0]} | {r[1]} | {r[2]}", callback_data=f"view_{r[0]}")] for r in reps]
    nav = []
    if offset > 0: nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"adm_reports_{max(0, offset-5)}"))
    nav.append(InlineKeyboardButton(text="➡️", callback_data=f"adm_reports_{offset+5}"))
    btns.append(nav)
    btns.append([InlineKeyboardButton(text="🏠 Menu", callback_data="adm_home")])
    
    await c.message.edit_text("Murojaatlar ro'yxati:", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns))

@dp.callback_query(F.data.startswith("view_"))
async def adm_view_detail(c: types.CallbackQuery):
    rid = c.data.split("_")[1]
    r = db_query("SELECT * FROM reports WHERE id = ?", (rid,), fetch=True)
    photos = json.loads(r[7])
    if photos:
        try: await bot.send_media_group(c.from_user.id, [InputMediaPhoto(media=p) for p in photos])
        except: pass
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟡 Ko'rilmoqda", callback_data=f"st_Process_{rid}"), InlineKeyboardButton(text="✅ Hal etildi", callback_data=f"st_Done_{rid}")],
        [InlineKeyboardButton(text="✍️ Javob yozish", callback_data=f"reply_{rid}")],
        [InlineKeyboardButton(text="📍 Lokatsiya", callback_data=f"loc_{r[8]}_{r[9]}")]
    ])
    msg = f"🆔 ID: #{r[0]}\n👤 Foydalanuvchi: {r[1]}\n🚩 {r[3]}\n📍 {r[4]}, {r[5]}\n📁 {r[2]}\n📝 {r[6]}\n🔄 Status: {r[10]}\n💬 Javob: {r[11]}"
    await bot.send_message(c.from_user.id, msg, reply_markup=kb)

@dp.callback_query(F.data.startswith("reply_"))
async def adm_reply_begin(c: types.CallbackQuery, state: FSMContext):
    await state.update_data(report_id=c.data.split("_")[1])
    await state.set_state(AdminAction.waiting_reply_text)
    await c.message.answer("Ushbu murojaat uchun matnli javob kiriting:")

@dp.message(AdminAction.waiting_reply_text)
async def adm_reply_submit(m: types.Message, state: FSMContext):
    d = await state.get_data()
    db_query("UPDATE reports SET admin_reply = ? WHERE id = ?", (m.text, d['report_id']))
    u = db_query("SELECT user_id FROM reports WHERE id = ?", (d['report_id'],), fetch=True)
    try:
        await bot.send_message(u[0], f"📩 **Sizning #{d['report_id']} murojaatingizga javob:**\n\n{m.text}")
        await m.answer("✅ Javob foydalanuvchiga yuborildi.")
    except: pass
    await state.clear()

@dp.callback_query(F.data.startswith("st_"))
async def adm_change_status(c: types.CallbackQuery):
    _, st, rid = c.data.split("_")
    db_query("UPDATE reports SET status = ? WHERE id = ?", (st, rid))
    u = db_query("SELECT user_id, lang FROM reports WHERE id = ?", (rid,), fetch=True)
    if st == "Done": db_query("UPDATE users SET points = points + 10 WHERE user_id = ?", (u[0],))
    try: await bot.send_message(u[0], TEXTS[u[1]].get('status_upd', 'Update').format(rid, st))
    except: pass
    await c.answer(f"Status: {st}")

@dp.callback_query(F.data.startswith("loc_"))
async def adm_see_loc(c: types.CallbackQuery):
    _, lat, lon = c.data.split("_")
    await bot.send_location(c.from_user.id, float(lat), float(lon))
    await c.answer()

@dp.callback_query(F.data == "adm_home")
async def adm_home(c: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📚 Murojaatlar", callback_data="adm_reports_0")], [InlineKeyboardButton(text="📣 Broadcast", callback_data="adm_broadcast")], [InlineKeyboardButton(text="📥 Excel Export", callback_data="adm_export")]])
    await c.message.edit_text("🔧 Admin Panel", reply_markup=kb)

# --- BROADCAST ---
@dp.callback_query(F.data == "adm_broadcast")
async def adm_broadcast_start(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminAction.broadcast_msg)
    await c.message.answer("Barcha foydalanuvchilarga yuboriladigan matnni yozing:")

@dp.message(AdminAction.broadcast_msg)
async def adm_broadcast_send(m: types.Message, state: FSMContext):
    users = db_query("SELECT user_id FROM users", fetchall=True)
    for u in users:
        try: 
            await bot.send_message(u[0], f"📢 **Rasmiy bildirishnoma:**\n\n{m.text}")
            await asyncio.sleep(0.05)
        except: pass
    await m.answer("✅ Xabar tarqatildi.")
    await state.clear()

# --- STATISTIKA VA EKSPORT ---
@dp.message(F.text.in_([TEXTS['uz']['btn_stats'], TEXTS['ru'].get('btn_stats', 'Stats'), TEXTS['en'].get('btn_stats', 'Stats')]))
async def view_stats(m: types.Message):
    u = db_query("SELECT points FROM users WHERE user_id = ?", (m.from_user.id,), fetch=True)
    total = db_query("SELECT COUNT(*) FROM reports", fetch=True)[0]
    done = db_query("SELECT COUNT(*) FROM reports WHERE status='Done'", fetch=True)[0]
    await m.answer(f"👤 Ballingiz: {u[0] if u else 0}\n📊 Jami murojaatlar: {total}\n✅ Hal etilgan: {done}")

@dp.callback_query(F.data == "adm_export")
async def adm_export(c: types.CallbackQuery):
    conn = sqlite3.connect('mahalla_platform.db')
    pd.read_sql_query("SELECT * FROM reports", conn).to_excel("platform_data.xlsx", index=False)
    await c.message.answer_document(FSInputFile("platform_data.xlsx"))

# --- BOSHQALAR ---
@dp.message(F.text.in_([TEXTS['uz']['btn_my_reports'], TEXTS['ru'].get('btn_my_reports'), TEXTS['en'].get('btn_my_reports')]))
async def view_my_reps(m: types.Message):
    reps = db_query("SELECT id, category, status, admin_reply FROM reports WHERE user_id = ? ORDER BY id DESC LIMIT 5", (m.from_user.id,), fetchall=True)
    if not reps: return await m.answer("Sizda murojaatlar mavjud emas.")
    for r in reps:
        await m.answer(f"🆔 #{r[0]} | {r[1]}\n🔄 Status: {r[2]}\n💬 Admin javobi: {r[3]}")

@dp.message(F.text.in_([TEXTS['uz']['btn_help'], TEXTS['ru'].get('btn_help'), TEXTS['en'].get('btn_help')]))
async def view_guide(m: types.Message):
    await m.answer(TEXTS[g_lang(m.from_user.id)]['guide'], parse_mode="Markdown")

@dp.message(F.text.in_([TEXTS['uz']['btn_lang'], TEXTS['ru'].get('btn_lang'), TEXTS['en'].get('btn_lang'), "🌐 Language"]))
async def ch_lang_menu(m: types.Message):
    await m.answer("Tilni tanlang:", reply_markup=get_lang_kb())

async def reminder_loop():
    while True:
        overdue = db_query("SELECT id FROM reports WHERE status = 'Yangi' AND created_at < ?", (datetime.now() - timedelta(hours=48),), fetchall=True)
        if overdue:
            for r in overdue:
                for adm in ADMIN_IDS:
                    try: await bot.send_message(adm, f"⚠️ Eslatma: #{r[0]} murojaat kutilmoqda (48h+).")
                    except: pass
        await asyncio.sleep(3600 * 12)

async def main():
    asyncio.create_task(reminder_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())