import threading
import webbrowser

from argparse import ArgumentParser, REMAINDER
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os.path import dirname
from mimetypes import guess_type
from zipfile import ZipFile

THIS_ZIP = dirname(__file__)

class ZipHandlerMaker(object):

    def __init__(self):
        self.added_files = {}

    def add_file(self, path, fs_path = None, content = None):
        if fs_path is None:
            fs_path = path
        if content is None:
            with open(fs_path) as f:
                content = f.read()
        self.added_files[path] = content

    def __call__(self, *other):
        zh = ZipHandler(self.added_files, *other)
        return zh # this isn't actually needed

class ZipHandler(BaseHTTPRequestHandler):

    def __init__(self, added_files, *other):
        self.added_files = added_files
        BaseHTTPRequestHandler.__init__(self, *other)

    def do_GET(self):
        path = self.path
        if path.endswith('/'):
            path += 'index.html'
        path = path[1:]
        if path in self.added_files:
            content = self.added_files[path]
        else:
            try:
                with ZipFile(THIS_ZIP) as f:
                    content = f.read('documentroot/' + path)
            except KeyError:
                self.send_response(404)
                self.end_headers()
                return
        self.send_response(200)
        mime_type, content_encoding = guess_type(path)
        if mime_type:
            self.send_header('Content-Type', mime_type)
        if content_encoding:
            self.send_header('Content-Encoding', content_encoding)
        self.send_header('Content-Length', len(content))
        self.send_header('Connection:', 'close')
        self.end_headers()
        self.wfile.write(content)

def start_browser(server_ready_event, url):
    server_ready_event.wait()
    webbrowser.open(url)

def main():

    parser = ArgumentParser(prog='zhs')
    parser.add_argument('--port', '-p', help = 'The port the server will listen to.', default = 8000)
    parser.add_argument('--no-broswer', '-n', default = False, action = 'store_true', help = 'If present, no browser window will be opened.')
    parser.add_argument('extra_files', help = 'A list of path[:fs_path] specification of additional files to serve.', nargs = REMAINDER)
    args = parser.parse_args()

    zhm = ZipHandlerMaker()
    for pp in args.extra_files:
        path, fs_path = pp.split(':') if ':' in pp else (path, None)
        zhm.add_file(path, fs_path)
    server = HTTPServer(('', int(args.port)), zhm)
    browser_thread = None
    if not args.no_broswer:
        server_ready = threading.Event()
        browser_thread = threading.Thread(target = start_browser, args = (server_ready, 'http://localhost:{}/'.format(args.port)))
        browser_thread.start()
        server_ready.set()
    print 'Starting server on port {}, press ^C sto stop...'.format(args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Shutting down the web server!'
    finally:
        server.shutdown()
        if browser_thread: browser_thread.join()

main()
