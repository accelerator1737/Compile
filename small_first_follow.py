import copy
FIRST = {}

FOLLOW = {}

sentences = []

start = ''


#初始化 first 集 和follow集合字典的键值对中的 值 为空
def initail_first():
    global FIRST, FOLLOW, sentences, start
    for str in sentences:
        part_begin = str.split("->")[0]
        part_end = str.split("->")[1]
        FIRST[part_begin] = []


def initail_follow():
    global FIRST, FOLLOW, sentences, start
    for str in sentences:
        part_begin = str.split("->")[0]
        part_end = str.split("->")[1]
        FOLLOW[part_begin] = []


###求first集 中第第一部分针对直接推出第一个字符为终结符
def getFirst():
    global FIRST, FOLLOW, sentences, start
    for str in sentences:
        part_begin = str.split("->")[0]
        hou = str.split("->")[1]
        if "|" in hou:      #如果后半部分有|则将其分开来
            part = hou.split("|")
            for i in part:
                if i[0] not in FIRST:
                    FIRST[part_begin].append(i[0])
        else:
            if hou[0] not in FIRST:
                FIRST[part_begin].append(hou[0])


##求first第二部分 针对 A -> Ba型  把B的first集加到A 的first集合中
def getFirst_2():
    global FIRST, FOLLOW, sentences, start
    for str in sentences:
        part_begin = str.split("->")[0]
        hou = str.split("->")[1]
        if "|" in hou:  # 如果后半部分有|则将其分开来
            part = hou.split("|")
            for i in part:
                if i[0] in FIRST:
                    for k in FIRST.get(i[0]):
                        if k != 'ε':
                            FIRST[part_begin].append(k)
        else:
            if hou[0] in FIRST:
                for k in FIRST.get(hou[0]):
                    if k != 'ε':
                        FIRST[part_begin].append(k)


##求first第二部分 针对 A -> BCD型,B或之后的能推导出ε
def getFirst_3():
    global FIRST, FOLLOW, sentences, start
    for str in sentences:
        part_begin = str.split("->")[0]
        hou = str.split("->")[1]
        remove_first_repeat()
        if "|" in hou:  # 如果后半部分有|则将其分开来
            part = hou.split("|")
            for i in part:
                j = 0
                while j < len(i):
                    if i[j] not in FIRST:
                        FIRST[part_begin].append(i[j])
                        break
                    else:
                        if 'ε' in FIRST[i[j]]:
                            if j + 1 < len(i):
                                if i[j + 1] in FIRST:
                                    for k in FIRST.get(i[j + 1]):
                                        if k != 'ε':
                                            FIRST[part_begin].append(k)
                                else:
                                    FIRST[part_begin].append(i[j + 1])
                            else:
                                break
                        else:
                            break
                    j += 1
        else:
            i = 0
            while i < len(hou):
                if hou[i] not in FIRST:
                    FIRST[part_begin].append(hou[i])
                    break
                else:
                    if 'ε' in FIRST[hou[i]]:
                        if i + 1 < len(hou):
                            if hou[i+1] in FIRST:
                                for k in FIRST.get(hou[i+1]):
                                    if k != 'ε':
                                        FIRST[part_begin].append(k)
                            else:
                                FIRST[part_begin].append(hou[i+1])
                        else:
                            break
                    else:
                        break
                i += 1



#去掉重复项
def remove_first_repeat():
    global FIRST, FOLLOW, sentences, start
    for i in FIRST:
        s = set(FIRST[i])
        l = list(s)
        FIRST[i] = l


#规则1，S是开始符号，则将#加入
def getFOLLOW_1():
    global FIRST, FOLLOW, sentences, start
    FOLLOW[start].append('$')


#规则2，产生式为B->aAb,将b加入其中
def getFOLLOW_2():
    global FIRST, FOLLOW, sentences, start
    for s in sentences:
        part_begin = s.split("->")[0]
        for ss in sentences:
            hou = ss.split("->")[1]
            if '|' in hou:
                part = hou.split('|')
                for i in part:
                    index = i.find(part_begin)
                    if index != -1:
                        if index + 1 < len(i):
                            if i[index + 1] not in FOLLOW:
                                FOLLOW[part_begin].append(i[index + 1])
            else:
                index = hou.find(part_begin)
                if index != -1:
                    if index + 1 < len(hou):
                        if hou[index+1] not in FOLLOW:
                            FOLLOW[part_begin].append(hou[index+1])

