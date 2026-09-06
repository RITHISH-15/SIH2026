#swapping two numbers(temporary variable)
'''
a=10
b=20
print('before swap',a)
t=a
a=b
b=a
print('after swap',a)
'''
#2 swaap without temp
'''
a,b=10,20
print('before swap',a,b)
a,b=b,a
print('after swap',a,b)

'''
#3,4 Area of circle /rectangle(l*b)
'''
r=int(input('r value'))
pi=3.14
a=pi*r*r
print('area',a)
'''
#5 perimeter

''''
length=int(input())
breadth=int(input())
side=int(input())
radius=int(input())
pi=3.14
rectangle=2*(length + breadth)
square=4*side
#triangle(3 sides)=a+b+c
circle=2*pi*radius
print("perimeter:",square,rectangle,circle)
'''
'''
#6celsius to farenheit
c=float(input())
f=(c*9/5)+32
print(f)
'''
'''
#7 farenheit to celsius
f=float(input())
c=(f-32)*5/9
print(c)
'''
#8 average of 3 num
'''
def add(n1,n2,n3):
    avg=n1+n2+n3/3
    return avg
n1=int(input())
n2=int(input())
n3=int(input())
result=add(n1,n2,n3)
print(result)
'''
#avg of num without function
'''
n=int(input())
total=0
for i in range(n):
    num=int(input('enter num'))
    total+=num
avg=total/num
print(avg)
'''
#avg with fn
'''
def avg(n):
    total=0
    for i in range(n):
        num=int(input('enter numbers:'))
        total+=num
    return total/n

n=int(input())
result=avg(n)
print(result)
''' 
#9 sum of digit
''''
n=int(input())
s=0
while(n>0):
    digit=n%10
    s+=digit
    n//=10
print(s)
'''
#10 product of digit
'''
n=int(input())
product=1
while n > 0:
    digit=n%10
    product*=digit
    n//=10
print(product)
'''
#11 reverse number
'''
#method -1
n=int(input())
rev=0
while n>0:
    digit=n%10
    rev=rev *10+digit
    n//=10
print(rev)
#method 2 when they mention no
n=123
print(n[::-1])
'''
