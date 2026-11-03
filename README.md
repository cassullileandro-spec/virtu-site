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

A hero aprovada é baseada no quadro 363:2864. As demais seções foram redesenhadas para o navegador. Referência: https://www.spectup.com/.

## Comportamento

Menu em diálogo nativo; jornadas e FAQ em `details`; desafios por controles; vídeo local 142 s com legendas automáticas; contato abre uma mensagem revisável no WhatsApp oficial confirmado na home da Virtù. Nenhuma mensagem é enviada automaticamente.

A prévia é um Site separado, inicialmente privado. A produção existente não foi modificada. Manifesto: `.openai/hosting.json`.

## Pendências editoriais

As legendas usam transcrição automática já existente no acervo e precisam de revisão audiovisual. Um trecho de baixa confiança foi marcado como incerto. As fotografias vêm do projeto; a hero aprovada tem cenário trabalhado por IA conforme manifesto original.
