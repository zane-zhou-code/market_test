'''
画一个红色正方形
import turtle
turtle.pensize(4)
turtle.pencolor('red')
turtle.forward(100)
turtle.right(90)
turtle.forward(100)
turtle.right(90)
turtle.forward(100)
turtle.right(90)
turtle.forward(100)
turtle.mainloop()

a = int(input('a = '))
b = int(input('b = '))
print('%d + %d = %d' % (a, b, a + b))
print('%d - %d = %d' % (a, b, a - b))
print('%d * %d = %d' % (a, b, a * b))
print('%d / %d = %f' % (a, b, a / b))
print('%d // %d = %d' % (a, b, a // b))
print('%d %% %d = %d' % (a, b, a % b))
print('%d ** %d = %d' % (a, b, a ** b))
'''
'''
a = 100
b = 12.345
c = 1 + 5j
d = 'hello, world'
e = True
print(type(a))
print(type(b))
print(type(c))
print(type(d))
print(type(e))
'''
'''
a = 5
b = 10
c = 3
d = 4
e = 5
a += b# 15
a -= c# 12
a *= d# 48
a /= e
print("a = ", a)
'''
'''
flag1 = 3 > 2
flag2 = 2 < 1
flag3 = flag1 and flag2
flag4 = flag1 or flag2
flag5 = not flag1
print("flag1 = ", flag1)
print("flag2 = ", flag2)
print("flag3 = ", flag3)
print("flag4 = ", flag4)
print("flag5 = ", flag5)
print(flag1 is True)
print(flag2 is not False)
'''
'''
f = float(input('请输入华氏温度:'))
c = (f-32)/1.8
print('%.1f华氏度 = %.1f摄氏度' % (f,c))'''
'''
import  math
radius = float(input('请输入圆的半径:'))
perimeter = 2 * math.pi *radius
area = math.pi * radius * radius
print('周长：%.2f'% perimeter)
print('面积：%.2f'% area)'''
'''
year = int(input('请输入年份:'))
is_leap = (year % 4 == 0 and year % 100 != 0 or
           year % 400 == 0)
print(is_leap)'''
'''
import getpass
username = input('请输入用户名：')
# password = input('请输入口令：')
password = getpass.getpass('请输入口令：')
if username == 'admin' and password == '123456':
    print('身份验证成功！')
else:
    print('身份验证失败！')'''
'''
x = float(input('x = '))
if x>1:
    y=3*x-5
elif x>=-1:
    y=x+2
else:
    y=5*x+3
print('f(%.2f)=%.2f'%(x,y))'''
'''
value = float(input('请输入长度：'))
unit =  input('请输入单位：')
if unit  =='in'or unit=='英寸':
    print('%f英寸=%f厘米'%(value,value*2.54))
elif unit=='cm'or unit=='厘米':
    print('%f厘米=%f英寸'%(value,value/2.54))
else:
    print('请输入有效的单位')'''
'''
# 使用了random模块的randint函数生成指定范围的随机数来模拟掷骰子
from random import randint
face = randint(1,6)
if face ==1:
    result = '唱个歌'
elif face ==2:
    result = '跳个舞'
elif face ==3:
    result = '学狗叫'
elif face ==4:
    result = '做俯卧撑'
elif face ==5:
    result = '念绕口令'
else:
    result = '讲冷笑话'
print(result)'''
'''
score = float(input('请输入成绩：'))
if score>=90:
    grade = 'A'
elif score>=80:
    grade='B'
elif score>=70:
    grade='C'
elif score>=60:
    grade='D'
else:
    grade='E'
print('对应的等级是：',grade)'''
'''
import  math
a=float(input('a='))
b=float(input('b='))
c=float(input('c='))
if a+b>c and a+c>b and b+c>a:
    print('周长：%.0f'%(a+b+c))
    p=(a+b+c)/2
    area=math.sqrt(p*(p-a)*(p-b)*(p-c))
    print('面积：%.0f'%(area))
else:
    print('不能构成三角形')'''
'''
salary = float(input('本月收入：'))
insurance = float(input('五险一金：'))
diff = salary-insurance-3500
if diff<=0:
    rate=0
    deduction=0
elif diff<1500:
    rate=0.03
    deduction=0
elif diff<4500:
    rate=0.1
    deduction=105
elif diff<9000:
    rate=0.2
    deduction=555
elif diff<35000:
    rate=0.25
    deduction=1005
elif diff<55000:
    rate=0.3
    deduction=2755
elif diff<8000:
    rate=0.35
    deduction=5505
else:
    rate=0.45
    deduction=13505
tax=abs(diff*rate-deduction)
print('个人所得税：%.2f元'%tax)
print('实际到手收入：%.2f元'%(diff+3500-tax))'''
'''
import  random
answer=random.randint(1,100)
counter=0
while True:
    counter+=1
    number=int(input('请输入：'))
    if number<answer:
        print('大一点')
    elif number>answer:
        print('小一点')
    else:
        print('恭喜你猜对了！')
        break
print('你总共猜对了%d次'%counter)
if counter>7:
    print('你的智商余额明显不足')'''
