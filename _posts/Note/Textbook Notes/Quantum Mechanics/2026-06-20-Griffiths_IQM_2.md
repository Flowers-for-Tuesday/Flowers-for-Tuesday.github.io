---
title: "Quantum Mechanics // WKB Approximation"
date: 2026-06-20 18:40
categories:
  - Note
tags:
  - Textbook Notes
  - Quantum Mechanics
cover: /assets/images/Note/Textbook%20Notes/Quantum%20Mechanics/Griffiths_IQM_2/cover.jpg
excerpt: "I Don't Know，无知无罪"
---

本文为Griffiths《Introduction to Quantum Mechanics》第九章笔记。

---

## 0. something irrelevant

当我们求解波函数时，其实是在求解一个势能函数对应的所有可能状态。势垒之下，无限处的概率收敛必然要求能级的分立。势垒之上，能量可自由选取，无限远处以平面波的形式存在，其代表的就是自由粒子的运动。

我个人倾向以系综的思想来思考波与粒子的对应关系。以谐振子为例，当某一能级$E_n$的粒子的波函数是这样的

$$\Psi_n(x, t) = \psi_n(x) e^{-i \frac{E_n}{\hbar} t}$$

定态叠加相位旋转因子，就算把它转换到动量空间，也是相似的形式。

这意味着波函数的物理意义，与宏观下的一个粒子在谐振子势下振荡的描述是两回事。更合理的想法是这个值对应着许多相同系统的平均值，也即系综平均。真正让我们惊奇的是微观的一个粒子居然就可以表现出这种宏观上的平均效应（符合直觉的认知应该恰好相反），正如我们难以理解一个动量确定的粒子其位置弥散在全空间一样。

但其实我们可以用另一种视角来思考微观与宏观的对应，那就是用高斯波包来模拟一个宏观粒子。会发现二者在势函数下的运动即为相似（或者说其实宏观粒子就是高斯波包质量趋于无穷的极限）。高斯波包的随时演化过程，几乎和宏观粒子的随时运动完全一致。

我们应该如何理解这两种差异极大的描述形式的共存呢？

哎其实稍微一想就会发现又陷入了唯象的老毛病。事实上任何可以回归公理的问题都不算问题。为什么可以这么解释？因为薛定谔方程告诉我们波函数就应该按照这种形式演化，粒子的状态就是可以用波函数表达。所谓的入射、出射，都是人类先入为主的概念。宇宙怎么知道什么是出射，什么是入射。

如果波函数的初始状态是高斯波包，那么在势场中的出射和入射的确有其意义，因为演化过程的直观表现形式如此。但势场下的定态波函数就没有意义了吗，显然不是的，二者都以同样的逻辑存在，没有任何区别。仅仅是人类没见过而已。（稍微一想就知道“见过”是一种多么局限的观测手段）

更直接地，就是因为人类的宏观世界质量太大了，我们见到的宏观下的态，都是极端形式的高斯波包，导致其对运动的概念就是位置和动量的共同变化。始终用极端视角来观测，自然会对一般的演化带有偏见，这何尝不是一种傲慢。

这么想的话，为什么能量定态这么像宏观的系综呢，具体的原因其实是WKB近似下

$$\psi_n(x) \propto \frac{1}{\sqrt{p(x)}} \implies |\psi_n(x)|^2 \propto \frac{1}{p(x)} = \frac{1}{mv(x)}$$

以至于会有类似运动得快所以待的时间短，所以分布概率低这种不伦不类的解释出现。但此处的$p(x)$虽然长着动量的形式，实则是势场的换种形式写法，尽管其确实是宏观形式下的动量。

什么，你问什么是WKB近似？这就是今天的主题了。

## 1. The “Classical” Region

WKB近似，其实就是半经典近似。我们知道经典判据就是德布罗意波长远小于问题所讨论的尺度，换言之$m \gg 0$或$\hbar \rightarrow 0$。又换言之，对应的其实就是一般波函数的高能级。我们可以用谐振子来近似地理解一下，在谐振子高能级波函数差不多长这样

