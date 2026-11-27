FROM docker.io/library/python:3.14 AS zip
WORKDIR /game
COPY game.py main.py crt.py ./
COPY scripts scripts
COPY data data
RUN mkdir /site && python -m zipfile -c /site/game.zip game.py main.py crt.py scripts data

FROM docker.io/library/nginx
COPY index.html /usr/share/nginx/html/index.html
COPY --from=zip /site/game.zip /usr/share/nginx/html/game.zip

# podman build . -t ninja-game && podman run --rm -p 8000:80 ninja-game
