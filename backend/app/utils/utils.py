import json
import re

def extract_json(text: str):
    text = text.strip()
    
    try:
        return json.loads(text)
    except Exception:
        pass
    
    match = re.search(
        r"```json\s*(.*?)\s*```",
        text,
        re.DOTALL
    )
    
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass
        
    match = re.search(
        r"(\[.*\])",
        text,
        re.DOTALL
    )
    
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass
        
    return []