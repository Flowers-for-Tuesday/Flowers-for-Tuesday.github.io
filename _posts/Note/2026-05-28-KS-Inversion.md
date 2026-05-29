---
title: "论文笔记 Kohn-Sham Inversion"
date: 2026-05-28 21:10
categories:
  - Note
tags:
  - Computational Physics
  - Condensed Matter Physics
cover: /assets/images/Note/KS-Inversion/cover.jpg
excerpt: "人类对DFT的开发程度似乎还未到头"
---

自己接下来的科研应该会偏向DFT方向（虽然具体课题还没确定），总之还是得尽快补充知识。

---

Kohn-Sham Inversion问题，简单来说就是如何在已知基态电子密度$\rho (r)$的前提下，求解KS方程中的等效势分布$v_{eff}(r)$。以下是两篇论文提出的启发性方法。

## 1. Zhao-Morrison-Parr method <sup> [1] </sup>

### 1.1 $v_{xc}$的自洽求解 

 经典的 KS 方程为
 
 $$\left[ -\frac{1}{2}\nabla^2 + v_{\text{ext}}(\mathbf{r})+ v_{\text{H}}(\mathbf{r})+ v_{\text{xc}}(\mathbf{r}) \right] \phi_i = \varepsilon_i \phi_i$$

 这个方程使用自洽法进行求解，但由于$v_{xc}$的形式未知，我们始终无法收敛到真正精确的密度解。现在如果我们转换思路，如果通过实验等手段得到密度分布$n(r)$，是否有可能数值求解得到$v_{xc}(r)$的分布。

 简单的思路是同样找一个能够自洽求解的交换相关势$v_{xc}[n(r),n_{tar}(r)]$，使得迭代过程中解出的波函数$\phi_i(\mathbf{r})$能够逐渐满足约束

 $$\sum_{i=1}^N |\phi_i(\mathbf{r})|^2 = \rho_0(\mathbf{r})$$

 ZMP方法最初按照这个设想，有如下的构造

 $$\left[ -\frac{1}{2}\nabla^2 + v_{ext}(\mathbf{r}) + v_c^\lambda(\mathbf{r}) \right] \phi_i^\lambda = \varepsilon_i^\lambda \phi_i^\lambda$$

 其中$v_c^\lambda(\mathbf{r})$是平均场相互作用能和交换相关能之和，这里直接将二者视作一个整体作为泛函。

 $$v_c^\lambda(\mathbf{r}) = \lambda \int \frac{\rho(\mathbf{r}') - \rho_0(\mathbf{r}')}{|\mathbf{r} - \mathbf{r}'|} d\mathbf{r}'$$

直观理解，对一个固定的$\lambda$，肯定都能通过自洽求解得到最终收敛的波函数$\phi_i^\lambda(\mathbf{r})$以及对应的电子密度$\rho^\lambda(\mathbf{r})$。且随着$\lambda$的增大，$\rho^\lambda(\mathbf{r})$一定会趋于给定的真实密度$\rho_0^\lambda(\mathbf{r})$，以保证总能量不会爆炸。最后通过外推法令$\lambda \rightarrow \infty$不难得到势函数$v_c^\lambda(\mathbf{r})$的数值分布形式。

这个想法倒是没什么问题，但有一个小细节需要优化。既然把电子相互作用的能量等效到一个函数$v_{c}$上，那这个函数必然在远处符合$\sim \frac{N-1}{r}$的衰减形式（即扣除电子自身后的静电势能），这个衰减并不算快，这意味着函数必须在原处也要有比较好的拟合，因此意味着迭代收敛速度会很慢。

论文提出的改进方法将自洽求解方程变成下面的形式

$$\left[ -\frac{1}{2}\nabla^2 + v_{ext}(\mathbf{r}) + \left(1 - \frac{1}{N}\right)v_H(\mathbf{r}) + v_c^\lambda(\mathbf{r}) \right] \phi_i^\lambda(\mathbf{r}) = \varepsilon_i^\lambda \phi_i^\lambda(\mathbf{r})$$

这里的 $\left(1 - \frac{1}{N}\right)v_J(\mathbf{r})$ 即为 Fermi-Amaldi 项。可以看作是（不严谨地）考虑了自相互作用的Hartree势。这么修正后$v_c^\lambda(\mathbf{r})$的衰减速度就会快得多，迭代时更多的优化可以体现在关键的近域部分。

对照标准的 KS 方程，可以得到精确交换相关势的数学表达式

$$v_{\text{xc}}(\mathbf{r}) = \lim_{\lambda \to \infty} \left[ v_c^\lambda(\mathbf{r}) - \frac{1}{N}v_J^\lambda(\mathbf{r}) \right]$$

实际计算中，会通过对一系列大 $\lambda$的结果，对自变量 $1/\lambda \to 0$ 进行多项式外推，从而精确锁定 $v_{\text{xc}}(\mathbf{r})$。

### 1.2 $E_{xc}$的非局域性证明

虽然有些偏题，但论文中有一个有趣的理论证明，这里一并放上。

> 试证：KS理论中的交换相关能泛函$E_{\text{xc}}[\rho]$能否写成定域（Local）形式，即只依赖于某一点的密度值$$E_{\text{local}}[n] = \int f(n(\mathbf{r})) d\mathbf{r}$$

设 $Q[\rho] = \int f(\rho) d\mathbf{r}$ 是一个严格的定域泛函。由于其空间各点独立，对其求变分

$$v_Q(\mathbf{r}) = \frac{\delta Q}{\delta \rho} = \frac{df(\rho)}{d\rho}$$

$f$关于径向坐标 $r$ 的导数为

$$\frac{df(\rho)}{dr} = \frac{df(\rho)}{d\rho} \cdot \frac{d\rho}{dr} = v_Q(\mathbf{r}) \frac{d\rho}{dr}$$

对球对称原子系统，将泛函 $Q$ 在球坐标下展开

$$Q = \int f(\rho) r^2 dr d\Omega$$

为了使用分布积分，设定：

$$u = f(\rho) \implies du = \frac{df}{dr}dr = v_Q \frac{d\rho}{dr} dr$$

$$dv = r^2 dr \implies v = \frac{1}{3}r^3$$

当 $r \to \infty$ 时，电子密度 $\rho \to 0$，导致 $f(\rho) \to 0$。因此边界项 $[uv]_0^\infty$ 严格为 0。代入分部积分公式

$$Q = 0 - \int \left( \frac{1}{3}r^3 \right) \left( v_Q(\mathbf{r}) \frac{d\rho}{dr} \right) dr d\Omega$$

$$Q = -\frac{1}{3} \int v_Q(\mathbf{r}) \cdot r \cdot \left( \frac{d\rho}{dr} \right) \underline{r^2 dr d\Omega} = -\frac{1}{3} \int v_Q(\mathbf{r}) \cdot r \cdot \frac{d\rho}{dr} d\mathbf{r}$$

若令 $Q = E_{\text{xc}}$，则其导数 $v_Q = v_{\text{xc}}$。若 $E_{\text{xc}}$ 是定域的，上式必须强行成立。根据定义

$$E_{xc}[n] \equiv (T[n] - T_s[n]) + (V_{ee}[n] - E_H[n])$$

我们知道，$E$ 和 $T$ 是不依赖任何密度泛函理论的、纯粹的物理真实值。因此完全可以对比真实值和高精度模拟结果以验证局域性的正误

根据论文，二者数值差异很大，否定了局域性假设，这也在意料之内。

![](/assets/images/Note/KS-Inversion/1.png)
 
## 2. Wu-Yang method <sup> [2] </sup>

---

[1] [Q. Zhao, R. C. Morrison, and R. G. Parr, Phys. Rev. A. 50, 2138 (1994).](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.50.2138)

[2] [Q. Wu and W. Yang, J. Chem. Phys. 118, 2498 (2003).](https://pubs.aip.org/aip/jcp/article-abstract/118/6/2498/438646)

