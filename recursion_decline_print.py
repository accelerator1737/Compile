import identify_status as identify
import First_Follow as ff
import identify_status as identify
row = 1

fen = []
fen_pos = []
error_tishi = ''
first = {}
follow = {}
now = 0
symbol_first = {}
symbol_follow = {}
profix = '------------------'
tian = '----------'
info = ''
guan = ['main', 'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
        'extern', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed',
        'sizeof', 'static', 'struct', 'switch', 'typedef', 'unsigned', 'union', 'void', 'volatile', 'while']#关键字
fu = ['223', '224', '231', '230', '232', '233', '234', '216', '217', '235', '224', '225', '226', '227', '228']


def alter_info(s):
    global info
    info = info + s + '\n'


def jian():
    global profix
    lio = len(tian)
    profix = profix[lio:]


def zeng():
    global profix
    profix += tian


#词法分析
def transform_ci(s_f):
    global fen, fen_pos
    fen.clear()
    fen_pos.clear()
    eryu_info, fen_pos, error_info, error_pos = identify.get_file_to_cifa(s_f)
    for part in eryu_info:
        l = []
        index = part.find(',')
        l.append(part[:index])
        l.append(part[index+1:])
        fen.append(l)


def check_it(op):
    if fen[now][0] not in symbol_first[op] and fen[now][1] not in first[op]:
        error()
        scan_to(op)


def scan_to(op):
    global now
    while fen[now][0] not in symbol_first[op] and fen[now][1] not in first[op] and \
            fen[now][0] not in symbol_follow[op] and fen[now][1] not in follow[op]:
        now += 1
        if now == len(fen):
            break


def A():
    if fen[now][1] in first['D'] or fen[now][0] in symbol_first['D']:
        D()
    elif fen[now][1] in first['E'] or fen[now][0] in symbol_first['E']:
        E()
    elif 'ε' in first['A'] and (fen[now][1] in follow['A'] or fen[now][0] in symbol_follow['A']):
        pass


def D():
    if fen[now][1] == '#':
        match('#')
        R()
    # else:
    #     error()


def R():
    check_it('R')
    if fen[now][1] == 'include':
        match('include')
        match('<')
        G()
        match('>')
        alter_info(profix + 'include 语句')
        print(profix + 'include 语句')
    elif fen[now][1] == 'define':
        match('define')
        match(token='700')
        match(token='0 400 408 416 450 500 600')
        alter_info(profix + 'define  语句')
        print(profix + 'define  语句')
    # else:
    #     error()


def G():
    check_it('G')
    if fen[now][0] == '900':
        match(token='900')
    # else:
    #     error()


def E():
    check_it('E')
    O()
    H()
    W()


def W():
    check_it('W')
    if fen[now][1] == ';':
        match(';')
    elif fen[now][0] == '700':
        match(token='700')
        u()
        F()


def u():
    if fen[now][1] == '[':
        alter_info(profix + '{}数组定义'.format(fen[now - 1][1]))
        print(profix + '{}数组定义'.format(fen[now - 1][1]))
        match('[')
        Q()
        match(']')
        B()
    elif fen[now][1] != '(':
        alter_info(profix + '{}变量定义'.format(fen[now - 1][1]))
        print(profix + '{}变量定义'.format(fen[now - 1][1]))


def O():
    if fen[now][1] == 'const':
        match('const')


def H():
    check_it('H')
    match(token='104 109 113 117 118')


def F():
    check_it('F')
    if fen[now][1] == '(':
        match('(')
        K()
        match(')')
        C()
    elif fen[now][1] == ',':
        match(',')
        W()
    else:
        P()
        i()
        W()


def i():
    if fen[now][1] == ',':
        match(',')


def P():
    if fen[now][1] == '=':
        match('=')
        v()


def v():
    check_it('v')
    if fen[now][1] == '{':
        match('{')
        J()
        match('}')
    else:
        w()


def w():
    check_it('w')
    if fen[now][0] in '0 400 408 416 450 500 600 700':
        match(token='0 400 408 416 450 500 600 700')


