import tkinter as tk
import re_mfa_test as re2mfa
import tkinter.messagebox
from tkinter import ttk
import os

inspect = False
shuru = ''


def check(s, b2, b3, b4, b5, b6, b7):
    global inspect, shuru
    inspect = re2mfa.check_string(s)
    if inspect:
        shuru = s
        b2.config(state=tk.NORMAL)
        b3.config(state=tk.NORMAL)
        b4.config(state=tk.NORMAL)
        b5.config(state=tk.NORMAL)
        b6.config(state=tk.NORMAL)
        b7.config(state=tk.NORMAL)
    if not inspect:
        tkinter.messagebox.showerror('错误提示', '表达式出错')


def table_nfa(text_left, e1, e2):    #生成nfa状态集
    global shuru
    e1.config(state=tk.NORMAL)
    e2.config(state=tk.NORMAL)
    nfa = re2mfa.generate_nfa_set(shuru)
    text_left.delete('1.0', 'end')
    for i in range(len(nfa)):
        if i != len(nfa) - 1:
            text_left.insert(tk.END, f"{str(nfa[i][0]):<4s}              {str(nfa[i][1]):^4s}             {str(nfa[i][2]):>4s}\n")
        else:
            text_left.insert(tk.END, f"{str(nfa[i][0]):<4s}              {str(nfa[i][1]):^4s}             {str(nfa[i][2]):>4s}")
    e1.delete(0, tk.END)
    e1.insert(tk.END, 'X')
    e2.delete(0, tk.END)
    e2.insert(tk.END, 'Y')
    e1.config(state=tk.DISABLED)
    e2.config(state=tk.DISABLED)


def table_dfa(text_left, e1, e2):    #生成dfa状态集
    global shuru
    e1.config(state=tk.NORMAL)
    e2.config(state=tk.NORMAL)
    dfa, last = re2mfa.generate_dfa_set(shuru)
    text_left.delete('1.0', 'end')
    for i in range(len(dfa)):
        if i != len(dfa) - 1:
            text_left.insert(tk.END,
                             f"{str(dfa[i][0]):<4s}              {str(dfa[i][1]):^4s}             {str(dfa[i][2]):>4s}\n")
        else:
            text_left.insert(tk.END,
                             f"{str(dfa[i][0]):<4s}              {str(dfa[i][1]):^4s}             {str(dfa[i][2]):>4s}")
    e1.delete(0, tk.END)
    e1.insert(tk.END, '0')
    e2.delete(0, tk.END)
    for i in range(len(last)):
        if i != len(last) - 1:
            e2.insert(tk.END, str(last[i]) + ',')
        else:
            e2.insert(tk.END, str(last[i]))
    e1.config(state=tk.DISABLED)
    e2.config(state=tk.DISABLED)


def table_mfa(text_left, e1, e2):    #生成mfa状态集
    global shuru
    e1.config(state=tk.NORMAL)
    e2.config(state=tk.NORMAL)
    mfa, last = re2mfa.generate_mfa_set(shuru)
    text_left.delete('1.0', 'end')
    for i in range(len(mfa)):
        if i != len(mfa) - 1:
            text_left.insert(tk.END,
                             f"{str(mfa[i][0]):<4s}              {str(mfa[i][1]):^4s}             {str(mfa[i][2]):>4s}\n")
        else:
            text_left.insert(tk.END,
                             f"{str(mfa[i][0]):<4s}              {str(mfa[i][1]):^4s}             {str(mfa[i][2]):>4s}")
    e1.delete(0, tk.END)
    e1.insert(tk.END, '0')
    e2.delete(0, tk.END)
    for i in range(len(last)):
        if i != len(last) - 1:
            e2.insert(tk.END, str(last[i]) + ',')
        else:
            e2.insert(tk.END, str(last[i]))
    e1.config(state=tk.DISABLED)
    e2.config(state=tk.DISABLED)


def image_nfa():    #生成nfa图像
    global shuru
    re2mfa.generate_nfa_image(shuru)


def image_dfa():    #生成dfa图像
    # global shuru
    re2mfa.generate_dfa_image(shuru)


def image_mfa():    #生成mfa图像
    global shuru
    re2mfa.generate_mfa_image(shuru)


