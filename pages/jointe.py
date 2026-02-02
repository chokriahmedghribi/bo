import streamlit as st
from datetime import datetime
import os
from sqlalchemy.orm import Session
from database.models import init_db, Jointe
from database.crud import create_jointe, get_jointe
import pandas as pd

st.set_page_config(page_title="البريد المشترك", layout="wide")

engine = init_db()
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine)

st.title("📄 إدارة البريد المشترك")

tab1, tab2 = st.tabs(["تسجيل بريد مشترك", "قائمة البريد المشترك"])

with tab1:
    st.subheader("تسجيل بريد مشترك جديد")
    
    with st.form("jointe_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            reference = st.text_input("رقم المرجع*")
            date_document = st.date_input("تاريخ الوثيقة*", datetime.now())
            type_document = st.selectbox(
                "نوع الوثيقة",
                ["اتفاقية", "عقد", "محضر اجتماع", "تقرير مشترك", "آخر"]
            )
            
        with col2:
            parties = st.text_area("الأطراف المشتركة*", height=100)
        
        objet = st.text_area("موضوع الوثيقة*", height=100)
        fichier_joint = st.file_uploader("رفع ملف مرفق", type=['pdf', 'doc', 'docx', 'jpg', 'png'])
        notes = st.text_area("ملاحظات إضافية")
        
        submitted = st.form_submit_button("💾 حفظ البريد المشترك")
        
        if submitted:
            if not reference or not objet or not parties:
                st.error("الرجاء ملء جميع الحقول الإلزامية (*)")
            else:
                fichier_path = None
                if fichier_joint:
                    upload_dir = "uploads/jointe"
                    os.makedirs(upload_dir, exist_ok=True)
                    fichier_path = f"{upload_dir}/{reference}_{fichier_joint.name}"
                    with open(fichier_path, "wb") as f:
                        f.write(fichier_joint.getbuffer())
                
                db = SessionLocal()
                jointe_data = {
                    "reference": reference,
                    "date_document": date_document,
                    "type_document": type_document,
                    "parties": parties,
                    "objet": objet,
                    "fichier_joint": fichier_path,
                    "notes": notes
                }
                
                try:
                    create_jointe(db, **jointe_data)
                    st.success("✅ تم حفظ البريد المشترك بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
                finally:
                    db.close()

with tab2:
    st.subheader("قائمة البريد المشترك")
    
    db = SessionLocal()
    jointe_docs = get_jointe(db)
    db.close()
    
    if jointe_docs:
        data = []
        for j in jointe_docs:
            data.append({
                "المرجع": j.reference,
                "تاريخ الوثيقة": j.date_document,
                "الأطراف": j.parties[:50] + "..." if len(j.parties) > 50 else j.parties,
                "الموضوع": j.objet[:50] + "..." if len(j.objet) > 50 else j.objet,
                "النوع": j.type_document,
                "ملاحظات": j.notes[:30] + "..." if j.notes and len(j.notes) > 30 else j.notes
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("لا توجد سجلات للبريد المشترك")