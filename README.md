# Introduction

## 功能介绍

实现分位数格兰杰(Granger)因果检验，计算各分位区间Sup-Wald统计量。

更新后，增加分位数VAR与脉冲响应函数计算。

## 代码实现原理

* 使用`pyqt5`生成GUI界面
* 使用`statsmodels`进行分位数回归
* 使用`pandas`将结果保存在excel文件

# Requirements

* python 3.6+ 
* 需要安装第三方库：`pandas`、`scipy`、`numpy`、`statsmodels`、`pyqt5`；推荐使用`anaconda`

# Display

## 主窗口界面

<img src="https://raw.githubusercontent.com/lei940324/picture/master/typora202004/03/224113-33109.png" alt="image-20200403224111470" style="zoom:50%;" />

主要包括：

- **工具栏**：

  * **导入数据**：点击该按钮，选择路径导入数据，如没有导入数据，默认导入测试数据
  * **开始运行**：点击后进行分位数Granger因果检验，计算Sup-wald统计量
  * **终止运行**：点击后终止程序
  * **查看数据**：点击查看导入数据
  * **初始化**：点击后初始化各参数设定
  * **QVAR估计**：点击后进行QVAR模型参数设定

- **区间设定**：区间**起点、中点、个数**设定以及**生成区间**按钮

  > **注意**：个数是点的个数，比如设定17个，则会生成16个分位区间

  **例子：**

  起点=0.1，终点=0.9，个数=2，则会生成区间：[0.1, 0.9]

  起点=0.1，终点=0.9，个数=3，则会生成区间：[0.1, 0.5]、[0.5, 0.9]

- **参数设定**

  * **日期**：勾选表示第一列为日期序列，在进行计算wald统计量时会将其删除；若取消勾选，则不会删除第一列数据

  * **模式设定**：代表循环模式，默认模式为**单因素对各市场**

    >  **注意：数据要根据模式进行相应的排序**

    假定p=1，q=2，估计方程形式则为：Y=c<sub>1</sub>+c<sub>2</sub>Y<sub>-1</sub>+c<sub>3</sub>X<sub>-1</sub>+c<sub>4</sub>X<sub>-2</sub>

    |      模式      |                           内容说明                           |                      数据排序                      |                         计算规则描述                         |
    | :------------: | :----------------------------------------------------------: | :------------------------------------------------: | :----------------------------------------------------------: |
    | 单因素对各市场 | 研究单一因素对各市场的因果关系，比如房价对股票，汇率市场的因果关系 | data=[X,Y<sub>1</sub>,Y<sub>2</sub>,Y<sub>3</sub>] | X对Y<sub>1</sub>回归；X对Y<sub>2</sub>回归；X对Y<sub>3</sub>回归 |
    |    相互影响    | 研究两因素之间的因果关系，比如房价与股票，汇率市场的相互因果关系 | data=[X,Y<sub>1</sub>,Y<sub>2</sub>,Y<sub>3</sub>] | X对Y<sub>1</sub>回归；X对Y<sub>2</sub>回归；X对Y<sub>3</sub>回归；Y<sub>1</sub>对X回归；Y<sub>1</sub>对Y<sub>2</sub>回归;Y<sub>1</sub>对Y<sub>3</sub>回归;......... |
    | 多因素对单市场 | 研究多因素对单个市场的因果关系，比如各情绪对汇率市场的因果关系 | data=[X<sub>1</sub>,X<sub>2</sub>,X<sub>3</sub>,Y] | X<sub>1</sub>对Y回归，X<sub>2</sub>对Y回归；X<sub>3</sub>对Y回归 |

  * **信息准则**：表示确定最优滞后阶数所选用的信息准则，包括AIC或BIC准则

    AIC(p, q) = lnS(θ) + (p+q+1)/T

    BIC(p, q) = lnS(θ) + (p+q+1)×lnT/(2T)

    其中S(θ)表示分位数非对称绝对值残差和，T为样本容量，p,q均为滞后阶数。

  * **滞后估计数**：计算最优滞后阶数时，需要分区间计算AIC/BIC值，选取该区间最小AIC/BIC值所对应的滞后阶数，则为最优滞后阶数。该参数是设定在整个分位区间选择计算的分位点个数，默认选取30个点

  * **最大阶数**：表示选取的最大滞后阶数，默认选取5阶

  - **wald估计数**：计算wald统计量时，在分位区间选择计算的分位点个数，默认选取1000个点
  - **有效数字**：表示保留的小数点位数，默认保留三位小数
  - **输出日志**：勾选后输出**运行细节.txt**文件，默认勾选

- **估计信息显示**：展示运行信息

