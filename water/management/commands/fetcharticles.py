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
            category = 'hani'
            url = ele.link
            filename = '%s/%s' % (category, urlparse(url).path.split('/')[-1])

            if default_storage.exists(filename):
                print 'Skip because already done - %s' % filename
                continue

            rep = requests.get(url)

            fp = default_storage.open('%s' % (filename), 'w')
            fp.write(rep.content)
            fp.close()

            print "Fetched %s, Save on S3 %s" % (rep.ok, fp)

    def load_from_S3(self):
        articles = {}
        for ele in default_storage.bucket.list():
            article = {}
            print ele
            content = ele.read()
            root = etree.HTML(content)

            try:
                article['url'] = root.xpath('//meta[@property="og:url"]/@content')[0]
                article['title'] = root.xpath('//title/text()')[0]

                subtitle = root.xpath('//div[@class="subtitle"]/text()')
                subtitle = '\n'.join(map(lambda x: x.strip(), subtitle))

                article['subtitle'] = subtitle

                text = root.xpath('//div[@class="text"]/text()')
                if len(text) == 0:
                    text = root.xpath('//div[@class="article-contents"]/text()')

                text = '\n'.join(map(lambda x: x.strip(), text)).strip()
                article['text'] = text

                try:
                    publish_at = root.xpath('//p[@class="date-time"]/span/text()')

                except ValueError:
                    publish_at = root.xpath('//p[@class="date"]/span/text()')

                article['publish_at'] = publish_at

                print article
                articles.append(article)

            except IndexError as e:
                print e

        return articles

    def handle(self, *args, **options):
        # self.load_from_S3()
        self.fetch_news_to_S3()
