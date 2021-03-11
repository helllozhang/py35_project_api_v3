import unittest
import requests
import os
from unittestreport import ddt,list_data
from common.handler_excel import do_excel
from common.handler_path import data_path
from common.handler_conf import conf
from common.handler_log import log
from common.handler_re import replace_data


@ddt
class TestLogin(unittest.TestCase):
    excel = do_excel(os.path.join(data_path,'api_data.xlsx'),'login')
    data = excel.read_excel()
    base_url = conf.get('env','base_url')
    headers = eval(conf.get('env','headers'))
    @list_data(data)
    def test_login(self,itme):
        url = self.base_url+ itme['url']
        method = itme['method'].lower()
        itme['data'] = replace_data(itme['data'],TestLogin)
        param = eval(itme['data'])
        expected = eval(itme['expected'])
        # 请求接口获取实际结果
        response = requests.request(method,url,json=param,headers=self.headers)
        res = response.json()
        #断言
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
        except AssertionError as e:
            log.error("用例--【{}】---执行失败".format(itme['title']))
            log.exception(e)
            raise e
        else:
            log.info("用例--【{}】---执行成功".format(itme['title']))
