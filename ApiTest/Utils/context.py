import copy
import importlib
import os
import sys
import types
from collections import OrderedDict

from Utils import testload
from Utils.testcase import TestcaseParser


def is_function(tup):
    """ Takes (name, object) tuple, returns True if it is a function.
    """
    name, item = tup
    return isinstance(item, types.FunctionType)

class Context(object):
    """ Manages context functions and variables.
        context has two levels, testset and testcase.
    """
    def __init__(self):
        self.testset_shared_variables_mapping = OrderedDict()
        self.testcase_variables_mapping = OrderedDict()
        self.testcase_parser = TestcaseParser()
        self.init_context()

    def init_context(self, level='testset'):
        """
        testset level context initializes when a file is loaded,
        testcase level context initializes when each testcase starts.
        """
        if level == "testset":
            self.testset_functions_config = {}
            self.testset_request_config = {}
            self.testset_shared_variables_mapping = OrderedDict()

        # testcase config shall inherit from testset configs,
        # but can not change testset configs, that's why we use copy.deepcopy here.
        self.testcase_functions_config = copy.deepcopy(self.testset_functions_config)
        self.testcase_request_config = {}
        self.testcase_variables_mapping = copy.deepcopy(self.testset_shared_variables_mapping)

        self.testcase_parser.bind_functions(self.testcase_functions_config)
        self.testcase_parser.bind_variables(self.testcase_variables_mapping)


        if level == "testset":
            self.import_module_functions(["Utils.common"], "testset")

    def import_requires(self, modules):
        """ import required modules dynamicly
        """
        for module_name in modules:
            globals()[module_name] = importlib.import_module(module_name)

    def bind_functions(self, function_binds, level="testcase"):
        eval_function_binds = {}
        for func_name, function in function_binds.items():
            if isinstance(function, str):
                function = eval(function)
            eval_function_binds[func_name] = function

        self.__update_context_functions_config(level, eval_function_binds)

    def import_module_functions(self, modules, level="testcase"):
        """ import modules and bind all functions within the context
        """
        sys.path.insert(0, os.getcwd())
        for module_name in modules:
            imported = importlib.import_module(module_name)
            imported_functions_dict = dict(filter(is_function, vars(imported).items()))
            self.__update_context_functions_config(level, imported_functions_dict)
    '''
        提取变量，保留原值或者调用方法生成
    '''
    def bind_variables(self, variable_binds, level="testcase"):
        for variable_bind in variable_binds:
            for variable_name, value in variable_bind.items():
                variable_evale_value = self.testcase_parser.parse_content_with_bindings(str(value))#所有的值都转为str类型

                if level == "testset":
                    self.testset_shared_variables_mapping[variable_name] = variable_evale_value

                self.testcase_variables_mapping[variable_name] = variable_evale_value
                self.testcase_parser.bind_variables(self.testcase_variables_mapping)



    def __update_context_functions_config(self, level, config_mapping):
        if level == "testset":
            self.testset_functions_config.update(config_mapping)

        self.testcase_functions_config.update(config_mapping)
        self.testcase_parser.bind_functions(self.testcase_functions_config)

    def register_request(self, request_dict, level="testcase"):
        # if "headers" in request_dict:
        #     # convert keys in request headers to lowercase
        #     headers = request_dict.pop("headers")
        #     if not isinstance(headers, dict):
        #         raise ParamsError("HTTP Request Headers invalid!")
        #     request_dict["headers"] = {key.lower(): headers[key] for key in headers}

        self.__update_context_request_config(level, request_dict)

    def __update_context_request_config(self, level, config_mapping):
        """
        @param level: testset or testcase
        @param config_type: request
        @param config_mapping: request config mapping
        """
        if level == "testset":
            self.testset_request_config.update(config_mapping)

        self.testcase_request_config = testload.deep_update_dict(
            copy.deepcopy(self.testset_request_config),
            config_mapping
        )


    def get_parsed_request(self):
        """ get parsed request, with each variable replaced by bind value.
        """
        parsed_request = self.testcase_parser.parse_content_with_bindings(
            self.testcase_request_config
        )

        return parsed_request

    def get_testcase_variables_mapping(self):
        return self.testcase_variables_mapping
