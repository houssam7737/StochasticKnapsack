import random

class item:
    def __init__(self,min_v,max_v,min_w,max_w):
        self.max_v = max(max_v,min_v)
        self.min_v = min(max_v,min_v)
        self.max_w = max(max_w,min_w)
        self.min_w = min(max_w,min_w)
        self.exp_v = (max_v + min_v)/2.0
        self.exp_w = (max_w + min_w)/2.0

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
        items += [item(v,V,w,W)]
    return items

def stoch_knapsack(items,weight):
    if not items:
        return 0
    items = sorted(items, key= lambda item: item.expected_return(weight)/item.exp_w)
    selected = items.pop(0)
    value = selected.exp_v
    used_cost = random.randint(selected.min_w,selected.max_w)
    if used_cost > weight:
        return 0
    else:
        return (value + stoch_knapsack(items,weight-used_cost))

items = make_items(100,1,1000,1,1000)

print(stoch_knapsack(items,10000))
