import identify_status as identify
import First_Follow as ff
row = 1

fen = []
first = {}
follow = {}
now = 0
source = ['A']
symbol_first = {}
symbol_follow = {}


#将词法分析的东西写入右上右下，错误直接丢掉
def write_cifa(word):
    global fen
    if word != '':
        if word[0] == '1':
            index = word.find(',')
            l = []
            l.append(word[2:index])
            l.append(word[index+1:-1])
            fen.append(l)
        elif word[0] == '0':
            print(word[1:])


#词法分析
def transform_ci(s_f):
    global fen
    fen.clear()
    j = 0
    while j < len(s_f):
        ss, eryu = identify.identify_string(s_f, j)
        write_cifa(eryu)
        j += len(ss)
        if j == len(s_f):
            break
        ss, eryu = identify.identify_annotation(s_f, j)
        write_cifa(eryu)
        j += len(ss)
        if j == len(s_f):
            break
        ss, eryu = identify.identify_operation(s_f, j)
        write_cifa(eryu)
        j += len(ss)
        if j == len(s_f):
            break
        ss, eryu = identify.identify_number(s_f, j)
        write_cifa(eryu)
        j += len(ss)
        if j == len(s_f):
            break
        ss, eryu = identify.identify_boundary(s_f, j)
        write_cifa(eryu)
        j += len(ss)
        if j == len(s_f):
            break
        ss, eryu = identify.identify_char(s_f, j)
        write_cifa(eryu)
        j += len(ss)
        if j == len(s_f):
            break
        ss, eryu = identify.identify_symbol(s_f, j)
        write_cifa(eryu)
        j += len(ss)
        if j == len(s_f):
            break
        ss, eryu = identify.identify_other(s_f, j)
        write_cifa(eryu)
        j += len(ss)
        if j == len(s_f):
            break


def A():
    global first, follow, fen, now
    if fen[now][1] in first['D'] or fen[now][0] in symbol_first['D']:
        D()
    elif fen[now][1] in first['E'] or fen[now][0] in symbol_first['E']:
        E()
    elif 'ε' in first['A'] and (fen[now][1] in follow['A'] or fen[now][0] in symbol_follow['A']):
        pass
    else:
        error()


def D():
    global first, follow, fen, now, source
    if fen[now][1] == '#':
        match('#')
        R()
    else:
        error()


def R():
    global first, follow, fen, now, source
    if fen[now][1] == 'include':
        match('include')
        match('<')
        G()
        match('>')
    elif fen[now][1] == 'define':
        match('define')
        match(token='700')
        match(token='0 400 408 416 450 500 600')
    else:
        error()


def G():
    global first, follow, fen, now, source
    if fen[now][0] == '900':
        match(token='900')
    else:
        error()



def E():
    global first, follow, fen, now, source
    O()
    H()
    W()


def W():
    if fen[now][1] == ';':
        match(';')
    elif fen[now][0] in '700 133':
        match(token='700 133')
        u()
        F()


def u():
    if fen[now][1] == '[':
        match('[')
        Q()
        match(']')


def O():
    global first, follow, fen, now, source
    if fen[now][1] == 'const':
        match('const')


def H():
    global first, follow, fen, now, source
    match(token='104 109 113 117 118')


def F():
    global first, follow, fen, now, source
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
    global first, follow, fen, now, source
    if fen[now][1] == '=':
        match('=')
        v()


def v():
    if fen[now][1] == '{':
        match('{')
        J()
        match('}')
    else:
        w()


def w():
    if fen[now][0] in '0 400 408 416 450 500 600 700':
        match(token='0 400 408 416 450 500 600 700')


def B():
    if fen[now][1] == '[':
        match('[')
        match(token='400')
        match(']')


def K():
    global first, follow, fen, now, source
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
    H()
    I()


def I():
    global first, follow, fen, now, source
    if fen[now][1] == '*':
        match('*')


def Q():
    global first, follow, fen, now, source
    if fen[now][0] == '400':
        match(token='400')


