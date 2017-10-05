# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.crawler import CrawlerProcess
import urlparse
import platform
import base64

user_name = raw_input("Please enter your usermame: ")
test_password = raw_input("Please enter your password: ")

'''
user_path = ""
try:
    user_path = os.environ['USERPROFILE']
except KeyError:
    user_path = os.environ['HOMEPATH']
'''

def encode_first(s):
    return base64.b64encode(s)

def encode_second(s):
    result = str(s[0])
    i = 1
    while i < len(s):
        result += '\x00' + s[i]
        i += 1
    result += '\x00'
    return base64.b64encode(result)

class VitalItem(scrapy.Item):
    course = scrapy.Field()
    link = scrapy.Field()	

class VitalSpider(scrapy.Spider):
    base_url = "https://vital.liv.ac.uk"
    name = "vital"
    allowed_domains = ["vital.liv.ac.uk"]
    headers = {
        "Host": "vital.liv.ac.uk",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
        "Referer": "https://vital.liv.ac.uk/",
        "Upgrade-Insecure-Requests": "1"
    }

    start_urls = ['https://vital.liv.ac.uk/webapps/login/']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            url="https://vital.liv.ac.uk/webapps/login/",
            formdata={
            'user_id':user_name,
            'login':'Login',
            'action':'login',
            'encoded_pw':encode_first(test_password),
            'encoded_pw_unicode':encode_second(test_password)
            },
            callback=self.real_parse
        )

    def real_parse(self, response):
        if response.url == 'https://vital.liv.ac.uk/webapps/login/':
            print "\nAuthentication failed."
        else:
			print "\nAuthentication succeeded."
			#basic_address = user_path+'\Dropbox\Test'
			print 'Please enter the absolute address at which you want to store your files.'
			#print "For example, '", example, "'"
			basic_address = raw_input('Your address: ')
			if (not (os.path.exists(basic_address))):
				os.makedirs(basic_address)
			print "Files will be stored at " + basic_address + '\n'
			count = 1;
			course_list = []
			name_list = []ID')):
					print("["+str(count)+"] " + name)
					count = count + 1
					name_list.append(name)
					course_list.append(self.base_url + sel.xpath('a/@href').extract()[0].strip())
			print "Separate your choices with one space: "
			user_choice = raw_input()
			for i in user_choice.split(' '):
				choice = int(i.strip())
				the_name = name_list[choice-1].split('-')[1].strip()
				the_path = course_list[choice-1]
				if (not (os.path.exists(basic_address + '/' + the_name))):
					os.makedirs(basic_address + '/' + the_name)
				request = scrapy.Request(the_path, callback=self.link_parse)
				request.meta['father_name'] = the_name
				request.meta['basic_address'] = basic_address
				yield request
    
    def link_parse(self, response):
        father = response.meta['father_name']
        basic_address = response.meta['basic_address']
        for sel in response.xpath('//li[@class ="clearfix "]'):
            address_list = sel.xpath('a/@href').extract()
            folder_list = sel.xpath('a/span/@title').extract()
            exist_before = True
            if (len(address_list) != 0 and len(folder_list) != 0):
                if (not (os.path.exists(basic_address + '/' + father + '/'+folder_list[0]) or (folder_list[0]=="What's New"))):
                    os.makedirs(basic_address + '/' + father + '/'+folder_list[0])
                    exist_before = False
                request =  scrapy.Request(self.base_url + address_list[0], callback = self.find_parse)
                request.meta['father'] = basic_address + '/' + father + '/'+ folder_list[0]
                request.meta['exist_before'] = exist_before
                yield request

    def find_parse(self, response):
        count = 0
        for sel in response.xpath('//a'):
            list = sel.xpath('@href').extract()
            names = sel.xpath('span/text()').extract()
            if ((len(names)!=0) and (len(list) != 0) and (list[0].startswith("/bbcs"))):
                item = VitalItem()
                item['course'] = names[0]
                request =  scrapy.Request(self.base_url + list[0], callback = self.save_pdf)
                request.meta['item'] = item
                request.meta['father'] = response.meta['father']
                count += 1
                yield request
        if (count == 0 and response.meta['exist_before'] == False):
            os.rmdir(response.meta['father'])

    def save_pdf(self, response):
        save_path = os.path.join(response.meta['father'],response.url.split('/')[-1])
        if (not os.path.exists(save_path) and save_path[-1] == 'f'):
            with open(save_path, 'wb') as f:
                f.write(response.body)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(VitalSpider)
process.start(stop_after_crawl=True)



    
    
    








