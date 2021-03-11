import unittest
import os
import requests
import random
from unittestreport import ddt,list_data
from common.handler_excel import do_excel
from common.handler_path import data_path
from common.handler_conf import conf
from common.handler_log import log
from common.handler_mysql import HandlerDB
from common.handler_re import replace_data

@ddt
class TestRegister(unittest.TestCase):
    excel = do_excel(os.path.join(data_path,'api_data.xlsx'),'register')
    db = HandlerDB()
    # 读取用例数据
    cases = excel.read_excel()
    # 项目地址
    base_url = conf.get('env','base_url')
    # 请求头
    headers = eval(conf.get('env','headers'))
    @list_data(cases)
    def test_register(self,itme):
        # 第一步:准备用例数据
        # 1.接口地址
        url = self.base_url+itme['url']
        # 2.请求参数
        if '#mobile#' in itme['data']:
            setattr(TestRegister,'mobile',self.ran_phone())
            itme['data'] = replace_data(itme['data'],TestRegister)
        params = eval(itme['data'])
        print(params)
        # 3.请求头
        # 4.获取请求方法,转换为小写
        method = itme['method'].lower()
        # 5.预期结果
        expected = eval(itme['expected'])

        # --------请求接口前，查看是否注册改手机号--------
        sql = "select * from futureloan.member where mobile_phone ='{}';".format(params['mobile_phone'])
        res1 = self.db.find_count(sql)
        print("{}请求接口前注册结果{}".format(params['mobile_phone'],res1))
        # 第二步:请求接口,返回实际结果
        response = requests.request(method,url,json=params,headers=self.headers)
        res = response.json()
        # --------请求接口后，查看是否注册改手机号--------
        res2 = self.db.find_count(sql)
        print("{}请求接口前注册结果{}".format(params['mobile_phone'],res2))
        # 第三步:断言
        try:
            # 断言code和msg是否一致
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if itme['check_sql']:
                # 注册成功，可以查到一条数据
                self.assertEqual(res2,1)
        except AssertionError as e:
            # 记录日志
            log.error("用例--【{}】---执行失败".format(itme['title']))
            log.exception(e)
            # 回写结果到excel(根据需求,回写需花费大量时间)
            raise e
        else:
            log.info("用例--【{}】---执行成功".format(itme['title']))

    def ran_phone(self):
        phone = str(random.randint(13300000000,13399999999))
        return phone