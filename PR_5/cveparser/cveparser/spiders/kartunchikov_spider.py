

import scrapy


class CveparserSpider(scrapy.Spider):
    name = "kartunchikov_spider"
    allowed_domains = ["opencve.io"]
    start_urls = ["https://www.opencve.io/cve"]
    pg_count = 0

    def parse(self, response):
        
        for cve in response.css('tr.cve-header'):
            cve_id = cve.css('td.col-md-2 strong::text').get().strip()
            date = cve.css('td.col-md-2.text-center::text').get().strip()
            
            try:
                cvss_label = cve.css('td.col-md-1.text-center span.label-danger::text').get().strip()
            except:
                cvss_label = cve.css('td.col-md-1.text-center span.label::text').get().strip()

            yield {
                'cve-id': cve_id,
                'date': date,
                'cvss': cvss_label.split()[0],
            }

        
        next_page = response.css('li.next ::attr(href)').get()

        if self.pg_count < 50:
            self.pg_count+=1
            next_page_url = 'https://www.opencve.io' + next_page
            yield response.follow(next_page_url, callback=self.parse)
            

