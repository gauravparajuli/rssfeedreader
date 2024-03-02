from flask import Flask, render_template
import jinja_partials
import feedparser

# app = Flask(__name__)

feed = {
    'title': 'The Teclado Blog',
    'href': 'https://blog.teclado.com/rss/',
    'show_images': True,
    'entries': {}
}

# @app.get('/')
# def home():
#     return dict(message="it's working"), 200

def create_app():
    app = Flask(__name__)
    jinja_partials.register_extensions(app) # will allow us to call jinja-partials functions from our template

    @app.route('/feed/')
    def render_feed():
        feed_url = feed['href']
        parsed_feed = feedparser(feed_url)
        for entry in parsed_feed.entries():
            if entry.link not in feed['entries']:
                feed['entries'][entry.link] = entry

    return render_template('feed.html', feed=feed)

    return app