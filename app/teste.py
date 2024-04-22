from dotenv import load_dotenv
import os

# Carregar variaveis do arquivo .env
load_dotenv()
print(os.getenv("DB_NAME"))
print(os.getenv("DB_USER"))
print(os.getenv("DB_PASSWORD"))
print(os.getenv("DB_HOST"))
print(os.getenv("DB_PORT"))