def B():
    if fen[now][1] == '[':
        match('[')
        match(token='400 408 416')
        match(']')
        B()


def K():
    if fen[now][1] in first['M'] or fen[now][0] in symbol_first['M']:
        M()
        L()
        K()
    elif fen[now][1] == ',':
        match(',')
        M()
        L()
        K()
    elif 'ε' in first['K'] and (fen[now][1] in follow['K'] or fen[now][0] in symbol_follow['K']):
        pass


def L():
    if fen[now][0] == '700':
        match(token='700')
        B()
    elif 'ε' in first['L'] and (fen[now][1] in follow['L'] or fen[now][0] in symbol_follow['L']):
        pass


def M():
    check_it('M')
    H()
    I()


def I():
    if fen[now][1] == '*':
        match('*')


def Q():
    if fen[now][0] == '400':
        match(token='400')


def J():
    if fen[now][1] == ',':
        match(',')
        match(token='0 400 408 416 450 500 600')
        J()
    elif fen[now][0] in '0 400 408 416 450 500 600':
        match(token='0 400 408 416 450 500 600')
        J()


def C():
    global error_tishi
    check_it('C')
    if fen[now][1] == ';':
        match(';')
        name = find_function_name()
        alter_info(profix + '{}函数声明语句'.format(fen[name][1]))
        print(profix + '{}函数声明语句'.format(fen[name][1]))
    elif fen[now][1] == '{':
        name = find_function_name()
        alter_info(profix + '分析{}函数'.format(fen[name][1]))
        print(profix + '分析{}函数'.format(fen[name][1]))
        match('{')
        zeng()
        while fen[now][1] != '}':
            N()
            if now == len(fen):
                print('line {},   column  {}:  缺失界符'.format(fen_pos[now-1][0], fen_pos[now-1][1]))
                error_tishi += 'line {},   column  {}:  缺失界符\n'.format(fen_pos[now-1][0], fen_pos[now-1][1])
                fen.append([302, '}'])
        jian()
        match('}')
        alter_info(profix + '{}函数分析结束'.format(fen[name][1]))
        print(profix + '{}函数分析结束'.format(fen[name][1]))
    # else:
    #     error()


def N():
    check_it('N')
    if fen[now][1] in first['S'] or fen[now][0] in symbol_first['S']:
        S()
    elif fen[now][1] in first['T'] or fen[now][0] in symbol_first['T']:
        T()

def S():
    check_it('S')
    if fen[now][1] == ';':
        match(';')
    elif fen[now][1] in first['E'] or fen[now][0] in symbol_first['E']:
        E()
    elif fen[now][1] in first['t'] or fen[now][0] in symbol_first['t']:
        t()
        match(';')


def t():
    check_it('t')
    if fen[now][0] == '700':
        match(token='700')
        B()
        U()
    elif fen[now][0] in '0 400 408 416 450 500 600':
        match(token='0 400 408 416 450 500 600')
        U()
    elif fen[now][1] in first['U'] or fen[now][0] in symbol_first['U']:
        U()



def U():
    if fen[now][1] == '=':
        match('=')
        X()
        alter_info(profix + '赋值表达式')
        print(profix + '赋值表达式')
    elif fen[now][1] in first['V'] or fen[now][0] in symbol_first['V']:
        V()
    elif fen[now][1] in first['Z'] or fen[now][0] in symbol_first['Z']:
        Z()


def X():
    check_it('X')
    Y()
    Z()


def Y():
    check_it('Y')
    b()
    c()


def c():
    if fen[now][0] in fu:
        match(fen[now][1])
        b()
        c()


def b():
    check_it('b')
    if fen[now][1] == '(':
        match('(')
        Y()
        match(')')
    elif fen[now][0] in '0 400 408 416 450 500 600':
        match(token='0 400 408 416 450 500 600')
    elif fen[now][0] == '700':
        match(token='700')
        x()


