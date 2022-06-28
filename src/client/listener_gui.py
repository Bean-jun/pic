import datetime
import os
import sys
import time

import xerox
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
                             QTextBrowser, QVBoxLayout, QWidget)

import tools


class Task(QThread):

    task_signal = pyqtSignal(int, bool)

    def __init__(self, widget):
        super().__init__()
        self.widgit = widget

    def run(self):
        while True:
            time.sleep(1)

    def _handle(self):
        path = self.widgit.gen_img_file_path()
        img_path = self.widgit.tools.saveImageGrab(path)
        if not img_path:
            self.widgit.show_message("剪贴板内容非图片")
            return

        status, filename_or_msg = self.widgit.tools.check_file_allow(img_path)
        if not status:
            self.widgit.show_message(filename_or_msg)
            return

        data = self.widgit.tools.read_file(img_path)
        filename = self.widgit.tools.clean_filename(filename_or_msg)
        response = self.widgit.tools.Request(
            "POST", self.widgit.line_edit.text(), files={filename: data})
        response_txt = self.widgit.tools.parse_response(response)

        if self.widgit.link_flag is False:
            xerox.copy(response_txt)
        else:
            xerox.copy("![%s](%s)" % (filename, response_txt))
        self.widgit.show_message("设置剪贴板成功\n%s" % response_txt)

    def handle(self, sleep=2, run_forever=False):
        if not run_forever:
            self._handle()
            return

        # while True:
        #     self._handle()
        #     time.sleep(sleep)


class MainWindow(QWidget):

    def __init__(self, tools=None):
        super().__init__()
        self.tools = tools
        self.workspace = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.temp_file = os.path.join(self.workspace, "temp")
        self.tools.mkdir(self.temp_file)
        self.init_ui()
        self.init_signal()
        # return http://xxxxx/xxx if link is y else ![](http://xxxxx/xxx)
        self.start_flag = False
        self.link_flag = False

    def gen_img_file_path(self):
        img_path = "img-%s.png" % self.tools.datetime_add_time(
            self.tools.format_datetime(
                datetime.datetime.now(),
                format="%Y%m%d%H%M%S"),
            self.tools.format_time(time.time()))
        return os.path.join(self.temp_file, img_path)

    def init_ui(self):

        self.setWindowIcon(QIcon("./images/pic.ico"))
        self.setWindowTitle("pic")

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("请输入服务器地址")
        self.btn_connect = QPushButton("点击连接", self)
        self.btn_out_mode = QPushButton("直接地址", self)
        self.btn_out_mode.setHidden(True)
        self.btn_once = QPushButton("运行一次", self)
        # self.btn_more = QPushButton("一直执行", self)
        self.btn_clean = QPushButton("清理窗口", self)
        self.btn_exit = QPushButton("退出", self)
        self.brower = QTextBrowser(self)

        # 定义布局
        self.h_layout_1 = QHBoxLayout()
        self.v_layout_1 = QVBoxLayout()
        self.h_layout_2 = QHBoxLayout()

        self.h_layout_1.addWidget(self.brower)
        self.v_layout_1.addWidget(self.line_edit)

        self.h_layout_2.addWidget(self.btn_connect)
        self.h_layout_2.addWidget(self.btn_out_mode)
        self.v_layout_1.addLayout(self.h_layout_2)

        self.v_layout_1.addWidget(self.btn_once)
        # self.v_layout_1.addWidget(self.btn_more)
        self.v_layout_1.addWidget(self.btn_clean)
        self.v_layout_1.addWidget(self.btn_exit)

        # 设置主布局
        self.h_layout_1.addLayout(self.v_layout_1)
        self.setLayout(self.h_layout_1)

    def init_signal(self):
        self.btn_connect.clicked.connect(self.btn_connect_signal)
        self.btn_out_mode.clicked.connect(self.btn_out_mode_signal)
        self.btn_once.clicked.connect(self.btn_one_signal)
        # self.btn_more.clicked.connect(self.btn_more_signal)
        self.btn_clean.clicked.connect(self.btn_clean_signal)
        self.btn_exit.clicked.connect(self.btn_exit_signal)

    def show_message(self, msg):
        date = self.tools.format_datetime(datetime.datetime.now())
        message = "%s:\n%s\n%s" % (date, msg, self.brower.toPlainText())
        self.brower.setText(message)

    def check_line_edit(self):
        text = self.line_edit.text()
        text = text.strip(" ")
        if not text:
            self.show_message("输入框内容为空!")
            return False, ""

        status, _ = self.tools.check_url(text)
        if not status:
            self.show_message("请设置有效的网络地址!")
            return False, ""

        status = self.tools.Ping("POST",
                                 text,
                                 files={"pic.ico": b""})
        if not status:
            self.show_message("该地址无法ping通")
            return False, ""

        self.line_edit.setText = text
        return True, text

    def btn_connect_signal(self, *args, **kwargs):
        status, _ = self.check_line_edit()
        if not status:
            return

        self.show_message("连接服务器成功...")

        # 禁用按键&输入框
        self.btn_connect.setDisabled(True)
        self.line_edit.setDisabled(True)

        # 开启后续执行模块
        self.start_flag = True
        self.btn_out_mode.setHidden(False)

        # 开启信号订阅
        self.handle_thread = Task(self)
        self.handle_thread.start()
        self.handle_thread.task_signal.connect(self.handle_thread.handle)

    def btn_out_mode_signal(self, *args, **kwargs):
        self.link_flag = not self.link_flag
        if self.link_flag is False:
            self.btn_out_mode.setText("直接地址")
        else:
            self.btn_out_mode.setText("Markdown地址")

    def btn_one_signal(self, *args, **kwargs):
        if self.start_flag:
            # self.handle()
            self.handle_thread.task_signal.emit(0, False)
        else:
            self.show_message("请设置server地址!")

    # def btn_more_signal(self, *args, **kwargs):
    #     if self.start_flag:
    #         # TODO:支持多线程执行
    #         self.handle()
    #         self.handle_thread.task_signal.emit(2, True)
    #     else:
    #         self.show_message("请设置server地址!")

    def btn_clean_signal(self, *args, **kwargs):
        self.brower.clear()

    def btn_exit_signal(self, *args, **kwargs):
        sys.exit(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(tools)
    window.show()
    sys.exit(app.exec())
