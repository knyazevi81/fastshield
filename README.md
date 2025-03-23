<p align="center">
  <img src="media/logo-goriz.png" alt="FastShield">
</p>
<p align="center">
    <em>FastShield - Web Application Firewall, easy to integrate, fast to deploy.</em>
</p>

<p align="center">
<a href="https://pypi.org/project/fastshield" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastshield?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastshield" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastshield.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

## 🚀 Features
- **Easy Integration**: Add security to your FastAPI application with minimal effort.
- **Custom Middleware**: Protect your application from common vulnerabilities like XSS, SQL Injection, and more.
- **Rate Limiting**: Prevent abuse by limiting the number of requests per client.
- **Country Blocking**: Restrict access based on geographic location.
- **Bot Protection**: Detect and block malicious bots.

---

## 📦 Installation
<div class="termy">

```console
pip install fastshield
```
</div>

---

## 🛠️ Usage
Here is an example of how to use `FastShield` in your FastAPI application:

```Python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastshield.middleware import HackMiddleware

app = FastAPI()

# Add FastShield middleware
app.add_middleware(HackMiddleware)  # Security middleware

@app.get("/redirect_endpoint")
def read_root(redirect_url: str):
    return HTMLResponse(
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>XSS Hack Test</title>
        </head>
        <body>
            <script>window.location="{redirect_url}"</script>
        </body>
        </html>
        """
    )
```

---

## 🔒 Security Features
### 1. **XSS Protection**
FastShield helps mitigate Cross-Site Scripting (XSS) attacks by sanitizing user inputs and blocking malicious scripts.

### 2. **Rate Limiting**
Prevent abuse by limiting the number of requests per client within a specified time window.

### 3. **Country Blocking**
Restrict access to your application based on geographic location.

### 4. **Bot Protection**
Detect and block malicious bots using advanced heuristics.

---

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

