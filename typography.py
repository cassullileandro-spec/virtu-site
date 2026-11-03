"""Keep the final word attached without rewriting approved copy."""
import re
from bs4 import BeautifulSoup

def finish_typography(html):
    doc = BeautifulSoup(html, 'html.parser')
    for block in doc.select('main h1, main h2, main h3, main h4, main p, main blockquote'):
        if len(block.get_text(' ', strip=True).split()) < 3:
            continue
        nodes = [node for node in block.find_all(string=True)
                 if node.strip() and not node.parent.has_attr('aria-hidden')]
        if nodes:
            last = nodes[-1]
            last.replace_with(re.sub(r'(?<=\S)\s+(\S+\s*)$', '\u00a0\\1', str(last)))
    return str(doc)
