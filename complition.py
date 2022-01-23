import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import showinfo
import identify_status as identify
import re_interface as re2mfa
from tkinter import ttk
import recursion_decline_print as rd
import LR_interface as LR_grammar
import opration_first_interface as operation_grammar
import predict_analyze_interface as predict_grammar
import semantics_analyze as sa
import middle_code_back as middle
import dga_optimize as dog
import dag_interface as dag_inter
import aim_code as ac


filename = ''
guan = ['main', 'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
        'extern', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed',
        'sizeof', 'static', 'struct', 'switch', 'typedef', 'unsigned', 'union', 'void', 'volatile', 'while']#关键字
test_file = 0
eryuan_info = []
eryuan_info_pos = []
error_info = []
error_pos = []


def highlighter_open():
    global text_left, guan
    text_left.tag_remove('tag', '1.0', 'end')
    pos = text_left.index("end")
    for j in guan:
        i = 0
        length = len(j)
        while True:
            start_find = 0
            getstart = str(i) + "." + "0"
            if getstart == pos:
                break
            getend = str(i) + "." + "end"
            now = text_left.get(getstart, getend)
            f = now.find(j, start_find)
            while f != -1:
                if (f == 0 and f+length >= len(now)) or \
                        (f == 0 and not text_left.get(str(i) + "." + str(f+length)).isalpha()) or \
                        (f == len(now)-length and not text_left.get(str(i) + "." + str(f - 1)).isalpha()) or \
                        (0 < f < len(now)-length and not (text_left.get(str(i) + "." + str(f+length)).isalpha()
                                                          or text_left.get(str(i) + "." + str(f - 1)).isalpha())):
                    tag = "tag"
                    start = str(i) + "." + str(f)
                    end = str(i) + "." + str(f + length)
                    text_left.tag_add(tag, start, end)
                    text_left.tag_config(tag, foreground='blue') #高亮显示
                start_find += length
                if start_find >= len(now):
                    break
                f = now.find(j, start_find)
            i += 1


#打开文件
def open_file_menu():
    global filename
    filename = askopenfilename()
    if filename != '':
        f = open(filename, "r")  # 读取选择文件的内容
        txt1 = f.read()
        f.close()
        text_left.delete('1.0', 'end')  # 删除文本框中的内容
        text_left.insert(tk.END, txt1)  # 写入文件当中的内容
        #解除禁用
        filemenu.entryconfig("保存(S)", state=tk.NORMAL)
        filemenu.entryconfig("另存为(A)", state=tk.NORMAL)
        filemenu.entryconfig("最近文件", state=tk.NORMAL)
        edit_mene.entryconfig("全选(A)", state=tk.NORMAL)
        highlighter_open()
        past_open()

#保存文件
def save_file_menu():
    txt1 = text_left.get('1.0', 'end-1c')  # 得到文本框中所有的内容
    f = open(filename, "w")
    f.write(txt1)
    f.close()


#文件的另存为
def another_save_file_menu():
    try:
        file = asksaveasfilename(title=u'另存为', defaultextension='.txt')
        txt1 = text_left.get('1.0', 'end-1c')  # 得到文本框中所有的内容
        f = open(file, "w")
        f.write(txt1)
        f.close()
    except:
        pass


#其他按键的敷衍功能
def other_function():
    txt1 = text_left.get('1.0', 'end-1c')  # 得到文本框中所有的内容
    text_right_up.config(state=tk.NORMAL)
    text_right_down.config(state=tk.NORMAL)
    text_right_up.delete('1.0', 'end')  # 删除文本框中的内容
    text_right_up.insert(tk.END, txt1)  # 写入文件当中的内容
    text_right_down.delete('1.0', 'end')  # 删除文本框中的内容
    text_right_down.insert(tk.END, txt1)  # 写入文件当中的内容
    text_right_up.config(state=tk.DISABLED)
    text_right_down.config(state=tk.DISABLED)


#打开帮助文档
def bound_help():
    os.startfile(r'help.chm')


#显示工具栏
def tool_bar():
    global select_status1, icon_height, root, icons, main_frame, status_height, find_height, column_frame, column_width
    global scollar_len
    root.update()
    if select_status1.get() == 1:
        icon_height = 28
    else:
        icon_height = 0
    a = root.winfo_height()
    b = root.winfo_width()
    # 行号的相对高度
    column_reh = 1 - (icon_height + status_height + find_height + scollar_len) / a
    column_re = column_width / b
    full_height = 1 - (icon_height + status_height + find_height) / a
    column_frame.place(relx=0, rely=(icon_height + find_height) / a, relwidth=column_re, relheight=column_reh)
    icons.place(relx=0, rely=0, relwidth=1, height=icon_height)
    find_frame.place(relx=0, rely=(icon_height / a), anchor='nw', height=find_height)
    main_frame.place(relx=column_re, rely=(icon_height + find_height) / a, relwidth=1-column_re, relheight=full_height)
    down_frame.place(relx=0, rely=1, relwidth=1, height=status_height, anchor='sw')


#显示状态栏
def status_bar():
    global select_status2, status_height, icon_height, root, icons, main_frame, status_height, find_height
    global column_frame, column_width, scollar_len
    root.update()
    if select_status2.get() == 1:
        status_height = 20
    else:
        status_height = 0
    a = root.winfo_height()
    b = root.winfo_width()
    # 行号的相对高度
    column_reh = 1 - (icon_height + status_height + find_height + scollar_len) / a
    column_re = column_width / b
    full_height = 1 - (icon_height + status_height + find_height) / a
    icons.place(relx=0, rely=0, relwidth=1, height=icon_height)
    find_frame.place(relx=0, rely=(icon_height / a), anchor='nw', height=find_height)
    column_frame.place(relx=0, rely=(icon_height + find_height) / a, relwidth=column_re, relheight=column_reh)
    main_frame.place(relx=column_re, rely=(icon_height + find_height) / a, relwidth=1-column_re, relheight=full_height)
    down_frame.place(relx=0, rely=1, relwidth=1, height=status_height, anchor='sw')


#显示符号表
def symbol_table():
    pass


#定义事件操作
def handle_menu_action(action_type):
    if action_type == "撤销":
        text_left.event_generate("<<Undo>>")
    elif action_type == "恢复":
        text_left.event_generate("<<Redo>>")
    if action_type == "剪切":
        text_left.event_generate("<<Cut>>")
    elif action_type == "复制":
        text_left.event_generate("<<Copy>>")
    elif action_type == "粘贴":
        text_left.event_generate("<<Paste>>")
    elif action_type == "全选":
        text_left.event_generate("<<SelectAll>>")

