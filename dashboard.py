import streamlit as st
import pandas as pd

from components import sidebar, visualizations
from utils import data_loader, pdf_generator # Importe o novo módulo
from models import ai_analyzer

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Análise de Dados com IA",
    page_icon="🧠",
    layout="wide"
)

# --- TÍTULO E DESCRIÇÃO ---
st.title("🧠 Dashboard de Análise de Dados com IA")
st.markdown("""
Carregue qualquer planilha Excel e receba uma análise automática, insights e visualizações interativas.
A IA irá identificar padrões, correlações e pontos de atenção nos seus dados.
""")
st.markdown("---")

# --- 2. SIDEBAR E CARREGAMENTO DE DADOS ---
uploaded_file = sidebar.show_sidebar()

if uploaded_file:
    df = data_loader.load_data(uploaded_file)

    if df is not None:
        # 🔹 Ajuste: converter automaticamente colunas de texto em categóricas
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype("category")

        st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso! A análise será iniciada.")
        
        # Exibe um preview dos dados em um expander
        with st.expander("Clique para ver uma amostra dos dados carregados"):
            st.dataframe(df.head())
        st.markdown("---")

        # --- 3. ANÁLISE AUTOMÁTICA DA IA ---
        with st.spinner("Aguarde... A IA está analisando seus dados..."):
            try:
                analysis_report, analysis_data = ai_analyzer.analyze_dataframe(df)
                
                st.subheader("🤖 Análise e Insights da IA")
                st.markdown(analysis_report)
                st.markdown("---")

                # --- 4. VISUALIZAÇÕES INTERATIVAS ---
                st.subheader("📊 Explore Seus Dados")
                visualizations.render_visualizations(df, analysis_data)

                # --- 5. GERAÇÃO E DOWNLOAD DO PDF ---
                st.markdown("---")
                st.subheader("📄 Exportar Relatório")
                
                # Gera o PDF em memória quando o botão é clicado
                pdf_bytes = pdf_generator.create_pdf_report(analysis_report, df, analysis_data)
                
                st.download_button(
                    label="Baixar Relatório Completo em PDF",
                    data=pdf_bytes,
                    file_name=f"relatorio_analise_{uploaded_file.name}.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Ocorreu um erro durante a análise dos dados: {e}")
                st.warning("Verifique se o arquivo está formatado corretamente e tente novamente.")

else:
    st.info("Aguardando o carregamento de um arquivo Excel para iniciar a análise.")