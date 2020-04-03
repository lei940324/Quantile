# 分位数Granger因果检验实现原理

## 各变量含义

待估计方程：
$$
Q_{Y_{t}}\left[\tau | Z_{t-1}\right]=a(\tau)+Y_{t-1, p}^{\prime} \alpha(\tau)+X_{t-1, q}^{\prime} \beta(\tau)=Z_{t-1}^{\prime} \theta(\tau)
$$
其中，$$a(\tau)$$为截距项，$\alpha(\tau)$和$\beta(\tau)$为回归系数列向量；$\theta(\tau)$为回归系数向量，
$$
a(\tau)=\left[alpha(\tau), \alpha(\tau)^{\prime}, \beta(\tau)^{\prime}\right]^{\prime}​
$$

$$
\quad Y_{t-1, p}^{\prime}=\left(Y_{t-1}, \cdots, Y_{t-p}\right)
$$

$$
\quad X_{t-1, q}^{\prime}=\left(X_{t-1}, \cdots, X_{t-q}\right)
$$

$$
Z_{t-1}^{\prime}=\left(Y_{t-1, p}^{\prime}, X_{t-1, q}^{\prime}\right)
$$

Wald检验量为：$\mathrm{W}_{T}(\tau)=T \frac{\hat{\beta}(\tau)^{\prime} \hat{\Sigma}(\tau)^{-1} \hat{\beta}(\tau)}{\tau(1-\tau)}$

Sup-Wald检验量为：$$\sup W_{T}=\sup _{i=1, \cdots, n} W_{T\left(\tau_{i}\right)} $$

> Python在进行分位数回归时，方差默认为核估计

## 分位数方差核密度估计原理（基于Eviews帮助文件）

**独立但不同分布假设下的参数渐近分布：**

当分位数密度函数独立但不同分布即与解释变量X相关时，$$\sqrt{T}(\hat{\beta}(\tau)-\beta(\tau))$$的渐近分布服从Huber sandwich形式：

$$
\sqrt{T}\left(\hat{\beta}_{(\tau)}-\beta_{(\tau)}\right){\sim} N\left(0, \tau(1-\tau) H(\tau)^{-1} J H(\tau)^{-1}\right)​
$$
其中$T$为样本容量，$\tau$为分位点，$\hat{\beta}_{(\tau)}$为$\tau$分位点下回归系数估计量，$N$为正态分布，$X_{i}$为解释变量矩阵；
$$
J=\lim _{n \rightarrow \infty}\left(\sum_{i} \frac{X_{i} X_{i}^{\prime}}{T}\right)=\lim _{n \rightarrow \infty}\left(\frac{X X}{T}\right)​
$$

$$
H(\tau)=\lim _{T \rightarrow \infty}\left(\sum_{i} X_{i} X_{i}^{\prime} f_{i}\left(q_{i}(\tau)\right) / T\right)
$$

$f_{i}\left(q_{i}(\tau)\right)$是个体$i$在$\tau$分位点上的条件密度函数。使用核密度进行估计：     
$$
\hat{H}(\tau)=(1 / T) \sum_{i=1}^{T} c_{T}^{-1} K\left(\hat{u}_{(\tau) t} / c_{T}\right) X_{i} X_{i}^{\prime}
$$
其中 $\hat{\mathcal{U}}_{(\tau) i}$表示分位数回归的残差；$c_T$为带宽，估计原理见下文；表示$\kappa$核密度函数。EViews中可以选择的核密度函数有Epanechnikov核函数（默认）、均匀 (Uniform) 核函数、三角(Triangular)核函数、二权(Biweight)核函数、三权(Triweight)核函数、正态(Normal)核函数、余弦(Cosinus)核函数，具体函数形式见图。

<img src="https://raw.githubusercontent.com/lei940324/picture/master/typora202003/31/180818-928273.png" alt="image-20200331180810735" style="zoom:67%;" />  

![image-20200331181950284](https://raw.githubusercontent.com/lei940324/picture/master/typora202003/31/181951-533816.png)

$c_T$的估计原理：$c_{T}=\kappa\left(\Phi^{-1}\left(\tau+h_{n}\right)-\Phi^{-1}\left(\tau-h_{n}\right)\right)$     

其中$\kappa=\min (s, I Q R / 1.34)$,$IQR$为四分位距，$\mathrm{I} Q \mathrm{R}=Q_{3}-Q_{1}$;$s$为残差的标准差；$h_n$是Siddiqui带宽，
$$
h_{n}=T^{-1 / 3} Z_{\alpha}^{2 / 3}\left(\frac{1.5\left(\varphi\left(\Phi^{-1}(\tau)\right)\right)^{2}}{2\left(\Phi^{-1}(\tau)\right)^{2}+1}\right)^{1 / 3}
$$
$\Phi$表示正态分布的积累分布函数，$\Phi^{-1}$表示正态分布的逆函数，$\varphi$表示正态分布的密度函数，$Z_{\alpha}=\Phi^{-1}(1-\alpha / 2)$为选择的显著性水平$\alpha$对应的$Z$值。

> 文中只列出一种方差的估计原理，更多内容详见Eviews 8帮助文件