import time


class RateClinetBaseSingle(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class RateClientBucket(RateClinetBaseSingle):
    def __init__(self) -> None:
        # Проверяем, была ли уже инициализация
        if not hasattr(self, "_initialized"):
            self.__client_bucket: dict[str, list[int | float]] = {}
            # Флаг, чтобы избежать повторной инициализации
            self._initialized = True

    @property
    def client_bucket(self) -> dict:
        return self.__client_bucket

    @client_bucket.setter
    def client_bucket(self, value: dict) -> None:
        if not isinstance(value, dict):
            raise ValueError("client_bucket должен быть словарем (dict).")
        self.__client_bucket = value

    def add_client(self, ip_address: str, value: int | float) -> None:
        if ip_address not in self.__client_bucket:
            self.__client_bucket[ip_address] = []
        self.__client_bucket[ip_address].append(value)

    def removed_expired_client(self, ip_address: str, ttl: int) -> None:
        current_time = int(time.time())

        if ip_address in self.__client_bucket:
            self.__client_bucket[ip_address] = list(
                filter(
                    lambda client_time: current_time - client_time < ttl,
                    self.__client_bucket[ip_address],
                )
            )
            return self.__client_bucket[ip_address]


class BlackBaseSingle(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class BlackListBucket(BlackBaseSingle):
    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self.__black_list_bucket: dict[str, list[int]] = {}
            self.__hard_list_bucket: dict[str:int] = {}
            self._initialized = True

    @property
    def black_list_bucket(self) -> dict[str, list[int]]:
        return self.__black_list_bucket

    @property
    def hard_list_bucket(self) -> dict[str, int]:
        return self.__black_list_bucket

    def add_client_black_list(self, ip_address: str):
        current_time: int = int(time.time())

        if ip_address not in self.__black_list_bucket:
            self.__black_list_bucket[ip_address] = []
        self.__black_list_bucket[ip_address].append(current_time)

    def removed_expired_warnings(
        self, ip_address: str, ttl: int
    ) -> None:
        current_time: int = int(time.time())

        if ip_address in self.__black_list_bucket:
            self.__black_list_bucket[ip_address] = list(
                filter(
                    lambda client_time: current_time - client_time < ttl,
                    self.__black_list_bucket[ip_address],
                )
            )
            return self.__black_list_bucket[ip_address]

    def add_client_hard_block(self, ip_address: str, expire: int = 420):
        current_time: int = int(time.time())
        hard_block_expire: int = current_time + expire

        self.__hard_list_bucket[ip_address] = hard_block_expire

    def hard_block_query(self, ip_address: str) -> bool:
        if ip_address not in self.__hard_list_bucket:
            return False

        current_time = int(time.time())
        client_expire = self.__hard_list_bucket[ip_address]

        if current_time > client_expire:
            return False
        return True
