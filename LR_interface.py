import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import copy
from tkinter.messagebox import showerror, showinfo

vi = {} #存储分析表信息
sequent = []    #存储分析表中的表头信息顺序
step = 1
gramma = []     #去除|关系的文法
start = ''
status = []
no_end_symbol = []  #非终结符
end_symbol = [] #终结符
flag = 0
s_stack = ''
status_stack = []
symbol_stack = []


def open_file(text):
    global filename
    try:
        filename = askopenfilename()
        f = open(filename, "r")  # 读取选择文件的内容
        txt1 = f.read()
        f.close()
        text.delete('1.0', 'end')
        text.insert(tk.END, txt1)
    except:
        pass


def save_file(text1):
    global filename
    if filename == '':
        file = asksaveasfilename(title=u'另存为', defaultextension='.txt')
        txt1 = text1.get('1.0', 'end-1c')  # 得到文本框中所有的内容
        f = open(file, "w")
        f.write(txt1)
        f.close()
    else:
        txt1 = text1.get('1.0', 'end-1c')  # 得到文本框中所有的内容
        f = open(filename, "w")
        f.write(txt1)
        f.close()


def text2sentence(t):       #字符串转文法列表，并去除|关系
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


def define_LR(text, b4):        #点击确定文法
    global gramma, start
    eassy = text.get('1.0', 'end')
    start = eassy[0]
    while eassy[-1] == '\n':
        eassy = eassy[0:-1]
    gramma = text2sentence(eassy)
    get_no_end(gramma)
    get_end(gramma)
    b4.config(state=tk.NORMAL)


def back_point(hou):    #将.号向右移一位
    index = hou.find('.')
    hou = hou.replace('.', '')
    list_hou = list(hou)
    list_hou.insert(index+1, '.')
    str_i = ''.join(list_hou)
    return str_i


def get_end(fen):    #得到终结符
    global end_symbol, no_end_symbol
    end_symbol = []
    for i in fen:
        hou = i.split('->')[1]
        for j in hou:
            if j not in no_end_symbol:
                end_symbol.append(j)
    end_symbol = set(end_symbol)
    end_symbol = list(end_symbol)


def get_no_end(fen):    #得到非终结符
    global no_end_symbol
    no_end_symbol = []
    for i in fen:
        no_end_symbol.append(i.split('->')[0])
    no_end_symbol = set(no_end_symbol)
    no_end_symbol = list(no_end_symbol)


#去掉重复项
def remove_follow_repeat(list1):
    s = set(list1)
    l = list(s)
    list1 = l
    return list1


def find_begin(next):#找到以这个非终结符开头的文法加进去
    global gramma, no_end_symbol
    fan = []
    len_g = 0
    for i in gramma:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        if qian == next:
            fan.append('{}->{}'.format(qian, hou))
    while True:
        dai = copy.deepcopy(fan)
        for j in dai:
            hou1 = j.split('->')[1]
            if hou1[0] in no_end_symbol:
                for i in gramma:
                    qian = i.split('->')[0]
                    hou = i.split('->')[1]
                    if qian == hou1[0]:
                        fan.append('{}->{}'.format(qian, hou))
        fan = remove_follow_repeat(fan)
        if len_g == len(fan):
            break
        else:
            len_g = len(fan)
    hui = []
    for i in fan:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        hui.append('{}->.{}'.format(qian, hou))
    return hui


def create_son(s):    #创建子集
    global status, end_symbol, no_end_symbol
    fen = []    #状态
    hu = []     #弧
    zhi = []    #本状态弧指向
    wen = []    #本状态的文法
    fen.append(zhi)
    fen.append(wen)
    fen.append(hu)
    status.append(fen)
    qian = s.split('->')[0]
    hou = s.split('->')[1]
    if hou[-1] == '.':  #点到末尾，不能创建子集了
        return False, ''
    else:
        if '.' not in hou:      #没有点，是最开始的开始文法
            hou = '.' + hou
        else:
            hou = back_point(hou)
        wen.append('{}->{}'.format(qian, hou))
        if hou[0] == '.':
            hu_zhi = ''
        else:
            hu_zhi = hou[hou.find('.') - 1]
        if hou[-1] == '.':
            return True, hu_zhi
        index = hou.find('.')
        next = hou[index+1]
        if next in end_symbol:
            return True, hu_zhi
        elif next in no_end_symbol:
            tian = find_begin(next) #找到以这个非终结符开头的文法加进去
            if len(tian) > 0:
                wen.extend(tian)
            return True, hu_zhi


def equate_set(j):   #集合查重,ture为重合
    global status
    ben = status[j][1]
    ce = status[-1][1]
    if len(ben) == len(ce):
        n = [x for x in ben if x in ce]  # 两个列表表都存在
        if len(n) == len(ben):
            return True
    return False


