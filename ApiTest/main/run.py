import logging
import os
import PyUnitReport
from collections import OrderedDict
from Utils.task import create_task


testset_paths =os.path.abspath("..")+"\\testcase\\MgsTest"


results = {}
subject = "SUCCESS"


task_suite = create_task(testset_paths)
output_folder_name = os.path.abspath("..")

log_level = getattr(logging, "INFO")
logging.basicConfig(level=log_level)

report_name = '接口自动化测试报告'

kwargs = {
    "output": output_folder_name,
    "report_name": report_name,
    # "failfast": 'store_true'
}

result = PyUnitReport.HTMLTestRunner(**kwargs).run(task_suite)
results[testset_paths] = OrderedDict({
    "total": result.testsRun,
    "successes": len(result.successes),
    "failures": len(result.failures),
    "errors": len(result.errors),
    "skipped": len(result.skipped)
})

if len(result.successes) != result.testsRun:
    subject = "FAILED"


'''
测试环境host
'''
# 10.65.209.181 pay.shbank.com
# 10.65.1.16 funcpay.sina.com.cn
# 222.73.39.37 func2pay.sina.com.cn func2pay.sina.com.cn
# 22.73.39.40 static.pay.sina.com.cn
# 10.65.1.19 merchant.pay.sina.com.cn www.weicaifu.com pay.sina.com.cn fcw.pay.sina.com.cn js.weibopay.com css.weibopay.com i1.weibopay.com i3.weibopay.com i4.weibopay.com www.wexmoney.com m.weibopay.com pay.xlubank.com mpay.xlubank.com
# 10.65.1.19 pay.weibopay.com mpay.sina.com.cn




