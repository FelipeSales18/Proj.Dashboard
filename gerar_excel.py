import pandas as pd
import numpy as np

# Define a semente para resultados reproduzíveis
np.random.seed(42)

# Cria o dicionário de dados
data = {
    "Mes": pd.to_datetime(pd.date_range("2023-01-01", periods=24, freq="M")),
    "Vendas": np.random.randint(200, 1000, 24),
    "Marketing": np.random.randint(1000, 5000, 24)
}

# Cria o DataFrame
df = pd.DataFrame(data)

# Calcula a coluna 'Receita' com base nas outras colunas
df["Receita"] = df["Vendas"] * 50 + df["Marketing"] * 0.3

# Formata a coluna 'Mes' para aparecer apenas a data no Excel
df['Mes'] = df['Mes'].dt.date

# Define o nome do arquivo de saída
output_filename = 'dados_teste.xlsx'

# Salva o DataFrame em um arquivo Excel
# O argumento index=False impede que o pandas escreva o índice do DataFrame no arquivo
df.to_excel(output_filename, index=False, engine='openpyxl')

print(f"Arquivo '{output_filename}' criado com sucesso!")
print("Você já pode usá-lo para testar o seu dashboard.")
