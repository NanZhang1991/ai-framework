def calculate(**kwargs):
    return kwargs.get('data')

if __name__ =="__main__":
    abc = {'a':2, 'b':3}
    res = calculate(data=abc)
    print(res)

