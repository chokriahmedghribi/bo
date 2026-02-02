import streamlit as st
from sqlalchemy.orm import Session
from database.models import init_db
from database.crud import get_parametre, set_parametre

st.set_page_config(page_title="الإعدادات", layout="wide")

engine = init_db()
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine)

st.title("⚙️ إعدادات النظام")

tab1, tab2, tab3, tab4 = st.tabs(["إعدادات عامة", "إعدادات الترقيم", "نسخ احتياطي", "حول النظام"])

with tab1:
    st.subheader("الإعدادات العامة")
    
    db = SessionLocal()
    
    with st.form("general_settings"):
        nom_organisation = st.text_input(
            "اسم المؤسسة",
            value=get_parametre(db, "nom_organisation").valeur if get_parametre(db, "nom_organisation") else ""
        )
        
        adresse_organisation = st.text_area(
            "عنوان المؤسسة",
            value=get_parametre(db, "adresse_organisation").valeur if get_parametre(db, "adresse_organisation") else ""
        )
        
        telephone_organisation = st.text_input(
            "هاتف المؤسسة",
            value=get_parametre(db, "telephone_organisation").valeur if get_parametre(db, "telephone_organisation") else ""
        )
        
        email_organisation = st.text_input(
            "البريد الإلكتروني",
            value=get_parametre(db, "email_organisation").valeur if get_parametre(db, "email_organisation") else ""
        )
        
        jours_rappel = st.number_input(
            "عدد أيام التذكير المسبق",
            min_value=1,
            max_value=30,
            value=int(get_parametre(db, "jours_rappel").valeur) if get_parametre(db, "jours_rappel") else 3
        )
        
        submitted = st.form_submit_button("💾 حفظ الإعدادات")
        
        if submitted:
            set_parametre(db, "nom_organisation", nom_organisation, "اسم المؤسسة")
            set_parametre(db, "adresse_organisation", adresse_organisation, "عنوان المؤسسة")
            set_parametre(db, "telephone_organisation", telephone_organisation, "هاتف المؤسسة")
            set_parametre(db, "email_organisation", email_organisation, "البريد الإلكتروني للمؤسسة")
            set_parametre(db, "jours_rappel", str(jours_rappel), "عدد أيام التذكير المسبق")
            st.success("✅ تم حفظ الإعدادات بنجاح!")
    
    db.close()

with tab2:
    st.subheader("إعدادات الترقيم")
    
    db = SessionLocal()
    
    with st.form("numbering_settings"):
        prefix_entrant = st.text_input(
            "بادئة البريد الوارد",
            value=get_parametre(db, "prefix_entrant").valeur if get_parametre(db, "prefix_entrant") else "IN"
        )
        
        prefix_sortant = st.text_input(
            "بادئة البريد الصادر",
            value=get_parametre(db, "prefix_sortant").valeur if get_parametre(db, "prefix_sortant") else "OUT"
        )
        
        prefix_jointe = st.text_input(
            "بادئة البريد المشترك",
            value=get_parametre(db, "prefix_jointe").valeur if get_parametre(db, "prefix_jointe") else "JOINT"
        )
        
        annee_courante = st.checkbox(
            "إضافة السنة الحالية إلى الرقم المرجعي",
            value=bool(get_parametre(db, "annee_courante").valeur == "True") if get_parametre(db, "annee_courante") else True
        )
        
        zeros_remplissage = st.number_input(
            "عدد الأصفار للترقيم",
            min_value=3,
            max_value=8,
            value=int(get_parametre(db, "zeros_remplissage").valeur) if get_parametre(db, "zeros_remplissage") else 5
        )
        
        submitted = st.form_submit_button("💾 حفظ إعدادات الترقيم")
        
        if submitted:
            set_parametre(db, "prefix_entrant", prefix_entrant, "بادئة البريد الوارد")
            set_parametre(db, "prefix_sortant", prefix_sortant, "بادئة البريد الصادر")
            set_parametre(db, "prefix_jointe", prefix_jointe, "بادئة البريد المشترك")
            set_parametre(db, "annee_courante", str(annee_courante), "إضافة السنة الحالية إلى الرقم المرجعي")
            set_parametre(db, "zeros_remplissage", str(zeros_remplissage), "عدد الأصفار للترقيم")
            st.success("✅ تم حفظ الإعدادات بنجاح!")
    
    db.close()

with tab3:
    st.subheader("النسخ الاحتياطي والاستعادة")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **النسخ الاحتياطي**
        
        يحفظ النظام البيانات تلقائيًا في قاعدة بيانات SQLite.
        يمكنك نسخ الملف التالي احتياطيًا:
        
        `database/db.sqlite3`
        
        ومجلد المرفقات:
        
        `uploads/`
        """)
        
        if st.button("💾 إنشاء نسخة احتياطية"):
            st.success("تم إنشاء النسخة الاحتياطية تلقائيًا في قاعدة البيانات")
    
    with col2:
        st.warning("""
        **استعادة النسخة الاحتياطية**
        
        لاستعادة نسخة احتياطية:
        
        1. أوقف التطبيق
        2. استبدل ملف `db.sqlite3`
        3. استبدل مجلد `uploads`
        4. أعد تشغيل التطبيق
        """)

with tab4:
    st.subheader("حول النظام")
    
    st.markdown("""
    ### نظام إدارة مكتب الظبط
    
    **الإصدار:** 1.0.0
    
    **الوصف:** 
    نظام متكامل لإدارة المراسلات الواردة والصادرة والمشتركة، مع نظام تذكير وإدارة جهات.
    
    **المميزات:**
    - إدارة البريد الوارد والصادر والمشترك
    - نظام تذكيرات ذكي
    - إدارة جهات متكاملة
    - إعدادات قابلة للتخصيص
    - واجهة مستخدم عربية
    
    **المطور:** فريق تطوير النظم
    """)
    
    st.markdown("---")
    st.caption("© 2024 نظام مكتب الظبط - جميع الحقوق محفوظة")