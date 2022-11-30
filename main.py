import os.path
import sys
from input import Input
from output import Output
# from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from program import Progpair
from equality import Equality
from queue import Queue
import ui

os.putenv("QTWEBENGINE_CHROMIUM_FLAGS", "--no-sandbox")

class ConfirmTool(QMainWindow, ui.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ConfirmTool, self).__init__(parent)
        self.setupUi(self)
        self.eq_list = []
        self.neq_list = []
        self.eq_pairs = []
        self.worklist: Queue = Queue()
        self.human_verified = []
        self.doubt = []
        self.current_pair: Progpair = None
        self.load_path = os.path.join(os.getcwd())
        self.export_path = os.path.join(os.getcwd())
        self.eq_button.clicked.connect(lambda: self.press(Equality.HUMAN_VERIFIED))
        self.neq_button.clicked.connect(lambda: self.press(Equality.NOT_EQUAL))
        self.notsure_button.clicked.connect(lambda: self.press(Equality.DOUBT))
        self.actionImport_from.triggered.connect(lambda: self.load(self.load_path))
        self.actionExport_to.triggered.connect(lambda: self.export(self.export_path))

    def get_next(self):
        if not self.worklist.empty():
            self.current_pair = self.worklist.get()
            self.show_diff(self.current_pair)

    def press(self, equality: Equality):
        if not self.current_pair is None:
            self.current_pair.eq = equality
            if equality == Equality.HUMAN_VERIFIED:
                self.human_verified.append(self.current_pair)
            elif equality == Equality.NOT_EQUAL:
                self.neq_list.append(self.current_pair)
            elif equality == Equality.DOUBT:
                self.doubt.append(self.current_pair)
            self.get_next()

    def show_diff(self, progpair):
        diff = progpair.diff()
        self.diff_render.setHtml(diff)

    def load(self, fname):
        eq_name = os.path.join(fname, 'input/equal.csv')
        neq_name = os.path.join(fname, 'input/inequal.csv')
        self.eq_list = Input.read(eq_name)
        self.neq_list = Input.read(neq_name)
        self.eq_pairs = [Progpair(pair[0], pair[1], Equality.EQUAL_M) for pair in self.eq_list]
        for pair in self.eq_pairs:
            self.worklist.put(pair)
        self.get_next()

    def export(self, fname):
        # eq_name = os.path.join(fname, 'input/equal.csv')
        o = Output(self.human_verified, fname)
        o.write_csv()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tool = ConfirmTool()
    tool.show()
    sys.exit(app.exec_())
