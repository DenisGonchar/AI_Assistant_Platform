from ddgs import DDGS

from app.web.base import BaseSearch


class DuckDuckGoSearch(BaseSearch):
    def search(self, query) -> list[dict]:
        with DDGS() as ddgs:
            results = ddgs.text(
                query=query,
                max_results=5
            )
            
            if not results():
                return []
            
            return [
                {
                    'title': item['title'],
                    'url': item['href'],
                    'content': item['body']
                }
                for item in results
            ]
        return []