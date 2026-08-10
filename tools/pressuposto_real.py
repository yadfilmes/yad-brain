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

# Linhas vazias sobrando no fim de cada bloco, para digitar sem inserir linha.
FOLGA_ENTRADAS = 3
FOLGA_AREAS = 3

MOEDA = 'R$ #,##0.00'
PORCENTO = '0.0%'
DATA = 'DD/MM/YYYY'

TINTA = {
    "escuro": "1F2933",
    "faixa": "3E4C59",
    "claro": "F5F7FA",
    "borda": "CBD2D9",
    "preencher": "FFF3C4",   # amarelo: célula que espera alguém digitar
    "resultado": "E3F9E5",   # verde: linha de resultado
    "atencao": "FFE3E3",
}

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

def _aba_saidas(wb: Workbook, saidas: list[dict], total_areas: int):
    ws = wb.create_sheet(ABA_SAIDAS)
    larguras = {"A": 2, "B": 26, "C": 34, "D": 26, "E": 9, "F": 15, "G": 15,
                "H": 13, "I": 14, "J": 30}
    for col, largura in larguras.items():
        ws.column_dimensions[col].width = largura

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

    ws.auto_filter.ref = f"B5:J{ULTIMA_LINHA}"


# --------------------------------------------------------------------------
# Aba RESUMO
# --------------------------------------------------------------------------

def _aba_resumo(wb: Workbook, cfg: dict, total_areas: int):
    ws = wb.create_sheet(ABA_RESUMO, 0)
    larguras = {"A": 2, "B": 44, "C": 17, "D": 16, "E": 14, "F": 34}
    for col, largura in larguras.items():
        ws.column_dimensions[col].width = largura

    _titulo(ws, "B2", "PRESSUPOSTO REAL", 20)
    ws["B3"] = cfg.get("job", "")
    ws["B3"].font = Font(bold=True, size=13, color=TINTA["faixa"])
    linha_ident = 4
    for rotulo, chave in (("Cliente", "cliente"), ("Contato", "contato"),
                          ("Período", "periodo")):
        if cfg.get(chave):
            ws.cell(row=linha_ident, column=2, value=f"{rotulo}: {cfg[chave]}")
            ws.cell(row=linha_ident, column=2).font = Font(size=10, color="52606D")
            linha_ident += 1

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
        CellIsRule(operator="greaterThanOrEqual", formula=["0"], fill=_fill(TINTA["resultado"])),
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

    ws["F2"] = "Preencha só a aba SAÍDAS. Esta aqui é toda fórmula."
    ws["F2"].font = Font(italic=True, bold=True, color="52606D")
    ws["F3"] = "Amarelo = campo para digitar."
    ws["F3"].font = Font(italic=True, color="52606D")


# --------------------------------------------------------------------------

def gerar(cfg: dict, saida: Path) -> Path:
    areas = cfg.get("areas") or AREAS_PADRAO
    wb = Workbook()
    wb.remove(wb.active)
    total_areas = _aba_areas(wb, areas)
    _aba_saidas(wb, cfg.get("saidas", []), total_areas)
    _aba_resumo(wb, cfg, total_areas)
    wb.active = 0
    saida.parent.mkdir(parents=True, exist_ok=True)
    wb.save(saida)
    return saida


EXEMPLO = {
    "job": "NOME DO JOB — descrição curta",
    "cliente": "CLIENTE",
    "contato": "Nome (DD) 90000-0000",
    "periodo": "01/01/2026 a 05/01/2026 — 5 diárias",
    "imposto_pct": IMPOSTO_PADRAO,
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
    args = p.parse_args()

    if args.exemplo:
        args.exemplo.write_text(
            json.dumps(EXEMPLO, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"exemplo escrito em {args.exemplo}")
        return 0

    cfg = {"imposto_pct": IMPOSTO_PADRAO}
    if args.config:
        cfg.update(json.loads(args.config.read_text(encoding="utf-8")))
    for chave, valor in (("job", args.job), ("cliente", args.cliente)):
        if valor:
            cfg[chave] = valor
    if args.imposto is not None:
        cfg["imposto_pct"] = args.imposto

    destino = gerar(cfg, args.saida)
    print(f"planilha gerada: {destino}")
    print(f"  imposto: {cfg['imposto_pct']:g}%  ·  "
          f"entradas: {len(cfg.get('entradas', []))}  ·  "
          f"saídas: {len(cfg.get('saidas', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
