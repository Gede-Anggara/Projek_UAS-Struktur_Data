# DSS Penentuan Lokasi Bisnis
> Sistem berbasis **_Weighted Undirected Graph_** & **Algoritma Dijkstra**, implementasi menggunakan **Python** + **Streamlit** untuk merekomendasikan bisnis terbaik di Wilayah **Bali, Indonesia**.

## Anggota Kelompok
- I Gede Anggara Suryantara | 2501010013 (Koordinator)
- Anak Agung Gede Anom Rangga Pratama | 2501010017

## Link Presentasi & Video Demo
Link Presentasi: https://canva.link/56na9l2afi61fti
Link Video Demo: https://drive.google.com/drive/folders/1jt2rUWuThSnxnVI5nRb_VVPAM7SDJPMp?usp=sharing

---

## BAB 1 - Pendahuluan

### 1.1 Latar Belakang
Pemilihan lokasi bisnis merupakan salah satu keputusan strategis yang berdampak besar terhadap keberhasilan usaha. Di wilayah Bali yang memiliki karakteristik pasar beragam, seorang calon pengusaha perlu mempertimbangkan berbagai faktor secara bersamaan, seperti potensi pasar, biaya sewa, tingkat persaingan, dan aksesibilitas kawasan.
<br> <br>
Pendekatan konvensional yang mengandalkan intuisi saja sering kali kurang optimal karena tidak mampu merepresentasikan hubungan geografis antar kawasan secara formal. Struktur data _graph_ hadir sebagai solusi yang tepat: Setiap lokasi dimodelkan sebagai _node_, sedangkan konektivitas antar kawasan direpresentasikan sebagai _edge_ berbobot (jarak dalam km).

### 1.2 Rumusan Masalah
- Bagaimana cara merepresentasikan hubungan antar kawasan di Bali menggunakan struktur data _graph_?
- Bagaimana cara menghitung skor kelayakan lokasi berdasarkan kriteria bisnis yang dapat dikonfigurasi?
- Bagaimana menentukan jalur terpendek antar kawasan menggunakan algoritma Dijkstra?

### 1.3 Tujuan
- Membangun DSS berbasis _weighted undirected graph_ untuk merekomendasikan lokasi bisnis di Bali.
- Mengimplementasikan algoritma Dijkstra untuk analisis aksesibilitas antar kawasan.
- Menyediakan antarmuka interaktif berbasis Streamlit yang memungkinkan konfigurasi bobot kriteria secara dinamis.

### 1.4 Manfaat
- Memberikan rekomendasi lokasi yang objektif dan berbasis data kepada calon pengusaha.
- Mmebantu pengguna memahami _trade-off_ antar kawasan melalui visualisasi _graph_ interaktif.
- Menjadi contoh implementasi nyata struktur data _graph_ dalam mengambil keputusan bisnis.

---

## BAB 2 - Dasar Teori

### 2.1 Struktur Data _Graph_
_Graph_ adalah struktur data _non-linier_ yang terdiri dari himpunan _node_ (_vertex_) dan _edge_. Secara formal, _graph_ G = (V,E) yang di mana V adalah himpunan _node_ dan E adalah himpunan _edge_ yang menghubungkan pasangan _node_.
<br><br>
Dalam proyek ini digunakan _Weighted Undirected Graph_, yaitu _graph_ tanpa arah dengan bobot pada setiap _edge_. Setiap _edge_ merepresentasikan jarak (km) antara dua kawasan. _Graph_ direpresentasikan menggunakan _Adjacency List_ untuk efisiensi memori, serta _Adjacency Matrix_ untuk keperluan visualisasi.

### 2.2 _Decision Support System_ (DSS)
DSS adalah sistem informasi berbasis komputer yang membantu mengambil keputusan dalam memilih alternatif terbaik dari sejumlah pilihan yang ada. DSS mengintegrasikan data, model analitis, dan antarmuka pengguna untuk menghasilkan rekomendasi yang dapat dipertanggungjawabkan.
<br><br>
Dalam sistem ini, DSS menggunakan metode _weighted scoring_: Setiap kriteria (potensi pasar, biaya sewa, kompetitor, aksesibilitas) diberi bobot yang dapat dikonfigurasi, kemudian skor total dihitung dan lokasi diurutkan berdasarkan nilai tertinggi.

