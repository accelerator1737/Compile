hang = 1
lie = 1
eryuan_info = []
eryuan_info_pos = []
error_info = []
error_pos = []

def hang_add():
    global hang
    hang += 1


def lie_add(n):
    global lie
    lie += n
    
    
def new_hang():
    global hang, lie
    hang += 1
    lie = 1


def get_pos():
    global hang, lie
    return (hang, lie)


def get_dectionary():       #得到各种别码
    f = open('token.txt', 'r')
    dec = {}
    line = f.readline()
    while line:
        sp = line.split()
        dec[sp[0]] = sp[1]
        line = f.readline()
    f.close()
    return dec


def identify_symbol(s, i):     #识别标识符
    global dec
    if len(s) == 0:
        return '', ''
    jie = ['{', '}', '[', ']', '(', ')', ',', ';', '//', '/*', ':', '\n', '\t']
    yun = ['^', '%', '*', '/', '=', '!', '~', '+', '-', '&', '|', '>', '<']
    sym = ''
    status = 0
    now = s[i]
    while status != 2:
        if status == 0:     #状态0
            if ('a' <= now <= 'z') or ('A' <= now <= 'Z') or now == '_':
                status = 1
                sym += now
            else:
                break
        elif status == 1:       #状态1
            if ('a' <= now <= 'z') or ('A' <= now <= 'Z') or ('0' <= now <= '9') or now == '_':
                sym += now
            else:
                if now == ' ' or now in jie or now in yun:
                    break
                else:
                    sym += now
                    i += 1
                    while i < len(s) and (not (s[i] == ' ' or s[i] in jie or s[i] in yun)):
                        now = s[i]
                        sym += now
                        i += 1
                    if sym in dec:
                        eryu = "1({},{})".format(dec[sym], sym)
                    else:
                        eryu = "0标识符错误  {}".format(sym)
                    #print("标识符错误  {}".format(sym))
                    return sym, eryu
        i += 1
        if i >= len(s):
            break
        else:
            now = s[i]
    if sym != '':
        if sym in dec:
            eryu = "1({},{})".format(dec[sym], sym)
        else:
            eryu = "1({},{})".format(dec['symbol'], sym)
        #print("({},{})".format(dec[sym], sym)) if sym in dec else #print("({},{})".format(dec['symbol'], sym))
        return sym, eryu
    return sym, ''


def identify_annotation(s, i):     #识别注释
    global dec
    if len(s) < 2:
        return '', ''
    annotation = ''
    pre = ''
    now = s[i:i + 2]
    if now == '//':  # 识别'//'开始的注释
        i += 2
        annotation += '//'
        if i == len(s):
            # #print("注释 {}".format(annotation))
            return annotation, ''
        now = s[i]
        annotation += now
        while now != '\n':
            i += 1
            if i == len(s):
                break
            now = s[i]
            annotation += now
    elif now == '/*':  # 识别出‘/**/’
        i += 2
        annotation += '/*'
        if i == len(s):
            eryu = "0注释出错，差你妈一个*/{}".format(annotation)
            #print("注释出错，差你妈一个*/{}".format(annotation))
            return annotation, eryu
        now = s[i]
        if i + 1 == len(s):
            eryu = "0注释出错，差你妈一个*/{}".format(annotation)
            #print("注释出错，差你妈一个*/{}".format(annotation))
            return annotation, eryu
        pre = s[i + 1]
        annotation += now
        while now != '*' or pre != '/':
            i += 1
            if i + 1 == len(s):
                eryu = "0注释出错，差你妈一个*/{}".format(annotation)
                #print("注释出错，差你妈一个*/{}".format(annotation))
                return annotation + now, eryu
            now = s[i]
            pre = s[i + 1]
            annotation += now
        annotation += pre
    # if annotation != '':
    #     #print("注释 {}".format(annotation))
    return annotation, ''


