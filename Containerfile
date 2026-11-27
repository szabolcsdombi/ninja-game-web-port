FROM docker.io/library/python:3.14 AS build
WORKDIR /game
COPY game.py main.py crt.py ./
COPY scripts scripts
COPY data data
RUN mkdir /site && python -m zipfile -c /site/game.zip game.py main.py crt.py scripts data
COPY index.html /site/index.html

FROM scratch AS site
COPY --from=build /site /

FROM docker.io/library/nginx
COPY --from=build /site /usr/share/nginx/html

# podman build . -t ninja-game && podman run --rm -p 8000:80 ninja-game
# podman build . --target site -o site
