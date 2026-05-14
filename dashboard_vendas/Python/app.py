import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Dashboard de Vendas | ROQT",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.main { background-color: #f8f9fb; }
[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e8eaed; }

.kpi-card {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 0;
}
.kpi-label { font-size: 12px; color: #6b7280; font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 6px; }
.kpi-value { font-size: 28px; font-weight: 600; color: #111827; line-height: 1; margin-bottom: 4px; }
.kpi-delta-pos { font-size: 12px; color: #059669; font-weight: 500; }
.kpi-delta-neg { font-size: 12px; color: #dc2626; font-weight: 500; }

.section-title { font-size: 14px; font-weight: 600; color: #374151; margin: 0 0 12px 0; letter-spacing: 0.01em; }
.chart-card {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 12px;
    padding: 20px 24px;
}

.roqt-header {
    background: #111827;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

div[data-testid="metric-container"] { display: none; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("vendas.csv", parse_dates=["data_venda"])
    df_metas = pd.read_csv("metas.csv")
    df["mes"] = df["data_venda"].dt.month
    df["mes_nome"] = df["data_venda"].dt.strftime("%b/%Y")
    df["trimestre"] = df["data_venda"].dt.quarter.map({1:"Q1", 2:"Q2", 3:"Q3", 4:"Q4"})
    return df, df_metas

df, df_metas = load_data()

with st.sidebar:
    st.markdown("### Filtros")
    st.markdown("---")

    meses_disp = sorted(df["mes"].unique())
    nomes_mes = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}
    mes_sel = st.multiselect("Mês", options=meses_disp, default=meses_disp, format_func=lambda x: nomes_mes[x])

    vendedores_disp = sorted(df["vendedor"].unique())
    vend_sel = st.multiselect("Vendedor", options=vendedores_disp, default=vendedores_disp)

    regioes_disp = sorted(df["regiao"].unique())
    reg_sel = st.multiselect("Região", options=regioes_disp, default=regioes_disp)

    status_disp = sorted(df["status"].unique())
    status_sel = st.multiselect("Status", options=status_disp, default=["Pago"])

    st.markdown("---")
    st.markdown("<p style='font-size:11px;color:#9ca3af;'>Dashboard de Vendas v1.0<br>Portfólio ROQT · 2024</p>", unsafe_allow_html=True)

mask = (
    df["mes"].isin(mes_sel) &
    df["vendedor"].isin(vend_sel) &
    df["regiao"].isin(reg_sel) &
    df["status"].isin(status_sel)
)
dff = df[mask].copy()

st.markdown("""
<div class="roqt-header">
    <div>
        <div style="font-size:20px;font-weight:600;color:#ffffff;letter-spacing:-0.01em;">Dashboard de Vendas</div>
        <div style="font-size:13px;color:#9ca3af;margin-top:2px;">Análise completa de performance comercial · 2024</div>
    </div>
    <div style="font-size:12px;color:#6b7280;font-family:'DM Mono',monospace;">ROQT Data & AI</div>
</div>
""", unsafe_allow_html=True)

fat_total = dff["valor_total"].sum()
ticket_medio = dff["valor_total"].mean() if len(dff) > 0 else 0
qtd_vendas = len(dff)
produtos_unicos = dff["produto"].nunique()

fat_total_all = df[df["status"]=="Pago"]["valor_total"].sum()
pct_representado = (fat_total / fat_total_all * 100) if fat_total_all > 0 else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Faturamento total</div>
        <div class="kpi-value">R$ {fat_total/1e6:.2f}M</div>
        <div class="kpi-delta-pos">↑ {pct_representado:.1f}% do total anual</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Ticket médio</div>
        <div class="kpi-value">R$ {ticket_medio:,.0f}</div>
        <div class="kpi-delta-pos">por transação</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Vendas realizadas</div>
        <div class="kpi-value">{qtd_vendas}</div>
        <div class="kpi-delta-pos">transações no período</div>
    </div>""", unsafe_allow_html=True)
with c4:
    conv = len(dff[dff["status"]=="Pago"]) / len(dff) * 100 if len(dff) > 0 else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Taxa de conversão</div>
        <div class="kpi-value">{conv:.1f}%</div>
        <div class="kpi-delta-pos">vendas pagas</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<p class='section-title'>Faturamento mensal</p>", unsafe_allow_html=True)
    mensal = df[df["status"]=="Pago"].groupby("mes")["valor_total"].sum().reset_index()
    mensal["mes_nome"] = mensal["mes"].map(nomes_mes)
    mensal = mensal.sort_values("mes")

    fig_linha = go.Figure()
    fig_linha.add_trace(go.Bar(
        x=mensal["mes_nome"], y=mensal["valor_total"],
        marker_color="#e8eaed", name="Faturamento",
        hovertemplate="<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>"
    ))
    if len(dff) > 0:
        mensal_sel = dff.groupby("mes")["valor_total"].sum().reset_index()
        mensal_sel["mes_nome"] = mensal_sel["mes"].map(nomes_mes)
        mensal_sel = mensal_sel.sort_values("mes")
        fig_linha.add_trace(go.Bar(
            x=mensal_sel["mes_nome"], y=mensal_sel["valor_total"],
            marker_color="#111827", name="Selecionado",
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>"
        ))
    fig_linha.update_layout(
        height=240, margin=dict(l=0,r=0,t=0,b=0),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=1.1, x=0),
        barmode="overlay",
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor="#f3f4f6", tickformat=",.0f", tickfont=dict(size=11)),
        font=dict(family="DM Sans")
    )
    st.plotly_chart(fig_linha, use_container_width=True)

with col2:
    st.markdown("<p class='section-title'>Vendas por produto</p>", unsafe_allow_html=True)
    por_prod = dff.groupby("produto")["valor_total"].sum().sort_values(ascending=True).reset_index()
    fig_prod = px.bar(por_prod, x="valor_total", y="produto", orientation="h",
                      color_discrete_sequence=["#111827"])
    fig_prod.update_traces(hovertemplate="<b>%{y}</b><br>R$ %{x:,.0f}<extra></extra>")
    fig_prod.update_layout(
        height=240, margin=dict(l=0,r=0,t=0,b=0),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#f3f4f6", tickformat=",.0f", tickfont=dict(size=10), title=""),
        yaxis=dict(showgrid=False, tickfont=dict(size=10), title=""),
        font=dict(family="DM Sans")
    )
    st.plotly_chart(fig_prod, use_container_width=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("<p class='section-title'>Ranking de vendedores</p>", unsafe_allow_html=True)
    rank = dff.groupby("vendedor")["valor_total"].sum().sort_values(ascending=False).reset_index()
    rank["pct"] = rank["valor_total"] / rank["valor_total"].sum() * 100
    colors = ["#111827", "#374151", "#6b7280", "#9ca3af", "#d1d5db"]
    fig_rank = px.bar(rank, x="valor_total", y="vendedor", orientation="h",
                      color="vendedor", color_discrete_sequence=colors)
    fig_rank.update_traces(hovertemplate="<b>%{y}</b><br>R$ %{x:,.0f}<extra></extra>")
    fig_rank.update_layout(
        height=220, margin=dict(l=0,r=0,t=0,b=0),
        plot_bgcolor="white", paper_bgcolor="white", showlegend=False,
        xaxis=dict(showgrid=True, gridcolor="#f3f4f6", tickformat=",.0f", tickfont=dict(size=10), title=""),
        yaxis=dict(showgrid=False, tickfont=dict(size=10), title="", categoryorder="total ascending"),
        font=dict(family="DM Sans")
    )
    st.plotly_chart(fig_rank, use_container_width=True)

with col4:
    st.markdown("<p class='section-title'>Vendas por região</p>", unsafe_allow_html=True)
    reg = dff.groupby("regiao")["valor_total"].sum().reset_index()
    fig_reg = px.pie(reg, values="valor_total", names="regiao",
                     color_discrete_sequence=["#111827","#374151","#6b7280","#9ca3af","#d1d5db","#e5e7eb"])
    fig_reg.update_traces(textposition="inside", textinfo="percent+label",
                          hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f}<extra></extra>",
                          textfont_size=10)
    fig_reg.update_layout(
        height=220, margin=dict(l=0,r=20,t=0,b=0),
        showlegend=False, paper_bgcolor="white",
        font=dict(family="DM Sans")
    )
    st.plotly_chart(fig_reg, use_container_width=True)

with col5:
    st.markdown("<p class='section-title'>Mix por segmento</p>", unsafe_allow_html=True)
    seg = dff.groupby("segmento")["valor_total"].sum().sort_values(ascending=False).reset_index()
    fig_seg = px.treemap(seg, path=["segmento"], values="valor_total",
                         color_discrete_sequence=["#111827","#1f2937","#374151","#4b5563","#6b7280","#9ca3af"])
    fig_seg.update_traces(hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f}<extra></extra>",
                          textfont_size=11)
    fig_seg.update_layout(
        height=220, margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="white", font=dict(family="DM Sans")
    )
    st.plotly_chart(fig_seg, use_container_width=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>Meta vs realizado por vendedor</p>", unsafe_allow_html=True)

real_vend = df[df["status"]=="Pago"].groupby(["mes","vendedor"])["valor_total"].sum().reset_index()
real_vend.columns = ["mes","vendedor","realizado"]
meta_real = df_metas.merge(real_vend, on=["mes","vendedor"], how="left").fillna(0)
meta_real["pct_meta"] = (meta_real["realizado"] / meta_real["meta"] * 100).round(1)
resumo_meta = meta_real.groupby("vendedor").agg(
    meta_total=("meta","sum"),
    realizado_total=("realizado","sum")
).reset_index()
resumo_meta["pct"] = (resumo_meta["realizado_total"] / resumo_meta["meta_total"] * 100).round(1)
resumo_meta = resumo_meta.sort_values("pct", ascending=False)

fig_meta = go.Figure()
fig_meta.add_trace(go.Bar(name="Meta", x=resumo_meta["vendedor"], y=resumo_meta["meta_total"],
                           marker_color="#e8eaed",
                           hovertemplate="<b>%{x}</b><br>Meta: R$ %{y:,.0f}<extra></extra>"))
fig_meta.add_trace(go.Bar(name="Realizado", x=resumo_meta["vendedor"], y=resumo_meta["realizado_total"],
                           marker_color="#111827",
                           hovertemplate="<b>%{x}</b><br>Realizado: R$ %{y:,.0f}<extra></extra>"))
fig_meta.update_layout(
    height=220, margin=dict(l=0,r=0,t=0,b=0),
    barmode="group", plot_bgcolor="white", paper_bgcolor="white",
    legend=dict(orientation="h", y=1.1, x=0),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor="#f3f4f6", tickformat=",.0f", tickfont=dict(size=11)),
    font=dict(family="DM Sans")
)
st.plotly_chart(fig_meta, use_container_width=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>Detalhamento das transações</p>", unsafe_allow_html=True)
tabela = dff[["data_venda","vendedor","produto","regiao","segmento","quantidade","valor_total","status"]].copy()
tabela["data_venda"] = tabela["data_venda"].dt.strftime("%d/%m/%Y")
tabela["valor_total"] = tabela["valor_total"].apply(lambda x: f"R$ {x:,.2f}")
tabela.columns = ["Data","Vendedor","Produto","Região","Segmento","Qtd","Valor","Status"]
st.dataframe(tabela, use_container_width=True, height=220, hide_index=True)
