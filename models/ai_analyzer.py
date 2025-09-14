import pandas as pd
import numpy as np

def analyze_dataframe(df):
    """
    Realiza uma análise exploratória completa em um DataFrame e gera um relatório textual.

    Args:
        df (pd.DataFrame): O DataFrame a ser analisado.

    Returns:
        tuple: Uma tupla contendo o relatório em markdown (str) e um dicionário com dados da análise.
    """
    report = []
    analysis_data = {}

    # 1. Visão Geral do Dataset
    report.append("1. Visão Geral do Dataset")
    num_rows, num_cols = df.shape
    report.append(f"- Número de Linhas: {num_rows}")
    report.append(f"- Número de Colunas: {num_cols}")
    
    # 2. Tipos de Colunas
    report.append("\n2. Tipos de Colunas")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
    
    report.append(f"- Colunas Numéricas ({len(numeric_cols)}): {', '.join(numeric_cols)}")
    report.append(f"- Colunas Categóricas ({len(categorical_cols)}): {', '.join(categorical_cols)}")
    report.append(f"- Colunas de Data/Hora ({len(datetime_cols)}): {', '.join(datetime_cols)}")
    
    analysis_data['numeric_cols'] = numeric_cols
    analysis_data['categorical_cols'] = categorical_cols
    analysis_data['datetime_cols'] = datetime_cols

    # 3. Análise de Correlação (apenas se houver colunas numéricas)
    if len(numeric_cols) > 1:
        report.append("\n3. Análise de Correlação")
        corr_matrix = df[numeric_cols].corr()
        analysis_data['corr_matrix'] = corr_matrix
        
        corr_pairs = corr_matrix.unstack().sort_values(ascending=False).drop_duplicates()
        high_corr = corr_pairs[(corr_pairs < 1) & (corr_pairs.abs() > 0.7)]
        
        if not high_corr.empty:
            report.append("Foram encontradas as seguintes correlações fortes (positivas ou negativas):")
            for (col1, col2), val in high_corr.items():
                tipo = "positiva" if val > 0 else "negativa"
                report.append(f'  - "{col1}" e "{col2}": Correlação {tipo} de {val:.2f}.')
        else:
            report.append("- Nenhuma correlação forte (acima de 0.7) foi encontrada.")

    # 4. Análise de Outliers
    if numeric_cols:
        report.append("\n4. Análise de Outliers")
        outliers_found = False
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            if not outliers.empty:
                report.append(f'- A coluna "{col}" parece ter {len(outliers)} valor(es) atípico(s).')
                outliers_found = True
        
        if not outliers_found:
            report.append("- Nenhuma coluna parece ter outliers significativos.")

    # 5. Análise de Destaques (Top Categorias)
    if categorical_cols and numeric_cols:
        report.append("\n5. Análise de Destaques")
        # Usar 'Vendas' ou 'Receita' como métrica principal, se existirem
        metric_col = next((col for col in ['Vendas', 'Receita_Liquida', 'Receita'] if col in numeric_cols), numeric_cols[0])
        report.append(f'Analisando os destaques com base na coluna "{metric_col}":')

        for cat_col in categorical_cols:
            if df[cat_col].nunique() > 1: # Analisa apenas se houver mais de uma categoria
                top_performer = df.groupby(cat_col)[metric_col].sum().idxmax()
                report.append(f'- Em "{cat_col}", a categoria com maior volume de "{metric_col}" é "{top_performer}".')

    # 6. Destaques de Vendas (Vendedores e Produtos)
    if 'Vendedor' in df.columns and 'Vendas' in df.columns:
        report.append("\n6. Destaques de Vendas")
        
        # Vendedores que mais compraram
        top_sellers = df.groupby('Vendedor')['Vendas'].sum().nlargest(5)
        report.append("\nTop 5 Vendedores por Vendas:")
        for seller, total_sales in top_sellers.items():
            report.append(f"- {seller}: R$ {total_sales:,.2f}")
        analysis_data['top_sellers'] = top_sellers

    if 'Categoria_Produto' in df.columns and 'Vendas' in df.columns:
        # Produtos que mais venderam
        top_products = df.groupby('Categoria_Produto')['Vendas'].sum().nlargest(5)
        report.append("\nTop 5 Produtos Mais Vendidos:")
        for product, total_sales in top_products.items():
            report.append(f"- {product}: R$ {total_sales:,.2f}")
        analysis_data['top_products'] = top_products
        
        # Produtos que menos venderam
        bottom_products = df.groupby('Categoria_Produto')['Vendas'].sum().nsmallest(5)
        report.append("\nTop 5 Produtos Menos Vendidos:")
        for product, total_sales in bottom_products.items():
            report.append(f"- {product}: R$ {total_sales:,.2f}")
        analysis_data['bottom_products'] = bottom_products

    return "\n".join(report), analysis_data