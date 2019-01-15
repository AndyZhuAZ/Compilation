# coding:utf8

import pandas as pd
from prettytable import PrettyTable

class LL1:
    def __init__(self):
        self.VT = set()    # 终结符
        self.VN = set()    # 非终结符
        self.representation = []

        self.first_state = 'E'   # 初始状态

        self.first = dict()
        self.follow = dict()

        self.table = dict()


    def get_representation(self):
        """
        从本地文件读取获取产生式，空格分隔
        :return:
        """
        fo = open("./产生式5.txt", "r")
        input = fo.read()
        # self.representation = input.split('\n')
        # self.representation = ['S -> A a | b','A -> A c | S d | ε']
        self.representation=['E -> E + T | T','T -> T * F | F','F -> ( E ) | id']
        # self.representation=['P -> A a | i','A -> P b']

        print('产生式：', self.representation)

    def get_VT_VN(self):
        """
        根据产生式，获取终结符，非终结符
        :return:
        """
        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')   # 前后消空格
            self.VN.add(left_representation)

        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')
            for r in right_representation.split(' '):
                if r not in self.VN | set(['|', 'ε']):
                    self.VT.add(r)



    def out_VT_VN(self):
        self.get_VT_VN()
        print('非终结符：', self.VN)
        print('终结符：', self.VT)



    #直接间接左递归选择入口
    def is_recursion(self):
        is_indirect = False
        is_direct = False
        left_set = set()

        # 获取表达式左部集
        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')
            left_set.add(left_representation)

        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')
            right_representation_list = right_representation.split(' | ')

            flag = 0

            for right in right_representation_list:
                right = right.split(' ')

                if left_representation == right[0]:
                    is_direct = True
                # 间接左递归
                for isIndirect_representation in self.representation:
                    if isIndirect_representation == representation:
                        continue
                    isIndirect_left_representation, isIndirect_right_representation = isIndirect_representation.split(' -> ')
                    # 判断是否又递归关系
                    if isIndirect_left_representation != right[0]:
                        continue
                    # 划分具体
                    isIndirect_right_representation_list = isIndirect_right_representation.split(' | ')
                    for isIndirect_right in isIndirect_right_representation_list:
                        isIndirect_right_list =  isIndirect_right.split(' ')
                        if left_representation == isIndirect_right_list[0]:
                            pass
                            is_indirect = True

                            print('间接', representation, isIndirect_representation)


        if is_indirect:
            pass
            print('indirect')
            self.indirect2direct()
            self.de_direct_recursion()
        elif is_direct:
            pass
            print('direct')
            self.de_direct_recursion()
        else:
            print('none')

            #     elif flag == 0:
            #         pass
            #
            #
            # for right in right_representation_list:
            #     r = right.split(' ')
            #     for isIndirect_representation in self.representation:
            #         isIndirect_left_representation, isIndirect_right_representation = isIndirect_representation.split(' -> ')
            #         if isIndirect_left_representation == r[0]:
            #             is_indirect = True
            #             break
            #     if is_indirect:
            #         break
            #
            #
            #
            #
            #
            #
            #
            #
            #
            #
            # right_representation_list_ = []
            # for i in right_representation_list:
            #     right_representation_list_ += i.split(' ')
            #
            # # 间接
            # for isIndirect_representation in self.representation:
            #     isIndirect_left_representation, isIndirect_right_representation = isIndirect_representation.split(
            #         ' -> ')
            #     # 划分具体
            #     isIndirect_representation_list = isIndirect_right_representation.split(' | ')
            #     # isIndirect_representation_list_ = isIndirect_representation_list.split(' ')
            #     isIndirect_representation_list_ = []
            #     for i in isIndirect_representation_list:
            #         isIndirect_representation_list_ += i.split(' ')
            #
            #     if isIndirect_left_representation in isIndirect_representation_list_:
            #         # print('间接', representation, ',   ', isIndirect_representation)
            #         is_indirect = True
            #         continue  # 注意这个continue，多种情况
            # # 如果是间接，不判断直接
            # if is_indirect:
            #     self.indirect2direct()
            #     self.de_direct_recursion()
            #     break
            #
            # if left_representation in right_representation_list_:
            #     # print('直接', representation)
            #     self.de_direct_recursion()
            #     break

        # print('无递归')
    # 间接左递归变直接左递归
    def indirect2direct(self):
        self.get_VT_VN()
        message = []
        remove_list = []
        for i in self.representation:
            left, right = i.split(' -> ')
            for j in right.split(' '):
                if j in self.VN:
                    message.append(str(j + ' at right of ' +i))
                    message.append(j)
        for i in self.representation:
            left, right = i.split(' -> ')
            right_list = right.split(' | ')
            if left in right:
                if str(left + ' at right of ' +i) in message:
                    flag = 0
                    for j in right_list:
                        j = j.split(' ')
                        if j[0] in self.VN:
                            if j[0] is not left:
                                for k in self.representation:
                                    kleft, kright = k.split(' -> ')#注意这里的leftright是k循环内的新变量
                                    kright_list = kright.split(' | ')
                                    if kleft is j[0]:
                                        a = []
                                        a += [str(r) for r in kright_list]
                                        for c in a :
                                            a[a.index(c)] = a[a.index(c)] + right_list[right_list.index(' '.join(tmp for tmp in j))][1:]
                                        right_list.remove(' '.join(tmp for tmp in j))
                                        right_list.extend(a)
                                        remove_list.append(k)
                    self.representation += [left + ' -> ' + ' | '.join(right for right in right_list)]
                    remove_list.append(i)
                    pass
        for i in remove_list:
            self.representation.remove(i)
        print('间接左递归变直接左递归', self.representation)

    def de_direct_recursion(self):
        remove_list = []

        for i in self.representation:

            if '|' in i:
                ldirect_flag = False
                flag = False
                epsilion_flag = False
                left, right = i.split(' -> ')
                right_list = right.split(' | ')

                remove_list_ = []
                follow_left = []  # 在右部中出现在左部之后的表达式
                new_right = []

                for j in right_list:
                    temp = j.split(' ')
                    if temp[0] is left:
                        ldirect_flag = True
                        remove_list_.append(j)    # 当前元素加入删除列表
                        follow_left.extend(temp[1:])    # left的follow
                        new_right.append(' '.join(temp[1:]) + " " + left + "'") # 新的右部
                    elif temp[0] == 'ε':  # 第一个为空，表示为空
                        new_right.append('ε')  # 新的右部
                        epsilion_flag = True
                        remove_list_.append(j)
                    # elif temp[0] == '(':
                    #     pass
                    elif not ldirect_flag:
                        pass
                    elif temp[0] is not left:
                        flag = True
                        right_list[right_list.index(j)] = j + str(" " + left + "'") # 所有开头非左部表达四，都变成以他开头加左部'

                if epsilion_flag:
                    right_list.append(left + "'")  # 新的右部
                if flag:
                    new_right.append('ε')
                    # if j in follow_left:
                    #     flag = 1
                    #     right_list[right_list.index(j)] = j + str(" " + left + "'")
                    # if j[0] is not left:
                    #     flag = 1
                    #     right_list[right_list.index(j)] = j + str(" " + left + "'")
                # if flag is 1:
                #     new_right.append('ε')
                for re in remove_list_:
                    right_list.remove(re)
                # right_list.extend(new_right)
                remove_list.append(i)
                # self.representation.remove(i) # 影响指针，修改循环外删除
                self.representation += [left + ' -> ' + str(right) for right in right_list]
                if flag:
                    self.representation += [left + "'" + ' -> ' + str(right) for right in new_right]
            # else:
            #     left, right = i.split(' -> ')
            #     remove_list_ = []
            #     folow_left = []  # 在右部中出现在左部之后的表达式
            #     new_right = []
            #     temp = right.split(' ')
            #     if temp[0] is left:
            #         self.representation += [left + ' -> ' + ' '.join(temp[1:]) + left + "'"]
            #         self.representation += [left + "'" + ' -> ' + str(right) for right in new_right]
            #         remove_list_.append(right_list[right_list.index(j)])
            #         folow_left.extend(temp[1:])
            #         new_right.append(' '.join(temp[1:]) + " " + left + "'")
        for i in remove_list:
            self.representation.remove(i)

        print('消除左递归', self.representation)

    def get_first_VN(self,r):
        """
        获取first集的递归调用
        :param r: 右子表达式，左边第一个非终结符
        :return: first集(set)
        """
        add = set()
        for representation_ in self.representation:
            left_representation_, right_representation_ = representation_.split(' -> ')
            if left_representation_ == r:
                right_representation_list_ = right_representation_.split(' ')
                if right_representation_list_[0] in self.VT|set(['ε']):
                    add.add(right_representation_list_[0])
                elif right_representation_list_[0] in self.VN:
                    add|=(self.get_first_VN(right_representation_list_[0]))
        return add

    def get_first(self):
        """
        获取first集
        :return:
        """
        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')

            if left_representation not in self.first.keys():
                self.first[left_representation] = set()

            # 3种情况，第一个为非终结符/ε/终结符
            right_representation_list = right_representation.split(' ')
            if right_representation_list[0] in self.VT|set(['ε']):
                self.first[left_representation].add(right_representation_list[0])
            elif right_representation_list[0] in self.VN:
                self.first[left_representation]|=self.get_first_VN(right_representation_list[0])

        print('FIRST')
        for i in self.first.keys():
            print(i, self.first[i])

    def get_follow(self):
        for i in self.VN:
            # 初始化
            if i not in self.follow.keys():
                self.follow[i] = set('$')

            for representation in self.representation:
                left_representation, right_representation = representation.split(' -> ')
                right_representation_list = right_representation.split(' ')

                if i in right_representation_list:
                    next = ''
                    # 第一种情况，后面没有
                    if len(right_representation_list) == right_representation_list.index(i)+1:    # 越界问题
                        # self.follow[i]|=self.follow[left_representation]    # 最后一位，后面没有的情况，follow加进来
                        pass
                    else:
                        next = right_representation_list[right_representation_list.index(i) + 1]

                    if next in self.VN:
                        # 第一种情况，后面指向空
                        if next + ' -> ε' in self.representation:
                            # self.follow[i] |= self.follow[left_representation]  # 最后一位，后面没有的情况，follow加进来
                            pass
                        self.follow[i]|=self.first[right_representation_list[right_representation_list.index(i) + 1]]
                        self.follow[i].remove('ε')

                    if next in self.VT:
                        self.follow[i].add(next)

        for i in self.VN:
            for representation in self.representation:
                left_representation, right_representation = representation.split(' -> ')
                right_representation_list = right_representation.split(' ')

                if i in right_representation_list:
                    next = ''
                    # 第一种情况，后面没有
                    if len(right_representation_list) == right_representation_list.index(i)+1:    # 越界问题
                        self.follow[i]|=self.follow[left_representation]    # 最后一位，后面没有的情况，follow加进来
                    else:
                        next = right_representation_list[right_representation_list.index(i) + 1]

                    if next in self.VN:
                        # 第一种情况，后面指向空
                        if next + ' -> ε' in self.representation:
                            self.follow[i] |= self.follow[left_representation]  # 最后一位，后面没有的情况，follow加进来
                        self.follow[i]|=self.first[right_representation_list[right_representation_list.index(i) + 1]]
                        self.follow[i].remove('ε')

                    if next in self.VT:
                        self.follow[i].add(next)

        for i in self.VN:
            for representation in self.representation:
                left_representation, right_representation = representation.split(' -> ')
                right_representation_list = right_representation.split(' ')

                if i in right_representation_list:
                    next = ''
                    # 第一种情况，后面没有
                    if len(right_representation_list) == right_representation_list.index(i)+1:    # 越界问题
                        self.follow[i]|=self.follow[left_representation]    # 最后一位，后面没有的情况，follow加进来
                    else:
                        next = right_representation_list[right_representation_list.index(i) + 1]

                    if next in self.VN:
                        # 第一种情况，后面指向空
                        if next + ' -> ε' in self.representation:
                            self.follow[i] |= self.follow[left_representation]  # 最后一位，后面没有的情况，follow加进来
                        self.follow[i]|=self.first[right_representation_list[right_representation_list.index(i) + 1]]
                        self.follow[i].remove('ε')

                    if next in self.VT:
                        self.follow[i].add(next)


        print('FOLLOW')
        for i in self.follow.keys():
            print(i, self.follow[i])


    def get_tabel(self):
        for representation in self.representation:
            left_representation, right_representation = representation.split(' -> ')
            right_representation_list = right_representation.split(' ')

            # 一阶字典初始化
            if left_representation not in self.table.keys():
                self.table[left_representation] = dict()

            first = set('ε')
            if right_representation_list[0] in self.VN:
                first = self.first[right_representation_list[0]]
            elif right_representation_list[0] in self.VT:
                first = set()
                first.add(right_representation_list[0])

            if 'ε' in first:
                for i in first:
                    if i == 'ε':
                        continue
                    self.table[left_representation][i] = representation
                for i in self.follow[left_representation]:
                    self.table[left_representation][i] = representation
            else:
                for i in first:
                    self.table[left_representation][i] = representation

        # 新加内容
        print('\n\n\n')
        for i in self.VN:
            for j in self.follow[i]:
                if j not in self.table[i]:
                    self.table[i][j] = 'synch'

        print('TABLE')
        for i in self.table.keys():
            print(i, self.table[i])
        print('df_TABLE')
        df_table = pd.DataFrame(ll1.table).T.fillna('')
        # tmp.to_csv('./table.csv')
        print(df_table)



    #2019年1月13日
    # def analyze(self):
    #     """
    #     对用户输入语句进行语法分析
    #     :return:
    #     """
    #     input_str = input("请输入：")
    #     input_str+=' $'
    #
    #     input_str = input_str.split(' ')
    #
    #     stack = ['$']
    #     # 开始符号
    #     stack.append(self.first_state)
    #
    #     c = stack.pop() # 访问栈
    #     i = 0           # 访问str
    #
    #     table = PrettyTable(["栈", "输入", "动作"])
    #     table.padding_width = 1
    #     table.align = "l"
    #
    #     table.add_row([stack.__str__(), input_str[i:], ''])
    #
    #     while c!='$':
    #         if input_str[i]!=c:
    #             if input_str[i] in self.table[c].keys():    # 如果有这个表达式
    #                 representation = self.table[c][input_str[i]]
    #                 left_representation, right_representation = representation.split(' -> ')
    #                 right_representation_list = right_representation.split(' ')
    #
    #                 if right_representation == 'ε':
    #                     c = stack.pop()
    #
    #                     continue
    #
    #                 stack+=[i for i in right_representation_list[::-1]]
    #                 print(stack)
    #
    #                 table.add_row([stack.__str__(), input_str[i:], representation])
    #
    #
    #
    #                 c = stack.pop()
    #
    #         else:
    #             print(stack)
    #
    #
    #
    #             table.add_row([stack.__str__(), input_str[i:], '匹配'+input_str[i]])
    #
    #             i = i + 1
    #             c = stack.pop()
    #
    #     print(table)

    def analyze(self):
        """
        对用户输入语句进行语法分析
        :return:
        """
        input_str = input("请输入：")
        input_str+=' $'

        input_str = input_str.split(' ')

        stack = ['$']
        # 开始符号
        stack.append(self.first_state)

        c = stack.pop() # 访问栈
        i = 0           # 访问str

        table = PrettyTable(["栈", "输入", "动作"])
        table.padding_width = 1
        table.align = "l"

        table.add_row([stack.__str__(), input_str[i:], ''])

        while c!='$':
            if c in self.VN:    # 非终结符
                if input_str[i] in self.table[c].keys():  # 如果有这个表达式，查表
                    representation = self.table[c][input_str[i]]

                    # 查表，弹栈顶
                    if representation == 'synch':
                        table.add_row([stack.__str__(), input_str[i:], 'error:' + str(i) + input_str[i]])   # 先报错，再弹栈顶
                        c = stack.pop()
                        continue

                    left_representation, right_representation = representation.split(' -> ')
                    right_representation_list = right_representation.split(' ')

                    # 如果指向空，则替换为空，直接弹下一个
                    if right_representation == 'ε':
                        c = stack.pop()
                        continue

                    # 正常情况反向进栈
                    stack+=[i for i in right_representation_list[::-1]]

                    table.add_row([stack.__str__(), input_str[i:], representation])
                    c = stack.pop()

                # 查表为空, 报错，忽略输入
                else:
                    table.add_row([stack.__str__(), input_str[i:], 'error:'+str(i)+input_str[i]])
                    i = i + 1

            elif c in self.VT:  # 终结符
                if input_str[i] == c:   # 栈顶是否匹配输入
                    table.add_row([stack.__str__(), input_str[i:], '匹配' + input_str[i]])
                    i = i + 1
                    c = stack.pop()
                else:   # 不匹配，栈顶弹出
                    c = stack.pop()


        print(table)





if __name__ == '__main__':
    pass
    ll1 = LL1()
    ll1.get_representation()
    ll1.is_recursion()
    # ll1.indirect2direct()
    # ll1.de_direct_recursion()
    exit()

    ll1.out_VT_VN()


    ll1.get_first()

    ll1.get_follow()

    ll1.get_tabel()

    ll1.analyze()







