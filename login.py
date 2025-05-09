import streamlit as st
from db import get_connection
import time

def show_login():

    # Inisialisasi session state login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "page" not in st.session_state:
        st.session_state.page = "login"

    ## Jika pengguna sudah login, langsung alihkan ke halaman utama
   # if st.session_state.logged_in:
        st.info(f"Anda sudah login sebagai {st.session_state.username}.")
     #   time.sleep(1.5)  # waktu tunggu sebelum redirect (dalam detik)
     #   st.switch_page("dashboard.py")  # pastikan halaman dashboard ada
     #   return

    # Jika belum login, tampilkan form login
    st.subheader("Silakan Login untuk Melanjutkan")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if username and password:
                try:
                    with get_connection() as conn:
                        # Jika koneksi menggunakan sqlite3, pastikan row_factory sudah diatur
                        # conn.row_factory = sqlite3.Row  <-- Bisa diatur di get_connection() atau di sini
                        cursor = conn.cursor()  # Hilangkan parameter dictionary=True
                        cursor.execute(
                            "SELECT * FROM user WHERE username = ? AND password = ?",
                            (username, password)
                        )
                        user = cursor.fetchone()
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.username = user['username']  # akses dengan key
                            st.success("Login berhasil! ")
                            time.sleep(1.5)
                            st.session_state.page = "dashboard"
                            st.rerun()
                            #time.sleep(1.5)  # waktu tunggu sebelum redirect (dalam detik)
                            #st.switch_page("dashboard.py")
                        else:
                            st.error("Username atau password salah.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat login: {e}")
            else:
                st.warning("Harap isi username dan password.")
            