def identify_char(s, i):   #识别字符常量
    global dec
    if len(s) == 0:
        return '', ''
    char_norm = ''
    status = 0
    while status != 3 or status != 4:
        now = s[i]
        if status == 0:
            if now == '\'':
                status = 1
                char_norm += now
            else:
                break
        elif status == 1:
            char_norm += now
            status = 2
        elif status == 2:
            if now == '\'':
                status = 4
                char_norm += now
            else:
                status = 3
                char_norm += now
        elif status == 3:
            eryu = "0不正常的字符常量  {}".format(char_norm)
            #print("不正常的字符常量  {}".format(char_norm))
            return char_norm, eryu
        elif status == 4:
            eryu = "1({},{})".format(dec['char'], char_norm)
            #print("({},{})".format(dec['char'], char_norm))
            return char_norm, eryu
        i += 1
        if i >= len(s):
            eryu = "0不正常的字符常量  {}".format(char_norm)
            #print("不正常的字符常量  {}".format(char_norm))
            return char_norm, eryu
    return char_norm, ''


def identify_string(s, i): #识别字符串
    global dec
    if len(s) == 0:
        return '', ''
    string_norm = ''
    status = 0
    now = s[i]
    while status != 2 or status != 3:
        if status == 0:
            if now == '\"':
                status = 1
                string_norm += now
            else:
                break
        elif status == 1:
            string_norm += now
            if now == '\"':
                status = 2
        elif status == 2:
            eryu = "1({},{})".format(dec['string'], string_norm)
            #print("({},{})".format(dec['string'], string_norm))
            return string_norm, eryu
        elif status == 3:
            eryu = "0不正常的字符串常量  {}".format(string_norm)
            #print("不正常的字符串常量  {}".format(string_norm))
            return string_norm, eryu
        i += 1
        if i >= len(s):
            status = 3
        else:
            now = s[i]
    return string_norm, ''


