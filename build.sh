docker build --no-cache -t isthistechsupport/discord_transcriber:latest \
    -t isthistechsupport/discord_transcriber:1 \
    -t isthistechsupport/discord_transcriber:1.0 \
    -t isthistechsupport/discord_transcriber:1.0.0 . &&
docker image prune -f && \
docker push -a isthistechsupport/discord_transcriber
