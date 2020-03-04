# 导入所需的库
import sys
import numpy as np
import scipy.constants as C
import argparse
import pandas as pd

# 定义全局变量

R = C.R

prompt = ">>>"
# 从交互式对话框读取信息
def read_chat():
    NumberAtom = int(input("请输入晶格中不同原子位置的种类个数。%s"%prompt)) 
    Elements = []
    for x in range(NumberAtom):
        MatrixElements = []
        NumberElement = int(input("请输入第%d种位置中元素种类个数。 %s"%(x+1,prompt)))
        for y in range(NumberElement):    
            NameElements = str(input("请输入第%d个位置第%d种元素的元素符号。 %s"%(x+1,y+1,prompt)))
            ElementSubscript = float(input("请输入第%d个位置第%d种元素的理论下标量。 %s"%(x+1,y+1,prompt)))
            MatrixElements.append([NameElements,ElementSubscript])
        ElementMole = np.sum(np.array([i[1] for i in MatrixElements]))                      

        Matrix = [x,ElementMole,MatrixElements]
        Elements.append(Matrix)
    print(Elements)

    return Elements

# 从文件中读取信息
def read_file():
    data = pd.read_table("mat.in",sep="\s+",header=None,comment="#")
    length = len(data)
    Elements = []
    if length%2 == 0:
        for i in range(int(length/2)):
            Matrix = []
            ElementsSymbol = data.iloc[i*2]
            ElementsMole = data.iloc[i*2+1]
            ElementsSymbol=ElementsSymbol.dropna(axis=0,how="any")
            ElementsMole = ElementsMole.dropna(axis=0,how="any")
            if len(ElementsSymbol) != len(ElementsMole):
                print("file error，check it again")
                sys.exit(1)
            MatrixElements=np.array([np.array(ElementsSymbol),np.array(ElementsMole,dtype=np.float)]).T
            TotMole = np.sum(np.array(ElementsMole,dtype=float))
            MatrixElements = MatrixElements.tolist()
            Matrix = [i,TotMole,MatrixElements]
            Elements.append(Matrix)
    else:
        print("file error，check it again")
        sys.exit(1)
    print(Elements)
    return Elements
        
        
#计算构型熵
def configurational_entropy(data):
    Elements =np.array(data)
    ListSum = []
    for i in Elements:
        ElementMoleInfo = i[2]
        MoleInfo = np.array(ElementMoleInfo).T[1]
        MoleInfo = MoleInfo.astype(np.float)
        SumA = i[1]*np.sum([j*np.log(j) for j in MoleInfo])
        ListSum.append(SumA)
    TotSum = np.sum(ListSum)
    EntropyValue = -1*R*TotSum
    
    return EntropyValue

# 输出到文件
def file_mode():
    print("*"*40+"文件读取中"+"*"*40)
    print("")   
    print(".")
    print(".")
    print(".")
    Elements = read_file()
    print("*"*40+"结果输出"+"*"*40)
    EntropyValue = configurational_entropy(Elements)
    
    print("原始数据为:",Elements)
    print("构型熵为: %f"%EntropyValue)
    data = pd.read_table("mat.in",sep="\s+",header=None,comment="#")
    
    data.to_csv("mat.out",sep="\t",header=None,index=False,mode="w")
    with open("mat.out","a+") as f:
        f.write("\n")
        f.write("#configurational_entropy\n")
        f.write(str(EntropyValue))
    print("保存至文件中mat.out")
    
    ExitInput=input("按任意键退出")


#输出到屏幕    
def interactive_mode():
    print("*"*40+"参数输入"+"*"*40)
    print("")    
    Elements = read_chat()
    
    print("")
    print("")
    print("")
    print("*"*40+"结果输出"+"*"*40)
    EntropyValue = configurational_entropy(Elements)
    
    #输出构型熵结果
    print("")
    print("原始数据为:",Elements)
    print("构型熵为: %f"%EntropyValue)
    ExitInput=input("按任意键退出")
    
# 主程序    
def main():
    parser = argparse.ArgumentParser(prog="ConfigEntropy")
    parser.add_argument("-v","--version",action="version",version="%(prog)s 0.1")
    parser.add_argument("-r","--read",help="reading 'mat.in'file and runing the code",action="store_true")
    
    parser.add_argument("-i","--interactive",help="run interactive mode (default)",action="store_true")
    
    args = parser.parse_args()
    if args.read:
        file_mode()
    elif args.interactive:
        interactive_mode()
    else:
        interactive_mode()
                    
if __name__ == "__main__":
    main()