def identify_operation(s, i): #识别运算符
    global dec
    if len(s) == 0:
        return '', ''
    yun = ['^', '%', '*', '/', '=', '!', '~', '+', '-', '&', '|', '>', '<']
    operation = ''
    now = s[i]
    if now == '^' or now == '%' or now == '*' or now == '/' or now == '!' or now == '~' or now == '=':#可与=成双
        operation += now
        i += 1
        if i < len(s):  #如果还不到字符结尾
            now = s[i]
            if now not in yun:
                eryu = "1({},{})".format(dec[operation], operation)
                #print("({},{})".format(dec[operation], operation))
                return operation, eryu
            elif now != '=':
                i += 1
                while now in yun and i < len(s):
                    operation += now
                    now = s[i]
                    i += 1
                eryu = "0无法识别的运算符  {} ".format(operation)
                #print("无法识别的运算符  {} ".format(operation))
                return operation, eryu
            elif now == '=':
                operation += now
                i += 1
                if i < len(s):
                    now = s[i]
                    if now not in yun:      #终止条件
                        eryu = "1({},{})".format(dec[operation], operation)
                        #print("({},{})".format(dec[operation], operation))
                        return operation, eryu
                    else:
                        while now in yun and i < len(s):
                            now = s[i]
                            operation += now
                            i += 1
                        eryu = "0无法识别的运算符  {} ".format(operation)
                        #print("无法识别的运算符  {} ".format(operation))
                        return operation, eryu
                else:
                    eryu = "1({},{})".format(dec[operation], operation)
                    #print("({},{})".format(dec[operation], operation))
                    return operation, eryu
        else:   #如果到了字符最后一位
            eryu = "1({},{})".format(dec[operation], operation)
            #print("({},{})".format(dec[operation], operation))
            return operation, eryu
    elif now == '-':
        operation += now
        i += 1
        if i < len(s):
            now = s[i]
            if now == '-' or now == '=' or now == '>':
                operation += now
                i += 1
                if i < len(s):
                    now = s[i]
                    if now not in yun:  # 终止条件
                        eryu = "1({},{})".format(dec[operation], operation)
                        #print("({},{})".format(dec[operation], operation))
                        return operation, eryu
                    else:
                        while now in yun and i < len(s):
                            now = s[i]
                            operation += now
                            i += 1
                        eryu = "0无法识别的运算符  {} ".format(operation)
                        #print("无法识别的运算符  {} ".format(operation))
                        return operation, eryu
                else:
                    eryu = "1({},{})".format(dec[operation], operation)
                    #print("({},{})".format(dec[operation], operation))
                    return operation, eryu
            elif now not in yun:
                eryu = "1({},{})".format(dec[operation], operation)
                #print("({},{})".format(dec[operation], operation))
                return operation, eryu
            else:
                i += 1
                while now in yun and i < len(s):
                    now = s[i]
                    operation += now
                    i += 1
                eryu = "0无法识别的运算符  {} ".format(operation)
                #print("无法识别的运算符  {} ".format(operation))
                return operation, eryu
        else:
            eryu = "1({},{})".format(dec[operation], operation)
            #print("({},{})".format(dec[operation], operation))
            return operation, eryu
    elif now == '+':
        operation += now
        i += 1
        if i < len(s):
            now = s[i]
            if now == '+' or now == '=':
                operation += now
                i += 1
                if i < len(s):
                    now = s[i]
                    if now not in yun:  # 终止条件
                        eryu = "1({},{})".format(dec[operation], operation)
                        #print("({},{})".format(dec[operation], operation))
                        return operation, eryu
                    else:
                        while now in yun and i < len(s):
                            now = s[i]
                            operation += now
                            i += 1
                        eryu = "0无法识别的运算符  {} ".format(operation)
                        #print("无法识别的运算符  {} ".format(operation))
                        return operation, eryu
                else:
                    eryu = "1({},{})".format(dec[operation], operation)
                    #print("({},{})".format(dec[operation], operation))
                    return operation, eryu
            elif now not in yun:
                eryu = "1({},{})".format(dec[operation], operation)
                #print("({},{})".format(dec[operation], operation))
                return operation, eryu
            else:
                i += 1
                while now in yun and i < len(s):
                    now = s[i]
                    operation += now
                    i += 1
                eryu = "0无法识别的运算符  {} ".format(operation)
                #print("无法识别的运算符  {} ".format(operation))
                return operation, eryu
        else:
            eryu = "1({},{})".format(dec[operation], operation)
            #print("({},{})".format(dec[operation], operation))
            return operation, eryu
    elif now == '&' or now == '|' or now == '>' or now == '<':
        operation += now
        i += 1
        if i < len(s):
            now = s[i]
            if now == s[i-1]:       #与上一步相同
                operation += now
                i += 1
                if i < len(s):
                    now = s[i]
                    if now == '=':
                        operation += now
                        i += 1
                        if i < len(s):
                            now = s[i]
                            if now in yun:
                                while now in yun and i < len(s):
                                    operation += now
                                    i += 1
                                    now = s[i]
                                eryu = "0无法识别的运算符  {} ".format(operation)
                                #print("无法识别的运算符  {} ".format(operation))
                                return operation, eryu
                            else:
                                eryu = "1({},{})".format(dec[operation], operation)
                                #print("({},{})".format(dec[operation], operation))
                                return operation, eryu
                        else:
                            eryu = "1({},{})".format(dec[operation], operation)
                            #print("({},{})".format(dec[operation], operation))
                            return operation, eryu
                    elif now not in yun:
                        eryu = "1({},{})".format(dec[operation], operation)
                        #print("({},{})".format(dec[operation], operation))
                        return operation, eryu
                    else:
                        while now in yun and i < len(s):
                            operation += now
                            i += 1
                            now = s[i]
                        eryu = "0无法识别的运算符  {} ".format(operation)
                        #print("无法识别的运算符  {} ".format(operation))
                        return operation, eryu
                else:
                    eryu = "1({},{})".format(dec[operation], operation)
                    #print("({},{})".format(dec[operation], operation))
                    return operation, eryu
            elif now == '=':
                operation += now
                i += 1
                if i < len(s):
                    now = s[i]
                    if now in yun:
                        while now in yun and i < len(s):
                            operation += now
                            i += 1
                            now = s[i]
                        eryu = "0无法识别的运算符  {} ".format(operation)
                        #print("无法识别的运算符  {} ".format(operation))
                        return operation, eryu
                    else:
                        eryu = "1({},{})".format(dec[operation], operation)
                        #print("({},{})".format(dec[operation], operation))
                        return operation, eryu
                else:
                    eryu = "1({},{})".format(dec[operation], operation)
                    #print("({},{})".format(dec[operation], operation))
                    return operation, eryu
            elif now not in yun:
                eryu = "1({},{})".format(dec[operation], operation)
                #print("({},{})".format(dec[operation], operation))
                return operation, eryu
            else:
                while now in yun and i < len(s):
                    operation += now
                    i += 1
                    now = s[i]
                eryu = "0无法识别的运算符  {} ".format(operation)
                #print("无法识别的运算符  {} ".format(operation))
                return operation, eryu
        else:
            eryu = "1({},{})".format(dec[operation], operation)
            #print("({},{})".format(dec[operation], operation))
            return operation, eryu
    return '', ''