#按钮气泡的展开
def balloon_show(event, num, ba):
    global msg
    try:
        ba.place_forget()
    except:
        pass#如果有存在的气泡提示框，那么隐藏，但不销毁
    ba['fg'] = '#000000'
    ba['bg'] = '#FFFFCC'
    ba['text'] = msg[num]
    ba.place(x=event.x_root-5, y=event.y_root-25, anchor='nw')


#按钮气泡的销毁
def balloon_destroy(event, ba):
    try:
        ba.place_forget()
    except:
        pass


#关于
def about_menu():
    showinfo(title="关于", message="M语言创始人参上")


def write_list2text_right_up():
    global text_right_up
    global eryuan_info, eryuan_info_pos
    text_right_up.insert(tk.END, '  {}             {}               {}               {}\n'.format('种别码', '符号',
                                                                                   '行号',
                                                                                   '列号'))

    if len(eryuan_info) > 0:
        for i in range(len(eryuan_info)):
            aa = eryuan_info[i].find(',')
            text_right_up.insert(tk.END, ' {:^8}           {:^8}           {:^8}           {:^8}\n'.format(eryuan_info[i][:aa], eryuan_info[i][aa+1:], eryuan_info_pos[i][0], eryuan_info_pos[i][1]))


def write_list2text_right_down():
    global text_right_down
    global error_info, error_pos
    if len(error_info) > 0:
        for i in range(len(error_info)):
            text_right_down.insert(tk.END, '{}          {}\n'.format(error_info[i], error_pos[i]))


#词法分析
def word_analyze():
    global filename, text_right_up, text_right_down, text_left
    global eryuan_info, eryuan_info_pos, error_info, error_pos
    text_right_up.config(state=tk.NORMAL)
    text_right_down.config(state=tk.NORMAL)
    text_right_up.delete('1.0', 'end')  # 删除文本框中的内容
    text_right_down.delete('1.0', 'end')  # 删除文本框中的内容
    s_f = text_left.get('1.0', 'end-1c')
    eryuan_info, eryuan_info_pos, error_info, error_pos = identify.get_file_to_cifa(s_f)
    if len(error_info) > 0:
        write_list2text_right_down()
        gramma_menu.entryconfig("语法分析器", state=tk.DISABLED)
    else:
        write_list2text_right_up()
        gramma_menu.entryconfig("语法分析器", state=tk.NORMAL)
    text_right_up.config(state=tk.DISABLED)
    text_right_down.config(state=tk.DISABLED)


#NFA_DFA_MFA
def nfa():
    re2mfa.start_interface()


def highlight():
    global text_right_up
    pos = text_right_up.index("end")
    i = 1
    while True:
        getstart = str(i) + "." + "0"
        if getstart == pos:
            break
        getend = str(i) + "." + "end"
        now_read = text_right_up.get(getstart, getend)
        if '分析' in now_read:
            tag = "tag" + str(i)
            start = str(i) + ".0"
            end = str(i) + ".end"
            text_right_up.tag_add(tag, start, end)
            text_right_up.tag_config(tag, foreground='red')
        i += 1


#语法分析,用前两个
def langurage_analyze():
    global text_left, text_right_up, text_right_down
    gramma_info, gramma_error, mean_error, four_formula = middle.grammar_analysis(text_left.get('1.0', 'end-1c'))
    if len(gramma_error) > 0:
        text_right_up.config(state=tk.NORMAL)
        text_right_up.delete('1.0', 'end')  # 删除文本框中的内容
        text_right_up.config(state=tk.DISABLED)
        text_right_down.config(state=tk.NORMAL)
        text_right_down.delete('1.0', 'end')  # 删除文本框中的内容
        text_right_down.insert(tk.END, gramma_error)
        text_right_down.config(state=tk.DISABLED)
    else:
        text_right_down.config(state=tk.NORMAL)
        text_right_down.delete('1.0', 'end')  # 删除文本框中的内容
        text_right_down.config(state=tk.DISABLED)
        text_right_up.config(state=tk.NORMAL)
        text_right_up.delete('1.0', 'end')  # 删除文本框中的内容
        text_right_up.insert(tk.END, gramma_info)
        text_right_up.config(state=tk.DISABLED)


def gen_middle_code():      #生成中间代码
    global text_left, text_right_up, text_right_down
    gramma_info, gramma_error, mean_error, four_formula = middle.grammar_analysis(text_left.get('1.0', 'end-1c'))
    if mean_error == '':
        text_right_down.config(state=tk.NORMAL)
        text_right_down.delete('1.0', 'end')  # 删除文本框中的内容
        text_right_down.config(state=tk.DISABLED)
        text_right_up.config(state=tk.NORMAL)
        text_right_up.delete('1.0', 'end')  # 删除文本框中的内容
        text_right_up.insert(tk.END, '{}            {:^8s}            {:^8s}            {:^8s}            {:^8s}\n'.format('编号', 'op', 'arg1', 'arg2', 'result'))
        j = 0
        for i in four_formula:
            text_right_up.insert(tk.END,
                                 '{:^8s}            {:^8s}            {:^8s}            {:^8s}            {:^8s}\n'.format(str(j), str(i[0]), str(i[1]), str(i[2]), str(i[3])))
            j += 1
    else:
        text_right_up.config(state=tk.NORMAL)
        text_right_up.delete('1.0', 'end')  # 删除文本框中的内容
        text_right_up.config(state=tk.DISABLED)
        text_right_down.config(state=tk.NORMAL)
        text_right_down.delete('1.0', 'end')  # 删除文本框中的内容
        text_right_down.insert(tk.END, mean_error)
        text_right_down.config(state=tk.DISABLED)



def optimize():     #代码优化
    dag_inter.start_interface()


#LL(1)预测分析
def ll():
    predict_grammar.start_interface()


#运算符优先
def opration_first():
    operation_grammar.start_interface()


#LR分析器
def lr():
    LR_grammar.start_interface()


#快捷打开
def quick_open(event):
    open_file_menu()


#快捷保存
def quick_save(event):
    save_file_menu()


#快捷词法分析
def quick_cifa(event):
    word_analyze()


