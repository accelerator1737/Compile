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
var = {}    #变量定义
fun = {}    #函数定义
array = {}  #数组定义
yu = 0      #作用域编号
assign = {'int': '400 408 416', 'float': '400 408 416 450', 'char': '500', 'long': '400', 'double': '400 408 416 450'}   #类型对应的值
state_assign = {'int': '400', 'float': '450', 'char': '500', 'long': '400', 'double': '450'}
ge = 0  #检验函数参数个数
accept = 1  #是否将函数纳入函数表
wei = []    #记录数组的维度信息
mean_error = '' #语义错误


def mean_error_add(s):  #增加错误提示
    global mean_error
    mean_error = mean_error + s + '\n'


def accept_0(): #accept变为0，不接受
    global accept
    accept = 0


def set_fun_arrive(name):    #设置函数为已到达
    global fun
    fun[name]['arrive'] = True


def compara_state(name):    #比较外部声明以及函数定义是否相同
    now_find = now + 1
    para = []
    while fen[now_find][1] != ')':
        if fen[now_find][0] in '104 109 113 117 118':
            para.append(fen[now_find][1])
        now_find += 1
    if para != fun[name]['parameter']:
        tishi = 'line {},   column  {} :声明函数 {} 与定义函数 {} 不相同'.format(fen_pos[now][0], fen_pos[now][1], name, name)
        mean_error_add(tishi)
        #print(tishi)


def wei_add(we):    #增加数组的维度
    global wei
    wei.append(we)


def wei_clear():    #清除维度
    global wei
    wei.clear()


def accept_1(): #accept变为1，接受
    global accept
    accept = 1


def spect_express(name):    #检查赋值表达式左右是否类型一样
    if str(yu) + name in array:
        ty = array[str(yu) + name]['type']
    elif str(yu) + name in var:
        ty = var[str(yu) + name]['type']
    else:
        return
    now_find = now
    while fen[now_find][1] != '=':
        now_find -= 1
    now_find += 1
    while now_find < now:
        if fen[now_find][0] in '0 400 408 416 450 500 600 700':
            if fen[now_find][0] == '700':
                if str(yu) + fen[now_find][1] in var:
                    if state_assign[var[str(yu) + fen[now_find][1]]['type']] not in assign[ty]:
                        tishi = 'line {},   column  {} :表达式两边类型不匹配'.format(fen_pos[now_find][0], fen_pos[now_find][1])
                        mean_error_add(tishi)
                        #print(tishi)
                        break
                elif str(yu) + fen[now_find][1] in array:
                    if state_assign[array[str(yu) + fen[now_find][1]]['type']] not in assign[ty]:
                        tishi = 'line {},   column  {} :表达式两边类型不匹配'.format(fen_pos[now_find][0], fen_pos[now_find][1])
                        mean_error_add(tishi)
                        #print(tishi)
                        break
                elif fen[now_find][1] in fun:
                    if state_assign[fun[fen[now_find][1]]['type']] not in assign[ty]:
                        tishi = 'line {},   column  {} :表达式两边类型不匹配'.format(fen_pos[now_find][0], fen_pos[now_find][1])
                        mean_error_add(tishi)
                        #print(tishi)
                        break
            else:
                if fen[now_find][0] not in assign[ty]:
                    tishi = 'line {},   column  {} :表达式两边类型不匹配'.format(fen_pos[now_find][0], fen_pos[now_find][1])
                    mean_error_add(tishi)
                    #print(tishi)
                    break
        now_find += 1


