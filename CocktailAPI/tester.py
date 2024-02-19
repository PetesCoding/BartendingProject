ourlist = [[1, 2, 3, 4], [5, 6, 7, 8]]

def yieldFromTester(list):

    yield from list
    
# for value in yieldFromTester(list):
#     print(value)

for value in yieldFromTester(ourlist):
    print(value)
