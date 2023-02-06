# using Nginx base image
FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY dockerfiles/nginx/nginx.conf /etc/nginx/nginx.conf