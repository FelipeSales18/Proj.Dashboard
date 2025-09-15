import pandas as pd
import numpy as np
import random

# Define semente para reprodutibilidade
np.random.seed(42)
random.seed(42)

# Número de linhas de dados
n = 1000

# --- ESTRUTURAS DE DADOS MAIS REALISTAS ---

# 1. Produtos, Categorias e Preços Base
produtos_por_categoria = {
    "Eletrônicos": {"Smartphone": 2500, "Notebook": 5500, "Smart TV": 3200, "Fone de Ouvido": 350, "Tablet": 1800},
    "Vestuário": {"Camiseta": 80, "Calça Jeans": 150, "Tênis": 250, "Jaqueta": 300, "Vestido": 180},
    "Alimentos e Bebidas": {"Café Especial": 50, "Vinho Tinto": 90, "Chocolate Artesanal": 30, "Azeite Extra Virgem": 45},
    "Móveis e Decoração": {"Cadeira de Escritório": 700, "Mesa de Jantar": 1200, "Luminária": 150, "Sofá": 2800},
    "Saúde e Beleza": {"Perfume": 280, "Creme Hidratante": 60, "Protetor Solar": 55, "Shampoo": 40}
}

# 2. Vendedores com especialidades (maior probabilidade de vender certas categorias)
vendedores = {
    "Ana Silva": ["Eletrônicos", "Móveis e Decoração"],
    "Carlos Oliveira": ["Vestuário", "Saúde e Beleza"],
    "Fernanda Lima": ["Alimentos e Bebidas", "Saúde e Beleza"],
    "João Pereira": ["Eletrônicos"],
    "Marcos Andrade": ["Móveis e Decoração"],
    "Patrícia Costa": ["Vestuário"],
    "Beatriz Martins": ["Eletrônicos", "Saúde e Beleza"],
    "Ricardo Souza": ["Alimentos e Bebidas", "Móveis e Decoração"]
}
lista_vendedores = list(vendedores.keys())

# 3. Outras listas
regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
canais_venda = ["Online", "Loja Física", "Distribuidor", "Telefone"]
formas_pagamento = ["Cartão de Crédito", "PIX", "Boleto", "Dinheiro"]

# --- GERAÇÃO DE DADOS EM LOOP PARA CRIAR RELAÇÕES ---

data_list = []
start_date = pd.to_datetime("2023-01-01")

for i in range(n):
    # Escolha da Categoria e Produto
    categoria = random.choice(list(produtos_por_categoria.keys()))
    produto_info = produtos_por_categoria[categoria]
    produto_nome = random.choice(list(produto_info.keys()))
    preco_base = produto_info[produto_nome]

    # Vendedor com viés para sua especialidade
    vendedor_sorteado = random.choice(lista_vendedores)
    if categoria in vendedores[vendedor_sorteado]:
        # Aumenta a chance de ser o vendedor sorteado se for sua especialidade
        vendedor_final = np.random.choice([vendedor_sorteado, random.choice(lista_vendedores)], p=[0.75, 0.25])
    else:
        vendedor_final = vendedor_sorteado

    # Quantidade vendida (com variação e tendência de aumento ao longo do tempo)
    quantidade = np.random.randint(1, 10) + int(i / 100) # Adiciona um pequeno crescimento

    # Variação de preço e custo
    preco_unitario = round(preco_base * np.random.uniform(0.95, 1.1), 2)
    custo_unitario = round(preco_unitario * np.random.uniform(0.55, 0.75), 2)

    # Cálculo da Receita Bruta
    receita_bruta = preco_unitario * quantidade

    # Desconto
    desconto_percentual = random.choices([0, 5, 10, 15, 20], weights=[40, 30, 15, 10, 5], k=1)[0]
    receita_liquida = receita_bruta * (1 - desconto_percentual / 100)
    
    # Custo Total e Lucro
    custo_total = custo_unitario * quantidade
    lucro = receita_liquida - custo_total
    
    data_list.append({
        "Data": start_date + pd.Timedelta(days=i),
        "Regiao": random.choices(regioes, weights=[45, 20, 20, 10, 5], k=1)[0],
        "Vendedor": vendedor_final,
        "Categoria_Produto": categoria,
        "Produto": produto_nome,
        "Canal_Venda": random.choices(canais_venda, weights=[50, 30, 15, 5], k=1)[0],
        "Forma_Pagamento": random.choices(formas_pagamento, weights=[50, 30, 15, 5], k=1)[0],
        "Quantidade": quantidade,
        "Preco_Unitario": preco_unitario,
        "Receita_Bruta": receita_bruta,
        "Desconto(%)": desconto_percentual,
        "Receita_Liquida": receita_liquida,
        "Custo_Unitario": custo_unitario,
        "Custo_Total": custo_total,
        "Lucro": lucro,
        "Cliente_VIP": np.random.choice([0, 1], p=[0.8, 0.2])
    })

# Criar DataFrame a partir da lista de dicionários
df = pd.DataFrame(data_list)

# Renomear a coluna de Receita_Liquida para Vendas para manter a compatibilidade com o dashboard
df.rename(columns={"Receita_Liquida": "Vendas"}, inplace=True)


# Definir nome do arquivo
output_filename = "dados_vendas_realistas.xlsx"

# Salvar no Excel
df.to_excel(output_filename, index=False, engine="openpyxl")

print(f"Arquivo '{output_filename}' criado com sucesso!")
print("Este arquivo contém dados mais complexos e realistas para testar seu dashboard.")