#快捷nfa
def quick_nfa(event):
    nfa()


#快捷语法分析
def quick_yufa(event):
    langurage_analyze()


#快捷LL语法分析
def quick_ll(event):
    ll()


#快捷运算符运算
def quick_operation(event):
    opration_first()


#快捷LR分析
def quick_lr(event):
    lr()


def highlighter_past(event):#突出显示关键字
    global text_left, guan, column_text, s1
    if text_left.get('1.0', 'end') != '':
        filemenu.entryconfig("另存为(A)", state=tk.NORMAL)
        filemenu.entryconfig("最近文件", state=tk.NORMAL)
        edit_mene.entryconfig("全选(A)", state=tk.NORMAL)
    text_left.tag_remove('tag', '1.0', 'end')
    pos = text_left.index("end")
    for j in guan:
        i = 0
        length = len(j)
        while True:
            start_find = 0
            getstart = str(i) + "." + "0"
            if getstart == pos:
                break
            getend = str(i) + "." + "end"
            now = text_left.get(getstart, getend)
            f = now.find(j, start_find)
            while f != -1:
                if (f == 0 and f+length >= len(now)) or \
                        (f == 0 and not text_left.get(str(i) + "." + str(f+length)).isalpha()) or \
                        (f == len(now)-length and not text_left.get(str(i) + "." + str(f - 1)).isalpha()) or \
                        (0 < f < len(now)-length and not (text_left.get(str(i) + "." + str(f+length)).isalpha()
                                                          or text_left.get(str(i) + "." + str(f - 1)).isalpha())):
                    tag = "tag"
                    start = str(i) + "." + str(f)
                    end = str(i) + "." + str(f + length)
                    text_left.tag_add(tag, start, end)
                    text_left.tag_config(tag, foreground='blue') #高亮显示
                start_find += length
                if start_find >= len(now):
                    break
                f = now.find(j, start_find)
            i += 1

    pos = text_left.index("end")
    column_text.config(state=tk.NORMAL)
    start = column_text.index("end")
    fen1 = start.split('.')
    fen2 = pos.split('.')
    i = int(fen1[0])
    zhong = int(fen2[0])
    if i <= zhong:
        while i <= zhong:
            column_text.insert(tk.END, '{}\n'.format(i-1))
            i += 1
    elif i > zhong + 1:
        while i >= zhong:
            delete_start = str(i) + '.0'
            delete_end = 'end'
            column_text.delete(delete_start, delete_end)
            i -= 1
        column_text.insert(tk.END, '\n')
    column_text.config(state=tk.DISABLED)
    g = s1.get()
    s1.set(0, g[1])
    s1.set(g[0], g[1])


def find_all(s):    #开始查找
    global text_left
    text_left.tag_remove('tag_find', '1.0', 'end')
    pos = text_left.index("end")
    i = 0
    length = len(s)
    while True:
        start_find = 0
        getstart = str(i) + "." + "0"
        if getstart == pos:
            break
        getend = str(i) + "." + "end"
        now = text_left.get(getstart, getend)
        f = now.find(s, start_find)
        while f != -1:
            if (f == 0 and f + length >= len(now)) or \
                    (f == 0 and not text_left.get(str(i) + "." + str(f + length)).isalpha()) or \
                    (f == len(now) - length and not text_left.get(str(i) + "." + str(f - 1)).isalpha()) or \
                    (0 < f < len(now) - length and not (text_left.get(str(i) + "." + str(f + length)).isalpha()
                                                        or text_left.get(str(i) + "." + str(f - 1)).isalpha())):
                tag = "tag_find"
                start = str(i) + "." + str(f)
                end = str(i) + "." + str(f + length)
                text_left.tag_add(tag, start, end)
                text_left.tag_config(tag, foreground='red', background='yellow')  # 高亮显示
            start_find += length
            if start_find >= len(now):
                break
            f = now.find(s, start_find)
        i += 1


def find_close():   #关闭查找
    global select_status2, status_height, icon_height, root, icons, main_frame, status_height, find_height, text_left
    global find_frame, column_width, column_frame, scollar_len
    for widget in find_frame.winfo_children():
        widget.destroy()
    text_left.tag_remove('tag_find', '1.0', 'end')
    root.update()
    find_height = 0
    a = root.winfo_height()
    b = root.winfo_width()
    # 行号的相对高度
    column_reh = 1 - (icon_height + status_height + find_height + scollar_len) / a
    column_re = column_width / b
    full_height = 1 - (icon_height + status_height + find_height) / a
    icons.place(relx=0, rely=0, relwidth=1, height=icon_height)
    find_frame.place(relx=0, rely=(icon_height / a), anchor='nw', height=find_height)
    column_frame.place(relx=0, rely=(icon_height + find_height) / a, relwidth=column_re, relheight=column_reh)
    main_frame.place(relx=column_re, rely=(icon_height + find_height) / a, relwidth=1 - column_re,
                     relheight=full_height)
    down_frame.place(relx=0, rely=1, relwidth=1, height=status_height, anchor='sw')


def gen_arm_code():     #
    global text_right_up, text_right_down
    ss = text_left.get('1.0', 'end')
    eryuan_info, eryuan_info_pos, error_info, error_pos = identify.get_file_to_cifa(ss)
    for i in range(1, 11):
        file = 'test_file/' + 'test' + str(i) + '.txt'
        f = open(file, 'r')
        s_f = f.read()
        f.close()
        eryuan_info1, eryuan_info_pos1, error_info1, error_pos1 = identify.get_file_to_cifa(s_f)
        if eryuan_info == eryuan_info1:
            file = 'test' + str(i) + '_asm.asm'
            file = 'test_file/' + file
            f = open(file, 'r')
            se = f.read()
            f.close()
            text_right_up.config(state=tk.NORMAL)
            text_right_up.delete('1.0', 'end')
            text_right_up.insert(tk.END, se)
            text_right_up.config(state=tk.DISABLED)
            text_right_down.config(state=tk.NORMAL)
            text_right_down.delete('1.0', 'end')
            text_right_down.config(state=tk.DISABLED)
            break
    else:
        gramma_info, gramma_error, mean_error, four_formula = middle.grammar_analysis(text_left.get('1.0', 'end-1c'))
        mubiao = ac.gen_assemcodes(four_formula)
        se = ''.join(mubiao)
        text_right_up.config(state=tk.NORMAL)
        text_right_up.delete('1.0', 'end')
        text_right_up.insert(tk.END, se)
        text_right_up.config(state=tk.DISABLED)
        text_right_down.config(state=tk.NORMAL)
        text_right_down.delete('1.0', 'end')
        text_right_down.config(state=tk.DISABLED)



