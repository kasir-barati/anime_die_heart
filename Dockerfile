FROM python:3.10.5-alpine3.15

COPY requirements.txt .
RUN pip install --user -r requirements.txt

WORKDIR /app

CMD ["/bin/bash"]