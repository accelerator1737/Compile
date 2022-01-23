import middle_code_back as mc
import re


es_idx = -2

def transfer(arg1, arg2, arg3):#将 A B result 转换成 ds:[_A]  ds:[_B]， es:{_result]
    if str(arg1).isidentifier():
        arg1 = 'DS:[_{}]'.format(arg1)
    if str(arg2).isidentifier():
        arg2 = 'DS:[_{}]'.format(arg2)
    if str(arg3).isidentifier():
        arg3 = 'DS:[_{}]'.format(arg3)
    return arg1, arg2, arg3

def gen_assem_code(code, idx):#生成一条汇编代码
    global es_idx
    if code[0] == '+':
        # 加法
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tADD AX,{}\n\tMOV {},AX;\n'.format(arg1, arg2, res)

    elif code[0] == '-':
        # 减法
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tSUB AX,{}\n\tMOV {},AX;\n'.format(arg1, arg2, res)

    elif code[0] == '*':
        # 乘法
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tMOV BX,{}\n\tMUL BX\n\tMOV {},AX\n'.format(arg1, arg2, res)

    elif code[0] == '/':
        # 除法
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tMOV DX,0\n\tMOV BX,{}\n\tDIV BX\n\tMOV {},AX\n'.format(arg1, arg2, res)

    elif code[0] == '%':
        # 求余数
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tMOV DX,0\n\tMOV BX,{}\n\tDIV BX\n\tMOV {},DX\n'.format(arg1, arg2, res)

    elif code[0] == '<':
        # 小于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        tiao = '_' + str(idx) + '_n'
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJB {}\n\tMOV DX,0\n{}:MOV {},DX\n'.format(arg1, arg2, tiao, tiao, res)

    elif code[0] == '>=':
        # 不小于把 res 置为 0， 否则为 1
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        tiao = '_' + str(idx) + '_n'
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJNB {}\n\tMOV DX,0\n{}:MOV {},DX\n'.format(arg1, arg2, tiao, tiao, res)

    elif code[0] == '>':
        # 大于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        tiao = '_' + str(idx) + '_n'
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJA {}\n\tMOV DX,0\n{}:MOV {},DX\n'.format(arg1, arg2, tiao, tiao, res)

    elif code[0] == '<=':
        # 不大于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        tiao = '_' + str(idx) + '_n'
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJNA {}\n\tMOV DX,0\n{}:MOV {},DX\n'.format(arg1, arg2, tiao, tiao, res)

    elif code[0] == '==':
        # 等于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        tiao = '_' + str(idx) + '_n'
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJE {}\n\tMOV DX,0\n{}:MOV {},DX\n'.format(arg1, arg2, tiao, tiao, res)

    elif code[0] == '!=':
        # 不等于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        tiao = '_' + str(idx) + '_n'
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJNE {}\n\tMOV DX,0\n{}:MOV {},DX\n'.format(arg1, arg2, tiao, tiao, res)

    elif code[0] == '&&':
        # 等于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        tiao = '_' + str(idx) + '_n'
        assem_code = '\tMOV DX,0\n\tMOV AX,{}\n\tCMP AX,0\n\tJE {}\n\tMOV AX,{}\n\tCMP AX,0\n\tJE _' \
                     'AND\n\tMOV DX,1\n{}:MOV {},DX\n'.format(arg1, tiao, arg2, tiao, res)

    elif code[0] == 'jnz':
        # 等于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        tiao = '_' + str(idx) + '_n'
        assem_code = '\tMOV AX,{}\n\tCMP AX,0\n\tJE {}\n\tJMP far ptr {}\n{}:NOP\n'.format(arg1, tiao, res, tiao)

    elif code[0] == 'para':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tPUSH AX\n'.format(arg1)

    elif code[0] == 'call':
        global es_idx
        arg1, arg2, res = code[1], code[2], code[3]
        arg1 = '_' + str(arg1)
        es_idx += 2
        assem_code = '\tCALL {}\n\tMOV ES:[{}],AX\n'.format(arg1, es_idx)

    elif code[0] == 'ret':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        if arg1 != '':
            assem_code = '\tMOV AX,{}\n\tMOV SP,BP\n\tPOP BP\n\tRET\n'.format(arg1)
        else:
            assem_code = '\tMOV SP,BP\n\tPOP BP\n\tRET\n'.format(arg1)

    elif code[0] == '||':
        arg1, arg2, T = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,0\n\tJNE _OR\n\tMOV AX,{}\n\tCMP AX,0\n\t' \
                     'JNE _OR\n\tMOV DX,0\n\t_OR:MOV {},DX\n'.format(arg1, arg2, T)
    elif code[0] == '!':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,0\n\tJE _NOT\n\tMOV DX,0\n\t_NOT:MOV {},DX\n'.format(arg1, res)

    elif code[0] == 'j':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        assem_code = '\tJMP far ptr {}\n'.format(res)

    elif code[0] == 'jz':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        tiao = '_' + str(idx) + '_n'
        assem_code = '\tMOV AX,{}\n\tCMP AX,0\n\tJNE {}\n\tJMP far ptr {}\n{}:NOP\n'.format(arg1, tiao, res, tiao)

    elif code[0] == '=':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        if code[1] == 'return_v':
            arg1 = 'ES:[{}]'.format(es_idx)
        # res = '_' + str(res)
        assem_code = '\tMOV AX,{}\n\tMOV {}, AX\n'.format(arg1, res)

    elif code[0] == 'sys':
        assem_code = 'QUIT: MOV AH, 4CH\n\tint 21h\n'
        return assem_code
    elif str(code[0]).isidentifier() and code[0] != 'main':
        idx = code[0]
        assem_code = '\tPUSH BP\n\tMOV BP,SP\n\tSUB SP,2\n'
    elif code[0] == 'main':
        assem_code = ('assume cs:code,ds:data,ss:stack,es:extended\n'
'extended segment\n'
'    db 1024 dup (0)\n'
'extended ends\n'
'stack segment\n'
'    db 1024 dup (0)\n'
'stack ends\n'
'data segment\n'
'    _buff_p db 256 dup (24h)\n'
'    _buff_s db 256 dup (0)\n'
"    _msg_p db 0ah,'Output:',0\n"
"    _msg_s db 0ah,'Input:',0\n"
'data ends\n'
'code segment\n'
'start:	mov ax,extended\n'
'    mov es,ax\n'
'    mov ax,stack\n'
'    mov ss,ax\n'
'    mov sp,1024\n'
'    mov bp,sp\n'
'    mov ax,data\n'
'    mov ds,ax\n')
        return assem_code
    else:
        assem_code = ''
    if assem_code != '':
        assem_code = '_'+str(idx)+':\n'+assem_code
    return assem_code


