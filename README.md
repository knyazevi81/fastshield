<p align="center">
  <img src="media/logo-goriz.png" alt="FastShield"></a>
</p>
<p align="center">
    <em>FastShield Web application firewall, easy to integration, fast to code
    </em>
</p>

<p align="center">
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastshield?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastshield.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

## Installation
<div class="termy">

```console
$ pip install fastshield
```
</div>

---
## Example
* code with a simple `vulnerability`
```Python
from typing import Union

from fastapi import FastAPI
from fastshield.fshield import FSMiddleware

app = FastAPI()

app.add_middleware(FSMiddleware)

@router.get("/redirect_endpoint")
def read_root(redirect_url: str):
    return HTMLResponse(
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>xss hack test</title>
        </head>
        <body>
            <script>window.location="{redirect_url}"</script>
        </body>
        </html>
        """
    )

```