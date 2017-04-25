import random
import math
import time

class item:
    def __init__(self,min_v,max_v,min_w,max_w,id_num):
        self.max_v = max(max_v,min_v)
        self.min_v = min(max_v,min_v)
        self.max_w = max(max_w,min_w)
        self.min_w = min(max_w,min_w)
        self.exp_v = (max_v + min_v)/2.0
        self.exp_w = (max_w + min_w)/2.0
        self.id_num = id_num

    def expected_return(self,remaining):
        range_w = self.max_w - self.min_w + 1
        allowed_w = remaining - self.min_w + 1
        possible_percent = float(allowed_w)/float(range_w)
        if possible_percent < 0:
            return 0
        else:
            return min(self.exp_v * possible_percent, self.exp_v)

def make_items(n,min_v,max_v,min_w,max_w):
    items = []
    for i in range(n):
        v = random.randint(min_v,max_v)
        V = random.randint(min_v,max_v)
        w = random.randint(min_w,max_w)
        W = random.randint(min_w,max_w)
        items += [item(v,V,w,W,i)]
    return items

def item_recomender(items,weight):
    if not items:
        return [0,[]]
    if weight < 0:
        return False
    items = sorted(items, key = lambda item: item.expected_return(weight)/item.exp_w)
    possible_items = []
    for i in range(int(math.ceil(len(items)**.5))):
        item = items[i]
        new_items = items[:]
        new_items.pop(i)
        #tries = [item.min_w,item.max_w]
        tries = []
        if math.floor(item.exp_w)  != math.ceil(item.exp_w):
            tries += [math.floor(item.exp_w),math.ceil(item.exp_w)]
        else:
            tries += [item.exp_w]
        item_gain = 0
        for attempt in tries:
            attempt_value = item_recomender(new_items,weight-attempt)
            if attempt_value != False:
                item_gain += attempt_value[0]
        possible_items += [((item_gain+item.exp_v)/len(tries),item.id_num)]
    return max(possible_items)

items = make_items(100,1,10,1,10)
time_start = time.time()
print(item_recomender(items,1000000))
time_end = time.time()
print(time_end - time_start)
