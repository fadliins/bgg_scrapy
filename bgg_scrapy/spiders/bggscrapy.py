import scrapy
import w3lib
from bgg_scrapy.items import BggScrapyItem

class BggscrapySpider(scrapy.Spider):
    name = 'bggscrapy'
    allowed_domains = ['boardgamegeek.com']
    start_urls = ['http://boardgamegeek.com/browse/boardgame']

    def parse(self, response):
        #collection_ranks = 1
        item = BggScrapyItem()
        for tabel in response.xpath("//tr[contains(@id, 'row_')]"):
            rank = tabel.xpath(".//td[contains(@class, 'collection_rank')]").get()
            rank = w3lib.html.remove_tags(rank)
            try:
                item['rank'] = w3lib.html.replace_escape_chars(rank)
                item['name'] = tabel.xpath(".//a[contains(@class, 'primary')]/text()").get()
                item['description'] = w3lib.html.replace_escape_chars(tabel.xpath(".//td[contains(@class, 'collection_objectname')]//p[contains(@class, 'smallefont')]/text()").get())
                item['rating'] = {
                    'geek_rating' : w3lib.html.replace_escape_chars(tabel.xpath(".//td[contains(@class, 'collection_bggrating')]/text()")[0].get()),
                    'avg_rating' : w3lib.html.replace_escape_chars(tabel.xpath(".//td[contains(@class, 'collection_bggrating')]/text()")[1].get()),
                    'num_voters' : w3lib.html.replace_escape_chars(tabel.xpath(".//td[contains(@class, 'collection_bggrating')]/text()")[2].get())
                }
                item['shop_link'] = 'boardgamegeek.com' + tabel.xpath(".//td[contains(@class, 'collection_shop')]//a/@href").get()
                item['link'] = 'boardgamegeek.com' + tabel.xpath(".//a[contains(@class, 'primary')]/@href").get()
                yield item
            except:
                item['rank'] = w3lib.html.replace_escape_chars(rank)
                item['name'] = tabel.xpath(".//a[contains(@class, 'primary')]/text()").get()
                item['description'] = ""
                item['rating'] = {
                    'geek_rating' : w3lib.html.replace_escape_chars(tabel.xpath(".//td[contains(@class, 'collection_bggrating')]/text()")[0].get()),
                    'avg_rating' : w3lib.html.replace_escape_chars(tabel.xpath(".//td[contains(@class, 'collection_bggrating')]/text()")[1].get()),
                    'num_voters' : w3lib.html.replace_escape_chars(tabel.xpath(".//td[contains(@class, 'collection_bggrating')]/text()")[2].get())
                }
                item['shop_link'] = 'boardgamegeek.com' + tabel.xpath(".//td[contains(@class, 'collection_shop')]//a/@href").get()
                item['link'] = 'boardgamegeek.com' + tabel.xpath(".//a[contains(@class, 'primary')]/@href").get()
                yield item
        
        try:
            next_page = response.xpath("//p//a[contains(.,'Next')]/@href").get()
            if next_page is not None:
                next = 'https://boardgamegeek.com' + next_page
                yield scrapy.Request(url=next, callback=self.parse)
        except:
            pass
            
