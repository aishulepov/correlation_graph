# Запуск из Docker

sudo docker build . -t correlation-app

sudo docker run -p 8501:8501 correlation-app:latest

# Запуск с сервера

streamlit run --server.port  8500 graph_correlation.py

# Запуск в облаке Streamlit

https://share.streamlit.io
