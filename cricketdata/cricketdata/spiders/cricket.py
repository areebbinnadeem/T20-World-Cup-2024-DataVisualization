import scrapy
import pandas as pd

class CricketSpider(scrapy.Spider):
    name = 'cricket'
    allowed_domains = ['espncricinfo.com']
    start_urls = ['http://espncricinfo.com/']

    def start_requests(self):
        urls = [
            "https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2024-15946",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('I am parsing')
        
        # Extract the headers
        headers = []
        table = response.css('#main-container > div.ds-relative > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div:nth-child(2) > div > div:nth-child(1) > div.ds-overflow-x-auto.ds-scrollbar-hide > table')
        for row in table.css('thead > tr'):
            tds = row.css('td')
            for td in tds:
                span_text = td.css('div > span::text').get()
                headers.append(span_text)

        # Initialize data storage
        data = []
        links = []

        # Extract the data
        for row in table.css('tbody > tr'):
            row_data = []
            tds = row.css('td')
            for i, td in enumerate(tds):
                if i in {0, 1, 2, 3, 5}:  # Columns with <span> tags
                    span_text = td.css('span::text').get()
                    row_data.append(span_text)
                elif i == 4:  # Column with <a> tag
                    a_title = td.css('span > a::attr(title)').get()
                    row_data.append(a_title)
                elif i == 6:  # Column with <a> tag and link to save
                    a_title = td.css('span > a::attr(title)').get()
                    link = td.css('span > a::attr(href)').get()
                    row_data.append(a_title)
                    links.append(link)
            data.append(row_data)

        # Create dataframe
        df = pd.DataFrame(data, columns=headers)

        # Save dataframe to CSV
        df.to_csv('cricket_match_summaries.csv', index=False)

        # Save links to a separate file
        with open('links.txt', 'w') as f:
            for link in links:
                f.write(f"{link}\n")

        # Print confirmation
        print(f"CSV and links file have been saved.")
