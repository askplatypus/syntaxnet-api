"""
Copyright 2016 Thomas Pellissier Tanon All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import parsey


class CORSMiddleware(object):
    _allow_origin = '*'
    _allow_headers = 'Origin, X-Requested-With, Content-Type, Content-Language, Accept, Accept-Language'
    _allow_methods = 'GET, POST, OPTIONS'

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ['REQUEST_METHOD'] == 'OPTIONS':
            start_response('200 OK', [
                ('Access-Control-Allow-Origin', self._allow_origin),
                ('Access-Control-Allow-Headers', self._allow_headers),
                ('Access-Control-Allow-Methods', self._allow_methods)
            ])
            return ['POST']
        else:
            def start_response_cors(status, headers, exc_info=None):
                headers.append(('Access-Control-Allow-Origin', self._allow_origin))
                headers.append(('Access-Control-Allow-Headers', self._allow_headers))
                headers.append(('Access-Control-Allow-Methods', self._allow_methods))
                return start_response(status, headers, exc_info)
            return self.app(environ, start_response_cors)


def _parsey_universal_full_handler(environ, start_response):
    text = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
    language_code = environ.get('HTTP_CONTENT_LANGUAGE', 'en').lower()

    try:
        conllu_result = parsey.parsey_universal_full_conllu(text, language_code)
        start_response('200 OK', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(conllu_result)))
        ])
        return [conllu_result]
    except ValueError as e:
        message = str(e)
        start_response('400 Bad Request', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(message)))
        ])
        return [message]
    except Exception as e:
        start_response('500 Internal Server Error', [])
        return []

@CORSMiddleware
def app(environ, start_response):
    path = environ.get('PATH_INFO')
    if path == '/v1/parsey-universal-full':
        return _parsey_universal_full_handler(environ, start_response)
    elif path == '/v1/swagger.yaml':
        swagger_file = open('swagger.yaml', 'rb')
        swagger = swagger_file.read()
        swagger_file.close()
        start_response('200 OK', [
            ('Content-Type', 'application/yaml'),
            ('Content-Length', str(len(swagger)))
        ])
        return [swagger]
    elif path == '/':
        start_response('301 Moved Permanently', [('Location', '/v1')])
        return []
    else:
        start_response('404 Not Found', [])
        return []
