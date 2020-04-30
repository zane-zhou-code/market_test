import heapq
import itertools
from collections import Counter
import sys
import time
from functools import wraps
from threading import Lock

class xhzhou():
    def select_sort(origin_items, comp=lambda x, y: x < y):
        """简单选择排序"""
        items = origin_items[:]
        for i in range(len(items) - 1):
            min_index = i
            for j in range(i + 1, len(items)):
                if comp(items[j], items[min_index]):
                    min_index = j
            items[i], items[min_index] = items[min_index], items[i]
        return items

    def bubble_sort(origin_items, comp=lambda x, y: x > y):
        """高质量冒泡排序(搅拌排序)"""
        items = origin_items[:]
        for i in range(len(items) - 1):
            swapped = False
            for j in range(i, len(items) - 1 - i):
                if comp(items[j], items[j + 1]):
                    items[j], items[j + 1] = items[j + 1], items[j]
                    swapped = True
            if swapped:
                swapped = False
                for j in range(len(items) - 2 - i, i, -1):
                    if comp(items[j - 1], items[j]):
                        items[j], items[j - 1] = items[j - 1], items[j]
                        swapped = True
            if not swapped:
                break
        return items

    def merge_sort(items, comp=lambda x, y: x <= y):
        """归并排序(分治法)"""
        if len(items) < 2:
            return items[:]
        mid = len(items) // 2
        left = xhzhou.merge_sort(items[:mid], comp)
        right = xhzhou.merge_sort(items[mid:], comp)
        return xhzhou.merge(left, right, comp)

    def merge(items1, items2, comp):
        """合并(将两个有序的列表合并成一个有序的列表)"""
        items = []
        index1, index2 = 0, 0
        while index1 < len(items1) and index2 < len(items2):
            if comp(items1[index1], items2[index2]):
                items.append(items1[index1])
                index1 += 1
            else:
                items.append(items2[index2])
                index2 += 1
        items += items1[index1:]
        items += items2[index2:]
        return items

    def seq_search(items, key):
        """顺序查找"""
        for index, item in enumerate(items):
            if item == key:
                return index
        return -1

    def bin_search(items, key):
        """折半查找"""
        start, end = 0, len(items) - 1
        while start <= end:
            mid = (start + end) // 2
            if key > items[mid]:
                start = mid + 1
            elif key < items[mid]:
                end = mid - 1
            else:
                return mid
        return -1

    def aa(self):
        # 字典
        prices = {
            'AAPL': 191.88,
            'GOOG': 1186.96,
            'IBM': 149.24,
            'ORCL': 48.44,
            'ACN': 166.89,
            'FB': 208.09,
            'SYMC': 21.29
        }
        # 用股票价格大于100元的股票构造一个新的字典
        prices2 = {key: value for key, value in prices.items() if value > 100}
        print(prices2)

    def ab(self):
        # 录入成绩
        names = ['关羽', '张飞', '赵云', '马超', '黄忠']
        courses = ['语文', '数学', '英语']
        # 录入五个学生三门课程的成绩
        # 错误 - 参考http://pythontutor.com/visualize.html#mode=edit
        # scores = [[None] * len(courses)] * len(names)
        scores = [[None] * len(courses) for _ in range(len(names))]
        for row, name in enumerate(names):
            for col, course in enumerate(courses):
                scores[row][col] = float(input(f'请输入{name}的{course}成绩: '))
                print(scores)

    def ac(self):
        """
            从列表中找出最大的或最小的N个元素
            堆结构(大根堆/小根堆)
            """
        list1 = [34, 25, 12, 99, 87, 63, 58, 78, 88, 92]
        list2 = [
            {'name': 'IBM', 'shares': 100, 'price': 91.1},
            {'name': 'AAPL', 'shares': 50, 'price': 543.22},
            {'name': 'FB', 'shares': 200, 'price': 21.09},
            {'name': 'HPQ', 'shares': 35, 'price': 31.75},
            {'name': 'YHOO', 'shares': 45, 'price': 16.35},
            {'name': 'ACME', 'shares': 75, 'price': 115.65}
        ]
        print(heapq.nlargest(3, list1))
        print(heapq.nsmallest(3, list1))
        print(heapq.nlargest(2, list2, key=lambda x: x['price']))
        print(heapq.nlargest(2, list2, key=lambda x: x['shares']))

    def ad(self):
        """
            迭代工具 - 排列 / 组合 / 笛卡尔积
            """
        itertools.permutations('ABCD')
        itertools.combinations('ABCDE', 3)
        itertools.product('ABCD', '123')

    def ae(self):
        """
        找出序列中出现次数最多的元素
        """
        words = [
            'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
            'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around',
            'the', 'eyes', "don't", 'look', 'around', 'the', 'eyes',
            'look', 'into', 'my', 'eyes', "you're", 'under'
        ]
        counter = Counter(words)
        print(counter.most_common(3))

    def af(self):
        # 公鸡5元一只 母鸡3元一只 小鸡1元三只
        # 用100元买100只鸡 问公鸡/母鸡/小鸡各多少只
        for x in range(20):
            for y in range(33):
                z=int(self)-x-y
                if 5*x+3*y+z//3==int(self) and z%3==0:
                    print(x,y,z)

    def ag(self):
        # A、B、C、D、E五人在某天夜里合伙捕鱼 最后疲惫不堪各自睡觉
        # 第二天A第一个醒来 他将鱼分为5份 扔掉多余的1条 拿走自己的一份
        # B第二个醒来 也将鱼分为5份 扔掉多余的1条 拿走自己的一份
        # 然后C、D、E依次醒来也按同样的方式分鱼 问他们至少捕了多少条鱼
        fish=6
        while True:
            total=fish
            enough=True
            for _ in range(5):
                if(total-1)%5==0:
                    total=(total-1)//5*4
                else:
                    enough=False
                    break
            if enough:
                print(fish)
                break
            fish+=5

        """
        贪婪法：在对问题求解时，总是做出在当前看来是最好的选择，不追求最优解，快速找到满意解。
        输入：
        20 6
        电脑 200 20
        收音机 20 4
        钟 175 10
        花瓶 50 2
        书 10 1
        油画 90 9
        """
    class Thing(object):
        """物品"""
        def __init__(self,name,price,weight):
            self.name=name
            self.price=price
            self.weight=weight
        def value(self):
            """价格重量对比"""
            return self.price/self.weight
    def input_thing(self):
        """输入物品信息"""
        name_str,price_str,weight_str=input().split()
        return name_str,int(price_str),int(weight_str)
    def main(self):
        """主函数"""
        max_weight,num_of_things=map(int,input().split)
        all_things=[]
        for _ in range(num_of_things):
            all_things.append(xhzhou.Thing(*xhzhou.input_thing()))
        all_things.sort(key=lambda x: x.value,reversed=True)
        total_weight=0
        total_price=0
        for thing in all_things:
            if total_weight+thing.weight<=max_weight:
                print(f'小偷拿走了{thing.name}')
                total_weight+=thing.weight
                total_price+=thing.price
        print(f'总价值：{total_price}美元')

    """
    快速排序 - 选择枢轴对元素进行划分，左边都比枢轴小右边都比枢轴大
    """
    def quick_sort(origin_items,comp=lambda x,y:x<=y):
        items=origin_items[:]
        xhzhou._quick_sort(items,0,len(items)-1,comp)
        return  items
    def _quick_sort(items,start,end,comp):
        if start<end:
            pos=xhzhou._partition(items,start,end,comp)
            xhzhou.quick_sort(items,start,pos-1,comp)
            xhzhou.quick_sort(items,pos+1,end,comp)
    def _partition(items,start,end,comp):
        pivot=items[end]
        i=start-1
        for j in range(start,end):
            if comp(items[j],pivot):
                i+=1
                items[i], items[j] = items[j], items[i]
        items[i + 1], items[end] = items[end], items[i + 1]
        return i + 1

    """
    递归回溯法：叫称为试探法，按选优条件向前搜索，当搜索到某一步，发现原先选择并不优或达不到目标时，就退回一步重新选择，比较经典的问题包括骑士巡逻、八皇后和迷宫寻路等。
    """
    SIZE=5
    total=0
    def print_board(board):
        for row in board:
            for col in row:
                print(str(col).center(4),end='')
            print()
    def patrol(board,row,col,step=1):
        if row>=0 and row<xhzhou.SIZE and \
            col>=0 and col<xhzhou.SIZE and \
            board[row][col]==0:
            board[row][col]=step
            if step==xhzhou.SIZE*xhzhou.SIZE:
                global total
                total+=1
                print(f'第{total}种走法：')
                xhzhou.print_board(board)
            xhzhou.patrol(board, row - 2, col - 1, step + 1)
            xhzhou.patrol(board, row - 1, col - 2, step + 1)
            xhzhou.patrol(board, row + 1, col - 2, step + 1)
            xhzhou.patrol(board, row + 2, col - 1, step + 1)
            xhzhou.patrol(board, row + 2, col + 1, step + 1)
            xhzhou.patrol(board, row + 1, col + 2, step + 1)
            xhzhou.patrol(board, row - 1, col + 2, step + 1)
            xhzhou.patrol(board, row - 2, col + 1, step + 1)
            board[row][col] = 0

    def ah(self):
        board = [[0] * xhzhou.SIZE for _ in range(xhzhou.SIZE)]
        xhzhou.patrol(board, xhzhou.SIZE - 1, xhzhou.SIZE - 1)

    """
    动态规划 - 适用于有重叠子问题和最优子结构性质的问题
    使用动态规划方法所耗时间往往远少于朴素解法(用空间换取时间)
    """
    def fib(num, temp={}):
        """用递归计算Fibonacci数"""
        if num in (1, 2):
            return 1
        try:
            return temp[num]
        except KeyError:
            temp[num] = xhzhou.fib(num - 1) + xhzhou.fib(num - 2)
            return temp[num]

    def ai(self):
        items = list(map(int, input().split()))
        size = len(items)
        overall, partial = {}, {}
        overall[size - 1] = partial[size - 1] = items[size - 1]
        for i in range(size - 2, -1, -1):
            partial[i] = max(items[i], partial[i + 1] + items[i])
            overall[i] = max(partial[i], overall[i + 1])
        print(overall[0])

    def record_time(func):
        """自定义装饰函数的装饰器"""
        @wraps(func)
        def wrapper(*args,**kwargs):
            start=time()
            result=func(*args,**kwargs)
            print(f'{func.__name__}:{time()-start}秒')
            return result
        return wrapper

    def record(output):
        """自定义带参数的装饰器"""
        def decorate(func):
            @wraps(func)
            def wrapper(*args,**kwargs):
                start=time()
                result=func(*args,**kwargs)
                output(func.__name__,time()-start)
                return result
            return wrapper
        return decorate

    def Record(self):
        """自定义装饰器类(通过__call__魔术方法使得对象可以当成函数调用)"""
        def __init__(self,output):
            self.output=output
        def __call__(self,func):
            @wraps(func)
            def wrapper(*args,**kwargs):
                start=time()
                result=func(*args,**kwargs)
                self.output(func.__name__,time()-start)
                return result
            return wrapper

    def singleton(cls):
        """线程安全的单例装饰器"""
        instances={}
        locker=Lock()
        @wraps(cls)
        def wrapper(*args,**kwargs):
            if cls not in instances:
                with locker:
                    if cls not in instances:
                        instances[cls]=cls(*args,**kwargs)
            return instances[cls]
        return wrapper












def main():
    print(xhzhou.select_sort([15, 3, 45, 2, 1, 5]))
    print(xhzhou.bubble_sort([115, 13, 145, 12, 11, 15]))
    print(xhzhou.merge_sort([115, 13, 145, 12, 11, 15]))
    print(xhzhou.seq_search([11, 15, 16, 88, 54], 54))
    # xhzhou.af(100)
    # xhzhou.ag()


if __name__ == '__main__':
    main()
