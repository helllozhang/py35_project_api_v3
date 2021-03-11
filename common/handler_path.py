import os

# 获取当前文件的绝对路径
res = os.path.abspath(__file__)
# 获取当前文件的上级目录的路径
path1 = os.path.dirname(res)
# 在当前文件中获取项目的根目录
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取日志文件路径
log_path = os.path.join(base_path,'logs')
# 获取配置文件路径
conf_path = os.path.join(base_path,'conf')
# 获取测试报告路径
report_path = os.path.join(base_path,'reports')
# 获取测试用例路径
case_path = os.path.join(base_path,'testcases')
# 获取测试数据路径
data_path = os.path.join(base_path,'datas')


