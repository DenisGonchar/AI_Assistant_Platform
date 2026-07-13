from tavily import TavilyClient

from app.core.config import settings

from app.web.base import BaseSearch


class TavilyProvider(BaseSearch):
    def __init__(self):
        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY
        )
        
    def search(self, query: str) -> list[dict]:
        response = self.client.search(
            query=query,
            search_depth='basic',
            max_results=5
        )
        
        return response['results']
        