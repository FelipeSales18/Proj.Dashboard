import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_visualizations(df, analysis_data):
    """
    Renderiza os componentes de visualização de dados de forma interativa.

    Args:
        df (pd.DataFrame): O DataFrame com os dados.
        analysis_data (dict): Dicionário com os resultados da análise da IA.
    """
    numeric_cols = analysis_data.get('numeric_cols', [])
    categorical_cols = analysis_data.get('categorical_cols', [])
    datetime_cols = analysis_data.get('datetime_cols', [])

    # Cria abas para organizar as visualizações
    tab1, tab2, tab3, tab4 = st.tabs(["Análise Univariada", "Análise Bivariada", "Análise Temporal", "Destaques de Vendas"])

    # Aba 1: Análise de uma variável por vez
    with tab1:
        st.markdown("#### Distribuição de Colunas Numéricas")
        if not numeric_cols:
            st.warning("Nenhuma coluna numérica para exibir histograma.")
        else:
            col_dist = st.selectbox("Selecione uma coluna numérica:", numeric_cols)
            if col_dist:
                fig_hist = px.histogram(df, x=col_dist, title=f'Distribuição de {col_dist}', nbins=30)
                st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("---")
        st.markdown("#### Análise de Colunas Categóricas")
        if not categorical_cols:
             st.warning("Nenhuma coluna categórica para analisar.")
        else:
            col_cat = st.selectbox("Selecione uma coluna categórica:", categorical_cols)
            
            chart_type = st.radio(
                "Escolha o tipo de gráfico:",
                ("Gráfico de Barras", "Gráfico de Pizza"),
                horizontal=True
            )

            if col_cat:
                counts = df[col_cat].value_counts().nlargest(10) # Limita às 10 maiores categorias
                counts_df = counts.reset_index()
                counts_df.columns = [col_cat, 'Contagem']

                if chart_type == "Gráfico de Barras":
                    fig_bar = px.bar(counts_df, x=col_cat, y='Contagem', title=f'Contagem em {col_cat}')
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                elif chart_type == "Gráfico de Pizza":
                    fig_pie = px.pie(counts_df, names=col_cat, values='Contagem', title=f'Distribuição em {col_cat}')
                    st.plotly_chart(fig_pie, use_container_width=True)

    # Aba 2: Relação entre duas variáveis
    with tab2:
        st.markdown("#### Relação entre Colunas Numéricas (Gráfico de Dispersão)")
        if len(numeric_cols) < 2:
            st.warning("São necessárias pelo menos duas colunas numéricas para um gráfico de dispersão.")
        else:
            col1, col2 = st.columns(2)
            x_axis = col1.selectbox("Selecione o eixo X:", numeric_cols, index=0)
            y_axis = col2.selectbox("Selecione o eixo Y:", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
            
            if x_axis and y_axis:
                fig_scatter = px.scatter(df, x=x_axis, y=y_axis, title=f'{y_axis} vs. {x_axis}', trendline="ols")
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### Mapa de Calor de Correlação")
        if 'corr_matrix' in analysis_data:
            corr_matrix = analysis_data['corr_matrix']
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmin=-1,
                zmax=1
            ))
            fig_heatmap.update_layout(title="Mapa de Calor de Correlação")
            st.plotly_chart(fig_heatmap, use_container_width=True)

    # Aba 3: Análise ao longo do tempo
    with tab3:
        st.markdown("#### Série Temporal")
        if not datetime_cols or not numeric_cols:
            st.warning("Para análise temporal, é necessária pelo menos uma coluna de data e uma numérica.")
        else:
            col1, col2 = st.columns(2)
            time_col = col1.selectbox("Selecione a coluna de tempo:", datetime_cols)
            value_col_time = col2.selectbox("Selecione a coluna de valor:", numeric_cols)
            
            if time_col and value_col_time:
                df_sorted = df.sort_values(by=time_col)
                fig_line = px.line(df_sorted, x=time_col, y=value_col_time, title=f'{value_col_time} ao longo do tempo', markers=True)
                st.plotly_chart(fig_line, use_container_width=True)

    # Aba 4: Destaques de Vendas
    with tab4:
        st.markdown("#### Desempenho de Vendedores e Produtos")

        if 'top_sellers' in analysis_data:
            st.markdown("##### Top 5 Vendedores com Mais Vendas")
            top_sellers = analysis_data['top_sellers']
            top_sellers_df = top_sellers.reset_index()
            top_sellers_df.columns = ['Vendedor', 'Total de Vendas']
            fig = px.bar(top_sellers_df, x='Vendedor', y='Total de Vendas', title='Top 5 Vendedores por Vendas')
            st.plotly_chart(fig, use_container_width=True)

        if 'top_products' in analysis_data:
            st.markdown("##### Top 5 Produtos Mais Vendidos")
            top_products = analysis_data['top_products']
            top_products_df = top_products.reset_index()
            top_products_df.columns = ['Produto', 'Total de Vendas']
            fig = px.bar(top_products_df, x='Produto', y='Total de Vendas', title='Top 5 Produtos Mais Vendidos')
            st.plotly_chart(fig, use_container_width=True)

        if 'bottom_products' in analysis_data:
            st.markdown("##### Top 5 Produtos Menos Vendidos")
            bottom_products = analysis_data['bottom_products']
            bottom_products_df = bottom_products.reset_index()
            bottom_products_df.columns = ['Produto', 'Total de Vendas']
            fig = px.bar(bottom_products_df, x='Produto', y='Total de Vendas', title='Top 5 Produtos Menos Vendidos')
            st.plotly_chart(fig, use_container_width=True)