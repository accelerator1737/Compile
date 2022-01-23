import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import showerror, showinfo
import FirstVT_LastVT as ff
filename = ''
first = {}
follow = {}
ss = ''
start = ''
sequent = []
table_value = {}
sta = ''
s_s = ''
st = 1
vi = {}
n_end = []
sent = []
tp = 0

flag = 0    #单步显示符号，0为未开始，1为开始了未结束，2为结束

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


def judge_LL1(text, b3, b4, b5):
    global first, follow, ss, start
    ss = text.get('1.0', 'end')
    start = ss[0]
    first = {}
    follow = {}
    while ss[-1] == '\n':
        ss = ss[0:-1]
    j1 = ff.judge_op(ss)
    if not j1:
        showerror(title="出错了", message="输入的文法不是OPG文法")
    else:
        j2 = ff.judge_op(ss)
        if not j2:
            showerror(title="出错了", message="输入的文法不是OPG文法")
        else:
            first = ff.get_firstvt(ss)
            follow = ff.get_lastvt(ss)
            b3.config(state=tk.NORMAL)
            b4.config(state=tk.NORMAL)
            b5.config(state=tk.NORMAL)



def get_first(tree):
    global first
    # 删除原来的内容
    tree.delete(*tree.get_children())
    tree['columns'] = ()

    li = [] #所有终结符
    for i in first:
        li.extend(first[i])
        s = set(li)
        li = list(s)
    tree['columns'] = tuple(li)
    for i in li:
        tree.heading(i, text=i)
        tree.column(i, width=50, anchor='center')
    tree.column("#0", width=70)
    tree.heading('#0', text='FirstVT集')
    v = {}
    for i in first:
        v[i] = []
        for j in li:
            if j in first[i]:
                v[i].append(1)
            else:
                v[i].append('')
    j = 0
    for i in v:
        tree.insert('', j, text=i, value=tuple(v[i]))
        j += 1


def get_follow(tree):
    global follow
    # 删除原来的内容
    tree.delete(*tree.get_children())
    tree['columns'] = ()

    li = []  # 所有终结符
    for i in follow:
        li.extend(follow[i])
        s = set(li)
        li = list(s)
    tree['columns'] = tuple(li)
    for i in li:
        tree.heading(i, text=i)
        tree.column(i, width=50, anchor='center')
    tree.column("#0", width=70)
    tree.heading('#0', text='LastVT集')
    v = {}
    for i in follow:
        v[i] = []
        for j in li:
            if j in follow[i]:
                v[i].append(1)
            else:
                v[i].append('')
    j = 0
    for i in v:
        tree.insert('', j, text=i, value=tuple(v[i]))
        j += 1


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


def struc_predict(tree, b7, b8):
    global first, follow, ss, sequent, table_value, vi, sent, flag
    flag = 0
    #删除原来的内容
    tree.delete(*tree.get_children())
    tree['columns'] = ()

    li1 = []  # 所有终结符
    for i in first:
        li1.extend(first[i])
        s = set(li1)
        li1 = list(s)
    li2 = []  # 所有终结符
    for i in follow:
        li2.extend(follow[i])
        s = set(li2)
        li2 = list(s)
    li = []
    li.extend(li1)
    li.extend(li2)
    s = set(li)
    li = list(s)
    if '#' not in li:
        li.append('#')
    tree['columns'] = tuple(li)
    for i in li:
        tree.heading(i, text=i)
        tree.column(i, width=70, anchor='center')
    tree.column("#0", width=50)
    tree.heading('#0', text='右/左')
    start = ss[0]
    sent = ff.get_single(ss)
    sen = ff.get_single(ss + '\n{}->#{}#'.format('β', start))
    insert_value = struct_insert(sen, li)
    j = 0
    sequent = li
    table_value = insert_value
    for i in insert_value:
        tree.insert('', j, text=i, value=tuple(insert_value[i]))
        j += 1
    vi = insert_value
    b7.config(state=tk.NORMAL)
    b8.config(state=tk.NORMAL)


def struct_insert(sen, li):
    global ss
    v = {}
    start = ss[0]
    for i in li:
        v[i] = []
        for j in li:
            v[i].append('')
    v = find_equate(v, sen, li) #先找等于的情形
    v = find_small(v, sen, li)  # 找小于的情形
    v = find_big(v, sen, li)  # 找大于的情形
    return v


def find_small(v, sen, li):
    global ss, n_end
    start = ss[0]
    tem = ss + '\n{}->#{}#'.format('β', start)
    lastvt = ff.get_lastvt(tem)
    no_end = ff.get_no_end(sen)
    n_end = no_end
    #P->...Rb...
    for i in sen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        j = 1
        while j < len(hou):
            if hou[j-1] in no_end and hou[j] not in no_end:
                for k in lastvt[hou[j-1]]:
                    v[k][li.index(hou[j])] = '<'
            j += 1
    return v