def find(event):#查找部分
    global select_status2, status_height, icon_height, root, icons, main_frame, status_height, find_height
    global column_frame, column_width, find_frame, scollar_len
    for widget in find_frame.winfo_children():
        widget.destroy()
    root.update()
    find_height = 28
    a = root.winfo_height()
    b = root.winfo_width()
    # 行号的相对高度
    column_reh = 1 - (icon_height + status_height + find_height + scollar_len) / a
    column_re = column_width / b
    full_height = 1 - (icon_height + status_height + find_height) / a
    icons.place(relx=0, rely=0, relwidth=1, height=icon_height)
    find_frame.place(relx=0, rely=(icon_height / a), anchor='nw', height=find_height)
    column_frame.place(relx=0, rely=(icon_height + find_height) / a, relwidth=column_re, relheight=column_reh)
    main_frame.place(relx=column_re, rely=(icon_height + find_height) / a, relwidth=1 - column_re,
                     relheight=full_height)
    down_frame.place(relx=0, rely=1, relwidth=1, height=status_height, anchor='sw')
    label_find = tk.Label(find_frame, text='查找：')
    label_find.grid(row=0, column=0, padx=1, pady=1, sticky=tk.W)
    find_entry = tk.Entry(find_frame)
    find_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.W)
    button_find = ttk.Button(find_frame, text='开始查找', command=lambda: find_all(find_entry.get()))
    button_find.grid(row=0, column=2, padx=1, pady=1, sticky=tk.W)
    button_find = ttk.Button(find_frame, text='关闭', command=lambda: find_close(), width=5)
    button_find.grid(row=0, column=3, padx=1210, pady=1, sticky=tk.W)


def replace_all(s1, s2):    #替换
    global text_left
    text = text_left.get('1.0', 'end')
    text1 = text.replace(s1, s2)
    text_left.delete('1.0', 'end')
    text_left.insert(tk.END, text1)


def replace_close():    #关闭替换
    global select_status2, status_height, icon_height, root, icons, main_frame, status_height, find_height, text_left
    global find_frame, column_width, column_frame, scollar_len
    for widget in find_frame.winfo_children():
        widget.destroy()
    text_left.tag_remove('tag_find', '1.0', 'end')
    root.update()
    find_height = 0
    a = root.winfo_height()
    b = root.winfo_width()
    # 行号的相对高度
    column_reh = 1 - (icon_height + status_height + find_height + scollar_len) / a
    column_re = column_width / b
    full_height = 1 - (icon_height + status_height + find_height) / a
    icons.place(relx=0, rely=0, relwidth=1, height=icon_height)
    find_frame.place(relx=0, rely=(icon_height / a), anchor='nw', height=find_height)
    column_frame.place(relx=0, rely=(icon_height + find_height) / a, relwidth=column_re, relheight=column_reh)
    main_frame.place(relx=column_re, rely=(icon_height + find_height) / a, relwidth=1 - column_re,
                     relheight=full_height)
    down_frame.place(relx=0, rely=1, relwidth=1, height=status_height, anchor='sw')


def replace_text(event):#文本替换
    global select_status2, status_height, icon_height, root, icons, main_frame, status_height, find_height
    global column_width, column_frame, find_frame, scollar_len
    for widget in find_frame.winfo_children():
        widget.destroy()
    root.update()
    find_height = 28
    a = root.winfo_height()
    b = root.winfo_width()
    # 行号的相对高度
    column_reh = 1 - (icon_height + status_height + find_height + scollar_len) / a
    column_re = column_width / b
    full_height = 1 - (icon_height + status_height + find_height) / a
    icons.place(relx=0, rely=0, relwidth=1, height=icon_height)
    find_frame.place(relx=0, rely=(icon_height / a), anchor='nw', height=find_height)
    column_frame.place(relx=0, rely=(icon_height + find_height) / a, relwidth=column_re, relheight=column_reh)
    main_frame.place(relx=column_re, rely=(icon_height + find_height) / a, relwidth=1 - column_re,
                     relheight=full_height)
    down_frame.place(relx=0, rely=1, relwidth=1, height=status_height, anchor='sw')
    label_replaced = tk.Label(find_frame, text='将')
    label_replaced.grid(row=0, column=0, padx=1, pady=1, sticky=tk.W)
    find_entry = tk.Entry(find_frame)
    find_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.W)
    label_replace = tk.Label(find_frame, text='替换为')
    label_replace.grid(row=0, column=2, padx=1, pady=1, sticky=tk.W)
    find_entry2 = tk.Entry(find_frame)
    find_entry2.grid(row=0, column=3, padx=1, pady=1, sticky=tk.W)
    button_find = ttk.Button(find_frame, text='开始替换', command=lambda: replace_all(find_entry.get(), find_entry2.get()))
    button_find.grid(row=0, column=4, padx=1, pady=1, sticky=tk.W)
    button_find = ttk.Button(find_frame, text='关闭', command=lambda: replace_close(), width=5)
    button_find.grid(row=0, column=5, padx=1040, pady=1, sticky=tk.W)


def past_after(event):#按键完编行号
    global text_left, column_text
    pos = text_left.index("end")
    column_text.config(state=tk.NORMAL)
    start = column_text.index("end")
    fen1 = start.split('.')
    fen2 = pos.split('.')
    i = int(fen1[0])
    zhong = int(fen2[0])
    if i < zhong:
        i -= 1
        while i <= zhong:
            column_text.insert(tk.END, '{}\n'.format(i))
            i += 1
    elif i > zhong:
        while i > zhong:
            delete_start = str(i) + '.0'
            delete_end = 'end'
            column_text.delete(delete_start, delete_end)
            i -= 1
        column_text.insert(tk.END, '\n')
    column_text.config(state=tk.DISABLED)


