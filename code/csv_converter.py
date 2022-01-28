import csv

from typing import List 


def convert_csv_to_list_of_dicts(csv_file: str) -> List[dict]:
    with open(csv_file, 'r') as file:
        list_of_dicts = [{key: value for key, value in row.items()}
                          for row in csv.DictReader(file)]
    return list_of_dicts


def convert_list_of_dicts_to_csv(list_of_dicts: List[dict], csv_file_name: str):
    keys = list_of_dicts[0].keys()
    with open(csv_file_name, 'w', newline='') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)
