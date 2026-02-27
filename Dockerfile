FROM python:3.12-slim

# Define pasta de trabalho dentro do container
WORKDIR /app

# Copia apenas requirements primeiro (melhora cache)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expõe a porta usada pelo FastAPI
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]