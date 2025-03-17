from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import FastAPI

import urllib.parse

from fastshield.request import BaseRequest
from fastshield.classifire.classifire import ThreatClassifier

from fastshield.exceptions.hackexceptions import HackException


class FSHackMiddleware(BaseHTTPMiddleware):
    def __init__(
            self, 
            app: FastAPI,
            allow_signature: bool = True
        # ADD allow_exceptions 404 json or redirect to 404.html
        ) -> None:
        super().__init__(app)
        self.allow_signature: bool = allow_signature
        self.origin: str = ""
        self.host: str = ""
        self.url: str = ""
        self.base_url: str = ""
        self.cut_url: str = ""
        self.headers: dict = {}
        self.method: str = ""


    def __singanture_analyse(self,) -> None:
        ...

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
        try:
            self.origin = str(request.client.host)
            self.host = str(request.url.hostname)
            self.url = urllib.parse.unquote(str(request.url))

            self.base_url = urllib.parse.unquote(str(request.base_url))
            
            # test?redirect_url=<script>alert(1)</script>
            self.cut_url = urllib.parse.unquote(self.url.replace(self.base_url, "")) 
            self.headers = dict(request.headers)
            self.method = str(request.method)

            if self.allow_signature:
                ...

            classifyed_request = self.__classfy()
            if not "valid" in classifyed_request.threats:
                return JSONResponse(status_code=403, content={"detail": "forbidden"})

            response = await call_next(request)
            return response
        except Exception as e:
            response = await call_next(request)
            return response
        

class FSCountryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        return await super().dispatch(request, call_next)
    

class FSBotMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        return await super().dispatch(request, call_next)