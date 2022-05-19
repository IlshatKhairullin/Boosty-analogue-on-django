# бинарный поиск, линейный поиск - это поиск нужного элемента в отсортированном списке(можно считать бин поиск - in)
# бинарный поиск ищет середину списка и сравнивает заданное число с элемом левого списка и правого, соответственно
# так продолжатеся, пока не останется один символ или не останется(значит символа нету)
# сложность logN(основание - 2) в худшем случае(может быть и O(1)), в отличии от линейного поиска - O(n) (worst)

# на рекурсии сделать не получится, тк лимит глубины рекурсии - 1000, а у тут явно больше

def binary_search(array, element):
    mid = 0
    start = 0
    end = len(array)
    step = 0

    while start <= end:
        # print("Subarray in step {}: {}".format(step, str(array[start:end+1])))
        step = step+1
        mid = (start + end) // 2

        if element == array[mid]:
            return mid

        if element < array[mid]:
            end = mid - 1
        else:
            start = mid + 1
    return 'Данного элемента в списке нету'


a = [i for i in range(10**4)]
print(binary_search(a, -1))