'''
for i in range(1,10):
    for j in range(1,i+1):
        print('%d*%d=%d'%(i,j,i*j),end='\t')
    print()'''
'''
from math import sqrt
num=int(input('请输入一个正整数：'))
end=int(sqrt(num))
is_prime=True
for x in range(2,end+1):
    if num%x ==0:
        is_prime=False
        break
if is_prime and num!=1:
    print('%d是素数'%num)
else:
    print('%d不是素数'%num)'''
'''
x=int(input('x='))
y=int(input('y='))
if x>y:
    x,y=y,x
for factor in range(x,0,-1):
    if x%factor ==0 and y%factor==0:
        print('%d和%d的最大公约数是%d'%(x,y,factor))
        print('%d和%d的最小公倍数是%d'%(x,y,x*y//factor))
        break'''
'''
row=int(input('请输入行数：'))
for i in range(row):
    for _ in range(i+1):
        print('*',end='')
    print()

for i in range(row):
    for j in range(row):
        if j<row-i-1:
            print(' ',end='')
        else:
            print('*',end='')
    print()

for i in range(row):
    for _ in range(row-i-1):
        print(' ',end='')
    for _ in range(2*i+1):
        print('*',end='')
    print()'''
'''
for x in range(0,20):
    for y in range(0,33):
        z=100-x-y
        if 5*x+3*y+z/3==100:
            print('公鸡：%d只，母鸡：%d只，小鸡：%d只'%(x,y,z))# 百钱百鸡
'''
'''
a=0
b=1
for _ in range(20):
    a,b=b,a+b
    print(a,end='')'''
'''
for num in range(100,1000):
    low=num%10
    mid=num//10%10
    high=num//100
    if num==low**3+mid**3+high**3:
        print(num)
        print(low,mid,high)# 水仙花数
'''
'''
num=int(input('请输入一个正整数:'))
temp=num
num2=0
while temp>0:
    num2*=10
    num2+=temp%10
    temp//=10
if num==num2:
    print('%d是回文数'%num)
else:
    print('%d不是回文数'%num)
'''
'''
import time
import math
for num in range(1,10000):
    sum=0
    for factor in range(1,int(math.sqrt(num))+1):
        if num%factor==0:
            sum+=factor
            if factor>1 and num/factor!=factor:
                sum+=num/factor
    if sum==num:
        print(num)'''
'''# math中已经有此内置函数
def factorial(num):
    result=1
    for n in range(1,num+1):
        result*=n
    return result
m=int(input('m='))
n=int(input('n='))
print(factorial(m)//factorial(n)//factorial(m-n))'''
'''
from random import  randint
def roll_dice(n=2):
    total=0
    for _ in range(n):
        total+=randint(1,6)
        return total
def add(a=0,b=0,c=0):
    return a+b+c
print(roll_dice())
print(roll_dice(3))
print(add())
print(add(1))
print(add(1,2))
print(add(1,2,3))
print(add(c=50,a=100,b=200))'''
'''
def add(*args):
    total=0
    for val in args:
        total+=val
    return total
print(add())
print(add(1))
print(add(1, 2))
print(add(1, 2, 3))
print(add(1, 3, 5, 7, 9))'''
'''
def foo():
    pass
def bar():
    pass
# __name__是Python中一个隐含的变量它代表了模块的名字
# 只有被Python解释器直接执行的模块的名字才是__main__
if __name__ == '__main__':
    print('call foo()')
    foo()
    print('call bar()')
    bar()'''
'''
def gcd(x, y):
    (x, y) = (y, x) if x > y else (x, y)
    for factor in range(x, 0, -1):
        if x % factor == 0 and y % factor == 0:
            return factor
def lcm(x, y):
    return x * y // gcd(x, y)
def is_palindrome(num):
    temp = num
    total = 0
    while temp > 0:
        total = total * 10 + temp % 10
        temp //= 10
    return total == num    
def is_prime(num):
    for factor in range(2, num):
        if num % factor == 0:
            return False
    return True if num != 1 else False
if __name__ == '__main__':
    num = int(input('请输入正整数: '))
    if is_palindrome(num) and is_prime(num):
        print('%d是回文素数' % num)
'''

