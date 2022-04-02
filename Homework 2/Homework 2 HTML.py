def check():
    with open('For Homework 2.html') as file:
        text = file.read()

        k1 = 0
        k2 = 0
        g = 0
        f = 0

        for i in range(len(text)):

            try:  # 1  блок кода для проверки </></> - т.е. кол-во закрытых скобок
                if text[i] == '<' and text[i + 1] == '/' and text[i + 2] == 'd' and text[i + 3] == 'i' and text[i + 4] == 'v':
                    f += 1
            except:
                continue

            try:  # 2
                if text[i] == '<' and text[i + 1] == '/' and text[i + 2] == 'p':
                    f += 1
            except:
                continue

            try:  # 3
                if text[i] == '<' and text[i + 1] == '/' and text[i + 2] == 'h' and text[i + 3] == '1':
                    f += 1
            except:
                continue

            try:  # обход ошибки с выходом из диапазона
                if text[i] == '<' and text[i + 1] == 'd' and text[i + 2] == 'i' and text[i + 3] == 'v':
                    k1 += 1  # открылась малая скобка <
                    d = 1
            except:
                continue

            try:
                if text[i] == '<' and text[i + 1] == 'p':
                    k1 += 1
                    p = 1
            except:
                continue

            try:
                if text[i] == '<' and text[i + 1] == 'h' and text[i + 2] == '1':
                    k1 += 1
                    h = 1
            except:
                continue

            if text[i] == '>' and k1 == 1:
                k1 -= 1  # закрылась малая скобка >
                g += 1  # как бы открылась большая скобка <>

            if k1 < 0:  # k1 не может быть меньше нуля - если так, то где-то лишний раз закрылась скобка
                return False

            try:  # 1
                if text[i] == '<' and text[i + 1] == '/' and text[i + 2] == 'd' and text[i + 3] == 'i' and text[i + 4] == 'v' and d == 1:
                    k2 += 1
                    d = 0
                    f -= 1
            except:
                continue

            try:  # 2
                if text[i] == '<' and text[i + 1] == '/' and text[i + 2] == 'p' and p == 1:
                    k2 += 1
                    p = 0
                    f -= 1
            except:
                continue

            try:  # 3
                if text[i] == '<' and text[i + 1] == '/' and text[i + 2] == 'h' and text[i + 3] == '1' and h == 1:
                    k2 += 1
                    h = 0
                    f -= 1
            except:
                continue

            if text[i] == '>' and k2 == 1:
                k2 -= 1
                g -= 1  # как бы закрылась большая скобка <></>

            if k2 < 0:  # аналогично k1
                return False
            elif g < 0:  # если g < 0, то значит где-то закрылась лишняя большая скобка (типа до открытия б.скобки)
                return False

        if k1 == 0 and k2 == 0 and g == 0 and f == 0:
            return True
        else:
            return False


print(check())
