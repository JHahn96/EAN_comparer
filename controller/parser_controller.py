import os
import logging
from controller.csv_parser import ImportJtlCSV, ImportAmazonItemCSV
from controller.csv_writer import ConflictPartsCSVExporter


class Controller(object):
    DATA_FOLDER = "data"
    CUSTOMER_DATA_FILE_NAME = "JTL-export-sample-data.csv"
    ITEM_FILE_NAME = "Amazon-export-sample-data.csv"
    OUTPUT_FOLDER = "output"
    OUTPUT_FILE_NAME = "Parts-with-ean-error.csv"
    OUTPUT_FIELD_NAMES = ["PartNo", "JTL-EAN", "Amazon-EAN"]

    def __init__(self):
        self.data_jtl = dict()
        self.data_amazon = dict()
        self.articles_with_different_ean_conflict = []

    def start(self):
        self._load_files()
        self.compare()
        self.write_csv()

    def _load_files(self):
        self._load_customer_data()
        self._load_items()

    def _load_customer_data(self):
        csv_reader = ImportJtlCSV()
        csv_reader.import_csv(self._create_path(self.DATA_FOLDER, self.CUSTOMER_DATA_FILE_NAME))
        self.data_jtl = csv_reader.parse()

    def _load_items(self):
        csv_reader = ImportAmazonItemCSV()
        csv_reader.import_csv(self._create_path(self.DATA_FOLDER, self.ITEM_FILE_NAME))
        self.data_amazon = csv_reader.parse()

    def compare(self):
        conflicting_elements = []
        for part_no_amazon_article, ean_amazon in self.data_amazon.items():
            try:
                ean_jtl = self.data_jtl.get(part_no_amazon_article)

                if ean_jtl != ean_amazon:
                    conflicting_elements.append(
                        {self.OUTPUT_FIELD_NAMES[0]: part_no_amazon_article,
                         self.OUTPUT_FIELD_NAMES[1]: ean_jtl,
                         self.OUTPUT_FIELD_NAMES[2]: ean_amazon})
            except KeyError:
                pass
        self.articles_with_different_ean_conflict = conflicting_elements

    def write_csv(self):
        logging.debug("Start csv writing")
        csv_writer = ConflictPartsCSVExporter()
        file = self._create_path(self.OUTPUT_FOLDER, self.OUTPUT_FILE_NAME)
        csv_writer.write_dict_to_csv(file_name=file, rows=self.articles_with_different_ean_conflict,
                                     field_names=self.OUTPUT_FIELD_NAMES)

    @staticmethod
    def _create_path(folder, file_name):
        return os.path.join(os.path.dirname(os.path.abspath(folder)), folder, file_name)
