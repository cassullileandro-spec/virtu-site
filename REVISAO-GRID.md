# Revisão de grid e posicionamento — 03/11/2026

Revisão focada nas 12 páginas da Virtù: alinhamento entre fotografia e texto, continuidade das colunas e espaçamento. A identidade vinho/creme, a copy aprovada e as funções existentes foram preservadas.

## Fundamentação

- [Carbon — 2x Grid](https://www.carbondesignsystem.com/building-blocks/foundations/2x-grid/overview): eixos de alinhamento horizontais e verticais, margens consistentes e colunas fluidas. As 12 colunas são uma decisão deste projeto; não uma regra universal nem a configuração do Carbon.
- [Carbon — Spacing](https://www.carbondesignsystem.com/building-blocks/foundations/spacing/overview): escala de espaçamento para estabelecer proximidade e hierarquia.
- [Nielsen Norman Group — Principles of Visual Design](https://www.nngroup.com/articles/principles-visual-design/): escala, posição e espaços participam da hierarquia; equilíbrio não exige simetria.
- [MDN — Subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid): compartilhamento de linhas entre cards para alinhar títulos, descrições e ações mesmo com quebras diferentes.

## Regras aplicadas

- Referência desktop: 1920 × 1080. Conteúdo útil de até 1440 px, 12 colunas e intervalos de 24 px. Em Full HD, o conteúdo começa em x=240; cada coluna mede 98 px.
- Aberturas mantidas em 100vh × 100vw, verificadas nos cinco tamanhos de tela abaixo.
- Nos blocos lado a lado, a caixa do título começa no topo da imagem. Quando existe CTA, sua base coincide com a base da fotografia. A imagem acompanha a altura necessária ao texto, usando recorte proporcional, sem deformação.
- Seções: espaçamento principal de 128 px no desktop, 96 px no tablet e 72 px no mobile. Separação entre marcador e conteúdo: 64/48/32 px. Parágrafos relacionados: 24 px.
- Texto corrido: entrelinha de 32 px no desktop e 28 px nas larguras menores. Isso estabelece ritmo; não representa uma grade tipográfica rígida de todas as linhas do site.
- Mobile: margens de 24 px, empilhamento e ordem de leitura. O alinhamento horizontal imagem/texto deixa de fazer sentido quando estão um abaixo do outro.
- FAQ, rodapé, faixa de vídeo, etapas e descrição/CTA das aberturas passam a compartilhar os eixos do conteúdo. Cards de soluções usam linhas compartilhadas quando o navegador suporta subgrid.

## Evidências e correções

S2 = problema visual relevante; S3 = inconsistência de acabamento. Classificação restrita a esta revisão, sem inferir impacto quantitativo em conversão.

| Achado | Prioridade | Antes | Depois |
| --- | --- | --- | --- |
| Títulos centralizados em relação à fotografia | S2 | Virtù: título 104 px abaixo do topo; ofertas de palestras: 199–239 px abaixo | Diferença de 0 px nos 15 pares medidos |
| Texto/CTA ultrapassando a fotografia | S2 | Veridiana, bloco 07: botão terminava 358 px abaixo da foto | Base do botão coincide com a foto |
| Ações sem alinhamento inferior | S2 | Palestras: botões 158–198 px acima da base | Diferença de 0 px nos 9 pares com CTA |
| Colunas e margens divergentes | S3 | Etapas com intervalo de 32 px; texto do vídeo começava em x=96 no Full HD | Intervalo de 24 px e borda do conteúdo em x=240 |
| Espaçamentos locais inconsistentes | S3 | Intervalos definidos separadamente por componente | Escala comum e agrupamento por proximidade |

Medições referem-se às caixas de layout do navegador, não ao limite visível de cada glifo. Evidências locais: qa/grid-before.json, qa/grid-after.json e screenshots qa/grid-after-virtu.png / qa/grid-after-palestras.png.

## Copy e validação

Nenhum texto comercial foi reescrito. Nas palestras, o rótulo da oferta foi movido do corpo para o marcador da seção, mantendo suas palavras. Foram conferidos 368 títulos/parágrafos aprovados das páginas internas. A copy da home permaneceu intacta.

As 12 páginas passaram em 1920×1080, 1280×720, 390×844, 360×640 e 844×390: 60 combinações no Chrome. Verificações: dimensões das aberturas, ausência de overflow horizontal, títulos sem sobreposição, imagens carregadas, links internos/âncoras existentes, navegação do menu por teclado e ausência de erros JavaScript. A medição específica confirmou o topo dos 15 pares e a base dos 9 pares com CTA; os grupos de cards medidos também coincidem com o grid mestre.

## Limites

Esta é uma revisão visual e técnica, não um estudo com usuários. Não foram medidos ganhos de conversão, nem testados Safari ou aparelhos físicos. Os recortes das fotos se adaptam à altura do texto e merecem revisão editorial por página. Não houve alteração da lógica dos formulários ou envio de mensagens.
