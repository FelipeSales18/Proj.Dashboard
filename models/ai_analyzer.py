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
    report.append("### 1. Visão Geral do Dataset")
    num_rows, num_cols = df.shape
    report.append(f"- **Número de Linhas:** {num_rows}")
    report.append(f"- **Número de Colunas:** {num_cols}")
    
    # 2. Tipos de Colunas
    report.append("\n### 2. Tipos de Colunas")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
    
    report.append(f"- **Colunas Numéricas ({len(numeric_cols)}):** `{', '.join(numeric_cols)}`")
    report.append(f"- **Colunas Categóricas ({len(categorical_cols)}):** `{', '.join(categorical_cols)}`")
    report.append(f"- **Colunas de Data/Hora ({len(datetime_cols)}):** `{', '.join(datetime_cols)}`")
    
    analysis_data['numeric_cols'] = numeric_cols
    analysis_data['categorical_cols'] = categorical_cols
    analysis_data['datetime_cols'] = datetime_cols

    # 3. Análise de Correlação (apenas se houver colunas numéricas)
    if len(numeric_cols) > 1:
        report.append("\n### 3. Análise de Correlação")
        corr_matrix = df[numeric_cols].corr()
        analysis_data['corr_matrix'] = corr_matrix
        
        # Encontra os pares mais correlacionados (excluindo a correlação de uma coluna com ela mesma)
        corr_pairs = corr_matrix.unstack().sort_values(ascending=False).drop_duplicates()
        high_corr = corr_pairs[(corr_pairs < 1) & (corr_pairs.abs() > 0.7)]
        
        if not high_corr.empty:
            report.append("Foram encontradas as seguintes correlações fortes (positivas ou negativas):")
            for (col1, col2), val in high_corr.items():
                tipo = "positiva" if val > 0 else "negativa"
                report.append(f"  - **`{col1}`** e **`{col2}`**: Correlação {tipo} de `{val:.2f}`. Isso sugere uma forte relação entre elas.")
        else:
            report.append("- Nenhuma correlação forte (acima de 0.7 ou abaixo de -0.7) foi encontrada entre as colunas numéricas.")

    # 4. Análise de Outliers (Valores Atípicos)
    if numeric_cols:
        report.append("\n### 4. Análise de Outliers")
        outliers_found = False
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            if not outliers.empty:
                report.append(f"- A coluna **`{col}`** parece ter `{len(outliers)}` valor(es) atípico(s). Isso pode indicar erros de entrada ou eventos raros que merecem atenção.")
                outliers_found = True
        
        if not outliers_found:
            report.append("- Nenhuma coluna parece ter outliers significativos com base no método IQR.")

    # 5. Análise de Tendência Temporal
    if datetime_cols and numeric_cols:
        report.append("\n### 5. Análise de Tendência Temporal")
        date_col = datetime_cols[0] # Usa a primeira coluna de data para a análise
        report.append(f"Analisando tendências ao longo do tempo usando a coluna **`{date_col}`**:")
        
        for col in numeric_cols:
            # Uma forma simples de verificar tendência é correlacionar com o tempo
            df_sorted = df.sort_values(by=date_col)
            trend_corr = df_sorted[col].corr(df_sorted[date_col].astype('int64'))
            
            if abs(trend_corr) > 0.6:
                direcao = "crescimento" if trend_corr > 0 else "decréscimo"
                report.append(f"- A coluna **`{col}`** mostra uma forte tendência de **{direcao}** ao longo do tempo.")

    return "\n".join(report), analysis_data