### 2.3 Algoritma Dijkstra
Djikstra adalah algoritma pencarian jalur terpendek pada _graph_ berbobot non-negatif yang dikembangkan oleh Edsger W. Dijkstra pada 1956. Algoritma ini bekerja dengan prinsip _greedy_: Selalu memilih _node_ dengan jarak kumulatif terkecil dari antrian prioritas.
<br><br>
Kompleksitas waktu dengan implementasi _min-heap_ (_priority queue_) adalah O((V + E) log V), di mana V adalah jumlah _node_ dan E adalah jumlah _edge_. Kompleksitas ruang adalah O(V + E).
<br><br>
_Pseudocode_ Dijkstra yang diimplementasikan:
```text
DIJKSTRA(G, s):
  dist[s] = 0; dist[v] = ∞ untuk semua v ≠ s
  Q = priority_queue dengan (0, s)
  while Q tidak kosong:
    (d, u) = Q.pop_min()
    if u sudah dikunjungi: continue
    tandai u sebagai dikunjungi
    for setiap tetangga v dari u:
      if dist[u] + w(u,v) < dist[v]:
      dist[v] = dist[u] + w(u,v)
      prev[v] = u
      Q.push((dist[v], v))
```

---

## BAB 3 - Analisis & Perancangan

### 3.1 Analisis Masalah
Permasalahan pemilihan lokasi bisnis di Bali dapat dimodelkan sebagai _graph_ karena memiliki dua komponen utama yang sesuai dengan sifat _graph_:

-	Node: 24 kawasan di Bali, masing-masing memiliki atribut berupa potensi pasar (1–10), biaya sewa (juta/bulan), jumlah kompetitor, dan aksesibilitas (1–10).
-	Edge: konektivitas jalan antar kawasan dengan bobot berupa jarak dalam kilometer, bersifat dua arah (_undirected_).

_Graph_ dipilih sebagai struktur data utama karena mampu merepresentasikan hubungan spasial antar kawasan secara alami dan mendukung penerapan algoritma jalur terpendek untuk analisis aksesibilitas.

### 3.2  Desain _Graph_
Desain _node_ menggunakan _dictionary_ Python dengan kunci nama kawasan dan nilai berupa atribut bisnis. Desain _edge_ menggunakan _adjacency list_ (_dictionary of lists_) untuk efisiensi operasi traversal.

**Atribut _Node_**
| Atribut | Tipe | Keterangan |
|---|---|---|
| potensi_pasar | float (1–10) | Potensi pasar kawasan |
| biaya_sewa | float (juta/bln) | Biaya sewa bulanan |
| kompetitor | int | Jumlah kompetitor di kawasan |
| aksesibilitas | float (1–10) | Kemudahan akses ke kawasan |
| keterangan | string | Deskripsi singkat kawasan |

**Statistik _Graph Default_**
| Komponen | Nilai |
|---|---|
| Jumlah _Node_ (kawasan) | 24 |
| Jumlah _Edge_ (koneksi) | 46 |
| Jenis _Graph_ | _Weighted Undirected Graph_ |
| Representasi Utama | _Adjacency List_ |
| Representasi Alternatif |	_Adjacency Matrix_ |

### 3.3  Formula _Scoring_
Skor setiap lokasi dihitung menggunakan weighted scoring dengan normalisasi sebagai berikut:
```python
skor_pasar      = potensi_pasar                   # sudah skala 1–10
skor_sewa       = max(0, 10 - biaya_sewa / 5)     # sewa murah = skor tinggi
skor_kompetitor = max(0, 10 - jumlah_kompetitor)  # sedikit kompetitor = skor tinggi
skor_akses      = aksesibilitas                   # sudah skala 1–10

skor_total = (w1*skor_pasar + w2*skor_sewa + w3*skor_kompetitor + w4*skor_akses)
           / (w1 + w2 + w3 + w4) * 10
```
### 3.4  Struktur File Proyek
```
dss-lokasi-bisnis/
├── app.py           # Entry point Streamlit, UI & routing tab
├── grafik.py        # Logika graph: node, edge, Dijkstra, scoring
├── visualisasi.py   # Render Plotly: graph interaktif & heatmap matrix
└── default_data.py  # Dataset 24 kawasan Bali + 46 koneksi jalan
```

---

## BAB 4 - Implementasi

