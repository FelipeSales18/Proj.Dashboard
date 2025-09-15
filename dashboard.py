import streamlit as st
import pandas as pd
import re

from components import sidebar, visualizations
from utils import data_loader, pdf_generator
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
uploaded_file = sidebar.show_uploader_and_info()

if uploaded_file:
    df_original = data_loader.load_data(uploaded_file)

    if df_original is not None:
        # 🔹 Ajuste: converter automaticamente colunas de texto em categóricas
        for col in df_original.select_dtypes(include="object").columns:
            df_original[col] = df_original[col].astype("category")

        # --- RENDERIZA FILTROS DINÂMICOS NA SIDEBAR ---
        selected_filters = sidebar.show_filters(df_original)
        df = df_original.copy() # Cria uma cópia para aplicar os filtros

        # --- APLICA OS FILTROS AO DATAFRAME ---
        if selected_filters:
            # Filtro de data
            if 'date_range' in selected_filters:
                start_date, end_date = selected_filters['date_range']
                date_col = selected_filters['date_col']
                df[date_col] = pd.to_datetime(df[date_col])
                df = df[df[date_col].between(start_date, end_date)]

            # Filtros categóricos
            for col, values in selected_filters.items():
                if col not in ['date_range', 'date_col']:
                    df = df[df[col].isin(values)]
        
        st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso! Exibindo dados com base nos filtros selecionados.")
        
        with st.expander("Clique para ver uma amostra dos dados (já filtrados)"):
            st.dataframe(df.head())
        st.markdown("---")

        # --- 3. RESUMO EXECUTIVO (KPIs) ---
        st.subheader("🚀 Resumo Executivo")
        
        kpi_metrics = {}
        if 'Vendas' in df.columns:
            kpi_metrics['Total de Vendas'] = ('Vendas', 'sum')
        if 'Receita_Liquida' in df.columns:
            kpi_metrics['Total de Receita'] = ('Receita_Liquida', 'sum')
        if 'Vendedor' in df.columns:
            kpi_metrics['Vendedores Únicos'] = ('Vendedor', 'nunique')

        if kpi_metrics:
            cols = st.columns(len(kpi_metrics))
            i = 0
            for label, (col_name, metric_type) in kpi_metrics.items():
                col_metric = cols[i]
                if metric_type == 'sum':
                    value = df[col_name].sum()
                    col_metric.metric(label=label, value=f"R$ {value:,.2f}")
                elif metric_type == 'nunique':
                    value = df[col_name].nunique()
                    col_metric.metric(label=label, value=value)
                i += 1
        else:
            st.info("Não foram encontradas colunas como 'Vendas', 'Receita_Liquida' ou 'Vendedor' para gerar KPIs automaticamente.")
        st.markdown("---")

        # --- 4. ANÁLISE AUTOMÁTICA DA IA ---
        st.subheader("🤖 Análise e Insights da IA")

        # Cria a barra de progresso e o espaço para o texto
        progress_bar = st.progress(0)
        progress_text = st.empty()

        def progress_callback(progress, message):
            progress_bar.progress(progress)
            progress_text.text(message)

        try:
            # Passa a função de callback para o analisador
            analysis_report, analysis_data = ai_analyzer.analyze_dataframe(df, progress_callback)
            
            # Limpa a barra de progresso e a mensagem após a conclusão
            progress_text.empty()
            progress_bar.empty()

            st.markdown(analysis_report)
            st.markdown("---")

            st.subheader("📊 Explore Seus Dados")
            generated_charts = visualizations.render_visualizations(df, analysis_data)

            st.markdown("---")
            st.subheader("📄 Exportar Relatório")
            
            pdf_report_text = re.sub(r'###\s*|(\*\*|`)', '', analysis_report)
            pdf_bytes = pdf_generator.create_pdf_report(pdf_report_text, generated_charts)
            
            st.download_button(
                label="Baixar Relatório Completo em PDF",
                data=pdf_bytes,
                file_name=f"relatorio_analise_{uploaded_file.name}.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Ocorreu um erro durante a análise dos dados: {e}")
            st.warning("Verifique se o arquivo está formatado corretamente e tente novamente.")
            # Limpa a barra de progresso em caso de erro
            progress_text.empty()
            progress_bar.empty()

else:
    st.info("Aguardando o carregamento de um arquivo Excel para iniciar a análise.")