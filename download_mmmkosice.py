import datetime
from loguru import logger
import os
import requests
from constants import *
import time


def main():
    current_year = datetime.datetime.today().year
    logger.info(f"Current year:", current_year)
    storage_path = os.path.join(MMMKOSICE_STORAGE_PATH, HTML_PATH)
    os.makedirs(storage_path, exist_ok=True)

    FIRST_YEAR = 1924
    for year in range(FIRST_YEAR, current_year + 1):
        saved_file = os.path.join(storage_path, f"{year}.html")
        if os.path.exists(saved_file):
            continue
        url = "https://www.kosicemarathon.com/prehlad-vysledkov/"
        r = requests.post(
            url, data={"search": "vysledky", "rok": year, "discipline": 1}
        )
        str_check = "Neboli nájdené žiadne výsledky"

        if str_check in r.text:
            logger.warning(f"Looks like there are no data for year: {year}")
            break
        else:
            with open(saved_file, "w") as f:
                f.write(r.text)

            logger.info(f"Done: {year}")
        time.sleep(1)


if __name__ == "__main__":
    main()
