#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Rui Vieira'
SITENAME = u'Rui Vieira'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

THEME = './theme/'
PLUGIN_PATHS = ["./plugins"]
PLUGINS = ["render_math", "pelican_javascript", "liquid_tags.video"]


# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

GOOGLE_ANALYTICS = 'UA-10507665-2'

#=============
# Twitter Card
#=============
# https://dev.twitter.com/cards
TWITTER_CARD_USE = (True) # (False)
TWITTER_CARD_SITE = '@ruimvieira'  # The site's Twitter handle like @my_blog
TWITTER_CARD_SITE_ID = ''  # The site's Twitter ID
TWITTER_CARD_CREATOR = '@ruimvieira'  # Your twitter handle like @monkmartinez
TWITTER_CARD_CREATOR_ID = ''  # The site creator's id
GRAVARTAR_URL = ''
