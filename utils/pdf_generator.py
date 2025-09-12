import pandas as pd
from fpdf import FPDF
import plotly.express as px
import tempfile
import os
from datetime import datetime

# Classe para criar o PDF com cabeçalho e rodapé personalizados
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Análise de Dados com IA', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_pdf_report(report_text, df, analysis_data):
    """
    Cria um relatório completo em PDF contendo o texto da análise e os gráficos.

    Args:
        report_text (str): O texto gerado pela análise da IA.
        df (pd.DataFrame): O DataFrame original.
        analysis_data (dict): O dicionário com os dados da análise (incluindo os dataframes dos tops).

    Returns:
        bytes: O conteúdo do arquivo PDF gerado.
    """
    pdf = PDF()
    pdf.add_page()
    
    # Adiciona o Título e a data
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Análise e Insights da IA', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 1, 'L')
    pdf.ln(10)

    # Adiciona o relatório textual da IA
    pdf.set_font('Arial', '', 12)
    # Usamos 'multi_cell' para que o texto quebre a linha automaticamente
    # O encode('latin-1', 'replace') ajuda a evitar erros com caracteres especiais
    pdf.multi_cell(0, 5, report_text.encode('latin-1', 'replace').decode('latin-1'))
    
    # --- Seção de Gráficos ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Visualizações dos Dados', 0, 1, 'L')
    pdf.ln(5)

    # Diretório temporário para salvar as imagens dos gráficos
    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = []

        # Gerar e salvar cada gráfico como uma imagem
        
        # Gráfico de Vendedores
        if 'top_sellers' in analysis_data:
            top_sellers = analysis_data['top_sellers']
            fig = px.bar(top_sellers, x=top_sellers.index, y=top_sellers.values, title='Top 5 Vendedores por Vendas', labels={'x': 'Vendedor', 'y': 'Total de Vendas'})
            path = os.path.join(temp_dir, 'top_sellers.png')
            fig.write_image(path, width=800, height=500)
            image_paths.append(('Top 5 Vendedores com Mais Vendas', path))

        # Gráfico de Produtos Mais Vendidos
        if 'top_products' in analysis_data:
            top_products = analysis_data['top_products']
            fig = px.bar(top_products, x=top_products.index, y=top_products.values, title='Top 5 Produtos Mais Vendidos', labels={'x': 'Produto', 'y': 'Total de Vendas'})
            path = os.path.join(temp_dir, 'top_products.png')
            fig.write_image(path, width=800, height=500)
            image_paths.append(('Top 5 Produtos Mais Vendidos', path))

        # Gráfico de Produtos Menos Vendidos
        if 'bottom_products' in analysis_data:
            bottom_products = analysis_data['bottom_products']
            fig = px.bar(bottom_products, x=bottom_products.index, y=bottom_products.values, title='Top 5 Produtos Menos Vendidos', labels={'x': 'Produto', 'y': 'Total de Vendas'})
            path = os.path.join(temp_dir, 'bottom_products.png')
            fig.write_image(path, width=800, height=500)
            image_paths.append(('Top 5 Produtos Menos Vendidos', path))
            
        # Adicionar as imagens ao PDF
        for title, path in image_paths:
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, title, 0, 1, 'L')
            pdf.image(path, w=180) # Largura da imagem no PDF
            pdf.ln(10)

    # Retorna o PDF como uma string de bytes
    return pdf.output(dest='S').encode('latin-1')