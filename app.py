import streamlit as st
import pandas as pd
import grafik as ge
from visualisasi import gambar_graph, gambar_adjancency_matrix
from default_data import DEFAULT_NODES, DEFAULT_EDGES

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="DSS Lokasi Bisnis",
    page_icon="🗺️",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Space+Mono&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans'}, sans-serif; }
.stApp { background: #0F172A; color: #E2E8F0; }
[data-testid="stSidebar"] { background: #1E293B !important; border-right: 1px solid #334155; }
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
.stButton > button {
    background: linear-gradient(135deg, #3B82F6, #6366F1) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
}
[data-testid="stMetric"] {
    background: #1E293B; border: 1px solid #334155;
    border-radius: 12px; padding: 1rem;
}
[data-testid="stMetricValue"] { color: #38BDF8 !important; font-family: 'Space Mono' !important; }
input, textarea { background: #1E293B !important; color: #E2E8F0 !important; border: 1px solid #334155 !important; }
.log-box {
    background: #0F172A; border-left: 3px solid #3B82F6;
    padding: .5rem 1rem; border-radius: 0 8px 8px 0;
    font-family: 'Space Mono', monospace; font-size: .78rem;
    color: #94A3B8; white-space: pre-wrap; margin: .25rem 0;
}
</style>
""", unsafe_allow_html=True)

# INISIALISASI DATA (HANYA SEKALI SAAT PERTAMA BUKA)
if "siap" not in st.session_state:
    for args in DEFAULT_NODES:
        ge.tambah_node(*args)
    for src, dst, jarak, _ in DEFAULT_EDGES:
        ge.tambah_edge(src, dst, jarak)
    st.session_state.siap = True

if "jenis_bisnis" not in st.session_state:
    st.session_state.jenis_bisnis = "Kafe / Coffee Shop"

if "bobot" not in st.session_state:
    st.session_state.bobot = {
        "potensi_pasar": 0.35,
        "biaya_sewa": 0.30,
        "kompetitor": 0.20,
        "aksesibilitas": 0.15,
    }

# SIDEBAR
with st.sidebar:
    st.markdown("## ⚙️ Konfigurasi")

    st.session_state.jenis_bisnis = st.text_input(
        "Jenis Bisnis", value=st.session_state.jenis_bisnis
    )

    st.markdown("### Bobot Prioritas Kriteria")
    st.caption("Geser sesuai prioritas bisnis kamu")

    b = st.session_state.bobot
    b["potensi_pasar"] = st.slider("📈 Potensi Pasar", 0.0, 1.0, b["potensi_pasar"], 0.05)
    b["biaya_sewa"] = st.slider("💰 Efisiensi Sewa", 0.0, 1.0, b["biaya_sewa"], 0.05)
    b["kompetitor"] = st.slider("⚔️ Hindari Kompetitor", 0.0, 1.0, b["kompetitor"], 0.05)
    b["aksesibilitas"] = st.slider("🚗 Aksesibilitas", 0.0, 1.0, b["aksesibilitas"], 0.05)

    total = sum(b.values())
    if abs(total - 1.0) > 0.05:
        st.warning(f"Total bobot: {total:.2f} (sebaiknya = 1.0)")
    else:
        st.success(f"Total bobot: {total:.2f} ✓")

    st.divider()

    # Form tambah node
    st.markdown("## ➕ Tambah Lokasi")
    with st.form("form_tambah_node", clear_on_submit=True):
        nama = st.text_input("Nama Lokasi", placeholder="misal: Canggu")
        pasar = st.slider("Potensi Pasar (1–10)", 1.0, 10.0, 7.0, 0.5)
        sewa = st.number_input("Biaya Sewa (juta/bln)", 1.0, 100.0, 20.0, 1.0)
        komp = st.number_input("Jumlah Kompetitor", 0, 20, 3, 1)
        akses = st.slider("Aksesibilitas (1–10)", 1.0, 10.0, 7.0, 0.5)
        ket = st.text_input("Keterangan (opsional)")

        if st.form_submit_button("Tambah Lokasi"):
            if not nama:
                st.error("Nama tidak boleh kosong!")
            elif nama in ge.node_data:
                st.error("Lokasi sudah ada!")
            else:
                ge.tambah_node(nama, pasar, sewa, int(komp), akses, ket)
                st.success(f"✓ '{nama}' ditambahkan")
                st.rerun()

    st.divider()

    # Form tambah edge
    nodes = list(ge.node_data.keys())
    if len(nodes) >= 2:
        st.markdown("## 🔗 Tambah Koneksi")
        with st.form("form_tambah_edge", clear_on_submit=True):
            src = st.selectbox("Dari", nodes)
            dst = st.selectbox("Ke", nodes)
            jarak = st.number_input("Jarak (km)", 0.1, 500.0, 5.0, 0.5)

            if st.form_submit_button("Tambah Koneksi"):
                if src == dst:
                    st.error("Pilih lokasi yang berbeda!")
                else:
                    ge.tambah_edge(src, dst, jarak)
                    st.success(f"✓ Koneksi {src} ↔ {dst} ditambahkan!")
                    st.rerun()
    
    st.divider()

    # Form hapus node
    if nodes:
        st.markdown("## 🗑️ Hapus Lokasi")
        with st.form("form_hapus", clear_on_submit=True):
            pilih = st.selectbox("Pilih lokasi", nodes)
            if st.form_submit_button("Hapus", type="secondary"):
                ge.hapus_node(pilih)
                st.success(f"'{pilih}' dihapus.")
                st.rerun()

    st.divider()
    if st.button("🔄 Reset ke Data Default"):
        ge.adjacency_list.clear()
        ge.node_data.clear()
        del st.session_state["siap"]
        st.rerun()

# HEADER

st.markdown("# 🗺️ DSS Penentuan Lokasi Bisnis")
st.markdown(
    "Sistem berbasis **Weighted Undirected Graph** + algoritma **Dijkstra** "
    "untuk merekomendasikan lokasi bisnis terbaik di wilayah Bali."
)
st.divider()

# TABS
nodes = list(ge.node_data.keys())

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Rekomendasi",
    "🗺️ Visualisasi Graph",
    "🔍 Analisis Dijkstra",
    "📋 Data & Representasi",
])

# TAB 1: REKOMENDASI
with tab1:
    if not nodes:
        st.info("Belum ada lokasi. Tambahkan melalui sidebar.")
    else:
        ranking = ge.ranking_semua(st.session_state.bobot)

        # Kartu ringkasan
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Jenis Bisnis", st.session_state.jenis_bisnis)
        col2.metric("Total Lokasi", len(nodes))
        col3.metric("Total Koneksi", len(ge.get_semua_edge()))
        col4.metric("Rekomendasi #1", ranking[0][0], f"Skor {ranking[0][1]:.1f}/100")

        st.divider()

        # Rekomendasi terbaik
        nama_terbaik, skor_terbaik = ranking[0]
        d = ge.node_data[nama_terbaik]
        st.success(f"### 🏆 Rekomendasi Terbaik: **{nama_terbaik}** — Skor {skor_terbaik:.1f}/100")
        st.markdown(f"> {d['keterangan'] or 'Tidak ada keterangan.'}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📈 Potensi Pasar", f"{d['potensi_pasar']}/10")
        c2.metric("💰 Biaya Sewa", f"Rp{d['biaya_sewa']:.0f}jt/bln")
        c3.metric("⚔️ Kompetitor", d["kompetitor"])
        c4.metric("🚗 Aksesibilitas", f"{d['aksesibilitas']}/10")

        st.divider()

        # Tabel ranking lengkap
        st.markdown("### 📋 Ranking Semua Lokasi")
        tabel = []
        for rank, (nama, skor) in enumerate(ranking, 1):
            d2 = ge.node_data[nama]
            tabel.append({
                "Rank": rank,
                "Lokasi": nama,
                "Skor (0–100)": skor,
                "Potensi Pasar": d2["potensi_pasar"],
                "Sewa (juta/bln)": d2["biaya_sewa"],
                "Kompetitor": d2["kompetitor"],
                "Akesibilitas": d2["aksesibilitas"],
            })
        st.dataframe(pd.DataFrame(tabel), use_container_width=True, hide_index=True)

# TAB 2: VISUALISASI GRAPH
with tab2:
    if not nodes:
        st.info("Belum ada node untuk divisualisasikan.")
    else:
        ranking = ge.ranking_semua(st.session_state.bobot)
        skor_map = {n: s for n, s in ranking}
        terbaik = ranking[0][0]

        # Pilihan highlight jalur
        col_a, col_b = st.columns(2)
        tampilkan_jalur = col_a.checkbox("Highlight jalur terpendek dari lokasi terbaik", value=True)
        tujuan_jalur = col_b.selectbox(
            "Tujuan jalur",
            [n for n in nodes if n != terbaik],
            disabled=not tampilkan_jalur,
        )

        jalur = []
        if tampilkan_jalur and tujuan_jalur:
            _, sebelum, _ = ge.dijkstra(terbaik, tujuan_jalur)
            jalur = ge.rekonstruksi_jalur(sebelum, terbaik, tujuan_jalur)

        fig = gambar_graph(
            ge.node_data, ge.adjacency_list, skor_map,
            jalur_highlight=jalur,
            node_terbaik=terbaik,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "🟡 Emas = rekomendasi terbaik | "
            "🟢–🔴 Warna = skor (hijau tinggi, merah rendah) | "
            "Edge emas = jalur terpendek aktif"
        )

# TAB 3: ANALISIS DIJKSTRA
with tab3:
    if len(nodes) < 2:
        st.info("Minimal 2 lokasi dan 1 koneksi diperlukan.")
    else:
        st.markdown("""
        **Dijkstra** adalah algoritma pencarian jalur terpendek pada graph berbobot.
        Dalam DSS ini, digunakan untuk menganalisis **aksesibilitas antar kawasan**,
        yang merupakan salah satu faktor penting dalam memilih lokasi bisnis.
        """)

        col1, col2 = st.columns(2)
        asal = col1.selectbox("📍 Lokasi Asal", nodes, key="d_asal")
        pilihan_tujuan = ["— Semua Lokasi —"] + [n for n in nodes if n != asal]
        tujuan = col2.selectbox("🎯 Lokasi Tujuan", pilihan_tujuan, key="d_tujuan")

        if st.button("▶ Jalankan Dijkstra"):
            end = None if tujuan == "— Semua Lokasi —" else tujuan
            jarak_map, sebelum, log = ge.dijkstra(asal, end)

            st.divider()

            # Tampilkan hasil
            if end:
                jalur = ge.rekonstruksi_jalur(sebelum, asal, end)
                total_km = jarak_map.get(end, float("inf"))
                if jalur:
                    st.success(f"**Jalur terpendek:** {' → '.join(jalur)}")
                    st.metric("Total Jarak", f"{total_km:.1f} km")
                else:
                    st.error(f"Tidak ada jalur dari '{asal}' ke '{end}'.")
            else:
                st.markdown(f"**Jarak terpendek dari '{asal}' ke semua lokasi:**")
                rows = []
                for n, km in jarak_map.items():
                    if n == asal:
                        continue
                    j = ge.rekonstruksi_jalur(sebelum, asal, n)
                    rows.append({
                        "Tujuan": n,
                        "Jarak (km)": f"{km:.1f}" if km != float("inf") else "∞",
                        "Jalur": " → ".join(j) if j else "-",
                    })
                df = pd.DataFrame(rows).sort_values("Jarak (km)")
                st.dataframe(df, use_container_width=True, hide_index=True)

            # Log langkah per langkah
            st.divider()
            with st.expander("📝 Lihat proses perhitungan step-by-step", expanded=True):
                for baris in log:
                    if not baris.strip():
                        continue
                    # pilih warna berdasarkan isi baris
                    if "MULAI" in baris or "=" * 5 in baris:
                        warna = "#38BDF8"
                    elif "Langkah" in baris:
                        warna = "#F59E0B"
                    elif "UPDATE" in baris or "✅" in baris:
                        warna = "#22C55E"
                    elif "Lewati" in baris:
                        warna = "#EF4444"
                    else:
                        warna = "#94A3B8"

                    st.markdown(
                        f'<div class="log-box" style="color:{warna}">{baris}</div>',
                        unsafe_allow_html=True,
                    )

            # Info kompleksitas
            st.divider()
            st.markdown("### 📐 Kompleksitas Algoritma")
            V = len(nodes)
            E = len(ge.get_semua_edge())
            c1, c2, c3 = st.columns(3)
            c1.metric("Jumlah Node (V)", V)
            c2.metric("Jumlah Edge (E)", E)
            c3.metric("Time Complexity", "O((V+E) log V)")
            st.caption(
                f"Dengan V={V} node dan E={E} edge menggunakan min-heap (priority queue). "
                f"Space complexity: **O(V+E)**."
            )

# TAB 4: DATA & REPRESENTASI
with tab4:
    sub1, sub2, sub3 = st.tabs(["📄 Data Node", "🔗 Adjacency List", "🔢 Adjacency Matrix"])

    with sub1:
        if not nodes:
            st.info("Belum ada data.")
        else:
            ranking = ge.ranking_semua(st.session_state.bobot)
            skor_map = {n: s for n, s in ranking}
            rows = [{
                "Lokasi": n,
                "Potensi Pasar": d["potensi_pasar"],
                "Sewa (juta/bln)": d["biaya_sewa"],
                "Kompetitor": d["kompetitor"],
                "Akesibilitas": d["aksesibilitas"],
                "Skor DSS": skor_map.get(n, 0),
                "Keterangan": d["keterangan"],
            } for n, d in ge.node_data.items()]
            df = pd.DataFrame(rows).sort_values("Skor DSS", ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)

    with sub2:
        col_1, col_r = st.columns(2)

        with col_1:
            st.markdown("**Adjacency List**")
            st.caption("Representasi utama graph dalam program")
            lines = []
            for nama in nodes:
                tetangga = ge.adjacency_list.get(nama, [])
                if tetangga:
                    isi = ", ".join([f"{d} ({j:.1f}km)" for d, j in tetangga])
                    lines.append(f"{nama}: [{isi}]")
                else:
                    lines.append(f"{nama}: []")
            st.code("\n".join(lines), language="text")

        with col_r:
            st.markdown("**Data Edge**")
            edges = ge.get_semua_edge()
            if edges:
                df_e = pd.DataFrame(
                    [(s, d, f"{j:.1f}") for s, d, j in edges],
                    columns=["Dari", "Ke", "Jarak (km)"]
                )
                st.dataframe(df_e, use_container_width=True, hide_index=True)
            else:
                st.info("Belum ada koneksi.")

    with sub3:
        node_list, matrix = ge.buat_adjacency_matrix()
        if node_list:
            st.plotly_chart(gambar_adjancency_matrix(node_list, matrix), use_container_width=True)
            with st.expander("Lihat dalam bentuk tabel"):
                df_m = pd.DataFrame(matrix, index=node_list, columns=node_list)
                st.dataframe(df_m.style.format("{:.1f}"), use_container_width=True)
        else:
            st.info("Belum ada data.")

st.divider()
st.caption("DSS Penentuan Lokasi Bisnis · Weighted Undirected Graph + Dijkstra")