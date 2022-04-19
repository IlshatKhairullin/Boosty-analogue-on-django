class BinaryHeap:
    def __init__(self):
        self.heapList = [0]
        self.size = 0

class MinBinaryHeap(BinaryHeap):

    def Down_to_Up(self, i):
        while i // 2 > 0:
            if self.heapList[i] < self.heapList[i // 2]:  # for min_heap
                parent = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = parent
            i = i // 2

    def push_to_end(self, num):
        self.heapList.append(num)
        self.size = self.size + 1
        self.Down_to_Up(self.size)  # self.size - как бы индекс последнего (добавленного) элемента

    def Up_to_Down(self, i):  # i - индекс элемента, который нужно спустить вниз
        while 2 * i <= self.size:
            min_child = self.minChild(i)
            if self.heapList[i] > self.heapList[min_child]:
                current_elem = self.heapList[i]
                self.heapList[i] = self.heapList[min_child]
                self.heapList[min_child] = current_elem
            i = min_child

    def minChild(self, i):
        if 2 * i + 1 > self.size:  # в процессе мы удалили last элемент, рано или поздно 2*i+1
            # будет больше размера кучи (это значит, что правый потомок не входит в диапазон размера кучи (его нету))
            return 2 * i
        # elif 2 * i > self.size:
        #     return 2 * i + 1
        else:
            if self.heapList[2 * i] > self.heapList[2 * i + 1]:
                return 2 * i + 1
            else:
                return 2 * i

    # def minChild(self, i):
    #     if i * 2 + 1 > self.size:
    #         return i * 2
    #     else:
    #         if self.heapList[i * 2] < self.heapList[i * 2 + 1]:
    #             return i * 2
    #         else:
    #             return i * 2 + 1

    def show_min_element(self):
        return self.heapList[1]

    def pop_min_elem(self):
        min_elem = self.heapList[1]  # минимальный элемент
        self.heapList[1] = self.heapList[self.size]  # ставим вместо удаленного миним элемента последний элемент
        self.heapList.pop()  # удаляем последний элемент
        self.size = self.size - 1
        self.Up_to_Down(1)  # падаем в метод индекс удаленного элемента
        return min_elem

    def buildHeap(self, alist):
        i = len(alist) // 2
        self.size = len(alist)
        self.heapList = [0] + alist[:]
        while i > 0:
            self.Up_to_Down(i)
            i = i - 1

    def show_len(self):
        return self.size

class MaxBinaryHeap(BinaryHeap):
    pass


bh = MinBinaryHeap()
bh.buildHeap([9, 5, 6, 2, 3])

print(bh.pop_min_elem())
print(bh.pop_min_elem())
print(bh.pop_min_elem())
print(bh.pop_min_elem())
print(bh.pop_min_elem())