def spect_array_length(name):     #检查并得到数组的长度
    global array
    now_find = now
    l = 1
    for i in range(1, len(wei)):
        l = l * int(wei[i])
        array[str(yu) + name]['dimension'].append(int(wei[i]))
    if fen[now_find][1] != '=':  #如果数组没有赋初值
        if wei[0] == '':
            array[str(yu) + name]['dimension'].insert(0, 1)
        else:
            array[str(yu) + name]['dimension'].insert(0, int(wei[0]))
    else:
        now_find += 2
        account = 0
        ty = array[str(yu) + name]['type']
        while fen[now_find][1] != '}':
            if fen[now_find][1] != ',':
                if fen[now_find][0] not in assign[ty]:
                    tishi = 'line {},   column  {} :数组 {} 值与数组类型不符合'.format(fen_pos[now_find][0], fen_pos[now_find][1], name)
                    mean_error_add(tishi)
                    #print(tishi)
                account += 1
            now_find += 1
        one = 0
        if wei[0] == '':
            if account % l == 0:
                one = account // l
            else:
                one = account // l + 1
            array[str(yu) + name]['dimension'].insert(0, one)
        else:
            array[str(yu) + name]['dimension'].insert(0, int(wei[0]))
            l = l * int(wei[0])
            if l < account:
                tishi = 'line {},   column  {} :数组 {} 初始长度不够'.format(fen_pos[now_find][0], fen_pos[now_find][1], name)
                mean_error_add(tishi)
                #print(tishi)


def spect_array():       #检查数组长度引用
    now_find = now
    while fen[now_find][0] != '700':
        now_find -= 1
    name = fen[now_find][1]
    if len(wei) == len(array[str(yu) + name]['dimension']):
        for i in range(len(wei)):
            if int(wei[i]) >= array[str(yu) + name]['dimension'][i]:
                tishi = 'line {},   column  {} :对数组 {} 引用超过定义的长度'.format(fen_pos[now][0], fen_pos[now][1], name)
                mean_error_add(tishi)
                #print(tishi)
                break
    else:
        tishi = 'line {},   column  {} :对数组 {} 的错误引用'.format(fen_pos[now][0], fen_pos[now][1], name)
        mean_error_add(tishi)
        #print(tishi)


def sepect_identify_var():  #检查是否有未声明的变量
    now_find = now
    while fen[now_find][0] != '700':
        now_find -= 1
    name = fen[now_find][1]
    for i in var:
        if name == i[1:]:
            break
    else:
        tishi = "line {},   column  {} :变量 {} 未声明".format(fen_pos[now][0], fen_pos[now][1], name)
        mean_error_add(tishi)
        #print(tishi)


def sepect_identify_array():  #检查是否有未声明的数组
    now_find = now
    while fen[now_find][0] != '700':
        now_find -= 1
    name = fen[now_find][1]
    for i in array:
        if name == i[1:]:
            break
    else:
        tishi = "line {},   column  {} :数组 {} 未声明".format(fen_pos[now][0], fen_pos[now][1], name)
        mean_error_add(tishi)
        #print(tishi)


def scope_clear(scope):     #清除过期作用域
    global var, array
    shan = []
    for i in var:
        if i[0] == str(scope):
            shan.append(i)
    for i in shan:
        var.pop(i)
    shan = []
    for i in array:
        if i[0] == str(scope):
            shan.append(i)
    for i in shan:
        array.pop(i)


def find_type():    #找到定义的类型
    now_find = now
    lei = ''
    while True:
        if fen[now_find][0] in '104 109 113 117 118':
            lei = fen[now_find][1]
            break
        now_find -= 1
    if fen[now_find-1][0] == '105':
        return False, lei
    else:
        return True, lei


def find_symbol():      #找到标识符
    now_find = now
    zhaodao = ''
    while True:
        if fen[now_find][0] == '700':
            zhaodao = fen[now_find][1]
            break
        now_find -= 1
    return zhaodao


def whether_statement(name): #检验函数是否声明
    global ge
    if name in fun:
        if ge != len(fun[name]['parameter']):
            tishi = 'line {},   column  {} :{} 函数参数传递的数量不对'.format(fen_pos[now][0], fen_pos[now][1], name)
            mean_error_add(tishi)
            #print(tishi)
    else:
        tishi = 'line {},   column  {} :函数 {} 未声明'.format(fen_pos[now][0], fen_pos[now][1], name)
        mean_error_add(tishi)
        #print(tishi)
    ge = 0