def start_interface():
    win = tk.Tk()
    win.geometry("{}x{}".format(800, 600))
    win.resizable(width=False, height=False)
    top_frame = tk.Frame(win, bd=2, width=770, height=50, relief='groove')
    frame1 = tk.Frame(win, bd=2, width=250, height=500, relief='groove')
    frame2 = tk.Frame(win, bd=2, width=250, height=500, relief='groove')
    frame3 = tk.Frame(win, bd=2, width=250, height=500, relief='groove')

    #设计最左边
    text_frame1 = tk.Frame(frame1, width=230, height=380, bd=2, relief='sunken')
    text_frame1.place(x=10, y=10)
    s1 = tk.Scrollbar(text_frame1)  # 竖直滚动条
    s1.place(relx=1, y=20, width=16, height=360, anchor='ne')
    s2 = tk.Scrollbar(text_frame1, orient=tk.HORIZONTAL)  # 水平滚动条
    s2.place(relx=0, rely=1, relwidth=1, height=15, anchor='sw')
    # wrap 设置不自动换行
    text_left = tk.Text(text_frame1, font=('Times New Roman', 12), yscrollcommand=s1.set, xscrollcommand=s2.set,
                        wrap='none', undo=True, maxundo=-1, width=26, height=18)
    s1.config(command=text_left.yview)
    s2.config(command=text_left.xview)
    text_left.place(x=0, y=20)
    l2 = tk.Label(text_frame1, text='   起始状态   ', height=1, bd=1, relief='sunken')
    l2.place(x=0, y=0)
    l3 = tk.Label(text_frame1, text='  接收符号   ', height=1, bd=1, relief='sunken')
    l3.place(x=70, y=0)
    l4 = tk.Label(text_frame1, text='  到达状态   ', height=1, bd=1, relief='sunken')
    l4.place(x=138, y=0)
    label3 = tk.Label(frame1, text='开始状态：')
    label3.place(x=10, y=398)
    e2 = tk.Entry(frame1, state=tk.DISABLED)     #输出开始状态
    e2.place(x=80, y=400)
    label5 = tk.Label(frame1, text='终结状态：')
    label5.place(x=10, y=423)
    e3 = tk.Entry(frame1, state=tk.DISABLED)  # 输出结束状态
    e3.place(x=80, y=425)
    b2 = ttk.Button(frame1, text='生成NFA状态集', command=lambda: table_nfa(text_left, e2, e3), state=tk.DISABLED)
    b2.place(x=10, y=455)
    b3 = ttk.Button(frame1, text='生成NFA图', command=lambda: image_nfa(), state=tk.DISABLED)
    b3.place(x=240, y=455, anchor='ne')

    # 设计中间
    text_frame2 = tk.Frame(frame2, width=230, height=380, bd=2, relief='sunken')
    text_frame2.place(x=10, y=10)
    s3 = tk.Scrollbar(text_frame2)  # 竖直滚动条
    s3.place(relx=1, y=20, width=16, height=360, anchor='ne')
    s4 = tk.Scrollbar(text_frame2, orient=tk.HORIZONTAL)  # 水平滚动条
    s4.place(relx=0, rely=1, relwidth=1, height=15, anchor='sw')
    # wrap 设置不自动换行
    text_left1 = tk.Text(text_frame2, font=('Times New Roman', 12), yscrollcommand=s3.set, xscrollcommand=s4.set,
                        wrap='none', undo=True, maxundo=-1, width=26, height=18)
    s3.config(command=text_left1.yview)
    s4.config(command=text_left1.xview)
    text_left1.place(x=0, y=20)
    l5 = tk.Label(text_frame2, text='   起始状态   ', height=1, bd=1, relief='sunken')
    l5.place(x=0, y=0)
    l6 = tk.Label(text_frame2, text='  接收符号   ', height=1, bd=1, relief='sunken')
    l6.place(x=70, y=0)
    l7 = tk.Label(text_frame2, text='  到达状态   ', height=1, bd=1, relief='sunken')
    l7.place(x=138, y=0)
    label7 = tk.Label(frame2, text='开始状态：')
    label7.place(x=10, y=398)
    e4 = tk.Entry(frame2, state=tk.DISABLED)  # 输出开始状态
    e4.place(x=80, y=400)
    label9 = tk.Label(frame2, text='终结状态：')
    label9.place(x=10, y=423)
    e5 = tk.Entry(frame2, state=tk.DISABLED)  # 输出结束状态
    e5.place(x=80, y=425)
    b4 = ttk.Button(frame2, text='生成DFA状态集', command=lambda: table_dfa(text_left1, e4, e5), state=tk.DISABLED)
    b4.place(x=10, y=455)
    b5 = ttk.Button(frame2, text='生成DFA图', command=lambda: image_dfa(), state=tk.DISABLED)
    b5.place(x=240, y=455, anchor='ne')

    # 设计最右边
    text_frame3 = tk.Frame(frame3, width=230, height=380, bd=2, relief='sunken')
    text_frame3.place(x=10, y=10)
    s5 = tk.Scrollbar(text_frame3)  # 竖直滚动条
    s5.place(relx=1, y=20, width=16, height=360, anchor='ne')
    s6 = tk.Scrollbar(text_frame3, orient=tk.HORIZONTAL)  # 水平滚动条
    s6.place(relx=0, rely=1, relwidth=1, height=15, anchor='sw')
    # wrap 设置不自动换行
    text_left2 = tk.Text(text_frame3, font=('Times New Roman', 12), yscrollcommand=s5.set, xscrollcommand=s6.set,
                         wrap='none', undo=True, maxundo=-1, width=26, height=18)
    s5.config(command=text_left2.yview)
    s6.config(command=text_left2.xview)
    text_left2.place(x=0, y=20)
    l8 = tk.Label(text_frame3, text='   起始状态   ', height=1, bd=1, relief='sunken')
    l8.place(x=0, y=0)
    l9 = tk.Label(text_frame3, text='  接收符号   ', height=1, bd=1, relief='sunken')
    l9.place(x=70, y=0)
    l10 = tk.Label(text_frame3, text='  到达状态   ', height=1, bd=1, relief='sunken')
    l10.place(x=138, y=0)
    label11 = tk.Label(frame3, text='开始状态：')
    label11.place(x=10, y=398)
    e6 = tk.Entry(frame3, state=tk.DISABLED)  # 输出开始状态
    e6.place(x=80, y=400)
    label13 = tk.Label(frame3, text='终结状态：')
    label13.place(x=10, y=423)
    e7 = tk.Entry(frame3, state=tk.DISABLED)  # 输出结束状态
    e7.place(x=80, y=425)
    b6 = ttk.Button(frame3, text='生成MFA状态集', command=lambda: table_mfa(text_left2, e6, e7), state=tk.DISABLED)
    b6.place(x=10, y=455)
    b7 = ttk.Button(frame3, text='生成MFA图', command=lambda: image_mfa(), state=tk.DISABLED)
    b7.place(x=240, y=455, anchor='ne')

    # 设计最顶层
    label1 = tk.Label(top_frame, text='请输入一个正则表达式:')
    label1.place(x=0, y=24, anchor='w')
    e1 = tk.Entry(top_frame, width=60)
    e1.insert(0, 'a*b|c')
    e1.place(x=130, y=24, anchor='w')
    b1 = ttk.Button(top_frame, text='验证正则表达式', command=lambda: check(e1.get(), b2, b3, b4, b5, b6, b7))
    b1.place(x=760, y=24, anchor='e')
    label2 = tk.Label(top_frame, text='例如: a*b|c')
    label2.place(x=620, y=24, anchor='e')

    labe1_re = tk.Label(win, text='表达式')
    labe1_re.place(x=25, y=10)
    labe1_nfa = tk.Label(win, text='正则->NFA')
    labe1_nfa.place(x=25, y=75)
    labe1_dfa = tk.Label(win, text='NFA->DFA')
    labe1_dfa.place(x=285, y=75)
    labe1_mfa = tk.Label(win, text='DFA->MFA')
    labe1_mfa.place(x=545, y=75)

    frame1.place(x=15, y=85)
    frame2.place(x=275, y=85)
    frame3.place(x=535, y=85)
    top_frame.place(x=15, y=20)
    win.mainloop()



# start_interface()
