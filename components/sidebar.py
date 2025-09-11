import streamlit as st

def show_sidebar():
    """
    Renderiza a barra lateral do dashboard e o uploader de arquivos.
    
    Returns:
        O objeto de arquivo carregado pelo usuário.
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
