import scrapy
import json
from pathlib import Path
from datetime import datetime

class NewspapersScraper(scrapy.Spider):
    name = 'newspaper-faz'
    start_urls = ['https://www.faz.net/']

    def parse(self, response):
        # headline = response.css('.block.font-brandUI.serifmode\:font-serifUI.font-extrabold.lg\:text-5xl.md\:text-5xl.sm\:text-3xl.leading-tight.mb-12 .align-middle::text').getall()[2]
        headline = response.css('a.top1-teaser__body::attr(title)').get().strip()
        link = response.css('a.top1-teaser__body::attr(href)').get()
        parts = link.split('/')
        category = parts[4]
        subtext = response.css('span[data-v-b7ce104a]::text').get()
        teaser = response.css('div.teaser-object__teaser-text.p2-teaser.sm\:p1-teaser.mb-\[10px\].cursor-pointer.sm\:mb-\[14px\]::text').get().strip()


        current_time = datetime.now()
        date_time = current_time.strftime("%Y-%m-%d %H:%M")
        weekday = current_time.strftime("%A")

        new_entry = {
            'headline': headline,
            'category': category,
            'subtext': subtext,
            'teaser' : teaser,
            'link' : link,
            'date_time': date_time,
            'weekday': weekday
        }

        file_path = '/home/faz.json'

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