### 4.1  Implementasi Struktur Data _Graph_
_Graph_ diimplementasikan menggunakan dua _dictionary global_ di grafik.py: adjacency_list untuk representasi relasi antar _node_, dan node_data untuk menyimpan atribut setiap kawasan.
```python
# grafik.py — Struktur data utama
adjacency_list = {}  # { 'Kuta': [('Seminyak', 4.0), ('Legian', 2.0), ...] }
node_data      = {}  # { 'Kuta': { potensi_pasar: 9.5, biaya_sewa: 35, ... } }

# ── Operasi Node ──────────────────────────────────────────
def tambah_node(nama, potensi_pasar, biaya_sewa, kompetitor, aksesibilitas, ket):
    node_data[nama] = { 'potensi_pasar': potensi_pasar, ... }
    if nama not in adjacency_list:
        adjacency_list[nama] = []

def hapus_node(nama):
    node_data.pop(nama, None)
    adjacency_list.pop(nama, None)
    for n in adjacency_list:                    # hapus dari semua tetangga
        adjacency_list[n] = [(d,j) for d,j in adjacency_list[n] if d != nama]

# ── Operasi Edge ──────────────────────────────────────────
def tambah_edge(src, dst, jarak_km):            # undirected → dua arah
    if not any(d == dst for d, _ in adjacency_list[src]):
        adjacency_list[src].append((dst, jarak_km))
        adjacency_list[dst].append((src, jarak_km))
```

### 4.2  Implementasi Algoritma Dijkstra
Dijkstra diimplementasikan menggunakan modul heapq Python sebagai _min-heap_ (_priority queue_). Fungsi mengembalikan tiga nilai: _Dictionary_ jarak terpendek, _dictionary predecessor_ untuk rekonstruksi jalur, serta log proses perhitungan langkah demi langkah.
```python
import heapq

def dijkstra(start, end=None):
    jarak  = { n: float('inf') for n in node_data }
    sebelum = { n: None for n in node_data }
    jarak[start] = 0
    antrian = [(0, start)]                           # (cost, node)
    dikunjungi = set()

    while antrian:
        d_skrg, node_skrg = heapq.heappop(antrian)
        if node_skrg in dikunjungi: continue
        dikunjungi.add(node_skrg)
        if end and node_skrg == end: break           # early exit

        for tetangga, bobot in adjacency_list[node_skrg]:
            jarak_baru = d_skrg + bobot
            if jarak_baru < jarak[tetangga]:
                jarak[tetangga] = jarak_baru
                sebelum[tetangga] = node_skrg
                heapq.heappush(antrian, (jarak_baru, tetangga))

    return jarak, sebelum, log
```

### 4.3  Tampilan Sistem
Sistem dibangun dengan Streamlit dan terdiri dari 4 tab utama:
| Tab |	Fungsi |
|---|---|
| 📊 Rekomendasi	| Ranking semua lokasi berdasarkan _weighted scoring_ dengan detail lokasi terbaik |
| 🗺️ Visualisasi _Graph_	| Graf interaktif Plotly dengan I jalur terpendek dari lokasi terbaik |
| 🔍 Analisis Dijkstra	| Pencarian jalur terpendek antar kawasan dengan _log_ langkah demi langkah |
| 📋 Data & Representasi | Tabel _node_, _adjacency list_ teks, dan _heatmap adjacency matrix_ |

_Sidebar_ menyediakan konfigurasi bobot kriteria via _slider_, serta _form_ tambah/hapus _node_ dan _edge_ secara dinamis tanpa _reload_ aplikasi.

---

## BAB 5 - Pengujian & Analisis

### 5.1  Skenario Pengujian
**Skenario 1: Rekomendasi dengan Bobot _Default_** <br>
Input: bobot _default_ (potensi pasar 0.35, sewa 0.30, kompetitor 0.20, aksesibilitas 0.15) untuk jenis bisnis Kafe / _Coffee Shop_.
| Rank | Lokasi | Skor | Potensi Pasar | Kompetitor |
|---|---|---|---|---|
| 1 | Kuta	| 72.1 | 9.5 / 10	| 8 |
| 2	| Seminyak | 68.4	| 9.0 / 10 | 7 |
| 3	| Denpasar Selatan | 67.9	| 8.5 / 10 | 5 |

