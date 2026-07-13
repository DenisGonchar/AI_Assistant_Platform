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
        
        lines = [
            "Ниже приведены актуальные результаты поиска в интернете.",
            "Используй их только если они помогают ответить на вопрос пользователя.",
            ''
        ]
        
        for index, result in enumerate(results, start=1):
            lines.extend([
                f'{index}. {result['title']}',
                f'Источник: {result['url']}',
                f'Описание: {result['content']}',
                ''
            ])
            
        return '\n'.join(lines)