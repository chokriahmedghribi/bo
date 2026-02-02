import streamlit as st
import sqlite3
import os
from datetime import datetime
from streamlit_option_menu import option_menu
import subprocess
import sys




# محاولة استيراد streamlit_option_menu مع معالجة الخطأ
try:
    from streamlit_option_menu import option_menu
    OPTION_MENU_AVAILABLE = True
except ImportError:
    OPTION_MENU_AVAILABLE = False
    st.error("⚠️ مكتبة streamlit-option-menu غير مثبتة. يرجى تثبيتها: pip install streamlit-option-menu")

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام مكتب الظبط",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# وظيفة بديلة لـ option_menu
def simple_menu(options, icons=None, default_index=0):
    with st.sidebar:
        st.markdown("### القائمة الرئيسية")
        selected = st.radio(
            "اختر الصفحة:",
            options,
            index=default_index,
            label_visibility="collapsed"
        )
    return selected

# تحميل تنسيق RTL
def load_css():
    css_file = "assets/rtl.css"
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # CSS افتراضي إذا لم يوجد الملف
        st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            direction: rtl;
            text-align: right;
        }
        </style>
        """, unsafe_allow_html=True)

load_css()

# إنشاء مجلدات إذا لم تكن موجودة
folders = ["uploads", "uploads/entrant", "uploads/sortant", 
           "uploads/jointe", "database", "assets", "templates"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# تهيئة قاعدة البيانات
try:
    from database.models import init_db
    init_db()
except Exception as e:
    st.warning(f"⚠️ تحذير في تهيئة قاعدة البيانات: {e}")

# القائمة الجانبية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=100)
    st.title("نظام مكتب الظبط")
    st.markdown("---")
    
    if OPTION_MENU_AVAILABLE:
        selected = option_menu(
            menu_title="القائمة الرئيسية",
            options=["الرئيسية", "البريد الوارد", "البريد الصادر", 
                    "البريد المشترك", "التذكير", "الجهات", "الإعدادات"],
            icons=["house", "inbox", "outbox", "envelope", "bell", "people", "gear"],
            menu_icon="menu-app",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "right", 
                           "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#2c3e50"},
            }
        )
    else:
        selected = simple_menu(
            ["الرئيسية", "البريد الوارد", "البريد الصادر", 
             "البريد المشترك", "التذكير", "الجهات", "الإعدادات"]
        )

# بقية الكود يبقى كما هو...
# إعدادات الصفحة
st.set_page_config(
    page_title="نظام مكتب الظبط",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحميل تنسيق RTL
def load_css():
    if os.path.exists("assets/rtl.css"):
        with open("assets/rtl.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# إنشاء مجلدات إذا لم تكن موجودة
os.makedirs("uploads", exist_ok=True)
os.makedirs("database", exist_ok=True)

# تهيئة قاعدة البيانات
from database.models import init_db
init_db()

# القائمة الجانبية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=100)
    st.title("نظام مكتب الظبط")
    st.markdown("---")
    
    selected = option_menu(
        menu_title="القائمة الرئيسية",
        options=["الرئيسية", "البريد الوارد", "البريد الصادر", "البريد المشترك", "التذكير", "الجهات", "الإعدادات"],
        icons=["house", "inbox", "outbox", "envelope", "bell", "people", "gear"],
        menu_icon="menu-app",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "right", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#2c3e50"},
        }
    )

# الصفحات
if selected == "الرئيسية":
    st.title("🏠 لوحة التحكم الرئيسية")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("البريد الوارد", "24", "+3")
    with col2:
        st.metric("البريد الصادر", "18", "+2")
    with col3:
        st.metric("البريد المشترك", "12", "+1")
    with col4:
        st.metric("التذكيرات", "8", "0")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 الإحصائيات الأخيرة")
        st.markdown("""
        - البريد الوارد غير المعالج: 5 وثائق
        - البريد الصادر المعلق: 3 وثائق
        - التذكيرات القريبة: 2 تذكير
        """)
    
    with col2:
        st.subheader("⚡ إجراءات سريعة")
        if st.button("📥 تسجيل بريد وارد جديد"):
            st.switch_page("pages/entrant.py")
        if st.button("📤 تسجيل بريد صادر جديد"):
            st.switch_page("pages/sortant.py")
        if st.button("🔔 إضافة تذكير جديد"):
            st.switch_page("pages/rappel.py")

elif selected == "البريد الوارد":
    st.switch_page("pages/entrant.py")
elif selected == "البريد الصادر":
    st.switch_page("pages/sortant.py")
elif selected == "البريد المشترك":
    st.switch_page("pages/jointe.py")
elif selected == "التذكير":
    st.switch_page("pages/rappel.py")
elif selected == "الجهات":
    st.switch_page("pages/contacts.py")
elif selected == "الإعدادات":
    st.switch_page("pages/parametre.py")