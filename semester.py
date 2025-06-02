import streamlit as st
import pandas as pd

from db import get_connection, init_db

def show_semester():
    init_db()
    st.title("📅 Semester")

    conn = get_connection()
    c = conn.cursor()

    # Add new semester
    with st.form("add_semester_form"):
        tahun_ajaran = st.text_input("Tahun Ajaran (misalnya 2024/2025)")
        nama = st.selectbox("Semester", ["Ganjil", "Genap"])
        submitted = st.form_submit_button("Tambah Semester")
        if submitted and tahun_ajaran:
            
            c.execute("SELECT id FROM tahun_ajaran WHERE th_ajar = ?", (tahun_ajaran,))
            th_ajar = c.fetchone()
            if not th_ajar:
                c.execute("INSERT INTO tahun_ajaran (th_ajar) VALUES (?)", (tahun_ajaran,))
                conn.commit()
                th_ajar_id = c.lastrowid
            else:
                th_ajar_id = th_ajar["id"]

           
            c.execute("SELECT id FROM semester_pil WHERE sm_pil = ?", (nama,))
            sm_pil = c.fetchone()
            if not sm_pil:
                c.execute("INSERT INTO semester_pil (sm_pil) VALUES (?)", (nama,))
                conn.commit()
                sm_pil_id = c.lastrowid
            else:
                sm_pil_id = sm_pil["id"]

           
            c.execute("INSERT INTO semester (th_ajar_id, sm_pil_id, nama) VALUES (?, ?, ?)",
                      (th_ajar_id, sm_pil_id, nama))
            conn.commit()
            st.success("Semester berhasil ditambahkan!")
            st.rerun()

    # Show list of tahun ajaran
    st.subheader("Daftar Tahun Ajaran")
    t_ajaran = c.execute("SELECT id, th_ajar FROM tahun_ajaran ORDER BY id DESC").fetchall()

    if t_ajaran:
        df = pd.DataFrame(t_ajaran, columns=["ID", "Tahun Ajaran"])
        df.set_index("ID", inplace=True)
        st.table(df)
    else:
        st.info("Belum ada data tahun ajaran.")

    st.divider()

    # Show list of semesters
    st.subheader("Daftar Semester")
    query = '''
        SELECT s.id, ta.th_ajar, sp.sm_pil, s.nama, s.aktif
        FROM semester s
        JOIN tahun_ajaran ta ON s.th_ajar_id = ta.id
        JOIN semester_pil sp ON s.sm_pil_id = sp.id
        ORDER BY s.id DESC
    '''
    semesters = c.execute(query).fetchall()

    if semesters:
        df = pd.DataFrame(semesters, columns=["ID", "Tahun Ajaran", "Semester Pilihan", "Nama", "Aktif"])
        df["Aktif"] = df["Aktif"].apply(lambda x: "✅ Ya" if x else "—")
        df.set_index("ID", inplace=True)
        st.table(df)
    else:
        st.info("Belum ada data semester.")
