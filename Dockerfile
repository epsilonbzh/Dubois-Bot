FROM python:3.8.15-slim-bullseye
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
#COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./src/dubois.py" ]