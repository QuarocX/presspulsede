import scrapy
import json
from pathlib import Path
from datetime import datetime

class NewspapersScraper(scrapy.Spider):
    name = 'newspaper-spiegel'
    start_urls = ['https://www.spiegel.de/']

    def parse(self, response):
        # headline = response.css('.block.font-brandUI.serifmode\:font-serifUI.font-extrabold.lg\:text-5xl.md\:text-5xl.sm\:text-3xl.leading-tight.mb-12 .align-middle::text').getall()[2]
        headline = response.css("article.lg\\:p-24.md\\:py-24.sm\\:py-16::attr(aria-label)").get()
        link = response.css("article > * > * > a::attr(href)").get()
        parts = link.split('/')
        category = parts[3]
        subtext = response.css('span.block.text-primary-base.hover\:text-primary-dark.focus\:text-primary-darker.dark\:text-shade-lightest.dark\:hover\:opacity-moderate.dark\:hover\:text-shade-lightest.dark\:focus\:opacity-moderate.dark\:focus\:text-shade-lightest.font-sansUI.font-normal.lg\:text-base.md\:text-base.sm\:text-s.leading-normal.mb-4::text').get().strip()
        teaser = response.css('span[data-target-teaser-el="text"]::text').get().strip()


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

        file_path = '/home/spiegel.json'


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
