# tests/smoke_test.py
# Oddiy smoke-test: muhit o'zgaruvchilarini o'rnatib, main modulini import qiladi
# va DB ichida kerakli jadvallar yaratilganini tekshiradi.

import os
import sys
import sqlite3
import importlib

# 1) Mühit o'zgaruvchilarini o'rnatish (lokal test uchun)
os.environ.setdefault('BOT_TOKEN', 'TEST_TOKEN_PLACEHOLDER')
os.environ.setdefault('DATA_DIR', './data_test')
os.environ.setdefault('ADMIN_IDS', '12345678')

# 2) DATA_DIR oldindan yaratiladi (agar main.py ham yaratmasa)
os.makedirs(os.environ['DATA_DIR'], exist_ok=True)

# 3) Import main modulini yuklash (bu init_db() ni chaqiradi)
try:
    # Agar modul allaqachon import qilingan bo'lsa, qayta yuklaymiz
    if 'main' in sys.modules:
        importlib.reload(sys.modules['main'])
        main = sys.modules['main']
    else:
        main = importlib.import_module('main')
except Exception as e:
    print('ERROR: main modulini import qilishda xato:', e)
    sys.exit(2)

# 4) DB faylining mavjudligini tekshirish
db_path = getattr(main, 'DB_PATH', None)
if not db_path:
    print('ERROR: main.DB_PATH topilmadi.')
    sys.exit(3)

print('DB_PATH:', db_path)
if not os.path.isfile(db_path):
    print('Xato: DB fayli topilmadi — init_db() chaqirilmagan yoki DATA_DIR noto\'g\'ri.')
    sys.exit(4)

# 5) Jadval(lar) borligini tekshirish
try:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = [r[0] for r in cur.fetchall()]
    print('DB jadvallari:', rows)
    expected = {'users', 'reports'}
    if expected.issubset(set(rows)):
        print('OK: Kerakli jadvallar mavjud.')
        sys.exit(0)
    else:
        print(f'Xato: Kerakli jadvallar topilmadi. Kutilyapti: {expected}')
        sys.exit(5)
except Exception as e:
    print('ERROR: DB bilan ishlashda xato:', e)
    sys.exit(6)
finally:
    try:
        conn.close()
    except Exception:
        pass
