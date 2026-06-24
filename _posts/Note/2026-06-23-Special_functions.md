---
title: "量子力学の特殊函数"
date: 2026-06-23 12:00
categories:
  - Note
tags:
  - Theoretical Physics
  - Mathematical Methods
cover: /assets/images/Note/Special Functions/cover.jpg
excerpt: "偷懒漏掉的数理方法总会在某一天找上门来"
---

做一个比较实用向的特殊函数总结，主要针对量子力学的学习。

## 1. Bessel函数

Bessel方程的形式如下：$$x^2 \frac{d^2y}{dx^2} + x \frac{dy}{dx} + (x^2 - n^2)y = 0$$

其有两个线性独立的基底解：

- 一类Bessel函数 $J_n(x)$：在 $x=0$ 处是收敛且有界的。

- 二类Bessel函数（Neumann函数） $Y_n(x)$：在 $x=0$ 处是发散（无穷大）的。

![](/assets/images/Note/Special%20Functions/1.png)

![](/assets/images/Note/Special%20Functions/2.png)

Bessel方程一般出现在柱对称性中，例如二维圆形边界的薄膜波动方程

$$\nabla^2 u = \frac{1}{v^2} \frac{\partial^2 u}{\partial t^2}$$

$$\frac{\partial^2 u}{\partial r^2} + \frac{1}{r} \frac{\partial u}{\partial r} + \frac{1}{r^2} \frac{\partial^2 u}{\partial \theta^2} = \frac{1}{v^2} \frac{\partial^2 u}{\partial t^2}$$

分离变量

$$u(r, \theta, t) = R(r) \Theta(\theta) T(t)$$

一通操作后发现径向部分满足

$$\frac{r^2}{R} \frac{d^2 R}{dr^2} + \frac{r}{R} \frac{dR}{dr} + k^2 r^2 = n^2$$

$$r^2 \frac{d^2 R}{dr^2} + r \frac{dR}{dr} + (k^2 r^2 - n^2)R = 0$$

考虑到薄膜内部振幅收敛，故故径向解为$J_n(kr)$

远场渐进展开

$$J_n(x) \approx \sqrt{\frac{2}{\pi x}} \cos\left(x - \frac{n\pi}{2} - \frac{\pi}{4}\right)$$

$$Y_n(x) \approx \sqrt{\frac{2}{\pi x}} \sin\left(x - \frac{n\pi}{2} - \frac{\pi}{4}\right)$$

可以注意到在远场，$J_n(x)$ 和 $Y_n(x)$ 之间刚好保持 $\pi/2$ 的相位差，就像常规的余弦和正弦函数一样。Bessel函数本身没有周期性，但随着零点序号的增加会越来越有“周期性”

近场渐进展开

当 $n = 0$ 时：

$$J_0(x) \approx 1 - \frac{x^2}{4}$$

$$Y_0(x) \approx \frac{2}{\pi} \ln\left(\frac{x}{2}\right)$$

当 $n > 0$ 时：

$$J_n(x) \approx \frac{1}{\Gamma(n+1)} \left(\frac{x}{2}\right)^n$$

 $$Y_n(x) \approx -\frac{\Gamma(n)}{\pi} \left(\frac{2}{x}\right)^n$$

普通的三角函数是在一个周期区间（如 $[0, 2\pi]$）内正交。而Bessel函数的正交性则稍有不同，它通常定义在一个固定的空间区间 $[0, R]$ 上（$R$ 可以看作是圆柱或圆盘的半径），并且需要引入一个权重因子 $x$。

$$\int_{0}^{R} x \, J_n\left(\frac{\alpha_{n,m}}{R}x\right) J_n\left(\frac{\alpha_{n,k}}{R}x\right) dx = 0 \quad (\text{当 } m \neq k)$$

以及自正交归一化

$$\int_{0}^{R} x \, \left[J_n\left(\frac{\alpha_{n,m}}{R}x\right)\right]^2 dx = \frac{R^2}{2} [J_{n+1}(\alpha_{n,m})]^2$$

于是对于半径边界约束下标准模态的组合

$$f(x) = \sum_{m=1}^{\infty} c_m J_n\left(\frac{\alpha_{n,m}}{R}x\right)$$

有

$$c_m = \frac{2}{R^2 [J_{n+1}(\alpha_{n,m})]^2} \int_{0}^{R} x \, f(x) \, J_n\left(\frac{\alpha_{n,m}}{R}x\right) dx$$