def equate_list(list1, list2):  #判断两列表元素是否相同
    a = [x for x in list1 if x in list2]  # 两个列表表都存在
    b = [y for y in (list1 + list2) if y not in a]  # 两个列表中的不同元素
    if len(b) > 0:
        return False
    return True


def tianjia(j, hu):  #添加元素，若增加的状态前面有，则指向前面，否则新添加
    global status
    end_status = status[-1]
    fl = 0
    for i in range(len(status) - 1):
        if equate_list(status[i][1], end_status[1]):
            fl = 1
            break
    if fl == 0: #不含与添加状态相等的状态
        status[j][0].append(len(status) - 1)
        status[j][2].append(hu)
    else:
        status.pop(-1)
        status[j][0].append(i)
        status[j][2].append(hu)


def get_len_max():  #得到最大的长度
    global status
    len_max = 0
    for i in status:
        len_now = len(i[1])
        if len_now > len_max:
            len_max = len_now
    return len_max


def show_status(tree, b4):     #点击状态信息
    global gramma, status
    status = []
    create_son('φ->{}'.format(start))
    j = 0
    while j < len(status):
        son_status = status[j]
        for i in son_status[1]:
            t, hu = create_son(i)
            if not t:
                status.pop(-1)
            elif equate_set(j):   #集合相等，指向自己
                status.pop(-1)
                status[j][0].append(j)
                status[j][2].append(hu)
            else:
                tianjia(j, hu)       #添加元素，若增加的状态前面有，则指向前面，否则新添加
        j += 1
    # 删除原来的内容
    tree.delete(*tree.get_children())
    tree['columns'] = ()
    xu = []
    for i in range(get_len_max()):
        xu.append('NO.' + str(i+1))
    tree['columns'] = tuple(xu)
    for i in xu:
        tree.heading(i, text=i)
        tree.column(i, width=80, anchor='center')
    tree.column("#0", width=50)
    tree.heading('#0', text='状态')
    j = 0
    for i in status:
        tree.insert('', j, text=j, value=tuple(i[1]))
        j += 1
    b4.config(state=tk.NORMAL)


def vi_init():      #初始化vi
    global vi, status
    vi = {}
    for i in range(len(status)):
        vi[i] = []
        for j in range(len(sequent)):
            vi[i].append('')


def find_term(s):       #找到规约串的grammar下标号
    global gramma
    s = s.replace('.', '')
    for i in range(len(gramma)):
        if gramma[i] == s:
            return i
    return -1


def is_acc(s):    #判断是否是接收态
    global start
    if len(s) == 1:
        str_s = s[0]
        str_s = str_s.replace('.', '')
        if str_s == 'φ->{}'.format(start):
            return True
    return False


def LR_analyze_table(tree, b7, b8):   #LR分析表
    global sequent, end_symbol, no_end_symbol, status, gramma
    print(gramma)
    sequent = []
    sequent.extend(end_symbol)
    sequent.append('#')
    sequent.extend(no_end_symbol)
    total_end_symbol = copy.deepcopy(end_symbol)
    total_end_symbol.append('#')
    vi_init()   #初始化vi
    for i in range(len(status)):
        if is_acc(status[i][1]):    #判断是否是接收态
            vi[i][sequent.index('#')] = 'acc'
            continue
        if len(status[i][0]) > 0:
            for j in range(len(status[i][0])):
                if status[i][2][j] in end_symbol: #箭头指标为终结符
                    vi[i][sequent.index(status[i][2][j])] = 'S' + str(status[i][0][j])
                elif status[i][2][j] in no_end_symbol:
                    vi[i][sequent.index(status[i][2][j])] = str(status[i][0][j])
        else:
            r_index = find_term(status[i][1][0])       #找到规约串的grammar下标号
            for j in total_end_symbol:
                vi[i][sequent.index(j)] = 'r' + str(r_index)
    # 删除原来的内容
    tree.delete(*tree.get_children())
    tree['columns'] = ()
    xu = []
    for i in sequent:
        xu.append(i)
    tree['columns'] = tuple(xu)
    for i in xu:
        tree.heading(i, text=i)
        tree.column(i, width=50, anchor='center')
    tree.column("#0", width=70)
    tree.heading('#0', text='LR分析表')
    j = 0
    for i in range(len(status)):
        tree.insert('', j, text=j, value=tuple(vi[i]))
        j += 1
    b7.config(state=tk.NORMAL)
    b8.config(state=tk.NORMAL)


def terms(num):
    global gramma, status_stack, s_stack, vi, symbol_stack, sequent
    guiyue = gramma[num]
    gui_to = guiyue.split('->')[0]
    gui = guiyue.split('->')[1]
    len_gui = len(gui)
    len_symbol = len(symbol_stack)
    len_status = len(status_stack)
    symbol_stack = symbol_stack[:len_symbol-len_gui]
    symbol_stack += gui_to
    status_stack = status_stack[:len_status-len_gui]
    now_status = status_stack[-1]
    status_stack.append(int(vi[now_status][sequent.index(gui_to)]))
    return guiyue



