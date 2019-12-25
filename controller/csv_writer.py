import csv
import logging
from abc import ABC, abstractmethod


class WriteCSV(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def write_dict_to_csv(self, file_name, rows, field_names):
        """Method that should write to file"""


class ConflictPartsCSVExporter(WriteCSV):

    def __init__(self):
        super().__init__()

    def write_dict_to_csv(self, file_name, rows, field_names):

        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
            csv_writer.writeheader()
            for row in rows:
                try:
                    csv_writer.writerow(row)
                except ValueError:
                    logging.warning("Error during csv-writing row {}".format(row))
