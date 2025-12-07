# db.py
# ملف منفصل لإدارة قاعدة البيانات فقط

import sqlite3
import os
from flask import g

# تحديد المسار الصحيح لملف قاعدة البيانات داخل مجلد am
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "am.db")

def get_db():
    """فتح اتصال بقاعدة البيانات إن لم يكن مفتوحًا بالفعل"""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # يخلي النتائج في شكل dict
    return g.db

def close_db(e=None):
    """إغلاق الاتصال بقاعدة البيانات بعد الطلب"""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """إنشاء الجداول إذا لم تكن موجودة"""
    db = get_db()
    cur = db.cursor()

    # جدول المستخدمين
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # جدول الكتب
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            available BOOLEAN DEFAULT 1,
            timestamp TEXT
        )
    """)

    # جدول السلة
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    """)

    db.commit()
    print("✅ Database initialized successfully!")