def is_zheng(number):       #判断指数是整数还是浮点数
    if 'e' in number:
        fen = number.split('e')
    elif 'E' in number:
        fen = number.split('E')
    if fen[0] != '-':
        if fen[0] == '+':
            fen[0] = fen[0][1:]
        pass
    return True


def identify_number(s, i):      #识别数字
    global dec
    if len(s) == 0:
        return '', ''
    jie = ['{', '}', '[', ']', '(', ')', ',', ';', '\'', '//', '/*', '_', ':', ' ', '\n', '\t']
    yun = ['^', '%', '*', '/', '=', '!', '~', '+', '-', '&', '|', '>', '<']
    number = ''
    now = s[i]
    status = 0
    while True:
        if status == 0:     #状态0
            if now == '0':
                status = 2
            elif now == '.':
                status = 5
            elif '1' <= now <= '9':
                status = 1
            else:
                break
        elif status == 1:   #状态1
            number += now
            i += 1
            if i >= len(s):
                status = 17
            else:
                now = s[i]      #判断下一个字符的状态
                if now == '.':
                    status = 5
                elif now in jie or now in yun:
                    status = 17
                elif '0' <= now <= '9':
                    status = 1
                elif now == 'E' or now == 'e':
                    status = 7
                else:
                    status = 16
        elif status == 2:
            number += now
            i += 1
            if i >= len(s):
                status = 19
            else:
                now = s[i]  # 判断下一个字符的状态
                if '0' <= now <= '7':
                    status = 2
                elif '8' <= now <= '9':
                    status = 4
                elif now == '.':
                    status = 5
                elif now in jie or now in yun:
                    status = 19
                elif now == 'x' or now == 'X':
                    status = 3
                else:
                    status = 16
        elif status == 3:
            number += now
            i += 1
            if i >= len(s):
                if number == '0x' or number == '0X':
                    eryu = "0不完整的十六进制数  {}".format(number)
                    #print("不完整的十六进制数  {}".format(number))
                    return number, eryu
                else:
                    status = 20
            else:
                now = s[i]  # 判断下一个字符的状态
                if '0' <= now <= '9' or 'a' <= now <= 'f' or 'A' <= now <= 'F':
                    status = 3
                elif now in jie or now in yun:
                    if number == '0x' or number == '0X':
                        eryu = "0不完整的十六进制数  {}".format(number)
                        #print("不完整的十六进制数  {}".format(number))
                        return number, eryu
                    else:
                        status = 20
                else:
                    status = 16
        elif status == 4:
            number += now
            i += 1
            if i >= len(s):
                eryu = "0错误的八进制数  {}".format(number)
                #print("错误的八进制数  {}".format(number))
                return number, eryu
            else:
                now = s[i]  # 判断下一个字符的状态
                if now == '.':
                    status = 5
                elif '0' <= now <= '9':
                    status = 4
                elif now in jie or now in yun:
                    eryu = "0错误的八进制数  {}".format(number)
                    #print("错误的八进制数  {}".format(number))
                    return number, eryu
                else:
                    status = 16
        elif status == 5:
            number += now
            i += 1
            if i >= len(s):
                if number == '.':
                    eryu = "0不能仅含小数点  {}".format(number)
                    #print("不能仅含小数点  {}".format(number))
                    return number, eryu
                else:
                    status = 17
            else:
                now = s[i]  # 判断下一个字符的状态
                if '0' <= now <= '9':
                    status = 6
                elif now in jie or now in yun:
                    if number == '.':
                        eryu = "0不能仅含小数点  {}".format(number)
                        #print("不能仅含小数点  {}".format(number))
                        return number, eryu
                    else:
                        status = 18
                else:
                    status = 16
        elif status == 6:
            number += now
            i += 1
            if i >= len(s):
                status = 18
            else:
                now = s[i]  # 判断下一个字符的状态
                if '0' <= now <= '9':
                    status = 6
                elif now == 'e' or now == 'E':
                    status = 7
                elif now in jie or now in yun:
                    status = 18
                else:
                    status = 16
        elif status == 7:
            number += now
            i += 1
            if i >= len(s):
                eryu = "0E后应含有数字  {}".format(number)
                #print("E后应含有数字  {}".format(number))
                return number, eryu
            else:
                now = s[i]  # 判断下一个字符的状态
                if now == '+' or now == '-':
                    status = 8
                elif '0' <= now <= '9':
                    status = 9
                else:
                    status = 16
        elif status == 8:
            number += now
            i += 1
            if i >= len(s):
                eryu = "0E后应含有数字  {}".format(number)
                #print("E后应含有数字  {}".format(number))
                return number, eryu
            else:
                now = s[i]  # 判断下一个字符的状态
                if '0' <= now <= '9':
                    status = 9
                else:
                    status = 16
        elif status == 9:
            number += now
            i += 1
            if i >= len(s):
                status = 21
            else:
                now = s[i]  # 判断下一个字符的状态
                if '0' <= now <= '9':
                    status = 9
                elif now in jie or now in yun:
                    status = 21
                else:
                    status = 16
        elif status == 16:      #处理错误状态
            if now in jie or now in yun:
                eryu = "0无法识别的数值  {}".format(number)
                #print("无法识别的数值  {}".format(number))
                return number, eryu
            number += now
            i += 1
            while i < len(s) and s[i] not in jie and s[i] not in yun:
                now = s[i]
                number += now
                i += 1
            eryu = "0无法识别的数值  {}".format(number)
            #print("无法识别的数值  {}".format(number))
            return number, eryu
        elif status == 17:      #处理整数态
            eryu = "1({},{})".format(dec['zheng'], number)
            #print("({},{})".format(dec['zheng'], number))
            return number, eryu
        elif status == 18:      #处理小数态
            eryu = "1({},{})".format(dec['fu'], number)
            #print("({},{})".format(dec['fu'], number))
            return number, eryu
        elif status == 19:      #处理八进制数态
            eryu = "1({},{})".format(dec['8'], number)
            #print("({},{})".format(dec['8'], number))
            return number, eryu
        elif status == 20:      #处理十六进制数态
            eryu = "1({},{})".format(dec['16'], number)
            #print("({},{})".format(dec['16'], number))
            return number, eryu
        elif status == 21:      #处理指数态
            if is_zheng(number):
                eryu = "1({},{})".format(dec['zheng'], number)
                #print("({},{})".format(dec['zheng'], number))
                return number, eryu
            else:
                eryu = "1({},{})".format(dec['fu'], number)
                #print("({},{})".format(dec['fu'], number))
                return number, eryu
    return number, ''


