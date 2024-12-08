# FROM python:3.12
FROM python:3.12-slim
# RUN apt-get update && apt-get install -y bash coreutils
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
EXPOSE 5000
CMD ["bash", "-c", "python src/run.py"]
# CMD ["-c", "python src/run.py"]
