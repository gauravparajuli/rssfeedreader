from flask import Flask, render_template
from pprint import pprint
import jinja_partials
import feedparser

feeds = {
    'https://blog.teclado.com/rss/': {
        'title': 'The Teclado Blog',
        'href': 'https://blog.teclado.com/rss/',
        'show_images': True,
        'entries': {}
    },
    'https://www.joshwcomeau.com/rss.xml': {
        'title': 'Josh W Comeau Blog',
        'href': 'https://www.joshwcomeau.com/rss.xml',
        'show_images': True,
        'entries': {}
    }
}

app = Flask(__name__)
jinja_partials.register_extensions(app) # will allow us to call jinja-partials functions from our template

@app.route('/')
@app.route('/feed/<path:feed_url>')
def render_feed(feed_url:str = None):
    for url, feed_ in feeds.items():
        parsed_feed = feedparser.parse(url)
        for entry in parsed_feed.entries:
            if entry.link not in feeds['entries']:
                feeds['entries'][entry.link] = entry

    if feed_url is None:
        feed = list(feed.values())[0]
    else:
        feed = feeds['feed_url']


    return render_template('feed.html', feed=feed['entries'].values(), feeds=feeds)