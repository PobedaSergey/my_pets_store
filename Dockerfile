FROM python:3.10.0

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8006

CMD [ "python", "./main.py" ]