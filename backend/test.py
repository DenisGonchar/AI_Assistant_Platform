from app.web.manager import SearchManager

manager = SearchManager()

results = manager.search('погода вс севастополе')

for item in results:
    print(item)