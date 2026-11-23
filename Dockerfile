FROM python:3.12
ENV MONGO_URL="mongodb://mongo:27017"
ENV MONGO_DB_NAME="movie_api"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 