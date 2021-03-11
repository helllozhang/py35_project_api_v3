import requests
import unittest
import os
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handler_conf import conf
from common.handler_excel import do_excel
from common.handler_path import data_path
from common.handler_log import log
from common.handler_mysql import HandlerDB
from common.handler_re import replace_data
from common.handler_sign import HandleSign
from testcases.fixture import BaseTest

@ddt
class TestWithdraw(unittest.TestCase,BaseTest):
    excel = do_excel(os.path.join(data_path,'api_data.xlsx'),'withdraw')
    cases = excel.read_excel()
    db = HandlerDB()
    @classmethod
    def setUpClass(cls):
        cls.user_login()
    @list_data(cases)
    def test_withdraw(self,item):
        url = conf.get('env','base_url')+ item['url']
        method = item['method'].lower()
        item['data'] = replace_data(item['data'],TestWithdraw)
        params = eval(item['data'])
        par_sign = HandleSign.generate_sign(self.token)
        params.update(par_sign)
        expected = eval(item['expected'])
        # --------请求接口前，查看用户余额--------
        sql =  "select leave_amount from futureloan.member where mobile_phone='{}'".format(conf.get('test_data', 'mobile'))
        start_wd = self.db.find_one(sql)[0]
        print("提现前用户余额为:{}".format(start_wd))
        response = requests.request(method,url,json=params,headers=self.headers)
        res = response.json()
        # --------请求接口后，查看用户余额--------
        end_wd = self.db.find_one(sql)[0]
        print("提现后用户余额为:{}".format(end_wd))
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if item['check_sql']:
                # 提现成功
                self.assertEqual(float(start_wd-end_wd),params['amount'])
            else:
                self.assertEqual(float(start_wd-end_wd),0)
        except AssertionError as e:
            log.error("用例--【{}】---执行失败".format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info("用例--【{}】---执行成功".format(item['title']))