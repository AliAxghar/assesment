import csv
from .data import Data


def fetch_raw_data_from_csv(csv_file):
    raw_data = []
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row["email"]
            referral = row["referral_email"]
            raw_data.append(Data(email, referral))
    return raw_data