def alter_info(s):
    global info
    info = info + s + '\n'


def yu_add():   #作用域的加法
    global yu
    yu += 1


def yu_sub():   #作用域的减法
    global yu
    yu -= 1


def add_ge():   #函数变量的增加
    global ge
    ge += 1


def jian():
    global profix
    lio = len(tian)
    profix = profix[lio:]


def zeng():
    global profix
    profix += tian


def init_per_array(lastly, con, lei):   #每一个数组刚写入符号表
    global array, yu
    if str(yu) + lastly not in array and str(yu) + lastly not in var:
        array[str(yu) + lastly] = {}
        array[str(yu) + lastly]['type'] = lei
        array[str(yu) + lastly]['value'] = []
        array[str(yu) + lastly]['visible'] = con
        array[str(yu) + lastly]['dimension'] = []
    else:
        tishi = 'line {},   column  {} :{} 重复定义'.format(fen_pos[now][0], fen_pos[now][1], lastly)
        mean_error_add(tishi)
        #print(tishi)


def init_per_var(lastly, con, lei):     #每一个变量刚写入符号表
    global var, yu
    now_find = now
    if str(yu) + lastly not in var and str(yu) + lastly not in array:
        var[str(yu) + lastly] = {}
        var[str(yu) + lastly]['type'] = lei
        var[str(yu) + lastly]['value'] = 0
        var[str(yu) + lastly]['visible'] = con
    else:
        tishi = 'line {},   column  {} :{} 重复定义'.format(fen_pos[now][0], fen_pos[now][1], lastly)
        mean_error_add(tishi)
        #print(tishi)


def init_per_fun(lastly, lei):     #每一个函数量刚写入符号表
    global fun
    if lastly not in fun:
        fun[lastly] = {}
        fun[lastly]['type'] = lei
        fun[lastly]['parameter'] = []
        fun[lastly]['arrive'] = False
    else:
        tishi = 'line {},   column  {} :函数 {} 重复定义'.format(fen_pos[now][0], fen_pos[now][1], lastly)
        mean_error_add(tishi)
        #print(tishi)


def give_value2var(name):       #将变量赋值
    global var
    now_find = now
    if str(yu) + name in var:
        if var[str(yu) + name]['visible']:
            if fen[now][0] in assign[var[str(yu) + name]['type']]:
                var[str(yu) + name]['value'] = fen[now][1]
            else:
                tishi = 'line {},   column  {} :对{} 所属类型 {} 的非法赋值'.format(fen_pos[now_find][0], fen_pos[now_find][1], name, var[str(yu) + name]['type'])
                mean_error_add(tishi)
                #print(tishi)
        else:
            while fen[now_find][0] not in '104 109 113 117 118':
                now_find -= 1
            if fen[now_find-1][1] != 'const':
                tishi = 'line {},   column  {} :定义的变量 {}不可改变'.format(fen_pos[now_find][0], fen_pos[now_find][1], name)
                mean_error_add(tishi)
                #print(tishi)
            else:
                if fen[now][0] in assign[var[str(yu) + name]['type']]:
                    var[str(yu) + name]['value'] = fen[now][1]
                else:
                    tishi = 'line {},   column  {} :对{} 所属类型 {} 的非法赋值'.format(fen_pos[now_find][0], fen_pos[now_find][1], name, var[str(yu) + name]['type'])
                    mean_error_add(tishi)
                    #print(tishi)
    else:
        tishi = 'line {},   column  {} :未定义的变量 {}'.format(fen_pos[now_find][0], fen_pos[now_find][1], name)
        mean_error_add(tishi)
        #print(tishi)


