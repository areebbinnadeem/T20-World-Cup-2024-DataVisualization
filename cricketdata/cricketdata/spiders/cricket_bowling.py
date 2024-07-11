import scrapy
import pandas as pd

class CricketBowlingSpider(scrapy.Spider):
    name = 'cricket_bowling'
    allowed_domains = ['espncricinfo.com']

    def __init__(self):
        self.data = []

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

        # Extract data for both teams
        # First team
        bowling_team_1 = response.css('#main-container > div.ds-relative > div > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child(3) > div > div.ds-flex.ds-px-4.ds-border-b.ds-border-line.ds-py-3.ds-bg-ui-fill-translucent-hover > div > span > span.ds-text-title-xs.ds-font-bold.ds-capitalize::text').get()
        table_1 = response.css('#main-container > div.ds-relative > div > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child(2) > div > div.ds-p-0 > table:nth-child(2)')

        for row in table_1.css('tbody > tr:not(.ds-hidden)'):
            tds = row.css('td')
            if len(tds) < 11:
                continue

            bowler_name = tds[0].css('div > a > span::text').get()
            o = tds[1].css('::text').get()
            m = tds[2].css('::text').get()
            r = tds[3].css('::text').get()
            w = tds[4].css('span > strong::text').get()
            econ = tds[5].css('::text').get()
            zeros = tds[6].css('::text').get()
            fours = tds[7].css('::text').get()
            sixes = tds[8].css('::text').get()
            wd = tds[9].css('::text').get()
            nb = tds[10].css('::text').get()

            self.data.append([
                match_title, bowling_team_1, bowler_name, o, m, r, w, econ, zeros, fours, sixes, wd, nb
            ])

        # Second team
        bowling_team_2 = response.css('#main-container > div.ds-relative > div > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child(2) > div > div.ds-flex.ds-px-4.ds-border-b.ds-border-line.ds-py-3.ds-bg-ui-fill-translucent-hover > div > span > span.ds-text-title-xs.ds-font-bold.ds-capitalize::text').get()
        table_2 = response.css('#main-container > div.ds-relative > div > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child(3) > div > div.ds-p-0 > table:nth-child(2)')

        for row in table_2.css('tbody > tr:not(.ds-hidden)'):
            tds = row.css('td')
            if len(tds) < 11:
                continue

            bowler_name = tds[0].css('div > a > span::text').get()
            o = tds[1].css('::text').get()
            m = tds[2].css('::text').get()
            r = tds[3].css('::text').get()
            w = tds[4].css('span > strong::text').get()
            econ = tds[5].css('::text').get()
            zeros = tds[6].css('::text').get()
            fours = tds[7].css('::text').get()
            sixes = tds[8].css('::text').get()
            wd = tds[9].css('::text').get()
            nb = tds[10].css('::text').get()

            self.data.append([
                match_title, bowling_team_2, bowler_name, o, m, r, w, econ, zeros, fours, sixes, wd, nb
            ])

    def closed(self, reason):
        df = pd.DataFrame(self.data, columns=['match', 'bowlingTeam', 'bowlerName', 'O', 'M', 'R', 'W', 'ECON', '0s', '4s', '6s', 'WD', 'NB'])
        df.to_csv('bowling_summaries.csv', mode='w', index=False)

# To run this spider, use the command: scrapy crawl cricket_bowling