def find_big(v, sen, li):
    global ss
    start = ss[0]
    tem = ss + '\n{}->#{}#'.format('β', start)
    firstvt = ff.get_firstvt(tem)
    no_end = ff.get_no_end(sen)
    #P->...aR...
    for i in sen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        j = 1
        while j < len(hou):
            if hou[j] in no_end and hou[j - 1] not in no_end:
                for k in firstvt[hou[j]]:
                    v[hou[j-1]][li.index(k)] = '>'
            j += 1
    return v


def find_equate(v, sen, li):
    start = ss[0]
    no_end = ff.get_no_end(sen)
    #P->...ab...
    for i in sen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        j = 1
        while j < len(hou):
            if hou[j] not in no_end and hou[j-1] not in no_end:
                v[hou[j]][li.index(hou[j-1])] = '='
            j += 1
    # P->...aQb...
    for i in sen:
        qian = i.split('->')[0]
        hou = i.split('->')[1]
        j = 2
        while j < len(hou):
            if hou[j] not in no_end and hou[j - 1] in no_end and hou[j-2] not in no_end:
                v[hou[j-2]][li.index(hou[j])] = '='
            j += 1
    return v


def one2end(s, tree):
    global sequent, table_value, ss, vi, flag
    flag = 0
    # 删除原来的内容
    tree.delete(*tree.get_children())
    tree['columns'] = ()

    h = ('栈', '输入缓冲区', '说明')
    tree['columns'] = h
    tree.column("#0", width=60)
    tree.heading('#0', text='步骤')
    for i in h:
        tree.heading(i, text=i)
        tree.column(i, width=160, anchor='center')

    start = ss[0]
    stack = '#'
    s = s + '#'
    step = 1
    shi = ''
    sen = ff.get_single(ss)
    no_end = ff.get_no_end(sen)
    top = 0
    tree.insert('', step - 1, text=str(step), value=(stack, s, shi))
    step += 1
    while stack != '#{}'.format(start) or s != '#':
        shu = s[0]
        if stack[top] in no_end:
            j = top - 1
        else:
            j = top
        if stack[j] not in vi or shu not in sequent:
            shi = '拒取'
            break
        if vi[stack[j]][sequent.index(shu)] == '>' or vi[stack[j]][sequent.index(shu)] == '=':
            top += 1
            stack += shu
            s = s[1:]
            shi = '移进'
        elif vi[stack[j]][sequent.index(shu)] == '<':
            q = j
            while vi[stack[j]][sequent.index(stack[q])] != '>':
                q = j
                if stack[j - 1] not in no_end:
                    j = j - 1
                else:
                    j = j - 2
            gui = stack[j+1:]
            stack = stack[:j+1]
            top = j + 1
            shi, stack = find_gui(sen, gui, stack, no_end) #找到要规约的串
        if shi == '拒取':
            break
        tree.insert('', step-1, text=str(step), value=(stack, s, shi))
        step += 1
    if shi == '拒取':
        tree.insert('', step - 1, text=str(step), value=(stack, s, shi))
    else:
        tree.insert('', step - 1, text=str(step), value=(stack, s, '接受'))


def find_gui(sen, gui, stack, no_end):
    flag3 = 0
    shi = ''
    jia = ''
    for p in sen:
        qian = p.split('->')[0]
        hou = p.split('->')[1]
        if len(hou) == len(gui):
            for i in range(len(hou)):
                if hou[i] in no_end and gui[i] in no_end:
                    continue
                elif hou[i] not in no_end and gui[i] not in no_end:
                    if hou[i] == gui[i]:
                        continue
                    else:
                        flag3 = 1
                        break
                else:
                    flag3 = 1
                    break
            else:
                flag3 = 0
                shi = p
                jia = qian
                break
    if flag3 == 1:
        return '拒取', stack
    else:
        stack += jia
        return shi, stack


