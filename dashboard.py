import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from analysis import prever

# CONFIG VISUAL
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .metric {
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# BANCO
conn = sqlite3.connect("cambio.db")
df = pd.read_sql("SELECT * FROM cotacoes", conn)

usd = df[df["moeda"] == "USD"]
eur = df[df["moeda"] == "EUR"]

# KPIs
col1, col2, col3, col4 = st.columns(4)

def calc_var(df):
    if len(df) < 2:
        return 0
    return ((df["valor"].iloc[-1] - df["valor"].iloc[0]) / df["valor"].iloc[0]) * 100

usd_var = calc_var(usd)
eur_var = calc_var(eur)

with col1:
    st.metric("💵 USD", f"R$ {usd['valor'].iloc[-1]:.2f}", f"{usd_var:.2f}%")

with col2:
    st.metric("💶 EUR", f"R$ {eur['valor'].iloc[-1]:.2f}", f"{eur_var:.2f}%")

# PROJEÇÃO
usd_prev = prever(usd)
eur_prev = prever(eur)

with col3:
    if usd_prev:
        st.metric("📈 USD (D+1)", f"{usd_prev[0]:.2f}")

with col4:
    if eur_prev:
        st.metric("📉 EUR (D+1)", f"{eur_prev[0]:.2f}")

# GRÁFICO USD
fig_usd = go.Figure()
fig_usd.add_trace(go.Scatter(
    x=usd["data"],
    y=usd["valor"],
    mode='lines',
    name='USD',
    line=dict(color='lime', width=2)
))

fig_usd.update_layout(
    title="USD/BRL",
    template="plotly_dark"
)

# GRÁFICO EUR
fig_eur = go.Figure()
fig_eur.add_trace(go.Scatter(
    x=eur["data"],
    y=eur["valor"],
    mode='lines',
    name='EUR',
    line=dict(color='orange', width=2)
))

fig_eur.update_layout(
    title="EUR/BRL",
    template="plotly_dark"
)

col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(fig_usd, use_container_width=True)

with col6:
    st.plotly_chart(fig_eur, use_container_width=True)

# TABELA
st.subheader("📊 Últimos registros")
st.dataframe(df.tail(20))
