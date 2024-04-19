docker build --no-cache -t discord_transcriber:latest . \
&& docker image prune -f && \
docker run --name discord_transcriber --network="host" -it --rm discord_transcriber:latest
