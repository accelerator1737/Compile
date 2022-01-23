import re
import tkinter as tk
from graphviz import Digraph
import copy

space = 'ε'
def check_string(s_re):  #验证正则表达式是否正确
    try:
        re.compile(s_re)
        return True
    except:
        return False


def add_point(s):#为表达式添加结合运算符，即点.
    ret = ''
    kuo = ['(', ')', '*', '|']
    for i in range(len(s)):
        ret += s[i]
        if i+1 < len(s) and ((s[i] not in kuo and s[i+1] not in kuo) or(s[i] == ')' and s[i+1] == '(') or (s[i] == ')'
                    and s[i+1] not in kuo) or (s[i] == '*' and
                                               s[i+1] != '|' and s[i+1] != ')') or (s[i] not in kuo and s[i+1] == '(')):
            ret += '.'
    return ret


def mid2pos(expression): #中缀表达式转后缀表达式
    operator_stack = []
    postfix = []
    kuo = ['(', ')', '*', '|', '.']
    dec = {}
    dec['*'] = 2
    dec['.'] = 1
    dec['|'] = 1
    dec['('] = 0
    expression_list = list(expression)
    for i in range(0, len(expression_list)):
        if expression_list[i] not in kuo:
            postfix.append(expression_list[i])
        elif expression_list[i] == '(':
            operator_stack.append(expression_list[i])
        elif expression_list[i] == ')':
            top_token = operator_stack.pop()
            postfix.append(top_token)
            while len(operator_stack) != 0 and top_token != '(':
                top_token = operator_stack.pop()
                if top_token != '(':
                    postfix.append(top_token)
        else:
            if len(operator_stack) != 0 and dec[expression_list[i]] <= dec[operator_stack[len(operator_stack) - 1]]:
                while len(operator_stack) != 0 and dec[expression_list[i]] <= dec[operator_stack[len(operator_stack)-1]]:
                    postfix.append(operator_stack.pop())
            operator_stack.append(expression_list[i])
    while not len(operator_stack) == 0:
        postfix.append(operator_stack.pop())
    return "".join(postfix)


def xing_element(res, n): #进行*运算
    start = res[0][0]
    end = res[0][1]
    if start == end:
        s = res[0][2]
        res.append([n + 1, s, n + 2])
        res.append([n + 2, space, n + 1])
        res.append([n, space, n + 1])
        res.append([n + 2, space, n + 3])
        res.append([n, space, n + 3])
        res[0][0] = n
        n += 3
        res[0][1] = n
    else:
        res.append([end, space, start])
        res.append([n, space, start])
        res.append([end, space, n + 1])
        res.append([n, space, n + 1])
        res[0][0] = n
        res[0][1] = n + 1
        n += 1
    return res, n


def huo(r1, r2, n):     #进行或运算
    res = []
    if r1[0][0] == r1[0][1] and r2[0][0] == r2[0][1]:
        res.append([n + 1, n + 6])
        res.append([n + 1, space, n + 2])
        res.append([n + 1, space, n + 3])
        res.append([n + 2, r1[0][2], n + 4])
        res.append([n + 3, r2[0][2], n + 5])
        res.append([n + 4, space, n + 6])
        res.append([n + 5, space, n + 6])
        n += 6
    elif r1[0][0] != r1[0][1] and r2[0][0] != r2[0][1]:
        res.append([n + 1, n + 2])
        res.append([n + 1, space, r1[0][0]])
        res.append([n + 1, space, r2[0][0]])
        res.append([r1[0][1], space, n + 2])
        res.append([r2[0][1], space, n + 2])
        res.extend(r1[1:])
        res.extend(r2[1:])
        n += 2
    elif r1[0][0] == r1[0][1] and r2[0][0] != r2[0][1]:
        res.append([n + 1, n + 4])
        res.append([n + 1, space, n + 2])
        res.append([n + 1, space, r2[0][0]])
        res.append([n + 3, space, n + 4])
        res.append([r2[0][1], space, n + 4])
        res.append([n + 2, r1[0][2], n + 3])
        res.extend(r2[1:])
        n += 4
    elif r1[0][0] != r1[0][1] and r2[0][0] == r2[0][1]:
        res.append([n + 1, n + 4])
        res.append([n + 1, space, n + 2])
        res.append([n + 1, space, r1[0][0]])
        res.append([n + 3, space, n + 4])
        res.append([r1[0][1], space, n + 4])
        res.append([n + 2, r2[0][2], n + 3])
        res.extend(r1[1:])
        n += 4
    return res, n


