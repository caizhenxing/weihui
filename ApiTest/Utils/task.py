import unittest

from Utils import testload, runner



class ApiTestCase(unittest.TestCase):
    """ create a testcase.
    """
    tecase_name = ""
    def __init__(self, test_runner, testcase):
        super(ApiTestCase, self).__init__()
        self.test_runner = test_runner
        self.testcase = testcase

    def runTest(self):
        """ run testcase and check result.
        """
        self.assertTrue(self.test_runner.run_test(self.testcase))

def create_suite(testset):
    """ create test suite with a testset, it may include one or several testcases.
        each suite should initialize a seperate Runner() with testset config.
    """
    suite = unittest.TestSuite()

    test_runner = runner.Runner()
    config_dict = testset.get("config", {})
    test_runner.init_config(config_dict, level="testset")
    testcases = testset.get("testcases", [])

    for testcase in testcases:
        ApiTestCase.runTest.__doc__ = testcase['name']
        test = ApiTestCase(test_runner, testcase)
        suite.addTest(test)


    return suite

def create_task(testcase_path):
    """ create test task suite with specified testcase path.
        each task suite may include one or several test suite.
    """
    task_suite = unittest.TestSuite()
    testsets = testload.load_testcases_by_path(testcase_path)

    for testset in testsets:
        suite = create_suite(testset)
        task_suite.addTest(suite)

    return task_suite

