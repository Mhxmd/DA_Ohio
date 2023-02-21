
# Lab 10b

# Use the Request library
import requests

# Set the target webpage
url = 'http://172.18.58.80/freebix/'


# Perform a GET request on the target website
webpage = requests.get(url)
# This will print the full webpage in text
print(webpage.text)


# Display an "OK" return status code
print("Status code:")
print("\t *", webpage.status_code)


# Display the website header
h = requests.head(url)
print("Header:")
print("**********")
# To print line by line
for x in h.headers:
    print("\t ", x, ":", h.headers[x])
print("**********")


# Modify the Header user-agent to display "iPhone 14"
headers = {'User-Agent': 'iPhone 14'}
# Test against test site that output the requester user-agent
#url2 = 'http://httpbin.org/headers'
url2 = 'http://172.18.58.80/headers.php'
request_header = requests.get(url2, headers=headers)
print(request_header.text)

# Lab 10c

# Use the Scrapy library
import scrapy


class NewSpider(scrapy.Spider):
    name = "new_spider"
    start_urls = ['http://172.18.58.80/freebix/']

    def parse(self, response):
        css_selector = 'img'
        for x in response.css(css_selector):
            newsel = '@src'
            yield {'Image Link': x.xpath(newsel).extract_first(), }

        # To recurse next page
        page_selector = '.next a ::attr(href)'
        next_page = response.css(page_selector).extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

# Test scrapytest.py
#   Terminal: scrapy runspider scrapytest.py
# Save the output to a file results.json
#   Terminal: scrapy runspider scrapytest.py -o results.json -t json



# Lab 8
# Demonstrate unit-testing

import unittest
import requests


url = "http://172.18.58.80/freebix/"


# Each test class must be a subclass of unittest.TestCase
# The class should be named as TestXXXX to indicate to the program that it is a test program
class TestMyProgram(unittest.TestCase):

    # All methods should be named as test_XXXX to indicate that it is a test case

    # Checking whether the url is responding to requests
    def test_TestUrl(self):
        try:
            resp = requests.get(url)
            if int(resp.status_code) == 200:
                print("[TestUrl] URL OK")
            else:
                print("[TestUrl] Requested URL not found")
        except Exception as e:
            print("[TestUrl] Error: ", {e})

    def test_TestCase_2(self):
        print("[TestCase_2] Test case 2")


# Must invoke the unittest.main() methods
if __name__ == '__main__':
    unittest.main()
