import streamlit as st
import pandas as pd

@st.cache_data # Usa o cache do Streamlit para otimizar o carregamento
def load_data(uploaded_file):
    """
    Carrega dados de um arquivo Excel (xlsx, xls) carregado via Streamlit.
    
    Args:
        uploaded_file: O objeto de arquivo do Streamlit.

    Returns:
        Um DataFrame do pandas se o carregamento for bem-sucedido, None caso contrário.
    """
    if uploaded_file is None:
        return None
        
    try:
        # Tenta ler o arquivo Excel. O engine 'openpyxl' é bom para .xlsx.
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        # Tenta converter colunas que parecem datas para o formato datetime
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
                except (ValueError, TypeError):
                    # Se não for uma data, mantém como está
                    pass
        
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        st.warning("Por favor, verifique se o arquivo é um Excel (.xlsx ou .xls) válido.")
        return None
