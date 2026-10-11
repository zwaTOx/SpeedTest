
import time
import uuid
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen


CHUNK_SIZE = 256 * 1024
MB = 1_000_000


@dataclass(frozen=True)
class DownloadResult:
    size: int
    duration: float
    ttfb: float

    @property
    def speed(self) -> float:
        return self.size / MB / self.duration


def add_cache_buster(url: str) -> str:
    """Добавляет уникальный параметр к URL."""
    parts = urlsplit(url)

    query = parts.query
    query += ("&" if query else "") + f"_cb={uuid.uuid4().hex}"

    return urlunsplit(parts._replace(query=query))


def download(
    url: str,
    timeout: float = 60,
) -> DownloadResult:
    '''Выполняет один запрос и полностью читает ответ.'''

    request = Request(
        url,
        headers={
            "User-Agent": "InternetSpeedTester/1.0",
            "Cache-Control": "no-cache, no-store",
            "Pragma": "no-cache",
            "Accept-Encoding": "identity",
        }
    )

    start = time.perf_counter()

    with urlopen(request, timeout=timeout) as response:
        first_byte = response.read(1)
        ttfb = time.perf_counter() - start

        if not first_byte:
            raise ValueError("Сервер вернул пустой ответ")

        total_size = len(first_byte)

        while True:
            chunk = response.read(CHUNK_SIZE)

            if not chunk:
                break

            total_size += len(chunk)

        duration = time.perf_counter() - start

        expected = response.headers.get("Content-Length")

        if expected is not None:
            if total_size != int(expected):
                raise ValueError(
                    f"Неполная загрузка: {total_size}/{expected}"
                )

    return DownloadResult(
        size=total_size,
        duration=duration,
        ttfb=ttfb
    )
