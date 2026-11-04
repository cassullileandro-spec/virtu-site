# Revisão de grid e posicionamento — 03/11/2026

## Aplicação visual na home — 04/11/2026

Adicionado modo opt-in `?grid=1`: colunas, limites/padding horizontais, caixas medidas dos blocos e malha opcional de 8 px. Na malha, os rótulos também mostram tamanho da fonte e entrelinha computados. O painel permite saltar entre as dez seções e o rodapé, alternar camadas e recolher os controles mantendo o desenho. As animações de entrada ficam pausadas apenas nesse modo. Âmbar significa deslocamento a investigar, não erro estético automático.

Correções aplicadas à home, preservando HTML, copy, imagens e hero aprovada:

- Seções principais com padding 104/80/64 px conforme a faixa; faixas compactas com 64/56/48 px. Alturas continuam determinadas pelo conteúdo.
- FAQ: título e lista passam a compartilhar topo; removida diferença de 35 px no desktop.
- Desafios: texto passa a ocupar colunas 5–12 do grid, substituindo a divisão percentual independente.
- Retrato: divisão 5/7 e altura mínima de 520 px no desktop, em vez de 6/6 e 640 px; pilha até 900 px.
- Introdução: foto acompanha a altura do texto; removido espaçamento adicional dentro do título. No mobile, o span colorido adicionava 12 px a uma entrelinha de 43,2 px; essa margem agora é zero. Preservadas as duas frases editoriais e a escala tipográfica.
- Contato: textos e ação alinhados ao grid no desktop e empilhados no mobile. Footer mobile com gutter igual ao da página.

Verificação geométrica da home em 1920×1080, 1440×1000, 900×900, 700×900, 390×844 e 360×640: conteúdo dentro da viewport; pares alinhados no desktop; desenho do retrato coincide com sua caixa real; margem adicional do título zerada. O FAQ empilha no mobile, portanto seus topos não precisam coincidir. Teste preservado em `test_grid_layout.js`; resultados locais em `qa/layout-results.json`.

Inspeção visual das seções no desktop e dos principais ajustes no mobile. Conferidos abertura do FAQ, controle de desafios, malha, recolhimento e modo normal sem overlay. Esta aplicação se limita à home; não constitui nova auditoria das onze páginas internas. Sem teste em aparelhos físicos ou Safari/Firefox.

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

## Atualização — rótulos e palavras viúvas

A pedido do usuário, foram removidos os marcadores numerados de seção, inclusive os da home, e os espaços reservados a eles. A identificação acessível do depoimento continua disponível aos leitores de tela. Números de etapas e controles de navegação continuam fazendo parte de seus componentes.

Títulos recebem composição equilibrada e parágrafos usam text-wrap: pretty conforme a [documentação MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap). Na geração do HTML, as duas últimas palavras ficam ligadas por um espaço inseparável; não se alteram as palavras. Títulos com apenas duas palavras mantêm quebras naturais. No celular, etapas passam a uma coluna e alguns títulos longos recebem escala menor para manter a leitura e evitar transbordamento.

Validação desta atualização: 451 blocos de conteúdo preservados em comparação com a versão anterior; 12 páginas em cinco viewports sem overflow horizontal e com aberturas de dimensão exata; 15 pares imagem/título e nove pares imagem/CTA alinhados. A inspeção de quebras em quatro larguras não encontrou palavras finais isoladas nos parágrafos visíveis, descontando a seta decorativa. Permanecem títulos curtos de duas palavras em duas linhas, uma composição intencional. Há um teste do formatador em test_typography.py. Safari e aparelhos físicos continuam fora da validação.

## Auditoria visual — 03/11/2026

12 páginas revisadas em 1920×1080 e 390×844, com 222 capturas de dobra, primeira impressão/hero estável, mapas completos e estados de interação. Relatório e evidências: `../output/auditoria-2026-11-03/relatorio.html`.

Correções: títulos e cards no mesmo eixo; ação de Veridiana fora da coluna estreita; linhas compartilhadas nos pilares; reflow intermediário em tablet; distância entre imagem e texto reduzida de 146 para 24 px em Full HD, ampliando fotos de 586 para 708 px sem distorção; navegação sobre faixa própria e remoção visual do contato flutuante; separação de 24 px entre título e parágrafo final de Contato no celular.

