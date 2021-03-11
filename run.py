from unittestreport import TestRunner
from common.handler_path import os,case_path,report_path
import unittest
suite = unittest.defaultTestLoader.discover(os.path.join(case_path))
runner = TestRunner(suite,os.path.join(report_path,'report.html'),tester='小菜鸡')
runner.run()



