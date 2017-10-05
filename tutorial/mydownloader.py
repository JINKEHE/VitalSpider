import subprocess
import scrapy
class MyDownloader(object):
    def process_request(self, request, spider):
        if request.url.endswith(".zip"):
            subprocess.Popen(["wget", request.url, "-P", "~/temp"])
            return scrapy.http.HtmlResponse(url="", body="", encoding='utf8')
