# ninja game on pgweb

The ninja platformer from [DaFluffyPotato's pygame tutorial](https://www.youtube.com/watch?v=2gABYM5M0ww), ported to the browser with [pgweb](https://pypi.org/project/pgweb/).
The game code is the tutorial's, the port adds the web entry, the page and a CRT screen shader drawn with moderngl.

```sh
podman build . -t ninja-game && podman run --rm -p 127.0.0.1:8000:80 ninja-game
```

Open http://127.0.0.1:8000/, arrow keys move and jump, `x` dashes.

`python desktop.py` runs the same game natively with pygame-ce and moderngl.
