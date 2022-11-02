import pandas as pd
from tabulate import tabulate


def load_data(path):
    date_parser = lambda x: pd.to_datetime(x, format=r"%Y-%m-%d %H:%M:%S")
    timestamp_cols = ["tgdat", "tgden", "tgdi", "tgbdau", "tgkthuc"]
    
    data = pd.read_csv(path).to_dict("records")
    for datum in data:
        for k, v in datum.items():
            if k in timestamp_cols:
                datum[k] = date_parser(v)
    return data


def print_table(data, schema):
    df = pd.DataFrame(data, columns=schema)
    print(tabulate(df, tablefmt='grid', headers=schema))