"""Serves site/ on http://localhost:8080.

Same as `python -m http.server`, except Markdown and text files are sent as UTF-8 plain text,
so the agent-mode pages open in the browser (instead of downloading) and the ₦ sign shows correctly.
"""
import functools, http.server, os

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.md': 'text/plain; charset=utf-8', '.txt': 'text/plain; charset=utf-8'}

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
http.server.ThreadingHTTPServer(('127.0.0.1', 8080), functools.partial(Handler, directory=root)).serve_forever()