def one2one(s, tree):
    global start, sequent, vi, flag, s_s, sta, st, n_end, sent, tp
    shi = ''
    if flag == 0:
        flag = 1
        # 删除原来的内容
        tree.delete(*tree.get_children())
        tree['columns'] = ()

        h = ('栈', '输入缓冲区', '说明')
        tree['columns'] = h
        tree.column("#0", width=60)
        tree.heading('#0', text='步骤')
        for i in h:
            tree.heading(i, text=i)
            tree.column(i, width=160, anchor='center')
        st = 1
        tp = 0

        sta = '#'
        s_s = s + '#'

        tree.insert('', st - 1, text=str(st), value=(sta, s_s, shi))
        st += 1
    elif flag == 1:
        shu = s_s[0]
        if sta[tp] in n_end:
            j = tp - 1
        else:
            j = tp
        if sta[j] not in vi or shu not in sequent:
            shi = '拒取'
            flag = 3
        if flag != 3:
            if vi[sta[j]][sequent.index(shu)] == '>' or vi[sta[j]][sequent.index(shu)] == '=':
                tp += 1
                sta += shu
                s_s = s_s[1:]
                shi = '移进'
            elif vi[sta[j]][sequent.index(shu)] == '<':
                q = j
                while vi[sta[j]][sequent.index(sta[q])] != '>':
                    q = j
                    if sta[j - 1] not in n_end:
                        j = j - 1
                    else:
                        j = j - 2
                gui = sta[j + 1:]
                sta = sta[:j + 1]
                tp = j + 1
                shi, sta = find_gui(sent, gui, sta, n_end)  # 找到要规约的串
            if shi == '拒取':
                flag = 3
            if sta == '#{}'.format(start) and s_s == '#':
                flag = 2
            tree.insert('', st - 1, text=str(st), value=(sta, s_s, shi))
            st += 1
    if flag == 2:
        tree.insert('', st - 1, text=str(st), value=(sta, s_s, '接受'))
        showinfo(title="完成", message='分析已完成')
        flag = 0
    if flag == 3:
        tree.insert('', st - 1, text=str(st), value=(sta, s_s, '拒取'))
        showerror(title="出错", message='分析已完成，输入表达式与文法不匹配')
        flag = 0



def start_interface():
    win = tk.Tk()
    win.geometry("{}x{}".format(900, 600))
    win.title('算符优先分析法')
    win.resizable(width=False, height=False)
    frame1 = tk.Frame(win, bd=2, width=900, height=50, relief='groove')
    frame2 = tk.Frame(win, bd=2, width=360, height=145, relief='groove')
    label1 = tk.Label(win, text='原始文法：请输入形如A->BC的LL(1)文法，空串用ε表示')
    frame3 = tk.Frame(win, bd=2, width=360, height=145, relief='groove')
    b5 = ttk.Button(win, text='求FirstVT集', state=tk.DISABLED, command=lambda: get_first(tree1))
    b6 = ttk.Button(win, text='求LastVT集', state=tk.DISABLED, command=lambda: get_follow(tree2))
    frame4 = tk.Frame(win, bd=2, width=360, height=150, relief='groove')
    frame5 = tk.Frame(win, bd=2, width=540, height=215, relief='groove')
    label2 = tk.Label(win, text='分析句子')
    e1 = tk.Entry(win, width=65)
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
    tree1.place(x=0, y=0, relwidth=1 - 17 / 360, relheight=1 - 17 / 145)
    sc3 = tk.Scrollbar(frame3, orient='horizon', command=tree1.xview)
    sc3.place(relx=0, rely=1, relwidth=1 - 17 / 360, height=17, anchor='sw')
    sc4 = tk.Scrollbar(frame3, orient='vertical', command=tree1.yview)
    sc4.place(relx=1, rely=0, width=17, relheight=1 - 17 / 145, anchor='ne')
    tree1.configure(xscrollcommand=sc3.set)
    tree1.configure(yscrollcommand=sc4.set)

    # frame4的部件
    tree2 = ttk.Treeview(frame4)  # 表格
    # frame4的布局
    tree2.place(x=0, y=0, relwidth=1 - 17 / 360, relheight=1 - 17 / 145)
    sc5 = tk.Scrollbar(frame4, orient='horizon', command=tree2.xview)
    sc5.place(relx=0, rely=1, relwidth=1 - 17 / 360, height=17, anchor='sw')
    sc6 = tk.Scrollbar(frame4, orient='vertical', command=tree2.yview)
    sc6.place(relx=1, rely=0, width=17, relheight=1 - 17 / 145, anchor='ne')
    tree2.configure(xscrollcommand=sc5.set)
    tree2.configure(yscrollcommand=sc6.set)

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
    b4 = ttk.Button(frame1, text='构造算符优先关系表', state=tk.DISABLED, command=lambda: struc_predict(tree3, b7, b8))
    b2 = ttk.Button(frame1, text='确认文法', command=lambda: judge_LL1(text1, b5, b6, b4))

    #frame1的布局
    b1.place(x=0, y=25, anchor='w')
    b2.place(x=100, y=25, anchor='w')
    b3.place(x=200, y=25, anchor='w')
    b4.place(x=600, y=25, anchor='w')

    #总的布局
    frame1.place(x=0, y=0, anchor='nw')
    label1.place(x=0, y=50, anchor='nw')
    frame2.place(x=0, y=80)
    frame3.place(x=0, y=230)
    b5.place(x=0, y=405, anchor='w')
    b6.place(x=150, y=405, anchor='w')
    frame4.place(x=0, y=430)
    frame5.place(x=360, y=50)
    label2.place(x=360, y=280, anchor='w')
    e1.place(x=420, y=280, anchor='w')
    b7.place(x=360, y=320, anchor='w')
    b8.place(x=480, y=320, anchor='w')
    frame6.place(x=360, y=345)

    win.mainloop()

# start_interface()

