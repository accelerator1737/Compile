import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import showinfo


filename = ''


#打开文件
def open_file_menu():
    global filename
    filename = askopenfilename()
    if filename != '':
        txt1 = open(filename, "r").read()  # 读取选择文件的内容
        text_left.delete('1.0', 'end')  # 删除文本框中的内容
        text_left.insert(tk.END, txt1)  # 写入文件当中的内容
        #解除禁用
        filemenu.entryconfig("保存(S)", state=tk.NORMAL)
        filemenu.entryconfig("另存为(A)", state=tk.NORMAL)
        filemenu.entryconfig("最近文件", state=tk.NORMAL)
        edit_mene.entryconfig("全选(A)", state=tk.NORMAL)

#保存文件
def save_file_menu():
    txt1 = text_left.get('1.0', 'end-1c')  # 得到文本框中所有的内容
    f = open(filename, "w")
    f.write(txt1)
    f.close()


#文件的另存为
def another_save_file_menu():
    file = asksaveasfilename(title=u'另存为', defaultextension='.txt')
    txt1 = text_left.get('1.0', 'end-1c')  # 得到文本框中所有的内容
    f = open(file, "w")
    f.write(txt1)
    f.close()


#其他按键的敷衍功能
def other_function():
    txt1 = text_left.get('1.0', 'end-1c')  # 得到文本框中所有的内容
    text_right_up.config(state=tk.NORMAL)
    text_right_down.config(state=tk.NORMAL)
    text_right_up.delete('1.0', 'end')  # 删除文本框中的内容
    text_right_up.insert(tk.END, txt1)  # 写入文件当中的内容
    text_right_down.delete('1.0', 'end')  # 删除文本框中的内容
    text_right_down.insert(tk.END, txt1)  # 写入文件当中的内容


#打开帮助文档
def bound_help():
    os.startfile(r'E:\编译原理\help.chm')


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
    showinfo(title="关于", message="想欣赏妾身的舞姿吗？")


#词法分析
def word_analyze():
    other_function()


#NFA_DFA_MFA
def nfa():
    other_function()


#语法分析
def langurage_analyze():
    other_function()


#LL(1)预测分析
def ll():
    other_function()


#运算符优先
def opration_first():
    other_function()


#LR分析器
def lr():
    other_function()


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
mid_code_menu = tk.Menu(menubar, tearoff=False, postcommand=lambda: other_function())
# 将其加入主菜单
menubar.add_cascade(label="中间代码(M)", menu=mid_code_menu)

# 创建一个子菜单“目标代码生成”，然后将它添加到顶级菜单中
arm_code_menu = tk.Menu(menubar, tearoff=False, postcommand=lambda: other_function())
# 将其加入主菜单
menubar.add_cascade(label="目标代码生成(O)", menu=arm_code_menu)

# 设置选择框的状态
select_status1 = tk.IntVar()
select_status2 = tk.IntVar()
select_status3 = tk.IntVar()
# 设置默认显示选择框
select_status1.set(1)
select_status2.set(1)
# 创建一个子菜单“查看”，然后将它添加到顶级菜单中
look_menu = tk.Menu(menubar, tearoff=False)
look_menu.add_checkbutton(label="工具栏", variable=select_status1)
look_menu.add_checkbutton(label="显示栏", variable=select_status2)
look_menu.add_checkbutton(label="显示符号表信息", variable=select_status3)
# 将其加入主菜单
menubar.add_cascade(label="查看(V)", menu=look_menu)

# 创建一个子菜单“帮助”，然后将它添加到顶级菜单中
help_menu = tk.Menu(menubar, tearoff=False)
help_menu.add_command(label="帮助", command=lambda: bound_help())
help_menu.add_command(label="关于本软件", command=lambda: about_menu())
# 将其加入主菜单
menubar.add_cascade(label="帮助(H)", menu=help_menu)

# 显示菜单
root.config(menu=menubar)
root.update()

#设置图标框的高度
icon_height = 28
#设置状态栏高度
status_height = 20
#设置文本框的最大相对高
full_height = 1 - (icon_height + status_height) / root.winfo_height()

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
lf_ry = icon_height / root.winfo_height()
#设置右上frame的相对布局
ruf_rx = lf_rw
ruf_ry = icon_height / root.winfo_height()
#设置右下frame的相对布局
rdf_rx = lf_rw
rdf_ry = ruf_ry + ruf_rh
#设置最下方的frame的相对布局
low_rx = 0
low_ry = 1

#设置菜单下面的图标的frame
icons = tk.Frame(root, bd=2, relief='ridge')

#设置左边的显示原文窗口frame
left_frame = tk.Frame(root, bd=2, relief='ridge')

#设置右上的方框frame
right_up_frame = tk.Frame(root, bd=2, relief='ridge')

#设置右下的方框frame
right_down_frame = tk.Frame(root, bd=2, relief='ridge')

#设置最下方的方框frame
down_frame = tk.Frame(root)

#布置最下方的状态栏
down_l1 = tk.Label(down_frame)
down_l1.config(text='就绪')
down_l1.place(relx=0, rely=0, anchor='nw')
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
img0 = ImageTk.PhotoImage(Image.open('open.png'))
img1 = ImageTk.PhotoImage(Image.open('save.png'))
img2 = ImageTk.PhotoImage(Image.open('cut.png'))
img3 = ImageTk.PhotoImage(Image.open('copy.png'))
img4 = ImageTk.PhotoImage(Image.open('paste.png'))
img5 = ImageTk.PhotoImage(Image.open('analyze.png'))
img6 = ImageTk.PhotoImage(Image.open('appear_hide.png'))
img7 = ImageTk.PhotoImage(Image.open('grammar_analyze.png'))
img8 = ImageTk.PhotoImage(Image.open('about.png'))
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

