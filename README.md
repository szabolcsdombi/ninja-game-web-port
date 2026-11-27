# ninja game on pgweb

A pygame-ce platformer ported to the browser with [pgweb](https://pypi.org/project/pgweb/), presented through a moderngl CRT shader.

```sh
podman build . -t ninja-game && podman run --rm -p 8000:80 ninja-game
```

Open http://127.0.0.1:8000/, arrow keys move and jump, `x` dashes.

`python desktop.py` runs the same game natively with pygame-ce and moderngl.
