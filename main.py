import streamlit as st
import pandas as pd
import plotly.express as px

# Função para criar a tabela inicial
def create_initial_table():
    weeks = ["Semana 1", "Semana 2", "Semana 3", "Semana 4", "Semana 5", "Semana 6", "Semana 7", "Semana 8"]
    table_data = {
        "Semana": weeks,
        "Aulas Planejadas": [6] * 8,
        "Aulas Concluídas": [0] * 8,
        "Simulado Planejado": [1] * 7 + [0],
        "Simulado Concluído": [0] * 8,
        "Horas Estudo Planejadas": [18] * 8,
        "Horas Estudo Concluídas": [0] * 8,
        "Pontuação Simulado": [0] * 8,
        "Comentários": [""] * 8
    }
    return pd.DataFrame(table_data)

# Função para carregar dados do arquivo CSV
def load_data():
    try:
        df = pd.read_csv('study_tracker.csv')
        return df
    except FileNotFoundError:
        df = create_initial_table()
        df.to_csv('study_tracker.csv', index=False)
        return df

# Função para salvar dados no arquivo CSV
def save_data(df):
    df.to_csv('study_tracker.csv', index=False)

# Carregar ou criar a tabela
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Título da aplicação
st.title("Acompanhamento de Estudos")

# Indicadores
st.header("Indicadores de Progresso")
total_aulas_concluidas = st.session_state.df["Aulas Concluídas"].sum()
total_simulados_concluidos = st.session_state.df["Simulado Concluído"].sum()
total_horas_estudo_concluidas = st.session_state.df["Horas Estudo Concluídas"].sum()


col1, col2, col3 = st.columns(3)
col1.metric("Aulas Concluídas", total_aulas_concluidas, )
col2.metric("Simulados Concluídos", total_simulados_concluidos)
col3.metric("Horas Estudo Concluídas", total_horas_estudo_concluidas)

# Calendário de Estudo
st.header("Calendário de Estudo")

calendar_data = {
    "Semana": [
        "Semana 1 (29/05 - 04/06)", "Semana 2 (05/06 - 11/06)", "Semana 3 (12/06 - 18/06)", 
        "Semana 4 (19/06 - 25/06)", "Semana 5 (26/06 - 02/07)", "Semana 6 (03/07 - 09/07)", 
        "Semana 7 (10/07 - 16/07)", "Semana 8 (17/07 - 21/07)"
    ],
    "Segunda": [
        "Inglês", "Inglês", "Adm. Geral", "Cont. Pública", "Macroeconomia", "Economia Bras.", "Auditoria", "Adm. Financeira"
    ],
    "Terça": [
        "Inglês", "Inglês", "Adm. Geral", "Cont. Custos", "Direito Adm.", "Cont. Geral", "Estatística", "Economia Internacional"
    ],
    "Quarta": [
        "Inglês", "Adm. Geral", "Adm. Geral", "Cont. Custos", "Direito Adm.", "Cont. Geral", "Estatística", "Economia Internacional"
    ],
    "Quinta": [
        "Inglês", "Adm. Geral", "Cont. Pública", "Cont. Custos", "Direito Adm.", "Economia Setor Público", "Gestão e Gov Pública", "Logística"
    ],
    "Sexta": [
        "Inglês", "Adm. Geral", "Cont. Pública", "Macroeconomia", "Economia Bras.", "Economia Setor Público", "Gestão e Gov Pública", "Qualidade"
    ],
    "Sábado": [
        "Inglês", "Adm. Geral", "Cont. Pública", "Macroeconomia", "Economia Bras.", "Auditoria", "Adm. Financeira", "Gestão de Processos"
    ],
    "Domingo": [
        "Simulado 1 (5h)", "Simulado 2 (5h)", "Simulado 3 (5h)", "Simulado 4 (5h)", "Simulado 5 (5h)", "Simulado 6 (5h)", "Simulado 7 (5h)", "-"
    ]
}

calendar_df = pd.DataFrame(calendar_data)

# Estilizar a tabela
st.markdown("""
    <style>
        .calendar-table {
            width: 100%;
            border-collapse: collapse;
        }
        .calendar-table th, .calendar-table td {
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
        }
        .calendar-table th {
            background-color: #f2f2f2;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(calendar_df.to_html(classes="calendar-table", index=False), unsafe_allow_html=True)
# Gráficos dos Indicadores
fig1 = px.bar(st.session_state.df, x="Semana", y="Aulas Concluídas", title="Aulas Concluídas por Semana")
fig2 = px.bar(st.session_state.df, x="Semana", y="Simulado Concluído", title="Simulados Concluídos por Semana")
fig3 = px.bar(st.session_state.df, x="Semana", y="Horas Estudo Concluídas", title="Horas de Estudo Concluídas por Semana")
fig4 = px.bar(st.session_state.df, x="Semana", y="Pontuação Simulado", title="Pontuação dos Simulados por Semana")

col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col1.plotly_chart(fig2, use_container_width=True)
col2.plotly_chart(fig3, use_container_width=True)
col2.plotly_chart(fig4, use_container_width=True)

# Atualização dos dados
selected_week = st.sidebar.selectbox("Selecione a Semana", st.session_state.df["Semana"])
aulas_concluidas = st.sidebar.number_input("Aulas Concluídas", min_value=0, max_value=6, step=1)
simulado_concluido = st.sidebar.checkbox("Simulado Concluído")
horas_estudo_concluidas = st.sidebar.number_input("Horas de Estudo Concluídas", min_value=0, max_value=18, step=1)
pontuacao_simulado = st.sidebar.number_input("Pontuação Simulado", min_value=0, max_value=100, step=1)
comentarios = st.sidebar.text_area("Comentários")

if st.sidebar.button("Atualizar"):
    index = st.session_state.df[st.session_state.df["Semana"] == selected_week].index[0]
    st.session_state.df.at[index, "Aulas Concluídas"] = aulas_concluidas
    st.session_state.df.at[index, "Simulado Concluído"] = 1 if simulado_concluido else 0
    st.session_state.df.at[index, "Horas Estudo Concluídas"] = horas_estudo_concluidas
    st.session_state.df.at[index, "Pontuação Simulado"] = pontuacao_simulado
    st.session_state.df.at[index, "Comentários"] = comentarios
    save_data(st.session_state.df)

# Recalcular os totais após atualização
total_aulas_concluidas = st.session_state.df["Aulas Concluídas"].sum()
total_simulados_concluidos = st.session_state.df["Simulado Concluído"].sum()
total_horas_estudo_concluidas = st.session_state.df["Horas Estudo Concluídas"].sum()
