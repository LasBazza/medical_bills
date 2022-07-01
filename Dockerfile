FROM python:3.10-slim

WORKDIR app

COPY ./ ./

RUN pip install -r requirements.txt

RUN chmod +x /app/run_script.sh

ENTRYPOINT ["/app/run_script.sh"]