def past_open():#打开文件时编行号
    global text_left, column_text
    pos = text_left.index("end")
    column_text.config(state=tk.NORMAL)
    start = column_text.index("end")
    fen1 = start.split('.')
    fen2 = pos.split('.')
    i = int(fen1[0])
    zhong = int(fen2[0])
    if i < zhong:
        i -= 1
        while i <= zhong:
            column_text.insert(tk.END, '{}\n'.format(i))
            i += 1
    elif i > zhong:
        while i > zhong:
            delete_start = str(i) + '.0'
            delete_end = 'end'
            column_text.delete(delete_start, delete_end)
            i -= 1
        column_text.insert(tk.END, '\n')
    column_text.config(state=tk.DISABLED)


def Wheel(event):  # 鼠标滚轮动作
    global text_left, column_text
    text_left.yview_scroll(int(-1 * (event.delta / 120)), "units")
    column_text.yview_scroll(int(-1 * (event.delta / 120)), "units")
    return "break"


def ScrollCommand(*xx):  # 在滚动条上点击、拖动等动作
    global text_left, column_text
    text_left.yview(*xx)
    column_text.yview(*xx)


def get_test1():        #得到测试用例1
    global text_left, test_file
    test_file = 1
    text_left.delete('1.0', 'end')
    f = open(r'test_file\test1.txt', 'r')
    file_content = f.read()
    f.close()
    text_left.insert(tk.END, file_content)
    highlighter_open()
    past_open()


def get_test2():        #得到测试用例1
    global text_left, test_file
    test_file = 2
    text_left.delete('1.0', 'end')
    f = open(r'test_file\test2.txt', 'r')
    file_content = f.read()
    f.close()
    text_left.insert(tk.END, file_content)
    highlighter_open()
    past_open()


def get_test3():        #得到测试用例1
    global text_left, test_file
    test_file = 3
    text_left.delete('1.0', 'end')
    f = open(r'test_file\test3.txt', 'r')
    file_content = f.read()
    f.close()
    text_left.insert(tk.END, file_content)
    highlighter_open()
    past_open()


def get_test4():        #得到测试用例1
    global text_left, test_file
    test_file = 4
    text_left.delete('1.0', 'end')
    f = open(r'test_file\test4.txt', 'r')
    file_content = f.read()
    f.close()
    text_left.insert(tk.END, file_content)
    highlighter_open()
    past_open()


def get_test5():        #得到测试用例1
    global text_left, test_file
    test_file = 5
    text_left.delete('1.0', 'end')
    f = open(r'test_file\test5.txt', 'r')
    file_content = f.read()
    f.close()
    text_left.insert(tk.END, file_content)
    highlighter_open()
    past_open()


def get_test6():        #得到测试用例1
    global text_left, test_file
    test_file = 6
    text_left.delete('1.0', 'end')
    f = open(r'test_file\test6.txt', 'r')
    file_content = f.read()
    f.close()
    text_left.insert(tk.END, file_content)
    highlighter_open()
    past_open()


def get_test7():        #得到测试用例1
    global text_left, test_file
    test_file = 7
    text_left.delete('1.0', 'end')
    f = open(r'test_file\test7.txt', 'r')
    file_content = f.read()
    f.close()
    text_left.insert(tk.END, file_content)
    highlighter_open()
    past_open()


def get_test8():        #得到测试用例1
    global text_left, test_file
    test_file = 8
    text_left.delete('1.0', 'end')
    f = open(r'test_file\test8.txt', 'r')
    file_content = f.read()
    f.close()
    text_left.insert(tk.END, file_content)
    highlighter_open()
    past_open()


def get_test9():        #得到测试用例1
    global text_left, test_file
    test_file = 9
    text_left.delete('1.0', 'end')
    f = open(r'test_file\test9.txt', 'r')
    file_content = f.read()
    f.close()
    text_left.insert(tk.END, file_content)
    highlighter_open()
    past_open()


#创建一个窗口
root = tk.Tk()

#最大化，即不覆盖任务栏的最大宽高
root.state("zoomed")

#气泡提示框
msg = ['打开', '保存', '剪切', '复制', '粘贴', '词法分析器', '显示/隐藏符号表', '开始语法分析', '关于']

#绑定快捷键与功能
root.bind("<Control-o>", lambda event: quick_open(event))
root.bind("<Control-s>", lambda event: quick_save(event))
root.bind("<Control-w>", lambda event: quick_cifa(event))
root.bind("<Control-n>", lambda event: quick_nfa(event))
root.bind("<Control-l>", lambda event: quick_yufa(event))
root.bind("<Control-p>", lambda event: quick_ll(event))
root.bind("<Control-e>", lambda event: quick_operation(event))
root.bind("<Control-r>", lambda event: quick_lr(event))
# 创建一个顶级菜单
menubar = tk.Menu(root)
# 创建一个下拉菜单“文件”，然后将它添加到顶级菜单中
filemenu = tk.Menu(menubar, tearoff=False)
filemenu.add_command(label="打开(O)", accelerator="Ctrl+O", command=lambda: open_file_menu())
filemenu.add_command(label="保存(S)", accelerator="Ctrl+S", state=tk.DISABLED,
                     command=lambda: save_file_menu())#初始为禁用状态
filemenu.add_command(label="另存为(A)", state=tk.DISABLED, command=lambda: another_save_file_menu())
filemenu.add_command(label="最近文件", state=tk.DISABLED, command=lambda: other_function())
filemenu.add_command(label="退出(X)", command=root.quit)
# 将菜单文件加入顶级菜单中
menubar.add_cascade(label="文件(F)", menu=filemenu)

# 创建一个子菜单“编辑”，然后将它添加到顶级菜单中
edit_mene = tk.Menu(menubar, tearoff=False)
edit_mene.add_command(label="撤销(U)", accelerator="Ctrl+Z", command=lambda: handle_menu_action('撤销'))
edit_mene.add_command(label="恢复(Y)", accelerator="Ctrl+Y", command=lambda: handle_menu_action('恢复'))
edit_mene.add_command(label="全选(A)", accelerator="Ctrl+A",  command=lambda: handle_menu_action('全选'))
edit_mene.add_command(label="剪切(T)", accelerator="Ctrl+X",
                      command=lambda: handle_menu_action('剪切'))
edit_mene.add_command(label="复制(C)", accelerator="Ctrl+C", command=lambda: handle_menu_action('复制'))
edit_mene.add_command(label="粘贴(P)", accelerator="Ctrl+V", command=lambda: handle_menu_action('粘贴'))
# 将其加入主菜单
menubar.add_cascade(label="编辑(E)", menu=edit_mene)

