import random
import time

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

    def get_score(self,remaining,lambdas):
        expected_return = self.expected_return(remaining)
        max_w = self.max_w
        min_w = self.min_w
        exp_v = self.exp_v
        exp_w = self.exp_w
        return (lambdas[0]*expected_return/float(exp_w) + lambdas[1]*(1/12.0*(max_w - min_w)**2) + lambdas[2]*(float(exp_v)/float(exp_v)))

def make_items(n,min_v,max_v,min_w,max_w):
    items = []
    for i in range(n):
        v = random.randint(min_v,max_v)
        V = random.randint(min_v,max_v)
        w = random.randint(min_w,max_w)
        W = random.randint(min_w,max_w)
        items += [item(v,V,w,W)]
    return items

def stoch_knapsack(items,weight,lambdas):
    if weight == 0:
        return 0
    if not items:
        return 0

    items = sorted(items, key= lambda item: item.get_score(weight,lambdas))
    selected = items.pop(0)
    value = selected.exp_v
    used_cost = random.randint(selected.min_w,selected.max_w)
    print(value,used_cost)
    if used_cost > weight:
        return 0
    else:
        return (value + stoch_knapsack(items,weight-used_cost,lambdas))
# for r in range(5):
#     random.seed(r)
#     items = make_items(100,1,10,1,10)
#     values = []
#     values_1 = []
#     lambdas = [1,0,0]
#     lambdas_1 = [0,1,0]
#     for t in range(100):
#         a = stoch_knapsack(items[:],100,lambdas)
#         b = stoch_knapsack(items[:],100,lambdas_1)
#         values += [a]
#         values_1 += [b]
#     print("Adjusted ratio: ", sum(values)/float(len(values)), " on seed ", r)
#     print("Pure ratio:     ", sum(values_1)/float(len(values_1)), " on seed ", r)
#     print('\n')

print(stoch_knapsack(items,100000,lambdas))
