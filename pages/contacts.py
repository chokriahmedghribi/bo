import streamlit as st
from sqlalchemy.orm import Session
from database.models import init_db, Contact
from database.crud import (
    create_contact, get_contacts, get_contact,
    update_contact, delete_contact
)
import pandas as pd

st.set_page_config(page_title="إدارة الجهات", layout="wide")

engine = init_db()
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine)

st.title("📇 إدارة الجهات والمراسلين")

tab1, tab2, tab3 = st.tabs(["إضافة جهة", "قائمة الجهات", "بحث وتعديل"])

with tab1:
    st.subheader("إضافة جهة جديدة")
    
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("اسم الجهة*")
            type_contact = st.selectbox(
                "نوع الجهة",
                ["جهة حكومية", "شركة خاصة", "فرد", "منظمة", "آخر"]
            )
            telephone = st.text_input("رقم الهاتف")
            
        with col2:
            email = st.text_input("البريد الإلكتروني")
            adresse = st.text_area("العنوان")
        
        notes = st.text_area("ملاحظات إضافية")
        
        submitted = st.form_submit_button("💾 حفظ الجهة")
        
        if submitted:
            if not nom:
                st.error("الرجاء إدخال اسم الجهة")
            else:
                db = SessionLocal()
                contact_data = {
                    "nom": nom,
                    "type_contact": type_contact,
                    "telephone": telephone,
                    "email": email,
                    "adresse": adresse,
                    "notes": notes
                }
                
                try:
                    create_contact(db, **contact_data)
                    st.success("✅ تم حفظ الجهة بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
                finally:
                    db.close()

with tab2:
    st.subheader("قائمة الجهات المسجلة")
    
    db = SessionLocal()
    contacts = get_contacts(db)
    db.close()
    
    if contacts:
        data = []
        for c in contacts:
            data.append({
                "الاسم": c.nom,
                "النوع": c.type_contact,
                "الهاتف": c.telephone,
                "البريد الإلكتروني": c.email,
                "العنوان": c.adresse[:50] + "..." if c.adresse and len(c.adresse) > 50 else c.adresse,
                "ملاحظات": c.notes[:30] + "..." if c.notes and len(c.notes) > 30 else c.notes
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # تصدير البيانات
        st.download_button(
            label="📥 تصدير إلى Excel",
            data=df.to_csv(index=False).encode('utf-8-sig'),
            file_name="الجهات.csv",
            mime="text/csv"
        )
    else:
        st.info("لا توجد جهات مسجلة")

with tab3:
    st.subheader("بحث وتعديل الجهات")
    
    search_term = st.text_input("🔍 بحث باسم الجهة")
    
    if search_term:
        db = SessionLocal()
        contacts = db.query(Contact).filter(Contact.nom.contains(search_term)).all()
        
        if contacts:
            for contact in contacts:
                with st.expander(f"📌 {contact.nom}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_nom = st.text_input("الاسم", value=contact.nom, key=f"nom_{contact.id}")
                        new_type = st.text_input("النوع", value=contact.type_contact, key=f"type_{contact.id}")
                        new_phone = st.text_input("الهاتف", value=contact.telephone, key=f"phone_{contact.id}")
                    
                    with col2:
                        new_email = st.text_input("البريد الإلكتروني", value=contact.email, key=f"email_{contact.id}")
                        new_address = st.text_area("العنوان", value=contact.adresse, key=f"addr_{contact.id}")
                    
                    new_notes = st.text_area("ملاحظات", value=contact.notes, key=f"notes_{contact.id}")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("💾 تحديث", key=f"update_{contact.id}"):
                            update_data = {
                                "nom": new_nom,
                                "type_contact": new_type,
                                "telephone": new_phone,
                                "email": new_email,
                                "adresse": new_address,
                                "notes": new_notes
                            }
                            update_contact(db, contact.id, **update_data)
                            st.success("تم التحديث بنجاح")
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("🗑️ حذف", key=f"delete_{contact.id}"):
                            delete_contact(db, contact.id)
                            st.success("تم الحذف بنجاح")
                            st.rerun()
        else:
            st.warning("لم يتم العثور على نتائج")
        db.close()