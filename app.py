from flask import Flask, render_template
from pprint import pprint
import jinja_partials
import feedparser

feed = {
    'title': 'The Teclado Blog',
    'href': 'https://blog.teclado.com/rss/',
    'show_images': True,
    'entries': {}
}

app = Flask(__name__)
jinja_partials.register_extensions(app) # will allow us to call jinja-partials functions from our template

@app.route('/feed/')
def render_feed():
    feed_url = feed['href']
    parsed_feed = feedparser.parse(feed_url)
    for entry in parsed_feed.entries:
        if entry.link not in feed['entries']:
            feed['entries'][entry.link] = entry

    return render_template('feed.html', feed=feed['entries'].values())