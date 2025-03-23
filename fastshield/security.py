from functools import wraps
from fastapi import Request
import time

from fastshield.utils import RateClientBucket, BlackListBucket
from fastshield.exceptions import RateLimitException, HardBlockException


class Secure:
    def __init__(
        self,
        hardblock_expire_seconds: int = 60,
        warning_steps: int = 10,
        block_ttl: int = 60
    ):
        self.block_ttl = 60
        self.hardblock_expire_seconds: int = hardblock_expire_seconds
        self.warning_steps = warning_steps

    def machine_protect(
        self
    ):
        ...

    def duble_protect(
        self,
    ): ...

    def singnature_protect(self): ...

    def rate_limit_protect(
        self,
        ttl: int,
        max_reqlen: int
    ):
        def inner_decorator(endpoint):
            @wraps(endpoint)
            async def wrapper(request: Request, *args, **kwargs):
                ip_address = str(request.client.host)
                block_bucket = BlackListBucket()

                if block_bucket.hard_block_query(ip_address):
                    raise HardBlockException()

                current_time = int(time.time())
                bucket = RateClientBucket()

                bucket.add_client(ip_address, current_time)
                bucket.removed_expired_client(
                    key=ip_address, ttl=ttl, current_time=current_time
                )

                if len(bucket.client_bucket[ip_address]) >= max_reqlen:
                    block_bucket.add_client_black_list(
                        ip_address,
                    )

                    block_bucket.removed_expired_warnings(
                        ip_address,
                        self.block_ttl
                    )

                    if len(block_bucket.black_list_bucket) >= self.warning_steps:
                        block_bucket.add_client_hard_block(
                            ip_address,
                            self.hardblock_expire_seconds
                        )
                    raise RateLimitException()

                return endpoint(request, *args, **kwargs)

            return wrapper

        return inner_decorator

    def country_protect(
        self,
    ): ...


secure = Secure()
