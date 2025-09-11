import pandas as pd
import numpy as np

# Define semente para reprodutibilidade
np.random.seed(42)

# Número de linhas de dados
n = 200

# Criar dados simulados
data = {
    "Data": pd.date_range("2023-01-01", periods=n, freq="D"),  # dias
    "Regiao": np.random.choice(["Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste"], n),
    "Categoria_Produto": np.random.choice(["Eletrônicos", "Vestuário", "Alimentos", "Móveis", "Serviços"], n),
    "Vendedor": np.random.choice(["Ana", "Carlos", "Fernanda", "João", "Marcos", "Patrícia"], n),
    "Canal_Venda": np.random.choice(["Online", "Loja Física", "Distribuidor"], n),
    "Forma_Pagamento": np.random.choice(["Cartão de Crédito", "Boleto", "PIX", "Dinheiro"], n),
    "Vendas": np.random.randint(100, 2000, n),
    "Marketing": np.random.randint(500, 10000, n),
    "Desconto(%)": np.random.choice([0, 5, 10, 15, 20], n)
}

# Criar DataFrame
df = pd.DataFrame(data)

# Criar coluna de Receita simulada (considerando desconto e investimento em marketing)
df["Receita_Bruta"] = df["Vendas"] * 50 + df["Marketing"] * 0.3
df["Receita_Liquida"] = df["Receita_Bruta"] * (1 - df["Desconto(%)"]/100)

# Adicionar coluna de "Cliente VIP" (exemplo de binária)
df["Cliente_VIP"] = np.random.choice([0, 1], n, p=[0.7, 0.3])  # 30% são VIPs

# Definir nome do arquivo
output_filename = "dados_teste_completos.xlsx"

# Salvar no Excel
df.to_excel(output_filename, index=False, engine="openpyxl")

print(f"Arquivo '{output_filename}' criado com sucesso!")
print("Você já pode usá-lo para testar seu dashboard com dados mais complexos.")
