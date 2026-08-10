# Conferir antes de entregar

Planilha de controladoria com fórmula errada é pior que planilha nenhuma: o erro
vira decisão. Este é o procedimento que já pegou três defeitos reais.

## Avaliar as fórmulas contra o arquivo gerado

O `openpyxl` **não calcula** — ele escreve a fórmula e lê o valor que o Excel
deixou em cache. Arquivo recém-gerado não tem cache, então `data_only=True`
devolve `None` para tudo. Avaliar de verdade exige um avaliador:

```
pip install formulas
```

```python
import formulas, warnings, openpyxl
warnings.filterwarnings("ignore")
ARQ = "PRESSUPOSTO_JOB.xlsx"
sol = formulas.ExcelModel().loads(ARQ).finish().calculate()

def val(aba, cel):
    v = sol.get(f"'[{ARQ}]{aba}'!{cel}")
    if v is None:
        return "<sem chave>"
    try:
        return v.value[0, 0]
    except Exception:
        return v

wb = openpyxl.load_workbook(ARQ)
erros = [(n, c.coordinate, val(n, c.coordinate))
         for n in wb.sheetnames
         for row in wb[n].iter_rows(max_row=60) for c in row
         if isinstance(c.value, str) and c.value.startswith("=")
         and isinstance(val(n, c.coordinate), str)
         and ("#" in val(n, c.coordinate) or val(n, c.coordinate) == "<sem chave>")]
print("células com erro:", len(erros), erros[:5])
```

A chave tem o nome do arquivo entre colchetes, com a extensão em minúsculas:
`'[PRESSUPOSTO_JOB.xlsx]RESUMO'!C15`. Erro comum é passar o nome todo em
maiúsculas e receber `None` em tudo.

Depois de contar os erros, **imprima os totais** — bruto, imposto, líquida, cada
área, total de saídas, lucro, margem — e confira contra o esperado. Zero erros
não garante conta certa; garante só que nenhuma fórmula quebrou.

## Quando o Felype devolve a planilha preenchida

Confira **totais linha a linha contra o arquivo dele**, não só contra a sua
expectativa:

```python
ref = openpyxl.load_workbook("arquivo-do-felype.xlsx", data_only=True)["RESUMO"]
# o arquivo dele passou pelo Excel, então tem cache — data_only funciona
esperado = {"bruto": ref["C15"].value, "lucro": ref["C41"].value, ...}
```

As coordenadas mudam conforme a versão do gerador (o timbrado empurrou tudo umas
seis linhas). Localize as linhas pelo rótulo na coluna B em vez de fixar
endereço.

Se algum total divergir, **investigue antes de gerar** — provavelmente ele
mudou algo que você não capturou.

## LibreOffice não serve como conferência

`soffice --convert-to` costuma estar quebrado no ambiente de execução (falha até
com um CSV trivial). Não conte com ele nem para recalcular nem para renderizar.
O avaliador de fórmulas em Python é o caminho.

## Armadilhas do formato .xlsx

Cada uma quebrou um arquivo de verdade.

**Rótulo que começa com `=` vira fórmula.** "= ENTRADA LÍQUIDA" no texto de uma
célula o Excel lê como fórmula e devolve `#NAME?`. Escreva `(=) ENTRADA
LÍQUIDA`. Vale para `+` e `-` no início também.

**Validação de lista não leva `=`.** Em `DataValidation(formula1=...)`, passar
`"='AREAS'!$A$2:$A$14"` gera XML inválido e o arquivo **não abre**. O certo é
`"AREAS!$A$2:$A$14"`, sem o sinal.

**`showDropDown` é invertido.** No OOXML o atributo significa "esconder a
setinha". `showDropDown=False` é o que **mostra** o menu.

**Nome de aba sem acento.** `RESUMO`, `SAIDAS`, `AREAS`. O arquivo circula entre
Excel, Google Sheets e LibreOffice, e nome acentuado é onde a referência entre
abas quebra.

**Fórmula até o fim da faixa, não até o fim dos dados.** A coluna TOTAL leva a
fórmula até a linha 500, para que linha nova digitada já nasça calculando. Sem
isso, alguém acrescenta um gasto e ele não entra em lugar nenhum.

## Prévia visual

Quando o Felype está no celular ou quer conferir o acabamento sem baixar,
renderize a planilha como página HTML fiel — lendo cores, mesclas, larguras e os
valores já calculados do próprio arquivo — e publique como artifact.

O que importa na renderização: largura de coluna em px é `width * 7 + 5`; altura
de linha é `height * 4/3`; a âncora da imagem é 0-based, então as colunas antes
dela são `1..anchor.col`; e o tamanho de exibição do logo está em
`img.anchor.ext.cx / 9525`, não no tamanho do PNG.

A folha deve manter as cores reais do arquivo nos dois temas (claro e escuro) —
é uma prévia de documento, não uma página de design. Só a moldura em volta
acompanha o tema de quem está lendo.