def dian(r1, r2, n):        #进行结合运算,r1在前
    res = []
    if r1[0][0] == r1[0][1] and r2[0][0] == r2[0][1]:
        res.append([n + 1, n + 3])
        res.append([n + 1, r1[0][2], n + 2])
        res.append([n + 2, r2[0][2], n + 3])
        n += 3
    elif r1[0][0] == r1[0][1] and r2[0][0] != r2[0][1]:
        start = r2[0][0]
        end = r2[0][1]
        res.append([n + 1, end])
        res.append([n + 1, r1[0][2], start])
        res.extend(r2[1:])
        n += 1
    elif r1[0][0] != r1[0][1] and r2[0][0] == r2[0][1]:
        start = r1[0][0]
        end = r1[0][1]
        res.append([start, n + 1])
        res.append([end, r2[0][2], n + 1])
        res.extend(r1[1:])
        n += 1
    elif r1[0][0] != r1[0][1] and r2[0][0] != r2[0][1]:
        start1 = r1[0][0]
        end1 = r1[0][1]
        start2 = r2[0][0]
        end2 = r2[0][1]
        res.append([start1, end2])
        res.append([end1, space, start2])
        res.extend(r1[1:])
        res.extend(r2[1:])
    return res, n


def pos2nfa(p):    #后缀表达式转nfa
    result_stack = []
    operation = ['*', '.', '|']
    res = []
    num = -2
    for i in range(len(p)):
        if p[i] not in operation:
            res = [[num, num, p[i]]]
            result_stack.append(res)
        elif p[i] == '*':
            now = result_stack.pop()
            res, num = xing_element(now, num + 1)
            result_stack.append(res)
        elif p[i] == '|':
            now1 = result_stack.pop()
            now2 = result_stack.pop()
            res, num = huo(now2, now1, num)
            result_stack.append(res)
        elif p[i] == '.':
            now1 = result_stack.pop()
            now2 = result_stack.pop()
            res, num = dian(now2, now1, num)
            result_stack.append(res)
    return res


def draw_generate(r, points):   #生成图片
    g = Digraph(format='jpg')
    for i in range(len(points)):
        if points[i] == 'Y':
            g.node(str(points[i]), str(points[i]), shape='doublecircle')
        else:
            g.node(str(points[i]), str(points[i]), shape='circle')
    for i in r:
        g.edge(str(i[0]), str(i[2]), i[1])
    # g.attr(layout='neato')
    g.view()


def deep(r):#深搜解决标号
    start = r[0][0]
    end = r[0][1]
    node = []
    all = []
    node.append(start)
    all.append(start)
    while len(node) != 0:
        now = node.pop(0)
        for j in range(1, len(r)):
            if r[j][0] == now and r[j][2] not in all:
                node.append(r[j][2])
                all.append(r[j][2])
    all.remove(end)
    all.append(end)

    # temp = copy.deepcopy(r)
    # for i in range(len(all)):
    #     for j in range(1, len(r)):
    #         if temp[j][0] == all[i]:
    #             r[j][0] = i - 1
    #         if temp[j][2] == all[i]:
    #             r[j][2] = i - 1

    n = len(all) - 2
    temp = copy.deepcopy(r)
    for j in range(1, len(r)):
        if temp[j][0] == start:
            r[j][0] = 'X'
        elif temp[j][0] == end:
            r[j][0] = 'Y'
        if temp[j][2] == start:
            r[j][2] = 'X'
        elif temp[j][2] == end:
            r[j][2] = 'Y'
    all.remove(start)
    all.remove(end)
    all.append('X')
    all.append('Y')
    return r[1:], all


def closure(r, s):#进行Closure计算
    res = []
    res.extend(s)
    stack = s
    while len(stack) != 0:
        now = stack.pop()
        for i in r:
            if i[0] == now and i[1] == space and i[2] not in res:
                stack.append(i[2])
                res.append(i[2])
    return res


def move(r, s, e):  #进行move操作
    res = []
    for i in r:
        if i[0] in s and i[1] == e:
            res.append(i[2])
    return res


