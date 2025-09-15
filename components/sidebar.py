import streamlit as st
import pandas as pd

def show_uploader_and_info():
    """
    Renderiza a parte estática da sidebar: cabeçalho, uploader e caixa de informação.
    Retorna o arquivo carregado.
    """
    st.sidebar.header("⚙️ Configurações")
    
    uploaded_file = st.sidebar.file_uploader(
        "Carregue sua planilha (Excel)",
        type=["xlsx", "xls"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Este dashboard utiliza IA para analisar automaticamente os dados de qualquer "
        "planilha Excel. Carregue um arquivo para começar."
    )
    
    return uploaded_file

def show_filters(df):
    """
    Renderiza os filtros dinâmicos com base no dataframe carregado.
    Retorna um dicionário com os filtros selecionados.
    """
    st.sidebar.header("🔍 Filtros Globais")
    
    selected_filters = {}

    # Filtro de data
    date_cols = df.select_dtypes(include=['datetime64[ns]', 'datetimetz']).columns.tolist()
    if date_cols:
        date_col = date_cols[0]
        min_date = df[date_col].min().date()
        max_date = df[date_col].max().date()

        date_range = st.sidebar.date_input(
            f"Filtro por {date_col}",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key=f"date_filter_{date_col}" # Adicionar chave única é uma boa prática
        )
        if len(date_range) == 2:
            selected_filters['date_range'] = (pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
            selected_filters['date_col'] = date_col

    # Filtros para colunas categóricas
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    for col in categorical_cols:
        if df[col].nunique() > 0 and df[col].nunique() < 20: 
            options = sorted(df[col].unique().tolist())
            selected = st.sidebar.multiselect(f"Filtro por {col}", options, default=options)
            selected_filters[col] = selected
            
    return selected_filters