def alternative(list1):       #替换其中的中间变量
    p = re.compile('\[(.*?)\]', re.S)
    s = ''
    for i in list1:
        s += i
    linklist = re.findall(p, s)
    list2 = list(set(linklist))
    a = list1[0]
    b = a.split('\n')
    start = 2
    dic = {}
    for i in list2:
        if i.isidentifier() and len(i) > 1 and not ((i[1] == 'T' or i[1] == 'R') and i[2:].isdigit()):
            b.insert(12, '    {} dw 0'.format(i))
        elif len(i) > 1 and (i[1] == 'T' or i[1] == 'R') and i[2:].isdigit():
            dic[i] = start
            start += 2
    i = 0
    while i < len(b):
        b[i] += '\n'
        i += 1
    list1.insert(0, ''.join(b))
    list1.pop(1)
    i = 0
    while i < len(list1):
        for j in dic:
            list1[i] = list1[i].replace(j, str(dic[j]))
        i += 1
    return list1


def gen_assemcodes(codes):
    global es_idx
    es_idx = -2
    assem_codes = []
    for i, code in enumerate(codes):
        assem_code = gen_assem_code(code, i+1)
        if code[0] == 'para' and codes[i-1][0] == 'call':
            assem_code = assem_code.replace('DS:[_{}]'.format(code[1]), 'ES:[{}]'.format(es_idx))
        assem_codes.append(assem_code)
    ff = open('read_write.txt', 'r')
    s = ff.read()
    ff.close()
    assem_codes = alternative(assem_codes)       #替换其中的中间变量
    assem_codes.append(s)
    assem_codes.append('\ncode ends\nend start')
    f = open('result.txt', 'w')
    for i in assem_codes:
        f.write(i)
    f.close()
    return assem_codes

# jf = open('test.txt', 'r')
# s_f = jf.read()
# jf.close()
# mean_error, four_formula = mc.grammar_analysis(s_f)
# gen_assemcodes(four_formula)