def identify_boundary(s, i):
    global dec
    if len(s) == 0:
        return '', ''
    jie = ['{', '}', '[', ']', '(', ')', ',', ';', ':', '#']
    if s[i] in jie:
        eryu = "1({},{})".format(dec[s[i]], s[i])
        #print("({},{})".format(dec[s[i]], s[i]))
        return s[0], eryu
    else:
        return '', ''


def identify_other(s, i):
    global dec
    if len(s) == 0:
        return '', ''
    jie = [' ', '\n', '\t']
    bo = ['{', '}', '[', ']', '(', ')', ',', ';', '\'', '\"', '//', '/*', '_', ':', '#']
    yun = ['^', '%', '*', '/', '=', '!', '~', '+', '-', '&', '|', '>', '<']
    if s[i] in jie:
        return s[i], ''
    elif not (('a' <= s[i] <= 'z') or ('A' <= s[i] <= 'Z') or ('0' <= s[i] <= '9') or s[i] == '_' or s[i] in bo or s[i] in yun):
        eryu = "0无法识别的字符  {} ".format(s[i])
        #print("无法识别的字符  {}".format(s[i]))
        return s[i], eryu
    else:
        return '', ''


f = open('token.txt', 'r')
dec = {}
line = f.readline()
while line:
    sp = line.split()
    dec[sp[0]] = sp[1]
    line = f.readline()
