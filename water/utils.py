# -*- coding: utf-8 -*-
import requests
from lxml import etree
from StringIO import StringIO
from urlparse import urlparse
from django.core.files.storage import default_storage
from datetime import datetime
from dateutil.parser import parse
from django.core.mail import EmailMultiAlternatives


def fetch_news_to_S3():
    feeds = requests.get('http://www.hani.co.kr/rss/')
    output = StringIO(feeds.content)
    tree = etree.parse(output)

    for item in tree.xpath('/rss/channel/item'):
        category = 'hani'
        url = item.xpath('link/text()')[0]
        published = parse(item.xpath('pubDate/text()')[0])
        filename = '%s/%s-%s' % (category,
                                 published.strftime('%Y-%m-%d'),
                                 urlparse(url).path.split('/')[-1])

        if default_storage.exists(filename):
            print 'Skip because already done - %s' % filename
            continue

        rep = requests.get(url)

        fp = default_storage.open('%s' % (filename), 'w')
        fp.write(rep.content)
        fp.close()


def load_from_S3():
    articles = []

    for ele in default_storage.bucket.list(
            prefix='hani/%s' % datetime.now().strftime('%Y-%m-%d')):

        article = {}
        content = ele.read()
        root = etree.HTML(content)

        try:
            article['url'] = root.xpath(
                '//meta[@property="og:url"]/@content')[0]
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

            articles.append(article)

        except IndexError as e:
            print e

    return articles


def send_email_for_fetched_articles(articles):
    subject = '%s - Daily News' % datetime.now().strftime('%Y-%m-%d')
    from_email, to = 'chharry@gmail.com', 'chharry@gmail.com'
    text_content = ''
    html_content = ''

    for article in articles:
        html_content += "<p>%s<a href='%s'></p>" % (
            article['title'], article['url'])

        text_content += "%s - %s" % (
            article['title'], article['url'],)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
