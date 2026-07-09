---
title: "从逆矩阵到格林函数"
date: 2026-06-23 12:00
categories:
  - Note
tags:
  - Theoretical Physics
  - Mathematical Methods
cover: /assets/images/Note/Green-Function/cover.jpg
excerpt: "与君歌一曲，请君为我倾耳听。"
---

同样是一篇想到哪写到哪的玩意

---

以下只在希尔伯特空间中进行讨论，我不好说能不能推广，留给数学家吧。

随便写个微分方程

$$\frac{d}{dx}f(x) = g(x)$$

这是在干嘛，用线性代数的视角，这是一个矩阵，把希尔伯特空间的位置表象下的一个向量$f$，变换到$g$去。

但你很快发现不止一个向量$f$满足这个方程，因为矩阵$\frac{d}{dx}$本质上是奇异的，换句说它的零空间不只有零向量。任何常数函数$f(x)=C$都满足

$$\frac{d}{dx}C = 0$$

我们知道奇异矩阵意味着方程$Ax=b$不一定有解，但在无限维希尔伯特空间中就比较微妙。此时即使矩阵奇异，但依然可以满足满射。对任意$g(x)$总是能找到$f(x)$的。这是一个比较有趣的点。

因为解空间不为0维，因此就需要有边界条件的存在。边界条件这个东西怎么在线性代数中对应呢，其实本质上就是线性空间的一个约束。常见的约束例如

$$f(x_0)=y_0$$

这本质上是寻找所有希尔伯特空间位置表象中满足$\delta(x-x_0)$基底分量值为$y_0$的函数。有了这个约束，结合线性方程，我们才能得到唯一解。

如果换个基底进行思考，位置表象下的求导算符本质上是傅里叶基底下的一个简单乘法

$$\mathcal{F}(\frac{d}{dx}f) = i\omega \mathcal{F}(f)$$

$i\omega$肯定是一个非奇异变换，那这个过程中常数$C$是怎么自然消失的呢。

注意到

$$\mathcal{F}\{C\} = 2\pi C \cdot \delta(\omega)$$

而$\omega \delta(\omega)$在$\omega=0$处又是一个未定式，你把它取成多少都行。而不同的取值逆变换后直接变成了一个不同的常数，这就导致了解的非唯一性。

而当边界条件恰好与算子的本征基底匹配，也就是说边界条件的约束刚好就是删去一部分本征基底的操作时，数学上就会显得很有美感。例如两段为0的$[0,2\pi]$有限边界，就可以自信地用分立的傅里叶基底$\psi_n(x) = \frac{1}{\sqrt{\pi}} \sin\left(\frac{n}{2}x\right)$进行展开。虽然依然是无限维的空间，但由于不存在$\omega = 0$的基底，所以前面的一系列考量就自然消失了。整个求解就非常优雅自然。

甚至这时候我们完全可以求出矩阵$A = \frac{d}{dx}$的矩阵元

$$A_{ij}=\langle i|A|j\rangle $$

由于$g(x)$可以完备地展开为

$$g(x) = \sum C_n \psi_n(x)$$

如果我们可以对每一个$\psi_n(x)$求出对应的解$f_n(x)$

$$\frac{d}{dx} | f_n \rangle = | \psi_n \rangle$$

则根据线性叠加

$$f(x) = \sum C_n | f_n \rangle$$

注意到$| f_n \rangle$本身也可以被完备基展开

$$| f_n \rangle = \sum B_{nm} | \psi_n \rangle$$

不知你是否看得出来，$B_{nm}$其实就是矩阵$A$的逆矩阵的矩阵元。换句话说

$$f = A^{-1}g = Bg $$

偏微分方程本质上也是做着同样的事情，把多元希尔伯特空间中的向量$f$变成向量$g$。但我们偏爱可变量分离的方程，这对算子本身提出了比较苛刻的要求。

我个人一直觉得氢原子薛定谔方程的求解是偏微分方程的最佳示例，涵盖了偏微分方程求解的绝大多数思想内涵，故我们在此不厌其烦地重写一遍其最基础的求解过程。

写出含时薛定谔方程

$$(\hat{H} - i\hbar \frac{\partial}{\partial t} )\Psi(\mathbf{r}, t) = 0$$

现在从纯数学的视角试着来求解这个方程，也就是说，位置和时间在我们看来都没有本质的差异，都只是偏微分方程的变量之一。这有助于我们洞察方程的本质。

进行算子和解的变量分离

$$\hat{\mathcal{L}}_{total} = \hat{H} \oplus \hat{T} = \hat{H} \otimes I_t + I_{\mathbf{r}} \otimes \hat{T}$$

$$|\Psi\rangle = |\psi\rangle \otimes |f\rangle$$

含时薛定谔方程本质上就是寻找总算子 $\hat{\mathcal{L}}_{total}$ 的零空间。

$$(\hat{H} \oplus \hat{T}) |\Psi\rangle = 0 \cdot |\Psi\rangle$$

设 $|\psi\rangle$ 是 $\hat{H}$ 在 $\mathcal{H}_{\mathbf{r}}$ 上的特征向量，特征值为 $E$；$|f\rangle$ 是 $\hat{T}$ 在 $\mathcal{H}_t$ 上的特征向量，特征值为 $\lambda_t$。

则满足特征值相加等于 $0$

$$E + \lambda_t = 0 \implies \lambda_t = -E$$

这就直接导出了两个空间的独立本征方程

$$\hat{H}|\psi\rangle = E|\psi\rangle$$

$$\hat{T}|f\rangle = -E|f\rangle \implies -i\hbar \frac{d}{dt} f(t) = -E f(t)$$

时间部分的特征向量显而易见

$$f(t) = e^{-\frac{iE}{\hbar} t}$$

> 一个很有趣的想法是，我们写下的物理方程，本质上是物理事实在人类的数学空间表象的体现，但人类的数学空间是完备的吗，没有人知道。