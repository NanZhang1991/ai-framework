import time

def calculate(data):
    # print(f"{data} is only test data")
    time.sleep(1)
    dic = {'test_A': [1, 2, 3], 'test_B': ['string0', 'string1', 'string2']}
    return dic 

if __name__ =="__main__":
    abc = [[1,2,3],["string0","string1","string2"]]
    res = calculate('file')
    print(res)

