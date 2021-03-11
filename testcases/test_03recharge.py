import unittest
import requests
import os
from unittestreport import ddt,list_data
from jsonpath import jsonpath
from common.handler_conf import conf
from common.handler_excel import do_excel
from common.handler_path import data_path
from common.handler_log import log
from common.handler_mysql import HandlerDB
from common.handler_re import replace_data
from testcases.fixture import BaseTest
from common.handler_sign import HandleSign

@ddt
class TestRecharge(unittest.TestCase,BaseTest):
    excel = do_excel(os.path.join(data_path,'api_data.xlsx'),'recharge')
    cases = excel.read_excel()
    db = HandlerDB()
    @classmethod
    def setUpClass(cls):
        # """用例类得前置方法,登陆提取token"""
        # # 1. 请求登陆接口,进行登陆
        # url = conf.get('env','base_url')+ '/member/login'
        # params ={
        #     'mobile_phone':conf.get('test_data','mobile'),
        #     'pwd':conf.get('test_data','pwd')
        # }
        # headers = eval(conf.get('env','headers'))
        # response = requests.post(url=url,json=params,headers=headers)
        # res = response.json()
        # # 2.登陆成功提取id和token
        # token = jsonpath(res,'$..token')[0]
        # # 将token添加到请求头重
        # headers['Authorization'] ='Bearer '+token
        # # 保存含有token得请求头为类属性
        # cls.headers = headers
        # # setattr(TestRecharge,'headers',headers)
        # # 3.提取用户id
        # cls.member_id = jsonpath(res,'$..id')[0]
        cls.user_login()


    @list_data(cases)
    def test_recharge(self,item):
        # 第一步准备数据
        url = conf.get('env','base_url') + item['url']
        # 动态处理需要替换得参数
        item['data'] = replace_data(item['data'],TestRecharge)
        params = eval(item['data'])
        par_sign = HandleSign.generate_sign(self.token)
        params.update(par_sign)
        expected = eval(item['expected'])
        method = item['method'].lower()
        # -------------请求之前获取数据库中用户余额--------------
        sql = "select leave_amount from futureloan.member where mobile_phone='{}'".format(conf.get('test_data', 'mobile'))
        #执行查询sql
        start_amount = self.db.find_one(sql)[0]
        print("用例执行前余额：{}".format(start_amount))

        # 第二步发送请求获取实际结果
        response = requests.request(method,url,json=params,headers=self.headers)
        res = response.json()
        # -------------请求接口之后获取数据库中用户余额--------------
        end_amount = self.db.find_one(sql)[0]
        print("用例执行后余额：{}".format(start_amount))
        # assert
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            # -------------校验数据库中用户余额的变化是否等于充值金额--------------
            if item['check_sql']:
                # 充值成功，用户余额变化为充值金额
                self.assertEqual(float(end_amount-start_amount),params['amount'])
            else:
                self.assertEqual(float(end_amount-start_amount),0)
        except AssertionError as e:
            log.error("用例--【{}】---执行失败".format(item['title']))
            log.exception(e)
            raise e
        else:
            log.info("用例--【{}】---执行成功".format(item['title']))
