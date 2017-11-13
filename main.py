from bs4 import BeautifulSoup

f = open('./assets/wbc_20171114.html')
input = f.read()

soup = BeautifulSoup(input, 'html.parser')

res = dict()
d = [c for c in soup.section.ul.children]

for node in d:
    date_key = node.find_all('span', class_='date') 
    res[date_key] = {
            'count': node.div.span.text,
            'date': date_key,
            'time': node.find_all('span', class_='time') 
            }

print(res)
