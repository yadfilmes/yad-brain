# Onde ficam os pressupostos antigos

A YAD tem cerca de **95 pressupostos** no OneDrive/SharePoint. Eles respondem
"quanto pagamos o fulano da última vez", "como foi a distribuição do último job
desse cliente" e "que fornecedor a gente usou pra isso".

## Como buscar e ler

```
mcp__Microsoft_365__sharepoint_search   → acha o arquivo, devolve uma URI
mcp__Microsoft_365__read_resource       → lê o conteúdo pela URI
```

A busca aceita `query`, `fileType: "xlsx"`, `folderName`, `author` e
`afterDateTime` (que entende linguagem natural: "last week", "March 2026"). A
leitura devolve o conteúdo completo da planilha — todas as abas, valores **e as
fórmulas**, separadas por aba.

Confirme quem está autenticado com `mcp__Microsoft_365__get_me` se houver dúvida
sobre a conta.

## Mapa das pastas

**Pressupostos novos do Felype** — `felype_yadfilmes_com` — **olhe aqui primeiro**
```
Documents/Documentos/Pressuposto/{ano}/{MÊS}/
```
Repare: **`Pressuposto`, no singular e sem "S"**. É a pasta onde os
pressupostos no formato novo estão sendo salvos. Existe também um
`Documents/Documentos/Pressuposto/AGOSTO` (sem o ano no meio) que está vazio —
duas pastas de agosto no mesmo lugar, e a que vale é a que passa pelo ano.

**Orçamentos do Felype** — `felype_yadfilmes_com`
```
Documents/Documentos/Orçamentos/{ano}/{CLIENTE}/
```
Exemplos reais: `2026/ALEX/BARRETOS 2026 - V2.xlsx`, `2026/BYD/DENZA LANÇAMENTO/`,
`2025/CLUBE DO COWBOY/`, `2026/RUDGE/`, `2026/NONSTOP/`, `2025/FOTON/`.
É aqui que mora o **orçamento** — o que o cliente paga.

**Pressupostos da Mariani** — `mariani_yadfilmes_com`
```
Documents/PRESSUPOSTOS YAD FILMES/
├── PRESSUPOSTO YAD PRODUÇÕES E ENTRETENIMENTO/PRESS.{ano}/{n}. {MÊS}/
└── PRESSUPOSTO DE CLIENTES FIXOS E INSTITUCIONAL/PRESSU {ano}/{n}. {MÊS}/
```
Organizado por mês, com o número na frente (`4. ABRIL`). É aqui que mora o
**pressuposto** — o que a produção gasta. Tem um `PRESSUPOSTO BASE .xlsx` que é
o modelo antigo da casa.

**Site de gestão** — `yadfilmes336.sharepoint.com`
```
sites/GestodeOperaodosProjetos-2026/Documentos Compartilhados/
```

Arquivos também aparecem em `Microsoft Teams Chat Files/` de várias pessoas,
quando foram trocados por chat. São cópias — prefira a versão da pasta oficial.

## Limitações que valem saber

**O índice de busca atrasa.** Arquivo salvo agora pode não aparecer na busca por
algumas horas. Se o Felype disse que subiu e você não acha, é isso — peça o
arquivo direto em vez de afirmar que não existe.

**A busca é por conteúdo e nome, não por caminho.** Para varrer uma pasta, use
`sharepoint_folder_search` e depois `read_resource` na URI da pasta para listar.

**`folder_search` casa substring, e substring tem direção.** Procurar por
`PRESSUPOSTOS` **não acha** a pasta `Pressuposto` — o nome dela não contém o
termo buscado. Foi assim que a pasta principal do Felype passou despercebida.
Busque pelo **radical mais curto** (`Pressupost`, `AGOSTO`) e deixe o resultado
mostrar as variações, em vez de apostar na grafia que você imagina.

**Ordene por data de modificação para achar o que é recente.** Quando o índice
de conteúdo ainda não pegou um arquivo novo, a pasta que o contém já aparece
com `lastModifiedDateTime` de hoje — foi o que localizou a pasta certa.

**Cópias com o mesmo nome são comuns** (`- Copiar`, versões em chat de várias
pessoas). Confira a data de modificação e o caminho antes de tratar um arquivo
como a versão boa.

## Escrever no OneDrive

`sharepoint_upload_file` e `sharepoint_update_file` existem e funcionam — dá
para salvar a planilha gerada direto na pasta do cliente.

**Sobrescrever arquivo vivo é ação com consequência.** Confirme com o Felype
antes, dizendo qual arquivo e qual pasta. Bibliotecas com versionamento guardam
o histórico, mas nem toda pasta tem.

## Formato antigo × formato novo

Os pressupostos históricos seguem o layout em blocos: `ITEM | CONCEITO | 
CLIENTE/ORÇADO | PRESSUPOSTO/BASE DE GASTOS | REAL/FECHADO | DATA DE PAGAMENTO |
OBS`, com subtotal por bloco e um `RESUMO GERAL` no fim.

O formato novo (gerado por `tools/pressuposto_real.py`) tem a mesma lógica com
outra mecânica: uma linha por gasto numa aba só, área escolhida numa listinha, e
o resumo montado por fórmula. Ao ler um pressuposto antigo para extrair
histórico, os dois traduzem direto — bloco vira área, "REAL/FECHADO" vira o
valor da linha.
