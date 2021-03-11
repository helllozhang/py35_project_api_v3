import unittest
import requests
import os
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handler_conf import conf
from common.handler_excel import do_excel
from common.handler_path import data_path
from common.handler_re import replace_data
from common.handler_log import log
from common.handler_mysql import HandlerDB
from common.handler_sign import HandleSign
from testcases.fixture import BaseTest

@ddt
class TestAudit(unittest.TestCase,BaseTest):
    excel = do_excel(os.path.join(data_path,'api_data.xlsx'),'audit')
    case = excel.read_excel()
    db = HandlerDB()
    @classmethod
    def setUpClass(cls):
        # 管理员登陆
        cls.admin_login()

        # 普通用户登陆
        cls.user_login()
    @classmethod
    def setUp(self):
        self.add_project()

    @list_data(case)
    def test_audit(self,item):
        url = conf.get('env','base_url')+ item['url']
        item['data'] = replace_data(item['data'],TestAudit)
        params = eval(item['data'])
        par_sign = HandleSign.generate_sign(self.token)
        params.update(par_sign)
        method = item['method'].lower()
        expected = eval(item['expected'])
        response = requests.request(url=url,method=method,json=params,headers=self.admin_headers)
        res = response.json()
        if res['msg'] == 'OK' and item['title'] == '审核通过':
            TestAudit.pass_loan_id = params['loan_id']
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if item['check_sql']:
                sql =  item['check_sql'].format(self.loan_id)
                status = self.db.find_one(sql)[0]
                print("数据库中的状态:",status)
                self.assertEqual(expected['status'],status)
        except AssertionError as e:
            log.error("用例--【{}】---执行失败".format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info("用例--【{}】---执行成功".format(item['title']))