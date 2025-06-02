import streamlit as st

from dashboard import show_dashboard
from siswa import show_siswa
from nilai import show_nilai
from login import show_login
from logout import show_logout
from semester import show_semester

# Set default page on first load
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# Sidebar layout
st.sidebar.title("📚 Navigasi")

def nav_button(label, key):
    is_active = st.session_state.page == key
    button_style = f"""
        <style>
        div[data-testid="stSidebar"] button#{key} {{
            background-color: {'#4ade80' if is_active else '#f0f0f0'} !important;
            color: {'black' if is_active else '#333'} !important;
            width: 100%;
            text-align: left;
            margin-bottom: 4px;
            border-radius: 6px;
        }}
        </style>
    """
    st.sidebar.markdown(button_style, unsafe_allow_html=True)
    if st.sidebar.button(label, key=key, use_container_width=True):
        st.session_state.page = key

# Define sidebar buttons
# Sidebar buttons berdasarkan status login
nav_button("🏠 Dashboard", "dashboard")
if st.session_state.get("logged_in", False):
    nav_button("👨‍🎓 Siswa", "siswa")
    nav_button("📝 Nilai", "nilai")
    nav_button("📅 Semester", "semester")
    nav_button("🚪 Logout", "logout")
else:
    nav_button("🚪 Login", "login")


# Page routing
page = st.session_state.page

# Pastikan status login diinisialisasi
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if page == "login":
    show_login()
elif page == "logout":
    if st.session_state.logged_in:
        show_logout()
    else:
        st.warning("Silakan login terlebih dahulu.")
        st.session_state.page = "login"
        st.rerun()
elif page == "siswa":
    if st.session_state.logged_in:
        show_siswa()
    else:
        st.warning("Silakan login terlebih dahulu.")
        st.session_state.page = "login"
        st.rerun()
elif page == "nilai":
    if st.session_state.logged_in:
        show_nilai()
    else:
        st.warning("Silakan login terlebih dahulu.")
        st.session_state.page = "login"
        st.rerun()
elif page == "semester":
    if st.session_state.logged_in:
        show_semester()
    else:
        st.warning("Silakan login terlebih dahulu.")
        st.session_state.page = "login"
        st.rerun()
elif page == "dashboard":
    show_dashboard()  # dashboard bisa diakses siapa saja
else:
    st.error("Halaman tidak ditemukan.")