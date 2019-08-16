# Question 1
def NumFunc(myList1=[],myList2=[],*args):
    list3  = list(set(myList1).intersection(myList2))
    return list3


myList1 = [1,2,3,4,5,6]
myList2 = [3, 5, 7, 9]
NumFunc(myList1,myList2)
   
