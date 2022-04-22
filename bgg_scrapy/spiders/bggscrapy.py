from gc import callbacks
import scrapy
import w3lib

class BggscrapySpider(scrapy.Spider):
    name = 'bggscrapy'
    allowed_domains = ['boardgamegeek.com']
    start_urls = ['http://boardgamegeek.com/browse/boardgame']

    def parse(self, response):
        #collection_ranks = 1
        for tabel in response.css('tr#row_'):
            rank = tabel.xpath("//td[@class='collection_rank']/text()")[1].get()
            try:
                yield{
                    'rank' : w3lib.html.replace_escape_chars(rank),
                    'name' : tabel.css('a.primary::text').get(),
                    'description' : w3lib.html.replace_escape_chars(tabel.css('td.collection_objectname p.smallefont::text').get()),
                    'rating' : {
                        'geek_rating' : w3lib.html.replace_escape_chars(tabel.css('td.collection_bggrating::text')[0].get()),
                        'avg_rating' : w3lib.html.replace_escape_chars(tabel.css('td.collection_bggrating::text')[1].get()),
                        'num_voters' : w3lib.html.replace_escape_chars(tabel.css('td.collection_bggrating::text')[2].get())
                    },
                    'shop_link' : 'boardgamegeek.com' + tabel.css('td.collection_shop a::attr(href)').get(),
                    'link' : 'boardgamegeek.com' + tabel.css('a.primary::attr(href)').get()
                }
            except:
                yield{
                    'rank' : w3lib.html.replace_escape_chars(rank),
                    'name' : tabel.css('a.primary::text').get(),
                    'description' : "",
                    'rating' : {
                        'geek_rating' : w3lib.html.replace_escape_chars(tabel.css('td.collection_bggrating::text')[0].get()),
                        'avg_rating' : w3lib.html.replace_escape_chars(tabel.css('td.collection_bggrating::text')[1].get()),
                        'num_voters' : w3lib.html.replace_escape_chars(tabel.css('td.collection_bggrating::text')[2].get())
                    },
                    'shop_link' : 'boardgamegeek.com' + tabel.css('td.collection_shop a::attr(href)').get(),
                    'link' : 'boardgamegeek.com' + tabel.css('a.primary::attr(href)').get()
                }
        try:
            next_page = response.xpath("//p//a[contains(.,'Next')]").attrib['href']
            if next_page is not None:
                next = 'https://boardgamegeek.com' + next_page
                yield scrapy.Request(url=next, callback=self.parse)
        except:
            pass
            
