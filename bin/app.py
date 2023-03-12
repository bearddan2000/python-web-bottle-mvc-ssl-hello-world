from bottle import (
    route,
    run,
    static_file,
    ServerAdapter
)

class SSLCherootAdapter(ServerAdapter):
    def run(self, handler):
        from cheroot import wsgi
        from cheroot.ssl.builtin import BuiltinSSLAdapter
        import ssl

        server = wsgi.Server((self.host, self.port), handler)
        server.ssl_adapter = BuiltinSSLAdapter("cert/server.crt", "cert/server.key")

        try:
            server.start()
        finally:
            server.stop()

@route('/')
def index():
	return static_file('index.html', root='./templates')

run(host='0.0.0.0', port=443, server=SSLCherootAdapter, debug=True)