def J():
    global first, follow, fen, now, source
    if fen[now][1] == ',':
        match(',')
        match(token='0 400 408 416 450 500 600')
        J()
    elif fen[now][0] in '0 400 408 416 450 500 600':
        match(token='0 400 408 416 450 500 600')
        J()


def C():
    global first, follow, fen, now, source
    if fen[now][1] == ';':
        match(';')
    elif fen[now][1] == '{':
        match('{')
        while fen[now][1] != '}':
            print(now)
            N()
        match('}')
    else:
        error()


def N():
    if fen[now][1] in first['S'] or fen[now][0] in symbol_first['S']:
        S()
    elif fen[now][1] in first['T'] or fen[now][0] in symbol_first['T']:
        T()

def S():
    if fen[now][1] in first['E'] or fen[now][0] in symbol_first['E']:
        E()
    elif fen[now][1] in first['t'] or fen[now][0] in symbol_first['t']:
        t()
        match(';')


def t():
    if fen[now][0] == '700':
        match(token='700')
        B()
        U()
    elif fen[now][0] in '0 400 408 416 450 500 600':
        match(token='0 400 408 416 450 500 600')
        U()


def U():
    if fen[now][1] == '=':
        match('=')
        X()
    elif fen[now][1] in first['V'] or fen[now][0] in symbol_first['V']:
        V()
    elif fen[now][1] in first['Z'] or fen[now][0] in symbol_first['Z']:
        Z()


def X():
    Y()
    Z()


def Y():
    b()
    c()


def c():
    if fen[now][1] == '+':
        match('+')
        b()
        c()
    elif fen[now][1] == '-':
        match('-')
        b()
        c()


def b():
    d()
    e()


def e():
    if fen[now][1] == '*':
        match('*')
        d()
        e()
    elif fen[now][1] == '/':
        match('/')
        d()
        e()
    elif fen[now][1] == '%':
        match('%')
        d()
        e()


def d():
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
    elif fen[now][1] in first['B'] or fen[now][0] in symbol_first['B']:
        B()


def Z():
    if fen[now][0] in '219 220 221 222 223 235':
        match(token='219 220 221 222 223 235')
        Y()


def V():
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
    if fen[now][0] == '120':
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
    if fen[now][0] == '116':
        match(token='116')
        match('(')
        t()
        match(')')
        k()
        y()


def p():
    if fen[now][0] == '114':
        match(token='114')
        match('(')
        t()
        match(';')
        t()
        match(';')
        t()
        match(')')
        h()


def q():
    if fen[now][0] == '132':
        match(token='132')
        match('(')
        t()
        match(')')
        h()


def r():
    if fen[now][0] == '108':
        match(token='108')
        match('{')
        while fen[now][1] != '}':
            f()
        match('}')
        match(token='132')
        match('(')
        t()
        match(')')
        match(';')


def k():
    if fen[now][1] == '{':
        match('{')
        while fen[now][1] != '}':
            N()
        match('}')
    elif fen[now][1] in first['N'] or fen[now][0] in symbol_first['N']:
        N()


def m():
    if fen[now][1] == ';':
        match(';')
    else:
        X()
        match(';')


def h():
    if fen[now][1] == '{':
        match('{')
        while fen[now][1] != '}':
            f()
        match('}')
    else:
        f()


def f():
    if fen[now][0] == '102':
        match(token='102')
        match(';')
    elif fen[now][0] == '106':
        match(token='106')
        match(';')
    else:
        N()


def y():
    if fen[now][0] == '110':
        match(token='110')
        k()
        print('if语句分析结束')
    else:
        print('if语句分析结束')
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
    print(str(now) + "mistake")


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
                symbol_first[i].append('228')
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
                symbol_follow[i].append('900')
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


def grammar_analysis():
    global first, follow, symbol_first, symbol_follow
    f = open('test.txt', 'r')
    s_f = f.read()
    f.close()
    transform_ci(s_f)
    first = ff.get_first_set()
    follow = ff.get_follow_set()
    init_symbol_first()
    c = len(fen)
    balance()
    while now < c:
        print(now)
        A()
    print(now)
grammar_analysis()