![](/assets/images/Note/Textbook%20Notes/Quantum%20Mechanics/Griffiths_IQM_2/1.png)

虽然我们知道它的严格解是厄米多项式，但是在半经典近似下，有更为巧妙的求解方法。写出一维定态薛定谔方程

$$\frac{d^2\psi}{dx^2} + \frac{2m}{\hbar^2}\big(E - V(x)\big)\psi(x) = 0$$

为了方便，定义经典局域动量函数 $p(x) = \sqrt{2m(E-V(x))}$。方程简写为

$$\hbar^2 \psi''(x) + p^2(x)\psi(x) = 0$$

$$\psi'' + k^2(x)\psi = 0 \quad \left(k^2(x) = \frac{2m(E-V(x))}{\hbar^2}\right)$$

令

$$\psi(x) = A(x)e^{i\phi(x)}$$

首先对 $\psi$ 求二阶导数

$$\psi' = (A' + iA\phi')e^{i\phi}$$

$$\psi'' = \left[ (A'' - A\phi'^2) + i(2A'\phi' + A\phi'') \right] e^{i\phi}$$

代入原方程并约去 $e^{i\phi}$

$$\left(A'' - A\phi'^2 + k^2(x)A\right) + i\left(2A'\phi' + A\phi''\right) = 0$$

实部

$$A\phi'^2 = k^2(x)A + A'' \implies \phi'^2 = k^2(x) + \frac{A''}{A}$$

虚部

$$2A'\phi' + A\phi'' = 0 \implies \frac{d}{dx}\left(A^2 \phi'\right) = 0$$

注意在转折点的邻域之外，$k(x)$是一个很大的量。这意味着 $\frac{A''}{A}$ 作为0阶是可以忽略的量。

于是积分得到零阶相位

$$\phi(x) = \pm \int k(x')dx' = \pm \frac{1}{\hbar}\int p(x')dx'$$

将解出的 $\phi' = k(x)$ 代入虚部方程

$$\frac{d}{dx}\left(A^2 k(x)\right) = 0 \implies A^2 k(x) = C^2$$

因为 $k(x) \propto p(x)$，所以我们可得振幅直接有该处的动量决定（更严格地说是能量）

$$A(x) = \frac{C}{\sqrt{k(x)}} \propto \frac{1}{\sqrt{p(x)}}$$

把 $A(x)$ 和 $\phi(x)$ 拼回去，得一阶 WKB 解

$$\psi(x) \approx \frac{C}{\sqrt{p(x)}} \exp\left( \pm \frac{i}{\hbar}\int p(x')dx' \right)$$

## 2. Tunneling

转折点就发生在$E=V(x)$的交界处，不过交界点的处理我们先放着，先来定性看看交界外所谓禁区的波函数。从前面的图片不难看到，不存在什么乱七八糟的振荡，就是非常干脆直接的局部隧穿和收敛。

前面的实部虚部方程同样成立

$$A\phi'^2 = k^2(x)A + A'' \implies \phi'^2 = k^2(x) + \frac{A''}{A}$$

$$2A'\phi' + A\phi'' = 0 \implies \frac{d}{dx}\left(A^2 \phi'\right) = 0$$

我们可以玩同样的trick，把这里的 $\frac{A''}{A}$扔掉。但理由与先前的局部平均化不同，这里纯粹是由于$\frac{A''}{A}$的确是个小量。

定义屏障函数 $\kappa(x) = \frac{\sqrt{2m(V(x)-E)}}{\hbar}$。事实上，不妨把WKB解出来的振幅 $A_{\text{WKB}}(x) = \kappa(x)^{-1/2}$ 带回原方程，去严格计算一下被扔掉的 $\frac{A''}{A}$ 到底有多大。屏障函数 $\kappa(x) = \frac{\sqrt{2m(V(x)-E)}}{\hbar}$

根据链式法则，对 $A = \kappa^{-1/2}$ 求二阶导数

$$A' = -\frac{1}{2}\kappa^{-3/2}\kappa'$$

$$A'' = \frac{3}{4}\kappa^{-5/2}(\kappa')^2 - \frac{1}{2}\kappa^{-3/2}\kappa''$$

我们把 $A''$ 除以 $A$

$$\frac{A''}{A} = \frac{3}{4}\left(\frac{\kappa'}{\kappa}\right)^2 - \frac{1}{2}\frac{\kappa''}{\kappa}$$

不难注意到

$$\phi'^2 = \underbrace{\kappa^2(x)}_{\mathcal{O}\left(\frac{1}{\hbar^2}\right)} + \underbrace{\frac{A''}{A}}_{\mathcal{O}(1)}$$

所以半经典近似下，禁区的隧穿衰减是非常快速的，此时忽略尾项确实是合情合理。

## 3. The Connection Formulas

看起来好像目前为止一帆风顺，接下来只要在转折点调一调参数满足归一化和连续性条件，一个看起来合情合理的波函数就诞生了。

个鬼啊，你也没注意看看前面振幅的分母是什么

$$A(x) = \frac{C}{\sqrt{k(x)}} \propto \frac{1}{\sqrt{p(x)}}$$

这玩意在转折点一眼发散，怎么可能是给你调调参就解决的。

事实上可以直接看这张图，会发现转折点处直接爆掉了。

![](/assets/images/Note/Textbook%20Notes/Quantum%20Mechanics/Griffiths_IQM_2/3.png)

这里肯定只能舍弃WKB的做法，转而采用最原始的薛定谔形式，考虑到我们只在转折点$x_0$附近的小区域进行求解，可对势能进行线性近似

$$V(x) \approx V(x_0) + F_0(x - x_0) = E + F_0(x - x_0)$$

斜率 $F_0 = V'(x_0)$

于是原方程化为

$$\frac{d^2\psi}{dx^2} - \frac{2mF_0}{\hbar^2}(x-x_0)\psi = 0$$

这个方程在数学上有严格的解析解，即艾里函数 $\text{Ai}(z)$ 和 $\text{Bi}(z)$。

数学形式有点复杂，直接上图

![](/assets/images/Note/Textbook%20Notes/Quantum%20Mechanics/Griffiths_IQM_2/2.png)

所以我们可以认为转折点附近的函数就是Airy函数$Ai(x-x_0)$的形式，因为$Bi(x)$会发散。

啊？

这是书上一笔带过的解释，同样非常扯淡。凭什么局部的势能近似就可以得到局部的波函数解一致，这也未免太没逻辑了。

这里更合适的说法应该是，我们在寻找一个小局域上的函数，使得其在这个局域满足薛定谔方程

$$\frac{d^2\psi}{dx^2} - \frac{2mF_0}{\hbar^2}(x-x_0)\psi = 0$$

同时在局域外符合WKB提供的边界条件。如果这两个条件都符合，那这个解毫无疑问就是我们需要的解。

条件一使得这个函数的形式只可能是Airy函数，所以关键就是看其如何对齐边界条件。

严格地用Ai函数来对其显然是做不到的，因为我们连函数解析式都写不出来，但在半经典的条件下就稍微有了不同。注意到

$$\psi_{\text{turning}}(x) = a \cdot \text{Ai}(z) = a \cdot \text{Ai}\left[ \alpha (x - x_0) \right] \quad \text{其中 } \alpha = \left(\frac{2mF_0}{\hbar^2}\right)^{1/3}$$

半经典下这个系数$\alpha$足够大，意味着即使是一个小的局域，对Ai函数来说就相当于是其渐进极限。这意味着我们可以不用普适的边界条件，而采用渐进极限条件下的同步来进行边界的对齐。

我们把经典区和禁区的解先摆着

右侧禁区的 WKB 解

$$\psi_{\text{fobidden}}(x) = \frac{D_1}{\sqrt{|p(x)|}} \exp\left( -\frac{1}{\hbar}\int_{x_0}^x |p(x')|dx' \right) + \frac{D_2}{\sqrt{|p(x)|}} \exp\left( +\frac{1}{\hbar}\int_{x_0}^x |p(x')|dx' \right)$$

左侧经典区的 WKB 解

$$\psi_{\text{classical}}(x) = \frac{C_1}{\sqrt{p(x)}} \sin\left( \frac{1}{\hbar}\int_x^{x_0} p(x')dx' \right) + \frac{C_2}{\sqrt{p(x)}} \cos\left( \frac{1}{\hbar}\int_x^{x_0} p(x')dx' \right)$$

$\text{Ai}(z)$ 在 $z \to +\infty$ 时的严格渐近展开式为

$$\text{Ai}(z) \sim \frac{1}{2\sqrt{\pi}z^{1/4}} \exp\left( -\frac{2}{3}z^{3/2} \right)$$

所以，局域艾里解在重叠区右侧的长相为

$$\psi_{\text{turning}} \approx \frac{a}{2\sqrt{\pi}z^{1/4}} \exp\left( -\frac{2}{3}z^{3/2} \right)$$

让其与禁区解严格对齐，形成恒等式

$$\frac{D}{\sqrt{\alpha\hbar} \cdot z^{1/4}} \exp\left( -\frac{2}{3}z^{3/2} \right) = \frac{a}{2\sqrt{\pi}z^{1/4}} \exp\left( -\frac{2}{3}z^{3/2} \right)$$

消去共有项，我们极其精准地锁定了艾里函数的归一化系数 $a$

$$a = \frac{2\sqrt{\pi}}{\sqrt{\alpha\hbar}} D$$

同理， $\text{Ai}(z)$ 在 $z \to -\infty$（即 $\bar{z} \to +\infty$）时的严格振荡渐近展开式为

$$\text{Ai}(-\bar{z}) \sim \frac{1}{\sqrt{\pi}\bar{z}^{1/4}} \cos\left( \frac{2}{3}\bar{z}^{3/2} - \frac{\pi}{4} \right)$$

这意味着

$$\psi_{\text{turning}} = a \cdot \text{Ai}(- \bar{z}) \approx \left(\frac{2\sqrt{\pi}}{\sqrt{\alpha\hbar}} D\right) \cdot \frac{1}{\sqrt{2\pi}\bar{z}^{1/4}} \left[ \sin\left(\frac{2}{3}\bar{z}^{3/2}\right) + \cos\left(\frac{2}{3}\bar{z}^{3/2}\right) \right]$$

与经典区的WKB解对齐，可得

$$C_1 = \sqrt{2}D, \quad C_2 = \sqrt{2}D$$

$$\psi_{\text{WKB}}^{\text{allowed}}(x) = \frac{2D}{\sqrt{p(x)}} \cos\left( \frac{1}{\hbar}\int_x^{x_0} p(x')dx' - \frac{\pi}{4} \right)$$

此即为WKB近似的最终解。在转折点正上方（$x = x_0$），真实的波函数直接由艾里函数在原点的值接管。这是一个确定值

$$\psi(x_0) = \frac{2\sqrt{\pi}D}{\sqrt{\alpha\hbar}} \text{Ai}(0) \approx \frac{2\sqrt{\pi}D}{\sqrt{\alpha\hbar}} \times 0.35503 \neq \infty$$

其实仔细想想会发现这一套连接的想法对非经典的条件应该也适用，例如还是谐振子势，我们可以在一个非常局域的地方对势能线性近似，然后在把该处的波函数用Airy函数表示

$$\psi_i(x) = C_i \text{Ai}(\xi_i) + D_i \text{Bi}(\xi_i)$$

然后在两段进行边界条件的调整，看似有四个边界方程，但是由于线性近似严格求解的Airy函数具有特殊性，所以是可以做到两个参数符合四个方程的。

而半经典近似下，虽然只是宏观的小局域，但是却已经足以达到Airy函数渐进展开的范畴。这就是为什么我们可以用渐进的对齐来达成边界条件的对齐，不难认识到这种可对齐是一种数学上的必然而非偶然。

是啊，肯定只会是必然。没什么值得惊讶的。