def give_value2array(name):       #将数组赋值
    global array
    if str(yu) + name in array:
        if array[str(yu) + name]['visible']:
            if fen[now][0] in assign[array[str(yu) + name]['type']]:
                array[str(yu) + name]['value'].append(fen[now][1])
            else:
                tishi = 'line {},   column  {} :对{} 所属类型 {} 的非法赋值'.format(fen_pos[now][0], fen_pos[now][1], name, array[str(yu) + name]['type'])
                mean_error_add(tishi)
                #print(tishi)
        else:
            tishi = 'line {},   column  {} :定义的数组变量 {}不可改变'.format(fen_pos[now][0], fen_pos[now][1], name)
            mean_error_add(tishi)
            #print(tishi)
    else:
        tishi = 'line {},   column  {} :未定义的数组变量 {}'.format(fen_pos[now][0], fen_pos[now][1], name)
        mean_error_add(tishi)
        #print(tishi)


def give_value2fun(name, now_find):       #将函数赋参数
    global fun
    if name in fun:
        if fen[now_find][0] in '104 113 117 118 109':
            fun[name]['parameter'].append(fen[now_find][1])
        else:
            tishi = 'line {},   column  {} :非法类型声明 {}'.format(fen_pos[now_find][0], fen_pos[now_find][1], fen[now_find][1])
            mean_error_add(tishi)
            #print(tishi)
    else:
        tishi = 'line {},   column  {} :未定义的函数 {}'.format(fen_pos[now_find][0], fen_pos[now_find][1], name)
        mean_error_add(tishi)
        #print(tishi)


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


def R():
    check_it('R')
    if fen[now][1] == 'include':
        match('include')
        match('<')
        G()
        match('>')
        alter_info(profix + 'include 语句')
        ##print(profix + 'include 语句')
    elif fen[now][1] == 'define':
        match('define')
        match(token='700')
        match(token='0 400 408 416 450 500 600')
        alter_info(profix + 'define  语句')
        ##print(profix + 'define  语句')
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
        con, lei = find_type()   #找到定义的类型
        init_per_array(fen[now - 1][1], con, lei)   #写入符号表
        alter_info(profix + '{}数组定义'.format(fen[now - 1][1]))
        ##print(profix + '{}数组定义'.format(fen[now - 1][1]))
        wei_clear()
        match('[')
        if fen[now][1] != ']':
            wei_add(fen[now][1])
        else:
            wei_add('')
        Q()
        match(']')
        B()
    elif fen[now][1] != '(':
        con, lei = find_type()  # 找到定义的类型
        init_per_var(fen[now - 1][1], con, lei)  # 写入符号表
        alter_info(profix + '{}变量定义'.format(fen[now - 1][1]))
        ##print(profix + '{}变量定义'.format(fen[now - 1][1]))


def O():
    if fen[now][1] == 'const':
        match('const')


def H():
    check_it('H')
    match(token='104 109 113 117 118')


def F():
    check_it('F')
    if fen[now][1] == '(':
        name = fen[now-1][1]
        if name not in fun:
            con, lei = find_type()  # 找到定义的类型
            init_per_fun(name, lei)  # 写入函数符号表
        elif fun[name]['arrive'] == False:
            accept_0()
            compara_state(name)
        else:
            accept_0()
            tishi = 'line {},   column  {} :{} 函数重复定义'.format(fen_pos[now][0], fen_pos[now][1], name)
            mean_error_add(tishi)
            #print(tishi)
        match('(')
        K()
        match(')')
        accept_1()
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
    if fen[now - 1][1] == ']':
        name = find_symbol()
        spect_array_length(name)  # 检查并得到数组的长度
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
        name = find_symbol()
        give_value2var(name)
        match(token='0 400 408 416 450 500 600 700')


def B():
    if fen[now][1] == '[':
        match('[')
        wei_add(fen[now][1])
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
    if accept:
        name = find_function_name()
        give_value2fun(fen[name][1], now)
    H()
    I()


def I():
    if fen[now][1] == '*':
        match('*')


def Q():
    if fen[now][0] in '400 408 416':
        match(token='400 408 416')


def J():
    if fen[now][1] == ',':
        match(',')
        now_symbol = find_symbol()  #找到数组名
        give_value2array(now_symbol)    #赋值给数组
        match(token='0 400 408 416 450 500 600')
        J()
    elif fen[now][0] in '0 400 408 416 450 500 600':
        now_symbol = find_symbol()  #找到数组名
        give_value2array(now_symbol)    #赋值给数组
        match(token='0 400 408 416 450 500 600')
        J()


