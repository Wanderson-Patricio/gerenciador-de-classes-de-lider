## Exemplo de Uso

```python
import requests
import os

data = requests.get(
    'http://localhost:3000/api/repositories/teste-de-repositorio',
    headers={
        'x-api-token': os.getenv('GITHUB_API_TOKEN')
    }
)

print(data.status_code)
print(data.json())
```