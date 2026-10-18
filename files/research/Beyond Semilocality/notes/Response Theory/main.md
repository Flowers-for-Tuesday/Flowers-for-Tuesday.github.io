---
title: "DFT的响应理论"
date: 2026-10-09
cover: cover.jpg
summary: "若是我所持有之物，便能交付与你"
---

## 1 / DFT 的 Legendre-transform 结构

HK 定理告诉我们，基态电子密度包含决定基态物理性质所需要的信息。但它本身并没有给出一个一般的构造泛函的方法。根据Levy-Lieb的约束搜索理论，DFT的泛函可以有以下写法

$$
F_{\mathrm{LL}}[n]
=
\inf_{\Psi\rightarrow n}
\langle\Psi|\hat T+\hat W|\Psi\rangle.
$$

而体系的基态能量又是

$$
E[v]
=
\inf_\Psi
\left[
\langle\Psi|\hat T+\hat W|\Psi\rangle
+
\int vn_\Psi
\right].
$$

于是直接得到

$$
\begin{aligned}
E[v]
&=
\inf_n\left\{
\inf_{\Psi\to n}
\left[
\langle\Psi|\hat T+\hat W|\Psi\rangle
+
\int vn
\right]
\right\}\\[4pt]
&=
\inf_n
\left\{
\underbrace{
\inf_{\Psi\to n}
\langle\Psi|\hat T+\hat W|\Psi\rangle
}_{F_{\mathrm{LL}}[n]}
+\int vn
\right\}.
\end{aligned}
$$

$$
E[v]=\inf_{n\in\mathcal I_N}
\left\{
F_{\mathrm{LL}}[n]
+
\int v(\mathbf r)n(\mathbf r)\,d\mathbf r
\right\}.
$$

注意这里把搜索空间从波函数空间变成了密度空间。$\mathcal I_N$ 是所有允许的、可以由某个有限能量 $N$ 电子波函数产生的密度集合，其不一定是某个外势下的基态密度。

