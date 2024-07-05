from datetime import datetime

from constants import BET_HISTORY_FILE_PREFIX
from csv_utils import read_csv
from path_anchor import OUTPUT_FOLDER


def start_date_from_week_window(num_weeks):
    pass


rows = read_csv(OUTPUT_FOLDER + "/" + BET_HISTORY_FILE_PREFIX + "_ryan_murphy.csv")
time = datetime.strptime(rows[0].get("time"), "%Y-%m-%dT%H:%M:%SZ")
print(type(time))
print(time)
