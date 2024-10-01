FROM python:3.12
EXPOSE 8000
ENV WIKI_PORT 8000
WORKDIR /app
RUN apt-get update && apt-get install pandoc -y
COPY requirements.txt .
RUN ["pip", "install", "-r", "requirements.txt", "--no-cache-dir"]
COPY . .
CMD ["python", "main.py"]
