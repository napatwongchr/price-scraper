import scrapy
import csv
import urllib.parse
import re


class CassavaPriceSpider(scrapy.Spider):
    name = 'cassava_spider'
    start_urls = ['http://www.oae.go.th/view/1/%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%AA%E0%B8%B4%E0%B8%99%E0%B8%84%E0%B9%89%E0%B8%B2%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%A7%E0%B8%B1%E0%B8%99/%E0%B8%81.%E0%B8%84.63/34375/TH-TH']
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
        COMPANIES = ["A", "B"]

        csv_data.append([time_label])
        csv_data.append(COMPANIES)

        return csv_data

    def parse(self, response):
        click_month_link = response.css(
            '#content-A > div > div.post_desc > div > div:nth-child(3) > div:nth-child(1) > a')
        price_month_label = urllib.parse.unquote(response.url).split('/')[6]
        csv_data = self.prepare_csv(price_month_label)

        for table_row in response.css('#table_data > tbody > tr.xl65'):
            prices = table_row.css('td.xl98 ::text').getall()
            if (len(prices)):
                csv_data.append(prices)

        self.create_csv(csv_data=csv_data, time_label=price_month_label)

        unquoted_click_mouth_link = urllib.parse.unquote(
            click_month_link.attrib['href'])
        has_baseurl = re.search('http://www.oae.go.th',
                                unquoted_click_mouth_link)
        if (has_baseurl):
            next_url = f"{click_month_link.attrib['href']}"
        else:
            next_url = f"{self.base_url}{click_month_link.attrib['href']}"
        yield scrapy.Request(url=next_url, callback=self.parse)