def x():
    if fen[now][1] in first['V'] or fen[now][0] in symbol_first['V']:
        V()
        name = find_function_name()
        alter_info(profix + '分析{}函数'.format(fen[name][1]))
    elif fen[now][1] in first['B'] or fen[now][0] in symbol_first['B']:
        B()


def Z():
    if fen[now][0] in '219 220 221 222 223 235':
        match(token='219 220 221 222 223 235')
        X()


def V():
    check_it('V')
    if fen[now][1] == '(':
        match('(')
        a()
        match(')')


def a():
    if fen[now][1] == ',':
        match(',')
        X()
        a()
    if fen[now][1] in first['X'] or fen[now][0] in symbol_first['X']:
        X()
        a()


def T():
    check_it('T')
    if fen[now][0] == '120':
        alter_info(profix + '开始进行return语句分析')
        print(profix + '开始进行return语句分析')
        match(token='120')
        m()
    elif fen[now][1] in first['o'] or fen[now][0] in symbol_first['o']:
        o()
    elif fen[now][1] in first['p'] or fen[now][0] in symbol_first['p']:
        p()
    elif fen[now][1] in first['q'] or fen[now][0] in symbol_first['q']:
        q()
    elif fen[now][1] in first['r'] or fen[now][0] in symbol_first['r']:
        r()


def o():
    check_it('o')
    if fen[now][0] == '116':
        alter_info(profix + '开始进行if语句分析')
        print(profix + '开始进行if语句分析')
        match(token='116')
        match('(')
        alter_info(profix + '布尔表达式分析')
        print(profix + '布尔表达式分析')
        t()
        alter_info(profix + '布尔表达式分析结束')
        print(profix + '布尔表达式分析结束')
        match(')')
        zeng()
        k()
        y()


def y():
    check_it('y')
    if fen[now][0] == '110':
        match(token='110')
        k()
        jian()
        alter_info(profix + 'if语句分析结束')
        print(profix + 'if语句分析结束')
    else:
        jian()
        alter_info(profix + 'if语句分析结束')
        print(profix + 'if语句分析结束')
        N()


def p():
    check_it('p')
    if fen[now][0] == '114':
        alter_info(profix + '开始进行for语句分析')
        print(profix + '开始进行for语句分析')
        zeng()
        match(token='114')
        match('(')
        t()
        match(';')
        t()
        match(';')
        t()
        match(')')
        h()
        jian()
        alter_info(profix + 'for语句分析结束')
        print(profix + 'for语句分析结束')


def q():
    check_it('q')
    if fen[now][0] == '132':
        alter_info(profix + '开始进行while语句分析')
        print(profix + '开始进行while语句分析')
        zeng()
        match(token='132')
        match('(')
        alter_info(profix + '布尔表达式分析')
        print(profix + '布尔表达式分析')
        t()
        alter_info(profix + '布尔表达式分析结束')
        print(profix + '布尔表达式分析结束')
        match(')')
        h()
        jian()
        alter_info(profix + 'while语句分析结束')
        print(profix + 'while语句分析结束')


def r():
    global error_tishi
    check_it('r')
    if fen[now][0] == '108':
        alter_info(profix + '开始进行do while语句分析')
        print(profix + '开始进行do while语句分析')
        zeng()
        match(token='108')
        match('{')
        while fen[now][1] != '}':
            f()
            if now == len(fen):
                print('line {},   column  {}:  缺失界符'.format(fen_pos[now - 1][0], fen_pos[now - 1][1]))
                error_tishi += 'line {},   column  {}:  缺失界符\n'.format(fen_pos[now - 1][0], fen_pos[now - 1][1])
                fen.append([302, '}'])
        match('}')
        match(token='132')
        match('(')
        alter_info(profix + '布尔表达式分析')
        print(profix + '布尔表达式分析')
        t()
        alter_info(profix + '布尔表达式分析结束')
        print(profix + '布尔表达式分析结束')
        match(')')
        match(';')
        jian()
        alter_info(profix + 'do while语句分析结束')
        print(profix + 'do while语句分析结束')


