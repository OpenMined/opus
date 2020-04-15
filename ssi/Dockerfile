# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:10 as build-stage
WORKDIR /app

COPY package*.json /app/

RUN npm install

copy ./ /app/

CMD ["npm", "start"]
