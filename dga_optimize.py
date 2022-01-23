from draw_DAG_ import draw
from my_create_DAG import create_DAG, optimize
from draw_DAG_ import draw
import middle_code_back as mc

op = ['=', '*', '/', '%' '+', '-', '<<', '>>', '<', '>', '<=', '>=', '==', '!=', '&', '^', '|', '&&', '||']

def transfer(s):
    '''
    把字符串的四元式转成list
    :param s:
    :return:
    '''
    res = []
    for line in s:
        res.append((line[0], line[1], line[2], line[3]))
    return res


def optimum(s):
    code = transfer(s)
    DAG = create_DAG(code)
    codes = optimize(DAG)
    draw(DAG)
    info = '\n'.join([','.join(c) for c in codes])
    c = info.split('\n')
    res = []
    for i in c:
        if i != '':
            a = i.split(',')
            res.append([a[0], a[1], a[2], a[3]])
        else:
            res.extend(s)
    return res


def creat_dag(block, four_formula):       #创建DAG
    op_block = []
    for i in block:
        op_part = optimum(i)
        op_block.append(op_part)
    return op_block
    #     fl = 0
    #     for j in range(len(i)):
    #         if i[j][0] == 'para':
    #             fl = 1
    #             break
    #     if fl == 1:
    #         continue
    #     for j in range(len(i)):
    #         if i[j][0] in op:
    #             start = j
    #             break
    #     for j in range(len(i)-1, -1, -1):
    #         if i[j][0] in op:
    #             end = j
    #             break
    #     if start == end:
    #         continue
    #     op_part = optimum(i[start: end])
    #     block_son = []
    #     block_son.extend(i[:start])
    #     block_son.append(op_part)
    #     block_son.append(i[end:])
    #     op_block.append(block_son)


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
    optime = creat_dag(block, four_formula)
    return optime


# jf = open('test.txt', 'r')
# s_f = jf.read()
# jf.close()
# mean_error, four_formula = mc.grammar_analysis(s_f)
# split_block(four_formula)