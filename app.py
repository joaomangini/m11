from flask import Flask, render_template, request
import scrapy
from scrapy.crawler import CrawlerProcess

app = Flask(__name__)

class MySpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['corinthians.com']  # Alterando o domínio para corinthians.com
    start_urls = []

    def parse(self, response):
        links = response.css('a::attr(href)').getall()

        for link in links:
            yield {
                'url': link,
                'content': response.css('::text').get()
            }

    def start_requests(self):
        # A URL inicial será definida na rota /scrape
        yield scrapy.Request(url=self.start_url, callback=self.parse)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        process = CrawlerProcess()
        process.crawl(MySpider, start_url=url)
        process.start()

        # Obtenha os resultados da spider e renderize-os na página
        results = process.crawlers[0].spider.results
        return render_template('index.html', results=results)

    return render_template('index.html', results=None)

if __name__ == '__main__':
    app.run(debug=True)
