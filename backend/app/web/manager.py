from app.web.providers.duckduchgo import DuckDuckGoSearch


class SearchManager:
    def __init__(self):
        self.provider = DuckDuckGoSearch()
        
    def search(self, query: str):
        return self.provider.search(query)