当然也有自由空间的形式

$$\int_{0}^{\infty} r \, J_n(kr) J_n(k'r) \, dr = \frac{1}{k} \delta(k - k')$$

其对应Hankle积分变换

$$\mathcal{H}_n\{f(r)\} = F_n(k) = \int_{0}^{\infty} f(r) J_n(kr) r \, dr$$

$$\mathcal{H}_n^{-1}\{F_n(k)\} = f(r) = \int_{0}^{\infty} F_n(k) J_n(kr) k \, dk$$

二阶拉普拉斯算符在Bessel基底下就是本征算子

$$\mathcal{H}_n \left\{ \frac{d^2 f}{dr^2} + \frac{1}{r}\frac{df}{dr} - \frac{n^2}{r^2}f \right\} = -k^2 F_n(k)$$

## 2. Legendre多项式

Legendre方程形式如下，$\nu$ 为方程参数

$$(1 - x^2) \frac{d^2y}{dx^2} - 2x \frac{dy}{dx} + \nu(\nu+1)y = 0$$

同样的，也可以写出其形式通解

$$y(x) = C_1 P_\nu(x) + C_2 Q_\nu(x)$$

这两个基解都非常难看，当参数 $\nu$ 恰好为非负整数 $n$（$n = 0, 1, 2, \dots$）时，情况就会稍好一些。此时$P_n(x)$是一个有限项的多项式，$Q_n(x)$可以写成

$$Q_n(x) = \frac{1}{2} P_n(x) \ln\left(\frac{1+x}{1-x}\right) - W_{n-1}(x)$$

其中 $W_{n-1}(x)$ 是一个 $n-1$ 次的普通多项式。
由于前面多了一个 $\ln\left(\frac{1+x}{1-x}\right)$ 项，当 $x \to \pm 1$ 时， $Q_n(x)$ 依然铁定发散。

其实如果 $l$ 不是整数，$P_n(x)$是一个无限项的幂级数，而这个级数在 $x = \pm 1$ 处的行为等价于调和级数，同样也是发散的。

实际使用到Legendre多项式的时候往往附带 $x=\pm 1$ 时收敛的边界条件，这意味着$C_2$肯定是0。$P_n(x)$退化成收敛的有限项。所以我们说的Legendre多项式其实就是$P_n(x)$

列举前几阶的形式

$P_0(x) = 1$

$P_1(x) = x$

$P_2(x) = \frac{1}{2}(3x^2 - 1)$

$P_3(x) = \frac{1}{2}(5x^3 - 3x)$

$P_4(x) = \frac{1}{8}(35x^4 - 30x^2 + 3)$

![](/assets/images/Note/Special%20Functions/3.png)

不难发现，$P_n(x)$具有确定的奇偶性

$$P_n(-x) = (-1)^n P_n(x)$$

另外，当且仅当 $\nu$ 为整数时，函数群 $\{P_0(x), P_1(x), P_2(x), \dots\}$ 才能在区间 $[-1, 1]$ 上构成一组带权重的正交完备集

$$\int_{-1}^{1} P_n(x) P_m(x) \, dx = \frac{2}{2n+1} \delta_{nm}$$

作为Legendre方程的延申，有连带Legendre方程

$$(1 - x^2) \frac{d^2y}{dx^2} - 2x \frac{dy}{dx} + \left[ l(l+1) - \frac{m^2}{1-x^2} \right] y = 0$$

在同样的边界收敛条件约束下，其解为连带勒让德多项式 $P_l^m(x)$

$$P_l^m(x) = (-1)^m (1 - x^2)^{m/2} \frac{d^m}{dx^m} P_l(x) \quad (\text{当 } m \ge 0)$$

有扩展的正交性

$$\int_{-1}^{1} P_l^m(x) P_k^m(x) \, dx = \frac{2}{2l+1} \frac{(l+m)!}{(l-m)!} \delta_{lk}$$

两个有趣的问题。

第一个问题，在常微分方程中，我们知道很多时候物理上合理的边界收敛性决定了参数只能取分立值，而真实的边界条件确定了真正的待定系数。

但是前面的两个例子让我们看到边界收敛性本身就是可以确定待定系数的，例如第二类Bessel函数和第二类Legendre函数。那么只剩下一个待定系数的通解能否符合边界条件的两个方程呢。

