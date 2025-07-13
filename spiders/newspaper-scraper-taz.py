import scrapy
import json
from pathlib import Path
from datetime import datetime

class NewspapersScraper(scrapy.Spider):
    name = 'newspaper-taz'
    start_urls = ['https://taz.de/']

    def parse(self, response):
        headline = response.css('.headline.link.typo-r-head-medium.mgt-xsmall-mobile.mgb-xsmall-mobile.mgb-small::text').get().strip()
        category = 'undefined'
        subtext = response.css('p.mgb-small.typo-r-topline.mgr-small::text').get().strip()
        teaser = response.css('div.typo-r-subline.mgt-xsmall-mobile::text').get().strip()

        link = response.css('a.mgt-small-medium-mobile.teaser-link::attr(href)').get()

        # Open article to extract proper category
        if link:
            yield response.follow(link, self.parse_article, meta={
                'headline': headline,
                'category': category,
                'subtext': subtext,
                'teaser': teaser,
                'link': link
            })
        else:
            yield self.create_entry(headline, category, subtext, teaser, link)


    def parse_article(self, response):
            breadcrumb_text = response.css('li[data-breadcrumb-level="1"] a::text').get()
            category = breadcrumb_text.strip() if breadcrumb_text else 'undefined'

            yield self.create_entry(
                response.meta['headline'],
                category,
                response.meta['subtext'],
                response.meta['teaser'],
                response.meta['link']
            )

    def create_entry(self, headline, category, subtext, teaser, link):
        current_time = datetime.now()
        date_time = current_time.strftime("%Y-%m-%d %H:%M")
        weekday = current_time.strftime("%A")

        new_entry = {
            'headline': headline,
            'category': category,
            'subtext': subtext,
            'teaser': teaser,
            'link': link,
            'date_time': date_time,
            'weekday': weekday
        }

        file_path = '/home/taz.json'

        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_entries = json.load(f)
        else:
            existing_entries = []

        # Check if the headline already exists in the existing entries
        headline_exists = any(entry['headline'] == headline for entry in existing_entries)

        if not headline_exists:
            existing_entries.append(new_entry)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_entries, f, ensure_ascii=False, indent=4)

            # Save to the second file path
            with open(file_path_2, 'w', encoding='utf-8') as f:
                json.dump(existing_entries, f, ensure_ascii=False, indent=4)


        return new_entry