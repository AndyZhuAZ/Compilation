testlist=['E -> E + T', 'E -> T','ε']
inputlist=['A -> A a1 | A a2 | b1 | b2']


def dell(self):
    if '|' in i.split(' '):
        j=i.count('|')
        newlist_in_preline = i.split(' ')
        a = newlist_in_preline.index('|')
        print(a)
        # print(j)
        new.extend(newlist_in_preline)
    else:
        new.extend(i.split(' '))
    new.append('￥')

def rpartd(rpart,lpart):
    rpart.insert(0,'|')
    print(rpart)
    if rpart[rpart.index(lpart) - 1] is '|':
        a = rpart.index(lpart)
        # print(a)
        new_rpart = rpart[a+1:].copy()
        # print(new_rpart)
        b = new_rpart.index('|')
        # print(b)
        print(rpart[:a-1])
        # print(new_rpart[b+1:])
        # print(rpart[:a]+new_rpart[b+1:])
        return rpartd(rpart[:a-1]+new_rpart[b+1:],lpart)
    else:
        rpart.remove('|')
        return rpart


if __name__ == '__main__':
    new = []
    # for i in inputlist:
    #     if '|' in i.split(' '):
    #         j = i.count('|')
    #         list_in_preline = i.split(' ')
    #         a = list_in_preline.index('|')
    #         print(a)
    #         outlist = list_in_preline[:a]
    #         print(outlist)
    #         newlist = list_in_preline[:list_in_preline.index('->') + 1]
    #         newlist.extend(list_in_preline[a + 1:])
    #         lpart = list_in_preline[:list_in_preline.index('->')]
    #         rpart = list_in_preline[list_in_preline.index('->') + 1:]
    #         rpart.reverse()
    #         rpart.append('|')
    #         rpart.reverse()
    #
    #         # rpart.extend()
    #         print(lpart)
    #         print(rpartd(rpart,lpart))
    #         # print(j)
    #         new.extend(newlist)
    #     else:
    #         new.extend(i.split(' '))
    #     new.append('￥')
    # print(new)
    p= rpartd(['c', '|', 'A', 'a1', '|', 'A', 'a2', '|', 'b1', '|', 'b2'],'A')
    print(p.remove('|'))

