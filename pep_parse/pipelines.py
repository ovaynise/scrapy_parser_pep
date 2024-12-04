import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class PepParsePipeline:
    def __init__(self, results_dir):
        self.results_dir = Path(results_dir)
        self.output_file = None

    @classmethod
    def from_crawler(cls, crawler):
        feeds_key = next(iter(crawler.settings.get('FEEDS').keys()))
        results_dir = Path(feeds_key).parent
        return cls(results_dir)

    def open_spider(self, spider):
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.status_counts = defaultdict(int)
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.output_file = self.results_dir / ('status_'
                                               f'summary_{current_time}.csv')

        with open(
                self.output_file,
                'w',
                newline='',
                encoding='utf-8') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=['Статус', 'Количество'])
            writer.writeheader()

    def process_item(self, item, spider):
        status = item.get('status')
        if status:
            self.status_counts[status] += 1
        return item

    def close_spider(self, spider):
        total = sum(self.status_counts.values())
        self.status_counts['Total'] = total

        with open(
                self.output_file,
                'a',
                newline='',
                encoding='utf-8') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=['Статус', 'Количество']
            )
            writer.writerows(
                [{'Статус': status,
                  'Количество': count} for status, count in
                 self.status_counts.items()]
            )
