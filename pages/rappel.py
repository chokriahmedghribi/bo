import streamlit as st
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import init_db, Rappel
from database.crud import create_rappel, get_rappels
import pandas as pd

st.set_page_config(page_title="التذكيرات", layout="wide")

engine = init_db()
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine)

st.title("🔔 إدارة التذكيرات")

tab1, tab2 = st.tabs(["إضافة تذكير جديد", "قائمة التذكيرات"])

with tab1:
    st.subheader("إضافة تذكير جديد")
    
    with st.form("rappel_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            titre = st.text_input("عنوان التذكير*")
            date_rappel = st.date_input("تاريخ التذكير*", datetime.now() + timedelta(days=1))
            priorite = st.selectbox("الأولوية", ["منخفضة", "متوسطة", "عالية"])
            
        with col2:
            statut = st.selectbox("الحالة", ["معلق", "مكتمل", "ملغى"])
            document_lie = st.text_input("وثيقة مرتبطة (رقم المرجع)")
        
        description = st.text_area("وصف التذكير", height=150)
        
        submitted = st.form_submit_button("💾 حفظ التذكير")
        
        if submitted:
            if not titre:
                st.error("الرجاء إدخال عنوان التذكير")
            else:
                db = SessionLocal()
                rappel_data = {
                    "titre": titre,
                    "description": description,
                    "date_rappel": date_rappel,
                    "priorite": priorite,
                    "statut": statut,
                    "document_lie": document_lie
                }
                
                try:
                    create_rappel(db, **rappel_data)
                    st.success("✅ تم حفظ التذكير بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
                finally:
                    db.close()

with tab2:
    st.subheader("قائمة التذكيرات")
    
    db = SessionLocal()
    rappels = get_rappels(db)
    db.close()
    
    if rappels:
        today = datetime.now().date()
        
        # تصنيف التذكيرات
        rappels_urgents = [r for r in rappels if r.date_rappel <= today + timedelta(days=3) and r.statut == "معلق"]
        rappels_futurs = [r for r in rappels if r.date_rappel > today + timedelta(days=3) and r.statut == "معلق"]
        rappels_completes = [r for r in rappels if r.statut == "مكتمل"]
        
        st.subheader("⚠️ تذكيرات عاجلة (خلال 3 أيام)")
        if rappels_urgents:
            for r in rappels_urgents:
                days_left = (r.date_rappel - today).days
                color = "red" if days_left < 0 else "orange"
                st.warning(f"**{r.titre}** - {r.date_rappel} (متبقي {days_left} يوم)")
        else:
            st.info("لا توجد تذكيرات عاجلة")
        
        st.markdown("---")
        
        st.subheader("📅 تذكيرات مستقبلية")
        if rappels_futurs:
            data = []
            for r in rappels_futurs:
                data.append({
                    "العنوان": r.titre,
                    "التاريخ": r.date_rappel,
                    "الأولوية": r.priorite,
                    "الحالة": r.statut,
                    "الوصف": r.description[:50] + "..." if r.description and len(r.description) > 50 else r.description
                })
            st.dataframe(pd.DataFrame(data))
        else:
            st.info("لا توجد تذكيرات مستقبلية")
        
        st.markdown("---")
        
        st.subheader("✅ تذكيرات مكتملة")
        if rappels_completes:
            data = []
            for r in rappels_completes:
                data.append({
                    "العنوان": r.titre,
                    "تاريخ الإكمال": r.date_rappel,
                    "الوصف": r.description
                })
            st.dataframe(pd.DataFrame(data))
        else:
            st.info("لا توجد تذكيرات مكتملة")
    else:
        st.info("لا توجد تذكيرات")