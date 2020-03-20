# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:10 as build-stage

WORKDIR /app

# Copy & install packages first to preserve layers
COPY package*.json /app/
COPY yarn.lock /app/

RUN yarn install

COPY ./ /app/

RUN yarn run build

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.15

COPY --from=build-stage /app/build/ /usr/share/nginx/html
COPY --from=build-stage /app/nginx.conf /etc/nginx/conf.d/default.conf
