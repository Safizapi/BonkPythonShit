import json
import datetime
from typing import Union


def db_id_to_date(db_id: int) -> Union[datetime.datetime, str]:
    with open("dbids.json") as file:
        db_ids = json.load(file)
        index = 0

    while index < len(db_ids) and db_ids[index]["number"] < db_id:
        index += 1

    if index == 0:
        return f"Before {db_ids[0]['date']}"
    elif index == len(db_ids):
        return f"After {db_ids[-1]['date']}"

    first_number = db_ids[index - 1]["number"]
    second_number = db_ids[index]["number"]

    first_date = db_ids[index - 1]["date"]
    second_date = db_ids[index]["date"]
    first_timestamp = datetime.datetime.strptime(first_date, "%Y-%m-%d").timestamp()
    second_timestamp = datetime.datetime.strptime(second_date, "%Y-%m-%d").timestamp()

    diff = (db_id - first_number) / (second_number - first_number)
    time = first_timestamp + diff * (second_timestamp - first_timestamp)

    return datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
