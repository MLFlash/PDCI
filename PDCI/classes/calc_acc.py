'''
Created on 08-Oct-2019

@author: akash
'''


class calc_acc:
    def __init__(self):
        pass

    def accuracy(self, pre, gold):
        count = 0
        for pt in pre:
            if pt in gold:
                count += 1
        return float(count) / len(gold)
