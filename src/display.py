from src.downloader import DownloadResult
from src.stats import SpeedStats

MB = 1_000_000
LINE = "=" * 60


def print_header(url: str, count: int):
    print(f"\n{LINE}")
    print("             INTERNET SPEED TEST")
    print(LINE)
    print(f"URL: {url}")
    print(f"Количество запросов: {count}")
    print(LINE)


def print_result(
    index: int,
    count: int,
    result: DownloadResult
):
    print(
        f"[{index:02}/{count:02}] OK | "
        f"{result.size / MB:6.3f} MB | "
        f"{result.duration:6.3f} sec | "
        f"{result.speed:6.3f} MB/s | "
    )


def print_summary(stats: SpeedStats):
    print(f"\n{LINE}")
    print("                  RESULTS")
    print(LINE)

    print(f"Успешных запросов:     {stats.success}")
    print(f"Ошибок:                {stats.errors}")
    print(f"Всего скачано:         {stats.total_size / MB:.2f} MB")
    print(f"Общее время:           {stats.total_time:.3f} sec")

    print("-" * 60)

    print(f"Среднее время:         {stats.average_time:.3f} sec")
    print(f"Медиана времени:       {stats.median_time:.3f} sec")
    print(f"P95 времени:           {stats.p95_time:.3f} sec")

    print("-" * 60)

    print(f"Минимальная скорость:  {stats.min_speed:.2f} MB/s")
    print(f"Максимальная скорость: {stats.max_speed:.2f} MB/s")
    print(f"Средняя скорость:      {stats.average_speed:.2f} MB/s")

    print(LINE)
    print(f"ИТОГОВАЯ СКОРОСТЬ:      {stats.total_speed:.2f} MB/s")
    print(f"В МЕГАБИТАХ:           {stats.total_speed * 8:.2f} Mbps")
    print(LINE)
