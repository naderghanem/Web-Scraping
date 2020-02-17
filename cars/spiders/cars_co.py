# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.http import Request, FormRequest
from cars.items import CarsItem
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from bs4 import BeautifulSoup
import re


class CarsCoSpider(scrapy.Spider):
	name = 'carscoza-12-2019-4'
	allowed_domains = ['cars.co.za']
	start_urls = ["https://www.cars.co.za/searchVehicle.php?new_or_used=&make_model=&vfs_area=&agent_locality=&price_range=&os="]


	def parse(self, response):

		liste = response.xpath('//a[@class="vehicle-list__vehicle-name"]/@href').extract()
		for url in liste:
			url = 'https://www.cars.co.za' + url
			if url is not None:
				#print (url)
				yield scrapy.Request(url=url, callback=self.parse_detail)
		page_suiv1 = response.xpath('//*[@class="pagination__page pagination__nav js-pagination fa fa-right-open-big"]/@href').extract_first()
		page_suiv = 'https://www.cars.co.za' + page_suiv1
		if page_suiv is not None:
			print(("------------------------>",page_suiv))
			yield scrapy.Request(url=page_suiv,callback=self.parse)


	def parse_detail(self, response):


		soup = BeautifulSoup(str(response.text).encode("utf-8"), 'lxml')

		current_url = response.url
		item = CarsItem ()

		item ['ANNONCE_LINK'] = response.url
		item ['ID_CLIENT'] = soup.findAll('div',{'class':'box vehicledetails'})[0]['data-vehicle-id']
		try:
			item ['GARAGE_ID'] = str(response.xpath("//a[@class='vehicle-view__content-links vehicle-view__content-links_blue']/@href").get()).split("/")[-2]
		except:
			pass

		if len(response.xpath("//div[@class='lead-form__title']/text()").extract_first()) > 4:
			if "Private seller" in (response.xpath("//div[@class='lead-form__title']/text()").extract_first()):
				item ['TYPE'] = "private"
			else:
				item ['TYPE'] = "dealer"

		item['SITE'] = "http://www.cars.co.za/"
		item ['MARQUE'] = response.xpath("//div[@class='container js-breadcrumbs']/ul/li[3]/a/text()").extract_first()
		item ['MODELE'] = response.xpath("//div[@class='container js-breadcrumbs']/ul/li[4]/a/text()").extract_first().split()[1]
		item ['ANNEE'] = response.xpath("//tr[2][@class='vehicle-details__row']/td[2]/text()").extract_first()
		item ['NOM'] = str(response.xpath('//*[@class="heading heading_size_xl"]/text()').extract_first()).replace('\n', '')
		sel = r"googletag\.pubads\(\)\.setTargeting\(\"body_type\", \"(\w+)\"\)"
		item ['CARROSSERIE'] = response.xpath('//script[@type="text/javascript"]').re(sel)

		item ['OPTIONS'] = response.xpath('//td[@class="vehicle-details__value"]/text()').extract()[8].strip()
		item ['OPTIONS'] =item ['OPTIONS'].replace(";"," ")
		item ['OPTIONS'] =item ['OPTIONS'].replace(","," ")
		item ['OPTIONS'] =item ['OPTIONS'].replace("\t"," ")
		item ['OPTIONS'] =item ['OPTIONS'].replace("\n"," ")


		if len(item ['OPTIONS'])>200:
			item ['OPTIONS'] = item ['OPTIONS'][0:200]
		
		item ['CARBURANT'] = response.xpath("//tr[2][@class='vehicle-details__row']/td[4]/text()").extract_first().replace("\n", "").replace("\r", "")
		item ['PRIX'] = response.xpath("//div[@class='price price_view vehicle-view__price']/text()").extract_first().replace("R", "").replace("\n", "").replace("\xa0", "")
		item ['KM'] =  response.xpath("//tr[@class='vehicle-details__row']/td[2]/text()").extract_first().replace("\xa0", " ").replace("Km", "").rstrip()
		item ['PROVINCE'] = response.xpath("//tr[3][@class='vehicle-details__row']/td[4]/text()").extract_first()
		item ['COULEUR'] = response.xpath("//tr[4][@class='vehicle-details__row']/td[2]/text()").extract_first()
		item ['PHOTO'] = len(response.xpath("//a[@rel='gallery']/@href").extract())
		item ['GARAGE_NAME'] = response.xpath("//a[@class='vehicle-view__content-links vehicle-view__content-links_blue']/text()").extract_first()
		item ['BOITE'] = response.xpath("//tr[@class='vehicle-details__row']/td[4]/text()").extract_first().replace("\n", "").replace("\r", "")
		descrp = response.xpath("//div[@class='vehicle-view__content']/text()").getall()
		descrp = ' '.join(descrp)
		item ['EMAIL'] = get_emails(descrp)
		phones = re.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,10}[0-9]', descrp)
		item ['TELEPHONE_2'] = ""
		item ['TELEPHONE_3'] = ""
		item ['TELEPHONE_4'] = ""
		try:
			item ['TELEPHONE_2'] = phones[0]
			item ['TELEPHONE_3'] = phones[1]
			item ['TELEPHONE_4'] = phones[2]
		except:
			pass

		scripts = soup.findAll('script', attrs={'type':'text/javascript'})
		for script in scripts:
			if "var tracking_number_url" in script.text:
				url_dealer = script.text.replace("var tracking_number_url =","").split(';')[0].replace('"','').split()[0]
				url_phone_dealer = "https://www.cars.co.za" + str(url_dealer)

				#print(url_phone_dealer)
		
				yield Request(url_phone_dealer, meta={'item': item}, callback=self.parse_phone, dont_filter=True)

		yield item

	def parse_phone(self, response):

		item = response.meta['item']
		try:
			item ['TELEPHONE'] = response.xpath("//body//*/text()").extract_first()
		except:
			pass
		yield item

def get_emails(s):
    email = re.findall("[a-z0-9.\-]+@[a-z0-9.\-]+", s)
    email = " ".join(" ".join(email).split())
    return email
'''

	def parse(self, response):

		for i in range (1, 3845):
			url = "https://www.cars.co.za/searchVehicle.php?new_or_used=&make_model=&vfs_area=&agent_locality=&price_range=&os=&P=" + str(i)
			yield scrapy.Request(url, callback=self.parse_url)
'''
