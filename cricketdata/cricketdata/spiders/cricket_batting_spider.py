import scrapy
import pandas as pd

class CricketBattingSpider(scrapy.Spider):
    name = 'cricket_batting'
    allowed_domains = ['espncricinfo.com']

    def start_requests(self):
        with open('links.txt', 'r') as f:
            links = f.readlines()
            for link in links:
                url = link.strip()
                if not url.startswith('http'):
                    url = 'https://www.espncricinfo.com' + url
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        match_title = response.css('#main-container > div.ds-relative > div > div > div.ds-flex.ds-space-x-5 > div.ds-grow > h1::text').get().split(',')[0]
        data = []

        # Extract data for both teams
        for i in range(2, 4):
            team_innings = response.css(f'#main-container > div.ds-relative > div > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child({i}) > div > div.ds-flex.ds-px-4.ds-border-b.ds-border-line.ds-py-3.ds-bg-ui-fill-translucent-hover > div > span > span.ds-text-title-xs.ds-font-bold.ds-capitalize::text').get()
            table = response.css(f'#main-container > div.ds-relative > div > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child({i}) > div > div.ds-p-0 > table.ds-w-full.ds-table.ds-table-md.ds-table-auto.ci-scorecard-table')
            
            for j, row in enumerate(table.css('tbody > tr:not(.ds-hidden)')):
                if j >= len(table.css('tbody > tr:not(.ds-hidden)')) - 4:
                    break  # Skip the last 4 rows
                
                tds = row.css('td')
                if len(tds) < 8:
                    continue
                
                batting_pos = j + 1
                batsman_name = tds[0].css('div > a::attr(title)').get()
                out_not_out = tds[1].css('span > span::text').get()
                r = tds[2].css('strong::text').get()
                b = tds[3].css('::text').get()
                m = tds[4].css('::text').get()
                fours = tds[5].css('::text').get()
                sixes = tds[6].css('::text').get()
                sr = tds[7].css('::text').get()
                
                data.append([
                    match_title, team_innings, batting_pos, batsman_name, out_not_out, r, b, m, fours, sixes, sr
                ])

        # Create dataframe and save to CSV
        df = pd.DataFrame(data, columns=['match', 'teamInnings', 'battingPos', 'batsmanName', 'out/not_out', 'R', 'B', 'M', '4s', '6s', 'SR'])
        df.to_csv('batting_summaries.csv', mode='a', index=False, header=True)

        print(f"Data for match '{match_title}' saved successfully.")

# To run this spider, use the command: scrapy crawl cricket_batting
