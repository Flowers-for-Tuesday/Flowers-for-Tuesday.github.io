---
title: "DFT on Transverse Ising"
category: Research Notes
date: 2026-10-18
cover: cover.jpg
summary: "Easy revenge"
---

## 1 / 广义密度泛函与自旋DFT理论

本文研究的核心问题是：

**能否从一维横场 Ising 模型（TFIM）的精确均匀解出发，构造一个既能描述均匀基态，又能正确预测非均匀外场下密度响应的泛函？**

为回答这个问题，我们首先建立三个基本关系：

$$
\boxed{ \text{外场 }g \longleftrightarrow \text{密度 }\rho \longleftrightarrow \text{内部密度泛函 }F[\rho]. }
$$

随后证明，泛函的二阶导数（Hessian）决定密度的线性响应。这将成为后续 LDA、GGA、No-Go 定理和 NRC-LDA 的共同理论基础。

### 1.1 从普通 DFT 推广到自旋体系

普通电子 DFT 的基本思想是：基态性质可以通过电子密度而非完整多体波函数来描述。

这一思想并不局限于电子数密度。对于更一般的量子体系，考虑

$$
\boxed{ H[\boldsymbol g] = H_{\mathrm{int}}-\sum_i g_iO_i, } \tag{1.1}
$$

其中：

- $H_{\mathrm{int}}$ 表示内部相互作用；
- $g_i$ 表示外场；
- $O_i$ 是与外场耦合的局域算符。

我们可以定义广义密度

$$
\boxed{ \rho_i=\langle O_i\rangle. } \tag{1.2}
$$

本文研究周期边界下的一维横场 Ising 链，取相互作用常数 $J=1$：

$$
\boxed{ H[\boldsymbol g] = -\sum_{i=1}^{N}\sigma_i^z\sigma_{i+1}^z -\sum_{i=1}^{N}g_i\sigma_i^x. } \tag{1.3}
$$

因此，自然选择横向磁化作为广义密度：

$$
\boxed{ \rho_i=\langle\sigma_i^x\rangle. } \tag{1.4}
$$

这里的 $\rho_i$ 不是粒子数，而是格点 $i$ 的横向自旋期望值。

**关键思想：只要外场与某个物理量线性耦合，就可以尝试以该物理量的期望值作为广义 DFT 的基本变量。**

### 1.2 从基态能量定义精确密度泛函

给定外场 $\boldsymbol g$，设精确基态能量为

$$
E_0[\boldsymbol g].
$$

根据 Hellmann–Feynman 定理，

$$
\frac{\partial E_0}{\partial g_i} = -\langle\sigma_i^x\rangle,
$$

因此

$$
\boxed{ \rho_i = -\frac{\partial E_0}{\partial g_i}. } \tag{1.5}
$$

这说明 $\boldsymbol g$ 与 $\boldsymbol\rho$ 是共轭变量。

通过 Legendre–Fenchel 变换，定义精确内部泛函：

$$
\boxed{ F[\boldsymbol\rho] = \sup_{\boldsymbol g} \left[ E_0[\boldsymbol g] +\sum_i g_i\rho_i \right]. } \tag{1.6}
$$

相应地，给定外场时的基态能量可以通过变分原理获得：

$$
\boxed{ E_0[\boldsymbol g] = \min_{\boldsymbol\rho} \left[ F[\boldsymbol\rho] -\sum_i g_i\rho_i \right]. } \tag{1.7}
$$

这里需要区分两个对象：

$$
\underbrace{F[\boldsymbol\rho]}_{\text{内部泛函}} \qquad\text{与}\qquad \underbrace{ \mathcal E[\boldsymbol\rho;\boldsymbol g] = F[\boldsymbol\rho]-\sum_i g_i\rho_i }_{\text{给定外场的总能量泛函}}.
$$

内部泛函由模型的相互作用决定；外场只通过线性耦合项进入总能量。

在可微的稳定极小值处，变分条件为

$$
\boxed{ \frac{\partial F}{\partial\rho_i}=g_i. } \tag{1.8}
$$

这就是自旋 DFT 的 Euler 方程。

因此，后续工作的目标就是构造一个可计算的 $F[\boldsymbol\rho]$，使它的变分解尽可能接近精确密度。

### 1.3 Hessian 与静态响应函数

现在考虑均匀背景：

$$
g_i=g,\qquad \rho_i=r,
$$

其中 $r=\rho_{\mathrm{hom}}(g)$。

定义精确泛函在该背景处的 Hessian：

$$
\boxed{ K_{ij}(r) = \left. \frac{\partial^2F} {\partial\rho_i\partial\rho_j} \right|_{\rho_1=\cdots=\rho_N=r}. } \tag{1.9}
$$

其物理意义是：某个格点的密度变化，会如何改变另一个格点上的变分有效场。

对 Euler 方程施加微小扰动：

$$
g_i\to g+\delta g_i,\qquad \rho_i\to r+\delta\rho_i.
$$

保留一阶项，得到

$$
\boxed{ \delta g_i=\sum_jK_{ij}(r)\delta\rho_j. } \tag{1.10}
$$

另一方面，定义静态响应函数

$$
\boxed{ \chi_{ij}(g) = \frac{\partial\rho_i}{\partial g_j}. } \tag{1.11}
$$

于是

$$
\delta\rho_i=\sum_j\chi_{ij}(g)\delta g_j.
$$

比较两式：

$$
\boxed{ K(r)=\chi(g(r))^{-1}. } \tag{1.12}
$$

这说明：

**Hessian 不是一个抽象的数学量，而是描述体系抵抗密度变化能力的逆响应矩阵。**

在可逆的稳定背景中，$K$ 越小，体系对微弱外场的响应就越强。

### 1.4 为什么要进入动量空间？

均匀 TFIM 具有平移对称性，因此

$$
K_{ij}(r)=K(i-j;r),
$$

$$
\chi_{ij}(g)=\chi(i-j;g).
$$

换句话说，两个格点之间的响应只取决于距离，而不取决于绝对位置。

对于周期链，定义 Fourier 变换：

$$
\eta_q=\sum_j e^{-iqj}\eta_j,\qquad \eta_j=\frac1N\sum_qe^{iqj}\eta_q,
$$

其中允许的波数为

$$
q=\frac{2\pi n}{N}.
$$

实空间 Hessian 在动量空间中变为

$$
\boxed{ K(q;r) = \sum_{\ell}K(\ell;r)e^{-iq\ell}. } \tag{1.13}
$$

由于 Fourier 变换将平移不变矩阵对角化，

$$
\boxed{ \delta g_q=K(q;r)\delta\rho_q, }
$$

而响应关系为

$$
\boxed{ \delta\rho_q=\chi(q;g)\delta g_q. }
$$

所以

$$
\boxed{ K(q;r)=\frac1{\chi(q;g(r))}. } \tag{1.14}
$$

这里两个变量具有不同含义：

- $q$：所研究密度扰动的空间波数；
- $r$：计算 Hessian 时所处的均匀密度背景。

也就是说，$K(q;r)$ 描述的是：**在密度为 $r$ 的均匀体系中，产生波数为 $q$ 的密度变化需要多大的能量代价。**

例如，对单模扰动

$$
\rho_i=r+A\cos(qi),\qquad q\neq0,\pi,
$$

其二阶能量变化为

$$
\boxed{ \Delta F^{(2)} = \frac{NA^2}{4}K(q;r). } \tag{1.15}
$$

至此，我们已经建立了本文最重要的理论关系：

$$
\boxed{ \text{密度泛函的 Hessian} \quad\Longleftrightarrow\quad \text{静态密度响应的逆}. }
$$

## 2 / LDA＆GGA on Transverse Ising

这一节的逻辑是：

首先利用 TFIM 的精确可解性得到均匀基态能量；再通过 Legendre 变换构造 LDA；最后分析 GGA 增加的空间修正为什么仍然不够。

### 2.1 均匀 TFIM 的精确解

考虑均匀横场

