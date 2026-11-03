from bs4 import BeautifulSoup
from typography import finish_typography

source = '<main><h2>Texto com <em>última palavra isolada.</em></h2><p>Texto longo com uma palavra final.</p><h3>Dúvidas frequentes</h3><h2>Como podemos ajudar?</h2></main><footer><p>Texto do rodapé.</p></footer>'
result = finish_typography(source)
assert 'palavra\u00a0isolada.' in result
assert 'palavra\u00a0final.' in result
assert 'podemos\u00a0ajudar?' in result
assert '<em>' in result and 'Dúvidas frequentes' in result
assert '<footer><p>Texto do rodapé.</p></footer>' in result
assert BeautifulSoup(source, 'html.parser').get_text().split() == BeautifulSoup(result, 'html.parser').get_text().split()
assert finish_typography(result) == result
print('Typography: words, markup, short titles, scope and idempotence OK')
