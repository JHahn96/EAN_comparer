import csv
from abc import ABC, abstractmethod


class ImportCSV(ABC):

    def __init__(self):
        self.rows = []

    def import_csv(self, file_name):
        with open(file_name, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for row in csv_reader:
                self.rows.append(row)

    @abstractmethod
    def parse(self):
        """Method that should parse the file"""


class ImportJtlCSV(ImportCSV):

    def __init__(self):
        super(ImportJtlCSV, self).__init__()
        self.articles = dict()

    def parse(self):
        for index, row in enumerate(self.rows):
            if index != 0:
                self.articles.setdefault(row[0], row[1])
        return self.articles


class ImportAmazonItemCSV(ImportCSV):

    def __init__(self):
        super(ImportAmazonItemCSV, self).__init__()
        self.items = dict()

    def parse(self):
        for index, row in enumerate(self.rows):
            row = row[0].split(",")
            if index != 0:
                self.items.setdefault(row[0], row[2])
        return self.items

