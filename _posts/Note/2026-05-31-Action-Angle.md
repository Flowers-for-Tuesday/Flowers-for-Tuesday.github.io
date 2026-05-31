---
title: "Action-Angle Variables"
date: 2026-05-31 7:40
categories:
  - Note
tags:
  - Theoretical Physics
  - Classical Mechanics
cover: /assets/images/Note/Action-Angle/cover.jpg
excerpt: "做了一场三年前的梦。"
---
今天一定会写完作业。

## Ⅰ. 作用量与角变量

回忆一下HJ方程的求解思路，列出偏微分方程

$$H+\frac{\partial S}{\partial t}=0$$

解出来一个含很多待定系数的特征函数$S$

$$S=S(q_\alpha,C_1,C_2...,C_n,t)$$

正则变换告诉我们，我们**可以**把这几个待定参数当作新正则变量的正则动量$P_\alpha$。然后对应的正则坐标可求

$$X_\alpha=\frac{\partial S}{\partial P_\alpha}=X_\alpha(q_\alpha,C_1,C_2...,C_n,t)$$

由于正则变换后的$X$、$P$都为常数，故可反解出运动方程

$$q_\alpha=q(X_\alpha,C_1,C_2...,C_n,t)$$

动量当然也是可以求的

$$p_\alpha=\frac{\partial S}{\partial q_\alpha}=p_\alpha(q(X_\alpha,C_1,C_2...,C_n,t),C_1,C_2...,C_n,t)$$

现在我们把目光放在周期运动上，所谓周期运动有两种，一是$q_\alpha$周期性运动的天平动（想象摆动幅度小的单摆），二是$q_\alpha$周期性增加的转动（想象摆动幅度超过顶点的单摆）。

对这两类运动，我们可以定义作用量

$$I_\alpha = \frac{1}{2\pi}\oint p_\alpha\,\mathrm{d}q_\alpha$$

下面我们来证明在一些特殊的周期运动下，这玩意是守恒的。

注意到先前我们在求解HJ方程时有

$$S=S(q_\alpha,C_1,C_2...,C_n,t)$$

那么把作用量改个写法

$$I_\alpha = \frac{1}{2\pi}\oint \frac{\partial S}{\partial q_\alpha}\,\mathrm{d}q_\alpha $$

现在有一个约束很强的假设，我们假设考虑的周期运动的特征函数可以写作

$$S(q_1...q_n,C_1...,C_n,t) = \sum_{\alpha=1}^n S_\alpha(q_\alpha,C_1,C_2...,C_n,t)$$

那么可以有

$$I_\alpha = \frac{1}{2\pi}\oint \frac{\partial S_\alpha}{\partial q_\alpha}\,\mathrm{d}q_\alpha =I_\alpha(C_1,C_2...,C_n,t)$$

这意味着我们完全可以把特征函数中的待定系数全部替换为作用量，写成

$$S=S(q_\alpha,I_1,I_2...,I_n,t)$$

这个形式显然也满足HJ方程

$$H+\frac{\partial S}{\partial t}=0$$

因此$\vec{I}$是合法的正则动量。

一旦完成了生成函数 $S(\vec{q}, \vec{I})$ 的构造，根据正则变换的微分关系，我们可以通过简单的偏导数直接推导出新坐标——角变量 $\theta_i$

$$\theta_\alpha = \frac{\partial S(\vec{q}, \vec{I})}{\partial I_\alpha} = \sum_{j=1}^n \frac{\partial S_j(q_j; \vec{C})}{\partial C_j} \frac{\partial C_j}{\partial I_\alpha}$$

一般来说我们处理的是不含时的哈密顿量，此时的特征函数可分离

$$S=\sum_{\alpha=1}^n W_\alpha(q_\alpha,I_1,I_2...,I_n) - Et$$

变换后的哈密顿函数

$$K=H+\frac{\partial W}{\partial t}=E(I_1,I_2,...,I_n)$$

能量怎么写成作用量的函数呢，好问题，注意到能量其实是先前$S=S(q_\alpha,C_1,C_2...,C_n,t)$中的一个待定系数，因此自然是可以反解出来$E(I_1,I_2,...,I_n)$的。

什么，你非要知道怎么算？好吧，首先

$$I_\alpha = \frac{1}{2\pi}\oint \frac{\partial W_\alpha}{\partial q_\alpha}\,\mathrm{d}q_\alpha =I_\alpha(E,C_2...,C_n)$$

然后有

$$\begin{cases}
I_1 = I_1(E, C_2, \dots, C_n) \\
I_2 = I_2(E, C_2, \dots, C_n) \\
\vdots \\
I_n = I_n(E, C_2, \dots, C_n)
\end{cases}$$

$E$可反解出来这一点，想必很合理吧。

那么这时候定义出来的角变量变化率为常数

$$\omega_\alpha = \frac{\partial K(\vec{I})}{\partial I_\alpha} = \frac{\partial E}{\partial I_\alpha}$$

因此我们直接对时间 $t$ 进行积分，就能匀速解

$$\theta_\alpha(t) = \omega_\alpha t + \theta_{\alpha 0}$$

这里一通操作不是想证明我们可以用这套正则变量进行运动学方程求解，这只是自找麻烦。我们其实可以发现这个正则坐标，也就是角变量$\omega_\alpha$是有一些内涵的。

