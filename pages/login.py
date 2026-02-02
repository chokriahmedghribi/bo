import streamlit as st
from database.auth import authenticate




def login_page():
   st.markdown("## 🔐 تسجيل الدخول")
   
   
   username = st.text_input("اسم المستخدم")
   password = st.text_input("كلمة المرور", type="password")
   
   
   if st.button("دخول"):
      user = authenticate(username, password)
   if user:
      st.session_state.logged_in = True
      st.session_state.user = user.username
      st.session_state.role = user.role
      st.success("تم تسجيل الدخول بنجاح")
      st.experimental_rerun()
   else:
      st.error("بيانات الدخول غير صحيحة")