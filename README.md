# Virtù — prévia editorial

Home responsiva em HTML/CSS/JavaScript, com GSAP 3.15.0 e ScrollTrigger locais. Sem backend, cookies de rastreamento ou formulário com envio simulado.

## Rodar

Na raiz deste diretório:

    python3 -m http.server 4173 --directory dist

## Editar

- `dist/styles.css`: layout e responsividade.
- `dist/app.js`: menu, jornadas, vídeo, desafios, WhatsApp e movimento.
- `build.py`: composição da home a partir dos textos oficiais.
- `copy-fonte.json`: captura da copy do quadro Figma 292:2012.
- `dist/assets`: fotografias, fontes, marca, dependências e teaser comprimido.

Após alterar `build.py` ou a copy, execute `python3 build.py`. CSS e JS não são sobrescritos.

A hero da home segue a capa das apresentações, componente Figma 194:1558: fundo cinza, retrato JEF01830 em preto e branco, Editor’s Note e Geist. O estilo responsivo está em `dist/hero-cover.css`; o recorte original e as fontes ficam em `dist/assets`. As demais seções foram redesenhadas para o navegador. Referência: https://www.spectup.com/.

## Comportamento

Menu em diálogo nativo; jornadas e FAQ em `details`; desafios por controles; vídeo local 142 s com legendas automáticas; contato abre uma mensagem revisável no WhatsApp oficial confirmado na home da Virtù. Nenhuma mensagem é enviada automaticamente.

A prévia é um Site separado, inicialmente privado. A produção existente não foi modificada. Manifesto: `.openai/hosting.json`.

## Revisão visual de grid

Na home, acrescente `?grid=1` à URL. O painel desenha colunas, limites/padding das seções, caixas dos blocos e, opcionalmente, uma malha de 8 px. Mostra diferenças entre topos e deslocamentos laterais. Âmbar indica uma diferença a investigar, não um erro automático. Recolher mantém o desenho; sair da revisão retorna ao site normal.

As animações de entrada são desativadas somente nessa URL para medir a composição final. O script `dist/grid-review.js` só é carregado nesse modo. A home mantém 12 colunas acima de 700 px e uma referência de quatro colunas abaixo; blocos lado a lado empilham até 900 px.

`test_grid_layout.js` contém uma função de verificação DOM, para executar no contexto da home renderizada. Confere overflow de conteúdo, alinhamento do FAQ, pares imagem/texto, margem adicional dentro do título, ativação da revisão e correspondência entre retângulo desenhado e caixa real. Não substitui inspeção visual.

## Pendências editoriais

As legendas usam transcrição automática já existente no acervo e precisam de revisão audiovisual. Um trecho de baixa confiança foi marcado como incerto. As fotografias vêm do projeto; a hero aprovada tem cenário trabalhado por IA conforme manifesto original.

## Páginas internas / grid

`python3 build-pages.py` recompõe a home e as 11 internas. Usa BeautifulSoup, já disponível no ambiente de autoria; a hospedagem serve somente HTML, CSS e JS estáticos.

`dist/pages.css` define a base Full HD: 1440 px úteis, grid de 12 colunas, gutters de 24 px e heros 100vh × 100vw. `dist/pages.js` cuida das animações internas e dos formulários que abrem rascunhos no WhatsApp. As fontes aprovadas e os ajustes editoriais estão em `sources/approved-pages.json` e `ALTERACOES-PAGINAS.md`.