我们固定周期内其他广义坐标不变，令其中一个广义坐标$q_i$进行一个周期的变化，则不同角变量的变化量为

$$\Delta_i \theta_j = \oint_{\gamma_i} \mathrm{d}\theta_j = \oint_{\gamma_i} \mathrm{d}\left( \frac{\partial W}{\partial I_j} \right)$$

注意到此时求导顺序可交换

$$\Delta_i \theta_j = \frac{\partial}{\partial I_j} \oint_{\gamma_i} \mathrm{d}W = \frac{\partial}{\partial I_j} \left( \Delta_i W \right)$$

注意到特征函数$W$的微分满足

$$\mathrm{d}W = \sum p_j \,\mathrm{d}q_j$$

因此在该回路下有

$$\Delta_i W = \oint_{\gamma_i} p_i \,\mathrm{d}q_i = 2\pi I_i$$

因此$q_i$转一圈后，对应所有的角变量变化为

$$\Delta_i \theta_j = \frac{\partial}{\partial I_j} (\Delta_i S) = \frac{\partial}{\partial I_j} (2\pi I_i) = 2\pi \delta_{ij}$$

也就是说，当原广义坐标 $q_i$ 完成一个周期的闭合运动时，对应的角变量 $\theta_i$ 恰好精准地增加了 $2\pi$。而先前证明了角变量在对应的广义坐标下是随时间线性增加的，这意味着其变化率

$$\omega_\alpha = \frac{\partial E}{\partial I_\alpha}$$

正是这个广义坐标对应的周期运动的角频率。但与之对应的广义坐标的周期运动可能是奇奇怪怪的形状。直观一点地说，作用量-角变量这组正则变量其实就是在把可能千奇百怪的周期运动，转化为相似的优雅形式。

当然，这要求不同广义坐标的周期运动是解耦的，这在先前特征函数的假设中可见一斑。

## Ⅱ. 浸渐不变量

浸渐是个神奇的翻译，这里的直接内涵是哈密顿量中包含一个随时间极其缓慢变化的参数 $\lambda(t)$（例如单摆的绳长被极其缓慢地拉短）。所谓缓慢，即一个周期内的变化量为小量

$$T\left<\frac{\mathrm{d}\lambda}{\mathrm{d}t}\right> \ll 0 $$

先让我们写一下这个体系的一些基本方程

$$W(q, I, \lambda) = \int p(q, I, \lambda) \,\mathrm{d}q$$

$$p = \frac{\partial W(q, I, \lambda)}{\partial q}, \quad \theta = \frac{\partial W(q, I, \lambda)}{\partial I}$$

由于$W$含时，这时新哈密顿量 $K$ 必须补上对时间的偏导数项

$$K(I, \theta, t) = H(q, p, \lambda) + \frac{\partial W(q, I, \lambda)}{\partial t}$$

$$\frac{\partial W}{\partial t} = \frac{\partial W}{\partial \lambda} \frac{\mathrm{d}\lambda}{\mathrm{d}t} = \dot{\lambda} \frac{\partial W}{\partial \lambda}$$

$$K(I, \theta, t) = E(I, \lambda) + \dot{\lambda} \frac{\partial W(q(I,\theta,\lambda), I, \lambda)}{\partial \lambda}$$

这时来考虑一下作用量的变化率

$$\dot{I} = -\frac{\partial K}{\partial \theta} = -\dot{\lambda} \frac{\partial}{\partial \theta} \left( \frac{\partial W}{\partial \lambda} \right)$$

不难注意到作用量的变化率同样是小量，但我们的目标不止于此，因为小量不意味着长时间累积量也是小量。现在计算对应坐标一个周期 $T$（从 $\theta = 0$ 到 $\theta = 2\pi$）内，作用量 $I$ 的净改变量 $\Delta_T I$

$$\Delta_T I = \int_0^T \dot{I} \,\mathrm{d}t = \int_0^{2\pi} \dot{I} \frac{\mathrm{d}\theta}{\dot{\theta}}$$

$$\Delta_T I = -\int_0^{2\pi} \dot{\lambda} \frac{\partial}{\partial \theta} \left( \frac{\partial W}{\partial \lambda} \right) \frac{\mathrm{d}\theta}{\omega}$$

由于$\lambda$缓变，角变量变化率可视作不变，可做零级近似，有

$$\Delta_T I \approx -\frac{\dot{\lambda}}{\omega} \int_0^{2\pi} \frac{\partial}{\partial \theta} \left( \frac{\partial W}{\partial \lambda} \right) \mathrm{d}\theta$$

老把戏，交换求导

$$\int_0^{2\pi} \frac{\partial}{\partial \theta} \left( \frac{\partial W}{\partial \lambda} \right) \mathrm{d}\theta =  \frac{\partial}{\partial \lambda} \int_0^{2\pi} \mathrm{d}W$$

$$\frac{\partial}{\partial \lambda} \Big( W(\theta = 2\pi) - W(\theta = 0) \Big) = \frac{\partial}{\partial \lambda} (2\pi I) = 0$$

$$\Delta_T I \approx -\frac{\dot{\lambda}}{\omega} \cdot 0 = 0$$

即$\Delta_T I$必然是更高阶的小量，由此作用量长时间内的不变性可保证。