FROM python:3.9
RUN useradd -m -s /bin/bash apiuser
WORKDIR /server
COPY requirements.txt .
COPY . . 
RUN pip install -r requirements.txt
RUN chown -R apiuser:apiuser /server
USER apiuser
EXPOSE 8000
CMD ["uvicorn", "postgres-test:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]