其实答案也并不让人意外，那就是收敛本身就算是一种边界条件了，当你确认其收敛时，本身就加了很大一层约束。就例如非0阶的贝塞尔方程，如果确认其原点处收敛，你就不可能给它一个原点处不为0的边界条件。换言之，逻辑是，因为收敛，所以可能的边界条件已经退化了一个维度，以确保求解过程是自洽的。

常微分方程换个视角（先局限在希尔伯特空间中进行思考），其实就是在寻找算子的解空间。某处的函数值收敛，本身就是希尔伯特空间的一个强约束。合理的边界条件，肯定只能在解空间中寻找。

第二个问题是为什么参数上一个小的变化，能使得解发生这么剧烈的差异。按理来说特解作为参数的确应该是平滑变化的。

我们把算子的参数进行一个小的变化，就意味着解空间发生一个小的移动。直观上地从发散与否来判断函数的距离是有点偏颇的，如果真正绘图，会发现$P_2(x)$与$P_{2.001}(x)$的图形差异其实很小，即使在边界发散，也是以非常慢的速度发散（对数发散）。如果用函数的夹角来定义距离，二者的夹角其实非常小。

## 3. Spherical Harmonics

先看一下线性代数中的一个定理，定义张量积算子 $A \otimes B$

$$A \otimes B = \begin{pmatrix} a_{11}B & a_{12}B \\ a_{21}B & a_{22}B \end{pmatrix} = \begin{pmatrix} 
a_{11}b_{11} & a_{11}b_{12} & a_{12}b_{11} & a_{12}b_{12} \\
a_{11}b_{21} & a_{11}b_{22} & a_{12}b_{21} & a_{12}b_{22} \\
a_{21}b_{11} & a_{21}b_{12} & a_{22}b_{11} & a_{22}b_{12} \\
a_{21}b_{21} & a_{21}b_{22} & a_{22}b_{21} & a_{22}b_{22}
\end{pmatrix}$$

设 $A$ 是 $n \times n$ 矩阵，其特征值为 $\lambda_i$，对应的特征向量为 $\mathbf{x}_i$；$B$ 是 $m \times m$ 矩阵，其特征值为 $\mu_j$，对应的特征向量为 $\mathbf{y}_j$。则大矩阵 $C = A \otimes B$ （大小为 $nm \times nm$）的特征向量必然是

$$\mathbf{v}_{i,j} = \mathbf{x}_i \otimes \mathbf{y}_j$$

且对应的特征值为 $\lambda_i \cdot \mu_j$。

证明就算了，但这个定理本身很有意思，我们不妨直接推广到希尔伯特空间，老样子，把算子当成矩阵，应该有

$$(A \otimes B) \cdot (|\psi_A\rangle \otimes |\phi_B\rangle) = (A|\psi_A\rangle) \otimes (B|\phi_B\rangle)$$

假设向量 $|\psi\rangle$ 是算子 $A$ 的本征向量， $A|\psi\rangle = \lambda|\psi\rangle$。

向量 $|\phi\rangle$ 是算子 $B$ 的本征向量，$B|\phi\rangle = \mu|\phi\rangle$。

现在，我们让张量积算子 $A \otimes B$ 去作用于它们的复合直积态 $|\psi\rangle \otimes |\phi\rangle$

$$(A \otimes B)(|\psi\rangle \otimes |\phi\rangle) = (A|\psi\rangle) \otimes (B|\phi\rangle)$$

$$= (\lambda|\psi\rangle) \otimes (\mu|\phi\rangle)$$

$$= (\lambda \cdot \mu) \cdot (|\psi\rangle \otimes |\phi\rangle)$$

除此之外，两个矩阵 $A$ 和 $B$ 的克罗内克和定义为

$$A \oplus B = A \otimes I_m + I_n \otimes B$$

它的特征向量依然是小矩阵特征向量的张量积 $\mathbf{x}_i \otimes \mathbf{y}_j$，但由于恒等矩阵 $I$ 的存在，其对应的特征值神奇地变成了相加

$$(A \otimes I + I \otimes B)(|u_i\rangle \otimes |v_j\rangle) = (A|u_i\rangle \otimes I|v_j\rangle) + (I|u_i\rangle \otimes B|v_j\rangle)$$

$$= (\lambda_i |u_i\rangle \otimes |v_j\rangle) + (|u_i\rangle \otimes \mu_j |v_j\rangle)$$

$$\mathbf{= (\lambda_i + \mu_j) (|u_i\rangle \otimes |v_j\rangle)}$$

这件事和分离变量本身有千丝万缕的联系，例如求解二维直角坐标边界下的Helmholtz方程

