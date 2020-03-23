'''
***************
Name:Sunny
Time:2020/3/12
***************
'''
import openpyxl


class ReadExcel(object):
    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name

    def open(self):
        # 创建一个工作簿对象
        self.workbook = openpyxl.load_workbook(self.file_name)
        # 读取工作簿中的表单
        self.sheet = self.workbook[self.sheet_name]

    def read_data(self):
        self.open()
        # 读取表单中每一行的内容
        cases = list(self.sheet.rows)
        # 读取表单的第一行作为字典的键
        title = [title.value for title in cases[0]]
        # 读取除第一行以外的数据作为表单的值
        li = []
        for case_data in cases[1:]:
            value = [case.value for case in case_data]
            # 将数据打包成字典
            case_datas = dict(zip(title, value))
            li.append(case_datas)
        return li

    def write_data(self, row, column, value):
        self.open()
        # 将数据写入表单中
        self.sheet.cell(row=row, column=column, value=value)
        # 保存工作簿
        self.workbook.save(self.file_name)