相当于说 $F_{\mathrm{LL}}[n]$ 可以定义在更大的密度集合上。详见Lieb [Density functionals for coulomb systems](https://doi.org/10.1002/qua.560240302)

把纯态波函数推广为密度矩阵

$$
\hat\Gamma
=
\sum_k w_k|\Psi_k\rangle\langle\Psi_k|
$$

对应的混合态（或者系综态）电子密度为

$$
n_{\Gamma}(\mathbf r)
=
\operatorname{Tr}\left[
\hat\Gamma\hat n(\mathbf r)
\right].
$$

在固定 $N$ 电子 Hilbert 空间上定义系综泛函

$$
F_{\mathrm{ens}}[n]
=
\inf_{\hat\Gamma\to n}
\operatorname{Tr}\left[
\hat\Gamma(\hat T+\hat W)
\right].
$$

纯态只是密度矩阵的特例，因此

$$
F_{\mathrm{ens}}[n]\leq F_{\mathrm{LL}}[n].
$$

选取两个允许密度 $n_1,n_2$，其对应的混合态为 $\Gamma_1,\Gamma_2$。构造

$$
\Gamma_\lambda
=
\lambda\Gamma_1+(1-\lambda)\Gamma_2,
\qquad 0\leq\lambda\leq1.
$$

$$
n_\lambda=\lambda n_1+(1-\lambda)n_2.
$$

$$
\operatorname{Tr}[\Gamma_\lambda(\hat T+\hat W)]
={}
\lambda\operatorname{Tr}[\Gamma_1(\hat T+\hat W)]
+(1-\lambda)\operatorname{Tr}[\Gamma_2(\hat T+\hat W)].
$$

对满足相应密度约束的态取下确界，可以得到

$$
F_{\mathrm{ens}}[\lambda n_1+(1-\lambda)n_2]
\leq
\lambda F_{\mathrm{ens}}[n_1]
+(1-\lambda)F_{\mathrm{ens}}[n_2].
$$

由此证明系综泛函的凸性。

可以证明将纯态变分空间扩大为所有混合态，并不会降低哈密顿量的全局最低能量。因为混合态能量本质是纯态能量的加权平均，而加权平均不可能低于所有纯态能量的下确界。也即

$$
\begin{aligned}
E_0[v]
&=\inf_n\{F_{\mathrm{LL}}[n]+\langle v,n\rangle\}\\[5pt]
&=\inf_n\{F_{\mathrm{ens}}[n]+\langle v,n\rangle\}.
\end{aligned}
$$

但采用系综泛函的好处是我们可以利用其凸性实现Legendre-transform

$$
F[n]
=
\sup_v\left\{
E[v]-\int v(\mathbf r)n(\mathbf r)\,d\mathbf r
\right\}.
$$

即普适泛函$F[n]$也可以写成对密度约束搜索的形式。但Legendre-transform不会告诉我们更多信息，其本质只是一个恒等变换。

尝试进行外势的微扰$v(\mathbf r)\longrightarrow
v(\mathbf r)+\delta v(\mathbf r)$，哈密顿量的变化为

$$
\delta\hat H
=
\int \delta v(\mathbf r)\hat n(\mathbf r)\,d\mathbf r.
$$

根据一阶微扰论

$$
\delta E
=
\langle\Psi_0|\delta\hat H|\Psi_0\rangle.
$$

于是

$$
\delta E
=
\int n_0(\mathbf r)\delta v(\mathbf r)\,d\mathbf r.
$$

$$
\frac{\delta E[v]}{\delta v(\mathbf r)}
=
n_0(\mathbf r).
$$

再考虑另一种微扰，保持粒子数不变的密度微扰，分析普适泛函$F[n]$的变化

$$
\int n(\mathbf r)\,d\mathbf r=N.
$$

$$
n(\mathbf r)\longrightarrow
n(\mathbf r)+\delta n(\mathbf r)
$$

因为 DFT 的基态密度是一个能量最小化问题的解，而在适当的可微性和约束条件下，泛函在极小值处的一阶变分必须为零。当然这一点需要先满足电子数守恒，所以用拉格朗日乘子引入归一化约束

$$
\mathcal L[n]
=
F[n]+\int vn
-\mu\left(\int n-N\right).
$$

有

$$
\frac{\delta\mathcal L}{\delta n(\mathbf r)}=0.
$$

$$
\frac{\delta F[n]}{\delta n(\mathbf r)}
=
-v(\mathbf r)+\mu.
$$

其中 $\mu$ 来自电子数约束。直观理解就是外势加个常数对密度和波函数本身不会有影响。

以上两个式子整理一下可得共轭关系

$$
\begin{aligned}
n(\mathbf r)
&=\frac{\delta E[v]}{\delta v(\mathbf r)},\\[6pt]
v(\mathbf r)
&=-\frac{\delta F[n]}{\delta n(\mathbf r)}+\mu.
\end{aligned}
$$

## 2 / 响应理论

接着进行更细致的响应分析，考虑一个微小外势扰动

$$
v(\mathbf r)
=
v_0(\mathbf r)+\delta v(\mathbf r).
$$

电子密度随之改变

$$
n(\mathbf r)
=
n_0(\mathbf r)+\delta n(\mathbf r).
$$

定义静态密度响应函数：

$$
\chi(\mathbf r,\mathbf r')
=
\left.
\frac{\delta n[v](\mathbf r)}
{\delta v(\mathbf r')}
\right|_{v_0}.
$$

有线性响应关系

$$
\delta n(\mathbf r)
=
\int
\chi(\mathbf r,\mathbf r')
\delta v(\mathbf r')\,d\mathbf r'.
$$

注意到粒子数守恒，有额外的约束方程

$$
\int\delta n(\mathbf r)\,d\mathbf r=0.
$$

$$
\int d\mathbf r\int d\mathbf r'\,
\chi(\mathbf r,\mathbf r')\delta v(\mathbf r')=0.
$$

$$
\int \chi(\mathbf r,\mathbf r')\,d\mathbf r=0.
$$

另外有常数势是静态响应算符的零模。还可以得到（或者可以直接从对称性？）

$$
\int \chi(\mathbf r,\mathbf r')\,d\mathbf r'=0.
$$

由先前推导的共轭关系，直接推出响应函数就是基态能量泛函对外势的二阶曲率。

$$
\chi(\mathbf r,\mathbf r')
=
\frac{\delta^2E[v]}
{\delta v(\mathbf r)\delta v(\mathbf r')}.
$$

考虑到$E[v]$是外势 $v$ 的凹泛函，如果二阶导数存在，那么自然有

$$
\iint
u(\mathbf r)\chi(\mathbf r,\mathbf r')
u(\mathbf r')\,d\mathbf r\,d\mathbf r'
\leq0
$$

此即响应算符的负半定性。直观理解就是电子密度往往朝着降低外势能量的方向重新分布。另外可以现在可以写出基态能量的展开式

$$
\begin{aligned}
E[v_0+\delta v]
={}&E[v_0]
+\int n_0(\mathbf r)\delta v(\mathbf r)\,d\mathbf r\\
&+\frac12\iint
\delta v(\mathbf r)
\chi(\mathbf r,\mathbf r')
\delta v(\mathbf r')\,
d\mathbf r\,d\mathbf r'\\
&+o(\|\delta v\|^2).
\end{aligned}
$$

另外再来分析普适泛函的扰动，类似的

$$
\frac{\delta F[n+\delta n]}{\delta n(\mathbf r)}
+v(\mathbf r)+\delta v(\mathbf r)
=
\mu+\delta\mu.
$$

$$
\int
\frac{\delta^2F[n]}
{\delta n(\mathbf r)\delta n(\mathbf r')}
\delta n(\mathbf r')\,d\mathbf r'
+
\delta v(\mathbf r)
=
\delta\mu.
$$

令

$$
K_F(\mathbf r,\mathbf r')
=
\frac{\delta^2F[n]}
{\delta n(\mathbf r)\delta n(\mathbf r')}.
$$

$$
K_F\,\delta n+\delta v=\delta\mu.
$$

同样的，这里的$\delta\mu$可以视作是用来抵消$\delta v$中的常数偏移。当然如果是不包含常数偏移的情况（或者把整个式子投影到不含零模的子空间），也可以直接写

$$
K_F\delta n=-\delta v
$$

$$
\displaystyle \chi=-K_F^{-1}
$$

以上严格来说其实并未真正用到DFT理论，但显然对无相互作用下的KS体系完全适用，首先列出KS方程

$$
\left[
-\frac12\nabla^2+v_s[n](\mathbf r)
\right]\phi_i(\mathbf r)
=
\varepsilon_i\phi_i(\mathbf r).
$$

$$
v_s[n]
=
v_{\mathrm{ext}}+v_H[n]+v_{\mathrm{xc}}[n].
$$

$$
v_H[n](\mathbf r)
=
\int
\frac{n(\mathbf r')}{|\mathbf r-\mathbf r'|}
\,d\mathbf r',
$$

$$
v_{\mathrm{xc}}[n](\mathbf r)
=
\frac{\delta E_{\mathrm{xc}}[n]}
{\delta n(\mathbf r)}
$$

假设有效势发生一个小变化导致的轨道变化

$$
v_s\to v_s+\delta v_s.
$$

$$
\phi_i\to\phi_i+\delta\phi_i.
$$

一阶微扰近似下

$$
|\delta\phi_i\rangle
=
\sum_{a\ne i}
|\phi_a\rangle
\frac{
\langle\phi_a|\delta v_s|\phi_i\rangle
}{
\varepsilon_i-\varepsilon_a
}.
$$

$$
n(\mathbf r)=\sum_i f_i|\phi_i(\mathbf r)|^2,
$$

$$
\delta n(\mathbf r)
=
2\operatorname{Re}
\sum_i f_i
\phi_i^*(\mathbf r)\delta\phi_i(\mathbf r).
$$

对比响应函数的展开形式

$$
\delta n(\mathbf r)
=
\int
\chi_s(\mathbf r,\mathbf r')
\delta v_s(\mathbf r')\,d\mathbf r'.
$$

$$
\begin{aligned}
\chi_s(\mathbf r,\mathbf r')
=
-2\operatorname{Re}
\sum_{\substack{i\in\mathrm{occ}\\a\in\mathrm{unocc}}}
\frac{
\phi_i^*(\mathbf r)\phi_a(\mathbf r)
\phi_a^*(\mathbf r')\phi_i(\mathbf r')
}{
\varepsilon_a-\varepsilon_i
}.
\end{aligned}
$$

如果反过来以密度的变化为变量，则注意到Hartree 势和交换关联势的一阶变化是（不需要考虑外势的变化）

$$
\delta v_H(\mathbf r)
=
\int
\frac{\delta n(\mathbf r')}
{|\mathbf r-\mathbf r'|}
\,d\mathbf r'.
$$

$$
\delta v_{\mathrm{xc}}(\mathbf r)
=
\int
f_{\mathrm{xc}}(\mathbf r,\mathbf r')
\delta n(\mathbf r')\,d\mathbf r'.
$$

分别有响应核

$$
f_H(\mathbf r,\mathbf r')
=
\frac{1}{|\mathbf r-\mathbf r'|}.
$$

$$
f_{\mathrm{xc}}(\mathbf r,\mathbf r')
=
\frac{\delta^2E_{\mathrm{xc}}[n]}
{\delta n(\mathbf r)\delta n(\mathbf r')}.
$$

定义 $f_{\mathrm{Hxc}}=f_H+f_{\mathrm{xc}}$，于是

$$
\delta v_s
=
\delta v_{\mathrm{ext}}
+
f_{\mathrm{Hxc}}\delta n.
$$

另一方面

$$
\delta n=\chi_s\delta v_s.
$$

代入

$$
\delta n
=
\chi_s\delta v_{\mathrm{ext}}
+
\chi_s f_{\mathrm{Hxc}}\delta n.
$$

## 3 / 进一步的微扰分析