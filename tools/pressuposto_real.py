#!/usr/bin/env python3
"""
Pressuposto real — traduz o orçamento fechado em caixa de produção.

    python3 tools/pressuposto_real.py --saida PRESSUPOSTO_JOB.xlsx
    python3 tools/pressuposto_real.py --config job.json --saida PRESSUPOSTO_JOB.xlsx
    python3 tools/pressuposto_real.py --exemplo job.json

Por que existe: orçamento é o que o cliente paga; pressuposto real é o que a
produção gasta. São dois documentos diferentes e a conta que liga um ao outro
(entrada bruta -> imposto -> entrada líquida -> saídas por área -> lucro) é
onde o erro passa despercebido quando se faz de cabeça, uma vez por job, num
arquivo novo. Aqui é sempre a mesma planilha, com as mesmas três abas.

A planilha gerada tem três abas e nenhuma a mais:

  RESUMO   entradas, imposto, saídas por área, lucro e caixa — tudo fórmula
  SAÍDAS   um gasto por linha; área escolhida numa listinha
  ÁREAS    a lista de áreas; escrever uma nova aqui já aparece no RESUMO

Regra de ouro do layout: quem preenche mexe só na aba SAÍDAS. O RESUMO se
atualiza sozinho, inclusive o que ainda não foi classificado em área — que
aparece numa linha própria em vez de sumir da conta.
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.drawing.image import Image as XLImage
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:  # pragma: no cover - dependência externa
    sys.exit("openpyxl não instalado. Rode: pip install openpyxl")

# Última linha útil das faixas de fórmula. Generoso de propósito: linha nova
# digitada no fim da tabela já entra nas somas, sem ninguém editar fórmula.
ULTIMA_LINHA = 500

# Nome das abas em ASCII: o mesmo arquivo circula por Excel, Google Sheets e
# LibreOffice, e nome de aba acentuado é onde a referência entre abas quebra.
ABA_RESUMO = "RESUMO"
ABA_SAIDAS = "SAIDAS"
ABA_AREAS = "AREAS"

# Primeira linha de dados de cada aba — fixa, porque as fórmulas dependem dela.
SAIDAS_INICIO = 6
AREAS_INICIO = 2

# As áreas que cobrem o gasto de uma produção de externa. Espelham os blocos
# que a YAD já usa no pressuposto (equipe, diversos, alimentação, transporte,
# locação, comissão) e acrescentam os dois que faltavam em job de estrada:
# hospedagem e manutenção do caminhão.
AREAS_PADRAO = [
    "EQUIPE",
    "TRANSPORTE E LOGÍSTICA",
    "ALIMENTAÇÃO",
    "HOSPEDAGEM",
    "EQUIPAMENTO E MANUTENÇÃO",
    "LOCAÇÃO DE TERCEIROS",
    "PRODUÇÃO E DIVERSOS",
    "COMISSÃO",
]

IMPOSTO_PADRAO = 16.0  # % sobre a entrada bruta

# Comissão de captação. A BASE muda o valor e é onde o combinado vira briga:
# "15% do job" pode ser sobre o que o cliente paga ou sobre o que sobra depois
# do imposto. Na novela vertical a diferença entre as duas leituras foi de
# R$ 5.400. Por isso a base é explícita no config e sai escrita na planilha.
COMISSAO_AREA = "COMISSÃO"
COMISSAO_BASES = {
    "liquida": ("entrada líquida", "liquida"),
    "bruta": ("entrada bruta", "bruta"),
}

# Linhas vazias sobrando no fim de cada bloco, para digitar sem inserir linha.
FOLGA_ENTRADAS = 3
FOLGA_AREAS = 3

MOEDA = 'R$ #,##0.00'
PORCENTO = '0.0%'
DATA = 'DD/MM/YYYY'

# Paleta amostrada do próprio logo: o gradiente vai de #7C3184 (roxo, ponta
# esquerda) a #5CA1DC (azul, ponta direita), passando por #6973B8 no meio.
# Faixa de seção usa o roxo escuro e cabeçalho de coluna o tom médio — mais
# escuro é hierarquia mais alta, e o documento inteiro fica na cor da marca.
TINTA = {
    "roxo": "7C3184",
    "roxo_escuro": "5B2A63",
    "meio": "6973B8",
    "azul": "5CA1DC",
    "escuro": "6973B8",      # cabeçalho de coluna
    "faixa": "5B2A63",       # faixa de seção
    "claro": "F7F5FA",
    "borda": "D6CEDE",
    "texto_fraco": "6B6478",
    "preencher": "FFF3C4",   # amarelo: célula que espera alguém digitar
    "resultado": "EDE4F3",   # lilás: linha de resultado
    "positivo": "E3F9E5",    # verde: lucro no azul
    "atencao": "FFE3E3",
}

# Dados da YAD, como aparecem no cabeçalho dos orçamentos. Sobrescrevíveis
# pelo bloco "empresa" do config.
EMPRESA_PADRAO = {
    "nome": "YAD FILMES PRODUÇÕES AUDIOVISUAIS LTDA",
    "endereco": "Av. Queiroz Filho, 1700 — Vila Hamburguesa, São Paulo — SP",
    "cnpj": "45.622.704/0001-34",
    "site": "yadfilmes.com",
    "instagram": "@yadfilmes",
    "telefone": "(12) 99119-0186",
}

# Logo relativo à raiz do repositório — nunca caminho absoluto.
LOGO_PADRAO = Path(__file__).resolve().parent / "assets" / "yad-logo.png"
LOGO_LADO_PX = 104

BRANCO = Font(color="FFFFFF", bold=True, size=11)
NEGRITO = Font(bold=True)
FINA = Side(style="thin", color=TINTA["borda"])
GRADE = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)


def _fill(cor: str) -> PatternFill:
    return PatternFill("solid", fgColor=cor)


def _data_br(valor):
    """Aceita 'dd/mm/aaaa', date ou vazio. Devolve date ou string original."""
    if valor in (None, ""):
        return None
    if isinstance(valor, (datetime.date, datetime.datetime)):
        return valor
    for formato in ("%d/%m/%Y", "%Y-%m-%d", "%d/%m/%y"):
        try:
            return datetime.datetime.strptime(str(valor).strip(), formato).date()
        except ValueError:
            continue
    return str(valor)  # texto livre tipo "PAGO" ou "05/07 e 22/07"


def _titulo(ws, celula: str, texto: str, tamanho: int = 16):
    ws[celula] = texto
    ws[celula].font = Font(bold=True, size=tamanho, color=TINTA["escuro"])


def _secao(ws, linha: int, texto: str, primeira: str, ultima: str):
    """Faixa escura de seção, mesclada de ponta a ponta."""
    ws.merge_cells(f"{primeira}{linha}:{ultima}{linha}")
    cel = ws[f"{primeira}{linha}"]
    cel.value = texto
    cel.font = BRANCO
    cel.fill = _fill(TINTA["faixa"])
    cel.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[linha].height = 22


def _logo(ws, ancora: str, lado_px: int = LOGO_LADO_PX, caminho: Path | None = None):
    """Fixa o logo numa célula. Falta do arquivo não derruba a geração."""
    arquivo = Path(caminho) if caminho else LOGO_PADRAO
    if not arquivo.is_file():
        return False
    img = XLImage(str(arquivo))
    img.width = img.height = lado_px  # o logo é quadrado
    img.anchor = ancora
    ws.add_image(img)
    return True


def _timbrado(ws, cfg: dict, primeira_linha: int = 1) -> int:
    """Logo à esquerda, bloco da empresa à direita. Devolve a linha seguinte."""
    empresa = {**EMPRESA_PADRAO, **(cfg.get("empresa") or {})}
    _logo(ws, f"B{primeira_linha}", caminho=cfg.get("logo"))

    linhas = [
        (empresa["nome"], Font(bold=True, size=12, color=TINTA["roxo_escuro"])),
        (empresa["endereco"], Font(size=9, color=TINTA["texto_fraco"])),
        (f"CNPJ {empresa['cnpj']}", Font(size=9, color=TINTA["texto_fraco"])),
        (f"{empresa['site']}  ·  {empresa['instagram']}  ·  {empresa['telefone']}",
         Font(size=9, color=TINTA["texto_fraco"])),
    ]
    for i, (texto, fonte) in enumerate(linhas):
        r = primeira_linha + i
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
        cel = ws.cell(row=r, column=3, value=texto)
        cel.font = fonte
        cel.alignment = Alignment(vertical="center")
    # O logo ocupa ~5 linhas de altura; garante que o bloco não fique por cima.
    for r in range(primeira_linha, primeira_linha + 5):
        ws.row_dimensions[r].height = 21
    return primeira_linha + 5


def _ficha(ws, cfg: dict, linha: int) -> int:
    """Quem fez, quem mexeu por último e em que versão. Devolve linha seguinte."""
    hoje = cfg.get("_hoje") or datetime.date.today()
    campos = [
        ("Elaborado por", cfg.get("elaborado_por", ""),
         "Em", _data_br(cfg.get("elaborado_em")) or hoje),
        ("Atualizado por", cfg.get("atualizado_por", cfg.get("elaborado_por", "")),
         "Em", _data_br(cfg.get("atualizado_em")) or hoje),
        ("Versão", cfg.get("versao", "v1"),
         "Situação", cfg.get("situacao", "EM ANDAMENTO")),
    ]
    for i, (rotulo, valor, rotulo2, valor2) in enumerate(campos):
        r = linha + i
        ws.cell(row=r, column=2, value=rotulo).font = Font(size=10, bold=True,
                                                           color=TINTA["texto_fraco"])
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        ws.cell(row=r, column=3, value=valor).font = Font(size=10)
        ws.cell(row=r, column=5, value=rotulo2).font = Font(size=10, bold=True,
                                                            color=TINTA["texto_fraco"])
        ws.cell(row=r, column=6, value=valor2).font = Font(size=10)
        if isinstance(valor2, datetime.date):
            ws.cell(row=r, column=6).number_format = DATA
        for col in range(2, 7):
            cel = ws.cell(row=r, column=col)
            cel.border = GRADE
            cel.fill = _fill(TINTA["claro"])
    return linha + len(campos)


def _impressao(ws, titulo: str, paisagem: bool = False):
    """Deixa pronto para virar PDF: cabe na largura, rodapé com job e página."""
    ws.page_setup.orientation = "landscape" if paisagem else "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.left.text = titulo[:80]
    ws.oddFooter.left.size = 8
    ws.oddFooter.right.text = "Página &P de &N"
    ws.oddFooter.right.size = 8


def _cabecalho(ws, linha: int, primeira_col: int, titulos: list[str]):
    for i, titulo in enumerate(titulos):
        cel = ws.cell(row=linha, column=primeira_col + i, value=titulo)
        cel.font = Font(bold=True, color="FFFFFF", size=10)
        cel.fill = _fill(TINTA["escuro"])
        cel.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
        cel.border = GRADE
    ws.row_dimensions[linha].height = 28


# --------------------------------------------------------------------------
# Aba ÁREAS
# --------------------------------------------------------------------------

def _aba_areas(wb: Workbook, areas: list[str]) -> int:
    ws = wb.create_sheet(ABA_AREAS)
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["C"].width = 62

    _cabecalho(ws, 1, 1, ["ÁREAS DE GASTO"])
    for i, area in enumerate(areas):
        cel = ws.cell(row=AREAS_INICIO + i, column=1, value=area)
        cel.border = GRADE
    # Folga para área nova. A linha em branco já está na faixa das fórmulas.
    for i in range(len(areas), len(areas) + FOLGA_AREAS + 2):
        ws.cell(row=AREAS_INICIO + i, column=1).border = GRADE
        ws.cell(row=AREAS_INICIO + i, column=1).fill = _fill(TINTA["preencher"])

    ws["C2"] = "Área nova? Escreva na primeira linha amarela."
    ws["C2"].font = NEGRITO
    ws["C3"] = "Ela aparece sozinha na listinha da aba SAÍDAS e vira uma linha no RESUMO."
    ws["C4"] = "Não apague área que já tem gasto lançado — o RESUMO perde a linha."
    for linha in (3, 4):
        ws[f"C{linha}"].alignment = Alignment(wrap_text=True)

    return len(areas) + FOLGA_AREAS + 2


# --------------------------------------------------------------------------
# Aba SAÍDAS
# --------------------------------------------------------------------------

def _aba_saidas(wb: Workbook, saidas: list[dict], total_areas: int, cfg: dict) -> int | None:
    ws = wb.create_sheet(ABA_SAIDAS)
    larguras = {"A": 2, "B": 26, "C": 34, "D": 26, "E": 9, "F": 15, "G": 15,
                "H": 13, "I": 14, "J": 30}
    for col, largura in larguras.items():
        ws.column_dimensions[col].width = largura

    _logo(ws, "J1", lado_px=48, caminho=cfg.get("logo"))
    _titulo(ws, "B2", "SAÍDAS — um gasto por linha")
    ws["B3"] = ("Como usar:  1) escreva o gasto numa linha vazia   "
                "2) escolha a ÁREA na listinha da célula   "
                "3) preencha QTD e VALOR UNITÁRIO — o TOTAL e o RESUMO se viram sozinhos.")
    ws["B3"].font = Font(italic=True, color="52606D")

    _cabecalho(ws, 5, 2, [
        "ÁREA", "DESCRIÇÃO / QUEM", "FUNÇÃO / DETALHE", "QTD",
        "VALOR UNITÁRIO", "TOTAL", "STATUS", "DATA PGTO", "OBS",
    ])
    ws.freeze_panes = "B6"

    for i, item in enumerate(saidas):
        linha = SAIDAS_INICIO + i
        ws.cell(row=linha, column=2, value=item.get("area", ""))
        ws.cell(row=linha, column=3, value=item.get("descricao", ""))
        ws.cell(row=linha, column=4, value=item.get("funcao", ""))
        qtd = item.get("qtd", "")
        unit = item.get("unit", "")
        ws.cell(row=linha, column=5, value=qtd if qtd != "" else None)
        ws.cell(row=linha, column=6, value=unit if unit != "" else None)
        ws.cell(row=linha, column=8, value=item.get("status", "A PAGAR"))
        ws.cell(row=linha, column=9, value=_data_br(item.get("data")))
        ws.cell(row=linha, column=10, value=item.get("obs", ""))

    # Fórmula de TOTAL e formatação vão até o fim da faixa, não até o fim dos
    # dados: linha digitada depois já nasce calculando.
    for linha in range(SAIDAS_INICIO, ULTIMA_LINHA + 1):
        ws.cell(row=linha, column=7).value = (
            f'=IF(OR(E{linha}="",F{linha}=""),"",ROUND(E{linha}*F{linha},2))'
        )
        for col in range(2, 11):
            cel = ws.cell(row=linha, column=col)
            cel.border = GRADE
            if col in (6, 7):
                cel.number_format = MOEDA
            elif col == 5:
                cel.alignment = Alignment(horizontal="center")
            elif col == 9:
                cel.number_format = DATA
                cel.alignment = Alignment(horizontal="center")
            elif col == 8:
                cel.alignment = Alignment(horizontal="center")
        # Amarelo em quem espera digitação; TOTAL é fórmula, fica cinza claro.
        for col in (5, 6):
            if ws.cell(row=linha, column=col).value in (None, ""):
                ws.cell(row=linha, column=col).fill = _fill(TINTA["preencher"])
        ws.cell(row=linha, column=7).fill = _fill(TINTA["claro"])

    # `formula1` vai SEM o `=` inicial — com ele o OOXML sai inválido e o
    # arquivo não abre no LibreOffice. showDropDown=False é o que exibe a
    # setinha: o atributo do OOXML é invertido em relação ao nome.
    fim_areas = AREAS_INICIO + total_areas - 1
    lista_areas = DataValidation(
        type="list", formula1=f"'{ABA_AREAS}'!$A${AREAS_INICIO}:$A${fim_areas}",
        allow_blank=True, showDropDown=False,
        showErrorMessage=True, errorStyle="warning",
    )
    lista_areas.error = ("Essa área não está na lista. Se for nova, acrescente "
                         "na aba ÁREAS para ela aparecer no RESUMO.")
    lista_areas.errorTitle = "Área fora da lista"
    ws.add_data_validation(lista_areas)
    lista_areas.add(f"B{SAIDAS_INICIO}:B{ULTIMA_LINHA}")

    lista_status = DataValidation(
        type="list", formula1='"A PAGAR,PAGO"', allow_blank=True, showDropDown=False,
    )
    ws.add_data_validation(lista_status)
    lista_status.add(f"H{SAIDAS_INICIO}:H{ULTIMA_LINHA}")

    # A comissão entra como linha própria e é preenchida por fórmula depois que
    # o RESUMO existe — é dele que vêm a base e o percentual.
    # Sempre presente, mesmo zerada. Comissão é a saída que mais some da
    # conta quando não tem campo esperando por ela — e quando some, some
    # inteira. Melhor uma linha em zero do que a pergunta não feita.
    linha_comissao = SAIDAS_INICIO + len(saidas)
    ws.cell(row=linha_comissao, column=2, value=COMISSAO_AREA)
    ws.cell(row=linha_comissao, column=3,
            value=cfg.get("comissao_descricao", "Comissão comercial"))
    ws.cell(row=linha_comissao, column=5, value=1)
    ws.cell(row=linha_comissao, column=8, value="A PAGAR")
    for col in (5, 6):
        ws.cell(row=linha_comissao, column=col).fill = _fill(TINTA["claro"])

    ws.auto_filter.ref = f"B5:J{ULTIMA_LINHA}"
    ws.print_title_rows = "5:5"   # o cabeçalho se repete em toda página
    _impressao(ws, f"{cfg.get('job', 'Pressuposto real')} — SAÍDAS", paisagem=True)
    return linha_comissao


# --------------------------------------------------------------------------
# Aba RESUMO
# --------------------------------------------------------------------------

def _aba_resumo(wb: Workbook, cfg: dict, total_areas: int) -> dict:
    ws = wb.create_sheet(ABA_RESUMO, 0)
    larguras = {"A": 2, "B": 44, "C": 17, "D": 16, "E": 14, "F": 34}
    for col, largura in larguras.items():
        ws.column_dimensions[col].width = largura

    linha_ident = _timbrado(ws, cfg) + 1

    _titulo(ws, f"B{linha_ident}", "PRESSUPOSTO REAL", 20)
    ws.row_dimensions[linha_ident].height = 28
    linha_ident += 1
    ws.merge_cells(start_row=linha_ident, start_column=2, end_row=linha_ident, end_column=6)
    ws.cell(row=linha_ident, column=2, value=cfg.get("job", ""))
    ws.cell(row=linha_ident, column=2).font = Font(bold=True, size=12, color=TINTA["meio"])
    linha_ident += 1

    identificacao = "   ·   ".join(
        f"{rotulo}: {cfg[chave]}"
        for rotulo, chave in (("Cliente", "cliente"), ("Contato", "contato"),
                              ("Período", "periodo"))
        if cfg.get(chave)
    )
    if identificacao:
        ws.merge_cells(start_row=linha_ident, start_column=2,
                       end_row=linha_ident, end_column=6)
        ws.cell(row=linha_ident, column=2, value=identificacao)
        ws.cell(row=linha_ident, column=2).font = Font(size=10, color=TINTA["texto_fraco"])
        linha_ident += 1

    linha_ident = _ficha(ws, cfg, linha_ident + 1)

    total_saidas_faixa = f"{ABA_SAIDAS}!$G${SAIDAS_INICIO}:$G${ULTIMA_LINHA}"
    area_faixa = f"{ABA_SAIDAS}!$B${SAIDAS_INICIO}:$B${ULTIMA_LINHA}"
    status_faixa = f"{ABA_SAIDAS}!$H${SAIDAS_INICIO}:$H${ULTIMA_LINHA}"

    # ---------------- 1. ENTRADAS ----------------
    linha = linha_ident + 1
    _secao(ws, linha, "1.  ENTRADAS — o que o cliente paga", "B", "F")
    linha += 1
    _cabecalho(ws, linha, 2, ["DESCRIÇÃO", "VALOR", "DATA PREVISTA", "STATUS", "OBS"])
    primeira_entrada = linha + 1

    entradas = cfg.get("entradas", [])
    for i, item in enumerate(entradas):
        r = primeira_entrada + i
        ws.cell(row=r, column=2, value=item.get("descricao", ""))
        ws.cell(row=r, column=3, value=item.get("valor"))
        ws.cell(row=r, column=4, value=_data_br(item.get("data")))
        ws.cell(row=r, column=5, value=item.get("status", "A RECEBER"))
        ws.cell(row=r, column=6, value=item.get("obs", ""))
    ultima_entrada = primeira_entrada + max(len(entradas), 1) + FOLGA_ENTRADAS - 1

    for r in range(primeira_entrada, ultima_entrada + 1):
        for col in range(2, 7):
            cel = ws.cell(row=r, column=col)
            cel.border = GRADE
            if col == 3:
                cel.number_format = MOEDA
                if cel.value is None:
                    cel.fill = _fill(TINTA["preencher"])
            elif col == 4:
                cel.number_format = DATA
                cel.alignment = Alignment(horizontal="center")
            elif col == 5:
                cel.alignment = Alignment(horizontal="center")

    lista_receb = DataValidation(
        type="list", formula1='"A RECEBER,RECEBIDO"', allow_blank=True, showDropDown=False,
    )
    ws.add_data_validation(lista_receb)
    lista_receb.add(f"E{primeira_entrada}:E{ultima_entrada}")

    linha = ultima_entrada + 1
    r_bruto = linha
    ws.cell(row=linha, column=2, value="TOTAL ENTRADAS (BRUTO)").font = NEGRITO
    ws.cell(row=linha, column=3,
            value=f"=SUM(C{primeira_entrada}:C{ultima_entrada})")
    linha += 1
    r_pct = linha
    ws.cell(row=linha, column=2, value="IMPOSTO (%)  ← edite aqui se mudar")
    ws.cell(row=linha, column=3, value=float(cfg.get("imposto_pct", IMPOSTO_PADRAO)) / 100)
    ws.cell(row=linha, column=3).number_format = PORCENTO
    ws.cell(row=linha, column=3).fill = _fill(TINTA["preencher"])

    # Percentual da comissão mora ao lado do imposto: são as duas fatias que
    # saem antes de qualquer pagamento, e ficam juntas para serem lidas juntas.
    comissao_pct = float(cfg.get("comissao_pct") or 0)
    base = str(cfg.get("comissao_base", "liquida")).lower()
    rotulo_base = COMISSAO_BASES.get(base, COMISSAO_BASES["liquida"])[0]
    ws.merge_cells(start_row=linha, start_column=4, end_row=linha, end_column=5)
    ws.cell(row=linha, column=4,
            value=f"COMISSÃO (%) sobre a {rotulo_base}  ← edite aqui")
    ws.cell(row=linha, column=4).font = Font(size=10)
    ws.cell(row=linha, column=4).alignment = Alignment(horizontal="right")
    ws.cell(row=linha, column=6, value=comissao_pct / 100)
    ws.cell(row=linha, column=6).number_format = PORCENTO
    ws.cell(row=linha, column=6).fill = _fill(TINTA["preencher"])
    ws.cell(row=linha, column=6).border = GRADE
    linha += 1
    r_imposto = linha
    ws.cell(row=linha, column=2, value="(−) IMPOSTO")
    ws.cell(row=linha, column=3, value=f"=ROUND(C{r_bruto}*C{r_pct},2)")
    linha += 1
    r_liquida = linha
    ws.cell(row=linha, column=2, value="(=) ENTRADA LÍQUIDA — é com isso que se paga tudo")
    ws.cell(row=linha, column=3, value=f"=C{r_bruto}-C{r_imposto}")

    for r in (r_bruto, r_pct, r_imposto, r_liquida):
        for col in range(2, 4):
            ws.cell(row=r, column=col).border = GRADE
        if r != r_pct:
            ws.cell(row=r, column=3).number_format = MOEDA
    for col in range(2, 4):
        ws.cell(row=r_liquida, column=col).font = Font(bold=True, size=12)
        ws.cell(row=r_liquida, column=col).fill = _fill(TINTA["resultado"])

    # ---------------- 2. SAÍDAS POR ÁREA ----------------
    linha = r_liquida + 2
    _secao(ws, linha, "2.  SAÍDAS POR ÁREA — vem sozinho da aba SAÍDAS", "B", "F")
    linha += 1
    _cabecalho(ws, linha, 2, ["ÁREA", "VALOR", "% DA LÍQUIDA", "PAGO", "A PAGAR"])
    primeira_area = linha + 1

    for i in range(total_areas):
        r = primeira_area + i
        ref = f"{ABA_AREAS}!$A${AREAS_INICIO + i}"
        ws.cell(row=r, column=2, value=f'=IF({ref}="","",{ref})')
        ws.cell(row=r, column=3,
                value=f'=IF(B{r}="","",SUMIF({area_faixa},B{r},{total_saidas_faixa}))')
        ws.cell(row=r, column=4,
                value=f'=IF(OR(B{r}="",$C${r_liquida}=0),"",C{r}/$C${r_liquida})')
        ws.cell(row=r, column=5,
                value=f'=IF(B{r}="","",SUMIFS({total_saidas_faixa},{area_faixa},B{r},'
                      f'{status_faixa},"PAGO"))')
        ws.cell(row=r, column=6,
                value=f'=IF(B{r}="","",C{r}-E{r})')
    ultima_area = primeira_area + total_areas - 1

    r_sem_area = ultima_area + 1
    ws.cell(row=r_sem_area, column=2, value="SEM ÁREA — classificar na aba SAÍDAS")
    ws.cell(row=r_sem_area, column=2).font = Font(italic=True)
    ws.cell(row=r_sem_area, column=3,
            value=f"=ROUND(SUM({total_saidas_faixa})-SUM(C{primeira_area}:C{ultima_area}),2)")
    # Meio centavo de tolerância: arredondamento não deve acender o alerta.
    ws.conditional_formatting.add(
        f"C{r_sem_area}",
        CellIsRule(operator="greaterThan", formula=["0.005"],
                   fill=_fill(TINTA["atencao"]), font=Font(bold=True, color="9B1C1C")),
    )

    r_total_saidas = r_sem_area + 1
    ws.cell(row=r_total_saidas, column=2, value="TOTAL SAÍDAS").font = Font(bold=True, size=12)
    ws.cell(row=r_total_saidas, column=3, value=f"=ROUND(SUM({total_saidas_faixa}),2)")
    ws.cell(row=r_total_saidas, column=4,
            value=f'=IF($C${r_liquida}=0,"",C{r_total_saidas}/$C${r_liquida})')
    ws.cell(row=r_total_saidas, column=5,
            value=f'=SUMIF({status_faixa},"PAGO",{total_saidas_faixa})')
    ws.cell(row=r_total_saidas, column=6, value=f"=C{r_total_saidas}-E{r_total_saidas}")

    for r in range(primeira_area, r_total_saidas + 1):
        for col in range(2, 7):
            cel = ws.cell(row=r, column=col)
            cel.border = GRADE
            if col in (3, 5, 6):
                cel.number_format = MOEDA
            elif col == 4:
                cel.number_format = PORCENTO
                cel.alignment = Alignment(horizontal="center")
        if r == r_total_saidas:
            for col in range(2, 7):
                ws.cell(row=r, column=col).font = Font(bold=True, size=12)

    # ---------------- 3. RESULTADO ----------------
    linha = r_total_saidas + 2
    _secao(ws, linha, "3.  RESULTADO", "B", "F")
    linha += 1
    ws.cell(row=linha, column=2, value="ENTRADA LÍQUIDA")
    ws.cell(row=linha, column=3, value=f"=C{r_liquida}")
    linha += 1
    ws.cell(row=linha, column=2, value="(−) TOTAL SAÍDAS")
    ws.cell(row=linha, column=3, value=f"=C{r_total_saidas}")
    linha += 1
    r_lucro = linha
    ws.cell(row=linha, column=2, value="(=) LUCRO DA YAD")
    ws.cell(row=linha, column=3, value=f"=C{r_liquida}-C{r_total_saidas}")
    linha += 1
    ws.cell(row=linha, column=2, value="MARGEM (sobre a entrada bruta)")
    ws.cell(row=linha, column=3,
            value=f'=IF(C{r_bruto}=0,"",C{r_lucro}/C{r_bruto})')
    ws.cell(row=linha, column=3).number_format = PORCENTO
    r_margem = linha

    for r in range(r_lucro - 2, r_margem + 1):
        for col in range(2, 4):
            ws.cell(row=r, column=col).border = GRADE
        if r != r_margem:
            ws.cell(row=r, column=3).number_format = MOEDA
    for col in range(2, 4):
        ws.cell(row=r_lucro, column=col).font = Font(bold=True, size=14)
    ws.row_dimensions[r_lucro].height = 24
    ws.conditional_formatting.add(
        f"B{r_lucro}:C{r_lucro}",
        CellIsRule(operator="lessThan", formula=["0"], fill=_fill(TINTA["atencao"])),
    )
    ws.conditional_formatting.add(
        f"B{r_lucro}:C{r_lucro}",
        CellIsRule(operator="greaterThanOrEqual", formula=["0"], fill=_fill(TINTA["positivo"])),
    )

    # ---------------- 4. CAIXA ----------------
    linha = r_margem + 2
    _secao(ws, linha, "4.  CAIXA — o que já andou e o que falta", "B", "F")
    linha += 1
    _cabecalho(ws, linha, 2, ["", "JÁ ANDOU", "FALTA"])
    linha += 1
    ws.cell(row=linha, column=2, value="ENTRADAS (recebido / a receber)")
    ws.cell(row=linha, column=3,
            value=f'=SUMIF(E{primeira_entrada}:E{ultima_entrada},"RECEBIDO",'
                  f'C{primeira_entrada}:C{ultima_entrada})')
    ws.cell(row=linha, column=4, value=f"=C{r_bruto}-C{linha}")
    linha += 1
    ws.cell(row=linha, column=2, value="SAÍDAS (pago / a pagar)")
    ws.cell(row=linha, column=3, value=f"=E{r_total_saidas}")
    ws.cell(row=linha, column=4, value=f"=F{r_total_saidas}")
    r_caixa_fim = linha

    for r in range(r_caixa_fim - 1, r_caixa_fim + 1):
        for col in range(2, 5):
            ws.cell(row=r, column=col).border = GRADE
            if col in (3, 4):
                ws.cell(row=r, column=col).number_format = MOEDA

    # ---------------- 5. DIVISÃO DO RESULTADO ----------------
    # Job em sociedade: o lucro se reparte entre os sócios. O primeiro da lista
    # absorve o resto do arredondamento — seu percentual e seu valor são o que
    # sobra depois dos outros. Assim o total distribuído fecha exatamente com o
    # lucro em qualquer divisão, inclusive um terço para cada, que em duas casas
    # decimais nunca soma 100%.
    socios = cfg.get("divisao_resultado") or []
    if socios:
        normalizados = []
        for item in socios:
            if isinstance(item, dict):
                normalizados.append((item.get("nome", ""), item.get("pct")))
            else:
                normalizados.append((str(item), None))
        n = len(normalizados)
        padrao = 100.0 / n

        linha = r_caixa_fim + 2
        _secao(ws, linha, "5.  DIVISÃO DO RESULTADO", "B", "F")
        linha += 1
        _cabecalho(ws, linha, 2, ["PARTICIPANTE", "%", "VALOR"])
        primeiro = linha + 1
        ultimo = primeiro + n - 1

        for i, (nome, pct) in enumerate(normalizados):
            r = primeiro + i
            ws.cell(row=r, column=2, value=nome)
            if i == 0:
                # O que sobra depois dos demais — garante que a soma bate.
                # O percentual sai da coluna C (percentuais) e o valor da
                # coluna D (reais) — somar a coluna errada aqui produz um
                # percentual absurdo que ninguém confere.
                ws.cell(row=r, column=3,
                        value=f"=1-SUM(C{primeiro + 1}:C{ultimo})" if n > 1 else 1)
                ws.cell(row=r, column=4,
                        value=f"=C{r_lucro}-SUM(D{primeiro + 1}:D{ultimo})"
                              if n > 1 else f"=C{r_lucro}")
                ws.cell(row=r, column=6,
                        value="leva a diferença de arredondamento")
                ws.cell(row=r, column=6).font = Font(italic=True, size=9,
                                                     color=TINTA["texto_fraco"])
            else:
                ws.cell(row=r, column=3,
                        value=(float(pct) if pct is not None else padrao) / 100)
                ws.cell(row=r, column=3).fill = _fill(TINTA["preencher"])
                ws.cell(row=r, column=4, value=f"=ROUND($C${r_lucro}*C{r},2)")
            ws.cell(row=r, column=3).number_format = PORCENTO
            ws.cell(row=r, column=3).alignment = Alignment(horizontal="center")
            ws.cell(row=r, column=4).number_format = MOEDA
            for col in range(2, 5):
                ws.cell(row=r, column=col).border = GRADE

        r_total_divisao = ultimo + 1
        ws.cell(row=r_total_divisao, column=2, value="TOTAL DISTRIBUÍDO")
        ws.cell(row=r_total_divisao, column=3, value=f"=SUM(C{primeiro}:C{ultimo})")
        ws.cell(row=r_total_divisao, column=4, value=f"=SUM(D{primeiro}:D{ultimo})")
        ws.cell(row=r_total_divisao, column=3).number_format = PORCENTO
        ws.cell(row=r_total_divisao, column=3).alignment = Alignment(horizontal="center")
        ws.cell(row=r_total_divisao, column=4).number_format = MOEDA
        for col in range(2, 5):
            cel = ws.cell(row=r_total_divisao, column=col)
            cel.border = GRADE
            cel.font = Font(bold=True, size=12)
            cel.fill = _fill(TINTA["resultado"])
        r_caixa_fim = r_total_divisao

    r_aviso = r_caixa_fim + 2
    ws.merge_cells(start_row=r_aviso, start_column=2, end_row=r_aviso, end_column=6)
    ws.cell(row=r_aviso, column=2,
            value="Preencha só a aba SAIDAS — esta aqui é toda fórmula. "
                  "Célula amarela é campo para digitar.")
    ws.cell(row=r_aviso, column=2).font = Font(italic=True, size=10,
                                               color=TINTA["texto_fraco"])

    _impressao(ws, f"{cfg.get('job', 'Pressuposto real')} — RESUMO")

    return {"bruto": f"C{r_bruto}", "liquida": f"C{r_liquida}",
            "comissao_pct": f"F{r_pct}"}


# --------------------------------------------------------------------------

def gerar(cfg: dict, saida: Path) -> Path:
    areas = list(cfg.get("areas") or AREAS_PADRAO)
    if COMISSAO_AREA not in areas:
        areas.append(COMISSAO_AREA)  # sem ela, a comissão cairia em SEM ÁREA
    wb = Workbook()
    wb.remove(wb.active)
    total_areas = _aba_areas(wb, areas)
    linha_comissao = _aba_saidas(wb, cfg.get("saidas", []), total_areas, cfg)
    refs = _aba_resumo(wb, cfg, total_areas)

    # A comissão só pode ser escrita depois do RESUMO: é dele que saem a base e
    # o percentual. Valor e observação vão por fórmula, não por número — assim
    # trocar a alíquota do imposto ou o percentual recalcula tudo sozinho, e a
    # observação nunca contradiz o valor que está do lado dela.
    if linha_comissao:  # sempre verdadeiro; guarda contra refatoração futura
        base = str(cfg.get("comissao_base", "liquida")).lower()
        rotulo_base = COMISSAO_BASES.get(base, COMISSAO_BASES["liquida"])[0]
        cel_base = refs["liquida"] if base != "bruta" else refs["bruto"]
        ws = wb[ABA_SAIDAS]
        ws.cell(row=linha_comissao, column=6,
                value=f"=ROUND({ABA_RESUMO}!${cel_base[0]}${cel_base[1:]}"
                      f"*{ABA_RESUMO}!${refs['comissao_pct'][0]}"
                      f"${refs['comissao_pct'][1:]},2)")
        ws.cell(row=linha_comissao, column=4, value=f"% sobre a {rotulo_base}")
        ws.cell(row=linha_comissao, column=10,
                value=f'=TEXT({ABA_RESUMO}!${refs["comissao_pct"][0]}'
                      f'${refs["comissao_pct"][1:]},"0.0%")&" da {rotulo_base} '
                      f'({ABA_RESUMO}!{cel_base})"')
    wb.active = 0
    wb.properties.creator = cfg.get("elaborado_por") or "YAD Filmes"
    wb.properties.lastModifiedBy = (cfg.get("atualizado_por")
                                    or cfg.get("elaborado_por") or "YAD Filmes")
    wb.properties.title = f"Pressuposto real — {cfg.get('job', '')}".strip(" —")
    wb.properties.company = (cfg.get("empresa") or {}).get(
        "nome", EMPRESA_PADRAO["nome"])
    saida.parent.mkdir(parents=True, exist_ok=True)
    wb.save(saida)
    return saida


EXEMPLO = {
    "job": "NOME DO JOB — descrição curta",
    "cliente": "CLIENTE",
    "contato": "Nome (DD) 90000-0000",
    "periodo": "01/01/2026 a 05/01/2026 — 5 diárias",
    "elaborado_por": "Quem montou (e-mail)",
    "elaborado_em": "01/01/2026",
    "atualizado_por": "Quem mexeu por último (e-mail)",
    "versao": "v1",
    "situacao": "EM ANDAMENTO",
    "imposto_pct": IMPOSTO_PADRAO,
    "comissao_pct": 0,
    "comissao_base": "liquida",
    "comissao_descricao": "Comissão comercial",
    "areas": AREAS_PADRAO,
    "entradas": [
        {"descricao": "1ª parcela (50%)", "valor": 0, "data": "01/01/2026",
         "status": "A RECEBER"},
        {"descricao": "2ª parcela (50%)", "valor": 0, "data": "15/01/2026",
         "status": "A RECEBER"},
    ],
    "saidas": [
        {"area": "EQUIPE", "descricao": "Fulano", "funcao": "Cinegrafista",
         "qtd": 5, "unit": 500, "status": "A PAGAR", "obs": ""},
        {"area": "TRANSPORTE E LOGÍSTICA", "descricao": "Combustível",
         "funcao": "ida e volta", "qtd": 1, "unit": "", "status": "A PAGAR"},
    ],
}


def main() -> int:
    p = argparse.ArgumentParser(
        description="Gera a planilha de pressuposto real (entradas − saídas por área).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--config", type=Path, help="JSON do job (ver --exemplo)")
    p.add_argument("--saida", type=Path, default=Path("PRESSUPOSTO_REAL.xlsx"),
                   help="arquivo .xlsx de saída")
    p.add_argument("--exemplo", type=Path,
                   help="escreve um JSON de exemplo neste caminho e sai")
    p.add_argument("--job", help="nome do job (sobrepõe o do config)")
    p.add_argument("--cliente")
    p.add_argument("--imposto", type=float,
                   help=f"alíquota em %%, padrão {IMPOSTO_PADRAO:g}")
    p.add_argument("--elaborado-por", help="quem montou o pressuposto")
    p.add_argument("--atualizado-por",
                   help="quem mexeu por último; a data vira hoje")
    p.add_argument("--versao", help='ex.: "v2"')
    p.add_argument("--comissao", type=float,
                   help="percentual de comissão de captação; 0 ou ausente não gera a linha")
    p.add_argument("--comissao-base", choices=sorted(COMISSAO_BASES),
                   help="sobre o que a comissão incide (padrão: liquida)")
    p.add_argument("--logo", type=Path,
                   help="PNG do logo; padrão tools/assets/yad-logo.png")
    args = p.parse_args()

    if args.exemplo:
        args.exemplo.write_text(
            json.dumps(EXEMPLO, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"exemplo escrito em {args.exemplo}")
        return 0

    cfg = {"imposto_pct": IMPOSTO_PADRAO}
    if args.config:
        cfg.update(json.loads(args.config.read_text(encoding="utf-8")))
    for chave, valor in (("job", args.job), ("cliente", args.cliente),
                         ("elaborado_por", args.elaborado_por),
                         ("versao", args.versao), ("logo", args.logo)):
        if valor:
            cfg[chave] = valor
    if args.atualizado_por:
        # Quem atualiza carimba a data de hoje: o par nome+data é o que dá
        # sentido ao campo, e separá-los é como ele acaba mentindo.
        cfg["atualizado_por"] = args.atualizado_por
        cfg["atualizado_em"] = datetime.date.today()
    if args.imposto is not None:
        cfg["imposto_pct"] = args.imposto
    if args.comissao is not None:
        cfg["comissao_pct"] = args.comissao
    if args.comissao_base:
        cfg["comissao_base"] = args.comissao_base

    destino = gerar(cfg, args.saida)
    print(f"planilha gerada: {destino}")
    print(f"  imposto: {cfg['imposto_pct']:g}%  ·  "
          f"entradas: {len(cfg.get('entradas', []))}  ·  "
          f"saídas: {len(cfg.get('saidas', []))}  ·  "
          f"versão: {cfg.get('versao', 'v1')}")
    if float(cfg.get("comissao_pct") or 0) > 0:
        base = COMISSAO_BASES.get(
            str(cfg.get("comissao_base", "liquida")).lower(),
            COMISSAO_BASES["liquida"])[0]
        print(f"  comissão: {float(cfg['comissao_pct']):g}% sobre a {base}")
    if not LOGO_PADRAO.is_file() and not cfg.get("logo"):
        print(f"  aviso: logo não encontrado em {LOGO_PADRAO} — gerada sem marca")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
