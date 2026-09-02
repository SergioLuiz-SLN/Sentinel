"""
╔════════════════════════════════════════════════════════════════════════════╗
║  SENTINEL — COMMAND CENTER                                                ║
║  Real-Time Anomaly Detection Platform                                      ║
║  © 2024 SLN IT Solutions                                                   ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime


# ──────────────────── CONFIGURAÇÃO DA PÁGINA ──────────────────── #

st.set_page_config(
    page_title="Sentinel Command Center | SLN IT",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ──────────────────── FUNÇÕES UTILITÁRIAS ──────────────────── #

def corrigir_texto(texto: str) -> str:
    """Corrige logs antigos em UTF-8 interpretados como latin-1."""
    try:
        return texto.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return texto


def abreviar_volume(valor: float) -> str:
    """Formata valores grandes em notação abreviada."""
    if valor >= 1_000_000:
        return f"{valor / 1_000_000:.1f}M"
    if valor >= 1_000:
        return f"{valor / 1_000:.1f}K"
    return f"{valor:.0f}"


def calcular_desvio_percentual(atual: float, baseline: float) -> float:
    """Calcula desvio percentual em relação ao baseline."""
    return ((atual / baseline - 1) * 100) if baseline > 0 else 0


@st.cache_data(ttl=5)
def ler_log_processado():
    """Lê e processa o log do motor de detecção."""
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_log = os.path.join(raiz, "data", "log_sistema.txt")
    
    if not os.path.exists(caminho_log):
        return pd.DataFrame(), None
    
    with open(caminho_log, "r", encoding="utf-8") as arquivo:
        linhas = [corrigir_texto(linha.strip()) for linha in arquivo if linha.strip()]
    
    if not linhas:
        return pd.DataFrame(), None

    dados = []
    for linha in linhas[1:]:
        if "Serviço:" not in linha:
            continue
        try:
            partes = linha.split(" | ")
            dados.append({
                "Status": "ANOMALIA" if "ANOMALIA" in partes[0] else "NORMAL",
                "Ativo": partes[1].replace("Serviço:", "").strip().replace(".SA", ""),
                "Data": partes[2].replace("Data:", "").strip(),
                "Preço": float(partes[3].replace("Preço:", "").strip()),
                "Volume atual": int(partes[4].replace("Atual:", "").replace(",", "").strip()),
                "Mediana": int(partes[5].replace("Mediana:", "").replace(",", "").strip()),
                "Limite": int(partes[6].replace("Limite:", "").replace(",", "").strip()),
            })
        except (IndexError, ValueError):
            continue
    
    return pd.DataFrame(dados), linhas[0].replace("MOTOR:", "").strip()


# ──────────────────── ESTILOS CSS ──────────────────── #

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #f4f7fb;
    --muted: #8e9bae;
    --panel: #121c2b;
    --line: #243247;
    --cyan: #50e3c2;
    --alert: #ff6b6b;
    --success: #51cf66;
    --warning: #ffd43b;
}

* {
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #050b14 0%, #0a1829 50%, #08111d 100%);
    color: var(--ink);
    font-family: 'Manrope', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 2.5rem 3.5rem 2rem;
    max-width: 1600px;
}

/* ── HEADER & HERO ── */
.hero {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 0.5rem 0 2rem;
    border-bottom: 2px solid var(--line);
    margin-bottom: 2rem;
    gap: 2rem;
}

.hero-left h1 {
    margin: 0.5rem 0 0;
    font-size: 2.5rem;
    letter-spacing: -0.06em;
    font-weight: 900;
    color: #fff;
    background: linear-gradient(135deg, #fff 0%, var(--cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-left p {
    margin: 0.5rem 0 0;
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 500;
}

.eyebrow {
    color: var(--cyan);
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.16em;
    font-weight: 600;
    text-transform: uppercase;
}

.live {
    color: var(--success);
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    background: rgba(81, 207, 102, 0.1);
    border: 1px solid rgba(81, 207, 102, 0.3);
    padding: 0.65rem 1rem;
    border-radius: 100px;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
}

.pulse {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--success);
    box-shadow: 0 0 12px var(--success);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* ── MÉTRICAS ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(20, 32, 48, 0.95), rgba(12, 21, 33, 0.95));
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1.2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: var(--cyan);
    box-shadow: 0 12px 48px rgba(80, 227, 194, 0.15);
}

div[data-testid="stMetricLabel"] {
    color: var(--muted);
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

div[data-testid="stMetricValue"] {
    color: var(--ink);
    font-size: 1.8rem;
    font-family: 'DM Mono', monospace;
    font-weight: 700;
}

/* ── SEÇÕES ── */
.section-label {
    color: var(--muted);
    text-transform: uppercase;
    font-family: 'DM Mono', monospace;
    margin: 2.5rem 0 1rem;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    font-weight: 600;
}

/* ── INSIGHTS ── */
.insight {
    height: 100%;
    background: linear-gradient(145deg, #122338, #0d1826);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1.4rem;
    box-sizing: border-box;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.insight:hover {
    border-color: var(--cyan);
}

.insight-title {
    color: var(--muted);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.insight-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--cyan);
    margin-bottom: 0.5rem;
}

.insight-text {
    color: #b6c0cd;
    font-size: 0.82rem;
    line-height: 1.7;
}

.insight-alert {
    border-left: 4px solid var(--alert);
}

.insight-alert .insight-value {
    color: var(--alert);
}

.insight-success {
    border-left: 4px solid var(--success);
}

.insight-success .insight-value {
    color: var(--success);
}

/* ── BOTÕES ── */
.stButton > button {
    border: 1.5px solid var(--cyan);
    background: rgba(80, 227, 194, 0.1);
    color: var(--cyan);
    border-radius: 8px;
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 0.65rem 1.2rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: rgba(80, 227, 194, 0.2);
    box-shadow: 0 0 20px rgba(80, 227, 194, 0.3);
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

/* ── RESPONSIVO ── */
@media (max-width: 800px) {
    .block-container { padding: 1.2rem; }
    .hero { 
        align-items: flex-start;
        gap: 1rem;
        flex-direction: column;
    }
    .hero-left h1 { font-size: 1.8rem; }
}
</style>
""", unsafe_allow_html=True)


