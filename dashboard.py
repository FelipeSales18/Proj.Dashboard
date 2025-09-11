import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard de Vendas com IA",
    page_icon="📊",
    layout="wide"
)

# --- FUNÇÃO PARA CARREGAR DADOS ---
def load_data(uploaded_file):
    """Carrega dados de um arquivo CSV ou Excel, ou gera dados de exemplo."""
    if uploaded_file:
        try:
            # Tenta ler como CSV e depois como Excel se falhar
            df = pd.read_csv(uploaded_file)
        except Exception:
            # Move o ponteiro do arquivo de volta para o início antes de ler de novo
            uploaded_file.seek(0)
            df = pd.read_excel(uploaded_file)
        # Converte a coluna 'Mes' para datetime se existir, tratando erros
        if 'Mes' in df.columns:
            df['Mes'] = pd.to_datetime(df['Mes'], errors='coerce')
        return df
    else:
        # Cria um dataset de exemplo se nenhum arquivo for carregado
        st.info("Nenhum arquivo carregado. Usando dados de exemplo.")
        np.random.seed(42)
        data = {
            "Mes": pd.to_datetime(pd.date_range("2022-01-01", periods=24, freq="M")),
            "Vendas": np.random.randint(200, 1000, 24),
            "Marketing": np.random.randint(1000, 5000, 24)
        }
        df = pd.DataFrame(data)
        df["Receita"] = df["Vendas"] * 50 + df["Marketing"] * 0.3
        return df

# --- 2. LAYOUT DO DASHBOARD ---

# Título Principal
st.title("📊 Dashboard de Vendas com IA")
st.markdown("Analise dados de vendas e preveja a receita futura usando Machine Learning.")
st.markdown("---")

# Barra Lateral (Sidebar)
st.sidebar.header("⚙️ Configurações")
uploaded_file = st.sidebar.file_uploader(
    "Carregue seu arquivo (CSV ou Excel)",
    type=["csv", "xlsx", "xls"]
)

# Carregar os dados
df = load_data(uploaded_file)

# --- Validação das colunas necessárias ---
required_columns = ["Vendas", "Marketing", "Receita", "Mes"]
if not all(col in df.columns for col in required_columns):
    st.error(f"Erro: O arquivo carregado ou os dados de exemplo não contêm as colunas necessárias: {', '.join(required_columns)}")
else:
    # --- 3. VISUALIZAÇÃO DOS DADOS ---
    st.header("📈 Análise Visual dos Dados")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Evolução das Vendas e Receita")
        fig_line = px.line(df, x="Mes", y=["Vendas", "Receita"], markers=True,
                           title="Performance Mensal")
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        st.subheader("Relação entre Marketing e Receita")
        fig_scatter = px.scatter(df, x="Marketing", y="Receita", trendline="ols",
                                 title="Investimento em Marketing vs. Receita")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Mostrar tabela de dados
    if st.checkbox("Mostrar dados brutos"):
        st.dataframe(df)
    
    st.markdown("---")
    
    # --- 4. IA - PREVISÃO DE RECEITA ---
    st.header("🤖 Previsão de Receita com Machine Learning")

    # Preparar dados para o modelo
    X = df[["Vendas", "Marketing"]]
    y = df["Receita"]

    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Avaliar o modelo
    mae = mean_absolute_error(y_test, y_pred)
    st.metric(
        label="**Performance do Modelo (Erro Médio)**",
        value=f"R$ {mae:,.2f}",
        help="O Erro Médio Absoluto (MAE) indica a diferença média entre a receita prevista e a receita real. Quanto menor, melhor o modelo."
    )
    
    # --- 5. SIMULAÇÃO INTERATIVA NA SIDEBAR ---
    st.sidebar.subheader("🔮 Simulação de Receita")
    vendas_input = st.sidebar.slider(
        "Quantidade de Vendas",
        min_value=int(df['Vendas'].min()),
        max_value=int(df['Vendas'].max() * 2),
        step=50,
        value=int(df['Vendas'].median())
    )
    marketing_input = st.sidebar.slider(
        "Investimento em Marketing",
        min_value=int(df['Marketing'].min()),
        max_value=int(df['Marketing'].max() * 2),
        step=500,
        value=int(df['Marketing'].median())
    )

    # Prever com os dados da simulação
    receita_prevista = model.predict([[vendas_input, marketing_input]])[0]
    st.sidebar.metric("Receita Prevista para a Simulação", f"R$ {receita_prevista:,.2f}")
