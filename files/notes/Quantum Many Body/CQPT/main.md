---
title: "连续量子相变理论 / Continuous Quantum Phase Transition"
date: 2026-10-10
cover: cover.jpeg
summary: "还请，莫向外求。"
---

本文主要参考Subir Sachdev 的Quantum Phase Transitions，以及他关于连续量子相变的经典综述 [​Continuous quantum phase transitions](https://link.aps.org/doi/10.1103/RevModPhys.69.315) 

以及PI的[​Quamtum Matter](https://pirsa.org/c25062) 课程，听了前几节感觉挺有收获的，推荐一下

真心喜欢这些理论漂亮的工作，在一众待读列表里简直是清流

---

## 1 / 经典相变理论

以2D Ising为例，经典的相变理论无外乎朗道和平均场近似，最简单的铁磁 Ising 模型的哈密顿量为

$$
H=-J\sum_{\langle i,j\rangle}s_is_j-h\sum_i s_i
$$

随着温度变换会出现有序到无序的转变，具体来说我们可以用平均磁化强度 $m$ 来描述这种无序的程度

$$
m=\frac{1}{N}\sum_i\langle s_i\rangle
$$

朗道的想法是用惊人的注意力注意到既然相变可以用这玩意描述，就把自由能写成它的幂级数展开

$$
f(m,T)=f_0(T)+a_1m+a_2m^2+a_3m^3+a_4m^4+\cdots
$$

这个逆天操作的槽点实在太多而且肯定严格意义上是错的，但不妨碍它能得出一些有趣的结果，所以不妨先看下去，首先不难发现体系满足无磁场下的 $Z_2$ 对称性

$$
H(\{s_i\})=H(\{-s_i\})
$$

所以应该有

$$
f(m,T)=f(-m,T)
$$

这要求自由能只能包含 $m$ 的偶数次幂，在最简单的连续相变情形中，可以忽略六次及更高次项，并引入外磁场的耦合项，有

$$
f(m,T,h)=f_0(T)+\frac{r(T)}{2}m^2+\frac{u}{4}m^4-hm
$$

其中

$$
r(T)=A(T-T_c),\qquad A>0,\quad u>0
$$

这就是用于描述 Ising 相变的四次朗道自由能。平衡态对应于自由能的最小值。对应着求解

$$
\frac{\partial f}{\partial m}=0 \Rightarrow rm+um^3-h=0
$$

$$
m=0
$$

$$
m=\pm\sqrt{-\frac{r}{u}}
$$

即无外磁场下存在两类驻点，后一组解仅在 $r<0$ 时存在。换句话说就是在 $T=T_c$ 处发生相变。注意到

$$
m_{\mathrm{eq}}=\pm\sqrt{\frac{A(T_c-T)}{u}}
$$

因此有幂律关系

$$
m_{\mathrm{sp}}\propto(T_c-T)^{1/2}
$$

说明朗道理论预言磁化强度在接近临界温度时连续趋近于零，这也就是临界相变的特征。当然，由于这个推导太过粗糙，所以求出来的幂律系数也就图一乐。不过虽然自由能的幂律展开式看着很扯淡，但其实其还是有一定道理的，其对应的是平均场近似的结果。

设每个格点有 $z$ 个最近邻自旋，平均磁化强度为 $m$。在平均场近似中，将相邻自旋的相关性近似为

$$
\langle s_i s_j\rangle\approx\langle s_i\rangle\langle s_j\rangle=m^2
$$

那么每个自旋的平均能量为

$$
e(m)=-\frac{zJ}{2}m^2-hm
$$

设向上和向下的自旋分别占比

$$
p_+=\frac{1+m}{2},\qquad p_-=\frac{1-m}{2}
$$

在独立自旋近似下，每个自旋的熵为

$$
s(m)=-k_B\left[p_+\ln p_++p_-\ln p_-\right]
$$

因此自由能

$$
f(m,T)=e(m)-Ts(m)
$$

可以写成

$$
\begin{aligned}
f(m,T,h)={}&-\frac{zJ}{2}m^2-hm\\
&+k_BT\left[\frac{1+m}{2}\ln\frac{1+m}{2}+\frac{1-m}{2}\ln\frac{1-m}{2}\right].
\end{aligned}
$$

简单的泰勒展开可以得到

$$
f(m,T,h)=-k_BT\ln2+\frac{k_BT-zJ}{2}m^2+\frac{k_BT}{12}m^4+\frac{k_BT}{30}m^6+\cdots-hm.
$$

当二次项系数为零时，有

$$
k_BT_c^{\mathrm{MF}}=zJ
$$

这就是平均场理论预言的临界温度。二维对应 $z=4$，也即

$$
k_BT_c^{\mathrm{MF}}=4J
$$

而精确解给出

$$
k_BT_c=\frac{2J}{\ln(1+\sqrt2)}\approx2.269J
$$

差距还是不小，可见平均场实在是过于粗糙的理论。更合理的平均场或许是不对全局求平均，而是求局域的平均，把序参量从单一的参数变成位置的函数

$$
m\longrightarrow m(\mathbf x)
$$

由此可得推广的Landau–Ginzburg理论。其自由能对应的变成了泛函

$$
F[m]=\int d^d x\left[\frac r2m(\mathbf x)^2+\frac u4m(\mathbf x)^4+\frac{\kappa}{2}|\nabla m(\mathbf x)|^2-hm(\mathbf x)\right]
$$

这里 $d$ 是空间维数。会发现这里多了一个修正的梯度项 $\frac\kappa2|\nabla m|^2$，用于一定程度上描述局域磁化在空间中变化所需的自由能代价。但很遗憾这依然是经验公式，并不意味这自由能真就完全写成这个样子。但引入空间变化的好处就在于我们可以在其之上研究一下体系的关联长度。这里定义自旋关联函数来描述位置 $\mathbf x$ 和 $\mathbf y$ 的磁化涨落之间有多大关联。

$$
G(\mathbf x-\mathbf y)=\langle m(\mathbf x)m(\mathbf y)\rangle-\langle m(\mathbf x)\rangle\langle m(\mathbf y)\rangle
$$

进行傅里叶变换：

$$
m(\mathbf x)=\int\frac{d^2q}{(2\pi)^2}m_{\mathbf q}e^{i\mathbf q\cdot\mathbf x}
$$

利用

$$
\nabla m\longleftrightarrow i\mathbf q m_{\mathbf q}
$$

忽略四次项，得到

$$
F_G=\frac12\int\frac{d^2q}{(2\pi)^2}(r+\kappa q^2)|m_{\mathbf q}|^2
$$

利用高斯积分，可以得到动量空间关联函数：

$$
G(\mathbf q)=\frac{k_BT}{r+\kappa q^2}=\frac{k_BT/\kappa}{q^2+\xi^{-2}},
$$

其中

$$
\xi=\sqrt{\frac{\kappa}{r}}
$$

即为特征长度尺度，在平均场近似下

$$
r\propto T-T_c^{\mathrm{MF}}
$$

于是

$$
\xi\propto(T-T_c^{\mathrm{MF}})^{-1/2}
$$

同样的，这里的临界指数也就图一乐。

## 2 / 重整化群＆普适类

虽然和接下来要讲的量子相变没啥关系 ，但为了严谨还是写一下处理经典相变相对更准确的方法，大名鼎鼎的RG重整化群理论。

## 3 / 横场Ising＆量子相变
