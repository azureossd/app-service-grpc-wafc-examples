FROM node:18.4.0-alpine3.16

WORKDIR /app
COPY package.json /app
RUN npm i 

COPY . /app

EXPOSE 50051 3000

CMD [ "node", "server.js" ]
