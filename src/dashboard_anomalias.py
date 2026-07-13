import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Sentinel Dashboard",
    layout="wide"
)


def ler_log_processado():

    src_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(src_dir)

    caminho_log = os.path.join(root_dir, "data", "log_sistema.txt")

    if not os.path.exists(caminho_log):
        return None, None

    with open(caminho_log, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    if len(linhas) == 0:
        return None, None

    ultima_execucao_motor = linhas[0].replace("MOTOR:", "").strip()

    dados = []

    for linha in linhas[1:]:

        if "Serviço:" not in linha:
            continue

        try:

            partes = linha.split(" | ")

            status = partes[0].strip()

            ticker = partes[1].replace("Serviço:", "").strip()

            data = partes[2].replace("Data:", "").strip()

            preco = float(partes[3].replace("Preço:", "").strip())

            atual = int(partes[4].replace("Atual:", "").replace(",", "").strip())

            mediana = int(partes[5].replace("Mediana:", "").replace(",", "").strip())

            limite = int(partes[6].replace("Limite:", "").replace(",", "").strip())

            dados.append({

                "Status": status,

                "Ticker": ticker,

                "Data Yahoo": data,

                "Preço": preco,

                "Volume Atual": atual,

                "Mediana": mediana,

                "Limite": limite

            })

        except:
            pass

    return pd.DataFrame(dados), ultima_execucao_motor


st.title("📊 Sentinel Dashboard")

st.caption(
    "Monitoramento de **anomalias de volume de negociação** utilizando dados do Yahoo Finance."
)

st.info(
    "📈 O sistema compara o **volume negociado** (quantidade de ações ou cotas negociadas no período) "
    "com a mediana dos últimos 20 pregões."
)

df, hora_motor = ler_log_processado()

if df is not None and not df.empty:

    ultimo_pregao = df["Data Yahoo"].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🕒 Última atualização do motor",
            hora_motor
        )

    with col2:
        st.metric(
            "📅 Último pregão disponível",
            ultimo_pregao
        )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=df["Ticker"],
            y=df["Volume Atual"],
            name="Volume Atual"

        )

    )

    fig.add_trace(

        go.Scatter(

    x=df["Ticker"],
    y=df["Mediana"],
    mode="lines+markers",
    name="Mediana",

    line=dict(
        color="lime",
        width=3
    ),

    marker=dict(
        color="lime",
        size=8
    )

)

    )

    fig.add_trace(

        go.Scatter(

    x=df["Ticker"],
    y=df["Limite"],
    mode="lines",

    line=dict(
        color="red",
        width=3,
        dash="dash"
    ),

    name="Limite"

)

    )

    fig.update_layout(

        template="plotly_dark",

        title="Análise de Volume das Negociações",

        xaxis_title="Ativos",

        yaxis_title="Quantidade de ações negociadas",

        legend_title="Indicadores"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Resultado da análise")

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )

else:

    st.warning(
        "Aguardando processamento dos dados do Yahoo Finance..."
    )

if st.button("🔄 Atualizar painel"):

    st.rerun()