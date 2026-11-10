# Virtù — site aprovado no Figma

[Prévia online](https://virtu-editorial-previa.cassullileandro.chatgpt.site/) · [GitHub](https://github.com/cassullileandro-spec/virtu-site) · [Figma aprovado](https://www.figma.com/design/DtC8cjFITfeoEF3ejiVW8D?node-id=787-989)

As 16 páginas foram transpostas da versão aprovada de 10/11/2026. O desktop de referência tem 1920 px, conteúdo de 1280 px, fontes Editor’s Note e Geist e o rodapé compartilhado. A implementação preserva textos, fotografias, cores, posicionamentos e hierarquia do arquivo.

## Visualizar e reconstruir

As páginas de `dist/` são HTML, CSS e JavaScript estáticos, sem framework obrigatório no navegador.

```sh
python3 -m http.server 4180 --directory dist
python3 build.py
python3 test_figma_site.py
```

A reconstrução usa BeautifulSoup 4, já utilizado pelo projeto. `build-pages.py` é uma entrada equivalente. A hospedagem não requer Python.

## Fontes de edição

- `sources/figma/*.tsx`: snapshots do código de alta fidelidade retornado pelo Figma, com referências locais aos assets.
- `sync-figma.py`: converte os snapshots em HTML sem depender de React ou Tailwind; valida classes desconhecidas antes de gravar.
- `enhance-figma.py`: aplica semântica, destinos e controles nativos, preservando a composição.
- `dist/figma-site.css`: estilos desktop gerados; não editar manualmente.
- `dist/responsive.css`: composição mobile e adaptação de larguras.
- `dist/figma-site.js`: menu, vídeo, carrossel e abertura de rascunhos no WhatsApp.
- `sources/figma/interactions.json`: respostas e conteúdos de interação preservados da versão anterior.
- `sources/figma/dimensions.json`: medidas das 16 páginas e seções no Figma.

Os estilos antigos permanecem no histórico e no acervo, mas não são carregados pelas páginas atuais. Os antigos testes de seletores foram substituídos pela verificação de fonte e pela suíte de navegador abaixo.

## Fundos mobile

São 17 arquivos independentes em `dist/assets/mobile/`: um para cada hero e outro para o teaser. Os cards de palestras e jornadas também selecionam essas composições no celular por meio de `picture/source`. As imagens desktop foram mantidas.

Os fundos foram compostos com as fotografias aprovadas, usando recortes próprios, tratamentos originais e gradientes na cor da página. Não foram geradas novas pessoas.

As peças permanecem editáveis na página [Fundos mobile · site publicado](https://www.figma.com/design/DtC8cjFITfeoEF3ejiVW8D?node-id=1005-989). `mobile-backgrounds.json` relaciona cada arquivo ao seu frame.

## Verificação

`python3 test_figma_site.py` verifica preservação da copy do Figma, assets locais, links e âncoras, páginas das palestras, campos dos formulários e fundos mobile.

`qa/figma-site.cjs` usa Puppeteer Core e Chrome disponíveis no ambiente. Pode receber `PUPPETEER_MODULE`, `CHROME_BIN`, `QA_URL` e `QA_OUTPUT`. Cobre as 16 páginas em 390, 1440 e 1920 px, sem overflow de textos, imagens quebradas ou labels colapsadas; verifica menu, FAQ, jornadas, carrossel, vídeo e os dois formulários. O teste intercepta a abertura do WhatsApp: não envia mensagens.

As legendas do teaser continuam sendo a transcrição automática anterior e precisam de revisão audiovisual. A conferência foi feita em navegador, sem teste em aparelhos físicos.

## Publicação

O Site existente é mantido por `.openai/hosting.json`, no mesmo endereço público. O fluxo de publicação sincroniza o commit da fonte antes de empacotar `dist/`. A branch `main` do GitHub acompanha esse commit. O domínio institucional não é alterado por este projeto.
