<b>DOCKER SETUP:</b><br>
```
docker compose up --build --scale fastapi=4
```
It will spin one redis-cache database, one redis-insight container and 4 services with nginx as a reverse-proxy.

<b>REDIS INSIGHT: </b><br>
To add Redis Database select "I already have a database", and after that "Connect to a Redis Database":
- Host:host.docker.internal
- Port:6379
- Name: 0