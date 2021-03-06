# Compilation-Course-Design
## LL（1）语法分析器的设计与开发
### 一、设计内容及要求
  (1) 基于PL/0语言，通过编程判断该文法是否为LL(1)文法 
  (2) 计算出文法的First() 、Follow()
  (3) 构造相应文法的预测分析表
  (4) 对某个输入句子进行语法分析
要求：所有实现内容要通过编程的方式自动进行计算、分析，对语法分析的结果能够给出正确或错误，如果存在语法错误，要明确错误的类型和错误的位置，并给出修改建议。
### 二、实现原理
#### 1．LL(1)文法
LL(1)文法是一类可以进行确定的自顶向下语法分析的文法。就是要求描述语言的文法是无左递归的和无回溯的。根据LL(1)文法的定义，对于同一非终结符A的任意两个产生式A:=a和A:=b，都要满足：SELECT(A：=a )∩SELECT(A:=b)=Ø。
#####（1）文法的左递归
当一个文法是左递归文法时，采用自顶向下分析法会使分析过程进入无穷循环之中。所以采用自顶向下语法分析需要消除文法的左递归性。文法的左递归是指若文法中对任一非终结符A有推导AÞA…，则称该文法是左递归的。
左递归又可以分为直接左递归和间接左递归。
● 直接左递归
若文法中的某一产生式形如A→Aα，α∈V*，则称该文法是直接左递归的。
消除直接左递归的方法：
设有产生式是关于非终结符A的直接左递归：A→Aα|β  （α,β∈V*，且β不以A开头）
对A引入一个新的非终结符A′，把上式改写为：
A →βA′   
A′→αA′|ε 
● 间接左递归
若文法中存在某一非终结符A，使得AÞA…至少需要两步推导，则称该文法是间接左递归的。
消除间接左递归的方法：
【方法一】采用代入法把间接左递归变成直接左递归。
   【方法二】直接改写文法：设有文法G10[S]：
    S→Aα|β    ⑴
    A→Sγ       ⑵
因为SÞAαÞSγα，所以S是一个间接递归的非终结符。为了消除这种间接左递归，将⑵式代入⑴式，即可得到与原文法等价的文法（可以证明）：
    S→Sγα|β  ⑶
⑶式是直接左递归的，可以采用前面介绍的消除直接左递归的方法，对文法进行改写后可得文法：S→βS′
S′→γαS′|ε

#### 2. 计算First集
(1) 若X∈VT ，则First(X)={X}
(2) 若X∈VN ，且有产生式X→a…, a∈VT则First(X)={X}
(3) 若X∈VN ，且有产生式X→ε,则First(X)={X}
(4) 若X，Y1 ，Y2 ，…，Yn 都∈VN，而由产生式X→Y1 Y2 …Yn 。当Y1 ，Y2 ，…，Yi-1都能推导出ε时，（其中1≤i≤n），则First(Y1)-{ε}, First(Y2)-{ε},…, First(Yi)都包含在First(X)中
(5)当(4)中所有Yi都能推导出ε，（i=1，2，…，n），则First(X)=First(Y1)∪First(Y2)∪…First(Yn)∪{ε}
反复使用上述步骤直到每个符合的First集合不再增大为止。

#### 3. 计算Follow集
对文法中的每个A∈VN，计算Follw(A)：
(1) 设S为文法的开始符合，把{#}加入Follow(S)中；
(2) 若A→αBβ是一个产生式，则把First(β)的非空元素加入Follow(B)中，如果β能推导出ε，则把Follow(A)也加入(B)中；
(3) 反复使用以上步骤直到每个非终结符号的Follow集不再增大为止。
#### 4. 预测分析方法
预测分析方法是自顶向下分析的另一种方法，一个预测分析器是由三个部分组成：预测分析程序；先进后出栈；预测分析表。
