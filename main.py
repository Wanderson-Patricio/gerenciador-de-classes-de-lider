from dotenv import load_dotenv
import requests
import os

load_dotenv()

data = requests.delete(
    'http://localhost:3000/api/repositories/teste-de-repositorio-2',
    headers={
        'x-api-token': os.getenv('GITHUB_API_TOKEN')
    }
)

print(data.status_code)
print(data.json())