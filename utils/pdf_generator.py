import pandas as pd
from fpdf import FPDF
import plotly.graph_objects as go
import tempfile
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Define o cabeçalho com um fundo azul e texto branco
        self.set_fill_color(24, 69, 117) # Cor azul escura
        self.set_text_color(255, 255, 255) # Cor branca
        self.set_font('Arial', 'B', 15)
        self.cell(0, 12, 'Relatório de Análise de Dados com IA', 0, 1, 'C', fill=True)
        self.ln(5)

    def footer(self):
        # Define o rodapé com o número da página
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        # Cria um título de seção destacado
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(230, 230, 230) # Cinza claro
        self.set_text_color(0, 0, 0) # Preto
        self.cell(0, 8, f' {title}', 0, 1, 'L', fill=True)
        self.ln(4)

    def chapter_body(self, body):
        # Adiciona o corpo do texto
        self.set_font('Arial', '', 11)
        # O encode/decode ajuda a evitar erros com caracteres especiais
        body_cleaned = body.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 5, body_cleaned)
        self.ln()

def create_pdf_report(report_text, generated_charts):
    """
    Cria um relatório completo em PDF contendo o texto da análise e os gráficos gerados na interface.

    Args:
        report_text (str): O texto gerado pela análise da IA.
        generated_charts (dict): Um dicionário contendo os gráficos (figuras Plotly) gerados.

    Returns:
        bytes: O conteúdo do arquivo PDF gerado.
    """
    pdf = PDF()
    pdf.add_page()

    # Adiciona a data da geração do relatório
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 1, 'L')
    pdf.ln(5)

    # Adiciona o relatório textual da IA
    pdf.chapter_title('1. Análise e Insights da IA')
    pdf.chapter_body(report_text)

    # --- Seção de Gráficos ---
    if generated_charts:
        pdf.add_page()
        pdf.chapter_title('2. Visualizações dos Dados')

        # Diretório temporário para salvar as imagens dos gráficos
        with tempfile.TemporaryDirectory() as temp_dir:
            for title, fig in generated_charts.items():
                if isinstance(fig, go.Figure): # Verifica se é uma figura Plotly válida
                    
                    # APLICA UM TEMA CLARO PARA GARANTIR AS CORES NO PDF
                    fig.update_layout(template='plotly_white')
                    
                    # Salva a figura como imagem
                    path = os.path.join(temp_dir, f'{title}.png')
                    fig.write_image(path, width=800, height=500, scale=2)

                    # Adiciona o título do gráfico e a imagem ao PDF
                    pdf.set_font('Arial', 'B', 12)
                    pdf.cell(0, 10, fig.layout.title.text, 0, 1, 'L') # Usa o título do próprio gráfico
                    pdf.image(path, w=170) # Largura da imagem no PDF
                    pdf.ln(10)

    # Retorna o PDF como bytes (corrigido)
    return bytes(pdf.output(dest='S'))