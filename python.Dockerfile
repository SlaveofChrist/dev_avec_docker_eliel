FROM python:3.9
RUN useradd -m -s /bin/bash apiuser
WORKDIR /server
COPY requirements.txt .
COPY postgres-test.py .
RUN pip install -r requirements.txt
RUN chown -R apiuser:apiuser /server
USER apiuser
EXPOSE 8000