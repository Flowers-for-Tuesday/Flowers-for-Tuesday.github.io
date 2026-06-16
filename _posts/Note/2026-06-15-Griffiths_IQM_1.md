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

##  1.Nondegenerate Perturbation Theory

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

你可能会问$|n^{(0)}\rangle$的成分应该如何计算，事实上我们可以在$|n^{(1)}\rangle$中任意加入$|n^{(0)}\rangle$的成分，肯定还是会符合薛定谔方程（一如薛定谔方程解乘上一个系数肯定还是方程的解），这会在归一化后等效为乘以一个相位因子，不会改变物理实质，因此我们一般将其系数取0。

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