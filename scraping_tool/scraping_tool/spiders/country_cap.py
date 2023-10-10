import scrapy
import os
from os.path import dirname
import csv

current_dir = os.path.dirname(__file__)
url = os.path.join(current_dir, 'toptv.html')

"""
terminal: 

table = response.xpath('//div[@class="col-md-4 country"]')
for row in table.xpath('h3//text()'):
    print(row.extract())

table = response.xpath('//div[@class="country-info"]')
for row in table.xpath('//span[@class="country-capital"]'):
    print(row.xpath('text()').extract())


"""


class CountryCapSpider(scrapy.Spider):
    name = "country_cap"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/simple/"]
    #start_urls = [f"file://{url}"]  #Esto es para que use el archivo html descargado en vez de conectarse a la página cada vez


    def parse(self, response):

        count = 0
        country_names = []
        country_capitals = []
        csv_file =open('countryCap.csv', 'w')  # Create a csv file
        writer = csv.writer(csv_file)               # Writer to be able to write on it
        writer.writerow(['country id', 'name', 'capital'])   # The headers of the csv file

        table_1 = response.xpath('//div[@class="col-md-4 country"]')

        for row in table_1.xpath('h3//text()'):
            try:
                country_name = row.extract()
                if count%2 != 0:
                    country_name = country_name.replace(" ", "")
                    country_name = country_name.replace("\n", "")
                    country_names.append(country_name)
                count += 1
            except IndexError:
                pass
        
        count = 0
        table_2 = response.xpath('//div[@class="country-info"]')

        for row in table_2.xpath('//span[@class="country-capital"]'):
            if count == len(country_names):
                break
            cap_c = row.xpath('text()').extract()
            country_capitals.append(cap_c[0])
            count += 1

        for i in range(len(country_names)):
            writer.writerow([i, country_names[i], country_capitals[i]])   # Writes the data from html to csv
        
        csv_file.close() 