def one2end(s, tree):
    global status_stack, s_stack, vi, symbol_stack, flag, end_symbol, no_end_symbol, step
    flag = 0
    symbol_stack = '#'
    status_stack = [0]
    s_stack = s + '#'
    step = 1
    # 删除原来的内容
    tree.delete(*tree.get_children())
    tree['columns'] = ()
    h = ('状态栈', '符号栈', '剩余输入串', '说明')
    tree['columns'] = h
    tree.column("#0", width=60)
    tree.heading('#0', text='步骤')
    shi = '初始化'
    tree.insert('', step - 1, text=str(step), value=(str(status_stack), symbol_stack, s_stack, shi))
    step += 1
    for i in h:
        tree.heading(i, text=i)
        tree.column(i, width=110, anchor='center')
    while True:
        now_symbol = s_stack[0]
        now_status = status_stack[-1]
        if now_symbol not in end_symbol and now_symbol != '#':
            shi = '拒取'
            break
        if vi[now_status][sequent.index(now_symbol)] != '':
            action = vi[now_status][sequent.index(now_symbol)]
            if action == 'acc':
                shi = '接受'
                break
            if now_symbol in end_symbol or now_symbol == '#':
                if action[0] == 'S':
                    next_status = int(action[1:])
                    status_stack.append(next_status)
                    symbol_stack += now_symbol
                    s_stack = s_stack[1:]
                    shi = '移进'
                elif action[0] == 'r':
                    shi = terms(int(action[1:]))
                    shi += '规约'
        else:
            shi = '拒取'
            break
        tree.insert('', step - 1, text=str(step), value=(str(status_stack), symbol_stack, s_stack, shi))
        step += 1
    if shi == '拒取':
        tree.insert('', step - 1, text=str(step), value=(str(status_stack), symbol_stack, s_stack, shi))
    else:
        tree.insert('', step - 1, text=str(step), value=(str(status_stack), symbol_stack, s_stack, shi))


def one2one(s, tree):
    global status_stack, s_stack, vi, symbol_stack, flag, end_symbol, no_end_symbol, step
    if flag == 0:
        symbol_stack = '#'
        status_stack = [0]
        s_stack = s + '#'
        step = 1
        # 删除原来的内容
        tree.delete(*tree.get_children())
        tree['columns'] = ()
        h = ('状态栈', '符号栈', '剩余输入串', '说明')
        tree['columns'] = h
        tree.column("#0", width=60)
        tree.heading('#0', text='步骤')
        shi = '初始化'
        tree.insert('', step - 1, text=str(step), value=(str(status_stack), symbol_stack, s_stack, shi))
        step += 1
        flag = 1
        for i in h:
            tree.heading(i, text=i)
            tree.column(i, width=110, anchor='center')
    elif flag == 1:
        now_symbol = s_stack[0]
        now_status = status_stack[-1]
        if now_symbol not in end_symbol and now_symbol != '#':
            shi = '拒取'
            flag = 3
        if vi[now_status][sequent.index(now_symbol)] != '':
            action = vi[now_status][sequent.index(now_symbol)]
            if action == 'acc':
                shi = '接受'
                flag = 2
            if now_symbol in end_symbol or now_symbol == '#':
                if action[0] == 'S':
                    next_status = int(action[1:])
                    status_stack.append(next_status)
                    symbol_stack += now_symbol
                    s_stack = s_stack[1:]
                    shi = '移进'
                elif action[0] == 'r':
                    shi = terms(int(action[1:]))
                    shi += '规约'
        else:
            shi = '拒取'
            flag = 3
        tree.insert('', step - 1, text=str(step), value=(str(status_stack), symbol_stack, s_stack, shi))
        step += 1
    if flag == 2:
        showinfo(title="完成", message='分析已完成')
        flag = 0
    if flag == 3:
        showerror(title="出错", message='分析已完成，输入表达式与文法不匹配')
        flag = 0