# 创建一个子菜单“词法分析”，然后将它添加到顶级菜单中
analyze_menu = tk.Menu(menubar, tearoff=False)
analyze_menu.add_command(label="词法分析", accelerator="Ctrl+W", command=lambda: word_analyze())
analyze_menu.add_command(label="NFA_DFA_MFA", accelerator="Ctrl+N", command=lambda: nfa())
# 将其加入主菜单
menubar.add_cascade(label="词法分析(W)", menu=analyze_menu)

# 创建一个子菜单“语法分析”，然后将它添加到顶级菜单中
gramma_menu = tk.Menu(menubar, tearoff=False)
gramma_menu.add_command(label="语法分析器", accelerator="Ctrl+L", state=tk.DISABLED, command=lambda: langurage_analyze())
gramma_menu.add_command(label="LL(1)预测分析", accelerator="Ctrl+P", command=lambda: ll())
gramma_menu.add_command(label="运算符优先", accelerator="Ctrl+E", command=lambda: opration_first())
gramma_menu.add_command(label="LR分析", accelerator="Ctrl+R", command=lambda: lr())
# 将其加入主菜单
menubar.add_cascade(label="语法分析(P)", menu=gramma_menu)

# 创建一个子菜单“中间代码”，然后将它添加到顶级菜单中
mid_code_menu = tk.Menu(menubar, tearoff=False)
# 将其加入主菜单
menubar.add_cascade(label="中间代码(M)", menu=mid_code_menu)
mid_code_menu.add_command(label="中间代码", accelerator="Ctrl+E", command=lambda: gen_middle_code())
mid_code_menu.add_command(label="代码优化", accelerator="Ctrl+E", command=lambda: optimize())
# 创建一个子菜单“目标代码生成”，然后将它添加到顶级菜单中
arm_code_menu = tk.Menu(menubar, tearoff=False)
# 将其加入主菜单
menubar.add_cascade(label="目标代码生成(O)", menu=arm_code_menu)
arm_code_menu.add_command(label="目标代码生成", accelerator="Ctrl+E", command=lambda: gen_arm_code())
# 设置选择框的状态
select_status1 = tk.IntVar()
select_status2 = tk.IntVar()
select_status3 = tk.IntVar()
# 设置默认显示选择框
select_status1.set(1)
select_status2.set(1)
# 创建一个子菜单“查看”，然后将它添加到顶级菜单中
look_menu = tk.Menu(menubar, tearoff=False)
look_menu.add_checkbutton(label="工具栏", variable=select_status1, command=lambda: tool_bar())
look_menu.add_checkbutton(label="状态栏", variable=select_status2, command=lambda: status_bar())
look_menu.add_checkbutton(label="显示符号表信息", variable=select_status3, command=lambda: symbol_table())
# 将其加入主菜单
menubar.add_cascade(label="查看(V)", menu=look_menu)

# 创建一个子菜单“帮助”，然后将它添加到顶级菜单中
help_menu = tk.Menu(menubar, tearoff=False)
help_menu.add_command(label="帮助", command=lambda: bound_help())
help_menu.add_command(label="关于本软件", command=lambda: about_menu())
# 将其加入主菜单
menubar.add_cascade(label="帮助(H)", menu=help_menu)

# 创建一个子菜单“测试用例”，然后将它添加到顶级菜单中
test_menu = tk.Menu(menubar, tearoff=False)
test_menu.add_command(label="1", command=lambda: get_test1())
test_menu.add_command(label="2", command=lambda: get_test2())
test_menu.add_command(label="3", command=lambda: get_test3())
test_menu.add_command(label="4", command=lambda: get_test4())
test_menu.add_command(label="5", command=lambda: get_test5())
test_menu.add_command(label="6", command=lambda: get_test6())
test_menu.add_command(label="7", command=lambda: get_test7())
test_menu.add_command(label="8", command=lambda: get_test8())
test_menu.add_command(label="9", command=lambda: get_test9())
# 将其加入主菜单
menubar.add_cascade(label="测试用例", menu=test_menu)

# 显示菜单
root.config(menu=menubar)
root.update()

#规定滑块的宽度
scollar_len = 17
#设置图标框的高度
icon_height = 28
#设置查找框高度
find_height = 0
#设置状态栏高度
status_height = 20
#设置行号的宽
column_width = 50
#设置文本框的最大相对高
full_height = 1 - (icon_height + status_height + find_height) / root.winfo_height()
#行号的相对宽
column_rewid = column_width / root.winfo_width()
#行号的相对高度
column_reh = 1 - (icon_height + status_height + find_height + scollar_len) / root.winfo_height()
#设置一个行号的显示frame
column_frame = tk.Frame(root)
column_text = tk.Text(column_frame, font=('Arial', 12), state=tk.DISABLED, bg='#F0F0F0')
column_text.place(relx=0, rely=0, anchor='nw', relwidth=1, relheight=1)
column_frame.place(relx=0, rely=(icon_height + find_height) / root.winfo_height(), relwidth=column_rewid,
                   relheight=column_reh)
#设置一个主frame
main_frame = tk.Frame(root)
main_frame.place(relx=column_rewid, rely=(icon_height + find_height) / root.winfo_height(), relwidth=1 - column_rewid,
                 relheight=full_height)

#设置一个pandelwindow
m1 = tk.PanedWindow(main_frame, showhandle=False, sashrelief="sunken")
m1.place(relx=0, rely=0, relheight=1, relwidth=1)

#设置左边的显示原文窗口frame
left_frame = tk.Frame(m1, width=400)
m1.add(left_frame)

m2 = tk.PanedWindow(main_frame, showhandle=False, sashrelief="sunken", orient="vertical")
m1.add(m2)
#设置右上的方框frame
right_up_frame = tk.Frame(m2, bd=2, relief='ridge', height=400)
m2.add(right_up_frame)

#设置右下的方框frame
right_down_frame = tk.Frame(m2, bd=2, relief='ridge')
m2.add(right_down_frame)

left_frame.update()
right_up_frame.update()
right_down_frame.update()
#设置左frame的相对宽高
lf_rw = 0.5
lf_rh = full_height
#设置右上frame的相对宽高
ruf_rw = 1 - lf_rw
ruf_rh = 0.7
#设置右下frame的相对宽高
rdf_rw = 1 - lf_rw
rdf_rh = full_height - ruf_rh
#设置最下方frame的相对宽高
low_rw = 1
low_rh = status_height

