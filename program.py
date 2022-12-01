import difflib


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

