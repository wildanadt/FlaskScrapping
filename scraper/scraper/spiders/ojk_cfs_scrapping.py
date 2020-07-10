import scrapy
from flask import jsonify

class OjkCFS_Spider(scrapy.Spider):
    name = "ojk_cfs_post"
    req_form_data = {}
    req_headers = {}


    def __init__(self, req_head = '', req_form= '', **kwargs):
         self.req_form_data = req_form
         self.req_headers = req_head
        #  super().__init__(**kwargs)
        #  self.start_urls = 'https://cfs.ojk.go.id/cfs'

    def start_requests(self):
        # print(self.req_headers)
        # print(self.req_form_data)
        print('oi')
        yield scrapy.FormRequest(url='https://cfs.ojk.go.id/cfs', formdata=self.req_form_data, method='POST', headers=self.req_headers)

    def parse(self, response):
        # print(response.text)
        yield MyItem(resp= response.text)
        

    custom_settings = {'CLOSESPIDER_TIMEOUT' : 15}


class MyItem(scrapy.Item):
    resp = scrapy.Field()