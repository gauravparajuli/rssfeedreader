from flask import Flask, render_template, abort, request
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

# get entries
for url, feed_ in feeds.items():
    parsed_feed = feedparser.parse(url)
    for entry in parsed_feed.entries:
        if entry.link not in feed_['entries']:
            feed_['entries'][entry.link] = entry

app = Flask(__name__)
jinja_partials.register_extensions(app) # will allow us to call jinja-partials functions from our template

@app.route('/entries/<path:feed_url>')
def render_feed_entries(feed_url:str):
    try:
        feed = feeds[feed_url]
    except KeyError:
        abort(404, message='feed not found')

    page = int(request.args.get('page', 0))

    return render_template(
        'partials/entry_page.html',
        entries = list(feed['entries'].values())[page*5:page*5+5],
        href=feed_url,
        page=page,
        max_page = len(feed['entries']) // 5
    )


@app.route('/')
@app.route('/feed/<path:feed_url>')
def render_feed(feed_url:str = None):
    if feed_url is None:
        feed = list(feeds.values())[0]
    else:
        print(feed_url)
        feed = feeds[feed_url]


    return render_template('feed.html', feed=feed, entries=feed['entries'].values(), feeds=feeds)