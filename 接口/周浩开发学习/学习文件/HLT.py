#def move(n, a, b, c):
#    if n == 1:
#        print(a, '-->', c)
#    else:
#        move(n-1, a, c, b) #把n-1个盘子从 a 移动到 b
#        move(1, a, b ,c)#把1个盘子从 a 移动到 c
#        move(n-1, b, c, a)#把n-1个盘子从 b 移动到 a
                          #一直循环到n==1
#move(3, 'A', 'B', 'C')
def triangles():
    L = [1]
    yield L
    while True:
        L = [1] + [L[x] + L[x + 1] for x in range(len(L) - 1)] + [1]
        yield L
n = 0
for L in triangles():
    print(L)
    n = n + 1
    if n == 10:
        break

# 首先获得Iterator对象:
it = iter([1, 2, 3, 4, 5])
# 循环:
while True:
    try:
        # 获得下一个值:
        x = next(it)
    except StopIteration:
        # 遇到StopIteration就退出循环
        break
