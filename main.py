import streamlit as st
import pandas as pd
import plotly.express as px

# Função para criar a tabela inicial
def create_initial_table():
    weeks = ["Semana 1", "Semana 2", "Semana 3", "Semana 4", "Semana 5", "Semana 6", "Semana 7", "Semana 8"]
    table_data = {
        "Semana": weeks,
        "Aulas Planejadas": [6, 6, 6, 6, 6, 6, 6, 6],
        "Aulas Concluídas": [0] * 8,
        "Simulado Planejado": [1] * 7 + [0],
        "Simulado Concluído": [0] * 8,
        "Horas Estudo Planejadas": [18] * 8,
        "Horas Estudo Concluídas": [0] * 8,
        "Pontuação Simulado": [0] * 8,
        "Comentários": [""] * 8
    }
    return pd.DataFrame(table_data)

# Carregar ou criar a tabela
if 'df' not in st.session_state:
    st.session_state.df = create_initial_table()

# Título da aplicação
st.title("Acompanhamento de Estudos")

# Indicadores
st.header("Indicadores de Progresso")
total_aulas_concluidas = st.session_state.df["Aulas Concluídas"].sum()
total_simulados_concluidos = st.session_state.df["Simulado Concluído"].sum()
total_horas_estudo_concluidas = st.session_state.df["Horas Estudo Concluídas"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Aulas Concluídas", total_aulas_concluidas)
col2.metric("Simulados Concluídos", total_simulados_concluidos)
col3.metric("Horas Estudo Concluídas", total_horas_estudo_concluidas)

# Gráficos dos Indicadores
fig1 = px.bar(st.session_state.df, x="Semana", y="Aulas Concluídas", title="Aulas Concluídas por Semana")
fig2 = px.bar(st.session_state.df, x="Semana", y="Simulado Concluído", title="Simulados Concluídos por Semana")
fig3 = px.bar(st.session_state.df, x="Semana", y="Horas Estudo Concluídas", title="Horas de Estudo Concluídas por Semana")
fig4 = px.bar(st.session_state.df, x="Semana", y="Pontuação Simulado", title="Pontuação dos Simulados por Semana")

st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig4)

# Tabela de Aulas
st.header("Tabela de Acompanhamento de Aulas")
st.dataframe(st.session_state.df)

# Atualização dos dados
st.header("Atualizar Progresso Semanal")
selected_week = st.sidebar.selectbox("Selecione a Semana", st.session_state.df["Semana"])
aulas_concluidas = st.sidebar.number_input("Aulas Concluídas", min_value=0, max_value=6, step=1)
simulado_concluido = st.sidebar.checkbox("Simulado Concluído")
horas_estudo_concluidas = st.sidebar.number_input("Horas de Estudo Concluídas", min_value=0, max_value=18, step=1)
pontuacao_simulado = st.sidebar.number_input("Pontuação Simulado", min_value=0, max_value=100, step=1)
comentarios = st.sidebar.text_area("Comentários")

if st.button("Atualizar"):
    index = st.session_state.df[st.session_state.df["Semana"] == selected_week].index[0]
    st.session_state.df.at[index, "Aulas Concluídas"] = aulas_concluidas
    st.session_state.df.at[index, "Simulado Concluído"] = 1 if simulado_concluido else 0
    st.session_state.df.at[index, "Horas Estudo Concluídas"] = horas_estudo_concluidas
    st.session_state.df.at[index, "Pontuação Simulado"] = pontuacao_simulado
    st.session_state.df.at[index, "Comentários"] = comentarios

# Recalcular os totais após atualização
total_aulas_concluidas = st.session_state.df["Aulas Concluídas"].sum()
total_simulados_concluidos = st.session_state.df["Simulado Concluído"].sum()
total_horas_estudo_concluidas = st.session_state.df["Horas Estudo Concluídas"].sum()

col1.metric("Aulas Concluídas", total_aulas_concluidas)
col2.metric("Simulados Concluídos", total_simulados_concluidos)
col3.metric("Horas Estudo Concluídas", total_horas_estudo_concluidas)

# Reexibir os gráficos após atualização
st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig4)
