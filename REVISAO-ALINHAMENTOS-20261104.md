# Revisão pontual de alinhamentos — 04/11/2026

## Estado recuperável

Estado anterior: commit `0c0d8a57691e82bc37f25c26774c49ba5f41fc3c`, tag local `audit-alignements-20261104-before` e arquivo `qa/alinhamentos-20261104/estado-anterior.tar.gz`. O arquivo contém a origem rastreada antes desta revisão. As capturas e medições estão em `qa/alinhamentos-20261104/antes` e `depois` (artefatos locais, não publicados no site).

## Sistema reaproveitado

- Container útil máximo de 1440 px; margens de `max(32px, (viewport - 1440px)/2)` no desktop, 32 px no tablet e 24 px até 700 px.
- 12 colunas com gutter de 24 px acima de 700 px; 4 guias e gutter de 16 px no mobile. Componentes internos podem usar suas próprias trilhas.
- Breakpoints existentes: 700/701, 900/901 e 1100/1101 px. Nenhum substituído.
- Seções regulares da home: padding vertical 96/80/64 px. Frase de impacto, hero, filme, fotos editoriais e rodapé são famílias próprias, já aprovadas.
- Seções editoriais da home: 32 px entre título e corpo, 24 px entre parágrafos e 64 px antes do CTA no desktop (48 px na pilha). Valores preservados.

## Problemas demonstrados e menor correção

| Elemento / eixo esperado | Observado antes | Causa | Correção / depois |
| --- | --- | --- | --- |
| Lista de jornadas, alinhada ao início do container quando o guia lateral desaparece | Em viewport de 900 px: x=175,33 em vez de x=32; desvio de 143,33 px. Em 701/1100 px: desvios de 110,16/176,66 px | O guia lateral tinha `display:none`, mas a lista continuava em `grid-column:3/13` | `grid-column:1/-1` apenas entre 701 e 1100 px. x=32; no desktop amplo mantém o guia lateral e as duas colunas reservadas |
| Primeira linha de links do rodapé mobile; separação de 32 px após o texto introdutório | 47 px, inclusive em 390 px | Margem inferior de 15 px herdada somada ao row-gap de 32 px | Remoção dessa margem apenas até 700 px. Gap final: 32 px nas 12 páginas |
| Guias fixas versus contornos observados | Linhas de padding/limites e malha usavam a mesma família azul; desvios de caixas em relação ao grid global pareciam reprovação automática | Representação não distinguia referências de medidas | Mesmas coordenadas de referência, azul forte a cada 32 px e fino a cada 8 px. Limites medidos roxos tracejados, caixas verdes. Δx identificado como distância ao eixo global, não erro. Contornos agora incluem os textos internos das duas composições editoriais e blocos internos das páginas |

A malha mantém a origem no início da área interna da seção e incrementos fixos de 8/32 px. Não se reposiciona em função de títulos, parágrafos ou botões. Limites de seções e padding são medidas observadas separadas. Uma expansão aumenta a altura natural e desloca seções seguintes; não encaixa artificialmente suas bases.

## Exceções preservadas

- Fotos editoriais ocupam metade da viewport e chegam à borda. O texto tem recuo interno de 64 px (48 px entre 901 e 1100), com padding vertical de 96/80 px. Em 1920 px, o texto começa em x=1024, intencionalmente diferente da coluna global em x=972. Não é uma composição com topo visível do título igual ao topo da foto.
- Miniaturas e títulos das jornadas compartilham topo óptico; índice e controle ficam centralizados. O texto pertence ao grid interno da linha, após índice, miniatura e gaps. As miniaturas mantêm tamanho/proporção; as linhas não foram esticadas para múltiplos de oito.
- Textos independentes conservam alturas naturais. Não foram adicionados espaços vazios, quebras artificiais, cortes, alterações de fontes ou redução de entrelinha.
- `text-box-trim: trim-both` e `text-box-edge: cap alphabetic` existentes foram preservados. A caixa não equivale ao contorno dos acentos/descendentes; Range/contorno não foi apresentado como baseline medida.
- O rodapé tem padding próprio; o filme usa composição sobre imagem; hero e frase de impacto mantêm o respiro aprovado. Não se igualaram todas as alturas nem todos os paddings por força da malha.

## Validação efetivamente realizada

- Home: 360, 390, 700, 701, 900, 901, 1100, 1101, 1440 e 1920 px. Verificados overflow, eixo das jornadas, gap do rodapé, gaps editoriais, recuos/altura das fotos, tipografia, ativação da camada e correspondência das colunas e referências de 32 px.
- Onze páginas internas: 390 e 1440 px; todos os títulos/parágrafos quanto a overflow e trim, margens das seções e gap do rodapé mobile. Não equivale a uma auditoria óptica de cada bloco interno.
- Seis jornadas abertas individualmente em 360, 900 e 1920 px: conteúdo dentro do painel. Cinco FAQs abertas individualmente nas mesmas larguras: sem recortes de resposta.
- Capturas comparáveis com fonte carregada, guias ligadas/desligadas: sete posições da home em 1920×963 e 390×844, além da lista em 900×900. Nas comparações o modo de revisão pausa animações; modo normal é conferido separadamente.
- Comparação de medidas em 1920 px: nenhuma mudança de posição horizontal, dimensão, padding, margem ou tipografia nos blocos amostrados. Em 390 px: somente a margem removida no rodapé; seções anteriores conservadas.
- Conteúdo textual e fontes/alt das imagens das 12 páginas comparados ao backup: idênticos. Teste de normalização tipográfica, sintaxe JavaScript e `git diff --check` aprovados.

Não foram testados Safari/Firefox nem aparelhos físicos. As páginas internas receberam verificação geométrica compartilhada, não revisão visual integral dobra a dobra. Não houve mudanças de permissões de acesso.
