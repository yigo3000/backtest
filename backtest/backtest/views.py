from django.shortcuts import render
from django.http import HttpResponse
import threading
from rqalpha import run_code
import time
import inspect
import pickle
import pandas
import json
from django.views.decorators.csrf import csrf_exempt
pandas.set_option('display.max_rows',None)

class _backtest_Thread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, test_code, config):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.test_code = test_code
        self.confit = config

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        run_code(self.code, self.config)



# Create your views here.
'''
def start_backtest(request):
    request.encoding = 'utf-8'
    if request.method == "POST" or request.method == "OPTIONS":
        message = '你发了个post:' + request.POST['backtest_code']
    else:
        message = '你提交了空post'

    # 保存文件
    test_code = request.POST['backtest_code']
    test_code = reform_backtest_code(test_code)
    file_name = 'backtest'+str(time.time())+'.py'
    with open(file_name,'w') as f:
        f.write(test_code)

    # 获取配置
    config = request.POST['backtest_config']
    # 进行回测
    new_backtest = _backtest_Thread(0, test_code, config)
    new_backtest.start()

    return HttpResponse(message)
'''


def _load_benchmark_portfolio_unit_net_value(file_name):
    with open(file_name, 'rb') as f:
        report = pickle.load(f)
        x_axis = '['
        for tmp in report['benchmark_portfolio'].index:
            x_axis += '"' + str(tmp) + '"' + ', '
        x_axis = x_axis[:-2] + ']'
        y_axis = '['
        for tmp in report['benchmark_portfolio']['unit_net_value']:
            y_axis += str(tmp) + ', '
        y_axis = y_axis[:-3] + ']'
        response_json = '"benchmark_portfolio.unit_net_value":{"time":' + x_axis + ',\n"data":' + y_axis + '}'
        return response_json
def _load_portfolio_unit_net_value(file_name):
    with open(file_name, 'rb') as f:
        report = pickle.load(f)
        x_axis = '['
        for tmp in report['portfolio'].index:
            x_axis += '"' + str(tmp) + '"' + ', '
        x_axis = x_axis[:-2] + ']'
        y_axis = '['
        for tmp in report['portfolio']['unit_net_value']:
            y_axis += str(tmp) + ', '
        y_axis = y_axis[:-3] + ']'
        response_json = '"portfolio_unit_net_value":{"time":' + x_axis + ',\n"data":' + y_axis + '}'
    return response_json

def _load_portfolio_delt_day_value(file_name):
    with open(file_name, 'rb') as f:
        report = pickle.load(f)
        x_axis = '['
        for tmp in report['portfolio'].index:
            x_axis += '"' + str(tmp) + '"' + ', '
        x_axis = x_axis[:-2] + ']'
        y_axis = '['
        for i in range(report['portfolio'].index.size):
            if i == 0:
                tmp = 0
            else:
                tmp = report['portfolio'].iloc[i, 3] - report['portfolio'].iloc[i - 1, 3]
            y_axis += str(tmp) + ','
        y_axis = y_axis[:-1] + ']'
        response_json = '"portfolio_delt_day_value":{"time":' + x_axis + ',\n"data":' + y_axis + '}'
        return response_json
def _load_summary(file_name):
    with open(file_name, 'rb') as f:
        report = pickle.load(f)
        response_json = '"summary":{'
        for tmp in report['summary']:
            response_json += '"' + tmp + '":"' + str(report['summary'][tmp]) + '",\n'
        response_json = response_json[0:-2] + '}'
    return response_json

def _load_trades(file_name):
    with open(file_name, 'rb') as f:
        report = pickle.load(f)
        tmp = '"trades":{'
        for i in range(report['trades'].index.size):
            tmp += '"' + report['trades'].index[i] + '":{'  # 时间
            for j in range(report['trades'].columns.size):
                tmp += '"' + report['trades'].columns[j] + '":"' + str(report['trades'].iloc[i, j]) + '",'  #
            tmp = tmp[:-1] + '},\n'
        tmp = tmp[:-2] + '}'
    return tmp

