import networkx as nx
import plotly.graph_objects as go

def gambar_graph(node_data, adjacency_list, skor_dict, jalur_highlight=None, node_terbaik=None):
    if not node_data:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text="Belum ada lokasi.", x=0.5, y=0.5,
                              xref="paper", yref="paper", showarrow=False,
                              font=dict(size=16, color="#888"))]
        )
        return fig
    
    G = nx.Graph()
    G.add_nodes_from(node_data.keys())
    seen = set()
    for src, tetangga in adjacency_list.items():
        for dst, jarak in tetangga:
            key = tuple(sorted([src, dst]))
            if key not in seen:
                seen.add(key)
                G.add_edge(src, dst, weight=jarak)

    pos = nx.spring_layout(G, seed=42, k=1.5)

    edge_jalur = set()
    jalur_highlight = jalur_highlight or []
    for i in range(len(jalur_highlight) - 1):
        a, b = jalur_highlight[i], jalur_highlight[i + 1]
        edge_jalur.add((a, b))
        edge_jalur.add((b, a))

    traces = []

    for src, dst, jarak in [(u, v, d["weight"]) for u, v, d in G.edges(data=True)]:
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        is_jalur = (src, dst) in edge_jalur

        traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode="lines",
            line=dict(
                color="#F59E0B" if is_jalur else "#475569",
                width=4 if is_jalur else 1.5
            ),
            hoverinfo="none",
            showlegend=False,
        ))

        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        traces.append(go.Scatter(
            x=[mx], y=[my],
            mode="text",
            text=[f"{jarak:.1f} km"],
            textfont=dict(size=9, color="#94A3B8"),
            hoverinfo="none",
            showlegend=False,
        ))

    node_x, node_y = [], []
    node_labels = []
    node_hover = []
    node_warna = []
    node_ukuran = []

    for nama in node_data:
        x, y = pos[nama]
        node_x.append(x)
        node_y.append(y)
        node_labels.append(nama)

        d = node_data[nama]
        skor = skor_dict.get(nama, 0)
        node_hover.append(
            f"<b>{nama}</b><br>"
            f"Skor: {skor:.1f}/100<br>"
            f"Potensi Pasar: {d['potensi_pasar']}/10<br>"
            f"Sewa: Rp{d['biaya_sewa']:.0f}jt/bln<br>"
            f"Kompetitor: {d['kompetitor']}<br>"
            f"Aksesibilitas: {d['aksesibilitas']}/10"
        )

        if nama == node_terbaik:
            warna = "#F59E0B"
        elif nama in jalur_highlight:
            warna = "#3B82F6"
        else:
            rasio = skor / 100
            r = int(239 - rasio * 180)
            g = int(68 + rasio * 120)
            b = 68
            warna = f"rgb({r},{g},{b})"

        node_warna.append(warna)
        node_ukuran.append(20 + skor / 5)

    traces.append(go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=node_labels,
        textposition="top center",
        textfont=dict(size=11, color="#E2E8F0"),
        marker=dict(
            size=node_ukuran,
            color=node_warna,
            line=dict(color="#1E293B", width=2),
        ),
        hovertext=node_hover,
        hoverinfo="text",
        showlegend=False,
    ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        hovermode="closest",
    )
    return fig

def gambar_adjancency_matrix(nodes, matrix):
    if not nodes:
        return go.Figure()
    
    label_sel = [[f"{v:.1f}" if v > 0 else "-" for v in baris] for baris in matrix]

    fig = go.Figure(go.Heatmap(
        z=matrix,
        x=nodes,
        y=nodes,
        text=label_sel,
        texttemplate="%{text}",
        colorscale="Blues",
        showscale=True,
        colorbar=dict(title="km"),
        hovertemplate="Dari: %{y}<br>Ke: %{x}<br>Jarak: %{z:.1f} km<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
        margin=dict(l=10, r=10, t=30, b=10),
        height=380,
        xaxis=dict(tickangle=-35),
    )
    return fig