$$
g_i=g.
$$

Hamiltonian 为

$$
H(g) = -\sum_i\sigma_i^z\sigma_{i+1}^z -g\sum_i\sigma_i^x. \tag{2.1}
$$

该模型可以通过 Jordan–Wigner 变换映射为费米子体系，再利用 Fourier 和 Bogoliubov 变换对角化：

$$
\boxed{ H = \sum_k\varepsilon_k \left(\gamma_k^\dagger\gamma_k-\frac12\right), } \tag{2.2}
$$

其中

$$
\boxed{ \varepsilon_k(g) = 2\sqrt{1+g^2-2g\cos k}. } \tag{2.3}
$$

$\varepsilon_k$ 是动量为 $k$ 的准粒子激发能量，并非所有动量共有的同一个能隙。

真正的单准粒子能隙尺度为

$$
\Delta_{\mathrm{qp}} = \min_k\varepsilon_k = 2|g-1|. \tag{2.4}
$$

因此临界点是

$$
\boxed{g_c=1.}
$$

在基态中，没有 Bogoliubov 准粒子：

$$
\gamma_k^\dagger\gamma_k|0\rangle=0.
$$

但由于 Hamiltonian 中存在真空能常数项，基态能量为

$$
E_0(g)=-\frac12\sum_k\varepsilon_k.
$$

在热力学极限下，定义每格点基态能量

$$
e_{\mathrm{hom}}(g)=\lim_{N\to\infty}\frac{E_0(g)}N.
$$

于是

$$
\boxed{ e_{\mathrm{hom}}(g) = -\frac1\pi\int_0^\pi D_k(g)\,dk, } \tag{2.5}
$$

其中

$$
\boxed{ D_k(g)=\sqrt{1+g^2-2g\cos k}. }
$$

从实空间角度，同一个基态能量密度也可写为

$$
e_{\mathrm{hom}}(g) = -\langle\sigma_i^z\sigma_{i+1}^z\rangle -g\langle\sigma_i^x\rangle.
$$

因此：

实空间表示强调自旋关联与横场能；动量空间表示则将能量分解为不同准粒子模式的贡献。

### 2.2 从 $e(g)$ 构造 $f_{\mathrm{hom}}(\rho)$

根据 Hellmann–Feynman 定理，

$$
\rho_{\mathrm{hom}}(g) = -\frac{de_{\mathrm{hom}}(g)}{dg}.
$$

对式（2.5）求导：

$$
\boxed{ \rho_{\mathrm{hom}}(g) = \frac1\pi\int_0^\pi \frac{g-\cos k} {\sqrt{1+g^2-2g\cos k}}\,dk. } \tag{2.6}
$$

在正横场分支上，可以反解

$$
g=g(\rho).
$$

再通过 Legendre 变换定义均匀内部能量密度：

$$
\boxed{ f_{\mathrm{hom}}(\rho) = e_{\mathrm{hom}}(g(\rho)) + g(\rho)\rho. } \tag{2.7}
$$

求导可得

$$
\begin{aligned}
f_{\mathrm{hom}}'(\rho) &= e_{\mathrm{hom}}'(g)\frac{dg}{d\rho} +g+\rho\frac{dg}{d\rho}\\
&=g,
\end{aligned}
$$

因为 $e_{\mathrm{hom}}'(g)=-\rho$。

因此

