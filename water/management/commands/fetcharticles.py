# -*- coding: utf-8 -*-
import sys
import requests
from urlparse import urlparse
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from lxml import etree
import feedparser

reload(sys)
sys.setdefaultencoding('utf-8')


class Command(BaseCommand):
    help = "My shiny new management command."

    def fetch_news_to_S3(self):
        feed = feedparser.parse('http://www.hani.co.kr/rss/')

        for ele in feed.entries:
            url = ele.link
            category = 'hani'
            rep = requests.get(url)

            filename = urlparse(url).path.split('/')[-1]
            import ipdb; ipdb.set_trace()
            fp = default_storage.open('%s/%s' % (category, filename), 'w')
            fp.write(rep.content)
            fp.close()

            print "Fetched %s, Save on S3 %s" % (rep.ok, fp)

    def load_from_S3(self):
        for ele in default_storage.bucket.list():
            print ele
            content = ele.read()
            root = etree.HTML(content)

            try:
                url = root.xpath('//meta[@property="og:url"]/@content')[0]
                title = root.xpath('//title/text()')[0]

                subtitle = root.xpath('//div[@class="subtitle"]/text()')
                subtitle = '\n'.join(map(lambda x: x.strip(), subtitle))

                text = root.xpath('//div[@class="text"]/text()')
                if len(text) == 0:
                    text = root.xpath('//div[@class="article-contents"]/text()')

                text = '\n'.join(map(lambda x: x.strip(), text)).strip()

                try:
                    publish_at = root.xpath('//p[@class="date-time"]/span/text()')

                except ValueError:
                    publish_at = root.xpath('//p[@class="date"]/span/text()')

                print url, title, subtitle, text, publish_at

            except IndexError as e:
                print e

    def handle(self, *args, **options):
        self.load_from_S3()
        # self.fetch_news_to_S3()