**Skenario 2: Prioritas Efisiensi Biaya** <br>
Input: bobot diubah menjadi efisiensi sewa 0.50, kompetitor 0.30, sisanya rendah, mensimulasikan bisnis _budget-focused_.
| Rank | Lokasi | Skor | Sewa (juta) | Kompetitor |
|---|---|---|---|---|
| 1 | Jembrana	| 71.3 | 7	| 1 |
| 2	| Gilimanuk | 69.8	| 6 | 1 |
| 3	| Bangli | 68.5	| 8 | 1 |

**Skenario 3: Dijkstra: Kuta ke Ubud** <br>
Jalur terpendek yang ditemukan algoritma:
> Kuta → Denpasar Barat → Denpasar Timur → Ubud
> Total jarak: 7.0 + 4.0 + 25.0 = 36.0 km <br>
Hasil ini benar secara logika geografis dan sesuai dengan data _edge_ yang telah didefinisikan.

### 5.2  Analisis Kompleksitas
| Operasi | Kompleksitas Waktu | Kompleksitas Ruang |
|---|---|---|
| tambah_node / hapus_node | O(V + E)	| O(1) amortized |
| tambah_edge / hapus_edge | O(degree)	| O(1) |
| hitung_skor	| O(1) | O(1) |
| ranking_semua | O(V log V) | O(V) |
| dijkstra (all nodes) | O((V+E) log V) | O(V+E) |
| buat_adjacency_matrix | O(V² + E) |	O(V²) |

Dengan V = 24 _node_ dan E = 46 _edge_, Dijkstra berjalan sangat cepat dalam praktiknya karena ukuran _graph_ relatif kecil.

### 5.3  Kelebihan dan Kekurangan Sistem
**Kelebihan**
-	_Graph_ secara alami merepresentasikan hubungan geografis antar kawasan.
-	Sistem bersifat dinamis: _node_ dan _edge_ dapat ditambah/hapus tanpa restart aplikasi.
-	Bobot kriteria dapat dikonfigurasi sesuai kebutuhan bisnis spesifik pengguna.
-	Tersedianya _log_ perhitungan Dijkstra per langkah menjadikan sistem ini tidak hanya sebagai alat bantu keputusan, tetapi juga media pembelajaran algoritma graf.
-	Telah di-_deploy_ ke Streamlit Cloud sehingga dapat diakses secara online.

**Kekurangan**
-	Data _node_ bersifat statis (_hardcoded_); belum terintegrasi dengan sumber data _real-time_.
-	_Scoring_ menggunakan model _linear_ sederhana, belum mempertimbangkan interaksi antar kriteria.
-	_State graph_ hilang saat aplikasi di-_refresh_ karena tidak menggunakan _persistent storage_.

---

## BAB 6 - Kesimpulan

### 6.1  Kesimpulan
Proyek ini berhasil membangun DSS Penentuan Lokasi Bisnis berbasis _Weighted Undirected Graph_ dan algoritma Dijkstra. Beberapa poin utama yang dapat disimpulkan:
-	Struktur data _graph_ terbukti efektif untuk merepresentasikan hubungan geografis antar 24 kawasan di Bali dengan 46 koneksi jalan, mendukung analisis pasial yang tidak dapat dilakukan oleh struktur data _linier_.
-	Algoritma Dijkstra dengan implementasi _min-heap_ memberikan solusi jalur terpendek yang optimal dengan kompleksitas O((V+E) log V), cukup efisien untuk skala _graph_ yang digunakan.
-	Metode _weighted scoring_ yang dapat dikonfigurasi pengguna membuat sistem adaptif terhadap berbagai jenis bisnis dengan prioritas kriteria yang berbeda-beda.
-	Antarmuka Streamlit yang interaktif memungkinkan pengguna untuk tidak hanya melihat hasil rekomendasi, tetapi juga memahami proses perhitungan algoritma secara _step-by-step_.
  
### 6.2  Saran Pengembangan
-	Integrasi API data _real-time_ (seperti Lamudi atau Rumah123) agar data biaya sewa selalu terbarui.
-	Penambahan algoritma Floyd-Warshall untuk menghitung semua pasangan jalur terpendek sekaligus, berguna untuk analisis aksesibilitas jaringan secara menyeluruh.
-	Implementasi _database persistant_ (SQLite atau PostgreSQL) agar perubahan data _node_ dan _edge_ tersimpan antara sesi pengguna.
-	Penambahan fitur _machine learning_ sederhana (_regresi_ atau _clustering_) untuk memperkuat rekomendasi berdasarkan data historis keberhasilan bisnis per kawasan.
