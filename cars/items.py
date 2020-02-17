# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarsItem(scrapy.Item):
	# define the fields for your item here like:
	

	ANNONCE_LINK = scrapy.Field()
	ID_CLIENT = scrapy.Field()
	GARAGE_ID = scrapy.Field()
	TYPE = scrapy.Field()
	SITE = scrapy.Field()
	MARQUE = scrapy.Field()
	MODELE = scrapy.Field()
	ANNEE = scrapy.Field()
	NOM = scrapy.Field()
	CARROSSERIE = scrapy.Field()
	OPTIONS = scrapy.Field()
	CARBURANT = scrapy.Field()
	BOITE = scrapy.Field()
	PRIX = scrapy.Field()
	KM = scrapy.Field()
	COULEUR = scrapy.Field()
	PHOTO = scrapy.Field()
	GARAGE_NAME = scrapy.Field()
	PROVINCE = scrapy.Field()
	TELEPHONE = scrapy.Field()
	TELEPHONE_2 = scrapy.Field()
	TELEPHONE_3 = scrapy.Field()
	TELEPHONE_4 = scrapy.Field()
	EMAIL = scrapy.Field()
	#descrep = scrapy.Field()
	pass