$$\left( \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + k^2 \right) u(x,y) = 0$$

在 $\mathcal{H}_x$ 上，定义算子 $A = \frac{d^2}{dx^2}$，其定义域 $D(A)$ 包含 $x$ 方向的边界条件（如 $X(0)=X(a)=0$）。在 $\mathcal{H}_y$ 上，定义算子 $B = \frac{d^2}{dy^2}$，其定义域 $D(B)$ 包含 $y$ 方向的边界条件（如 $Y(0)=Y(b)=0$）。

则有

$$\hat{\mathcal{L}} = A \otimes I_y + I_x \otimes B$$

$$(A \otimes I_y + I_x \otimes B) |u\rangle = -k^2 |u\rangle$$

等式两边关于空间的依赖必须是独立的，这要求

$$\begin{cases} 
A|X\rangle = \lambda |X\rangle \\ 
B|Y\rangle = \mu |Y\rangle 
\end{cases}$$

$$\lambda + \mu = -k^2$$

这本质上，就是在进行分离变量的操作。

又比如，球面亥姆霍兹方程满足

$$\frac{1}{\sin\theta}\frac{\partial}{\partial \theta}\left(\sin\theta\frac{\partial Y}{\partial \theta}\right) + \frac{1}{\sin^2\theta}\frac{\partial^2 Y}{\partial \phi^2} + l(l+1)Y = 0$$

用算子写作

$$\nabla^2_{S^2} Y = -l(l+1)Y$$

其中

$$\nabla^2_{S^2} = \hat{\mathcal{L}}_\theta \otimes I_\phi + \frac{1}{\sin^2\theta} \otimes \hat{\mathcal{L}}_\phi$$

$$\hat{\mathcal{L}}_\phi = \frac{\partial^2}{\partial \phi^2}$$

$$\hat{\mathcal{L}}_\theta = \frac{1}{\sin\theta}\frac{\partial}{\partial \theta}\left(\sin\theta\frac{\partial}{\partial \theta}\right)$$

能这么写的原因是任何一个“普通函数”，都可以被完美等价地看作是一个“对角矩阵”。例如这里的$\frac{1}{\sin ^2(\theta)}$。因而在希尔伯特空间里，算子的乘法和张量积在代数行为能够视作等价。

进行变量分离 $Y(\theta, \phi) = \Theta(\theta) \cdot \Phi(\phi)$ 

于是

$$\left( \frac{1}{\sin^2\theta} \otimes \hat{\mathcal{L}}_\phi \right) \cdot \Big( \Theta(\theta) \otimes \Phi(\phi) \Big)$$

$$= \left( \frac{1}{\sin^2\theta} \cdot \Theta(\theta) \right) \otimes \left( \hat{\mathcal{L}}_\phi \cdot \Phi(\phi) \right)$$

$$= \left( \frac{1}{\sin^2\theta} \Theta(\theta) \right) \cdot \left( \frac{\partial^2}{\partial \phi^2} \Phi(\phi) \right)$$

$\hat{\mathcal{L}}_\phi$ 特征向量为 $e^{im\phi}$，特征值是 $-m^2$，于是直接把 $\Phi(\phi)=e^{im\phi}$ 代入

$$\nabla^2_{S^2} (\Theta_{l,m} \Phi_m) = \left[ \hat{\mathcal{L}}_\theta \Theta_{l,m} \right] \Phi_m + \frac{1}{\sin^2\theta} \Theta_{l,m} \left[ -m^2 \Phi_m \right]$$

$$\nabla^2_{S^2} Y_l^m = \left[ \frac{1}{\sin\theta}\frac{d}{d \theta}\left(\sin\theta\frac{d \Theta_{l,m}}{d \theta}\right) - \frac{m^2}{\sin^2\theta}\Theta_{l,m} \right] \Phi_m$$

注意到这里满足 $\nabla^2_{S^2} Y = -l(l+1)Y$ 的本征解就是Legendre多项式 $\Theta_{l,m}(\theta) = P_l^m(\cos\theta)$

$$\frac{1}{\sin\theta}\frac{d}{d \theta}\left(\sin\theta\frac{d P_l^m}{d \theta}\right) - \frac{m^2}{\sin^2\theta}P_l^m = -l(l+1)P_l^m$$

最终的解 $Y_l^m(\theta, \phi) = \Theta_{l,m}(\theta) \Phi_m(\phi)$ 又被称为球谐函数。