#规则3，B->aACb,Cb不能推出ε时，将First(C)中的非ε加入FOLLOW[A]，能时将FOLLOW[B]加入FOLLOW[A]
def getFOLLOW_3():
    global FIRST, FOLLOW, sentences, start
    for s in sentences:
        part_begin = s.split("->")[0]
        remove_follow_repeat()
        for ss in sentences:
            remove_follow_repeat()
            qian = ss.split("->")[0]
            hou = ss.split("->")[1]
            if '|' in hou:
                part = hou.split('|')
                for hou in part:
                    index = hou.find(part_begin)
                    if index != -1:
                        if index == len(hou) - 1:
                            FOLLOW[part_begin].extend(FOLLOW[qian])
                        while index + 1 < len(hou):
                            if hou[index + 1] not in FOLLOW:
                                FOLLOW[part_begin].append(hou[index + 1])
                                break
                            elif hou[index + 1] in FOLLOW:
                                if 'ε' not in FIRST[hou[index + 1]]:
                                    FOLLOW[part_begin].extend(FIRST[hou[index + 1]])
                                    break
                                else:
                                    if index + 1 == len(hou):
                                        FOLLOW[part_begin].extend(FOLLOW[qian])
                                    else:
                                        if hou[index + 1] in FIRST:
                                            for k in FIRST[hou[index + 1]]:
                                                if k != 'ε':
                                                    FOLLOW[part_begin].append(k)
                                            if index + 2 == len(hou):
                                                FOLLOW[part_begin].extend(FOLLOW[qian])
                                        else:
                                            FOLLOW[part_begin].append(hou[index + 1])
                                            break
                            index += 1
            else:
                index = hou.find(part_begin)
                if index != -1:
                    if index == len(hou) - 1:
                        FOLLOW[part_begin].extend(FOLLOW[qian])
                    while index + 1 < len(hou):
                        if hou[index+1] not in FOLLOW:
                            FOLLOW[part_begin].append(hou[index+1])
                            break
                        elif hou[index+1] in FOLLOW:
                            if 'ε' not in FIRST[hou[index+1]]:
                                FOLLOW[part_begin].extend(FIRST[hou[index+1]])
                                break
                            else:
                                if index + 1 == len(hou):
                                    FOLLOW[part_begin].extend(FOLLOW[qian])
                                else:
                                    if hou[index + 1] in FIRST:
                                        for k in FIRST[hou[index + 1]]:
                                            if k != 'ε':
                                                FOLLOW[part_begin].append(k)
                                        if index + 2 == len(hou):
                                            FOLLOW[part_begin].extend(FOLLOW[qian])
                                    else:
                                        FOLLOW[part_begin].append(hou[index + 1])
                                        break
                        index += 1


#去掉重复项
def remove_follow_repeat():
    global FIRST, FOLLOW, sentences, start
    for i in FOLLOW:
        s = set(FOLLOW[i])
        l = list(s)
        FOLLOW[i] = l


def element_equal(pre, after):
    global FIRST, FOLLOW, sentences, start
    for i in pre:
        m = []
        n = []
        n = [x for x in pre[i] if x in after[i]]  # 两个列表表都存在
        b = [y for y in (pre[i] + after[i]) if y not in n]
        if len(b) > 0:
            return False
    return True


def get_first_set_small(se1):
    global FIRST, FOLLOW, sentences, start
    FIRST = {}
    se = se1.split('\n')
    sentences = []
    for i in se:
        sentences.append(i)
    start = sentences[0].split('->')[0]
    initail_first()
    while True:
        getFirst()
        remove_first_repeat()
        pre = copy.deepcopy(FIRST)
        getFirst_2()
        remove_first_repeat()
        getFirst_3()
        remove_first_repeat()
        if element_equal(pre, FIRST):
            break
    return FIRST


def get_follow_set_small(se1):
    global FIRST, FOLLOW, sentences, start
    FIRST = {}
    FOLLOW = {}
    se = se1.split('\n')
    sentences = []
    for i in se:
        sentences.append(i)
    start = sentences[0].split('->')[0]
    initail_follow()
    get_first_set_small(se1)
    while True:
        getFOLLOW_1()
        remove_follow_repeat()
        getFOLLOW_2()
        remove_follow_repeat()
        pre = copy.deepcopy(FOLLOW)
        getFOLLOW_3()
        remove_follow_repeat()
        if element_equal(pre, FOLLOW):
            break
    return FOLLOW


def judge_left(t):
    s1 = t.split('\n')
    for i in s1:
        qian = i.split('->')[0]
        mi = i.split('->')[1]
        if '|' in i:
            s2 = mi.split('|')
            for j in s2:
                if j[0] == qian:
                    return False
        else:
            hou = mi[0]
            if qian == hou:
                return False
    return True

#判断是否为LL(1)文法
def judgement(t):
    global FIRST, FOLLOW, sentences, start
    FIRST = {}
    FOLLOW = {}
    get_first_set_small(t)
    get_follow_set_small(t)
    pan = []
    for i in sentences:
        if 'ε' in i:
            part_begin = i.split("->")[0]
            if len([v for v in FIRST[part_begin] if v in FOLLOW[part_begin]]) != 0:
                pan.append(part_begin)
    for i in sentences:
        if '|' in i:
            part = i.split("->")[1].split("|")
            l = []
            for j in part:
                n = []
                if j[0] in FIRST:
                    for kk in FIRST[j[0]]:
                        n.append(kk)
                else:
                    n.append(j[0])
                l.append(n)
            if len(l) > 1:
                fl = 0
                for j in range(len(l)):
                    for k in range(j + 1, len(l)):
                        if len([v for v in l[j] if v in l[k]]) != 0:
                            pan.append(i)
                            fl = 1
                            break
                    if fl == 1:
                        break
    if len(pan) == 0:
        return True
    else:
        return False


def text2sentence(t):
    se = t.split('\n')
    ss = []
    re = []
    for i in se:
        ss.append(i)
    for i in ss:
        if '|' not in i:
            re.append(i)
        else:
            qian = i.split('->')[0]
            mi = i.split('->')[1]
            zong = mi.split('|')
            for part in zong:
                sss = qian + '->' + part
                re.append(sss)
    return re