@csrf_exempt
def get_result(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        # if(request.POST['user id']=='demo' and request.POST['test id']=='demo'):
        body = json.loads(str(request.body, encoding="utf-8"))
        if (body['user id'] == 'demo' and body['test id'] == 'demo'):
            response_json = '{'+_load_benchmark_portfolio_unit_net_value('report.pkl')+',\n'
            response_json += _load_portfolio_unit_net_value('report.pkl') +',\n'
            response_json += _load_portfolio_delt_day_value('report.pkl') +',\n'
            response_json += _load_summary('report.pkl') +',\n'
            response_json += _load_trades('report.pkl') + '}'
            print(response_json)
            return HttpResponse(response_json)

@csrf_exempt
def benchmark_portfolio_unit_net_value(request):
    request.encoding = 'utf-8'
    if request.method == "POST" or request.method == "OPTIONS":
        # if(request.POST['user id']=='demo' and request.POST['test id']=='demo'):
        body = json.loads(str(request.body, encoding="utf-8"))
        if (body['user id'] == 'demo' and body['test id'] == 'demo'):
            with open('report.pkl','rb') as f:
                report = pickle.load(f)
                x_axis = '['
                for tmp in report['benchmark_portfolio'].index:
                    x_axis += '"' + str(tmp) + '"' + ', '
                x_axis = x_axis[:-2] + ']'
                y_axis = '['
                for tmp in report['benchmark_portfolio']['unit_net_value']:
                    y_axis += str(tmp) + ', '
                y_axis = y_axis[:-3] + ']'
                response_json = '{"time":' + x_axis + ',\n"data":' + y_axis + '}'
                print(response_json)
            return HttpResponse(response_json)


@csrf_exempt
def portfolio_unit_net_value(request):
    request.encoding = 'utf-8'
    if request.method == "POST" or request.method == "OPTIONS":
        #if(request.POST['user id']=='demo' and request.POST['test id']=='demo'):
        body = json.loads(str(request.body, encoding = "utf-8"))
        if(body['user id']=='demo' and body['test id']=='demo'):
            with open('report.pkl','rb') as f:
                report = pickle.load(f)
                x_axis = '['
                for tmp in report['portfolio'].index:
                    x_axis += '"' + str(tmp) + '"' + ', '
                x_axis = x_axis[:-2] + ']'
                y_axis = '['
                for tmp in report['portfolio']['unit_net_value']:
                    y_axis += str(tmp) + ', '
                y_axis = y_axis[:-3] + ']'
                response_json = '{"time":' + x_axis + ',\n"data":' + y_axis + '}'
                print(response_json)
            return HttpResponse(response_json)
@csrf_exempt
def portfolio_delt_day_value(request):
    request.encoding = 'utf-8'
    if request.method == "POST" or request.method == "OPTIONS":
        # if(request.POST['user id']=='demo' and request.POST['test id']=='demo'):
        body = json.loads(str(request.body, encoding="utf-8"))
        if (body['user id'] == 'demo' and body['test id'] == 'demo'):
            with open('report.pkl','rb') as f:
                report = pickle.load(f)
                x_axis = '['
                for tmp in report['portfolio'].index:
                    x_axis += '"' + str(tmp) + '"' + ', '
                x_axis = x_axis[:-2] + ']'
                y_axis = '['
                for i in range(report['portfolio'].index.size):
                    if i == 0:
                        tmp = 0
                    else:
                        tmp = report['portfolio'].iloc[i, 3] - report['portfolio'].iloc[i - 1, 3]
                    y_axis += str(tmp) + ','
                y_axis = y_axis[:-1]+']'
                response_json = '{"time":' + x_axis + ',\n"data":' + y_axis + '}'
                print(response_json)
            return HttpResponse(response_json)

@csrf_exempt
def summary(request):
    request.encoding = 'utf-8'
    if request.method == "POST" or request.method == "OPTIONS":
        # if(request.POST['user id']=='demo' and request.POST['test id']=='demo'):
        body = json.loads(str(request.body, encoding="utf-8"))
        if (body['user id'] == 'demo' and body['test id'] == 'demo'):
            with open('report.pkl','rb') as f:
                report = pickle.load(f)
                response_json = '{'
                for tmp in report['summary']:
                    response_json += '"' + tmp + '":"' + str(report['summary'][tmp]) + '",\n'
                response_json = response_json[0:-2] + '}'
            return HttpResponse(response_json)

@csrf_exempt
def trades(request):
    request.encoding = 'utf-8'
    if request.method == "POST" or request.method == "OPTIONS":
        # if(request.POST['user id']=='demo' and request.POST['test id']=='demo'):
        body = json.loads(str(request.body, encoding="utf-8"))
        if (body['user id'] == 'demo' and body['test id'] == 'demo'):
            with open('report.pkl','rb') as f:
                report = pickle.load(f)
                tmp = '{'
                for i in range(report['trades'].index.size):
                    tmp += '"' + report['trades'].index[i] + '":{'  # 时间
                    for j in range(report['trades'].columns.size):
                        tmp += '"' + report['trades'].columns[j] + '":"' + str(report['trades'].iloc[i, j]) + '",'  #
                    tmp = tmp[:-1] + '},\n'
                tmp = tmp[:-2] + '}'
                print(tmp)
            return HttpResponse(tmp)