#规定滑块的宽度
scollar_len = 30
# 在左边的frame中添加文本框
s1 = tk.Scrollbar(left_frame)  # 竖直滚动条
s1.place(relx=1, rely=0, relwidth=0.03, relheight=0.97, anchor='ne')
s2 = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL)  # 水平滚动条
s2.place(relx=0, rely=1, relwidth=0.97, relheight=0.03, anchor='sw')
# wrap 设置不自动换行
text_left = tk.Text(left_frame, font=('Arial', 12), yscrollcommand=s1.set, xscrollcommand=s2.set, wrap='none',
                    undo=True, maxundo=-1)
s1.config(command=text_left.yview)
s2.config(command=text_left.xview)


# 在右上边的frame中添加文本框
s3 = tk.Scrollbar(right_up_frame)  # 竖直滚动条
s3.place(relx=1, rely=0, relwidth=0.03, relheight=0.97, anchor='ne')
s4 = tk.Scrollbar(right_up_frame, orient=tk.HORIZONTAL)  # 水平滚动条
s4.place(relx=0, rely=1, relwidth=0.97, relheight=0.03, anchor='sw')
text_right_up = tk.Text(right_up_frame, font=('Arial', 12), yscrollcommand=s3.set, xscrollcommand=s4.set, wrap='none')

s3.config(command=text_right_up.yview)
s4.config(command=text_right_up.xview)
text_right_up.configure(state=tk.DISABLED)  # 用户不可编辑

# 在右下边的frame中添加文本框
s5 = tk.Scrollbar(right_down_frame)  # 竖直滚动条
s5.place(relx=1, rely=0, relwidth=0.03, relheight=0.9, anchor='ne')
s6 = tk.Scrollbar(right_down_frame, orient=tk.HORIZONTAL)  # 水平滚动条
s6.place(relx=0, rely=1, relwidth=0.97, relheight=0.1, anchor='sw')
text_right_down = tk.Text(right_down_frame, font=('Arial', 12), yscrollcommand=s5.set, xscrollcommand=s6.set,
                          wrap='none')

s5.config(command=text_right_down.yview)
s6.config(command=text_right_down.xview)
text_right_down.configure(state=tk.DISABLED)  # 用户不可编辑

# 设置菜单下面的图标的frame
icons.place(relx=0, rely=0, relwidth=1, height=icon_height)

# 设置左边的显示原文窗口frame
left_frame.place(relx=lf_rx, rely=lf_ry, relwidth=lf_rw, relheight=lf_rh)

# 设置右上的方框frame
right_up_frame.place(relx=ruf_rx, rely=ruf_ry, relwidth=ruf_rw, relheight=ruf_rh)

# 设置右下的方框frame
right_down_frame.place(relx=rdf_rx, rely=rdf_ry, relwidth=rdf_rw, relheight=rdf_rh)

# 设置最下方的方框frame
down_frame.place(relx=low_rx, rely=low_ry, relwidth=low_rw, height=low_rh, anchor='sw')
text_right_up.place(relx=0, rely=0, relwidth=0.97, relheight=0.97)
text_left.place(relx=0, rely=0, relwidth=0.97, relheight=0.97)
text_right_down.place(relx=0, rely=0, relwidth=0.97, relheight=0.9)
root.update()
a = root.winfo_height()
b = root.winfo_width()

#窗体大小改变事件
def change(event):
    global left_frame, right_down_frame, right_up_frame, text_left, text_right_down, text_right_up, root, a, b
    global s1, s2, s3, s4, s5, s6
    root.update()
    if root.winfo_height() != a or root.winfo_width() != b:
        a = root.winfo_height()
        b = root.winfo_width()
        # 设置图标框的高度
        icon_height = 28
        # 设置状态栏高度
        status_height = 20
        # 设置文本框的最大相对高
        full_height = 1 - (icon_height + status_height) / a

        # 设置左frame的相对宽高
        lf_rw = 0.5
        lf_rh = full_height
        # 设置右上frame的相对宽高
        ruf_rw = 1 - lf_rw
        ruf_rh = 0.7
        # 设置右下frame的相对宽高
        rdf_rw = 1 - lf_rw
        rdf_rh = full_height - ruf_rh
        # 设置最下方frame的相对宽高
        low_rw = 1
        low_rh = status_height

        # 设置左frame的相对布局
        lf_rx = 0
        lf_ry = icon_height / a
        # 设置右上frame的相对布局
        ruf_rx = lf_rw
        ruf_ry = icon_height / a
        # 设置右下frame的相对布局
        rdf_rx = lf_rw
        rdf_ry = ruf_ry + ruf_rh
        # 设置最下方的frame的相对布局
        low_rx = 0
        low_ry = 1

        # 设置菜单下面的图标的frame
        icons.place(relx=0, rely=0, relwidth=1, height=icon_height)

        # 设置左边的显示原文窗口frame
        left_frame.place(relx=lf_rx, rely=lf_ry, relwidth=lf_rw, relheight=lf_rh)
        left_frame.update()
        # 设置右上的方框frame
        right_up_frame.place(relx=ruf_rx, rely=ruf_ry, relwidth=ruf_rw, relheight=ruf_rh)
        right_up_frame.update()
        # 设置右下的方框frame
        right_down_frame.place(relx=rdf_rx, rely=rdf_ry, relwidth=rdf_rw, relheight=rdf_rh)
        right_down_frame.update()
        # 规定滑块的宽度
        scollar_len = 17

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