def nfa2dfa(r, k): #NFA 转 DFA
    table = []
    rs = []
    dfa = []
    zhong = []      #最终态
    for i in range(len(k) + 1):
        co = []
        table.append(co)
        co1 = []
        rs.append(co1)
    init = ['X']
    c = closure(r, init)
    table[0].append(c)
    i = 0
    while len(table[0]) != len(table[1]):
        init = table[0][i]
        i += 1
        for j in range(len(k)):
            m = move(r, init, k[j])
            c = closure(r, m)
            table[j+1].append(c)
            if c not in table[0]:
                table[0].append(c)
    dic = {}
    n = -1
    for i in range(len(table)):
        for j in table[i]:
            kk = str(j)
            if kk not in dic:
                dic[kk] = n
                n += 1
    for i in range(len(table[0])):
        for j in range(1, len(table)):
            if 'Y' in str(table[j][i]) and dic[str(table[j][i])] not in zhong:
                zhong.append(dic[str(table[j][i])])
            dfa.append([dic[str(table[0][i])], k[j-1], dic[str(table[j][i])]])
    # for i in dfa:
    #     if i[0] == -1:
    #         i[0] = 'X'
    #     if i[2] == -1:
    #         i[2] = 'X'
    point = list(dic.values())
    # point.remove(-1)
    # point.append('X')
    if '[]' in dic:
        shan = dic['[]']
        j = 0
        while j < len(dfa):
            if dfa[j][0] == shan or dfa[j][2] == shan:
                dfa.pop(j)
            else:
                j += 1
        point.remove(shan)
    return dfa, zhong, point    #返回dfa边以及终态结点，所有节点


def can(posfix):    #统计参数的多少
    fei = ['.', '*', '|']
    li = []
    for i in posfix:
        if i not in li and i not in fei:
            li.append(i)
    return li


def draw_dfa(r, last, points):    #画出dfa
    g = Digraph(format='jpg')
    for i in range(len(points)):
        if points[i] in last:
            g.node(str(points[i]), str(points[i]), shape='doublecircle')
        else:
            g.node(str(points[i]), str(points[i]), shape='circle')
    for i in r:
        g.edge(str(i[0]), str(i[2]), i[1])
    # g.attr(layout='neato')
    g.view()


def draw_mfa(r, last, points):    #画出dfa
    g = Digraph(format='jpg')
    for i in range(len(points)):
        if points[i] in last:
            g.node(str(points[i]), str(points[i]), shape='doublecircle')
        else:
            g.node(str(points[i]), str(points[i]), shape='circle')
    for i in r:
        g.edge(str(i[0]), str(i[2]), i[1])
    g.attr(layout='neato')
    g.view()


def fenli(now, dui, group, li, temp):    #将相同的分离开来
    zong = []
    already = []
    all = []
    all.extend(group)
    all.extend(li)
    all.extend(temp)
    all.append(now)
    correspond = []
    for i in all:
        if len(i) == 0:
            all.remove(i)
    for i in range(len(dui)):
        for j in range(len(all)):
            if dui[i] in all[j]:
                correspond.append(j)
    for i in range(len(correspond)):
        same = correspond[i]
        tong = []
        tong.append(now[i])
        for j in range(i+1, len(correspond)):
            if correspond[j] == same:
                tong.append(now[j])
        if same not in already:
            zong.append(tong)
            already.append(same)
    return zong


def find_mfa(d, group, last):    #从合并的状态中找到
    eventual = []
    n = 0
    if len(group) == 0:
        eventual.extend(last)
    else:
        for i in range(len(group)): #找到终态
            for j in group[i]:
                if j in last:
                    eventual.append(i)
                    break
            if -1 not in group[i]:
                n += 1
    n = 0
    now = n
    topu = copy.deepcopy(d)
    for i in range(len(group)):
        if -1 not in group[i]:
            now = n
        else:
            now = -1
        for j in group[i]:
            for k in range(len(d)):
                if d[k][0] == j:
                    topu[k][0] = now
                if d[k][2] == j:
                    topu[k][2] = now
        if -1 not in group[i]:
            n += 1
    xin = []
    for i in topu:
        if i not in xin:
            xin.append(i)
    return xin, eventual


