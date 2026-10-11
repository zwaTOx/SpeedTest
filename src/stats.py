
import math
import statistics
from dataclasses import dataclass

from src.downloader import DownloadResult


MB = 1_000_000


@dataclass(frozen=True)
class SpeedStats:
    success: int
    errors: int
    total_size: int
    total_time: float
    average_time: float
    median_time: float
    p95_time: float
    average_ttfb: float
    min_speed: float
    max_speed: float
    average_speed: float
    total_speed: float


def percentile(values: list[float], p: float) -> float:
    """Расчёт перцентиля методом ближайшего ранга."""
    values = sorted(values)
    index = max(0, math.ceil(len(values) * p / 100) - 1)

    return values[index]


def calculate_stats(
    results: list[DownloadResult],
    errors: int
) -> SpeedStats:

    if not results:
        raise ValueError("Нет успешных запросов")

    durations = [r.duration for r in results]
    speeds = [r.speed for r in results]
    ttfbs = [r.ttfb for r in results]

    total_size = sum(r.size for r in results)
    total_time = sum(durations)

    # Скорость = суммарные байты / время всех загрузок
    total_speed = total_size / MB / total_time

    return SpeedStats(
        success=len(results),
        errors=errors,
        total_size=total_size,
        total_time=total_time,
        average_time=statistics.mean(durations),
        median_time=statistics.median(durations),
        p95_time=percentile(durations, 95),
        average_ttfb=statistics.mean(ttfbs),
        min_speed=min(speeds),
        max_speed=max(speeds),
        average_speed=statistics.mean(speeds),
        total_speed=total_speed,
    )
