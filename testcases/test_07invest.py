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
class Test_invest(unittest.TestCase,BaseTest):
    excel = do_excel(os.path.join(data_path,'api_data.xlsx'),'invest')
    case = excel.read_excel()
    db = HandlerDB()

    @classmethod
    def setUpClass(cls):
        # 管理员登陆
        cls.admin_login()
        # 普通用户登陆
        cls.user_login()
        # 增加项目
        cls.add_project()
        # 审核项目
        cls.audit()

    @list_data(case)
    def test_invest(self,item):
        # 准备数据
        url = conf.get('env', 'base_url') + item['url']
        item['data'] = replace_data(item['data'], Test_invest)
        params = eval(item['data'])
        par_sign = HandleSign.generate_sign(self.token)
        params.update(par_sign)
        method = item['method'].lower()
        expected = eval(item['expected'])
        # ----------------投资前查询数据库---------------------------------
        # 查用户表的sql
        sql1 = 'SELECT leave_amount FROM futureloan.member WHERE id="{}"'.format(self.member_id)
        # 查投资记录的sql
        sql2 = 'SELECT id FROM futureloan.invest WHERE member_id="{}"'.format(self.member_id)
        # 查流水记录的sql
        sql3 = 'SELECT id FROM futureloan.financelog WHERE pay_member_id="{}"'.format(self.member_id)
        #
        if item['check_sql']:
            s_amount = self.db.find_one(sql1)[0]
            s_invest = self.db.find_count(sql2)
            s_financelog = self.db.find_count(sql3)
        # 发送请求
        response = requests.request(url=url, method=method, json=params, headers=self.headers)
        res = response.json()
        # -------------------投资后查询数据库--------------------------------
        if item['check_sql']:
            e_amount = self.db.find_one(sql1)[0]
            e_invest = self.db.find_count(sql2)
            e_financelog = self.db.find_count(sql3)
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            # 断言实际结果中的msg是否包含 预期结果msg中的内容
            if item['check_sql']:
                # 断言用户余额
                self.assertEqual(params['amount'], float(s_amount - e_amount))
                # 断言投资记录
                self.assertEqual(1, e_invest-s_invest)
                # 断言流水记录
                self.assertEqual(1, e_financelog - s_financelog)

        except AssertionError as e:
            log.error("用例--【{}】---执行失败".format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info("用例--【{}】---执行成功".format(item['title']))
