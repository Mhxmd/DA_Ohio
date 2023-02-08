
# 1st version before testing and extraction of JPG images
'''

import scrapy
import json

class WebsiteMapperSpider(scrapy.Spider):
    name = "website_mapper"
    start_urls = [
        'http://172.18.58.80/freebix/',
    ]

    def parse(self, response):
        # Display the reference webpage
        print("Reference webpage: ", response.url)

        # Store the retrieved information in JSON
        data = {}
        data['title'] = response.css('title::text').get()
        data['header'] = response.headers
        with open('mapped_data.json', 'w') as outfile:
            json.dump(data, outfile)

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    })
    process.crawl(WebsiteMapperSpider)
    process.start()
'''
# 2nd Modified and Refined Version

import scrapy
import json


class WebsiteImageSpider(scrapy.Spider):
    name = "website_image"
    start_urls = [
        'http://172.18.58.80/freebix/',
    ]
    image_urls = []

    def parse(self, response):
        for next_page in response.css('a::attr(href)').getall():
            if next_page is not None:
                yield response.follow(next_page, self.parse)

        for img in response.css('img::attr(src)').getall():
            if img.endswith('.jpg'):
                self.image_urls.append(response.urljoin(img))

    def closed(self, reason):
        with open('image_links.json', 'w') as outfile:
            json.dump(self.image_urls, outfile)


def test_image_urls():
    with open('image_links.json', 'r') as infile:
        image_urls = json.load(infile)
    assert len(image_urls) > 0, "No image URLs found"
    for url in image_urls:
        assert url.endswith('.jpg'), f"Expected a JPG image, got {url}"


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    })
    process.crawl(WebsiteImageSpider)
    process.start()
    test_image_urls()