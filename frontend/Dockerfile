FROM node:18-alpine as builder
WORKDIR /app
ARG MODE=local
ARG SERVER_NAME
ENV PROTOCOL=http
RUN if [ "$MODE" != "local" ]; then PROTOCOL=https; fi
RUN echo "VITE_API_URL=$PROTOCOL://$SERVER_NAME" >> .env
COPY ./package*.json .
RUN npm install
COPY . .
CMD [ "npm", "run", "build" ]
