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


    def get_(self):
        fo = open("./产生式.txt", "r")
        input = fo.read()

        tmp = input.split('\n')

        # self.VT = tmp[0].split(',')
        # self.VN = tmp[1].split(',')
        self.representation = tmp[2:]

        # print('终结符：', self.VT)
        # print('非终结符：', self.VN)
        print('产生式：', self.representation)


    def get_VT_VN(self):
        for representation in self.representation:
            left_representation, right_representation = representation.split('->')
            self.VN.add(left_representation)

        for representation in self.representation:
            left_representation, right_representation = representation.split('->')
            for r in right_representation:
                if r not in self.VN | set(['|', 'ε']):
                    self.VT.add(r)

    def get_first_state(self):
        for i in self.VN:
            flag = 0
            for representation in self.representation:
                left_representation, right_representation = representation.split('->')
                if i in right_representation:
                    flag+=1
            if flag==0:
                self.first_state = i

        print('first_state:', self.first_state)




#TODO: 消除左递归
    def delleft(self):
        remove_list = []
        for i in self.representation:
            # print(i)
            if '|' in i:
                # print(i)
                left, right = i.split('->')
                right_list = right.split('|')
                remove_list.append(i)
                # self.representation.remove(i) # 影响指针，修改循环外删除
                self.representation+=[left+'->'+str(right) for right in right_list]

        for i in remove_list:
            self.representation.remove(i)




    def get_first_VN(self,r):
        add = set()
        for representation_ in self.representation:
            left_representation_, right_representation_ = representation_.split('->')
            if left_representation_ == r[0]:
                if right_representation_[0] in self.VT|set(['ε']):
                    add.add(right_representation_[0])
                elif right_representation_[0] in self.VN:
                    add|=(self.get_first_VN(right_representation_))

        return add

    def get_first(self):
        for representation in self.representation:
            left_representation, right_representation = representation.split('->')

            if left_representation not in self.first.keys():
                self.first[left_representation] = set()

            # 3种情况，第一个为非终结符/ε/终结符
            if right_representation[0] in self.VT|set(['ε']):
                self.first[left_representation].add(right_representation[0])
            elif right_representation[0] in self.VN:
                self.first[left_representation]|=self.get_first_VN(right_representation[0])

        print('FIRST')
        for i in self.first.keys():
            print(i, self.first[i])

    def get_follow(self):
        for i in self.VN:
            if i not in self.follow.keys():
                self.follow[i] = set('$')

            for representation in self.representation:
                left_representation, right_representation = representation.split('->')

                if i in right_representation:
                    next = ''
                    # 第一种情况，后面没有
                    if len(right_representation) == right_representation.index(i)+1:    # 越界问题
                        # self.follow[i]|=self.follow[left_representation]    # 最后一位，后面没有的情况，follow加进来
                        pass
                    else:
                        next = right_representation[right_representation.index(i) + 1]

                    if next in self.VN:
                        # 第一种情况，后面指向空
                        if next + '->ε' in self.representation:
                            # self.follow[i] |= self.follow[left_representation]  # 最后一位，后面没有的情况，follow加进来
                            pass
                        self.follow[i]|=self.first[right_representation[right_representation.index(i) + 1]]
                        self.follow[i].remove('ε')

                    if next in self.VT:
                        self.follow[i].add(next)

        for i in self.VN:
            for representation in self.representation:
                left_representation, right_representation = representation.split('->')
                
                if i in right_representation:
                    next = ''
                    # 第一种情况，后面没有
                    if len(right_representation) == right_representation.index(i)+1:    # 越界问题
                        print(self.follow[i], self.follow[left_representation])
                        self.follow[i]|=self.follow[left_representation]    # 最后一位，后面没有的情况，follow加进来
                    else:
                        next = right_representation[right_representation.index(i) + 1]

                    if next in self.VN:
                        # 第一种情况，后面指向空
                        if next + '->ε' in self.representation:
                            self.follow[i] |= self.follow[left_representation]  # 最后一位，后面没有的情况，follow加进来
                        self.follow[i]|=self.first[right_representation[right_representation.index(i) + 1]]
                        self.follow[i].remove('ε')

                    if next in self.VT:
                        self.follow[i].add(next)


        print('FOLLOW')
        for i in self.follow.keys():
            print(i, self.follow[i])

    def get_tabel(self):
        for representation in self.representation:
            left_representation, right_representation = representation.split('->')

            if left_representation not in self.table.keys():
                self.table[left_representation] = dict()

            # if 'ε' in self.first[left_representation]:
            #     for i in self.follow[left_representation]:
            #         self.table[left_representation][i] = representation
            #     for i in self.first[left_representation]:
            #         if i == 'ε':
            #             continue
            #         self.table[left_representation][i] = representation
            # else:
            #     # 直接创建，没有空
            #     for i in self.first[left_representation]:
            #         self.table[left_representation][i] = representation

            first = set('ε')

            if right_representation[0] in self.VN:
                first = self.first[right_representation[0]]

            elif right_representation[0] in self.VT:
                first = set(right_representation[0])

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

        pass

        print('TABLE')
        for i in self.table.keys():
            print(i, self.table[i])

        tmp = pd.DataFrame(ll1.table).T
        print(tmp.fillna(''))


    def analyze(self):
        input_str = input("请输入：")
        input_str+='$'

        stack = []
        stack.append('$')
        # 开始符号
        stack.append(self.VN[0])

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
                    left_representation, right_representation = representation.split('->')

                    if right_representation == 'ε':
                        continue

                    stack+=[i for i in right_representation[::-1]]
                    print(stack)

                    table.add_row([stack.__str__(), input_str[i:], representation])



                    c = stack.pop()

            else:
                print(stack)

                i=i+1
                c = stack.pop()

                table.add_row([stack.__str__(), input_str[i:], '匹配'+input_str[i]])


                # table.add_row(['123456789987654321', '123456789987654321', '123456789987654321'])

                # exit()
        print(table)

        exit()






        print(stack)





if __name__ == '__main__':
    pass
    ll1 = LL1()
    ll1.get_()

    ll1.get_VT_VN()

    # ll1.get_first_state()


    print('终结符：', ll1.VT)
    print('非终结符：', ll1.VN)
    # exit()

    ll1.delleft()

    ll1.get_first()

    print(ll1.representation)
    ll1.get_follow()

    ll1.get_tabel()



    ll1.analyze()






