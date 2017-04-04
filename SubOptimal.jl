
#I don't know how the data will be structured, so I am going to format all item data as follows:

#There should only be two inputs into the function, items and their traits, and then the size of knapsack.

#Each item has four interesting pieces of info, a max and min size and value.

#The list "items" that will appear often is going to be a list of item object, that I will write first. It will contain all the needed info

#I am going to implement two algorithms in this document, one should be reasonably fast, and the other a nightmare but more accurate.

type item
    max_size::Real
    min_size::Real
    
    max_value::Real
    min_value::Real
    
    expected_value::Real
    expected_size::Real
end

type real_item
    size::Real
    value::Real
end

function new_item(min_size,max_size,min_value,max_value)
    new_item = item(max_size,min_size,max_value,min_value,(max_value+min_value)/2,(max_size+min_size)/2)
    return new_item
end

function ponder_size(items::Array,remaining_space)
    #Ponder size is a function for getting the expected addition of an item to the knapsack
    #If an item is guarenteed to fix, the expected value will simply be the expected value of the item
    #However, if an item has a possibility of not fitting, we set the gain to the knapsack to 0
    #For instance, an item A has size range of (1,6) and value range of (2, 6)
    # ponder_size([A],6)
    # returns: [4]
    # or 
    # ponder_size([A],3)
    # returns: [2]
    # Since we can expect to gain 4 50% of the time, and gain 0 50% of the time.
    #
    # This function is what allows the entire algorithm to work.    
    result = zeros(length(items))
    if remaining_space == 0
        return result
    end
    for item_num in 1:length(items)
        sel_item = items[item_num]
        if sel_item.min_size > remaining_space
            result[item_num] = 0 
        else
            max_size_diff = maximum([sel_item.max_size - remaining_space 0])
            if max_size_diff != 0
                biggest_allowable_size = remaining_space
            else
                biggest_allowable_size = sel_item.max_size
            end
            expected_value = (sel_item.expected_value * (biggest_allowable_size - sel_item.min_size+1))/(sel_item.max_size - sel_item.min_size+1)    
            result[item_num] = expected_value
        end
    end
    return(result)
end

#What are some terms we can score to train on?
#Variance of size, variance of value, expected gain, and max size strike me as important, so lets start with those.


function order_rank(items::Array,lambdas::Array,remaining_space::Int64)
    #This function is currently not being used; only keeping it just in case
    results = zeros(length(items))
    expected_values = ponder_size(items,remaining_space)
    for item_num in 1:length(items)
        sel_item = items[item_num]
        size_var = ((sel_item.max_size - sel_item.min_size + 1)^2 - 1)/12
        val_var = ((sel_item.max_value - sel_item.min_value + 1)^2 - 1)/12
        expected_gain = expected_values[item_num] / ((sel_item.max_size - sel_item.min_size)/2)
        max_size = sel_item.max_size
        results[item_num] = lambdas[1] * size_var + lambdas[2] * val_var + lambdas[3]*expected_gain + lambdas[4] * max_size
    end
    return results
end

function max_score(possibilities::Array)
    #Takes in a set of possible packing orders
    #possibilites is a list of items that look like [[A,B],10,1]
    #The first item is a list of items
    #The second is the total score we expect by taking that path
    #The last number is the remaining space by taking that path
    #Returns the one with the best score
    best = [[],0,0]
    for i in possibilities
        if i[2] > best[2]
            best = i
        end
    end
    return best
end

function expected_knapsack(items::Array, space)
    #Items is a list of item objects that have 4 invariant properties; max size, min size, max value, min value
    #space is obviously the amount of size the knapsack can hold
    #Returns an ordered list with the objects we selected, and a number that was our final score.
    #BECAUSE push!() IS THE BEST METHOD I COULD THINK OF, AND I USED DYNAMIC PROGRAMMING, THE LIST IS BACKWARDs
    #please read that part. The first item that needs to be added is the LAST item in the final output list
    #The first item in the list is the last item to be added. 
    if space <= 0
        return [[],0,space]
    end
    expected_sizes = ponder_size(items, space)
    possibilities = Vector(length(items))
    found = false
    for item_num in 1:length(items)
        new_space = space - items[item_num].expected_size
        possibilities[item_num] = expected_knapsack(items, new_space)
        possibilities[item_num][2] += expected_sizes[item_num]
        push!(possibilities[item_num][1], item_num)
        found = true  
    end
    best_path = max_score(possibilities)
    return best_path
end    

function get_item(item::item)
    #Gets me a real item
    value = rand(item.min_value:item.max_value)
    size = rand(item.min_size:item.max_size)
    return real_item(size,value)
end

function stochastic_knapsack(items::Array, space::Real, added_items::Array = [], value::Real = 0)
    #Final algorithm
    #Takes items same as before, and a space, and a current value in the pack.
    #Should run in time nW^2, where W is the total initial space and n is the number of objects.
    #computes the path with best expected value, and then actually takes the item
    #Revalutes after that, and then takes comutes path with best expected value
    #Goes until either expected gain is 0 or we over-fill the bag.
    #return the value
    best_path = expected_knapsack(items, space)
    if best_path[2] <= 0
        return [added_items,value]
    end
    next_item = best_path[1][length(best_path[1])]
    actual_item::real_item = get_item(items[next_item])
    new_space = space - actual_item.size
    if new_space < 0
        return [added_items,value]
    end
    value += actual_item.value
    push!(added_items, next_item)
    return stochastic_knapsack(items,new_space,added_items,value)
end

item_1 = new_item(2,4,5,5)
item_2 = new_item(1,1,1,1)
stochastic_knapsack([item_1,item_2],10)


