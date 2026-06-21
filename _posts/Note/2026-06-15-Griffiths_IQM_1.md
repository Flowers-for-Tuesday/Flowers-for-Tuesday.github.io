---
title: "Time-Independent Perturbation Theory"
date: 2026-06-15 8:40
categories:
  - Note
tags:
  - Theoretical Physics
  - Quantum Mechanics
  - Textbook Notes
cover: /assets/images/Note/Griffiths_IQM/cover1.jpg
excerpt: "Track in Time，追溯时光"
---

本文为Griffiths《Introduction to Quantum Mechanics》第七章笔记。

##  1. Nondegenerate Perturbation Theory

### 1.1 General Formulation

简单来说，微扰就是这么一个方程

$$(H_0 + \lambda H') |n\rangle = E_n |n\rangle$$

其中 $H_0$ 的本征态 $|n^{(0)}\rangle$ 和本征值 $E_n^{(0)}$ 完全已知。现在关键就是求出微扰后的能量 $E_n(\lambda)$ 和真实的态矢量 $|n\rangle(\lambda)$ ，使用大家都喜欢的小量幂函数展开

$$E_n = E_n^{(0)} + \lambda E_n^{(1)} + \lambda^2 E_n^{(2)} + \dots$$

$$|n\rangle = |n^{(0)}\rangle + \lambda |n^{(1)}\rangle + \lambda^2 |n^{(2)}\rangle + \dots$$

代入原方程

$$(H_0 + \lambda H') \left( |n^{(0)}\rangle + \lambda |n^{(1)}\rangle + \lambda^2 |n^{(2)}\rangle + \dots \right) = \left( E_n^{(0)} + \lambda E_n^{(1)} + \lambda^2 E_n^{(2)} + \dots \right) \left( |n^{(0)}\rangle + \lambda |n^{(1)}\rangle + \lambda^2 |n^{(2)}\rangle + \dots \right)$$

为了让这个等式对任意小量的 $\lambda$ 都成立，等式两边 $\lambda$ 的同次幂系数必须严格相等。

其中零阶方程就是无微扰的薛定谔方程，自然成立。

一阶方程整理如下

$$(H_0 - E_n^{(0)}) |n^{(1)}\rangle = (E_n^{(1)} - H') |n^{(0)}\rangle$$

二阶方程整理如下

$$(H_0 - E_n^{(0)}) |n^{(2)}\rangle = (E_n^{(1)} - H') |n^{(1)}\rangle + E_n^{(2)} |n^{(0)}\rangle$$

求解这些方程，即可得到一阶和二阶近似下修正能量和修正波函数与零阶能量、零阶波函数的关系。

### 1.2 First-Order Theory

先看一阶能量修正，我们在方程 A的两边左乘未微扰态 $\langle n^{(0)} |$

$$\langle n^{(0)} | (H_0 - E_n^{(0)}) |n^{(1)}\rangle = \langle n^{(0)} | (E_n^{(1)} - H') |n^{(0)}\rangle$$

因为 $H_0$ 是厄米算符，有 $\langle n^{(0)} | H_0 = \langle n^{(0)} | E_n^{(0)}$，因此等式左边直接化为 $0$

$$0 = E_n^{(1)} \langle n^{(0)}|n^{(0)}\rangle - \langle n^{(0)} | H' | n^{(0)} \rangle$$

因为 $\langle n^{(0)}|n^{(0)}\rangle = 1$，我们得到一阶能量修正公式

$$E_n^{(1)} = \langle n^{(0)} | H' | n^{(0)} \rangle$$

不难看出这就是微扰算符在原未微扰态上的平均值。

然后是波函数的修正，为了求解 $|n^{(1)}\rangle$，我们可以把它在未微扰态的完备基 $\{|m^{(0)}\rangle\}$ 下进行展开

$$|n^{(1)}\rangle = \sum_{m} c_m |m^{(0)}\rangle$$

我们在一阶方程的两边左乘另一个不同的未微扰态 $\langle m^{(0)} |$（其中 $m \neq n$）

$$\langle m^{(0)} | (H_0 - E_n^{(0)}) |n^{(1)}\rangle = \langle m^{(0)} | (E_n^{(1)} - H') |n^{(0)}\rangle$$

$$(E_m^{(0)} - E_n^{(0)}) \langle m^{(0)} | n^{(1)} \rangle = E_n^{(1)} \langle m^{(0)}|n^{(0)}\rangle - \langle m^{(0)} | H' | n^{(0)} \rangle$$

因为 $m \neq n$，所以 $\langle m^{(0)}|n^{(0)}\rangle = 0$，且 $\langle m^{(0)} | n^{(1)} \rangle = c_m$。带入后得到

$$(E_m^{(0)} - E_n^{(0)}) c_m = - \langle m^{(0)} | H' | n^{(0)} \rangle$$

$$c_m = \frac{\langle m^{(0)} | H' | n^{(0)} \rangle}{E_n^{(0)} - E_m^{(0)}}$$

由此得到一阶波函数修正公式

$$|n^{(1)}\rangle = \sum_{m \neq n} \frac{\langle m^{(0)} | H' | n^{(0)} \rangle}{E_n^{(0)} - E_m^{(0)}} |m^{(0)}\rangle$$

你可能会问$|n^{(0)}\rangle$的成分应该如何计算，事实上我们可以在$|n^{(1)}\rangle$中任意加入$|n^{(0)}\rangle$的成分，不难发现在一阶近似下归一化后波函数是完全不变的。因此为方便起见直接把其取0即可。

### 1.3 Second-Order Energies

有时一阶能量修正计算出来的结果恰好为 $0$。这时我们就必须前进到二阶。

在二阶方程的两边左乘 $\langle n^{(0)} |$

$$\langle n^{(0)} | (H_0 - E_n^{(0)}) |n^{(2)}\rangle = \langle n^{(0)} | (E_n^{(1)} - H') |n^{(1)}\rangle + E_n^{(2)} \langle n^{(0)} | n^{(0)} \rangle$$

同理，左边项因为厄米性化为 $0$，右边展开

$$0 = E_n^{(1)} \langle n^{(0)} | n^{(1)} \rangle - \langle n^{(0)} | H' | n^{(1)}\rangle + E_n^{(2)}$$

因为 $\langle n^{(0)} | n^{(1)} \rangle = 0$，方程简化为

$$E_n^{(2)} = \langle n^{(0)} | H' | n^{(1)}\rangle$$

将前面求得的 $|n^{(1)}\rangle$ 代入上式

$$E_n^{(2)} = \langle n^{(0)} | H' \left( \sum_{m \neq n} \frac{\langle m^{(0)} | H' | n^{(0)} \rangle}{E_n^{(0)} - E_m^{(0)}} |m^{(0)}\rangle \right)$$

最终得到二阶能量修正公式

$$E_n^{(2)} = \sum_{m \neq n} \frac{|\langle m^{(0)} | H' | n^{(0)} \rangle|^2}{E_n^{(0)} - E_m^{(0)}}$$

至于二阶波函数修正，虽然的确可以用同样的方法求出来，但是实用性不大，这里就不作推导了。

##  2. Degenerate Perturbation Theory

显然，虽然我们并没有在前面的推导中提及简并的假设，但从一阶波函数修正中的分母

$$|n^{(1)}\rangle = \sum_{m \neq n} \frac{\langle m^{(0)} | H' | n^{(0)} \rangle}{E_n^{(0)} - E_m^{(0)}} |m^{(0)}\rangle$$

不难看出这个公式对简并态是失效的，因为简并态对应的分母为0。

怎么理解这件事情呢，其实这完全可以用线性代数的视角来思考。前面的推导中其实隐形地包含了一个假设，那就是当哈密顿量$H$发生小量变化是，波函数的本征态发生的变换也是一个小量。从一般线性代数的角度讲，就是当一个矩阵发生一个小的扰动后

$$A'=A_0+\lambda A_1$$

其本征向量的改变量也是一个小量

$$\mathbf{n}'=\mathbf{n_0}+\lambda \mathbf{n_1}$$

这在大多情况下是没问题的，但对有简并的本征向量的矩阵就有点特殊，因为在相同本征值的向量空间中，本征态可以选取空间的任意基底。但是一旦矩阵微扰，微扰后的本征态虽然与先前的向量空间差一个小量，但对某个原先特定的本征态，可就不尽如此了。

这启发我们，对有简并能级的哈密顿量，需要在本征能量的态空间中选取特定的基底，使得微扰后的基底改变仍是一个小量。显然，这个基底应该直接与$H'$的形式相关。

由于先前的非简并理论并没有简并假设，所以其方程仍然是检验简并理论的必要条件，也就是说这组特殊的基底必须至少满足

$$\langle m^{(0)} | H' | n^{(0)} \rangle = 0$$

换言之，假设某已知能级 $E_n^{(0)}$ 具有 $f$ 重简并，对应的本征态为 $|\psi_{n\alpha}^{(0)}\rangle$（其中 $\alpha = 1, 2, \dots, f$）。微扰哈密顿量为 $\hat{H}'$。我们将原本的 $f$ 个简并本征态排成一个行向量（基底向量）

$$|\boldsymbol{\psi}_{n}^{(0)}\rangle = \begin{pmatrix} |\psi_{n1}^{(0)}\rangle, & |\psi_{n2}^{(0)}\rangle, & \dots, & |\psi_{nf}^{(0)}\rangle \end{pmatrix}$$

在旧基底之下，微扰算符对应的矩阵为 $\mathbf{H}'$，其矩阵元为 $\mathbf{H}'_{\alpha\beta} = \langle\psi_{n\alpha}^{(0)}| \hat{H}' |\psi_{n\beta}^{(0)}\rangle$。

现在，问题转换为寻找一个系数矩阵 $C_n$来得到新基底 $|\boldsymbol{\psi}_{n}'^{(0)}\rangle$

$$|\boldsymbol{\psi}_{n}'^{(0)}\rangle = |\boldsymbol{\psi}_{n}^{(0)}\rangle C_n$$

使得新矩阵为对角矩阵

$$\left(\mathbf{H}'_\text{new}\right)_{\alpha\beta} = \langle\psi_{n\alpha}'^{(0)}| \hat{H}' |\psi_{n\beta}'^{(0)}\rangle$$

写成矩阵乘法形式，新矩阵就是

$$\mathbf{H}'_\text{new} = C_n^{\dagger} \mathbf{H}' C_n$$

我们把对角线上的元素（特征值）记为 $\Lambda$

$$\mathbf{H}'_\text{new} = C_n^{\dagger} \mathbf{H}' C_n = \Lambda = \begin{pmatrix} E_1^{(1)} & 0 \\ 0 & E_2^{(1)} \end{pmatrix}$$

直接求解久期方程

$$\det(H' - E^{(1)}I) = 0$$

得到特征值后，结合$C_n$ 幺正矩阵正交归一的特性，可以反向可求得系数矩阵。

于是，接下来的操作和非简并就没什么差异了。

对于一级能量修正，会发现刚好就是我们求出来的本征值$E^{(1)}$

而一级波函数修正变成了$0/0$的不定形

$$|n^{(1)}\rangle = \sum_{n}\sum_{\alpha \ne \beta} \frac{\langle n_{\beta}^{(0)} | H' | n_{\alpha}^{(0)} \rangle}{E_{n_{\alpha}}^{(0)} - E_{n_{\beta}}^{(0)}} |n_{\alpha}^{(0)}\rangle$$

理论上，这里的系数同样可以任意，但这里与先前不同，掺杂后一阶近似下的波函数毫无疑问与先前不同了，但是可以验证，掺杂后的波函数依然是一阶近似下薛定谔方程的解。

不过一般我们直接把这一系数取0。二阶能量修正也是同理。