f.close()


def get_something(ss, eryu):
    global eryuan_info, eryuan_info_pos, error_info, error_pos
    if ss == '\n':
        new_hang()
        return
    if eryu != '':
        if eryu[0] == '0':        #错误信息
            error_info.append(eryu[1:])
            error_pos.append(get_pos())
        elif eryu[0] == '1':
            eryuan_info.append(eryu[2:-1])
            eryuan_info_pos.append(get_pos())
    lie_add(len(ss))


def get_file_to_cifa(s_f):
    global eryuan_info, eryuan_info_pos, error_info, error_pos, hang, lie
    eryuan_info = []
    eryuan_info_pos = []
    error_info = []
    error_pos = []
    hang = 1
    lie = 1
    j = 0
    while j < len(s_f):
        ss, eryu = identify_string(s_f, j)
        j += len(ss)
        get_something(ss, eryu)
        if j == len(s_f):
            break
        ss, eryu = identify_annotation(s_f, j)
        j += len(ss)
        get_something(ss, eryu)
        if j == len(s_f):
            break
        ss, eryu = identify_operation(s_f, j)
        j += len(ss)
        get_something(ss, eryu)
        if j == len(s_f):
            break
        ss, eryu = identify_number(s_f, j)
        j += len(ss)
        get_something(ss, eryu)
        if j == len(s_f):
            break
        ss, eryu = identify_boundary(s_f, j)
        j += len(ss)
        get_something(ss, eryu)
        if j == len(s_f):
            break
        ss, eryu = identify_char(s_f, j)
        j += len(ss)
        get_something(ss, eryu)
        if j == len(s_f):
            break
        ss, eryu = identify_symbol(s_f, j)
        j += len(ss)
        get_something(ss, eryu)
        if j == len(s_f):
            break
        ss, eryu = identify_other(s_f, j)
        j += len(ss)
        get_something(ss, eryu)
        if j == len(s_f):
            break
    return eryuan_info, eryuan_info_pos, error_info, error_pos

# while len(s_f) > 0:
#     ss = identify_other(s_f, 0)
#     s_f = s_f[len(ss):]
#     if len(s_f) == 0:
#         break
#     ss = identify_string(s_f, 0)
#     s_f = s_f[len(ss):]
#     if len(s_f) == 0:
#         break
#     ss = identify_annotation(s_f, 0)
#     s_f = s_f[len(ss):]
#     if len(s_f) == 0:
#         break
#     ss = identify_operation(s_f, 0)
#     s_f = s_f[len(ss):]
#     if len(s_f) == 0:
#         break
#     ss = identify_number(s_f, 0)
#     s_f = s_f[len(ss):]
#     if len(s_f) == 0:
#         break
#     ss = identify_boundary(s_f, 0)
#     s_f = s_f[len(ss):]
#     if len(s_f) == 0:
#         break
#     ss = identify_char(s_f, 0)
#     s_f = s_f[len(ss):]
#     if len(s_f) == 0:
#         break
#     ss = identify_symbol(s_f, 0)
#     s_f = s_f[len(ss):]
#     if len(s_f) == 0:
#         break
# get_file_to_cifa("123\n58 @ sdfa \n 892 596 3.2")

