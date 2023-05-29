FROM python:3.9.13

WORKDIR /app

COPY main.py requirements.txt ./
COPY pages ./pages

RUN pip install -r requirements.txt

EXPOSE 8090

CMD ["streamlit", "run", "main.py", "--server.port", "8090"]
