import urllib.parse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

import urllib
import json

from fastshield.request import BaseRequest
from fastshield.classifire.classifire import ThreatClassifier


class FSMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.origin: str = ""
        self.host: str = ""
        self.url: str = ""
        self.base_url: str = ""
        self.cut_url: str = ""
        self.headers: dict = {}
        self.method: str = ""

    def __classfy(self) -> BaseRequest:
        req = BaseRequest(
            origin=self.origin,
            host=self.host,
            request=self.cut_url,
            method=self.method,
            headers=self.headers,
            body=self.cut_url
        )
        req = ThreatClassifier().classify_request(req)

        return req


    async def dispatch(self, request: Request, call_next):
        self.origin = str(request.client.host)
        self.host = str(request.url.hostname)
        self.url = urllib.parse.unquote(str(request.url))

        self.base_url = urllib.parse.unquote(str(request.base_url))
        self.cut_url = urllib.parse.unquote(self.url.replace(self.base_url, "")) # test?redirect_url=<script>alert(1)</script>
        self.headers = dict(request.headers)
        self.method = str(request.method)

        req = self.__classfy()
        print(req.threats)

        response = await call_next(request)
        return response