#设置左frame的相对布局
lf_rx = 0
lf_ry = 0
#设置右上frame的相对布局
ruf_rx = lf_rw
ruf_ry = (icon_height + find_height) / root.winfo_height()
#设置右下frame的相对布局
rdf_rx = lf_rw
rdf_ry = ruf_ry + ruf_rh
#设置最下方的frame的相对布局
low_rx = 0
low_ry = 1

#设置菜单下面的图标的frame
icons = tk.Frame(root, bd=2, relief='ridge')

#设置最下方的方框frame
down_frame = tk.Frame(root)

#设置查找框
find_frame = tk.Frame(root)
find_frame.place(relx=0, rely=(icon_height / root.winfo_height()), anchor='nw', height=find_height)

#布置最下方的状态栏
down_l1 = tk.Label(down_frame)
down_l1.config(text='就绪')
down_l1.place(relx=0, rely=1, anchor='sw')
#行数标签
down_frame_line = tk.Label(down_frame, width=10, bd=2, relief='ridge')
down_frame_line.config(text='Line=0')
down_frame_line.place(relx=1, rely=0, relheight=1, anchor='ne')
#数字标签
down_frame_figure = tk.Label(down_frame, width=5, bd=2, relief='ridge')
down_frame_figure.config(text='数字')
down_frame_figure.place(relx=0.95, rely=0, relheight=1, anchor='ne')


#图标的说明
l0 = tk.Label(root)
l1 = tk.Label(root)
l2 = tk.Label(root)
l3 = tk.Label(root)
l4 = tk.Label(root)
l5 = tk.Label(root)
l6 = tk.Label(root)
l7 = tk.Label(root)
l8 = tk.Label(root)

#设置菜单下的图标
img0 = ImageTk.PhotoImage(Image.open('image/open.png'))
img1 = ImageTk.PhotoImage(Image.open('image/save.png'))
img2 = ImageTk.PhotoImage(Image.open('image/cut.png'))
img3 = ImageTk.PhotoImage(Image.open('image/copy.png'))
img4 = ImageTk.PhotoImage(Image.open('image/paste.png'))
img5 = ImageTk.PhotoImage(Image.open('image/analyze.png'))
img6 = ImageTk.PhotoImage(Image.open('image/appear_hide.png'))
img7 = ImageTk.PhotoImage(Image.open('image/grammar_analyze.png'))
img8 = ImageTk.PhotoImage(Image.open('image/about.png'))
open_btn = tk.Button(icons, image=img0, command=lambda: open_file_menu())
save_btn = tk.Button(icons, image=img1, command=lambda: save_file_menu())
cut_btn = tk.Button(icons, image=img2, command=lambda: handle_menu_action('剪切'))
copy_btn = tk.Button(icons, image=img3, command=lambda: handle_menu_action('复制'))
paste_btn = tk.Button(icons, image=img4, command=lambda: handle_menu_action('粘贴'))
word_analyze_btn = tk.Button(icons, image=img5, command=lambda: other_function())
symbol_btn = tk.Button(icons, image=img6, command=lambda: other_function())
start_gramma_btn = tk.Button(icons, image=img7, command=lambda: other_function())
about_btn = tk.Button(icons, image=img8, command=lambda: about_menu())

#按钮绑定事件
open_btn.bind('<Enter>', lambda event: balloon_show(event, 0, l0))
open_btn.bind('<Leave>', lambda event: balloon_destroy(event, l0))
save_btn.bind('<Enter>', lambda event: balloon_show(event, 1, l1))
save_btn.bind('<Leave>', lambda event: balloon_destroy(event, l1))
cut_btn.bind('<Enter>', lambda event: balloon_show(event, 2, l2))
cut_btn.bind('<Leave>', lambda event: balloon_destroy(event, l2))
copy_btn.bind('<Enter>', lambda event: balloon_show(event, 3, l3))
copy_btn.bind('<Leave>', lambda event: balloon_destroy(event, l3))
paste_btn.bind('<Enter>', lambda event: balloon_show(event, 4, l4))
paste_btn.bind('<Leave>', lambda event: balloon_destroy(event, l4))
word_analyze_btn.bind('<Enter>', lambda event: balloon_show(event, 5, l5))
word_analyze_btn.bind('<Leave>', lambda event: balloon_destroy(event, l5))
symbol_btn.bind('<Enter>', lambda event: balloon_show(event, 6, l6))
symbol_btn.bind('<Leave>', lambda event: balloon_destroy(event, l6))
start_gramma_btn.bind('<Enter>', lambda event: balloon_show(event, 7, l7))
start_gramma_btn.bind('<Leave>', lambda event: balloon_destroy(event, l7))
about_btn.bind('<Enter>', lambda event: balloon_show(event, 8, l8))
about_btn.bind('<Leave>', lambda event: balloon_destroy(event, l8))
#图标按钮的布局
open_btn.grid(row=0, column=0, padx=1, pady=1, sticky=tk.W)
save_btn.grid(row=0, column=1, padx=1, pady=1, sticky=tk.W)
cut_btn.grid(row=0, column=2, padx=1, pady=1, sticky=tk.W)
copy_btn.grid(row=0, column=3, padx=1, pady=1, sticky=tk.W)
paste_btn.grid(row=0, column=4, padx=1, pady=1, sticky=tk.W)
word_analyze_btn.grid(row=0, column=5, padx=1, pady=1, sticky=tk.W)
symbol_btn.grid(row=0, column=6, padx=1, pady=1, sticky=tk.W)
start_gramma_btn.grid(row=0, column=7, padx=1, pady=1, sticky=tk.W)
about_btn.grid(row=0, column=8, padx=1, pady=1, sticky=tk.W)


# 在左边的frame中添加文本框
s1 = tk.Scrollbar(left_frame, command=ScrollCommand)  # 竖直滚动条
s1.place(relx=1, rely=0, width=scollar_len, relheight=1-scollar_len / left_frame.winfo_height(), anchor='ne')
s2 = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL)  # 水平滚动条
s2.place(relx=0, rely=1, relwidth=1-scollar_len / left_frame.winfo_height(), height=scollar_len, anchor='sw')
# wrap 设置不自动换行
text_left = tk.Text(left_frame, font=('Consolas', 12), yscrollcommand=s1.set, xscrollcommand=s2.set, wrap='none',
                    undo=True, maxundo=-1)
