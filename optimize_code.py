import middle_code_back as mc
import re

op = ['=', '*', '/', '%' '+', '-', '<<', '>>', '<', '>', '<=', '>=', '==', '!=', '&', '^', '|', '&&', '||']

def check(str):     #检查是否含有字母
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if len(res):
        return True
    else:
        return False


def aculate(a, b, op1):     #计算出值
    if op1 == '*':
        return a * b
    elif op1 == '/':
        return a / b
    elif op1 == '%':
        return a % b
    elif op1 == '+':
        return a + b
    elif op1 == '-':
        return a - b
    elif op1 == '>>':
        return a >> b
    elif op1 == '<<':
        return a << b
    elif op1 == '>':
        return 1 if a > b else 0
    elif op1 == '<':
        return 1 if a < b else 0
    elif op1 == '>=':
        return 1 if a >= b else 0
    elif op1 == '<=':
        return 1 if a <= b else 0
    elif op1 == '!=':
        return 1 if a != b else 0
    elif op1 == '==':
        return 1 if a == b else 0
    elif op1 == '|':
        return a | b
    elif op1 == '&':
        return a & b
    elif op1 == '^':
        return a ^ b
    elif op1 == '&&':
        return 1 if a and b else 0
    elif op1 == '||':
        return 1 if a or b else 0



def spect(dag, s):      #检查s是否在dag中
    for i in dag:
        if s in i[0] or s in i[3]:
            return True
    else:
        return False


def add_nod(dag, s, v): #添加结点进附加符号表
    for i in range(len(dag)):
        if v in dag[i][0] or v in dag[i][3]:
            dag[i][0].append(s)
            break
    return dag


def creat_nod(dag, v, s, le, ri, pa):     #创建结点，值与附加符号
    nod = []    #该结点
    symbol = [s] #附加符号
    value = v   #值
    left = []   #左节点
    right =[]   #右节点
    parent = [] #父节点
    nod.extend([symbol, value, left, right, parent])
    if le != -1:
        left.append(le)
    if ri != -1:
        right.append(ri)
    if pa != -1:
        parent.append(pa)
    dag.append(nod)
    return dag


def traverse(s):
    if '.' in s:
        a = float(s)
    else:
        a = int(s)
    return a


def is_value(dag, s):   #如果发现另一个有值
    for i in dag:
        if s in i[0] and i[1] != '' and i[1] not in op:
            return True
    return False


def creat_little_dag(sentiment):        #优化一个小模块的dag
    dag = []
    for i in sentiment:
        if i[0] == '=':
            if spect(dag, i[1]):        #检查是否存在结点，有返回True,无返回False
                dag = add_nod(dag, i[3], i[1]) #添加结点进附加符号表
            else:
                dag = creat_nod(dag, i[1], i[3], -1, -1, -1)     #创建结点，值与附加符号,左、右、父结点
        else:   #a = b * c
            if not check(i[1]) and not check(i[2]): #b,c为常数，直接计算出来
                a = traverse(i[1])
                b = traverse(i[2])
                value = aculate(a, b, i[0])     #计算出值
                if spect(dag, value):  # 检查是否存在结点，有返回True,无返回False
                    dag = add_nod(dag, i[3], value)  # 添加结点进附加符号表
                else:
                    dag = creat_nod(dag, value, i[3], -1, -1, -1)  # 创建结点，值与附加符号,左、右、父结点
            elif not check(i[1]) and check(i[2]) and is_value(dag, i[2]):   #b为常数，c不为常数
                pass
            elif not check(i[2]) and check(i[1]) and is_value(dag, i[2]):  # c为常数，b不为常数
                pass
            else:   # c不为常数，b不为常数
                if not spect(dag, i[1]) and not spect(dag, i[2]):   #a,b不存在
                    dag = creat_nod(dag, '', i[1], -1, -1, len(dag)+2)  # 创建a结点，值与附加符号,左、右、父结点
                    dag = creat_nod(dag, '', i[2], -1, -1, len(dag)+1)  # 创建b结点，值与附加符号,左、右、父结点
                    dag = creat_nod(dag, i[0], i[3], len(dag)-2, len(dag)-1, -1)  # 创建b结点，值与附加符号,左、右、父结点
                elif spect(dag, i[1]) and not spect(dag, i[2]):
                    locate = get_locate(i[1])
                    dag = correct(dag, i[1], -1, -1, len(dag)+1)
                    dag = creat_nod(dag, '', i[2], -1, -1, len(dag) + 1)  # 创建b结点，值与附加符号,左、右、父结点
                    dag = creat_nod(dag, i[0], i[3], locate, len(dag) - 1, -1)  # 创建b结点，值与附加符号,左、右、父结点
                elif not spect(dag, i[1]) and spect(dag, i[2]):
                    locate = get_locate(i[2])
                    dag = correct(dag, i[2], -1, -1, len(dag) + 1)
                    dag = creat_nod(dag, '', i[1], -1, -1, len(dag) + 1)  # 创建b结点，值与附加符号,左、右、父结点
                    dag = creat_nod(dag, i[0], i[3], len(dag) - 1, locate, -1)  # 创建b结点，值与附加符号,左、右、父结点
                else:
                    pass



def creat_dag(block, four_formula):       #创建DAG
    op_block = []
    for i in block:
        fl = 0
        for j in range(len(i)):
            if i[j][0] == 'para':
                fl = 1
                break
        if fl == 1:
            continue
        for j in range(len(i)):
            if i[j][0] in op:
                start = j
                break
        for j in range(len(i)-1, -1, -1):
            if i[j][0] in op:
                end = j
                break
        if start == end:
            continue
        op_part = creat_little_dag(i[start: end])
        block_son = []
        block_son.extend(i[:start])
        block_son.append(op_part)
        block_son.append(i[end:])
        op_block.append(block_son)



def split_block(four_formula):      #传入四元式,划分基本块
    block = []
    entrance = [0]
    for i in range(len(four_formula)):
        if isinstance(four_formula[i][3], int): #添加转移语句转移到的地方为入口
            entrance.append(four_formula[i][3])
            if i + 1 < len(four_formula):   #添加转移语句后的语句为入口
                entrance.append(i + 1)
        if four_formula[i][0] not in ['ret', 'sys'] and four_formula[i][1] == '' and four_formula[i][2] == '' and four_formula[i][3] == '':#函数语句
            entrance.append(i)
    entrance = list(set(entrance))
    entrance.sort()
    i = 1
    while i < len(entrance):
        block_son = four_formula[entrance[i-1]: entrance[i]]
        i += 1
        block.append(block_son)
    if len(entrance) == 1:
        block.append(four_formula)
    creat_dag(block, four_formula)


jf = open('test.txt', 'r')
s_f = jf.read()
jf.close()
mean_error, four_formula = mc.grammar_analysis(s_f)
split_block(four_formula)