def C():
    global error_tishi
    check_it('C')
    if fen[now][1] == ';':
        match(';')
        name = find_function_name()
        alter_info(profix + '{}函数声明语句'.format(fen[name][1]))
        ##print(profix + '{}函数声明语句'.format(fen[name][1]))
    elif fen[now][1] == '{':
        name = find_function_name()
        set_fun_arrive(fen[name][1])  # 设置函数为已到达
        alter_info(profix + '分析{}函数'.format(fen[name][1]))
        ##print(profix + '分析{}函数'.format(fen[name][1]))
        match('{')
        zeng()
        yu_add()
        while fen[now][1] != '}':
            N()
            if now == len(fen):
                ##print('line {},   column  {}:  缺失界符'.format(fen_pos[now-1][0], fen_pos[now-1][1]))
                error_tishi += 'line {},   column  {}:  缺失界符\n'.format(fen_pos[now-1][0], fen_pos[now-1][1])
                fen.append([302, '}'])
        scope_clear(yu)  # 清除上一个作用域
        yu_sub()
        jian()
        match('}')
        alter_info(profix + '{}函数分析结束'.format(fen[name][1]))
        ##print(profix + '{}函数分析结束'.format(fen[name][1]))
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
        if fen[now][1] == '[':
            sepect_identify_array()
        elif fen[now][1] == '(':
            # name = find_function_name()
            # whether_statement(fen[name][1])  # 检验函数是否声明
            pass
        else:
            sepect_identify_var()
        wei_clear()
        B()
        if fen[now-1][1] == ']':
            spect_array()       #检查数组长度引用
        U()
    elif fen[now][0] in '0 400 408 416 450 500 600':
        match(token='0 400 408 416 450 500 600')
        U()
    elif fen[now][1] in first['U'] or fen[now][0] in symbol_first['U']:
        U()



def U():
    if fen[now][1] == '=':
        name = find_symbol()
        match('=')
        X()
        alter_info(profix + '赋值表达式')
        spect_express(name)     #检查赋值表达式左右是否类型一样
        ##print(profix + '赋值表达式')
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
        wei_clear()
        sepect_identify_array()
        B()
        if fen[now-1][1] == ']':
            spect_array()       #检查数组长度引用
    else:
        sepect_identify_var()


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
        name = find_function_name()
        whether_statement(fen[name][1])  # 检验函数是否声明


def a():
    if fen[now][1] == ',':
        match(',')
        add_ge()
        X()
        a()
    if fen[now][1] in first['X'] or fen[now][0] in symbol_first['X']:
        add_ge()
        X()
        a()


def T():
    check_it('T')
    if fen[now][0] == '120':
        alter_info(profix + '开始进行return语句分析')
        ##print(profix + '开始进行return语句分析')
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
        ##print(profix + '开始进行if语句分析')
        match(token='116')
        match('(')
        alter_info(profix + '布尔表达式分析')
        ##print(profix + '布尔表达式分析')
        t()
        alter_info(profix + '布尔表达式分析结束')
        ##print(profix + '布尔表达式分析结束')
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
        ##print(profix + 'if语句分析结束')
    else:
        jian()
        alter_info(profix + 'if语句分析结束')
        ##print(profix + 'if语句分析结束')
        N()


def p():
    check_it('p')
    if fen[now][0] == '114':
        alter_info(profix + '开始进行for语句分析')
        ##print(profix + '开始进行for语句分析')
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
        ##print(profix + 'for语句分析结束')


def q():
    check_it('q')
    if fen[now][0] == '132':
        alter_info(profix + '开始进行while语句分析')
        ##print(profix + '开始进行while语句分析')
        zeng()
        match(token='132')
        match('(')
        alter_info(profix + '布尔表达式分析')
        ##print(profix + '布尔表达式分析')
        t()
        alter_info(profix + '布尔表达式分析结束')
        ##print(profix + '布尔表达式分析结束')
        match(')')
        h()
        jian()
        alter_info(profix + 'while语句分析结束')
        ##print(profix + 'while语句分析结束')