## 4. Spherical Bessel Functions

才发现漏掉了球贝塞尔函数。。

回头看看贝塞尔方程，本质上它是由极坐标Laplace算子的本征方程自然导出的

$$\nabla^2 = \frac{\partial^2}{\partial r^2} + \frac{1}{r}\frac{\partial}{\partial r} + \frac{1}{r^2}\frac{\partial^2}{\partial \theta^2}$$

$$\nabla^2 = \hat{\mathcal{L}}_r \otimes I_\theta + \frac{1}{r^2} \otimes \hat{\mathcal{L}}_\theta$$

$$\hat{\mathcal{L}}_\theta |\Theta\rangle = -n^2 |\Theta\rangle \quad \implies \quad \Theta(\theta) = e^{in\theta} \quad (n \in \mathbb{Z})$$

$$\left( \hat{\mathcal{L}}_r \otimes I_\theta + \frac{1}{r^2} \otimes (-n^2) \right) \Big(|R\rangle \otimes |\Theta\rangle\Big) = -k^2 \Big(|R\rangle \otimes |\Theta\rangle\Big)$$

$$\left( \frac{d^2}{dr^2} + \frac{1}{r}\frac{d}{dr} - \frac{n^2}{r^2} \right) R(r) = -k^2 R(r)$$

即得到一般形式下的贝塞尔方程

$$r^2 \frac{d^2 R}{dr^2} + r \frac{d R}{dr} + (k^2 r^2 - n^2) R = 0$$

而对于三维球坐标Laplace算子的本征方程

$$\nabla^2 = \frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial}{\partial r}\right) + \frac{1}{r^2\sin\theta}\frac{\partial}{\partial \theta}\left(\sin\theta\frac{\partial}{\partial \theta}\right) + \frac{1}{r^2\sin^2\theta}\frac{\partial^2}{\partial \phi^2}$$

$$\nabla^2 = \hat{\mathcal{L}}_r \otimes I_{S^2} + \frac{1}{r^2} \otimes \nabla^2_{S^2}$$

其中 $\nabla^2_{S^2}$ 正是我们前两问刚刚讨论过的二维球面拉普拉斯算子，其本征解为球谐函数 $Y_l^m(\theta, \phi) = \Theta_{l,m}(\theta) \Phi_m(\phi)$

于是分离变量

$$|\psi\rangle = |R(r)\rangle \otimes |Y(\theta, \phi)\rangle$$

得到

$$\left[ \frac{d^2}{dr^2} + \frac{2}{r}\frac{d}{dr} - \frac{l(l+1)}{r^2} \right] R(r) = -k^2 R(r)$$

$$r^2 \frac{d^2 R}{dr^2} + 2r \frac{d R}{dr} + \left[ k^2r^2 - l(l+1) \right] R = 0$$

这个方程被称为球贝塞尔方程。其通解和贝塞尔方程很类似，分别为一类球贝塞尔函数 $j_l(x)$ 和二类球贝塞尔函数 $y_l(x)$ （当$k=1$）

同样的，$y_l(x)$会在原点处发散，这使得很多时候会把它扔掉。

一个令人惊讶的事情是球贝塞尔函数是可以写成解析形式的

$$j_l(x) = (-x)^l \left( \frac{1}{x} \frac{d}{dx} \right)^l \left( \frac{\sin x}{x} \right)$$

$$y_l(x) = -(-x)^l \left( \frac{1}{x} \frac{d}{dx} \right)^l \left( \frac{\cos x}{x} \right)$$

以及其与贝塞尔函数之间存在点关系

$$j_l(x) = \sqrt{\frac{\pi}{2x}} J_{l+1/2}(x)$$

$$y_l(x) = \sqrt{\frac{\pi}{2x}} Y_{l+1/2}(x)$$

注意到标准贝塞尔函数的渐近行为是

$$J_\nu(x) \sim \frac{1}{\sqrt{x}}$$

这意味着球贝塞尔函数以 $\frac{1}{x}$ 形式收敛，这也与我们的直觉相符，毕竟其为球亥姆霍兹方程的径向解。

严格的远程渐进行为如下，可作参考

$$j_l(x) \approx \frac{1}{x} \sin\left( x - \frac{l\pi}{2} \right) \quad (x \to \infty)$$

$$y_l(x) \approx -\frac{1}{x} \cos\left( x - \frac{l\pi}{2} \right) \quad (x \to \infty)$$