# -*- coding: utf-8 -*-
import requests_mock
import os
import boto
import json
from django.core import mail
from datetime import datetime
from django.test import TestCase
from water.utils import (fetch_news_to_S3,
                         load_from_S3, send_email_for_fetched_articles,
                         insert_news_to_db)
from water.tasks import celery_send_email_for_fetched_articles
from django.core.files.storage import default_storage
from moto import mock_s3


class ArticlesTestCase(TestCase):
    def setUp(self):
        self.moto = mock_s3()
        self.moto.start()
        conn = boto.connect_s3('<aws-access-key>', '<aws-secret-key>')
        conn.create_bucket('hmapps')

        self.rep_hani_rss = open('water/dumps/hani.rss', 'r').read()
        self.rep_mk_rss = open('water/dumps/mk.rss', 'r').read()
        self.rep_790164 = open('water/dumps/790164.html', 'r').read()
        self.rep_790165 = open('water/dumps/790165.html', 'r').read()
        self.rep_790166 = open('water/dumps/790166.html', 'r').read()

        self.rep_245269 = open('water/dumps/245269.html', 'r').read()
        self.rep_245273 = open('water/dumps/245273.html', 'r').read()
        self.rep_245393 = open('water/dumps/245393.html', 'r').read()

    def test_insert_news_to_db(self):
        fp = open('water/dumps/articles.txt', 'r')
        articles = json.loads(fp.read())
        insert_news_to_db(articles)

    @requests_mock.mock()
    def test_fetch_news_to_S3(self, m):
        # It fetches from rss file
        # parses the root rss file properly
        # save the content of link in rss into S3

        m.get('http://www.hani.co.kr/rss/',
              text=self.rep_hani_rss.decode('utf8'))
        m.get('http://www.hani.co.kr/arti/society/labor/790164.html',
              text=self.rep_790164.decode('utf8'))
        m.get('http://www.hani.co.kr/arti/economy/it/790165.html',
              text=self.rep_790165.decode('utf8'))
        m.get('http://www.hani.co.kr/arti/society/health/790166.html',
              text=self.rep_790166.decode('utf8'))

        fetch_news_to_S3()
        self.assertEqual(len(default_storage.bucket.get_all_keys()), 3)

    def test_load_from_S3(self):
        # It parses the article
        # parse the content of each article

        for ele in [e for e in os.listdir('water/dumps/') if 'html' in e]:
            default_storage.save('hani/%s-%s' %
                                 (datetime.now().strftime('%Y-%m-%d'), ele),
                                 open('water/dumps/%s' % ele, 'r'))

        articles = load_from_S3()
        self.assertEqual(len(articles), 6)

        send_email_for_fetched_articles(articles)
        mail_article = mail.outbox.pop()
        self.assertIn(u'한겨레', mail_article.body)

    @requests_mock.mock()
    def test_celery_send_email_for_fetched_articles(self, m):

        m.get('http://www.hani.co.kr/rss',
              text=self.rep_hani_rss.decode('utf8'))
        m.get('http://file.mk.co.kr/news/rss/rss_30100041.xml',
              text=self.rep_mk_rss.decode('euc-kr', 'ignore'))

        m.get('http://www.hani.co.kr/arti/society/labor/790164.html',
              text=self.rep_790164.decode('utf8'))
        m.get('http://www.hani.co.kr/arti/economy/it/790165.html',
              text=self.rep_790165.decode('utf8'))
        m.get('http://www.hani.co.kr/arti/society/health/790166.html',
              text=self.rep_790166.decode('utf8'))

        m.get('http://news.mk.co.kr/newsRead.php?no=245393&year=2017',
              text=self.rep_245269.decode('euc-kr', 'ignore'))
        m.get('http://news.mk.co.kr/newsRead.php?no=245273&year=2017',
              text=self.rep_245273.decode('euc-kr', 'ignore'))
        m.get('http://news.mk.co.kr/newsRead.php?no=245269&year=2017',
              text=self.rep_245393.decode('euc-kr', 'ignore'))

        kwargs = {"url": "http://www.hani.co.kr/rss"}
        kwargs = {"url": "http://file.mk.co.kr/news/rss/rss_30100041.xml"}

        celery_send_email_for_fetched_articles(**kwargs)

    def tearDown(self):
        self.moto.stop()