def r():
    global error_tishi
    check_it('r')
    if fen[now][0] == '108':
        alter_info(profix + '开始进行do while语句分析')
        ##print(profix + '开始进行do while语句分析')
        zeng()
        match(token='108')
        match('{')
        yu_add()
        while fen[now][1] != '}':
            f()
            if now == len(fen):
                ##print('line {},   column  {}:  缺失界符'.format(fen_pos[now - 1][0], fen_pos[now - 1][1]))
                error_tishi += 'line {},   column  {}:  缺失界符\n'.format(fen_pos[now - 1][0], fen_pos[now - 1][1])
                fen.append([302, '}'])
        scope_clear(yu)  # 清除上一个作用域
        yu_sub()
        match('}')
        match(token='132')
        match('(')
        alter_info(profix + '布尔表达式分析')
        ##print(profix + '布尔表达式分析')
        t()
        alter_info(profix + '布尔表达式分析结束')
        ##print(profix + '布尔表达式分析结束')
        match(')')
        match(';')
        jian()
        alter_info(profix + 'do while语句分析结束')
        ##print(profix + 'do while语句分析结束')


def k():
    global error_tishi
    check_it('k')
    if fen[now][1] == '{':
        match('{')
        yu_add()
        while fen[now][1] != '}':
            N()
            if now == len(fen):
                ##print('line {},   column  {}:  缺失界符'.format(fen_pos[now - 1][0], fen_pos[now - 1][1]))
                error_tishi += 'line {},   column  {}:  缺失界符\n'.format(fen_pos[now - 1][0], fen_pos[now - 1][1])
                fen.append([302, '}'])
        scope_clear(yu)  # 清除上一个作用域
        yu_sub()
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
        yu_add()
        while fen[now][1] != '}':
            f()
            if now == len(fen):
                ##print('line {},   column  {}:  缺失界符'.format(fen_pos[now - 1][0], fen_pos[now - 1][1]))
                error_tishi += 'line {},   column  {}:  缺失界符\n'.format(fen_pos[now - 1][0], fen_pos[now - 1][1])
                fen.append([302, '}'])
        scope_clear(yu)  # 清除上一个作用域
        yu_sub()
        match('}')
    else:
        f()


def f():
    check_it('f')
    if fen[now][0] == '102':
        alter_info(profix + 'break 语句分析')
        ##print(profix + 'break 语句分析')
        match(token='102')
        match(';')
    elif fen[now][0] == '106':
        alter_info(profix + 'continue 语句分析')
        ##print(profix + 'continue 语句分析')
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
    ##print('line {},   column  {}:  unexpect {} in that position'.format(fen_pos[now][0], fen_pos[now][1], fen[now][1]))


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
                symbol_first[i].extend(['400', '408', '416'])
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
                symbol_follow[i].extend(['400', '408', '416'])
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
    global first, follow, symbol_first, symbol_follow, info, now, profix, error_tishi, mean_error
    #初始化
    mean_error = ''
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
    ##print(profix + '开始进行语法分析')
    zeng()
    while now < c:
        check_it('A')
        if now == len(fen):
            break
        A()
    jian()
    alter_info(profix + '语法分析结束')
    if 'main' not in fun:
        mean_error_add('程序中必须存在main函数')
        #print('程序中必须存在main函数')
    #print(error_tishi)
    # for i in var:
    #     #print('{} —— {}'.format(i, var[i]))
    # for i in array:
    #     #print('{} —— {}'.format(i, array[i]))
    # for i in fun:
    #     #print('{} —— {}'.format(i, fun[i]))

    ##print(profix + '语法分析结束')
    return info, error_tishi, mean_error


# jf = open('test.txt', 'r')
# s_f = jf.read()
# jf.close()
# grammar_analysis(s_f)

