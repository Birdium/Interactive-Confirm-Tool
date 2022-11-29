import os.path
import csv


class Output:

    def __init__(self, verified_pairs, output_dir):
        self.__output_dir__ = output_dir
        self.__verified_pairs__ = verified_pairs

    def write_csv(self):
        if not os.path.exists(self.__output_dir__):
            os.mkdir(self.__output_dir__)
        eq_csv_path = os.path.join(self.__output_dir__, "equal.csv")
        header = ['file1', 'file2']
        with open(eq_csv_path, "w", encoding='utf-8', newline='') as eq_csv:
            writer = csv.writer(eq_csv)
            writer.writerow(header)
            writer.writerows(self.__verified_pairs__)
