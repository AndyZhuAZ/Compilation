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
        self.representation = input.split('\n')

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



    # def delleft(self):
    #     """
    #     消除左递归与|
    #     :return:
    #     """
    #     remove_list = []
    #     for i in self.representation:
    #         # print(i)
    #         if '|' in i:
    #             # print(i)
    #             left, right = i.split(' -> ')
    #             right_list = right.split(' | ')
    #             remove_list.append(i)
    #             # self.representation.remove(i) # 影响指针，修改循环外删除
    #             self.representation+=[left+' -> '+str(right) for right in right_list]
    #
    #     for i in remove_list:
    #         self.representation.remove(i)
    #
    #     print('消除左递归', self.representation)

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
                flag = 0
                left, right = i.split(' -> ')
                right_list = right.split(' | ')
                remove_list_ = []
                folow_left = []  # 在右部中出现在左部之后的表达式
                new_right = []
                for j in right_list:
                    temp = j.split(' ')
                    if temp[0] is left:
                        remove_list_.append(right_list[right_list.index(j)])
                        folow_left.extend(temp[1:])
                        new_right.append(' '.join(temp[1:]) + " " + left + "'")
                    if j in folow_left:
                        flag = 1
                        right_list[right_list.index(j)] = j + str(" " + left + "'")
                    if j[0] is not left:
                        flag = 1
                        right_list[right_list.index(j)] = j + str(" " + left + "'")
                if flag is 1:
                    new_right.append('ε')
                for re in remove_list_:
                    right_list.remove(re)
                remove_list.append(i)
                # self.representation.remove(i) # 影响指针，修改循环外删除
                self.representation += [left + ' -> ' + str(right) for right in right_list]
                if flag is 1:
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

        print('TABLE')
        for i in self.table.keys():
            print(i, self.table[i])
        print('TABLE Dataframe')
        tmp = pd.DataFrame(ll1.table).T.fillna('')
        # tmp.to_csv('./table.csv')
        print(tmp)




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
            if input_str[i]!=c:
                if input_str[i] in self.table[c].keys():    # 如果有这个表达式
                    representation = self.table[c][input_str[i]]
                    left_representation, right_representation = representation.split(' -> ')
                    right_representation_list = right_representation.split(' ')

                    if right_representation == 'ε':
                        c = stack.pop()

                        continue

                    stack+=[i for i in right_representation_list[::-1]]
                    print(stack)

                    table.add_row([stack.__str__(), input_str[i:], representation])



                    c = stack.pop()

            else:
                print(stack)



                table.add_row([stack.__str__(), input_str[i:], '匹配'+input_str[i]])

                i = i + 1
                c = stack.pop()

        print(table)






if __name__ == '__main__':
    pass
    ll1 = LL1()
    ll1.get_representation()
    ll1.indirect2direct()
    ll1.de_direct_recursion()


    ll1.out_VT_VN()


    ll1.get_first()

    ll1.get_follow()

    ll1.get_tabel()

    ll1.analyze()







