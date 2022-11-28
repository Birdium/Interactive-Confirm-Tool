import csv


class Input:

    @staticmethod
    def read(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            return [row for row in reader]
