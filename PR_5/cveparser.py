import scrapy


class CveparserSpider(scrapy.Spider):
    name = "kartunchikov_spider"
    allowed_domains = ["opencve.io"]
    start_urls = ["https://www.opencve.io/cve"]

    def parse(self, response):
        
        response = response.css('tr.cve-header')

        for cve in response:
            cve_id = cve.css('td.col-md-2 strong::text').get().strip()
            date = cve.css('td.col-md-2.text-center::text').get().strip()
            cvss_label = cve.css('td.col-md-1.text-center span::text').get().strip()

            if cvss_label == 'N/A':
                cvss = 'N/A'
            else:
                cvss = cvss_label.split()[0]  # Extract the numeric CVSS score


            yield {
                'cve-id': cve_id,
                'date': date,
                'cvss': cvss,
            }
