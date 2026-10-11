
from http.client import HTTPException
from urllib.error import URLError

from src.downloader import download
from src.stats import calculate_stats
from src.display import print_header, print_result, print_summary

URL = "https://cachefly.cachefly.net/10mb.test"
COUNT = 10
TIMEOUT = 60

def main():
    results = []
    errors = 0

    print_header(URL, COUNT)

    for i in range(1, COUNT + 1):
        try:
            result = download(
                url=URL,
                timeout=TIMEOUT,
            )

            results.append(result)
            print_result(i, COUNT, result)

        except (URLError, OSError, HTTPException, ValueError) as error:
            errors += 1
            print(f"[{i:02}/{COUNT:02}] ERROR: {error}")

    if not results:
        print("\nВсе запросы завершились ошибкой")
        return 1

    summary = calculate_stats(results, errors)
    print_summary(summary)

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
