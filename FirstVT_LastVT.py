import copy


def get_firstvt(t): #得到firstVT集
    fen = get_single(t)
    no_end = get_no_end(fen)
    firstvt = init_firstvt(no_end)
    while True:
        pre = copy.deepcopy(firstvt)
        firstvt = get_firstvt_rule(firstvt, fen, no_end)
        firstvt = remove_repeat(firstvt)
        if element_equal(pre, firstvt):
            break
    return firstvt


def get_firstvt_rule(firstvt, fen, no_end):
    #以终结符开头,A->a...,加入firstVT
    for i in fen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        if hou[0] not in no_end:
            firstvt[qian].append(hou[0])
    # 以非终结符开头,终结符第二个，A->Ba...,加入firstVT
    for i in fen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        if len(hou) > 1:
            if hou[0] in no_end:
                if hou[1] not in no_end:
                    firstvt[qian].append(hou[1])
    # 以非终结符，A->B...,该非终结符的FirstVT加入A的firstVT
    for i in fen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        if hou[0] in no_end:
            a = copy.deepcopy(firstvt[hou[0]])
            for j in a:
                firstvt[qian].append(j)
    return firstvt


def remove_repeat(FIRST):       #去除重复元素
    for i in FIRST:
        s = set(FIRST[i])
        l = list(s)
        FIRST[i] = l
    return FIRST


def element_equal(pre, after):  #列表的比较
    for i in pre:
        m = []
        n = []
        n = [x for x in pre[i] if x in after[i]]  # 两个列表表都存在
        b = [y for y in (pre[i] + after[i]) if y not in n]
        if len(b) > 0:
            return False
    return True


def init_firstvt(no_end):#初始化firstvt集
    firstvt = {}
    for i in no_end:
        firstvt[i] = []
    return firstvt


def get_single(t):  #去除"|"关系
    re = []
    s = t.split('\n')
    for p in s:
        if '|' not in p:
            re.append(p)
        else:
            qian = p.split('->')[0]
            mi = p.split('->')[1]
            fen = mi.split('|')
            for part in fen:
                x = qian + '->' + part
                re.append(x)
    return re


def get_no_end(fen):    #得到非终结符
    s = []
    for i in fen:
        s.append(i.split('->')[0])
    s = set(s)
    s = list(s)
    return s


def judge_op(t):    #判断是否是OG文法
    fen = get_single(t)
    no_end = get_no_end(fen)
    for i in fen:
        mi = i.split('->')[1]
        ji = 0
        for j in mi:
            if j in no_end:
                ji += 1
            else:
                ji = 0
            if ji == 2:
                return False
    return True


def get_lastvt(t):  #获得LastVT集
    fen = get_single(t)
    no_end = get_no_end(fen)
    lastvt = init_firstvt(no_end)
    while True:
        pre = copy.deepcopy(lastvt)
        lastvt = get_lastvt_rule(lastvt, fen, no_end)
        lastvt = remove_repeat(lastvt)
        if element_equal(pre, lastvt):
            break
    return lastvt


def get_lastvt_rule(lastvt, fen, no_end):   #LastVT集的运算规则
    # 以终结符结束,A->...a,a加入LastVT
    for i in fen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        if hou[-1] not in no_end:
            lastvt[qian].append(hou[-1])
    # 以终结符结束,非终结符倒数第二，A->...aB,a加入LastVT
    for i in fen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        if len(hou) > 1:
            if hou[-1] in no_end:
                if hou[-2] not in no_end:
                    lastvt[qian].append(hou[-2])
    # 以非终结符结束，A->...B,该非终结符的LastVT加入A的LastVT
    for i in fen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        if hou[-1] in no_end:
            a = copy.deepcopy(lastvt[hou[-1]])
            for j in a:
                lastvt[qian].append(j)
    return lastvt


