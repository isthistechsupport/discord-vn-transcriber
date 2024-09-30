docker build --no-cache -t discord_transcriber:latest . && \
docker image prune -f && \
docker run --name discord-transcriber --network="host" --rm discord_transcriber:latest -d && \
docker logs discord-transcriber -f
