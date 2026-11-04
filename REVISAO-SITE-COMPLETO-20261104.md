# Revisão de grid — Virtù — 04/11/2026

Aplicação da skill `layout-grid-responsivo`, preservando conteúdo, identidade, tipografia, imagens e composição aprovada. Escopo: home e 11 páginas internas.

## Recuperação e evidências

Estado inicial: commit `7e7066a195aa1f57eb607718a9b30f41691ef364`.
Backup recuperável: `qa/site-completo-20261104/estado-anterior.tar.gz`.
Capturas completas das 11 internas, antes/depois, em 1440 e 390 px; capturas por seção com guias. Diretórios `qa/site-completo-20261104/antes` e `depois`. As guias são uma sobreposição do viewport; os prints por seção complementam as capturas completas.

## Sistema preservado

Container de até 1440 px; margens desktop mínimas de 32 px, ampliadas em telas largas; 12 colunas e gutters de 24 px. Mobile: margens de 24 px e guias de 4 colunas com gutter de 16 px. Guias estruturais fixas em intervalos de 32 px a partir da origem interna da seção, subdivisão de 8 px opcional. Contornos observados separados das referências.

Páginas internas: padding regular de 104 px desktop, 96 px tablet e 72 px mobile. Home: família já aprovada de 96/80/64 px; seção de impacto e hero preservam sua composição. Igualdade entre componentes equivalentes, sem impor a mesma altura a todos os módulos.

## Problemas e correções mínimas

| Elemento / eixo esperado | Observado | Causa e correção |
|---|---|---|
| CTA da hero interna / início da coluna 9 | Em 1440 px, exemplo começava perto de x1131 em vez de x965 | Alinhamento ao final da área de grid. Alterado `justify-self` para início acima de 700 px. |
| CTA de fechamento / base compartilhada com a copy | Desvio de aproximadamente 80 px em fechamento com uma linha | Margem global de actions e span em linhas implícitas. Copy agrupada, CTA na mesma linha externa, margem redundante removida. |
| Processo da Mentoria / texto dentro da coluna | “ACOMPANHAMENTO” excedia em 57 px em 1101 px | Quatro tracks estreitos para o tamanho aprovado. Duas colunas entre 701–1359 px; quatro a partir de 1360 px. |
| Quatro pilares / títulos dentro de cada componente | “CULTURA DE CRESCIMENTO” excedia cerca de 43 px | Mesma adaptação para duas colunas intermediárias, sem reduzir fonte. |
| Títulos de índice, formulário e linhas de pilares / coluna reservada | PHD excedia 61 px em 901 px; “Como podemos ajudar” cerca de 17 px | Havia uma coluna vazia antes da área vizinha. Span ampliado nessa coluna em 901–1359 px, mantendo gutter. |
| Padding de módulos equivalentes | Alguns módulos mobile usavam 65 px contra 72; fechamento tablet usava 100 contra 96 | Regra compartilhada de padding reaproveita `--space` nas internas até 900 px. |
| Último bloco de contato / fluxo título-copy-CTA | Gap da copy herdava altura da coluna do título | Parágrafos e actions agrupados em `.editorial-copy`, mantendo ordem textual. |
| Revisão de grid / medidas estáveis | Animações internas ainda moviam elementos durante a revisão | `pages.js` agora respeita `gridReview`; animações continuam no modo normal. Contornos incluem textos e botões internos. |

Não foram adicionados offsets isolados, quebras artificiais, redução de fonte nem cortes de conteúdo. Fontes e entrelinhas existentes foram mantidas. Cap height, baseline e trim óptico permanecem conforme o sistema já aprovado; caixa e tinta visível não são tratadas como a mesma medida.

## Cobertura e validação

Páginas: index, virtu, veridiana, palestras, gravado, oficina, mentoria, phd, vanguard, empresas, trabalhe, contato.

- 132 verificações DOM reais: 11 internas × 12 larguras (360, 390, 700, 701, 900, 901, 1100, 1101, 1359, 1360, 1440, 1920), altura 900 px, fontes carregadas. Resultados em `depois/testes-grid.json`.
- Verificação por Range dos textos dentro de suas colunas, eixos dos CTAs, bases dos fechamentos e padding dos containers.
- 28 perguntas/tópicos abertos em 390, 901 e 1440 px, nas páginas Palestras, Oficina, PHD e Vanguard: 12 estados completos aprovados.
- Formulário de contato expandido para Palestra: 11 campos visíveis dentro da coluna em 390, 901 e 1440 px. Sem envio de formulário ou mensagem.
- Home: nove larguras, de 390 a 1920 px, incluindo transições 700/701, 900/901 e 1100/1101. Topos das fotos, coluna 7, largura da foto e gaps de título/texto/CTA preservados.
- Heroes internas em 390×667, 844×390 e 1440×650: 33 verificações de espaço/overflow aprovadas.
- Todas as seções das 11 internas percorridas em desktop/mobile para carregar imagens antes das capturas. Nenhuma imagem ausente nesses estados.
- Comparação visual das páginas completas e dos módulos com guias. Exemplo pareado: `antes/mentoria-1101-processo.jpg` e `depois/mentoria-1101-processo.jpg`.
- Modo normal da Mentoria: hero e copy visíveis após animação, opacidade 1, transformação final sem deslocamento e camada de revisão ausente.
- `python3 build-pages.py`, `python3 test_typography.py`, checagem de sintaxe JS e `git diff --check`: aprovados.
- Comparação contra backup: mesmas palavras na mesma ordem, mesmas imagens/alt e mesmos destinos dos links em todas as 12 páginas.

`antes/detalhes.json` e `depois/transicoes.json` contêm diagnósticos intermediários anteriores à correção final; não representam o resultado final. Os arquivos `testes-*.json` finais registram os estados aprovados.

## Exceções intencionais e limites

Parágrafos independentes conservam alturas naturais. Cards conservam padding próprio. Hero, foto editorial, seção de impacto e rodapé não recebem artificialmente o padding dos módulos comuns. Fotos grandes e espaço editorial aprovado permanecem. Não há obrigação de terminar cada linha de texto sobre a malha.

Não foram testados Safari/Firefox, aparelhos físicos nem envio real de formulários. Não foi feita auditoria funcional completa de todos os destinos externos. Compatibilidade de trim óptico pode variar por navegador.

A publicação e a confirmação no Chrome ficam registradas no comprovante em `qa/site-completo-20261104/depois/publicacao.json` e nos prints `chrome-*.jpg` após o deploy.
