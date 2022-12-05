FROM python:3.10.8-alpine3.17
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./src/dubois.py" ]