import logging

import requests

from Utils import exception, response
from Utils.client import request
from Utils.common import get_request_msg, sleep
from Utils.context import Context


class Runner(object):
    def __init__(self, http_client_session=None):
        self.http_client_session = http_client_session
        self.context = Context()

    def init_config(self, config_dict, level):

        self.context.init_context(level)
        requires = config_dict.get('requires', [])
        self.context.import_requires(requires)

        function_binds = config_dict.get('function_binds', {})
        self.context.bind_functions(function_binds, level)

        module_functions = config_dict.get('import_module_functions', [])
        self.context.import_module_functions(module_functions, level)

        variable_binds = config_dict.get('variable_binds', [])
        self.context.bind_variables(variable_binds, level)

        request_config = config_dict.get('request', {})
        request_config['name'] = config_dict.get('name')

        self.http_client_session = requests.Session()
        self.context.register_request(request_config, level)

    def run_test(self, testcase):
        self.init_config(testcase,level="testcase")
        parsed_request = self.context.get_parsed_request()

        try:
            logging.info(" start run test " + parsed_request.pop('name'))
            url = parsed_request.pop('url')
            method = parsed_request.pop('method')
        except KeyError:
            raise exception.ParamsError("URL or METHOD missed!")

        run_times = int(testcase.get("times", 1))
        extract_binds = testcase.get("extract_binds", {})
        validators = testcase.get("validators", [])

        parsed_request.setdefault("data", get_request_msg(parsed_request))

        try:
            parsed_request.pop('basic_data')
            parsed_request.pop('unique_data')
            parsed_request.pop('encrypt_data')
        except KeyError:
            pass

        second = 0
        try:
            second = parsed_request.pop('sleep')
        except KeyError:
            pass

        for _ in range(run_times):
            resp = request(method, url, **parsed_request)
            resp_obj = response.ResponseObject(resp)
            sleep(second)#发送请求后延时
            extracted_variables_mapping_list = resp_obj.extract_response(extract_binds)
            self.context.bind_variables(extracted_variables_mapping_list, level="testset")
            resp_obj.validate(validators)

        return True

    def run_testset(self, testset):
        results = []

        config_dict = testset.get("config", {})
        self.init_config(config_dict, level="testset")
        testcases = testset.get("testcases", [])
        for testcase in testcases:
            result = self.run_test(testcase)
            results.append(result)

        return results

    def run_testsets(self, testsets):
        return [self.run_testset(testset) for testset in testsets]
