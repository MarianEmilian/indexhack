# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from main.models import Article

class ScraperPipeline:
    def process_item(self, item, spider):
        if not Article.objects.filter(blog_id = item['blog_id']).exists():
            item.save()
        return item
