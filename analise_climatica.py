"""
Análise Climática - Curitiba, 2003
Dados: 17/02/2003 a 11/10/2003
Estação: 83842 - INMET
"""

import pandas as pd

# ─────────────────────────────────────────────
# 1. Leitura e limpeza dos dados
# ─────────────────────────────────────────────

df = pd.read_csv(
    "dados_83842_D_2003-02-17_2003-10-11.csv",
    sep=";",
    skiprows=10,
    header=0,
    encoding="latin-1",
    decimal=","
)

df.columns = ["Data", "Precipitacao_mm", "Temp_Max_C", "Temp_Min_C"]

# Converter data e remover linhas inválidas
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y", errors="coerce")
df = df.dropna(subset=["Data"]).reset_index(drop=True)

# Converter colunas numéricas (já com decimal=",")
for col in ["Precipitacao_mm", "Temp_Max_C", "Temp_Min_C"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ─────────────────────────────────────────────
# 2. RANKING 1 — Temperaturas mínimas (menor → maior)
# ─────────────────────────────────────────────

rank_min = (
    df[["Data", "Temp_Min_C"]]
    .dropna()
    .sort_values("Temp_Min_C", ascending=True)
    .reset_index(drop=True)
)
rank_min.index += 1
rank_min.index.name = "Rank"
rank_min["Data"] = rank_min["Data"].dt.strftime("%d/%m/%Y")
rank_min.columns = ["Data", "Temp. Mínima (°C)"]

# ─────────────────────────────────────────────
# 3. RANKING 2 — Temperaturas máximas (menor → maior)
# ─────────────────────────────────────────────

rank_max = (
    df[["Data", "Temp_Max_C"]]
    .dropna()
    .sort_values("Temp_Max_C", ascending=True)
    .reset_index(drop=True)
)
rank_max.index += 1
rank_max.index.name = "Rank"
rank_max["Data"] = rank_max["Data"].dt.strftime("%d/%m/%Y")
rank_max.columns = ["Data", "Temp. Máxima (°C)"]

# ─────────────────────────────────────────────
# 4. RANKING 3 — Precipitação (maior → menor, todos os dias)
# ─────────────────────────────────────────────

rank_prec = (
    df[["Data", "Precipitacao_mm"]]
    .sort_values("Precipitacao_mm", ascending=False)
    .reset_index(drop=True)
)
rank_prec.index += 1
rank_prec.index.name = "Rank"
rank_prec["Data"] = rank_prec["Data"].dt.strftime("%d/%m/%Y")
rank_prec.columns = ["Data", "Precipitação (mm)"]

# ─────────────────────────────────────────────
# 5. RANKING 4 — Temperatura média diária (maior → menor)
# ─────────────────────────────────────────────

df_media = df.copy()
df_media["Temp_Media_C"] = (df_media["Temp_Min_C"] + df_media["Temp_Max_C"]) / 2

rank_media = (
    df_media[["Data", "Temp_Min_C", "Temp_Max_C", "Temp_Media_C"]]
    .dropna()
    .sort_values("Temp_Media_C", ascending=False)
    .reset_index(drop=True)
)
rank_media.index += 1
rank_media.index.name = "Rank"
rank_media["Data"] = rank_media["Data"].dt.strftime("%d/%m/%Y")
rank_media.columns = ["Data", "Temp. Mínima (°C)", "Temp. Máxima (°C)", "Temp. Média (°C)"]

# ─────────────────────────────────────────────
# 6. Impressão dos resultados
# ─────────────────────────────────────────────

separador = "=" * 65

print(separador)
print(" ANÁLISE CLIMÁTICA — CURITIBA, 2003")
print(" Estação 83842 | 17/02/2003 a 11/10/2003")
print(separador)

print("\n📉 RANKING 1 — Temperaturas Mínimas (menor → maior)\n")
print(rank_min.to_string())

print(f"\n{separador}")
print("\n📈 RANKING 2 — Temperaturas Máximas (menor → maior)\n")
print(rank_max.to_string())

print(f"\n{separador}")
print("\n🌧️  RANKING 3 — Precipitação Diária (maior → menor)\n")
print(rank_prec.to_string())

print(f"\n{separador}")
print("\n🌡️  RANKING 4 — Temperatura Média Diária (maior → menor)")
print("    Média = (Temp. Mínima + Temp. Máxima) / 2\n")
print(rank_media.to_string())

print(f"\n{separador}")
print("\n📊 ESTATÍSTICAS GERAIS")
print(f"   Total de dias analisados : {len(df)}")
print(f"   Dias sem precipitação    : {(df['Precipitacao_mm'] == 0).sum()}")
print(f"   Dias com precipitação    : {(df['Precipitacao_mm'] > 0).sum()}")
print(f"   Temp. mínima absoluta    : {df['Temp_Min_C'].min():.1f} °C "
      f"({df.loc[df['Temp_Min_C'].idxmin(), 'Data'].strftime('%d/%m/%Y')})")
print(f"   Temp. máxima absoluta    : {df['Temp_Max_C'].max():.1f} °C "
      f"({df.loc[df['Temp_Max_C'].idxmax(), 'Data'].strftime('%d/%m/%Y')})")
print(f"   Maior precipitação       : {df['Precipitacao_mm'].max():.1f} mm "
      f"({df.loc[df['Precipitacao_mm'].idxmax(), 'Data'].strftime('%d/%m/%Y')})")
print(f"   Precip. total no período : {df['Precipitacao_mm'].sum():.1f} mm")
print(separador)

# ─────────────────────────────────────────────
# 7. Exportar tabelas em HTML interativo (Plotly)
# ─────────────────────────────────────────────
import plotly.graph_objects as go

def tabela_plotly(df_rank, titulo):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(df_rank.columns),
            fill_color="#2c3e50",
            font=dict(color="white", size=13),
            align="center"
        ),
        cells=dict(
            values=[df_rank[col] for col in df_rank.columns],
            fill_color=[["#f2f2f2" if i % 2 == 0 else "white"
                         for i in range(len(df_rank))]],
            font=dict(size=12),
            align="center",
            height=28
        )
    )])
    fig.update_layout(title=dict(text=titulo, font=dict(size=16)), margin=dict(t=60))
    return fig

tabelas = [
    (rank_min.reset_index(),  "Ranking — Temperaturas Mínimas (menor → maior)"),
    (rank_max.reset_index(),  "Ranking — Temperaturas Máximas (menor → maior)"),
    (rank_prec.reset_index(), "Ranking — Precipitação Diária (maior → menor)"),
    (rank_media.reset_index(),"Ranking — Temperatura Média Diária (maior → menor)"),
]

html_completo = "<html><head><meta charset='utf-8'><title>Análise Climática Curitiba 2003</title></head><body>"
for df_r, titulo in tabelas:
    fig = tabela_plotly(df_r, titulo)
    html_completo += fig.to_html(full_html=False, include_plotlyjs="cdn")
    html_completo += "<hr>"
html_completo += "</body></html>"

with open("analise_climatica.html", "w", encoding="utf-8") as f:
    f.write(html_completo)

print("\n✅ Arquivo 'analise_climatica.html' gerado — abra no navegador.")

import webbrowser, os
webbrowser.open("file://" + os.path.abspath("analise_climatica.html"))