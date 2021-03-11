import requests
import unittest
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
class Test_add(unittest.TestCase,BaseTest):
    data = do_excel(os.path.join(data_path,'api_data.xlsx'),'add')
    excel = data.read_excel()
    db = HandlerDB()
    @classmethod
    def setUpClass(cls):
        cls.user_login()

    @list_data(excel)
    def test_addp(self,item):
        url = conf.get('env','base_url')+ item['url']
        method = item['method']
        params = eval(replace_data(item['data'],Test_add))
        par_sign = HandleSign.generate_sign(self.token)
        params.update(par_sign)
        expected = eval(item['expected'])
        # 调用接口前查询该用户项目数量
        sql = "SELECT * FROM futureloan.loan WHERE member_id={}".format(self.member_id)
        strat_count = self.db.find_count(sql)
        print("调用接口之前的数量",strat_count)
        response = requests.request(url=url,method=method,json=params,headers=self.headers)
        res = response.json()
        end_count = self.db.find_count(sql)
        print("调用接口之后的数量",end_count)

        print("实际结果",res)
        print("预期结果",expected)
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if res['msg'] == 'OK':
                self.assertEqual(end_count-strat_count,1)
        except AssertionError as e:
            log.error("用例--【{}】---执行失败".format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info("用例--【{}】---执行成功".format(item['title']))

