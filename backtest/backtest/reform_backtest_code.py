import time
import inspect
import re



def _get_variebles(backtest_code):
    excluded_words = ["False", "class", "finally", "is", "return","None", "continue",
                      "for", "lambda","try","True", "def", "from", "nonlocal","while",
                      "and", "del", "global","not", "with","as", "elif", "if", "or", "yield",
                      "assert","else", "import","pass","break", "except","in", "raise"
                      "rqalpha","init","logger","info","context","XSHE","update_universe","before_trading",
                      "handle_bar","bar_dict"
    ]
    solved_words = [] # 已经处理完的words
    pattern = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
    match = pattern.findall(backtest_code)
    for va in match:
        if(va not in excluded_words and va not in solved_words):
            solved_words.append(va)
            yield va

def reform_backtest_code(backtest_code):
    '''
    修整回测代码。主要是处理未经声明的变量。
    '''
    reformed_code = backtest_code # 修改后的回测代码
    list_type_variables = {"closes": "closes = rqalpha.api.history_bars(order_book_id, %s, frequency, 'close')",
                          "highs": "highs = rqalpha.api.history_bars(order_book_id, %s, frequency, 'high')",
                            "opens": "highs = rqalpha.api.history_bars(order_book_id, %s, frequency, 'high')"}

    # setp 1: 找出所有变量名和关键字
    # setp 2: 从中去掉python关键字和无需处理的变量
    for veriable in _get_variebles(backtest_code):
        if(veriable in list_type_variables):
            # setp 3: 处理list类型的变量，得到list长度
            pattern = re.compile('%s\[([0-9]+)\]' %veriable)
            result = pattern.findall(backtest_code)
            #找出其中最大的数字，作为取数据的长度
            max=0 #数据的长度为max+1
            for i in result:
                i=int(i)
                if(i>max):
                    max = i
            # setp 4: 在list类型变量前添加相应的语句
            reformed_code = list_type_variables[veriable] %(max+1) + "\n" + reformed_code
        else:
            pass
    return reformed_code


    # setp 5: 在number类型变量前添加相应的语句

    return backtest_code

'''def save_code(file_name, backtest_code):
    with open(file_name,'w') as f:
        f.write(backtest_code)

def load_code(file_name):
    with open(file_name,'r') as f:
        return f.read()
'''
if __name__=="__main__":
    code = """
    from rqalpha.api import *


    def init(context):
        logger.info("init")
        context.s1 = "000001.XSHE"
        update_universe(context.s1)
        context.fired = False


    def before_trading(context):
        pass


    def handle_bar(context, bar_dict):
        closes[9] < opens[9]
        closes[100] = 10
        if not context.fired:
            # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
            order_percent(context.s1, 1)
            context.fired = True
    """
    print(reform_backtest_code(code))
    #file_name = 'backtest' + str(time.time()) + '.py'
