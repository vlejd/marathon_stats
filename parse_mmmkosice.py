from constants import *
import glob
from loguru import logger
import os
import pandas as pd


def load_mmmkosice_as_df(files):
    dfs = []
    for file in files:

        year = int(os.path.basename(file).split(".")[0])

        df = pd.read_html(file, match="Priezvisko")
        assert len(df) == 2

        df[0]["Rocnik"] = year
        df[0]["Gender"] = "M"
        df[1]["Rocnik"] = year
        df[1]["Gender"] = "F"

        dfs.append(df[0])
        dfs.append(df[1])
    dfs = pd.concat(dfs)
    return dfs


def parse_time(time_str):
    if time_str != time_str or time_str in ["?", "DNF", "DNS"]:
        return float("nan")
    parts = time_str.split(":")
    assert len(parts) == 3, str(parts)
    h = parts[0]
    m = parts[1]
    s = parts[2]
    return int(h) * 60 * 60 + int(m) * 60 + float(s.replace(",", "."))


def clean_df(df):
    # standing, start_number, surname, first_name, birth_year, club, state, finish_time, half_time, race_year, gender.
    # DNF
    clean = pd.DataFrame()
    mapping = [
        ("standing", "Poradie"),
        ("start_number", "Št. číslo"),
        ("surname", "Priezvisko"),
        ("first_name", "Meno"),
        ("birth_year", "Rok nar."),
        ("club", "Klub"),
        ("state", "Štát"),
        ("race_year", "Rocnik"),
        ("gender", "Gender"),
    ]
    for target_name, source_name in mapping:
        clean[target_name] = df[source_name]

    clean["dnf"] = df["Cieľ. čas"] == "DNF"

    clean["finish_time_s"] = df["Cieľ. čas"].apply(parse_time)
    clean["mid_time_s"] = df["Medzičas"].apply(parse_time)

    return clean


def main():
    storage_path = os.path.join(MMMKOSICE_STORAGE_PATH, HTML_PATH)
    result_files = sorted(glob.glob(os.path.join(storage_path, "*")))
    logger.info("Loading")
    df = load_mmmkosice_as_df(result_files)
    logger.info("Cleaning")
    clean = clean_df(df)
    logger.info("Saving")
    clean_path = os.path.join(MMMKOSICE_STORAGE_PATH, PARSED)
    clean.to_csv(clean_path, index=False)


if __name__ == "__main__":
    main()
