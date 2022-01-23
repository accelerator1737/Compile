import tkinter as tk
from tkinter import ttk
import dga_optimize as dag


def get_graph(s, text):
    enter = []
    ss = s.split('\n')
    for i in ss:
        if i != '':
            n = []
            m = i.split(',')
            n.extend([m[0], m[1], m[2], m[3]])
            enter.append(n)
    you = dag.split_block(enter)
    text.config(state=tk.NORMAL)
    text.delete('1.0', 'end')
    for i in you:
        for j in i:
            text.insert(tk.END, '({}, {}, {}, {})\n'.format(j[0], j[1], j[2], j[3]))
    text.config(state=tk.DISABLED)


def start_interface():
    win = tk.Tk()
    win.title('预测分析法')
    win.geometry("{}x{}".format(500, 400))
    win.resizable(width=False, height=False)
    frame1 = tk.Frame(win, bd=2, width=230, height=340, relief='groove')
    frame2 = tk.Frame(win, bd=2, width=230, height=260, relief='groove')
    labe1_re = tk.Label(win, text='原四元式')
    labe1_re.place(x=25, y=10)
    labe1_nfa = tk.Label(win, text='优化后四元式')
    labe1_nfa.place(x=265, y=10)

    text_frame1 = tk.Frame(frame1, width=210, height=320, bd=2, relief='sunken')
    text_frame1.place(x=10, y=10)
    s1 = tk.Scrollbar(text_frame1)  # 竖直滚动条
    s1.place(relx=1, y=0, width=16, height=300, anchor='ne')
    s2 = tk.Scrollbar(text_frame1, orient=tk.HORIZONTAL)  # 水平滚动条
    s2.place(relx=0, rely=1, relwidth=1, height=15, anchor='sw')
    # wrap 设置不自动换行
    text_left = tk.Text(text_frame1, font=('Times New Roman', 10), yscrollcommand=s1.set, xscrollcommand=s2.set,
                        wrap='none', undo=True, maxundo=-1, width=31, height=20)
    s1.config(command=text_left.yview)
    s2.config(command=text_left.xview)
    text_left.place(x=0, y=0)
    f = open('test_dag.txt', 'r')
    s = f.read()
    f.close()
    text_left.insert(tk.END, s)

    text_frame2 = tk.Frame(frame2, width=210, height=240, bd=2, relief='sunken')
    text_frame2.place(x=10, y=10)
    s3 = tk.Scrollbar(text_frame2)  # 竖直滚动条
    s3.place(relx=1, y=0, width=16, height=220, anchor='ne')
    s4 = tk.Scrollbar(text_frame2, orient=tk.HORIZONTAL)  # 水平滚动条
    s4.place(relx=0, rely=1, relwidth=1, height=20, anchor='sw')
    # wrap 设置不自动换行
    text_left1 = tk.Text(text_frame2, font=('Times New Roman', 10), yscrollcommand=s3.set, xscrollcommand=s4.set,
                        wrap='none', undo=True, maxundo=-1, width=31, height=14, state=tk.DISABLED)
    s3.config(command=text_left1.yview)
    s4.config(command=text_left1.xview)
    text_left1.place(x=0, y=0)

    # 总的布局
    frame1.place(x=15, y=20, anchor='nw')
    frame2.place(x=255, y=20)
    b1 = ttk.Button(win, text='DAG优化四元式', width=31, command=lambda: get_graph(text_left.get('1.0', 'end-1c'), text_left1))
    b1.place(x=255, y=300)

    win.mainloop()

# start_interface()