$$
\boxed{ f_{\mathrm{hom}}'(\rho)=g(\rho). } \tag{2.8}
$$

进一步，

$$
\boxed{ f_{\mathrm{hom}}''(\rho) = \frac{dg}{d\rho} = \frac1{\chi_{\mathrm{exact}}(0;g(\rho))}. } \tag{2.9}
$$

这一步是 LDA 与后续响应核之间的关键联系。

### 2.3 LDA：精确均匀能量的局域推广

局域密度近似（LDA）定义为

$$
\boxed{ F_{\mathrm{LDA}}[\boldsymbol\rho] = \sum_i f_{\mathrm{hom}}(\rho_i). } \tag{2.10}
$$

它假设每个格点的内部能量只由该格点的密度决定。

在非均匀外场下，变分方程为

$$
f_{\mathrm{hom}}'(\rho_i)=g_i.
$$

因此

$$
\boxed{ \rho_i^{\mathrm{LDA}} = \rho_{\mathrm{hom}}(g_i). } \tag{2.11}
$$

这一公式直观地说明：LDA 把每个格点当作局部均匀体系处理，没有考虑不同格点密度响应之间的耦合。

但由于 $f_{\mathrm{hom}}$ 本身来自精确均匀解，**对于均匀外场，LDA 是精确的**。

例如，在严格临界均匀外场 $g=1$ 下，

$$
\boxed{ e_{\mathrm{hom}}(1)=-\frac4\pi, \qquad \rho_{\mathrm{hom}}(1)=\frac2\pi. } \tag{2.12}
$$

LDA 能准确恢复这两个结果。

所以不能简单地说“LDA 在临界点失效”；更准确的说法是：

**LDA 在临界均匀基态上仍然精确，但无法描述临界点附近的完整非均匀响应。**

### 2.4 为什么 $q=0$ 是理解 LDA 的关键？

现在研究均匀背景下的微弱外场扰动：

$$
\delta g_i=\lambda\cos(qi).
$$

当

$$
q=0,
$$

外场变化为

$$
\delta g_i=\lambda,
$$

即所有格点受到完全相同的扰动。

因此，$q=0$ 表示**均匀响应模式**。

精确均匀磁化率是

$$
\boxed{ \chi_{\mathrm{exact}}(0;g) = \frac{d\rho_{\mathrm{hom}}(g)}{dg}. } \tag{2.13}
$$

由式（2.6）直接求导：

$$
\boxed{ \chi_{\mathrm{exact}}(0;g) = \frac1\pi\int_0^\pi \frac{\sin^2k} {\left(1+g^2-2g\cos k\right)^{3/2}} \,dk. } \tag{2.14}
$$

而 LDA 的 Hessian 为

$$
K_{ij}^{\mathrm{LDA}} = f_{\mathrm{hom}}''(r)\delta_{ij}.
$$

Fourier 变换后：

$$
\boxed{ K_{\mathrm{LDA}}(q;r) = f_{\mathrm{hom}}''(r) = K_{\mathrm{exact}}(0;r), \quad \forall q. } \tag{2.15}
$$

这是需要特别理解的地方：

**LDA 不是只包含 $q=0$ 模式，而是把 $q=0$ 的精确刚度错误地用于所有动量。**

因此，对于 $q\neq0$，一般有

$$
K_{\mathrm{LDA}}(q;r) \neq K_{\mathrm{exact}}(q;r).
$$

在严格临界点，情况更加明显：

$$
\chi_{\mathrm{exact}}(0;1)\to\infty,
$$

因此热力学意义下

$$
K_{\mathrm{LDA}}(q;1)=0,\qquad\forall q.
$$

但精确理论中，非零动量的 $K_{\mathrm{exact}}(q;1)$ 并不为零。

所以即使均匀临界能量和密度完全正确，LDA 仍可能错误预测空间调制下的密度响应。

### 2.5 如何精确计算 $\chi(q;g)$ 与 $K(q;g)$？

LDA 只使用零动量响应，但 TFIM 的 Jordan–Wigner 解实际上允许我们求得**所有动量的精确静态响应**。

定义动量空间横向磁化算符：

$$
O_q=\sum_j e^{-iqj}\sigma_j^x.
$$

零温静态响应可以写成 Lehmann 谱表示：

$$
\boxed{ \chi_{\mathrm{exact}}(q;g) = \frac2N\sum_{n>0} \frac{ |\langle n|O_q|0\rangle|^2 }{ E_n-E_0 }. } \tag{2.16}
$$

这个公式说明，静态响应由两部分决定：

一是激发该状态所需的能量 $E_n-E_0$；二是密度算符与该激发态之间的跃迁矩阵元。

对 TFIM，横向自旋算符在 JW 费米子表示中是双线性算符，因此在均匀基态上，相关响应可归结为双准粒子激发。

定义

$$
A_k=g-\cos k,\qquad B_k=\sin k,
$$

$$
D_k=\sqrt{A_k^2+B_k^2}.
$$

通过 Bogoliubov 变换计算这些激发的能量与矩阵元，可以得到热力学极限下的精确积分：

$$
\boxed{ \chi_{\mathrm{exact}}(q;g) = \frac1{2\pi}\int_{-\pi}^{\pi} \frac{ 1-\dfrac{ A_kA_{k+q}-B_kB_{k+q} }{ D_kD_{k+q} } }{ D_k+D_{k+q} }\,dk. } \tag{2.17}
$$

这就是可以直接用于数值积分的表达式。

作为一致性检查，令 $q=0$，分子变为

$$
1-\frac{A_k^2-B_k^2}{D_k^2} = \frac{2\sin^2k}{D_k^2}.
$$

因此式（2.17）退化为

$$
\chi_{\mathrm{exact}}(0;g) = \frac1\pi\int_0^\pi \frac{\sin^2k}{D_k^3}\,dk,
$$

恰好与式（2.14）一致。

最后，利用 Hessian 与响应之间的逆关系：

$$
\boxed{ K_{\mathrm{exact}}(q;g) = \frac1{\chi_{\mathrm{exact}}(q;g)}. } \tag{2.18}
$$

这里的倒数是因为平移不变响应矩阵已在 Fourier 空间对角化。

为了将核写成密度的函数，利用

$$
r=\rho_{\mathrm{hom}}(g)
$$

反解 $g=g(r)$，并定义

$$
\boxed{ K_{\mathrm{exact}}(q;r) = K_{\mathrm{exact}}(q;g(r)). } \tag{2.19}
$$

因此，TFIM 所需的响应数据可由如下流程得到：

$$
\boxed{ g \longrightarrow D_k \longrightarrow\chi_{\mathrm{exact}}(q;g) \longrightarrow K_{\mathrm{exact}}(q;g) \longrightarrow K_{\mathrm{exact}}(q;r). }
$$

**这整套均匀响应输入来自精确解，不需要经验拟合。**

### 2.6 GGA：用最近邻梯度修正 LDA

2021 年 Mao 等人的论文 *Testing density functional theory in a quantum Ising chain* 在 LDA 基础上采用了如下 GGA：

$$
\boxed{ F_{\mathrm{GGA}}[\rho] = F_{\mathrm{LDA}}[\rho] + J_{\mathrm{eff}} \sum_i (\rho_i^2-\rho_{i+1}^2)^2, } \tag{2.20}
$$

其中固定

$$
\boxed{J_{\mathrm{eff}}=0.35.}
$$

这一系数是经验拟合参数，而不是由完整精确响应解析推导出来的。

该修正项具有清晰的物理意义：如果相邻格点的密度发生变化，需要付出额外的能量。

此外，它在均匀密度下为零，不改变均匀能量；使用 $\rho^2$ 还能保留 TFIM 内部泛函的局域符号对称性。

下面计算它的 Hessian。

令

$$
\rho_i=r+\eta_i,\qquad |\eta_i|\ll r.
$$

则

$$
\rho_i^2-\rho_{i+1}^2 = 2r(\eta_i-\eta_{i+1})+O(\eta^2).
$$

因此，GGA 修正项的二阶部分为

$$
G_{\mathrm{GGA}}^{(2)} = 4J_{\mathrm{eff}}r^2 \sum_i(\eta_i-\eta_{i+1})^2.
$$

利用 Fourier 恒等式

$$
\sum_i(\eta_i-\eta_{i+1})^2 = \frac4N\sum_q \sin^2\frac q2\,|\eta_q|^2,
$$

得到

$$
G_{\mathrm{GGA}}^{(2)} = \frac1{2N}\sum_q 32J_{\mathrm{eff}}r^2 \sin^2\frac q2\,|\eta_q|^2.
$$

因此

$$
\boxed{ K_{\mathrm{GGA}}(q;r) = K_{\mathrm{exact}}(0;r) + 32J_{\mathrm{eff}}r^2 \sin^2\frac q2. } \tag{2.21}
$$

在小动量处：

$$
\boxed{ K_{\mathrm{GGA}}(q;r) - K_{\mathrm{exact}}(0;r) = 8J_{\mathrm{eff}}r^2q^2+O(q^4). } \tag{2.22}
$$

与 LDA 相比，GGA 已经具有动量依赖，因而能够改善某些非均匀密度预测。

但它仍然只能描述一种固定的解析动量结构。

**问题因此转变为：通过增加更多有限距离的梯度项、或者重新调整它们的系数，能否最终恢复临界点附近的完整 Hessian？**

这就是 No-Go Theorem 要回答的问题。

## 3 / No Go Theorem

前一节已经说明：

- LDA 只能恢复精确的零动量 Hessian；
- GGA 增加了动量依赖，但修正项仍然具有固定的 $q^2$ 型结构。

接下来我们证明一条更一般的定理：

**无论增加多少个固定距离的梯度修正，只要 Hessian 的作用范围不随临界距离增长，就无法恢复 TFIM 的完整临界响应结构。**

### 3.1 为什么有限范围 Hessian 必然是三角多项式？

考虑一个保留精确均匀能量的近似泛函 $F_R[\rho]$。

假设它在均匀背景附近的 Hessian 作用范围不超过 $R$：

$$
K_{ij}^{(R)}=0,\qquad |i-j|>R. \tag{3.1}
$$

这里的 $R$ 指 Hessian 的格点耦合范围，而不是泛函表达式中形式上的导数阶数。

由于均匀背景具有平移对称性，

$$
K_{ij}^{(R)}=a_{i-j}(g).
$$

又由于 Hessian 是对称矩阵，

$$
a_{-\ell}(g)=a_\ell(g).
$$

因此它的 Fourier 变换为

$$
\begin{aligned}
K_R(q;g) &=\sum_{\ell=-R}^{R}a_\ell(g)e^{-iq\ell}\\
&=a_0(g)+2\sum_{\ell=1}^{R}a_\ell(g)\cos(\ell q).
\end{aligned} \tag{3.2}
$$

这说明：**任何平移不变、固定有限范围的 Hessian，在动量空间都只能是有限阶偶三角多项式。**

现在再加入一个条件：近似泛函必须保留精确均匀能量，

$$
F_R[r,\ldots,r]=Nf_{\mathrm{hom}}(r).
$$

沿均匀密度方向求两次导数：

$$
\sum_{ij}K_{ij}^{(R)} = Nf_{\mathrm{hom}}''(r).
$$

另一方面，由平移对称性，

$$
\sum_{ij}K_{ij}^{(R)} = NK_R(0;g).
$$

因此

$$
\boxed{ K_R(0;g) = f_{\mathrm{hom}}''(r) = K_{\mathrm{exact}}(0;g). } \tag{3.3}
$$

由式（3.2）在 $q=0$ 的值，

$$
a_0+2\sum_{\ell=1}^{R}a_\ell = K_{\mathrm{exact}}(0;g).
$$

消去 $a_0$，并定义 $b_\ell=-a_\ell$，就得到

$$
\boxed{ K_R(q;g) = K_{\mathrm{exact}}(0;g) + 2\sum_{\ell=1}^{R} b_\ell(g)[1-\cos(\ell q)]. } \tag{3.4}
$$

这就是之前讨论的有限范围 Hessian 一般形式。

它由三个条件推出：

1. **固定范围：** 只有有限距离的 Hessian 矩阵元非零。
2. **平移对称性：** 矩阵元只与格点间距有关。
3. **精确均匀极限：** $K_R(0)=K_{\mathrm{exact}}(0)$。

因此，式（3.4）不是对 GGA 的特殊假设，而是所有满足上述条件的固定范围泛函所共有的结构。

作为特例：

$$
\begin{aligned}
R=0:\quad& K_{\mathrm{LDA}}(q)=K_{\mathrm{exact}}(0),\\[3pt]
R=1:\quad& K_1(q)=K_{\mathrm{exact}}(0) +2b_1(1-\cos q).
\end{aligned}
$$

对于 Mao 等人的 GGA，

$$
b_1(g)=8J_{\mathrm{eff}}r(g)^2,
$$

因此式（3.4）正好恢复式（2.21）。

### 3.2 精确 TFIM 在临界点具有非解析 Hessian

由第 2 节的精确响应积分，可以研究临界点 $g_c=1$ 附近的低动量行为。

在 $g=1$ 时，

$$
D_k(1) = \sqrt{2-2\cos k} \sim |k|.
$$

低动量准粒子能量因此趋于零。

由精确静态响应积分的红外部分可得

$$
\boxed{ \chi_{\mathrm{exact}}(q;1) \sim \frac1\pi\log\frac1{|q|}, \qquad q\to0. } \tag{3.5}
$$

于是

$$
\boxed{ K_{\mathrm{exact}}(q;1) \sim \frac{\pi}{\log(1/|q|)}. } \tag{3.6}
$$

这是关键的临界行为。

相比之下，固定范围 Hessian 满足

$$
1-\cos(\ell q) = \frac{\ell^2q^2}{2}+O(q^4).
$$

如果 $b_\ell(1)$ 有限，则临界点处

$$
K_R(q;1)=O(q^2), \tag{3.7}
$$

因为 $K_{\mathrm{exact}}(0;1)=0$。

因此

$$
\frac{K_R(q;1)} {K_{\mathrm{exact}}(q;1)} = O\!\left(q^2\log\frac1{|q|}\right) \longrightarrow0. \tag{3.8}
$$

这说明两个 Hessian 的渐近结构根本不同：

$$
\boxed{ \text{固定范围：解析的 }q^2,q^4,\ldots \quad\neq\quad \text{精确临界核：}\frac1{\log(1/|q|)}. }
$$

不过，上面的推导假设临界点的 $b_\ell$ 有限。为了给出更严格的定理，还要考虑允许系数在临界附近发散的情况。

### 3.3 No-Go Theorem：固定范围无法恢复完整临界响应

定理：固定范围临界 Hessian 不可精确匹配

设

$$
m=|g-1|\to0,\qquad q=ms,
$$

其中 $s$ 取任意固定的非退化区间

$$
0<a\le s\le b.
$$

假设近似泛函保留精确均匀能量，且其 Hessian 的作用范围 $R$ 不随 $m$ 增长。

那么，无论如何选择系数 $b_\ell(m)$，即使允许这些系数在 $m\to0$ 时发散，固定范围 Hessian 都无法一致恢复整个临界交叉响应函数。

**证明分为三步。**

**第一步：求精确 Hessian 的临界标度。**

在 $g=1\pm m$、$m\to0$ 时，低能区满足

$$
D_k(g)\simeq\sqrt{k^2+m^2}.
$$

将这一形式代入精确响应积分，并对动量积分的红外部分进行分析，可以得到

$$
\chi_{\mathrm{exact}}(0;m) = \frac1\pi\log\frac1m+O(1), \tag{3.9}
$$

以及在 $q=ms$ 时，

$$
\chi_{\mathrm{exact}}(0;m) - \chi_{\mathrm{exact}}(ms;m) \longrightarrow \frac1{2\pi} \int_0^1 \log[1+x(1-x)s^2]\,dx. \tag{3.10}
$$

由

$$
K=\frac1\chi
$$

可得

$$
\begin{aligned}
&K_{\mathrm{exact}}(ms;m) -K_{\mathrm{exact}}(0;m)\\
&\quad= \frac{ \chi_{\mathrm{exact}}(0;m) -\chi_{\mathrm{exact}}(ms;m) }{ \chi_{\mathrm{exact}}(ms;m) \chi_{\mathrm{exact}}(0;m) }.
\end{aligned}
$$

因此

$$
\boxed{ \log^2\frac1m\, \Delta K_{\mathrm{exact}}(ms;m) \longrightarrow S(s), } \tag{3.11}
$$

其中

$$
\boxed{ S(s)= \frac{\pi}{2} \int_0^1 \log[1+x(1-x)s^2]\,dx. } \tag{3.12}
$$

这就是精确 TFIM 的临界交叉函数。它描述当临界距离 $m$ 与波数 $q$ 同时趋于零、但 $q/m=s$ 保持固定时，逆响应核如何变化。

**第二步：固定范围 Hessian 只能给出有限阶多项式。**

由式（3.4），

$$
\Delta K_R(q;m) = 2\sum_{\ell=1}^{R} b_\ell(m)[1-\cos(\ell q)].
$$

利用

$$
\cos(\ell q)=T_\ell(\cos q),
$$

其中 $T_\ell$ 是 Chebyshev 多项式，可以将固定范围核写成 $1-\cos q$ 的至多 $R$ 阶多项式。

定义

$$
x_m(s)=\frac{4\sin^2(ms/2)}{m^2}.
$$

由于

$$
x_m(s)\to s^2,
$$

若缩放后的固定范围核在整个 $s$ 区间上具有有限一致极限，则该极限只能具有形式

$$
\boxed{ P_R(s)=c_1s^2+c_2s^4+\cdots+c_Rs^{2R}. } \tag{3.13}
$$

这个结论不依赖 $b_\ell(m)$ 是否有界：如果上述缩放核一致收敛，在 $R$ 个不同的 $s$ 点考察其取值，便可通过多项式插值确定所有缩放系数；有限维插值的极限仍然只能是至多 $R$ 阶多项式。

**第三步：精确交叉函数不是有限阶多项式。**

展开式（3.12）：

$$
\boxed{ S(s) = \frac{\pi}{12}s^2 -\frac{\pi}{120}s^4 +\frac{\pi}{840}s^6-\cdots. } \tag{3.14}
$$

它包含无限多个非零偶次幂。

因此对任意固定 $R$：

$$
\boxed{ S(s)\ne P_R(s) }
$$

不可能在整个非退化区间上成立。

所以，固定范围泛函不可能精确恢复完整的临界交叉 Hessian。

$$
\boxed{\text{Q.E.D.}}
$$

这一统一定理涵盖了固定系数 GGA，也涵盖允许系数随背景重新拟合的有限范围修正。其关键限制是 $R$ 固定，而不是参数是否经过拟合。

`TFIM_核心研究与临界适用窗口_含重拟合对照(2).pdf`

### 3.4 Hessian 无法匹配，为什么会造成密度误差？

考虑稳定的均匀背景 $g_0\neq1$，施加微弱非均匀外场：

$$
\boxed{ g_i=g_0+\lambda v_i. } \tag{3.15}
$$

精确密度展开为

$$
\rho_{\mathrm{exact}} = \rho_0+\lambda\chi_{\mathrm{exact}}v+O(\lambda^2).
$$

近似泛函的密度为

$$
\rho_R = \rho_0+\lambda\chi_Rv+O(\lambda^2).
$$

因此

$$
\boxed{ \rho_R-\rho_{\mathrm{exact}} = \lambda(\chi_R-\chi_{\mathrm{exact}})v +O(\lambda^2). } \tag{3.16}
$$

对于被外场激发的单一动量 $q$，其相对线性密度响应误差为

$$
\boxed{ \epsilon_\rho(q) = \left| \frac{\chi_R(q)}{\chi_{\mathrm{exact}}(q)}-1 \right| = \left| \frac{K_{\mathrm{exact}}(q)}{K_R(q)}-1 \right|. } \tag{3.17}
$$

所以只要该动量上的 Hessian 不一致，就会留下非零的一阶响应误差。

这意味着：

$$
\boxed{ \|\rho_R-\rho_{\mathrm{exact}}\| = O(\lambda) } \tag{3.18}
$$

是 LDA/GGA 在一般弱非均匀外场下的领先误差形式。

### 3.5 为什么固定范围的泛函在非临界区能够表现较好？

前面的 No-Go Theorem 说明，固定范围 Hessian 无法精确恢复 TFIM 的完整临界响应结构。但这并不意味着 LDA、GGA 以及更一般的有限范围泛函在所有参数区域都不可靠。

实际上，**固定范围近似在非临界区之所以能够表现较好，是因为精确响应核具有良好的解析性，其空间非局域性可以由有限距离的修正有效近似。**

**第一，非临界区的有限能隙保证了精确 Hessian 的低动量解析性。**

考虑正横场分支上一个固定的、稳定的非临界均匀背景 $g_0>0$、$g_0\neq1$，定义

$$
m=|g_0-1|>0,\qquad r=\rho_{\mathrm{hom}}(g_0).
$$

由式（2.3）和式（2.4），准粒子能隙为

$$
\Delta_{\mathrm{qp}}=2m>0,\qquad D_k(g_0)\ge m.
$$

因此，式（2.17）中的响应积分不再具有临界点处的红外奇异性。在固定的非临界背景下，可以对小动量 $q$ 进行 Taylor 展开。结合反演对称性 $K_{\mathrm{exact}}(-q;g_0)=K_{\mathrm{exact}}(q;g_0)$，得到

$$
\boxed{
K_{\mathrm{exact}}(q;g_0)
=K_{\mathrm{exact}}(0;g_0)+c_2(g_0)q^2+c_4(g_0)q^4+\cdots.
} \tag{3.19}
$$

其中 $K_{\mathrm{exact}}(0;g_0)=1/\chi_{\mathrm{exact}}(0;g_0)>0$，各展开系数在该固定背景下有限。

相比之下，式（3.4）给出的有限范围 Hessian 在小动量处满足

$$
\begin{aligned}
K_R(q;g_0)={}&K_{\mathrm{exact}}(0;g_0)\\
&+\left[\sum_{\ell=1}^{R}\ell^2b_\ell(g_0)\right]q^2\\
&-\frac1{12}\left[\sum_{\ell=1}^{R}\ell^4b_\ell(g_0)\right]q^4+\cdots.
\end{aligned}
$$

这说明，在非临界区，固定范围 Hessian 与精确 Hessian 具有相同类型的偶次幂展开。两者的差别主要在于展开系数，而不再像严格临界点处那样存在解析结构上的根本冲突。

例如，LDA 已经精确匹配常数项，因此对于足够长波长的微弱外场，其 Hessian 误差为 $O(q^2)$。

而由式（2.22），最近邻 GGA 进一步给出

$$
K_{\mathrm{GGA}}(q;r)-K_{\mathrm{exact}}(0;r)
=8J_{\mathrm{eff}}r^2q^2+O(q^4).
$$

如果该二阶系数能够较好地近似精确系数 $c_2(g_0)$，GGA 就有可能进一步减小长波长响应误差。特别地，若两者恰好匹配，则 Hessian 误差可以从 $O(q^2)$ 降为 $O(q^4)$。

这里并不是说固定的经验参数 $J_{\mathrm{eff}}=0.35$ 必然在所有非临界背景下都能匹配 $c_2(g_0)$，而是说明最近邻梯度修正在非临界区具有合理的数学结构。

**第二，从实空间看，非临界区的精确 Hessian 可以由短程耦合有效近似。**

在上述固定的非临界背景下，式（2.17）的积分核可以解析延拓到实动量附近的复动量区域。由于稳定、可逆背景下的 $\chi_{\mathrm{exact}}(q;g_0)$ 在实动量上连续且严格为正，其倒数也在某个包含实动量轴的复动量带内保持解析。

由 Fourier 系数的衰减性质，精确实空间 Hessian 的长距离矩阵元可以用指数衰减界估计：

$$
|K(\ell;r)|\le C(g_0)e^{-|\ell|/\xi_K(g_0)}.
$$

其中 $\xi_K(g_0)$ 是用于描述逆响应核空间衰减的长度尺度，不必等同于自旋关联长度。

令 $b_\ell^{\mathrm{exact}}(g_0)=-K(\ell;r)$（$\ell\ge1$），则精确 Hessian 可以写成式（3.4）的无限范围推广：

$$
K_{\mathrm{exact}}(q;g_0)
=K_{\mathrm{exact}}(0;g_0)
+2\sum_{\ell=1}^{\infty}b_\ell^{\mathrm{exact}}(g_0)[1-\cos(\ell q)].
$$

如果只保留前 $R$ 个距离的精确系数，并保持零动量 Hessian 不变，得到截断核 $\widetilde K_R$，则截断误差满足

$$
\boxed{
\begin{aligned}
|\widetilde K_R(q;g_0)-K_{\mathrm{exact}}(q;g_0)|
&\le4\sum_{\ell>R}|b_\ell^{\mathrm{exact}}(g_0)|\\
&\le C'(g_0)e^{-R/\xi_K(g_0)}.
\end{aligned}
} \tag{3.20}
$$

因此，当 $R$ 足以覆盖精确逆响应核的主要空间作用范围时，有限范围 Hessian 就可以较好地逼近完整响应核。

这并不意味着非临界区的精确泛函本身是严格局域的，而是意味着被忽略的远距离耦合可以足够小。式（3.20）说明的是适当选取有限范围系数时所能达到的近似精度，并不是任意经验 GGA 都自动满足的误差界。

**第三，有限的响应刚度使 Hessian 误差不必被显著放大为密度误差。**

由式（3.17），在稳定的线性响应范围内，单一动量模式的相对密度响应误差为

$$
\boxed{
\epsilon_\rho(q)
=\frac{|K_{\mathrm{exact}}(q;g_0)-K_R(q;g_0)|}
{|K_R(q;g_0)|}.
} \tag{3.21}
$$

在固定的非临界背景下，精确 Hessian 在整个 Brillouin 区内连续且严格为正，因而存在正的下界 $\kappa_{\min}(g_0)=\min_q K_{\mathrm{exact}}(q;g_0)>0$。

若近似核的最大误差为 $\delta_R=\max_q|K_R(q;g_0)-K_{\mathrm{exact}}(q;g_0)|$，且 $\delta_R<\kappa_{\min}$，则有

$$
\epsilon_\rho(q)\le\frac{\delta_R}{\kappa_{\min}-\delta_R}.
$$

这说明，只要 Hessian 近似足够准确，而且响应刚度没有过度软化，密度的线性响应误差就能够受到控制。

对于 LDA 和 GGA，虽然一般弱场密度误差仍然是 $O(\lambda)$，但其一阶误差系数可以很小。特别是当外场主要包含长波长模式时，LDA 的相对线性响应误差为 $O(q^2)$；若 GGA 又精确匹配了二阶动量系数，则该误差可以进一步降为 $O(q^4)$。

因此，**非临界区的良好表现并不与 No-Go Theorem 矛盾：有限范围泛函可以在一定背景和波长范围内提供高精度近似，但无法在逼近临界点时一致恢复完整的临界交叉响应。**

当 $m\to0$ 时，准粒子能隙闭合，零动量刚度趋于零，式（3.5）和式（3.6）所描述的非解析结构逐渐显现。此时，非临界区的解析展开和有限距离截断误差估计不能直接作为一致适用于临界极限的近似保证。

不过，这仍不意味着任意外场下的误差都会随临界距离单调增加。有限范围泛函的实际精度还取决于作用范围 $R$、系数的选取、外场的波长以及扰动幅度。

至此，No-Go Theorem 给出的设计要求已经十分明确：

$$
\boxed{ \text{要精确恢复完整均匀 Hessian，} \quad \text{就必须超越固定有限范围修正。} }
$$

接下来要解决的问题是：**到底需要补充什么信息，以及怎样将它构造成一个真正可以变分求解的统一密度泛函？**

## 4 / Fixed Functional（NRC-LDA）

上一节的 No-Go Theorem 说明，固定范围的局域或半局域修正不能恢复 TFIM 的完整临界 Hessian。

但这并不意味着我们需要重新构造整个密度泛函。

事实上，LDA 已经准确包含了均匀体系的全部能量信息，以及零动量响应。我们真正需要修复的只是它缺少的非零动量响应。

这引出了 NRC-LDA（Nonlocal Response-Corrected Local Density Approximation）的核心设计思想：

$$
\boxed{ \text{保留精确均匀 LDA} + \text{补回完整的非局域逆响应}. }
$$

### 4.1 首先确定 LDA 究竟缺少什么

在均匀密度背景 $r$ 附近，令

$$
\rho_i=r+\eta_i.
$$

精确泛函的二阶展开为

$$
\begin{aligned}
F_{\mathrm{exact}}[r+\eta] ={}&Nf_{\mathrm{hom}}(r) +g(r)\sum_i\eta_i\\
&+\frac1{2N}\sum_q K_{\mathrm{exact}}(q;r)|\eta_q|^2 +O(\eta^3).
\end{aligned} \tag{4.1}
$$

而 LDA 的展开是

$$
\begin{aligned}
F_{\mathrm{LDA}}[r+\eta] ={}&Nf_{\mathrm{hom}}(r) +g(r)\sum_i\eta_i\\
&+\frac1{2N}\sum_q K_{\mathrm{exact}}(0;r)|\eta_q|^2 +O(\eta^3).
\end{aligned} \tag{4.2}
$$

两者具有完全相同的均匀能量和一阶项，区别仅在于 Hessian 的动量依赖。

因此，相减便得到所需要的二阶修正：

$$
\boxed{ G^{(2)}[\eta;r] = \frac1{2N}\sum_{q\neq0} \Delta K(q;r)|\eta_q|^2, } \tag{4.3}
$$

其中

$$
\boxed{ \Delta K(q;r) = K_{\mathrm{exact}}(q;r) - K_{\mathrm{exact}}(0;r). } \tag{4.4}
$$

利用 $K=\chi^{-1}$，也可以写成

$$
\boxed{ \Delta K(q;r) = \frac1{\chi_{\mathrm{exact}}(q;g(r))} - \frac1{\chi_{\mathrm{exact}}(0;g(r))}. } \tag{4.5}
$$

因此，**所需的二阶修正核由精确响应唯一确定，不需要增加经验拟合系数。**

注意，$\Delta K(0;r)=0$，因为零动量 Hessian 已经由 LDA 正确给出。

接下来，还需要把式（4.3）推广成一个能够对非均匀密度直接求值和变分的泛函。

### 4.2 为什么选择平方密度 $\rho_i^2$？

TFIM 的内部 Hamiltonian 为

$$
H_{\mathrm{int}} = -\sum_i\sigma_i^z\sigma_{i+1}^z.
$$

考虑仅作用于格点 $i$ 的酉变换

$$
U_i=\sigma_i^z.
$$

它满足

$$
U_i\sigma_i^xU_i^\dagger=-\sigma_i^x,
$$

但保持内部 Hamiltonian 不变：

$$
U_iH_{\mathrm{int}}U_i^\dagger = H_{\mathrm{int}}.
$$

因此，对于内部密度泛函，单独翻转任意格点横向密度的符号，不应改变内部能量：

$$
\boxed{ F(\rho_1,\ldots,\rho_i,\ldots) = F(\rho_1,\ldots,-\rho_i,\ldots). } \tag{4.6}
$$

为了让 NRC 修正自动满足这一精确对称性，我们定义

$$
\boxed{ u_i=\rho_i^2. } \tag{4.7}
$$

由于

$$
(-\rho_i)^2=\rho_i^2,
$$

使用 $u_i$ 构造的修正项天然保持逐点符号对称性。

同时，定义整体参考密度

$$
\boxed{ r^2=\frac1N\sum_i\rho_i^2. } \tag{4.8}
$$

这里 $r$ 是整个密度分布的均方根（RMS）。

当体系处于正的均匀背景时，

$$
\rho_i=\rho_0>0 \quad\Rightarrow\quad r=\rho_0.
$$

因此，$r$ 可以用来确定非局域核所参照的均匀状态。

这两个选择各自具有明确作用：

$$
\boxed{ \begin{aligned}
u_i=\rho_i^2 &\quad\text{保证符号对称性},\\
r=\sqrt{\langle\rho^2\rangle} &\quad\text{提供密度依赖的参考背景}.
\end{aligned} }
$$

### 4.3 NRC-LDA 的最终泛函

定义平方密度的 Fourier 变换：

$$
u_q=\sum_i e^{-iqi}\rho_i^2.
$$

构造如下非局域修正：

$$
G_{\mathrm{NRC}}[\rho] = \frac1{8Nr^2} \sum_{q\neq0} \Delta K(q;r)|u_q|^2. \tag{4.9}
$$

于是完整 NRC-LDA 泛函为

$$
\boxed{ \begin{aligned}
F_{\mathrm{NRC}}[\boldsymbol\rho] ={}& \sum_i f_{\mathrm{hom}}(\rho_i)\\
&+ \frac1{8Nr^2} \sum_{q\neq0} \Delta K(q;r)|u_q|^2,
\end{aligned} } \tag{4.10}
$$

其中

$$
\boxed{ \begin{gathered}
u_i=\rho_i^2,\qquad u_q=\sum_i e^{-iqi}u_i,\\[3pt]
r^2=\frac1N\sum_i\rho_i^2,\\[3pt]
\Delta K(q;r)= K_{\mathrm{exact}}(q;r)-K_{\mathrm{exact}}(0;r).
\end{gathered} } \tag{4.11}
$$

这是当前研究采用的最终 NRC-LDA 形式。

`TFIM_核心研究与临界适用窗口_含重拟合对照(2).pdf`

它包含两个部分：

$$
\boxed{ F_{\mathrm{NRC}} = \underbrace{F_{\mathrm{LDA}}}_{\text{精确均匀能量}} + \underbrace{G_{\mathrm{NRC}}}_{\text{非局域响应修正}}. }
$$

这里的 $1/(8Nr^2)$ 不是拟合系数，而是为保证二阶 Hessian 精确匹配而确定的归一化因子。

下面直接证明这一点。

### 4.4 证明 NRC 能够精确匹配完整 Hessian

考虑均匀正密度背景附近的小扰动：

$$
\rho_i=r+\eta_i.
$$

由平方密度定义，

$$
u_i=(r+\eta_i)^2 =r^2+2r\eta_i+\eta_i^2.
$$

对于非零动量 $q\neq0$，均匀常数项的 Fourier 分量为零，因此

$$
\boxed{ u_q=2r\eta_q+O(\eta^2). } \tag{4.12}
$$

代入 NRC 修正：

$$
\begin{aligned}
G_{\mathrm{NRC}} &= \frac1{8Nr^2}\sum_{q\neq0} \Delta K(q;r)|u_q|^2\\
&= \frac1{8Nr^2}\sum_{q\neq0} \Delta K(q;r)\,4r^2|\eta_q|^2 +O(\eta^3).
\end{aligned}
$$

所以

$$
\boxed{ G_{\mathrm{NRC}}^{(2)} = \frac1{2N}\sum_{q\neq0} \Delta K(q;r)|\eta_q|^2. } \tag{4.13}
$$

这恰好等于式（4.3）中需要补充的二阶能量。

需要注意，严格求导时 $r$ 也随密度改变。但由于 NRC 修正项在均匀背景处从二阶开始，$r$ 以及核的变化只会影响三阶及更高阶项，不改变上述 Hessian。

因此，NRC 的完整二阶能量为

$$
\begin{aligned}
F_{\mathrm{NRC}}^{(2)} &= \frac1{2N}\sum_q \left[ K_{\mathrm{exact}}(0;r) + \Delta K(q;r) \right] |\eta_q|^2\\
&= \frac1{2N}\sum_q K_{\mathrm{exact}}(q;r)|\eta_q|^2.
\end{aligned}
$$

最终得到

$$
\boxed{ K_{\mathrm{NRC}}(q;r) = K_{\mathrm{exact}}(q;r), \qquad \forall q. } \tag{4.14}
$$

由 $K=\chi^{-1}$：

$$
\boxed{ \chi_{\mathrm{NRC}}(q;r) = \chi_{\mathrm{exact}}(q;r). } \tag{4.15}
$$

**这是 NRC-LDA 最重要的理论结果：它能够精确恢复均匀稳定背景下所有动量的静态线性密度响应。**

这里的精确性是关于完整均匀 Hessian 的，而不是关于任意非均匀密度下的整个精确泛函。

### 4.5 NRC 是否需要针对每个外场重新构造？

**不需要。NRC 是同一个 TFIM 内部 Hamiltonian 的统一密度泛函。**

这是理解 NRC 与一般密度泛函理论关系时非常重要的一点。

对任意给定的非均匀外场 $\boldsymbol g$，我们都使用同一个

$$
F_{\mathrm{NRC}}[\rho].
$$

只需要改变总能量中的外场耦合项：

$$
\boxed{ \mathcal E_{\mathrm{NRC}}[\rho;\boldsymbol g] = F_{\mathrm{NRC}}[\rho] -\sum_i g_i\rho_i. } \tag{4.16}
$$

例如，对两种不同外场：

$$
g_i^{(A)}=1.1+\lambda\cos(qi),
$$

$$
g_i^{(B)}=0.9+\lambda\cos(2qi),
$$

分别求解

$$
\rho^{(A)} = \operatorname*{arg\,min}_{\rho} \left[ F_{\mathrm{NRC}}[\rho] -\sum_i g_i^{(A)}\rho_i \right]
$$

和

$$
\rho^{(B)} = \operatorname*{arg\,min}_{\rho} \left[ F_{\mathrm{NRC}}[\rho] -\sum_i g_i^{(B)}\rho_i \right].
$$

这两个问题使用的是**完全相同的内部泛函**。

那么为什么计算过程中还需要更新 $\Delta K(q;r)$？

因为

$$
r=\sqrt{\frac1N\sum_i\rho_i^2}
$$

本身是密度的函数。

当优化器改变试探密度时，

$$
\boxed{ \rho^{(n)} \longrightarrow r^{(n)} \longrightarrow \Delta K(q;r^{(n)}) \longrightarrow \text{新的能量与梯度}. }
$$

这是对同一个密度依赖泛函进行求值，并不是针对外场重新拟合或重新发明一个泛函。

实际计算时，可以预先通过精确均匀 TFIM 建立

$$
\Delta K(q;r)
$$

的数值表，优化时通过插值查询。

因此要区分：

$$
\boxed{ \begin{aligned}
&\text{不同外场：改变变分问题},\\
&\text{不同试探密度：改变 }r\text{ 和核的取值},\\
&\text{泛函本身：始终保持同一定义}.
\end{aligned} }
$$

这一点与普通电子 DFT 中同一个内部泛函 $F[n]$ 适用于不同外势的思想完全一致。

### 4.6 NRC 的完整变分方程

为了预测非均匀密度，我们需要求解

$$
\frac{\partial F_{\mathrm{NRC}}}{\partial\rho_i} =g_i.
$$

由于 NRC 的核依赖 $r$，而 $r$ 又依赖所有格点的密度，所以求导时必须考虑这种间接依赖。

为简化表达，定义

$$
z_i=\frac{\rho_i^2}{r^2}-1,
$$

以及

$$
w_i= \operatorname{IFFT} \left[\Delta K(q;r)z_q\right]_i,
$$

其中 Fourier 变换采用前文的归一化约定。

再定义

$$
S_0= \sum_{q\neq0} \Delta K(q;r)|z_q|^2,
$$

$$
S_1= \sum_{q\neq0} \frac{\partial\Delta K(q;r)}{\partial r} |z_q|^2.
$$

利用

$$
\frac{\partial r}{\partial\rho_i} = \frac{\rho_i}{Nr},
$$

对式（4.10）完整求导，得到

$$
\boxed{ \frac{\partial F_{\mathrm{NRC}}}{\partial\rho_i} = f_{\mathrm{hom}}'(\rho_i) +\frac{\rho_i}{2}w_i +\frac{\rho_i}{N} \left( \frac{rS_1}{8N} -\frac{S_0}{4N} \right). } \tag{4.17}
$$

因此 NRC 的自洽 Euler 方程为

$$
\boxed{ g_i = f_{\mathrm{hom}}'(\rho_i) +\frac{\rho_i}{2}w_i +\frac{\rho_i}{N} \left( \frac{rS_1}{8N} -\frac{S_0}{4N} \right). } \tag{4.18}
$$

它由局域项与非局域修正共同决定。

在均匀密度下，

$$
\rho_i=r,
$$

所有非零动量的 $u_q$ 都消失，因此

$$
w_i=S_0=S_1=0.
$$

Euler 方程退化为

$$
g=f_{\mathrm{hom}}'(r),
$$

恰好恢复精确均匀关系。

这再次说明：NRC 的非局域修正不会破坏 LDA 已经正确给出的均匀结果。

### 4.7 为什么 NRC 将领先密度误差从一阶降为二阶？

考虑弱非均匀外场：

$$
\boxed{ g_i=g_0+\lambda v_i, \qquad \lambda\to0. } \tag{4.19}
$$

设背景 $g_0\neq1$，并且所研究的自洽分支稳定、光滑。

精确密度可以展开为

$$
\rho_{\mathrm{exact}} = \rho_0 +\lambda\chi_{\mathrm{exact}}v +\lambda^2\rho_{\mathrm{exact}}^{(2)} +O(\lambda^3). \tag{4.20}
$$

近似泛函的密度为

$$
\rho_{\mathrm{app}} = \rho_0 +\lambda\chi_{\mathrm{app}}v +\lambda^2\rho_{\mathrm{app}}^{(2)} +O(\lambda^3). \tag{4.21}
$$

两式相减：

$$
\begin{aligned}
\rho_{\mathrm{app}}-\rho_{\mathrm{exact}} ={}& \lambda(\chi_{\mathrm{app}}-\chi_{\mathrm{exact}})v\\
&+\lambda^2 (\rho_{\mathrm{app}}^{(2)} -\rho_{\mathrm{exact}}^{(2)}) +O(\lambda^3).
\end{aligned} \tag{4.22}
$$

对于 LDA/GGA，一般存在

$$
\chi_{\mathrm{app}}\neq\chi_{\mathrm{exact}},
$$

因此密度误差包含非零的一阶项：

$$
\boxed{ \|\rho_{\mathrm{LDA/GGA}} -\rho_{\mathrm{exact}}\| \sim C_1\lambda. } \tag{4.23}
$$

但对于 NRC，已证明

$$
\chi_{\mathrm{NRC}}=\chi_{\mathrm{exact}}.
$$

因此一阶项严格抵消：

$$
\boxed{ \rho_{\mathrm{NRC}} -\rho_{\mathrm{exact}} = O(\lambda^2). } \tag{4.24}
$$

也就是说：

$$
\boxed{ \text{完整 Hessian 匹配} \Longrightarrow \text{完整线性响应匹配} \Longrightarrow \text{领先一阶密度误差消失}. }
$$

这是 NRC 相较于普通梯度修正最根本的优势。

它不是简单地降低某个固定外场上的误差，而是通过匹配整个均匀 Hessian，消除了稳定背景附近所有弱外场方向上的一阶响应失配。

### 4.8 为什么 NRC 仍然不是精确的完整密度泛函？

因为 Hessian 只决定密度泛函的二阶结构。

在均匀背景附近，精确泛函还包含三阶及更高阶项：

$$
\begin{aligned}
F_{\mathrm{exact}}[r+\eta] ={}&F_0 +\sum_i g_i\eta_i\\
&+\frac12\sum_{ij}K_{ij}\eta_i\eta_j\\
&+\frac1{3!}\sum_{ijk} T_{ijk}^{\mathrm{exact}} \eta_i\eta_j\eta_k+\cdots.
\end{aligned} \tag{4.25}
$$

这里

$$
T_{ijk}^{\mathrm{exact}} = \frac{\partial^3F_{\mathrm{exact}}} {\partial\rho_i\partial\rho_j\partial\rho_k}
$$

表示精确的三阶响应顶角。

NRC 已经满足

$$
K_{ij}^{\mathrm{NRC}} = K_{ij}^{\mathrm{exact}},
$$

但一般不满足

$$
T_{ijk}^{\mathrm{NRC}} = T_{ijk}^{\mathrm{exact}}.
$$

因此，NRC 的二阶及更高阶密度响应仍然可能存在误差。

这就是为什么 NRC 的密度误差通常是

$$
O(\lambda^2),
$$

而不是对任意非均匀外场都完全为零。

另外，由于 NRC 的误差从二阶开始，若比较**同一个 NRC 总能量泛函**在精确密度与 NRC 稳定驻点上的取值，其松弛能量差通常为

$$
\boxed{ \mathcal E_{\mathrm{NRC}}[\rho_{\mathrm{exact}}] - \mathcal E_{\mathrm{NRC}}[\rho_{\mathrm{NRC}}] = O(\lambda^4). } \tag{4.26}
$$

这是由于驻点附近的能量差对密度偏差是二次的。

但必须强调：这个四阶关系不是 NRC 基态总能量相对于真实基态能量的误差阶数。

### 4.9 为什么 NRC 仍然存在临界适用范围？

接近临界点时，

$$
m=|g_0-1|\to0,
$$

体系的响应越来越敏感。

虽然 NRC 消除了线性密度误差，但其剩余误差可以写成

$$
\boxed{ \|\rho_{\mathrm{NRC}}-\rho_{\mathrm{exact}}\| = C_2(m,v)\lambda^2+O(\lambda^3). } \tag{4.27}
$$

这里的系数 $C_2(m,v)$ 依赖临界距离和外场波形，并不保证保持有界。

因此，即使误差对 $\lambda$ 仍然是二阶，它的系数也可能在临界附近变大。

定义相对于实际诱导密度的误差：

$$
\boxed{ \epsilon_\rho = \frac{ \|\rho_{\mathrm{NRC}}-\rho_{\mathrm{exact}}\| }{ \|\rho_{\mathrm{exact}}-\rho_0\| }. } \tag{4.28}
$$

由于弱场诱导密度为

$$
\rho_{\mathrm{exact}}-\rho_0 = \lambda\chi_{\mathrm{exact}}v+O(\lambda^2),
$$

可得

$$
\boxed{ \epsilon_\rho \sim \lambda \frac{C_2(m,v)} {\|\chi_{\mathrm{exact}}v\|}. } \tag{4.29}
$$

因此，NRC 的相对误差不仅取决于微扰幅度 $\lambda$，还取决于临界距离、扰动波长以及剩余高阶响应的大小。

这说明：

**NRC 能精确修复二阶响应，不代表它在严格临界点、有限幅度强场或所有非均匀密度分支上都精确。**

现有研究报告中的临界适用窗口实验正是针对这一问题：检验在给定误差容差下，允许多大的非均匀外场，以及能够逼近临界点多近。

`TFIM_核心研究与临界适用窗口_含重拟合对照(2).pdf`

### 4.10 NRC-LDA 的非局域性与“最小修复”的含义

最后还需要解释：为什么 NRC 的修正称为非局域，以及“最小必要”究竟指什么。

定义逆 Fourier 核：

$$
D_\ell(r)= \frac1N\sum_q \Delta K(q;r)e^{iq\ell}.
$$

则 NRC 修正可以写成实空间形式：

$$
\boxed{ G_{\mathrm{NRC}}[\rho] = \frac1{8r^2} \sum_{i,j} u_iD_{i-j}(r)u_j. } \tag{4.30}
$$

这说明，NRC 修正将不同位置上的平方密度通过核 $D_{i-j}(r)$ 耦合起来。

对于有限范围 GGA，这种耦合仅发生在固定的几个邻近格点之间。

而对于完整 NRC，$D_\ell(r)$ 来自精确的动量响应核，一般具有超出任何固定作用距离的非零尾部。

因此，NRC 是真正意义上的非局域密度泛函。

不过，所谓“最小必要修复”，应理解为：

在已经固定精确均匀 LDA、密度变量及完整均匀 Hessian 匹配要求后，必须补充的二阶信息恰好是

$$
\boxed{ \Delta K(q;r) = K_{\mathrm{exact}}(q;r) - K_{\mathrm{exact}}(0;r). }
$$

**这个二阶核是唯一的，但完整非线性泛函并不唯一。**

平方密度 $u_i=\rho_i^2$ 和 RMS 背景 $r$ 是当前 NRC 选择的、满足对称性和 Hessian 匹配要求的一种简洁非线性延拓。

它们并非由 No-Go 定理单独唯一推出。

### 四种理论结果之间的关系

| 研究内容         | LDA              | GGA              | NRC-LDA            |
| ------------ | ---------------- | ---------------- | ------------------ |
| 均匀 TFIM 能量   | 精确               | 精确               | 精确                 |
| 零动量 Hessian  | 精确               | 精确               | 精确                 |
| 非零动量 Hessian | 使用 $K(0)$ 近似 | 最近邻解析修正          | 精确匹配               |
| 临界非解析响应      | 无法恢复             | 无法完整恢复           | 通过精确核保留            |
| 是否包含经验拟合系数   | 否                | 是                | 否                  |
| 一般弱场密度误差     | $O(\lambda)$ | $O(\lambda)$ | $O(\lambda^2)$ |
| 非线性高阶响应      | 近似               | 近似               | 仍为近似               |
| 是否针对每个外场重构   | 否                | 否                | 否                  |

## 理论总结

整篇理论推导可以凝练为以下逻辑：

**1. 广义自旋 DFT**

$\rho_i=\langle\sigma_i^x\rangle,\quad K=\chi^{-1}$

**2. 精确均匀解构造 LDA**

$e(g)\longrightarrow\rho(g)\longrightarrow f_{\mathrm{hom}}(\rho)$

$\displaystyle K_{\mathrm{LDA}}(q)=K_{\mathrm{exact}}(0)$

**3. No-Go Theorem**

$\displaystyle K_R(q)=K(0)+2\sum_{\ell=1}^{R}b_\ell[1-\cos(\ell q)]$

固定范围无法恢复完整临界响应

**4. NRC-LDA**

$\displaystyle \Delta K(q;r)=K_{\mathrm{exact}}(q;r)-K_{\mathrm{exact}}(0;r)$

$\displaystyle K_{\mathrm{NRC}}(q;r)=K_{\mathrm{exact}}(q;r)$

**领先密度响应误差消除**

$\displaystyle O(\lambda)\longrightarrow O(\lambda^2)$

这项研究的理论贡献可以用一段话完整概括：

> 在一维横场 Ising 模型中，精确均匀基态能量能够构造出对均匀状态完全正确的 LDA，但其 Hessian 缺少动量依赖。固定范围的半局域修正只能产生有限阶三角多项式，因而无法恢复临界点附近精确逆响应的非解析结构及完整交叉标度。为此，我们提出 NRC-LDA：在精确均匀 LDA 基础上，引入由 TFIM 精确静态响应唯一确定的非局域核差，并利用平方密度构造保持局域符号对称性的变分泛函。该泛函不依赖特定非均匀外场，不引入额外经验拟合系数，能够精确匹配所有动量的均匀 Hessian，从而消除稳定背景下弱非均匀外场所导致的领先一阶密度误差。其剩余误差来自尚未精确匹配的高阶非线性响应，因此仍需限定临界距离、扰动幅度和波长的适用范围。

**全文最重要的区别是：精确均匀能量不等于精确非均匀响应；精确 Hessian 也不等于精确完整泛函。NRC-LDA 的理论价值，恰恰在于明确识别并精确修复这两者之间缺失的二阶非局域信息。**
