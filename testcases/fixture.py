import requests
from jsonpath import jsonpath
from common.handler_conf import conf


class BaseTest:

    @classmethod
    def admin_login(cls):
        url = conf.get('env', 'base_url') + '/member/login'
        # 管理员登陆
        params = {
            'mobile_phone': conf.get('test_data', 'admin_mobile'),
            'pwd': conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        admin_token = 'Bearer ' + jsonpath(res, '$..token')[0]
        headers['Authorization'] = admin_token
        cls.admin_member_id = jsonpath(res, '$..id')[0]
        cls.admin_headers = headers

    @classmethod
    def user_login(cls):
        url = conf.get('env', 'base_url') + '/member/login'
        # 普通用户登陆
        params = {
            'mobile_phone': conf.get('test_data', 'mobile'),
            'pwd': conf.get('test_data', 'pwd')
        }

        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        cls.token = jsonpath(res, '$..token')[0]
        headers['Authorization'] = 'Bearer ' + cls.token
        cls.member_id = jsonpath(res, '$..id')[0]
        cls.headers = headers

    @classmethod
    def add_project(cls):
        # 增加项目
        url = conf.get('env', 'base_url') + '/loan/add'
        params = {
            "member_id": cls.member_id,
            "title": "借钱现财富自由",
            "amount": 2000,
            "loan_rate": 12.0,
            "loan_term": 3,
            "loan_date_type": 1,
            "bidding_days": 5
        }
        response = requests.post(url=url, json=params, headers=cls.headers)
        res = response.json()
        cls.loan_id = jsonpath(res, '$..id')[0]

    @classmethod
    def audit(cls):
        # 审核项目
        url = conf.get('env', 'base_url') + '/loan/audit'
        params = {"loan_id": cls.loan_id,
                  "approved_or_not": True
                  }
        response = requests.patch(url=url,json=params,headers=cls.admin_headers)
