from sys import stdin
import itertools

stdin = open('t.txt')

def replace2(data, ind, char):
    listed = list(data)
    listed[ind] = char
    return ''.join(listed)

def make9(data, y, x, zone_y, zone_x, data_type):
    if data_type == 'row':
        return data[y]
    elif data_type == 'column':
        return ''.join([data[i][x] for i in range(9)])
    elif data_type == 'square':
        return ''.join([data[3*zone_y + i][3*zone_x : 3*(zone_x+1)] for i in range(3)])

def del_option(option, y, x, num):
    # y, x, num: int
    # option:  list
    for j in range(9): # row
        if num in option[y][j]:
            option[y][j].remove(num)
    for j in range(9): # column
        if num in option[j][x]:
            option[j][x].remove(num)
    for p, q in itertools.product(range(3),range(3)): # square
        m, n = (y//3)*3 + p, (x//3)*3 + q
        if num in option[m][n]:
            option[m][n].remove(num)
    return option

def main():
    """#
    data = ['000 000 000',
            '000 000 000',
            '000 000 000',
            '000 000 000',
            '000 000 000',
            '000 000 000',
            '000 000 000',
            '000 000 000',
            '000 000 000']
    data = [data[k].replace(' ','') for k in range(9)]
    #"""
    data = [stdin.readline().rstrip() for i in range(9)]
    print(*data, sep = '\n', end = '\n')
    print()
    #
    option = [[ [] for _ in range(9)] for _ in range(9)]
    for j, i in itertools.product(range(9),range(9)):
        if data[j][i] != '0':
            option[j][i] = []
        else:
            tmp = ''.join([make9(data = data, y = j, x = i, zone_y = j//3, zone_x = i//3, data_type = k) \
                    for k in ['row', 'column', 'square']])
            option[j][i] = [k for k in range(1,10) if str(k) not in tmp]
    aft = ''.join(data).count('0')
    while aft > 0:
        bef = aft
        # while any([len(option[k//9][k%9]) == 1 for k in range(81)]) :
        for j, i in itertools.product(range(9),range(9)):
            if len(option[j][i]) == 1 and data[j][i] == '0':
                num = option[j][i].pop()
                option[j][i].clear()
                data[j] = replace2(data[j], i, str(num))
                # delete options of row/column/square
                option = del_option(option = option, y = j, x = i, num = num)
        # for data_type in ['row', 'column', 'square']:
        for dt, j, num in itertools.product(['row','column','square'], range(9), range(1,10)):
            if str(num) in make9(data, y=j, x=j, zone_y = j//3, zone_x = j%3, data_type=dt):
                continue
            if dt == 'row':
                s = [1 if num in option[j][k] else 0 for k in range(9)]
            elif dt == 'column':
                s = [1 if num in option[k][j] else 0 for k in range(9)]
            elif dt == 'square':
                m, n = j//3, j%3 
                s = [1 if num in option[m*3 + k//3][n*3 + k%3] else 0 for k in range(9)]
            if sum(s) == 1:
                ind = s.index(1)
                if dt == 'row':
                    y, x = j, ind
                elif dt == 'column':
                    y, x = ind, j
                elif dt == 'square':
                    y = m*3 + ind//3
                    x = n*3 + ind%3
                data[y] = replace2(data[y], x, str(num))
                option = del_option(option = option, y = y, x = x, num = num)
                option[y][x].clear()
        aft = ''.join(data).count('0')
        if aft == bef:
            print('cannot go on, zero qty: {0}.'.format(aft))
            print()
            break
    else:
        print('completed.', end = '\n')
        print()
    print(*data, sep = '\n', end = '\n')
    #
    print()
    if aft != 0:
        for j, i in itertools.product(range(9),range(9)):
            if data[j][i] == '0':
                print('y:{0} x:{1} : option:{2}'.format(j, i, option[j][i]))

if __name__ == '__main__':
    main()