## 

<img src="https://raw.githubusercontent.com/lei940324/picture/master/typora202004/03/224150-525667.png" alt="image-20200403224146935" style="zoom:50%;" />

# Usage

**第一步**：在当前路径下的命令行输入：

```shell
python main.py
```

> 提示：在当前文件夹中，右键点击cmd或者shell打开命令行

**第二步**：点击**导入数据**按钮

输入成功的话，会有导入成功的提示

**第三步**：设定各参数

**第四步**：点击**开始运行**按钮，等待程序运行结束，结果保存在**运行结果**文件夹下的**Granger.xlsx**文件内

# 项目目录

```
<<<<<<< HEAD
|-- Quantile_Ganger
    |-- beauty_UI.py             // 美化GUI界面代码    
    |-- func.py                  // 主函数代码，定义分位数Granger因果检验计算    
    |-- main.py                  // 构建GUI界面    
    |-- MainWindow.ui            // 使用Qt Creator生成的GUI界面代码    
    |-- README.md                // 说明文件   
    |-- res_rc.py                // 资源文件转译   
    |-- uic.bat                  // 转化代码   
    |-- ui_MainWindow.py         // 使用Qt Creator生成的GUI界面代码，并转化为py文件  
    |-- data
    |   |-- output.xlsx          // 测试产生的结果文件   
    |   |-- Sup_wald_lag.xlsx    // 检验Sup_wald显著性文件   
    |   |-- 测试数据.xlsx         // 可以使用该文件进行测试，查看结果  
    |   |-- 运行细节.txt          // 测试日志  
    |-- GUI                      // 使用Qt Creator 建立主窗口项目产生的文件   
    |-- image                    // 项目中用的图片   
    |-- 公式原理              
```

> 代码主体为**main.py**与**func.py**文件

# 估计原理

## 使用函数介绍

使用`statsmodels`库进行分位数回归命令：

1)  使用R型公式来拟合模型

| **formula** | **说明**                               | **示例**             |
| ----------- | -------------------------------------- | -------------------- |
| ~           | 分隔符，左边为响应变量，右边为解释变量 | y ~ x                |
| +           | 添加变量                               | y ~ x1 + x2          |
| -           | 移除变量                               | y ~  x - 1(移除截距) |

2)  参数命令

| **属性**   | **说明**       | **方法**             | **说明**       |
| ---------- | -------------- | -------------------- | -------------- |
| res.params | 获取估计参数值 | res.summary()        | 展示估计结果   |
| res.bse    | 获取标准差     | res.cov_params()     | 获取协方差矩阵 |
| res.resid  | 获取残差       | res.f_test("x2 = 0") | Wald检验       |



## 分位数Granger因果检验实现原理

由于github很难查看latex格式的公式，可以点击 [分位数Granger因果检验实现原理.pdf](https://github.com/lei940324/Quantile_Granger/blob/master/%E5%85%AC%E5%BC%8F%E5%8E%9F%E7%90%86/%E5%88%86%E4%BD%8D%E6%95%B0Granger%E5%9B%A0%E6%9E%9C%E6%A3%80%E9%AA%8C%E5%AE%9E%E7%8E%B0%E5%8E%9F%E7%90%86.pdf) 进行查看

# Development Tool

- **Qt Creator**：GUI界面可视化

  <img src="https://raw.githubusercontent.com/lei940324/picture/master/typora202003/31/182029-164220.png" alt="image-20200331182028292" style="zoom:50%;" />

- **PyCharm**：代码编辑器

  ![image-20200331182339215](https://raw.githubusercontent.com/lei940324/picture/master/typora202003/31/182340-937174.png)



# reference

* **书籍：**
  * 《Python Qt GUI与数据可视化编程》
  * 《陈强高级计量经济学》
* **文献：**
  * Koenker & Machado1999 Inference QuantileReg
  * Asymmetric Least Squares Estimation and Testing
  * Tests-for-Parameter-Instability-and-Structural-Change-With-Unknown-Change-Point
  * 房地产价格与汇率的联动关系研究———基于分位数 Granger 因果检验法
  * 基于分位数Granger因果的网络情绪与股市收益关系研究
* **其他:**
  * Eviews 8帮助文件
  * [张晓峒分位数回归讲义](https://github.com/lei940324/Quantile_Granger/blob/master/%E5%85%AC%E5%BC%8F%E5%8E%9F%E7%90%86/%E5%BC%A0%E6%99%93%E5%B3%92%E5%88%86%E4%BD%8D%E6%95%B0%E5%9B%9E%E5%BD%92%E8%AE%B2%E4%B9%89.doc)