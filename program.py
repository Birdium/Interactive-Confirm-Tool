import os
import subprocess
import difflib


class Program:
    @staticmethod
    def get_bin_dir(src_dir):
        portion = os.path.splitext(src_dir)
        return portion[0] + ".out"

    def get_dir(self):
        return self.__src_name__

    def __init__(self, src_dir):
        self.__src_name__ = src_dir
        self.__src_dir__ = os.path.abspath(src_dir)
        self.__bin_dir__ = self.get_bin_dir(src_dir)
        self.__compiled__ = False

    def __del__(self):
        if self.__compiled__:
            os.remove(self.__bin_dir__)

    def run(self, str_in):
        if not self.__compiled__:
            self.__compiled__ = True
            args = ["g++", self.__src_dir__, "-w", "-o", self.__bin_dir__]
            proc = subprocess.run(args)
        args = [self.__bin_dir__]
        return subprocess.run(args, input=str_in.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class Progpair:
    def __init__(self, prog1, prog2, eq):
        self.prog1 = prog1
        self.prog2 = prog2
        self.eq = eq

    def diff(self):
        with open(self.prog1, 'r', encoding='utf-8') as f1:
            contents1 = f1.read().splitlines(keepends=True)
        with open(self.prog2, 'r', encoding='utf-8') as f2:
            contents2 = f2.read().splitlines(keepends=True)
        d = difflib.HtmlDiff()
        return d.make_file(contents1, contents2)

    def get_eq(self):
        return self.eq

    def set_eq(self, eq):
        self.eq = eq

    def get_list(self):
        return [self.prog1, self.prog2]
