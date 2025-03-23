from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI

import urllib.parse
import time

from fastshield.request import BaseRequest
from fastshield.classifire.classifire import ThreatClassifier
from fastshield.utils import RateClientBucket
from fastshield.exceptions import HackBlockException, RateLimitException


class HackMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        dispatch=None,
        allow_signature: bool = True,
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

    def __classfy(self) -> BaseRequest:
        req = BaseRequest(
            origin=self.origin,
            host=self.host,
            request=self.cut_url,
            method=self.method,
            headers=self.headers,
            body=self.cut_url,
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
            self.cut_url = urllib.parse.unquote(
                self.url.replace(self.base_url, "")
            )
            self.headers = dict(request.headers)
            self.method = str(request.method)

            if self.allow_signature:
                ...

            classifyed_request = self.__classfy()
            if "valid" not in classifyed_request.threats:
                raise HackBlockException()

            response = await call_next(request)
            return response
        except Exception:
            response = await call_next(request)
            return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: FastAPI,
            dispatch=None,
            allow_ttl: int = 60,
            allow_max_reqlen: int = 50
    ):
        super().__init__(app, dispatch)
        self.allow_ttl = allow_ttl
        self.allow_max_reqlen = allow_max_reqlen

    async def dispatch(self, request: Request, call_next):
        ip_address = str(request.client.host)
        current_time = int(time.time())
        bucket = RateClientBucket()
        bucket.add_client(
            ip_address,
            current_time 
        )
        bucket.removed_expired_client(
            key=ip_address,
            ttl=self.allow_ttl
        )
        if len(bucket.client_bucket[ip_address]) >= self.allow_max_reqlen:
            return RateLimitException()

        response = await call_next(request)
        return response


class CountryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        return await super().dispatch(request, call_next)


class BotMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        return await super().dispatch(request, call_next)
