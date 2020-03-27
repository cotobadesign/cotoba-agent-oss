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
import resource

from sanic import Sanic
from sanic import response
from sanic_cors import CORS

from programy.utils.logging.ylogger import YLogger
from programy.clients.restful.yadlan.client import YadlanRestBotClient

resource.setrlimit(resource.RLIMIT_NOFILE, (1024, 4096))


class SanicYadlanClient(YadlanRestBotClient):

    def __init__(self, id, argument_parser=None):
        YadlanRestBotClient.__init__(self, id, argument_parser)
        self.initialise()

    def get_request_body(self, request):
        return request.body

    def run(self, sanic):
        YLogger.set_default_level()
        YLogger.debug(self, "%s Client running on %s:%s" %
                      (self.id,
                       self.configuration.client_configuration.host,
                       self.configuration.client_configuration.port))
        self.startup()
        self._sanic = sanic

        if self.configuration.client_configuration.debug is True:
            YLogger.debug(self, "%s Client running in debug mode" % self.id)

        if self.configuration.client_configuration.ssl_cert_file is not None and \
                self.configuration.client_configuration.ssl_key_file is not None:
            context = (self.configuration.client_configuration.ssl_cert_file,
                       self.configuration.client_configuration.ssl_key_file)

            YLogger.debug(self, "%s Client running in https mode" % self.id)
            sanic.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug,
                      workers=self.configuration.client_configuration.workers,
                      ssl_context=context,
                      access_log=False)
        else:
            YLogger.debug(self, "%s Client running in http mode, careful now !" % self.id)
            sanic.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug,
                      workers=self.configuration.client_configuration.workers,
                      access_log=False)

        self.shutdown()


if __name__ == '__main__':
    REST_CLIENT = None

    print("Initiating Yadlan Sanic Service...")
    APP = Sanic()
    CORS(APP)
    APP.config['JSON_AS_ASCII'] = False

    @APP.route('/<version>/stop', methods=['POST'])
    def stopPost(request, version=None):
        if REST_CLIENT.checkBotVersion(version) is False:
            return response.text('', status='404')

        try:
            REST_CLIENT.save_data_before_exit()
        except Exception:
            pass

        APP.stop()
        return response.text('')

    @APP.route('/<version>/ask', methods=['POST'])
    async def askPost(request, version=None):
        if REST_CLIENT.checkBotVersion(version) is False:
            return response.text('', status='404')

        currentStartTime = time.time()
        response_data, status = REST_CLIENT.process_request(request)
        latency = (time.time() - currentStartTime)
        response_data['latency'] = latency
        response_data = REST_CLIENT.create_response(request, response_data, status, latency)

        rest_response = response.json(response_data,
                                      headers={'Content-type': 'application/json; charset=utf-8'},
                                      status=status,
                                      ensure_ascii=False)
        return rest_response

    @APP.route('/<version>/status', methods=['GET'])
    async def statGet(request, version):
        if REST_CLIENT.checkBotVersion(version) is False:
            return response.text("", status='404')
        return response.text('')

    @APP.route('/<version>/debug', methods=['POST'])
    async def debugPost(request, version):
        if REST_CLIENT.checkBotVersion(version) is False:
            return response.text("", status='404')

        try:
            debugInfo, status = REST_CLIENT.process_debug_request(request)
        except Exception:
            pass

        return response.json(debugInfo,
                             headers={'Content-type': 'application/json; charset=utf-8'},
                             status=status,
                             ensure_ascii=False)

    print("Loading, please wait...")
    REST_CLIENT = SanicYadlanClient("yadlan")
    print("Server start...")
    REST_CLIENT.run(APP)
