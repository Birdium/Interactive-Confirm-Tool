from input import Input
from output import Output
from program import Progpair
from equality import Equality
from queue import Queue


equal_path = r'equal.csv'
inequal_path = r'inequal.csv'

output_path = 'output'


if __name__ == '__main__':
    eq_list = Input.read(equal_path)
    neq_list = Input.read(inequal_path)
    eq_pairs = [Progpair(pair[0], pair[1], Equality.EQUAL_M) for pair in eq_list]
    worklist = Queue(eq_pairs)
    human_verified, doubt = [], []
    while not worklist.empty():
        pair = worklist.get()
        # judge pair
        if pair.get_eq() == Equality.NOT_EQUAL:
            pass
        elif pair.get_eq() == Equality.HUMAN_VERIFIED:
            human_verified.append(pair)
        elif pair.get_eq() == Equality.DOUBT:
            doubt.append(pair)
    o = Output([pair.get_list() for pair in eq_pairs], output_path)
    o.write_csv()