def dfa2mfa(d, last, points, k):
    group = []
    group.append(last)
    group.append([x for x in points if x not in last])
    li = []
    temp = []
    temp.extend(group)
    group = []
    for o in k:
        li = temp
        temp = []
        while len(li) != 0:
            now = li.pop()
            dui = [' '] * len(now)
            for i in range(len(now)):   #每个要遍历的点
                for j in d: #每一条边的去查看
                    if now[i] == j[0] and j[1] == o:
                        dui[i] = j[2]
            sr = fenli(now, dui, group, li, temp)    #传入要分离的集合以及对应元素的下一个转换态
            for i in sr:
                if len(i) == 1:
                    group.append(i)
                else:
                    temp.append(i)
    if len(temp) != 0:
        group.extend(temp)  #得到分离后的状态
    mfa, eventual = find_mfa(d, group, last)   #找到dfa
    points_mfa = []
    for i in mfa:
        if i[0] not in points_mfa:
            points_mfa.append(i[0])
        if i[2] not in points_mfa:
            points_mfa.append(i[2])

    return mfa, eventual, points_mfa


def generate_nfa_image(st): #生成nfa图像
    st_point = add_point(st)  # st添加结合运算符
    posfix = mid2pos(st_point)  # 得到后缀表达式
    r = pos2nfa(posfix)
    r, points = deep(r)  # 改变数字顺序
    draw_generate(r, points)  # 生成图片


def generate_dfa_image(st): #生成dfa图像
    st_point = add_point(st)  # st添加结合运算符
    posfix = mid2pos(st_point)  # 得到后缀表达式
    parses = can(posfix)  # 算出式子中参数的个数
    r = pos2nfa(posfix)
    r, points = deep(r)  # 改变数字顺序
    dfa, last, dfa_point = nfa2dfa(r, parses)  # 转为dfa
    draw_dfa(dfa, last, dfa_point)


def generate_mfa_image(st): #生成mfa图像
    st_point = add_point(st)  # st添加结合运算符
    posfix = mid2pos(st_point)  # 得到后缀表达式
    parses = can(posfix)  # 算出式子中参数的个数
    r = pos2nfa(posfix)
    r, points = deep(r)  # 改变数字顺序
    dfa, last, dfa_point = nfa2dfa(r, parses)  # 转为dfa
    mfa, eventual, points_mfa = dfa2mfa(dfa, last, dfa_point, parses)
    draw_mfa(mfa, eventual, points_mfa)


def generate_nfa_set(st):  #生成nfa子集集合
    st_point = add_point(st)  # st添加结合运算符
    posfix = mid2pos(st_point)  # 得到后缀表达式
    parses = can(posfix)  # 算出式子中参数的个数
    r = pos2nfa(posfix)
    r, points = deep(r)  # 改变数字顺序
    return r


def generate_dfa_set(st):  #生成dfa子集集合
    st_point = add_point(st)  # st添加结合运算符
    posfix = mid2pos(st_point)  # 得到后缀表达式
    parses = can(posfix)  # 算出式子中参数的个数
    r = pos2nfa(posfix)
    r, points = deep(r)  # 改变数字顺序
    dfa, last, dfa_point = nfa2dfa(r, parses)  # 转为dfa

    # #全属性加 1
    # for i in range(len(dfa)):
    #     dfa[i][0] += 1
    #     dfa[i][2] += 1
    # for i in range(len(last)):
    #     last[i] += 1
    return dfa, last


def generate_mfa_set(st):  #生成mfa子集集合
    st_point = add_point(st)  # st添加结合运算符
    posfix = mid2pos(st_point)  # 得到后缀表达式
    parses = can(posfix)  # 算出式子中参数的个数
    r = pos2nfa(posfix)
    r, points = deep(r)  # 改变数字顺序
    dfa, last, dfa_point = nfa2dfa(r, parses)  # 转为dfa
    mfa, eventual, points_mfa = dfa2mfa(dfa, last, dfa_point, parses)

    # # 全属性加 1
    # for i in range(len(mfa)):
    #     mfa[i][0] += 1
    #     mfa[i][2] += 1
    # for i in range(len(eventual)):
    #     eventual[i] += 1
    return mfa, eventual


def action(st):
    st_point = add_point(st)#st添加结合运算符
    posfix = mid2pos(st_point)  #得到后缀表达式
    print(posfix)
    parses = can(posfix)     #算出式子中参数的个数
    r = pos2nfa(posfix)
    r, points = deep(r) #改变数字顺序
    # print(r)
    # draw_generate(r, points)        #生成图片
    dfa, last, dfa_point = nfa2dfa(r, parses)  #转为dfa
    draw_dfa(dfa, last, dfa_point)
    mfa, eventual, points_mfa = dfa2mfa(dfa, last, dfa_point, parses)
    draw_mfa(mfa, eventual, points_mfa)
    # print(mfa)
    # print(eventual)
# action('a*b|c')
