import scrapy
import json
from pathlib import Path
from datetime import datetime

class NewspapersScraper(scrapy.Spider):
    name = 'newspaper'
    start_urls = ['https://www.sueddeutsche.de']

    def parse(self, response):
        headline = response.css('span.css-1868ir3::text').get()
        # old (deteced eilmeldungen first and replace link with eilmeldung link)
        #link = response.css('a[data-track-szde]::attr(href)').get()
        link = response.css('a.css-bbw7r5::attr(href)').get()
        # extract category from link
        parts = link.split('/')
        category = parts[3]
        subtext = response.css('span[data-tb-headline]::text').get().strip()
        # only gets the first "big" category
        # category = response.css('span.css-1yaw99a::text').get()
        teaser = response.css('p[data-manual="teaser-text"]::text').get().strip()

        current_time = datetime.now()
        date_time = current_time.strftime("%Y-%m-%d %H:%M")
        weekday = current_time.strftime("%A")

        new_entry = {
            'headline': headline,
            'category': category,
            'subtext' : subtext,
            'teaser' : teaser,
            'link' : link,
            'date_time': date_time,
            'weekday': weekday
        }

        file_path = '/home/sueddeutsche.json'

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


