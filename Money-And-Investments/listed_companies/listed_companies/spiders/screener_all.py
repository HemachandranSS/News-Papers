import scrapy
import urllib.parse
from datetime import datetime


class ScreenerAllSpider(scrapy.Spider):
    name = "screener_all"
    allowed_domains = ["screener.in"]
    start_urls = [f"https://www.screener.in/screens/357649/all-listed-companies/?page={i}" for i in range(1, 198)]

    current_date = datetime.now().strftime("%b_%d_%Y")
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 3,
        "FEED_URI": f"{current_date}_all_listed_companies_with_links.json",
        "FEED_FORMAT": "json",
    }

    def parse(self, response):
        companies = response.xpath("//td/a")
        for company in companies:
            name = company.xpath("text()").get()
            relative_link = company.xpath("@href").get()
            full_link = response.urljoin(relative_link)

            # Follow each company link to extract more details
            yield scrapy.Request(
                url=full_link,
                callback=self.parse_company,
                meta={"name": name, "link": full_link}
            )

    def parse_company(self, response):
        name = response.meta["name"]
        link = response.meta["link"]

        def safe_xpath(path):
            return response.xpath(path).get(default="").strip()

        company_name = safe_xpath("/html/body/main/div[3]/div[1]/div/h1/text()")
        company_link = safe_xpath("/html/body/main/div[3]/div[2]/a[1]/@href")
        sector = safe_xpath("/html/body/main/section[3]/div[1]/div[1]/p/a[1]/text()")
        industry = safe_xpath("/html/body/main/section[3]/div[1]/div[1]/p/a[2]/text()")

        encoded_name = urllib.parse.quote(company_name)
        google_link = f"https://www.google.com/search?q={encoded_name}"
        business_line_link = f"https://www.thehindubusinessline.com/stocks/{company_name.lower().replace(' ', '-')}"

        yield {
            "company_name": company_name,
            "company_link": company_link,
            "business_line_link": business_line_link,
            "google_link": google_link,
            "name": name,
            "link": link,
            "sector": sector,
            "industry": industry
        }