# ──────────────────── CARREGAMENTO DE DADOS ──────────────────── #

df, hora_motor = ler_log_processado()


# ──────────────────── HEADER ──────────────────── #

st.markdown("""
<div class="hero">
    <div class="hero-left">
        <div class="eyebrow">🛡️ SLN IT · INTELLIGENT OPERATIONS</div>
        <h1>Sentinel <span style="color:var(--cyan)">/</span></h1>
        <p>Detecção inteligente de anomalias estatísticas em tempo real</p>
    </div>
    <div class="live"><span class="pulse"></span>MONITORAMENTO ATIVO</div>
</div>
""", unsafe_allow_html=True)


# ──────────────────── VERIFICAÇÃO DE DADOS ──────────────────── #

if df.empty:
    st.warning("⏳ O Sentinel está aguardando a primeira execução do motor de análise.")
    st.info("Execute `python src/anomaly_engine.py` para iniciar o processamento.", icon="ℹ️")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Atualizar painel", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with col2:
        if st.button("📖 Ver documentação", use_container_width=True):
            st.info("Acesse o README.md para mais informações sobre configuração.")
    st.stop()


# ──────────────────── CÁLCULOS DE MÉTRICAS ──────────────────── #

anomalias = df[df["Status"] == "ANOMALIA"]
num_ativos = len(df)
num_anomalias = len(anomalias)
normalidade = ((num_ativos - num_anomalias) / num_ativos * 100) if num_ativos > 0 else 0
maior_desvio = calcular_desvio_percentual(df["Volume atual"].max(), df["Mediana"].max())
taxa_desvio_medio = calcular_desvio_percentual(df["Volume atual"].mean(), df["Mediana"].mean())


# ──────────────────── DASHBOARD KPI ──────────────────── #

st.markdown('<div class="section-label">📊 KPIs de Operação</div>', unsafe_allow_html=True)

kpi_cols = st.columns(5)

with kpi_cols[0]:
    kpi_cols[0].metric(
        "Ativos Monitorados",
        num_ativos,
        delta=f"{num_ativos} em análise"
    )

with kpi_cols[1]:
    delta_text = f"{num_anomalias} crítico{'s' if num_anomalias != 1 else ''}" if num_anomalias > 0 else "Tudo normal"
    kpi_cols[1].metric(
        "Alertas Críticos",
        num_anomalias,
        delta=delta_text,
        delta_color="inverse" if num_anomalias > 0 else "normal"
    )

with kpi_cols[2]:
    kpi_cols[2].metric(
        "Estabilidade Operacional",
        f"{normalidade:.1f}%",
        delta="Dentro dos limites" if normalidade >= 90 else "Investigar"
    )

with kpi_cols[3]:
    kpi_cols[3].metric(
        "Maior Desvio Detectado",
        f"+{maior_desvio:.1f}%",
        delta="Acima do baseline"
    )

with kpi_cols[4]:
    kpi_cols[4].metric(
        "Desvio Médio",
        f"{taxa_desvio_medio:+.1f}%",
        delta="Variação geral"
    )


# ──────────────────── GRÁFICO PRINCIPAL ──────────────────── #

st.markdown(f'<div class="section-label">📈 Panorama de Mercado · Última leitura: {df["Data"].iloc[0]}</div>', unsafe_allow_html=True)

fig = go.Figure()

# Cores por status
cores = ["#ff6b6b" if status == "ANOMALIA" else "#3d84c6" for status in df["Status"]]

