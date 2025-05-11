import streamlit as st
import sqlite3
from datetime import datetime

def show_nilai():
    st.title("📝 Rekap Nilai")
    
    # Cek login dan role
    if not st.session_state.get("logged_in", False) or st.session_state.get("role") != "guru":
        st.warning("Anda tidak memiliki akses ke halaman ini")
        return
    
    # Koneksi database
    conn = sqlite3.connect('sinfomik.db')
    cursor = conn.cursor()
    
    # 1. Ambil daftar kelas yang diajar guru ini
    cursor.execute("""
        SELECT DISTINCT k.id, k.nama_kelas 
        FROM guru_mapel_kelas gmk
        JOIN kelas k ON gmk.kelas_id = k.id
        WHERE gmk.user_id = ?
    """, (st.session_state.user_id,))
    
    kelas_options = cursor.fetchall()
    
    if not kelas_options:
        st.error("Anda belum ditugaskan mengajar kelas apapun")
        conn.close()
        return
    
    # 2. Pilih kelas
    selected_kelas = st.selectbox(
        "Pilih Kelas",
        options=[k[1] for k in kelas_options],
        key="select_kelas"
    )
    kelas_id = next(k[0] for k in kelas_options if k[1] == selected_kelas)

    # 3. Ambil mata pelajaran yang diajar
    cursor.execute("""
        SELECT mp.id, mp.nama_mapel
        FROM guru_mapel_kelas gmk
        JOIN mata_pelajaran mp ON gmk.mapel_id = mp.id
        WHERE gmk.user_id = ? AND gmk.kelas_id = ?
    """, (st.session_state.user_id, kelas_id))
    
    mapel_options = cursor.fetchall()
    
    if not mapel_options:
        st.error("Anda tidak mengajar mata pelajaran di kelas ini")
        conn.close()
        return

    selected_mapel = st.selectbox(
        "Pilih Mata Pelajaran",
        options=[m[1] for m in mapel_options],
        key="select_mapel"
    )
    mapel_id = next(m[0] for m in mapel_options if m[1] == selected_mapel)
    
    # 4. Ambil daftar siswa di kelas tersebut
    cursor.execute("""
        SELECT id, nisn, nama 
        FROM siswa 
        WHERE kelas_id = ?
        ORDER BY nama ASC
    """, (kelas_id,))
    
    siswa_kelas = cursor.fetchall()
    
    # 5. Form input nilai
    with st.form("input_nilai_form"):
        st.subheader(f"Input Nilai {selected_mapel} - Kelas {selected_kelas}")
        
        jenis_nilai = st.selectbox(
            "Jenis Penilaian",
            ["UTS", "UAS", "Harian", "Tugas", "Praktikum"],
            key="jenis_nilai"
        )
        
        nilai_siswa = {}
        for siswa in siswa_kelas:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{siswa[2]} (NISN: {siswa[1]})")
            with col2:
                nilai = st.number_input(
                    "Nilai",
                    min_value=0,
                    max_value=100,
                    value=75,
                    key=f"nilai_{siswa[0]}",
                    label_visibility="collapsed"
                )
                nilai_siswa[siswa[0]] = nilai
        
        submitted = st.form_submit_button("Simpan Nilai")
        
        if submitted:
            try:
                tanggal_hari_ini = datetime.now().strftime("%Y-%m-%d")
                for siswa_id, nilai in nilai_siswa.items():
                    # Cek duplikasi
                    cursor.execute("""
                        SELECT 1 FROM nilai 
                        WHERE siswa_id = ? 
                        AND mapel_id = ? 
                        AND jenis_nilai = ? 
                        AND tanggal = ?
                    """, (siswa_id, mapel_id, jenis_nilai, tanggal_hari_ini))
                    
                    if cursor.fetchone():
                        st.warning(f"Data nilai untuk {next(s[2] for s in siswa_kelas if s[0] == siswa_id)} sudah ada")
                        continue
                        
                    # Simpan jika belum ada
                    cursor.execute("""
                        INSERT INTO nilai (
                            siswa_id, mapel_id, jenis_nilai, 
                            nilai, tanggal, guru_id
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        siswa_id, mapel_id, jenis_nilai,
                        nilai, tanggal_hari_ini, st.session_state.user_id
                    ))
                
                conn.commit()
                st.success("✅ Nilai berhasil disimpan!")
                
            except sqlite3.Error as e:
                conn.rollback()
                st.error(f"❌ Gagal menyimpan nilai: {str(e)}")

    # 6. Tampilkan riwayat nilai LENGKAP
    st.divider()
    st.subheader("📋 Riwayat Nilai Lengkap")
    
    try:
        # Ambil semua nilai yang pernah diinput guru ini
        cursor.execute("""
            SELECT 
                s.nisn, s.nama,
                n.jenis_nilai, n.nilai, n.tanggal,
                mp.nama_mapel, k.nama_kelas
            FROM nilai n
            JOIN siswa s ON n.siswa_id = s.id
            JOIN mata_pelajaran mp ON n.mapel_id = mp.id
            JOIN kelas k ON s.kelas_id = k.id
            WHERE n.guru_id = ?
            ORDER BY n.tanggal DESC, s.nama ASC
        """, (st.session_state.user_id,))
        
        riwayat = cursor.fetchall()
        
        if riwayat:
            # Tampilkan filter
            st.write("**Filter Data:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_kelas = st.selectbox(
                    "Kelas",
                    ["Semua"] + sorted(list(set([r[6] for r in riwayat]))),
                    key="filter_kelas"
                )
            with col2:
                filter_mapel = st.selectbox(
                    "Mata Pelajaran",
                    ["Semua"] + sorted(list(set([r[5] for r in riwayat]))),
                    key="filter_mapel"
                )
            with col3:
                filter_jenis = st.selectbox(
                    "Jenis Nilai",
                    ["Semua"] + sorted(list(set([r[2] for r in riwayat]))),
                    key="filter_jenis"
                )
            
            # Apply filters
            filtered_data = []
            for row in riwayat:
                if (filter_kelas == "Semua" or row[6] == filter_kelas) and \
                   (filter_mapel == "Semua" or row[5] == filter_mapel) and \
                   (filter_jenis == "Semua" or row[2] == filter_jenis):
                    filtered_data.append(row)
            
            # Tampilkan dalam bentuk tabel HTML sederhana
            st.write("""
            <style>
            .nilai-table {
                width: 100%;
                border-collapse: collapse;
            }
            .nilai-table th, .nilai-table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            .nilai-table tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .nilai-table th {
                background-color: #4CAF50;
                color: white;
            }
            </style>
            
            <table class="nilai-table">
                <tr>
                    <th>NISN</th>
                    <th>Nama</th>
                    <th>Kelas</th>
                    <th>Mapel</th>
                    <th>Jenis</th>
                    <th>Nilai</th>
                    <th>Tanggal</th>
                </tr>
            """, unsafe_allow_html=True)
            
            for row in filtered_data:
                st.write(f"""
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[6]}</td>
                    <td>{row[5]}</td>
                    <td>{row[2]}</td>
                    <td>{row[3]}</td>
                    <td>{row[4]}</td>
                </tr>
                """, unsafe_allow_html=True)
            
            st.write("</table>", unsafe_allow_html=True)
            
            # Tampilkan jumlah data
            st.write(f"Menampilkan {len(filtered_data)} dari {len(riwayat)} data nilai")
        else:
            st.info("Belum ada data nilai yang tersimpan")
            
    except sqlite3.Error as e:
        st.error(f"Gagal memuat riwayat: {str(e)}")
    finally:
        conn.close()