import scrapy
import json
from pathlib import Path
from datetime import datetime

class NewspapersScraper(scrapy.Spider):
    name = 'newspaper-zeit'
    start_urls = ['https://www.zeit.de/index']

    def parse(self, response):
        headline = response.css('span.zon-teaser__title.zon-teaser__title--extralarge::text').get()
        # split for getting subtext title
        subtext_download = response.css('a.zon-teaser__faux-link::text').get()
        subtext_strip = subtext_download.split(':', 1)
        subtext = subtext_strip[0]

        link = response.css('a.zon-teaser__link::attr(href)').get()
        parts = link.split('/')
        category = parts[3]
        teaser = response.css('p.zon-teaser__summary::text').get()


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

        file_path = '/home/zeit.json'

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

