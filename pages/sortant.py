import streamlit as st
from datetime import datetime
import os
from sqlalchemy.orm import Session
from database.models import init_db, Sortant, Contact
from database.crud import create_sortant, get_sortants, get_contacts
import pandas as pd

st.set_page_config(page_title="البريد الصادر", layout="wide")

engine = init_db()
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine)

st.title("📤 إدارة البريد الصادر")

tab1, tab2 = st.tabs(["تسجيل بريد صادر", "قائمة البريد الصادر"])

with tab1:
    st.subheader("تسجيل بريد صادر جديد")
    
    with st.form("sortant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            reference = st.text_input("رقم المرجع*")
            date_envoi = st.date_input("تاريخ الإرسال*", datetime.now())
            type_document = st.selectbox(
                "نوع الوثيقة",
                ["مراسلة", "مذكرة", "تقرير", "قرار", "تعميم", "آخر"]
            )
            moyen_envoi = st.selectbox(
                "وسيلة الإرسال",
                ["بريد", "فاكس", "بريد إلكتروني", "تسليم يدوي", "آخر"]
            )
            
        with col2:
            db = SessionLocal()
            contacts = get_contacts(db)
            db.close()
            
            contact_names = [c.nom for c in contacts]
            destinataire_nom = st.selectbox("المستلم", [""] + contact_names)
            
            if destinataire_nom == "":
                destinataire_nom = st.text_input("أدخل اسم المستلم (إذا غير موجود)")
            
            statut = st.selectbox("الحالة", ["مسودة", "مرسل", "مؤرشف"])
        
        objet = st.text_area("الموضوع*", height=100)
        fichier_joint = st.file_uploader("رفع ملف مرفق", type=['pdf', 'doc', 'docx'])
        notes = st.text_area("ملاحظات الإرسال")
        
        submitted = st.form_submit_button("💾 حفظ البريد الصادر")
        
        if submitted:
            if not reference or not objet:
                st.error("الرجاء ملء جميع الحقول الإلزامية (*)")
            else:
                fichier_path = None
                if fichier_joint:
                    upload_dir = "uploads/sortant"
                    os.makedirs(upload_dir, exist_ok=True)
                    fichier_path = f"{upload_dir}/{reference}_{fichier_joint.name}"
                    with open(fichier_path, "wb") as f:
                        f.write(fichier_joint.getbuffer())
                
                db = SessionLocal()
                destinataire_id = None
                
                if destinataire_nom and destinataire_nom != "":
                    # البحث عن الجهة في قاعدة البيانات
                    existing_contact = db.query(Contact).filter(Contact.nom == destinataire_nom).first()
                    
                    if existing_contact:
                        destinataire_id = existing_contact.id
                    else:
                        # إنشاء جهة جديدة
                        new_contact = Contact(
                            nom=destinataire_nom,
                            type_contact="غير محدد"
                        )
                        db.add(new_contact)
                        db.commit()
                        db.refresh(new_contact)
                        destinataire_id = new_contact.id
                
                sortant_data = {
                    "reference": reference,
                    "date_envoi": date_envoi,
                    "type_document": type_document,
                    "destinataire_id": destinataire_id,
                    "objet": objet,
                    "fichier_joint": fichier_path,
                    "moyen_envoi": moyen_envoi,
                    "statut": statut,
                    "notes": notes
                }
                
                try:
                    create_sortant(db, **sortant_data)
                    st.success("✅ تم حفظ البريد الصادر بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())
                finally:
                    db.close()

with tab2:
    st.subheader("قائمة البريد الصادر")
    
    db = SessionLocal()
    sortants = get_sortants(db)
    
    if sortants:
        data = []
        for s in sortants:
            # جلب اسم المستلم إذا كان موجودًا
            destinataire_name = "غير محدد"
            if s.destinataire_id:
                contact = db.query(Contact).filter(Contact.id == s.destinataire_id).first()
                if contact:
                    destinataire_name = contact.nom
            
            data.append({
                "المرجع": s.reference,
                "تاريخ الإرسال": s.date_envoi,
                "المستلم": destinataire_name,
                "الموضوع": s.objet[:50] + "..." if len(s.objet) > 50 else s.objet,
                "وسيلة الإرسال": s.moyen_envoi,
                "الحالة": s.statut
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # إحصاءات
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("إجمالي المراسلات", len(df))
        with col2:
            st.metric("مرسل", len(df[df["الحالة"] == "مرسل"]))
        with col3:
            st.metric("مسودة", len(df[df["الحالة"] == "مسودة"]))
    else:
        st.info("لا توجد سجلات للبريد الصادر")
    
    db.close()