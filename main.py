import os.path
import sys
from input import Input
from output import Output
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from program import Progpair
from equality import Equality
from collections import deque
import ui

os.putenv("QTWEBENGINE_CHROMIUM_FLAGS", "--no-sandbox")


class ConfirmTool(QMainWindow, ui.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ConfirmTool, self).__init__(parent)
        self.setupUi(self)
        self.eq_list = []
        self.neq_list = []
        self.worklist: deque = None
        self.eq_pairs = []
        self.neq_pairs = []
        self.human_verified_pairs = []
        self.doubt_pairs = []
        self.current_pair: Progpair = None
        self.load_path = os.path.join(os.getcwd())
        self.export_path = os.path.join(os.getcwd())
        self.eq_button.clicked.connect(lambda: self.press(Equality.HUMAN_VERIFIED))
        self.neq_button.clicked.connect(lambda: self.press(Equality.NOT_EQUAL))
        self.notsure_button.clicked.connect(lambda: self.press(Equality.DOUBT))
        self.actionImport_from.triggered.connect(lambda: self.load(self.load_path))
        self.actionExport_to.triggered.connect(lambda: self.export(self.export_path))
        self.waiting_listview.itemClicked.connect(self.item_click_judged)
        self.nequal_listview.itemClicked.connect(self.item_click_neq)
        self.equal_listview.itemClicked.connect(self.item_click_verified)
        self.nsure_listview.itemClicked.connect(self.item_click_doubt)
        self.item_map = {}

    def item_click_judged(self):
        item = self.waiting_listview.selectedItems()[0]
        clicked_pair = self.item_map[item.text()]
        if self.current_pair is not None and self.current_pair is not clicked_pair:
            self.worklist.appendleft(self.current_pair)
            self.current_pair = clicked_pair
        self.display()

    def item_click_neq(self):
        item = self.nequal_listview.selectedItems()[0]
        clicked_pair = self.item_map[item.text()]
        if self.current_pair is not None and self.current_pair is not clicked_pair:
            self.worklist.appendleft(self.current_pair)
        self.current_pair = clicked_pair
        self.display()

    def item_click_verified(self):
        item = self.equal_listview.selectedItems()[0]
        clicked_pair = self.item_map[item.text()]
        if self.current_pair is not None and self.current_pair is not clicked_pair:
            self.worklist.appendleft(self.current_pair)
            self.current_pair = clicked_pair
        self.display()

    def item_click_doubt(self):
        item = self.nsure_listview.selectedItems()[0]
        clicked_pair = self.item_map[item.text()]
        if self.current_pair is not None and self.current_pair is not clicked_pair:
            self.worklist.appendleft(self.current_pair)
            self.current_pair = clicked_pair
        self.display()

    def get_next(self):
        if len(self.worklist) > 0:
            self.current_pair = self.worklist.popleft()
            self.display()
        widget2list = [
            [self.equal_listview, self.human_verified_pairs],
            [self.nequal_listview, self.neq_pairs],
            [self.waiting_listview, self.eq_pairs],
            [self.nsure_listview, self.doubt_pairs]
        ]
        self.item_map = {}
        for widget, pair_list in widget2list:
            widget.clear()
            for pair in pair_list:
                item_str = pair.prog1 + "," + pair.prog2
                item = QListWidgetItem(pair.prog1 + "," + pair.prog2)
                self.item_map[item_str] = pair
                widget.addItem(item)

    def press(self, equality: Equality):
        if self.current_pair is not None:
            self.current_pair.eq = equality
            for pairlist in [self.eq_pairs, self.neq_pairs, self.human_verified_pairs, self.doubt_pairs]:
                if self.current_pair in pairlist:
                    pairlist.remove(self.current_pair)

            if equality == Equality.HUMAN_VERIFIED:
                self.human_verified_pairs.append(self.current_pair)
            elif equality == Equality.NOT_EQUAL:
                self.neq_pairs.append(self.current_pair)
            elif equality == Equality.DOUBT:
                self.doubt_pairs.append(self.current_pair)
            self.get_next()

    def display(self):
        if self.current_pair is not None:
            diff = self.current_pair.diff()
            self.prog1_text.setText(self.current_pair.prog1)
            self.prog2_text.setText(self.current_pair.prog2)
            self.diff_render.setHtml(diff)
            if self.current_pair.eq == Equality.EQUAL_M:
                self.pair_category.setText("Machine Judged Equal")
            elif self.current_pair.eq == Equality.NOT_EQUAL:
                self.pair_category.setText("Not Equal")
            elif self.current_pair.eq == Equality.HUMAN_VERIFIED:
                self.pair_category.setText("Human Verified Equal")
            elif self.current_pair.eq == Equality.DOUBT:
                self.pair_category.setText("Doubt")


    def load(self, fname):
        eq_name = os.path.join(fname, 'input/equal.csv')
        neq_name = os.path.join(fname, 'input/inequal.csv')
        self.eq_list = Input.read(eq_name)
        self.neq_list = Input.read(neq_name)
        self.item_map = {}
        self.eq_pairs = [Progpair(pair[0], pair[1], Equality.EQUAL_M) for pair in self.eq_list]
        self.neq_pairs = [Progpair(pair[0], pair[1], Equality.NOT_EQUAL) for pair in self.neq_list]
        self.human_verified_pairs = []
        self.doubt_pairs = []
        self.worklist = deque(self.eq_pairs)
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
