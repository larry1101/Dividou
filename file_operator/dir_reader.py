import os
import winreg


class Direader:
    def __init__(self):
        self.PARTITIONS = [item + ':' for item in self.__get_partition_names__()]
        # self.home()
        self.temp_dir_path = ''
        self.temp_dir_name = ''
        self.dirs = self.PARTITIONS.copy()
        self.files = []
        self.files_ext_names = []
        self.deeper_dirs = []
        self.temp_deeper_dir_name = ''
        self.temp_deeper_dir_path = ''

    def is_at_home(self):
        if self.temp_dir_path is '':
            return True
        else:
            return False

    def get_tmp_path(self, full=True):
        if full:
            if self.temp_dir_path == '': return '/'
            return self.temp_dir_path
        else:
            if self.temp_dir_name == '': return '/'
            return self.temp_dir_name

    def __get_partition_names__(self):
        res = []
        deviceID = ''
        subKey = 'SYSTEM\MountedDevices'
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subKey)
        i = 0
        try:
            while True:
                name, value, type = winreg.EnumValue(key, i)
                if name.startswith('\\DosDevices\\'):
                    res.append((name, repr(value)[0:16]))
                    if name.startswith('\\DosDevices\\C'):
                        deviceID = repr(value)[0:16]
                i += 1
        except WindowsError:
            pass
        res = filter(lambda item: item[1] == deviceID, res)
        res = list(zip(*res))[0]
        index = res[0].rindex('\\')
        res = sorted([item[index + 1:-1] for item in res])
        return res

    def enter_dir(self, dir_index):
        self.temp_dir_name = self.dirs[dir_index]
        self.temp_dir_path = self.temp_dir_path + self.temp_dir_name + os.sep
        self.dirs = list(filter(lambda item: os.path.isdir(self.temp_dir_path + os.sep + item),
                                os.listdir(self.temp_dir_path)))
        self.files = list(filter(lambda item: os.path.isfile(self.temp_dir_path + os.sep + item),
                                 os.listdir(self.temp_dir_path)))
        self.files_ext_names.clear()
        for file in self.files:
            index = file.rfind('.')
            ext_name = 'no ext name'
            if index >= 0:
                ext_name = file[index:]
            if ext_name not in self.files_ext_names:
                self.files_ext_names.append(ext_name)

        self.deeper_dirs.clear()
        self.temp_deeper_dir_name = ''
        self.temp_deeper_dir_path = ''

    def home(self):
        self.temp_dir_name = ''
        self.temp_dir_path = ''
        self.dirs = self.PARTITIONS.copy()
        self.files.clear()
        self.files_ext_names.clear()
        self.deeper_dirs.clear()
        self.temp_deeper_dir_name = ''
        self.temp_deeper_dir_path = ''

    def get_deeper(self, dir_index):
        self.temp_deeper_dir_name = self.dirs[dir_index]
        self.temp_deeper_dir_path = self.temp_dir_path + self.temp_deeper_dir_name + os.sep
        self.deeper_dirs = list(
            filter(lambda item: os.path.isdir(self.temp_deeper_dir_path + item),
                   os.listdir(self.temp_deeper_dir_path)
                   )
        )

    def go_to(self, dir_path):
        if not os.path.exists(dir_path):
            raise Exception('path not exist')
        if not isinstance(dir_path, str):
            raise Exception('dir path should be str')
        # dir_path has a '\' at the last
        self.temp_dir_path = dir_path
        self.temp_dir_name = dir_path[dir_path.rfind(os.sep, 0, -1) + 1:-1]
        self.dirs = list(filter(lambda item: os.path.isdir(self.temp_dir_path + os.sep + item),
                                os.listdir(self.temp_dir_path)))
        self.files = list(filter(lambda item: os.path.isfile(self.temp_dir_path + os.sep + item),
                                 os.listdir(self.temp_dir_path)))
        self.files_ext_names.clear()
        for file in self.files:
            index = file.rfind('.')
            ext_name = 'no ext name'
            if index >= 0:
                ext_name = file[index:]
            if ext_name not in self.files_ext_names:
                self.files_ext_names.append(ext_name)
        self.deeper_dirs.clear()
        self.temp_deeper_dir_name = ''
        self.temp_deeper_dir_path = ''

    def back(self):
        if self.temp_dir_path == '':
            print('Already at home')
        # elif self.temp_dir_path in self.PARTITIONS:
        #     self.home()
        else:
            parent_dir = self.temp_dir_path[:self.temp_dir_path.rfind(os.sep, 0, -1) + 1]
            if parent_dir == '':
                self.home()
            else:
                self.go_to(parent_dir)

    def refresh_deeper(self):
        self.deeper_dirs.clear()
        self.deeper_dirs = list(
            filter(lambda item: os.path.isdir(self.temp_deeper_dir_path + item),
                   os.listdir(self.temp_deeper_dir_path)
                   )
        )
