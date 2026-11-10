# Virtù — implementação responsiva

[Site](https://virtu-editorial-previa.cassullileandro.chatgpt.site/) · [GitHub](https://github.com/cassullileandro-spec/virtu-site) · [Figma aprovado](https://www.figma.com/design/DtC8cjFITfeoEF3ejiVW8D?node-id=787-989)

A base responsiva e as interações da versão 29 foram recuperadas. As alterações editoriais do Figma foram aplicadas sobre essa base. O canvas de 1920 px é uma referência de composição: não define a largura do navegador e não é reduzido com CSS zoom.

## Construir e visualizar

A entrada completa é:

```sh
python3 build-pages.py
python3 test_figma_site.py
python3 -m http.server 4180 --directory dist
```

A construção usa BeautifulSoup 4, já utilizado pelo projeto. A hospedagem serve HTML, CSS e JavaScript estáticos, sem Python ou framework no navegador.

- `build.py`: home original, navegação, contato, vídeo, carrossel e jornadas.
- `build-pages.py`: páginas internas e palestras; chama a aplicação editorial ao terminar.
- `apply-approved.py`: textos, fotografias, cards, paletas e rodapé aprovados; converte as colunas editoriais em trilhas fluidas e mantém formulários e FAQs anteriores.
- `sync-figma.py` / `enhance-figma.py`: leitura dos snapshots e identificação dos conteúdos. Não geram mais um site com largura fixa.
- `dist/styles.css`, `pages.css`, `design-system.css`, `hero-cover.css`, `internal-editorial.css`, `journey-covers.css`: estilos originais.
- `dist/approved.css`: ajustes editoriais e contrato responsivo atual.
- `dist/app.js` / `pages.js`: comportamentos e animações GSAP originais, com os novos blocos incluídos nos seletores.

Não executar somente `build.py` para publicar: ele produz apenas a base da home. `build-pages.py` constrói o conjunto completo.

## Contrato de layout

Conteúdo útil máximo de **1280 px**, com margens mínimas de 32 px no desktop e 24 px no celular. Em 1440 px, o conteúdo central tem 80 px de margem; em 1920 px, 320 px. Heroes e imagens de fundo podem ocupar a tela inteira.

Texto de leitura permanece em **18/28 px** no desktop e **16/24 px** no celular. A escala tipográfica anterior de títulos foi preservada. O DPR de uma tela Retina não altera o tamanho CSS do texto. Os fundos e as colunas se adaptam à largura disponível; não há escala global.

Seções usam alturas determinadas pelo conteúdo e espaçamento vertical de 96 px no desktop, 80 px na faixa intermediária e 64 px no celular. Fotos e capas têm proporções ou altura mínima próprias.

No mobile, grades e cards passam a uma coluna, com 24 px de recuo, 32 px entre blocos e 16 px entre título e descrição de um card. Padding interno herdado do desktop não se soma ao padding da seção. Capas com fotografia se dividem em imagem e texto; os números das listas mantêm uma coluna própria.

Os arquivos de `sources/figma/` preservam a referência aprovada. Os fundos mobile ficam separados em `dist/assets/mobile/`, com seus frames editáveis na página [Fundos mobile](https://www.figma.com/design/DtC8cjFITfeoEF3ejiVW8D?node-id=1005-989). As páginas internas selecionam seus fundos por `picture/source`.

## Verificação

`test_figma_site.py` confere 16 rotas, copy aprovada, assets, links, formulários e o carregamento do runtime original.

`qa/responsive-recovery.cjs` verifica larguras de 390, 1280, 1440, 1512 e 1920 px, ausência de escala global, overflow, imagens quebradas e fotografias colapsadas; também produz capturas completas.

`qa/native-interactions.cjs` verifica Retina 1440 px, movimentos ativos nas 16 páginas, menu, FAQ, jornadas, carrossel, vídeo, contato e os dois formulários. A abertura do WhatsApp é interceptada: nenhum teste envia mensagens.

Os testes usam Chrome e Puppeteer Core locais. A simulação de viewport não substitui testes em Safari e aparelhos físicos. As legendas automáticas anteriores do teaser ainda precisam de revisão audiovisual.

## Publicação e recuperação

A identidade do Site está em `.openai/hosting.json`. O endereço público permanece o mesmo e a branch main do GitHub recebe o mesmo commit.

A versão 29, commit `b85194900fc9b6007c1c61c9011d37b6f802d96d`, é a base anterior recuperável. A versão 30 permanece no histórico, mas sua implementação com canvas escalado foi retirada.
