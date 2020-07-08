import scrapy
import csv
import urllib.parse
import re


class CassavaPriceSingleSpider(scrapy.Spider):
    name = 'cassava_single_spider'
    start_urls = ['http://www.oae.go.th/view/1/%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%AA%E0%B8%B4%E0%B8%99%E0%B8%84%E0%B9%89%E0%B8%B2%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%A7%E0%B8%B1%E0%B8%99/%E0%B8%81.%E0%B8%84.61/28574/TH-TH']
    base_url = 'http://www.oae.go.th'

    def create_csv(self, csv_data, time_label):
        csv.register_dialect('my_dialect', delimiter=',',
                             quoting=csv.QUOTE_NONE)
        csv_file = open(f"./data/cassava_price_{time_label}.csv", 'w')
        with csv_file:
            writer = csv.writer(
                csv_file, dialect='my_dialect', escapechar='\\')
            writer.writerows(csv_data)

    def prepare_csv(self, time_label):
        csv_data = []
        COMPANIES = ["A", "B", "C", "D"]

        csv_data.append([time_label])
        csv_data.append(COMPANIES)

        return csv_data

    def parse(self, response):
        price_month_label = urllib.parse.unquote(response.url).split('/')[6]
        csv_data = self.prepare_csv(price_month_label)

        for table_row in response.css('#table_data > tbody > tr.xl65'):
            prices = table_row.css('td.xl98 > div ::text').getall()
            if (len(prices)):
                csv_data.append(prices)

        self.create_csv(csv_data=csv_data, time_label=price_month_label)


# Patterns
# 1. no div, in td
# 2. has div, in td
# 3. no class