def k():
    global error_tishi
    check_it('k')
    if fen[now][1] == '{':
        match('{')
        while fen[now][1] != '}':
            N()
            if now == len(fen):
                print('line {},   column  {}:  缺失界符'.format(fen_pos[now - 1][0], fen_pos[now - 1][1]))
                error_tishi += 'line {},   column  {}:  缺失界符\n'.format(fen_pos[now - 1][0], fen_pos[now - 1][1])
                fen.append([302, '}'])
        match('}')
    elif fen[now][1] in first['N'] or fen[now][0] in symbol_first['N']:
        N()


def m():
    check_it('m')
    if fen[now][1] == ';':
        match(';')
    else:
        X()
        match(';')


def h():
    global error_tishi
    check_it('h')
    if fen[now][1] == '{':
        match('{')
        while fen[now][1] != '}':
            f()
            if now == len(fen):
                print('line {},   column  {}:  缺失界符'.format(fen_pos[now - 1][0], fen_pos[now - 1][1]))
                error_tishi += 'line {},   column  {}:  缺失界符\n'.format(fen_pos[now - 1][0], fen_pos[now - 1][1])
                fen.append([302, '}'])
        match('}')
    else:
        f()


def f():
    check_it('f')
    if fen[now][0] == '102':
        alter_info(profix + 'break 语句分析')
        print(profix + 'break 语句分析')
        match(token='102')
        match(';')
    elif fen[now][0] == '106':
        alter_info(profix + 'continue 语句分析')
        print(profix + 'continue 语句分析')
        match(token='106')
        match(';')
    else:
        N()


def match(ss=None, token='miss'):
    global first, follow, fen, now, source
    if token == 'miss':
        if fen[now][1] == ss:
            now += 1
        else:
            error()
    else:
        if fen[now][0] in token:
            now += 1
        else:
            error()


def error():
    global error_tishi
    error_tishi += 'line {},   column  {}:  unexpect \"{}\" in that position\n'.format(fen_pos[now][0], fen_pos[now][1], fen[now][1])
    print('line {},   column  {}:  unexpect {} in that position'.format(fen_pos[now][0], fen_pos[now][1], fen[now][1]))


def find_function_name():
    name = now
    while fen[name][1] != '(':
        name -= 1
    return name - 1


