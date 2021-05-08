import scrapy



from ..indexer import UnhscrapeIndex



class PostsSpider(scrapy.Spider):



    name = "posts"



    start_urls = [

        'https://www.newhaven.edu/search/?cx=007701188165887638683%3A9z5n0yvnab4&cof=FORID%3A11&ie=UTF-8&q=*&search-term='

    ]





    def parse(self, response):

        page = response.url.split('/')[-1]

        filename = 'posts-%s.html' % page

        with open(filename, 'wb') as f:

            f.write(response.body)



    

    def parse(self, response):



        index = UhcscrapeIndex()



        for post in response.css('a.gs-title::atrr(href)'):

            title = post.css('.gs-title::text').get()

            section = post.css('.gs-snippet::text').get()



            index['title'] = title

            index['section'] = section



            yield index





            yield {

                'title' : title,

                'section' : section,

                'intro': post.css('.gsc-webResults gsc-result a::text')[2].get()

            }

        next_page = response.css('a.gsc-cursor-page::attr(href)').get()

        if next_page is not None:

            next_page = response.urljoin(next_page)

            yield scrapy.Request(next_page, callback=self.parse)







# To store the data in json

# type in terminal  "scrapy crawl posts -o items.json"



import json



search = input('Find:')



with open('items.json') as f:

    data = json.load(f)

    for search in data:

        value = data.get(search)

        

        if search == value:

            print(value)

        else:

            print("Not found")



            
