'''
def compare_clocks(clock_A, clock_B):
        if clock_A == clock_B:
            return "equal"
        
        less_than = True
        greater_than = True
        
        for i in range(len(clock_A)):
            if clock_A[i] > clock_B[i]:
                less_than = False
            elif clock_A[i] < clock_B[i]:
                greater_than = False
        
        if less_than and not greater_than:
            return "less"
        elif greater_than and not less_than:
            return "greater"
        else:
            return "not comparable"


print(compare_clocks([2,2,2], [2,2,1]))


li = [[2,2,2], [2,2,1]]

sorted(li)
print(li)

def compare_clocks(clock_A, clock_B):
    for i in range(len(clock_A)):
        if clock_A[i] < clock_B[i]:
            return -1
        elif clock_A[i] > clock_B[i]:
            return 1
    return 0

def sort_clocks(clock_list):
    return sorted(clock_list, key=compare_clocks)


clocks = [[1, 0, 2], [2, 1, 0], [0, 1, 2], [1, 1, 1]]

sorted_clocks = sort_clocks(clocks)
print(sorted_clocks)
'''

clocks = [{"clock":[1, 2, 3]},{ "clock":[2, 1, 4]}, { "clock":[0, 3, 1]}, {"clock":[1, 2, 2]} ]

sorted_clocks = sorted(clocks,key=lambda x :x["clock"])

print(sorted_clocks)