def balance():
    global first, follow, symbol_first, symbol_follow
    for i in first:
        j = 0
        while j < len(first[i]):
            if first[i][j] == '0':
                first[i][j] = 'include'
            elif first[i][j] == '1':
                first[i][j] = 'define'
            elif first[i][j] == '2':
                j -= 1
                first[i].remove('2')
                symbol_first[i].extend(['0', '400', '408', '416', '450', '500', '600'])
            elif first[i][j] == '3':
                j -= 1
                first[i].remove('3')
                symbol_first[i].append('700')
            elif first[i][j] == '4':
                first[i][j] = 'const'
            elif first[i][j] == '5':
                j -= 1
                first[i].remove('5')
                symbol_first[i].extend(['104', '109', '113', '117', '118'])
            elif first[i][j] == '6':
                j -= 1
                first[i].remove('6')
                symbol_first[i].append('400')
            elif first[i][j] == '7':
                j -= 1
                first[i].remove('7')
                symbol_first[i].append('900')
            elif first[i][j] == '8':
                j -= 1
                first[i].remove('8')
                symbol_first[i].extend(fu)
            elif first[i][j] == '9':
                j -= 1
                first[i].remove('9')
                symbol_first[i].extend(['219', '220', '221', '222', '223', '235'])
            elif first[i][j] == 'β':
                j -= 1
                first[i].remove('β')
                symbol_first[i].append('120')
            elif first[i][j] == 'δ':
                j -= 1
                first[i].remove('δ')
                symbol_first[i].append('116')
            elif first[i][j] == 'ζ':
                j -= 1
                first[i].remove('ζ')
                symbol_first[i].append('114')
            elif first[i][j] == 'η':
                j -= 1
                first[i].remove('η')
                symbol_first[i].append('132')
            elif first[i][j] == 'θ':
                j -= 1
                first[i].remove('θ')
                symbol_first[i].append('108')
            elif first[i][j] == 'ψ':
                j -= 1
                first[i].remove('ψ')
                symbol_first[i].append('110')
            elif first[i][j] == 'τ':
                j -= 1
                first[i].remove('τ')
                symbol_first[i].append('102')
            elif first[i][j] == 'φ':
                j -= 1
                first[i].remove('φ')
                symbol_first[i].append('106')
            j += 1

    for i in follow:
        j = 0
        while j < len(follow[i]):
            if follow[i][j] == '0':
                follow[i][j] = 'include'
            elif follow[i][j] == '1':
                follow[i][j] = 'define'
            elif follow[i][j] == '2':
                j -= 1
                follow[i].remove('2')
                symbol_follow[i].extend(['0', '400', '408', '416', '450', '500', '600'])
            elif follow[i][j] == '3':
                j -= 1
                follow[i].remove('3')
                symbol_follow[i].append('700')
            elif follow[i][j] == '4':
                follow[i][j] = 'const'
            elif follow[i][j] == '5':
                j -= 1
                follow[i].remove('5')
                symbol_follow[i].extend(['104', '109', '113', '117', '118'])
            elif follow[i][j] == '6':
                j -= 1
                follow[i].remove('6')
                symbol_follow[i].append('400')
            elif follow[i][j] == '7':
                j -= 1
                follow[i].remove('7')
                symbol_follow[i].extend(fu)
            elif follow[i][j] == '8':
                j -= 1
                follow[i].remove('8')
                symbol_follow[i].append('228')
            elif follow[i][j] == '9':
                j -= 1
                follow[i].remove('9')
                symbol_follow[i].extend(['219', '220', '221', '222', '223', '235'])
            elif follow[i][j] == 'β':
                j -= 1
                follow[i].remove('β')
                symbol_follow[i].append('120')
            elif follow[i][j] == 'δ':
                j -= 1
                follow[i].remove('δ')
                symbol_follow[i].append('116')
            elif follow[i][j] == 'ζ':
                j -= 1
                follow[i].remove('ζ')
                symbol_follow[i].append('114')
            elif follow[i][j] == 'η':
                j -= 1
                follow[i].remove('η')
                symbol_follow[i].append('132')
            elif follow[i][j] == 'θ':
                j -= 1
                follow[i].remove('θ')
                symbol_follow[i].append('108')
            elif follow[i][j] == 'ψ':
                j -= 1
                follow[i].remove('ψ')
                symbol_follow[i].append('110')
            elif follow[i][j] == 'τ':
                j -= 1
                follow[i].remove('τ')
                symbol_follow[i].append('102')
            elif follow[i][j] == 'φ':
                j -= 1
                follow[i].remove('φ')
                symbol_follow[i].append('106')
            j += 1


def init_symbol_first():
    global first, symbol_first, symbol_follow
    for i in first:
        symbol_first[i] = []
        symbol_follow[i] = []


def grammar_analysis(s_f):
    global first, follow, symbol_first, symbol_follow, info, now, profix, error_tishi
    #初始化
    error_tishi = ''
    first = {}
    follow = {}
    now = 0
    symbol_first = {}
    symbol_follow = {}
    profix = '------------------'
    info = ''

    transform_ci(s_f)
    first = ff.get_first_set()
    follow = ff.get_follow_set()
    init_symbol_first()
    c = len(fen)
    balance()
    alter_info(profix + '开始进行语法分析')
    print(profix + '开始进行语法分析')
    zeng()
    while now < c:
        check_it('A')
        if now == len(fen):
            break
        A()
    jian()
    alter_info(profix + '语法分析结束')
    print(profix + '语法分析结束')
    return info, error_tishi


# jf = open('test.txt', 'r')
# s_f = jf.read()
# jf.close()
# grammar_analysis(s_f)

