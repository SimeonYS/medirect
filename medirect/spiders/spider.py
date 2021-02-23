import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import MedirectItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class MedirectSpider(scrapy.Spider):
	name = 'medirect'
	start_urls = ['https://www.medirect.be/nl-be/nieuws-research/nieuws-dossiers/all-news']

	def parse(self, response):
		category = response.xpath('//a[@class="_2vaL8Fl8zO"]/@href').getall()
		yield from response.follow_all(category, self.parse_links)
	def parse_links(self, response):
		links = response.xpath('//a[@class="uyWe0RjGLq _3_7Kx6vUwP"]/@href').getall()
		yield from response.follow_all(links, self.parse_post)

	def parse_post(self, response):

		date = response.xpath('//div[@class="_1Dkin6kVrK"]//text()').get()
		title = response.xpath('//div[@class="_1NBhnuUStO"]/h1//text()').get()
		content = response.xpath('//div[@class="_2GNKU4NLmi"]//text()').getall()[1:]
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=MedirectItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
