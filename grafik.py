import heapq

adjacency_list = {}
node_data = {}


# OPERASI NODE
def tambah_node(nama, potensi_pasar, biaya_sewa, kompetitor, aksesibilitas, keterangan=""):
    node_data[nama] = {
        "potensi_pasar": potensi_pasar,
        "biaya_sewa": biaya_sewa,
        "kompetitor": kompetitor,
        "aksesibilitas": aksesibilitas,
        "keterangan": keterangan
    }
    if nama not in adjacency_list:
        adjacency_list[nama] = []

def hapus_node(nama):
    node_data.pop(nama, None)

    adjacency_list.pop(nama, None)

    for n in adjacency_list:
        adjacency_list[n] = [(dst, j) for dst, j in adjacency_list[n] if dst != nama]

# OPERASI EDGE
def tambah_edge(src, dst, jarak_km):
    if src not in adjacency_list:
        adjacency_list[src] = []
    if dst not in adjacency_list:
        adjacency_list[dst] = []

    if not any(d == dst for d, _ in adjacency_list[src]):
        adjacency_list[src].append((dst, jarak_km))
    if not any(d == src for d, _ in adjacency_list[dst]):
        adjacency_list[dst].append((src, jarak_km))

def hapus_edge(src, dst):
    adjacency_list[src] = [(d, j) for d, j in adjacency_list[src] if d != dst]
    adjacency_list[dst] = [(d, j) for d, j in adjacency_list[dst] if d != src]

def get_semua_edge():
    seen = set()
    hasil = []
    for src, tetangga in adjacency_list.items():
        for dst, jarak in tetangga:
            key = tuple(sorted ([src, dst]))
            if key not in seen:
                seen.add(key)
                hasil.append((src, dst, jarak))
    return hasil

# SCORING LOKASI
def hitung_skor(nama, bobot):
    d = node_data[nama]

    skor_pasar = d["potensi_pasar"]
    skor_sewa = max(0, 10 - d["biaya_sewa"] / 5)
    skor_kompetitor = max(0, 10 - d["kompetitor"])
    skor_akses = d["aksesibilitas"]
    
    total_bobot = sum(bobot.values()) or 1
    skor = (
        bobot.get("potensi_pasar", 0) * skor_pasar +
        bobot.get("biaya_sewa", 0) * skor_sewa +
        bobot.get("kompetitor", 0) * skor_kompetitor +
        bobot.get("aksesibilitas", 0) * skor_akses
    ) / total_bobot * 10
    
    return round(skor, 2)

def ranking_semua(bobot):
    hasil = [(nama, hitung_skor(nama, bobot)) for nama in node_data]
    return sorted(hasil, key=lambda x: x[1], reverse=True)

# ALGORITMA DIJKSTRA
def dijkstra(start, end=None):
    jarak = {n: float('inf') for n in node_data}
    sebelum = {n: None for n in node_data}
    jarak[start] = 0
    sudah_dikunjungi = set()
    antrian = [(0, start)]
    log = []
    
    log.append(f"MULAI dari '{start}' | Jarak awal = 0")
    log.append(f"Semua node lain = ∞")
    log.append("=" * 45)
    
    langkah = 1
    while antrian:
        jarak_skrg, node_skrg = heapq.heappop(antrian)
        
        if node_skrg in sudah_dikunjungi:
            continue
        sudah_dikunjungi.add(node_skrg)
        
        log.append(f"\nLangkah {langkah}: Proses '{node_skrg}' (jarak_kumulatif = {jarak_skrg:.1f} km)")
        
        if end and node_skrg == end:
            log.append(f"✅ Tujuan '{end}' tercapai!")
            break
        
        for tetangga, bobot_edge, in adjacency_list.get (node_skrg, []):
            if tetangga in sudah_dikunjungi:
                continue
            
            jarak_baru = jarak_skrg + bobot_edge
            
            if jarak_baru < jarak[tetangga]:
                log.append(f"  → '{tetangga}': {jarak_skrg:.1f} + {bobot_edge:.1f} = {jarak_baru:.1f} km ✓ UPDATE")
                jarak[tetangga] = jarak_baru
                sebelum[tetangga] = node_skrg
                heapq.heappush(antrian, (jarak_baru, tetangga))
            else:
                log.append(f"  → '{tetangga}': {jarak_skrg:.1f} + {bobot_edge:.1f} = {jarak_baru:.1f} km (lewati, sudah ada jalur yang lebih pendek)")
        
        langkah += 1
    
    log.append(f"\n✅ Selesai. {len(sudah_dikunjungi)} node diproses.")
    return jarak, sebelum, log

def rekonstruksi_jalur(sebelum, start, end):
    jalur = []
    node = end
    while node is not None:
        jalur.append(node)
        node = sebelum.get(node)
    jalur.reverse()
    if jalur and jalur[0] == start:
        return jalur
    return []

# ADJACENCY MATRIX (Representasi alternatif)
def buat_adjacency_matrix():
    nodes = list(node_data.keys())
    n = len(nodes)
    indeks = {nama: i for i, nama in enumerate(nodes)}
    matrix = [[0.0] * n for _ in range(n)]
    
    for src, tetangga in adjacency_list.items():
        for dst, jarak in tetangga:
            if src in indeks and dst in indeks:
                matrix[indeks[src]][indeks[dst]] = jarak
                
    return nodes, matrix