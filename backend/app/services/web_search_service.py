from app.web.manager import SearchManager

class WebSearchService:
    def __init__(self):
        self.manager = SearchManager()
        
    def search(self, query: str):
        return self.manager.search(query)
    
    def build_prompt(self, query: str) -> str:
        results = self.search(query)
        
        if not results:
            return ''
        
        prompt = "Информация из Интернета:\n\n"

        for result in results:
            prompt += (
                f"Источник: {result['url']}\n"
                f"Заголовок: {result['title']}\n"
                f"Текст: {result['content']}\n\n"
            )
            
        return prompt