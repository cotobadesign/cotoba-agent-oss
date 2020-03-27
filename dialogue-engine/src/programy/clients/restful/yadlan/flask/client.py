"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import time
import logging

from flask import Flask, jsonify, request, Response, make_response
from flask_cors import CORS

from programy.utils.logging.loghandler import YadlanLogHandler
from programy.utils.logging.ylogger import YLogger
from programy.clients.restful.yadlan.client import YadlanRestBotClient


class FlaskYadlanClient(YadlanRestBotClient):

    def __init__(self, id, argument_parser=None):
        YadlanRestBotClient.__init__(self, id, argument_parser)
        self.initialise()

    def get_request_body(self, request):
        return request.data

    def run(self, flask):
        YLogger.set_default_level()
        YLogger.debug(self, "%s Client running on %s:%s" %
                      (self.id,
                       self.configuration.client_configuration.host,
                       self.configuration.client_configuration.port))
        self.startup()

        if self.configuration.client_configuration.debug is True:
            YLogger.debug(self, "%s Client running in debug mode" % self.id)

        if self.configuration.client_configuration.ssl_cert_file is not None and \
                self.configuration.client_configuration.ssl_key_file is not None:
            context = (self.configuration.client_configuration.ssl_cert_file,
                       self.configuration.client_configuration.ssl_key_file)

            YLogger.debug(self, "%s Client running in https mode" % self.id)
            flask.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug,
                      ssl_context=context)
        else:
            YLogger.debug(self, "%s Client running in http mode, careful now !" % self.id)
            flask.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug)

        self.shutdown()


if __name__ == '__main__':
    REST_CLIENT = None

    print("Initiating Yadlan Flask Service...")
    APP = Flask(__name__)
    CORS(APP)
    APP.config['JSON_AS_ASCII'] = False

    handler = YadlanLogHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))

    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.handlers.clear()
    werkzeug_logger.addHandler(handler)

    @APP.route('/<version>/stop', methods=['POST'])
    def stopPost(version=None):
        if REST_CLIENT.checkBotVersion(version) is False:
            return Response(status='404')

        try:
            REST_CLIENT.save_data_before_exit()
        except Exception:
            pass

        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 'OK'

    @APP.route('/<version>/ask', methods=['POST'])
    def askPost(version=None):
        if REST_CLIENT.checkBotVersion(version) is False:
            return Response(status='404')

        currentStartTime = time.time()
        response_data, status = REST_CLIENT.process_request(request)
        latency = (time.time() - currentStartTime)
        response_data['latency'] = latency

        rest_response = make_response(jsonify(REST_CLIENT.create_response(request, response_data, status, latency)))
        rest_response.mimetype = 'application/json; charset=utf-8'
        return rest_response, status

    @APP.route('/<version>/status', methods=['GET'])
    def statGet(version=None):
        if REST_CLIENT.checkBotVersion(version) is False:
            return Response(status='404')
        return ''

    @APP.route('/<version>/debug', methods=['POST'])
    def debugPost(version=None):
        if REST_CLIENT.checkBotVersion(version) is False:
            return Response(status='404')

        try:
            debugInfo, status = REST_CLIENT.process_debug_request(request)
        except Exception:
            pass

        response = make_response(jsonify(debugInfo))
        response.mimetype = 'application/json; charset=utf-8'
        return response, status

    print("Loading, please wait...")
    REST_CLIENT = FlaskYadlanClient("yadlan")
    print("Server start...")
    REST_CLIENT.run(APP)
