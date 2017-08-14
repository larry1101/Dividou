"""
已知bugs：
缩小程序对话框的时候会导致某些控件消失，再放大的时候消失的控件就会重新出现……
对于文件a，如果目标分类文件夹内有文件名相同哈希值不同的文件b存在，会导致a可以无限复制进去……
"""
import os
from tkinter import *
from tkinter import simpledialog

import shutil
from PIL import ImageTk, Image

from file_operator import *


class Dividour:
    def __init__(self):
        self.__init_obj__()
        self.chosen_source_file_path = None
        self.chosen_source_file_index = -1
        self.__init_UI__()
        self.__init_data__()
        self.root_window.mainloop()

    def __init_obj__(self):
        self.direader = Direader()
        self.destreader = Direader()
        self.file_display_manager = self.FileDisplayManager()

    def __init_UI__(self):
        # window
        self.root_window = Tk()
        self.root_window.title('Dividou')
        self.root_window.bind('<Expose>', self.on_window_resize)

        self.mainframe = Frame(self.root_window)
        self.mainframe.pack(expand=True, fill=BOTH)

        # operation frame
        self.oper_win = Frame(self.mainframe)
        self.oper_win.pack(fill=BOTH, expand=True)

        # dirs to get sources
        self.dirs_source = Frame(self.oper_win)
        self.dirs_source.pack(fill=Y, side=LEFT)

        # monitor
        self.label_source_path = Label(self.dirs_source)
        self.label_source_path.pack(side=TOP, fill=X)

        # navigation
        self.dirs_source_navigation = Frame(self.dirs_source)
        self.dirs_source_navigation.pack(anchor=N, side=TOP, fill=X)

        # navigation buttons
        Button(self.dirs_source_navigation,
               text='Home',
               command=self.dir_s_home
               ).pack(side=LEFT, fill=X, expand=True)
        Button(self.dirs_source_navigation,
               text='Back',
               command=self.dir_s_back
               ).pack(side=LEFT, fill=X, expand=True)

        # dirs and filter

        frame_dir_n_filter = Frame(self.dirs_source)
        frame_dir_n_filter.pack(side=LEFT, expand=True, fill=BOTH)

        # dirs list
        self.lv_dirs_source = Listbox(frame_dir_n_filter)
        self.lv_dirs_source.pack(side=TOP, expand=True, fill=BOTH, padx=1)
        self.lv_dirs_source.bind("<Double-Button-1>", self.on_lv_dir_s_db_click)

        # filter
        self.lv_file_filter = Listbox(frame_dir_n_filter, selectmode=MULTIPLE)
        self.lv_file_filter.pack(side=TOP, fill=X, padx=1)
        self.lv_file_filter.bind("<ButtonRelease-1>", self.on_filter_selection_change)

        # filter btns
        Button(frame_dir_n_filter,
               text='Clear Select',
               command=self.on_btn_clear_filter
               ).pack(side=LEFT, padx=1, fill=X)

        Button(frame_dir_n_filter,
               text='Select All',
               command=self.on_btn_full_filter
               ).pack(side=LEFT, padx=1, fill=X)

        # files in dir
        self.lv_files_source = Listbox(self.dirs_source)
        self.lv_files_source.pack(side=LEFT, fill=BOTH, padx=1)
        self.lv_files_source.bind("<ButtonRelease-1>", self.on_lv_file_sel)

        # img display frame
        img_monitor = Frame(self.oper_win, bg='#E8F2DB')
        img_monitor.pack(side=LEFT, fill=BOTH, expand=True)

        # img path
        self.label_file_chosen = Label(img_monitor, text='选择的文件显示的地方')
        self.label_file_chosen.pack(side=TOP, fill=X)

        # img view
        # holder
        self.img_view_holder = Frame(img_monitor, bg='#EEF4F9', height=404, width=404)
        self.img_view_holder.pack(side=TOP, expand=True, fill=BOTH, padx=2, pady=2)

        # view
        self.img_view = Label(self.img_view_holder, bg='#DDD', height=400, width=400)  # 这里应该按照显示器改吧……
        self.img_view.bind('<Double-Button-1>', self.on_click_img_view)

        # dest
        dest = Frame(self.oper_win)
        dest.pack(anchor=NE, fill=Y, expand=True)

        # dest path root monitor
        self.label_dest_path = Label(dest, text='the dest path')
        self.label_dest_path.pack(side=TOP, fill=X)

        # navigation
        dirs_dest_navigation = Frame(dest)
        dirs_dest_navigation.pack(side=TOP, fill=X)

        # navigation buttons
        Button(dirs_dest_navigation,
               text='Home',
               command=self.dir_d_home
               ).pack(side=LEFT, fill=X, expand=True)
        Button(dirs_dest_navigation,
               text='Back',
               command=self.dir_d_back
               ).pack(side=LEFT, fill=X, expand=True)

        # dest dirs frame
        frame_dest_dirs = Frame(dest)
        frame_dest_dirs.pack(side=LEFT, expand=True, fill=BOTH)

        # OK BUTTON
        Button(frame_dest_dirs,
               text='Copy\nor press Enter',
               command=self.on_btn_copy
               ).pack(side=TOP, fill=X, padx=1)

        # chosen dir name
        self.label_chosen_dir = Label(frame_dest_dirs)
        self.label_chosen_dir.pack(side=TOP, fill=X)

        # dest dirs' path
        self.lv_dirs_dest = Listbox(frame_dest_dirs, selectmode=MULTIPLE)
        self.lv_dirs_dest.pack(expand=True, fill=BOTH, padx=1)
        self.lv_dirs_dest.bind("<Key>", self.on_lv_dirs_dest_key)

        # clear choose button
        Button(frame_dest_dirs,
               text='Clear',
               command=self.on_btn_clear_dest_dir_chosen_clicked
               ).pack(side=TOP, fill=X, padx=1)

        # new folder button
        Button(frame_dest_dirs,
               text='+',
               command=self.on_btn_new_folder_clicked
               ).pack(side=TOP, fill=X, padx=1)

        # dest dirs chooser
        self.lv_dirs_dest_root = Listbox(dest)
        self.lv_dirs_dest_root.pack(side=LEFT, expand=True, fill=BOTH, padx=1)
        self.lv_dirs_dest_root.bind("<Double-Button-1>", self.on_lv_dir_d_root_db_click)
        self.lv_dirs_dest_root.bind("<ButtonRelease-1>", self.on_lv_dir_d_root_sg_click)

        # btn ok, copy file 2 chosen dest dirs

        # dock, only an exit button
        self.dock = Frame(self.mainframe, height=20)
        self.dock.pack(side=BOTTOM, fill=X)

        # btn exit
        Button(self.dock,
               text='Exit',
               width=40, height=2,
               command=self.root_window.destroy
               ).pack(fill=BOTH, expand=True)

    def __init_data__(self):
        # dir sources
        self.refresh_lv_dir_s()
        self.refresh_lv_dir_root_d()

    def dir_s_home(self):
        self.direader.home()
        self.refresh_lv_dir_s()
        self.refresh_lv_file_s()

    def dir_s_back(self):
        self.direader.back()
        self.refresh_lv_dir_s()
        self.refresh_lv_file_s()

    def dir_d_home(self):
        self.destreader.home()
        self.refresh_lv_dir_root_d()
        self.refresh_lv_dirs_d()

    def dir_d_back(self):
        self.destreader.back()
        self.refresh_lv_dir_root_d()
        self.refresh_lv_dirs_d()

    def refresh_lv_dir_s(self):
        """
        左侧navigator，刷新正在浏览的文件夹里的文件夹们
        """
        self.lv_dirs_source.delete(0, END)
        for 文件夹 in self.direader.dirs:
            self.lv_dirs_source.insert(END, 文件夹)
        self.label_source_path['text'] = self.direader.get_tmp_path()

    def refresh_lv_file_s(self):
        """
        左侧navigator，刷新正在浏览的文件夹里的文件们
        """
        self.lv_files_source.delete(0, END)
        self.clear_cur_sel_s_file()
        for file in self.direader.files:
            self.lv_files_source.insert(END, file)
        # 下面的filter
        self.lv_file_filter.delete(0, END)
        if self.direader.files_ext_names.__len__() == 0:
            # self.lv_file_filter.insert(END, '所在目录里面没有文件')
            return
        for ext_name in self.direader.files_ext_names:
            self.lv_file_filter.insert(END, ext_name)

    def refresh_lv_dir_root_d(self):
        """
        右侧destination，刷新显示正在浏览的文件夹里有哪些文件夹
        """
        self.lv_dirs_dest_root.delete(0, END)
        for 文件夹 in self.destreader.dirs:
            self.lv_dirs_dest_root.insert(END, 文件夹)
        self.label_dest_path['text'] = self.destreader.get_tmp_path()

    def refresh_lv_dirs_d(self):
        """
        单击了右侧dir list中的item，显示选取的文件夹内包含的文件夹到右侧左框
        """
        self.lv_dirs_dest.delete(0, END)
        for deep_dir in self.destreader.deeper_dirs:
            self.lv_dirs_dest.insert(END, deep_dir)
        self.label_chosen_dir['text'] = self.destreader.temp_deeper_dir_name

    # def refresh_lv_filter(self):
    #     """
    #     左侧navigator，所在目录变化时调用
    #     """
    #     self.lv_file_filter.delete(0, END)
    #     if self.direader.files_ext_names.__len__() == 0:
    #         self.lv_file_filter.insert(END, '所在目录里面没有文件')
    #         return
    #     for ext_name in self.direader.files_ext_names:
    #         self.lv_file_filter.insert(END, ext_name)

    def on_lv_dir_s_db_click(self, event):
        if self.lv_dirs_source.curselection() == ():
            print('No item to select')
            return
        cur_sel_index = self.lv_dirs_source.curselection()[0]
        self.direader.enter_dir(cur_sel_index)
        self.refresh_lv_dir_s()
        self.refresh_lv_file_s()

    def on_lv_dir_d_root_db_click(self, event):
        if self.lv_dirs_dest_root.curselection() == ():
            print('No item to select')
            return
        cur_sel_index = self.lv_dirs_dest_root.curselection()[0]
        self.destreader.enter_dir(cur_sel_index)
        self.refresh_lv_dir_root_d()
        self.refresh_lv_dirs_d()

    def on_lv_dir_d_root_sg_click(self, event):
        if self.lv_dirs_dest_root.curselection() == ():
            return
        cur_sel_index = self.lv_dirs_dest_root.curselection()[0]
        self.destreader.get_deeper(cur_sel_index)
        self.refresh_lv_dirs_d()

    def on_btn_new_folder_clicked(self):
        if self.lv_dirs_dest_root.curselection() is ():
            print('错误：还没选择分类的根文件夹，新文件夹没有办法创建')
            return
        folder_name = simpledialog.askstring('Folder Name Picker', '\n\t\t请输入新文件夹的名字，点击“OK”将会在目标分类根文件夹内创建新文件夹\t\t\n')
        if folder_name is '' or folder_name is None:
            print('错误：未获得分类文件夹名，新文件夹没有办法创建')
            return
        try:
            os.mkdir(self.destreader.temp_dir_path + self.destreader.temp_deeper_dir_name + os.sep + folder_name)
            print('在', self.destreader.temp_dir_path + self.destreader.temp_deeper_dir_name, '里面，\n\t成功创建了文件夹：',
                  folder_name)
            self.destreader.refresh_deeper()
            self.refresh_lv_dirs_d()
        except FileExistsError:
            print('错误：在', self.destreader.temp_dir_path + self.destreader.temp_deeper_dir_name, '里面，\n\t文件夹【',
                  folder_name, '】已存在，新文件夹没有创建成功')

    def on_btn_clear_dest_dir_chosen_clicked(self):
        print('清空选择')
        self.lv_dirs_dest.selection_clear(0, END)

    def on_filter_selection_change(self, event=None):
        self.lv_files_source.delete(0, END)
        sel_ext_names = [self.direader.files_ext_names[index] for index in self.lv_file_filter.curselection()]
        for cur_file in self.direader.files:
            index = cur_file.rfind('.')
            ext_name = 'no ext name'
            if index >= 0:
                ext_name = cur_file[index:]
            if ext_name in sel_ext_names:
                self.lv_files_source.insert(END, cur_file)

    def on_btn_clear_filter(self):
        self.lv_file_filter.selection_clear(0, END)
        self.on_filter_selection_change()

    def on_btn_full_filter(self):
        self.lv_file_filter.selection_set(0, END)
        self.on_filter_selection_change()

    def on_lv_dirs_dest_key(self, event):
        if event.keysym == 'Return':
            # 在右侧选择完后按下了回车，call on_btn_copy
            self.on_btn_copy()

    def on_lv_file_sel(self, event=None):
        if self.lv_files_source.curselection() == ():
            return
        self.chosen_source_file_index = self.lv_files_source.curselection()[0]
        sel_file = self.lv_files_source.get(self.chosen_source_file_index)
        # monitor 显示 格式
        self.chosen_source_file_path = self.direader.temp_dir_path + sel_file
        self.display_chosen_file()

    class FileDisplayManager:
        def __init__(self):
            self.SUPPORT_EXT_NAMES = [
                '.jpg',
                '.bmp',
                '.png',
                '.gif'
            ]
            self.EXT_2_FILE_TYPE = {
                '.jpg': 'img',
                '.png': 'img',
                '.bmp': 'img',
                '.gif': 'img',
                '.txt': 'txt'
            }
            self.file_path = ''
            self.file_name = ''
            self.file_ext_name = ''
            self.file_ext_type = ''
            self.img_var = None
            self.img_file = None
            self.file_loaded = False
            self.img_size = (400, 400)

        def __is_file_supported__(self):
            return self.file_ext_name.lower() in self.SUPPORT_EXT_NAMES

        def sel_file(self, file_path):
            if not isinstance(file_path, str):
                raise Exception('File path should be an str')
            if not os.path.isfile(file_path):
                raise Exception('Not a file!')
            self.file_path = file_path
            self.file_name = os.path.split(file_path)[1]
            self.file_ext_name = os.path.splitext(self.file_name)[1].lower()
            if not self.__is_file_supported__():
                print('File type unsupported')
                self.clear_file()
                return ''
            self.file_ext_type = self.EXT_2_FILE_TYPE[self.file_ext_name]

            self.file_loaded = True

            if self.file_ext_type is 'img':
                self.img_file = Image.open(self.file_path)
                (x, y) = self.img_file.size
                if x > self.img_size[0]:
                    y = int(max(y * self.img_size[0] / x, 1))
                    x = int(self.img_size[0])
                if y > self.img_size[1]:
                    x = int(max(x * self.img_size[1] / y, 1))
                    y = int(self.img_size[1])
                self.img_var = ImageTk.PhotoImage(self.img_file.resize((x, y)))

            return self.file_ext_type

        def clear_file(self):
            self.file_path = ''
            self.file_name = ''
            self.file_ext_name = ''
            self.file_ext_type = ''
            self.img_var = None
            self.img_file = None
            self.file_loaded = False

        def open_img(self):
            """
            在资源管理器中打开
            """
            # todo 在资源管理器中打开
            print('should open')
            print(self.file_path)

        def req_size(self, size_img_view):
            self.img_size = size_img_view

        def resize_img(self):
            (x, y) = self.img_file.size
            if x > self.img_size[0]:
                y = int(max(y * self.img_size[0] / x, 1))
                x = int(self.img_size[0])
            if y > self.img_size[1]:
                x = int(max(x * self.img_size[1] / y, 1))
                y = int(self.img_size[1])
            self.img_var = ImageTk.PhotoImage(self.img_file.resize((x, y)))

    def display_chosen_file(self):
        # todo 需要新开一个线程去加载图片，在UI线程里干大事是在作死啊
        self.label_file_chosen['text'] = self.chosen_source_file_path
        sel_file_type = self.file_display_manager.sel_file(self.chosen_source_file_path)
        if sel_file_type is 'img':
            if not self.img_view.winfo_viewable():
                self.img_view.pack()
            self.img_view['image'] = self.file_display_manager.img_var
        else:
            print('File:', self.chosen_source_file_path, 'unsupported')
            if self.img_view.winfo_viewable():
                self.img_view.forget()

    def on_btn_copy(self):
        dest_dirs = [
            self.destreader.temp_dir_path + self.destreader.temp_deeper_dir_name + os.sep + self.lv_dirs_dest.get(index)
            for index in self.lv_dirs_dest.curselection()]
        # 判断
        if self.chosen_source_file_path is '' or self.chosen_source_file_path is None:
            print('未选择文件')
            return
        if dest_dirs.__len__() <= 0:
            print('未选择目标文件夹')
            return
        # 把左侧选择到的文件复制到右边选择的文件夹里面，重名的计算哈希，不等就复制并重命名，等就提示并不复制
        for dest_dir in dest_dirs:
            print('\n正在将文件：\t', self.chosen_source_file_path)
            print('复制到：\t\t', dest_dir)
            chosen_file_name = os.path.split(self.chosen_source_file_path)[1]
            # 文件名重复,计算哈希
            # 相同哈希不同文件名的不考虑了……代价小的方法不会整……
            if os.path.exists(dest_dir + os.sep + chosen_file_name):
                if get_file_sha512(self.chosen_source_file_path) == get_file_sha512(
                                        dest_dir + os.sep + chosen_file_name):
                    print('文件重复了，不会被复制')
                    continue
                else:
                    print('出现重名，文件将会被重命名后复制进去')
                    chosen_file_name = \
                        os.path.splitext(chosen_file_name)[0] \
                        + '_%d' % (os.listdir(dest_dir).__len__() + 1) \
                        + os.path.splitext(chosen_file_name)[1]
            shutil.copy(self.chosen_source_file_path, dest_dir + os.sep + chosen_file_name)
            print('复制成功')

        # 然后把右侧的选择清除掉
        self.lv_dirs_dest.selection_clear(0, END)
        # 再在左侧文件列表中选择下一个文件并打印到monitor
        if self.lv_files_source.size() > 0:
            self.lv_files_source.selection_clear(self.chosen_source_file_index)
            self.chosen_source_file_index += 1
            self.chosen_source_file_index %= self.lv_files_source.size()
            self.lv_files_source.selection_set(self.chosen_source_file_index)
            self.on_lv_file_sel()

    def clear_cur_sel_s_file(self):
        self.chosen_source_file_path = ''
        self.chosen_source_file_index = -1
        self.label_file_chosen['text'] = ''
        self.file_display_manager.clear_file()
        self.img_view.forget()

    def on_click_img_view(self, event):
        if self.chosen_source_file_path is not '':
            if self.file_display_manager.file_ext_type is 'img':
                self.file_display_manager.open_img()

    def on_window_resize(self, event):
        winfo = self.img_view_holder.winfo_geometry().split('+')
        size_img_view = tuple(int(item) - 4 for item in winfo[0].split('x'))
        self.file_display_manager.req_size(size_img_view)
        if self.file_display_manager.file_loaded:
            if self.file_display_manager.file_ext_type is 'img':
                self.img_view['width'] = size_img_view[0]
                self.img_view['height'] = size_img_view[1]
                # 以下两行影响性能……会导致缩放的时候卡……
                self.file_display_manager.resize_img()
                self.img_view['image'] = self.file_display_manager.img_var

Dividour()
