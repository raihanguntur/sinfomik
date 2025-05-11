import streamlit as st
from dashboard import show_dashboard
from siswa import show_siswa
from nilai import show_nilai
from login import show_login
from logout import show_logout

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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

# Define navigation
NAV_ITEMS = {
    "dashboard": {"label": "🏠 Dashboard", "show": True},
    "siswa": {"label": "👨‍🎓 Siswa", "show": "logged_in"},
    "nilai": {"label": "📝 Nilai", "show": "logged_in"},
    "login": {"label": "🚪 Login", "show": "not_logged_in"},
    "logout": {"label": "🚪 Logout", "show": "logged_in"}
}

for key, item in NAV_ITEMS.items():
    show_item = True
    if isinstance(item["show"], str):
        if item["show"] == "logged_in":
            show_item = st.session_state.get("logged_in", False)
        elif item["show"] == "not_logged_in":
            show_item = not st.session_state.get("logged_in", False)
    
    if show_item:
        nav_button(item["label"], key)

# Page routing
PAGE_HANDLERS = {
    "dashboard": show_dashboard,
    "siswa": show_siswa,
    "nilai": show_nilai,
    "login": show_login,
    "logout": show_logout
}

page = st.session_state.page

try:
    # Check authentication for protected pages
    if page in ["siswa", "nilai", "logout"] and not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        st.session_state.page = "login"
        st.rerun()
    
    # Show the page
    if page in PAGE_HANDLERS:
        PAGE_HANDLERS[page]()
    else:
        st.error("Halaman tidak ditemukan.")

except Exception as e:
    st.error(f"Terjadi kesalahan: {str(e)}")
    st.stop()