Validação: 60 combinações de rota/viewport para hero, menu, links e imagens; 88 combinações para overflow interno; 15 alinhamentos superiores e nove inferiores com diferença zero. Copy preservada. Permanecem recomendações editoriais registradas no relatório. Não houve envio real de formulário, teste em aparelho físico, avaliação integral de contraste/leitor de tela ou validação em Safari/Firefox.


## Hero agrupada e padding uniforme — 04/11/2026

- Hero em fluxo, com altura mínima de uma tela e crescimento pelo conteúdo; retirado o posicionamento independente entre título e descrição.
- Pequeno título → H1: 24 px; H1 → descrição: 32 px; descrição → botão no mobile: 24 px. Desktop preserva as colunas da descrição e ação.
- Entrelinha do H1: 1; corrigida a margem negativa da última linha para o limite do bloco incluir a área de proteção dos glifos.
- Todas as seções de conteúdo da home com `.section-pad`: 96 px em desktop, 80 px entre 701 e 1100 px, 64 px até 700 px, acima e abaixo. Hero, filme em tela cheia e rodapé mantêm composições próprias.
- Verificadas larguras 1440, 900, 700, 470, 390, 360 e 844 px (paisagem, altura 390): sem overflow horizontal, distâncias e padding conferidos por asserções. Modo normal conferido em 390 e 1440 px; contato abre e fecha. Não houve envio de mensagem.
- Evidências locais em qa/explicacao/hero-ajustada-*.jpg. Páginas internas não foram alteradas; sem teste em dispositivos físicos.


## Caixa tipográfica e alinhamento óptico — 04/11/2026

- Aplicado cap height até baseline (`text-box-trim: trim-both; text-box-edge: cap alphabetic`) no sistema compartilhado de h1–h4, p e blockquote, incluindo as páginas internas. Browsers antigos que não suportam essas propriedades conservam a caixa tipográfica tradicional.
- Títulos da introdução, das jornadas e da seção Veridiana com entrelinha 1; mesma entrelinha no trecho colorido. Títulos adjacentes às imagens passam a alinhar o topo das maiúsculas, e não somente caixas com leading invisível.
- Miniaturas e títulos das jornadas alinhados pelo topo; números e controles permanecem centralizados.
- Nos blocos de introdução e Veridiana: 32 px título/texto e 24 px entre parágrafos. Eliminada a soma de margem do último parágrafo com a do botão no mobile; intervalo de 32 px.
- Malha de revisão preservada integralmente, como solicitado. Nenhuma imagem substituída; as oito imagens verificadas na introdução, jornadas e Veridiana carregaram. A falha de carregamento do print não se reproduziu.
- Home: asserções em 1920, 1440, 1100, 901, 900, 700, 390 e 360 px; incluindo alinhamento de miniaturas, título/foto, botão/base e gaps. Onze páginas internas: aplicação da tipografia e overflow dos textos em 1440 e 390 px. Revisão visual dos três trechos indicados e da seção Veridiana sem guias em desktop/mobile; jornadas abrem e fecham.
- Os testes geométricos não substituem a conferência visual. Não foi realizada auditoria visual completa de todas as páginas internas, teste em aparelhos físicos nem validação em navegadores antigos.
- Critério óptico registrado na skill layout-grid-responsivo, sem tornar os valores desta implementação universais.

- Na conferência publicada, a aba reutilizou CSS anterior. URLs de pages.css e design-system.css versionadas em todas as páginas e no gerador para invalidar esse cache.


## Hierarquia e entrelinha — 04/11/2026

Confirmado no Chrome a 1920 px: título da Veridiana crescia a 86,4 px e dois parágrafos alternavam 22/18 px, enquanto o container já estava limitado. Hero tinha rótulo, título, descrição e frase lateral com níveis concorrentes.

- Escala compartilhada estável: títulos de seção 48/48, 40/40 ou 32/32; texto 18/28 e 16/24; itens 32/40 ou 24/30. Abertura da home 128, 80 ou 48 px.
- Hero simplificada para título, descrição e botão; linhas com trim óptico nos wrappers, sem padding/margem negativos e sem recorte de descendentes.
- Parágrafos da Veridiana unificados; 32 px entre título/texto e texto/CTA, 24 px entre parágrafos. Foto acompanha o conteúdo sem min-height de 520 px e botão sem margem automática.
- Malha original preservada. Mantida a adição remota de botão Grid existente em 964fed8.
- Home: 1920, 1440, 1100, 901, 900, 700, 390 e 360 px. 11 internas: 1440 e 390 px, sem overflow e com trim ativo. Prints e resultados em qa/hierarquia (não versionado).
