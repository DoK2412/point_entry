import httpx

from settings import URL_REGISTRATION_SERVISE, URL_SESSION_SERVISE, URL_DATA_SERVISE

timeout = httpx.Timeout(60.0)


class RegistrationServise(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            base_url=URL_REGISTRATION_SERVISE,
            verify=False,
            timeout=timeout,
            **kwargs,
        )


class SessionServise(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            base_url=URL_SESSION_SERVISE,
            verify=False,
            timeout=timeout,
            **kwargs
        )

class DataServise(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            base_url=URL_DATA_SERVISE,
            verify=False,
            timeout=timeout,
            **kwargs
        )