def start_interface():
    win = tk.Tk()
    win.geometry("{}x{}".format(900, 600))
    win.title('LR分析法')
    win.resizable(width=False, height=False)
    frame1 = tk.Frame(win, bd=2, width=900, height=50, relief='groove')
    frame2 = tk.Frame(win, bd=2, width=360, height=145, relief='groove')
    label1 = tk.Label(win, text='原始文法：请输入形如A->BC的LL(1)文法，空串用ε表示')
    frame3 = tk.Frame(win, bd=2, width=360, height=310, relief='groove')
    frame5 = tk.Frame(win, bd=2, width=540, height=215, relief='groove')
    label2 = tk.Label(win, text='分析句子')
    e1 = tk.Entry(win, width=65)
    b5 = ttk.Button(win, text='显示状态信息', state=tk.DISABLED, command=lambda: show_status(tree1, b4))
    b7 = ttk.Button(win, text='一键显示', state=tk.DISABLED, command=lambda: one2end(e1.get(), tree4))
    b8 = ttk.Button(win, text='单步显示', state=tk.DISABLED, command=lambda: one2one(e1.get(), tree4))
    frame6 = tk.Frame(win, bd=2, width=540, height=235, relief='groove')

    # frame2的部件
    text1 = tk.Text(frame2, font=('Consolas', 10), wrap='none')
    # frame2的布局
    text1.place(x=0, y=0, relwidth=1 - 17 / 360, relheight=1 - 17 / 145)
    sc1 = tk.Scrollbar(frame2, orient='horizon', command=text1.xview)
    sc1.place(relx=0, rely=1, relwidth=1 - 17 / 360, height=17, anchor='sw')
    sc2 = tk.Scrollbar(frame2, orient='vertical', command=text1.yview)
    sc2.place(relx=1, rely=0, width=17, relheight=1 - 17 / 145, anchor='ne')
    text1.configure(xscrollcommand=sc1.set)
    text1.configure(yscrollcommand=sc2.set)

    # frame3的部件
    tree1 = ttk.Treeview(frame3)  # 表格
    # frame3的布局
    tree1.place(x=0, y=0, relwidth=1 - 17 / 360, relheight=1 - 17 / 310)
    sc3 = tk.Scrollbar(frame3, orient='horizon', command=tree1.xview)
    sc3.place(relx=0, rely=1, relwidth=1 - 17 / 360, height=17, anchor='sw')
    sc4 = tk.Scrollbar(frame3, orient='vertical', command=tree1.yview)
    sc4.place(relx=1, rely=0, width=17, relheight=1 - 17 / 310, anchor='ne')
    tree1.configure(xscrollcommand=sc3.set)
    tree1.configure(yscrollcommand=sc4.set)

    # frame5的部件
    tree3 = ttk.Treeview(frame5)  # 表格
    # frame5的布局
    tree3.place(x=0, y=0, relwidth=1 - 17 / 540, relheight=1 - 17 / 215)
    sc7 = tk.Scrollbar(frame5, orient='horizon', command=tree3.xview)
    sc7.place(relx=0, rely=1, relwidth=1 - 17 / 540, height=17, anchor='sw')
    sc8 = tk.Scrollbar(frame5, orient='vertical', command=tree3.yview)
    sc8.place(relx=1, rely=0, width=17, relheight=1 - 17 / 215, anchor='ne')
    tree3.configure(xscrollcommand=sc7.set)
    tree3.configure(yscrollcommand=sc8.set)

    # frame6的部件
    tree4 = ttk.Treeview(frame6)  # 表格
    # frame6的布局
    tree4.place(x=0, y=0, relwidth=1 - 17 / 540, relheight=1 - 17 / 235)
    sc9 = tk.Scrollbar(frame6, orient='horizon', command=tree4.xview)
    sc9.place(relx=0, rely=1, relwidth=1 - 17 / 540, height=17, anchor='sw')
    sc10 = tk.Scrollbar(frame6, orient='vertical', command=tree4.yview)
    sc10.place(relx=1, rely=0, width=17, relheight=1 - 17 / 235, anchor='ne')
    tree4.configure(xscrollcommand=sc9.set)
    tree4.configure(yscrollcommand=sc10.set)

    #frame1的部件
    b1 = ttk.Button(frame1, text='打开文件', command=lambda: open_file(text1))
    b3 = ttk.Button(frame1, text='保存文件', command=lambda: save_file(text1))
    b4 = ttk.Button(frame1, text='构造LR分析表', state=tk.DISABLED, command=lambda: LR_analyze_table(tree3, b7, b8))
    b2 = ttk.Button(frame1, text='确认文法', command=lambda: define_LR(text1, b5))

    #frame1的布局
    b1.place(x=0, y=25, anchor='w')
    b2.place(x=100, y=25, anchor='w')
    b3.place(x=200, y=25, anchor='w')
    b4.place(x=600, y=25, anchor='w')

    #总的布局
    frame1.place(x=0, y=0, anchor='nw')
    label1.place(x=0, y=50, anchor='nw')
    frame2.place(x=0, y=80)
    frame3.place(x=0, y=270)
    frame5.place(x=360, y=50)
    label2.place(x=360, y=280, anchor='w')
    e1.place(x=420, y=280, anchor='w')
    b5.place(x=100, y=247, anchor='w')
    b7.place(x=360, y=320, anchor='w')
    b8.place(x=480, y=320, anchor='w')
    frame6.place(x=360, y=345)

    win.mainloop()

# start_interface()

