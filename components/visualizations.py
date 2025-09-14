import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_visualizations(df, analysis_data):
    """
    Renderiza os componentes de visualização de dados de forma interativa.
    """
    generated_charts = {}
    numeric_cols = analysis_data.get('numeric_cols', [])
    categorical_cols = analysis_data.get('categorical_cols', [])
    datetime_cols = analysis_data.get('datetime_cols', [])
    all_cols = numeric_cols + categorical_cols

    color_palette = px.colors.qualitative.Plotly

    tab1, tab2, tab3, tab4 = st.tabs(["Análise Univariada", "Análise Bivariada", "Análise Temporal", "Destaques de Vendas"])

    # --- ABA 1: ANÁLISE UNIVARIADA (sem alterações) ---
    with tab1:
        st.markdown("#### Distribuição de Colunas Numéricas")
        if not numeric_cols:
            st.warning("Nenhuma coluna numérica para exibir histograma.")
        else:
            col_dist = st.selectbox("Selecione uma coluna numérica:", numeric_cols, key="univar_num")
            if col_dist:
                fig_hist = px.histogram(df, x=col_dist, title=f'Distribuição de {col_dist}', nbins=30,
                                        color_discrete_sequence=[color_palette[0]])
                st.plotly_chart(fig_hist, use_container_width=True)
                generated_charts['distribuicao_numerica'] = fig_hist

        st.markdown("---")
        st.markdown("#### Análise de Colunas Categóricas")
        if not categorical_cols:
             st.warning("Nenhuma coluna categórica para analisar.")
        else:
            col_cat = st.selectbox("Selecione uma coluna categórica:", categorical_cols, key="univar_cat")
            chart_type = st.radio("Escolha o tipo de gráfico:", ("Gráfico de Barras", "Gráfico de Pizza"), horizontal=True)
            if col_cat:
                counts = df[col_cat].value_counts().nlargest(10)
                counts_df = counts.reset_index()
                counts_df.columns = [col_cat, 'Contagem']
                if chart_type == "Gráfico de Barras":
                    fig_bar = px.bar(counts_df, x=col_cat, y='Contagem', title=f'Contagem em {col_cat}', color=col_cat, color_discrete_sequence=color_palette)
                    st.plotly_chart(fig_bar, use_container_width=True)
                    generated_charts['analise_categorica'] = fig_bar
                elif chart_type == "Gráfico de Pizza":
                    fig_pie = px.pie(counts_df, names=col_cat, values='Contagem', title=f'Distribuição em {col_cat}', color_discrete_sequence=color_palette)
                    st.plotly_chart(fig_pie, use_container_width=True)
                    generated_charts['analise_categorica'] = fig_pie

    # --- ABA 2: ANÁLISE BIVARIADA (com a nova funcionalidade) ---
    with tab2:
        st.markdown("#### Relação entre Duas Variáveis")
        
        if len(all_cols) < 2:
            st.warning("São necessárias pelo menos duas colunas para a análise bivariada.")
        else:
            col1, col2 = st.columns(2)
            x_axis_col = col1.selectbox("Selecione a coluna para o Eixo X:", all_cols, index=0)
            y_axis_col = col2.selectbox("Selecione a coluna para o Eixo Y:", all_cols, index=1)

            if x_axis_col and y_axis_col:
                # Caso 1: Numérica vs. Numérica
                if x_axis_col in numeric_cols and y_axis_col in numeric_cols:
                    st.markdown("##### Gráfico de Dispersão")
                    fig_scatter = px.scatter(df, x=x_axis_col, y=y_axis_col, title=f'{y_axis_col} vs. {x_axis_col}', trendline="ols")
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    generated_charts['bivariada_scatter'] = fig_scatter

                # Caso 2: Categórica vs. Numérica
                elif (x_axis_col in categorical_cols and y_axis_col in numeric_cols) or \
                     (x_axis_col in numeric_cols and y_axis_col in categorical_cols):
                    
                    # Garante que a categórica esteja no eixo X
                    cat_col = x_axis_col if x_axis_col in categorical_cols else y_axis_col
                    num_col = y_axis_col if y_axis_col in numeric_cols else x_axis_col

                    plot_type = st.radio("Escolha o tipo de gráfico:", ("Boxplot", "Gráfico de Barras (Média)"), horizontal=True)
                    
                    if plot_type == "Boxplot":
                        st.markdown(f"##### Distribuição de '{num_col}' por '{cat_col}'")
                        fig_box = px.box(df, x=cat_col, y=num_col, title=f'Distribuição de {num_col} por {cat_col}', color=cat_col, color_discrete_sequence=color_palette)
                        st.plotly_chart(fig_box, use_container_width=True)
                        generated_charts['bivariada_box'] = fig_box

                    elif plot_type == "Gráfico de Barras (Média)":
                        st.markdown(f"##### Média de '{num_col}' por '{cat_col}' (Ordenado)")
                        # Calcula a média, ordena e pega as top 15 categorias
                        grouped_data = df.groupby(cat_col)[num_col].mean().sort_values(ascending=False).nlargest(15).reset_index()
                        fig_bar_mean = px.bar(grouped_data, x=cat_col, y=num_col, title=f'Média de {num_col} por {cat_col}', color=cat_col, color_discrete_sequence=color_palette)
                        st.plotly_chart(fig_bar_mean, use_container_width=True)
                        generated_charts['bivariada_bar_mean'] = fig_bar_mean
                
                # Caso 3: Categórica vs. Categórica
                elif x_axis_col in categorical_cols and y_axis_col in categorical_cols:
                    st.markdown("##### Mapa de Calor de Frequência")
                    crosstab = pd.crosstab(df[y_axis_col], df[x_axis_col])
                    fig_heatmap = go.Figure(data=go.Heatmap(
                        z=crosstab.values,
                        x=crosstab.columns,
                        y=crosstab.index,
                        colorscale='Blues'
                    ))
                    fig_heatmap.update_layout(title=f'Frequência de {y_axis_col} vs. {x_axis_col}')
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                    generated_charts['bivariada_heatmap'] = fig_heatmap
                
                else:
                    st.info("Selecione uma combinação válida de colunas.")


    # --- ABA 3: ANÁLISE TEMPORAL (sem alterações) ---
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
                generated_charts['serie_temporal'] = fig_line

    # --- ABA 4: DESTAQUES DE VENDAS (sem alterações) ---
    with tab4:
        st.markdown("#### Desempenho de Vendedores e Produtos")
        if 'top_sellers' in analysis_data:
            st.markdown("##### Top 5 Vendedores com Mais Vendas")
            top_sellers = analysis_data['top_sellers']
            top_sellers_df = top_sellers.reset_index()
            top_sellers_df.columns = ['Vendedor', 'Total de Vendas']
            fig = px.bar(top_sellers_df, x='Vendedor', y='Total de Vendas', title='Top 5 Vendedores por Vendas', color='Vendedor', color_discrete_sequence=color_palette)
            st.plotly_chart(fig, use_container_width=True)
            generated_charts['top_vendedores'] = fig

        if 'top_products' in analysis_data:
            st.markdown("##### Top 5 Produtos Mais Vendidos")
            top_products = analysis_data['top_products']
            top_products_df = top_products.reset_index()
            top_products_df.columns = ['Produto', 'Total de Vendas']
            fig = px.bar(top_products_df, x='Produto', y='Total de Vendas', title='Top 5 Produtos Mais Vendidos', color='Produto', color_discrete_sequence=color_palette)
            st.plotly_chart(fig, use_container_width=True)
            generated_charts['top_produtos'] = fig

        if 'bottom_products' in analysis_data:
            st.markdown("##### Top 5 Produtos Menos Vendidos")
            bottom_products = analysis_data['bottom_products']
            bottom_products_df = bottom_products.reset_index()
            bottom_products_df.columns = ['Produto', 'Total de Vendas']
            fig = px.bar(bottom_products_df, x='Produto', y='Total de Vendas', title='Top 5 Produtos Menos Vendidos', color='Produto', color_discrete_sequence=color_palette)
            st.plotly_chart(fig, use_container_width=True)
            generated_charts['bottom_produtos'] = fig

    return generated_charts