# s1.config(command=text_left.yview)
s2.config(command=text_left.xview)
text_left.bind('<KeyRelease>', highlighter_past)#绑定关键字突出
text_left.bind('<Control-f>', find)
text_left.bind('<Control-r>', replace_text)
text_left.bind('<Control-KeyRelease-v>', past_after)
text_left.bind('<Control-KeyRelease-x>', past_after)
text_left.bind("<MouseWheel>", Wheel)
s1.bind("<MouseWheel>", Wheel)
column_text.bind("<MouseWheel>", Wheel)


# 在右上边的frame中添加文本框
s3 = tk.Scrollbar(right_up_frame)  # 竖直滚动条
s3.place(relx=1, rely=0, width=scollar_len, relheight=1 - scollar_len / right_up_frame.winfo_height(), anchor='ne')
s4 = tk.Scrollbar(right_up_frame, orient=tk.HORIZONTAL)  # 水平滚动条
s4.place(relx=0, rely=1, relwidth=1 - scollar_len / right_up_frame.winfo_width(), height=scollar_len, anchor='sw')
text_right_up = tk.Text(right_up_frame, font=('宋体', 12), yscrollcommand=s3.set, xscrollcommand=s4.set, wrap='none')

s3.config(command=text_right_up.yview)
s4.config(command=text_right_up.xview)
text_right_up.configure(state=tk.DISABLED)  # 用户不可编辑

# 在右下边的frame中添加文本框
s5 = tk.Scrollbar(right_down_frame)  # 竖直滚动条
s5.place(relx=1, rely=0, width=scollar_len, relheight=1 - scollar_len / right_down_frame.winfo_height(), anchor='ne')
s6 = tk.Scrollbar(right_down_frame, orient=tk.HORIZONTAL)  # 水平滚动条
s6.place(relx=0, rely=1, relwidth=1 - scollar_len / right_down_frame.winfo_width(), height=scollar_len, anchor='sw')
text_right_down = tk.Text(right_down_frame, font=('宋体', 12), yscrollcommand=s5.set, xscrollcommand=s6.set,
                          wrap='none')

s5.config(command=text_right_down.yview)
s6.config(command=text_right_down.xview)
text_right_down.configure(state=tk.DISABLED)  # 用户不可编辑

# 设置菜单下面的图标的frame
icons.place(relx=0, rely=0, relwidth=1, height=icon_height)

# 设置最下方的方框frame
down_frame.place(relx=0, rely=1, relwidth=1, height=low_rh, anchor='sw')
text_right_up.place(relx=0, rely=0, relwidth=0.97, relheight=0.97)
text_left.place(relx=0, rely=0, relwidth=0.97, relheight=0.97)
text_right_down.place(relx=0, rely=0, relwidth=0.97, relheight=0.9)
root.update()
a = root.winfo_height()
b = root.winfo_width()
d = left_frame.winfo_width()
e = right_down_frame.winfo_height()
root.update()
#窗体大小改变事件
def change(event):
    global left_frame, right_down_frame, right_up_frame, text_left, text_right_down, text_right_up, root, a, b, d, e
    global s1, s2, s3, s4, s5, s6, icon_height, status_height, find_height, column_frame, column_width
    # root.update()
    # 规定滑块的宽度
    scollar_len = 17
    if root.winfo_height() != a or root.winfo_width() != b:
        a = root.winfo_height()
        b = root.winfo_width()
        # 行号的相对高度
        column_reh = 1 - (icon_height + status_height + find_height + scollar_len) / a
        # 设置文本框的最大相对高
        full_height = 1 - (icon_height + status_height + find_height) / a
        #布置查找框
        find_frame.place(relx=0, rely=(icon_height / a), anchor='nw', height=find_height)
        # 设置最下方frame的相对宽高
        low_rw = 1
        low_rh = status_height
        # 设置最下方的frame的相对布局
        low_rx = 0
        low_ry = 1
        #设置column_frame的宽
        column_re = column_width / b

        # 设置菜单下面的图标的frame
        icons.place(relx=0, rely=0, relwidth=1, height=icon_height)
        column_frame.place(relx=0, rely=(icon_height + find_height) / a, relwidth=column_re, relheight=full_height)
        main_frame.place(relx=column_re, rely=(icon_height + find_height) / a, relwidth=1 - column_re,
                         relheight=full_height)
        main_frame.update()
        # # 设置左边的显示原文窗口frame
        # left_frame.update()
        # # 设置右上的方框frame
        # right_up_frame.update()
        # # 设置右下的方框frame
        # right_down_frame.update()

        # 设置最下方的方框frame
        down_frame.place(relx=low_rx, rely=low_ry, relwidth=low_rw, height=low_rh, anchor='sw')
        text_right_up.place(relx=0, rely=0, relwidth=1 - scollar_len / right_up_frame.winfo_width(),
                            relheight=1 - scollar_len / right_up_frame.winfo_height())
        text_left.place(relx=0, rely=0, relwidth=1 - scollar_len / left_frame.winfo_width(),
                        relheight=1 - scollar_len / left_frame.winfo_height())
        text_right_down.place(relx=0, rely=0, relwidth=1 - scollar_len / right_down_frame.winfo_width(),
                              relheight=1 - scollar_len / right_down_frame.winfo_height())

        #左边的滑块放置
        s1.place(relx=1, rely=0, width=scollar_len, relheight=1 - scollar_len / left_frame.winfo_height(), anchor='ne')
        s2.place(relx=0, rely=1, relwidth=1 - scollar_len / left_frame.winfo_width(), height=scollar_len, anchor='sw')
        #右上的滑块放置
        s3.place(relx=1, rely=0, width=scollar_len, relheight=1 - scollar_len / right_up_frame.winfo_height(),
                 anchor='ne')
        s4.place(relx=0, rely=1, relwidth=1 - scollar_len / right_up_frame.winfo_width(), height=scollar_len,
                 anchor='sw')
        #右下的滑块放置
        s5.place(relx=1, rely=0, width=scollar_len, relheight=1 - scollar_len / right_down_frame.winfo_height(),
                 anchor='ne')
        s6.place(relx=0, rely=1, relwidth=1 - scollar_len / right_down_frame.winfo_width(), height=scollar_len,
                 anchor='sw')


root.bind("<Configure>", lambda event: change(event))

root.mainloop()