# Barras de volume atual
fig.add_trace(go.Bar(
    x=df["Ativo"],
    y=df["Volume atual"],
    name="Volume Atual",
    marker=dict(color=cores, line=dict(width=0)),
    hovertemplate="<b>%{x}</b><br>Volume Atual: %{y:,.0f}<extra></extra>",
    showlegend=True
))

# Linha de mediana histórica
fig.add_trace(go.Scatter(
    x=df["Ativo"],
    y=df["Mediana"],
    name="Baseline (Mediana Móvel)",
    mode="lines+markers",
    line=dict(color="#50e3c2", width=3),
    marker=dict(size=7, symbol="circle"),
    hovertemplate="<b>%{x}</b><br>Mediana: %{y:,.0f}<extra></extra>",
    showlegend=True
))

# Linha de limite estatístico
fig.add_trace(go.Scatter(
    x=df["Ativo"],
    y=df["Limite"],
    name="Limite Estatístico (MAD 3σ)",
    mode="lines",
    line=dict(color="#ffd43b", width=2.5, dash="dot"),
    hovertemplate="<b>%{x}</b><br>Limite: %{y:,.0f}<extra></extra>",
    showlegend=True
))

fig.update_layout(
    height=420,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(18,28,43,.35)",
    margin=dict(l=12, r=12, t=18, b=12),
    font=dict(family="Manrope", color="#aebccc", size=12),
    legend=dict(
        orientation="h",
        y=1.12,
        x=0,
        font=dict(size=11),
        bgcolor="rgba(0,0,0,0.3)",
        bordercolor="var(--line)",
        borderwidth=1
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(color="#dbe6f2")
    ),
    yaxis=dict(
        gridcolor="#233246",
        zeroline=False,
        tickformat="~s",
        title=None
    ),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ──────────────────── ANÁLISE & RECOMENDAÇÕES ──────────────────── #

col_rec, col_status = st.columns([1.2, 1])

with col_rec:
    st.markdown('<div class="section-label">⚡ Recomendações</div>', unsafe_allow_html=True)
    
    if not anomalias.empty:
        ativo_critico = anomalias.iloc[0]
        excesso = calcular_desvio_percentual(ativo_critico["Volume atual"], ativo_critico["Limite"])
        
        st.markdown(f"""
        <div class="insight insight-alert">
            <div class="insight-title">🚨 Ação Necessária</div>
            <div class="insight-value">{num_anomalias} Alerta{'s' if num_anomalias != 1 else ''}</div>
            <div class="insight-text">
                <strong>{ativo_critico['Ativo']}</strong> está {excesso:.1f}% acima do limite estatístico. 
                Recomenda-se investigação imediata. Volume detectado: <strong>{abreviar_volume(ativo_critico['Volume atual'])}</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="insight insight-success">
            <div class="insight-title">✓ Status Operacional</div>
            <div class="insight-value">Sem Desvios</div>
            <div class="insight-text">
                Todos os ativos estão dentro dos limites estatísticos esperados. 
                O comportamento operacional está normalizado e sob controle.
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_status:
    st.markdown('<div class="section-label">🔧 Status do Motor</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight">
        <div class="insight-title">Última Execução</div>
        <div class="insight-value">{hora_motor or "—"}</div>
        <div class="insight-text">
            Motor executando com baseline adaptativo. 
            Algoritmo: Mediana Móvel + MAD (3σ). 
            Atualização a cada 5 segundos.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────── TABELA DETALHADA ──────────────────── #

st.markdown('<div class="section-label">📋 Fila de Observabilidade</div>', unsafe_allow_html=True)

tabela_display = df.copy()

# Formatar colunas numéricas
for coluna in ["Volume atual", "Mediana", "Limite"]:
    tabela_display[coluna] = tabela_display[coluna].apply(abreviar_volume)

# Formatar status
tabela_display["Status"] = tabela_display["Status"].apply(
    lambda x: "🔴 Atenção" if x == "ANOMALIA" else "🟢 Normal"
)

# Calcular desvio
tabela_display["Desvio %"] = df.apply(
    lambda row: f"{calcular_desvio_percentual(row['Volume atual'], row['Mediana']):+.1f}%",
    axis=1
)

# Reordenar colunas
tabela_display = tabela_display[["Status", "Ativo", "Data", "Preço", "Volume atual", "Mediana", "Limite", "Desvio %"]]

st.dataframe(
    tabela_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Preço": st.column_config.NumberColumn("Preço", format="R$ %.2f"),
        "Status": st.column_config.TextColumn("Status", width="medium")
    }
)


# ──────────────────── FOOTER & AÇÕES ──────────────────── #

col_info, col_actions = st.columns([3, 1])

with col_info:
    st.caption(
        "🛡️ SENTINEL v1.0 · SLN IT SOLUTIONS · "
        "Detecção robusta de anomalias para operações que não podem parar."
    )

with col_actions:
    if st.button("🔄 Atualizar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
