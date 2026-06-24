---
title: "Thijssen《Computational Physics》笔记其一"
date: 2026-06-24 15:40
categories:
  - Note
tags:
  - Computational Physics
  - Quantum Mechanics
  - Textbook Notes
cover: /assets/images/Note/Thijssen_CP/cover1.jpeg
excerpt: "Thijssen《Computational Physics》第1-2章笔记"
---

Thijssen的这本《Computational Physics》相较于国内绝大多数教材的教学方法有显著的差异，体现在每一章介绍的都是具体情形下的物理问题，并在问题中引入计算方法的思路和应用。

当然这里无意比较两种方式的优劣，只作为纯粹的笔记分享。

另，以下笔记内容包含大量个人解读，还请谨慎食用

## 1. Quantum scattering with a spherically symmetric potential

### 1.1 关于初值

前接量子力学中的分波法，总结一下，现在我们面对的是这么一个问题。在短程低能散射条件下，我们可以对球对称势能进行一个人为的截断

$$V_{\text{截断}}(r) = \begin{cases} V(r), & r \le R \\ 0, & r > R \end{cases}$$

在截断势内我们对要对满足$l < kR$的波函数本征态分别进行相移$\delta_l$的计算以得到微分散射截面

$$f(\theta) = \sum_{l=0}^{\infty} \frac{2l+1}{k} e^{i\delta_l} \sin\delta_l P_l(\cos\theta)$$

截断边界处理应有边界条件的对齐

$$L_{\text{内}} = L_{\text{外}}(R)$$

在截断外边界处我们有

$$u_l(r) \propto \cos\delta_l \hat{j}_l(kr) - \sin\delta_l \hat{n}_l(kr)$$

$$L_{\text{外}}(R) = \frac{u_{\text{外}}'(R)}{u_{\text{外}}(R)} = k \cdot \frac{\cos\delta_l \hat{j}_l'(kR) - \sin\delta_l \hat{n}_l'(kR)}{\cos\delta_l \hat{j}_l(kR) - \sin\delta_l \hat{n}_l(kR)}$$

所以可以得到

$$L_{\text{内}} = k \cdot \frac{\cos\delta_l \hat{j}_l'(kR) - \sin\delta_l \hat{n}_l'(kR)}{\cos\delta_l \hat{j}_l(kR) - \sin\delta_l \hat{n}_l(kR)}$$

反解出$\delta_l$就是理论可行的事情了。

$$\tan\delta_l = \frac{k \hat{j}_l'(kR) - L_{\text{内}} \hat{j}_l(kR)}{k \hat{n}_l'(kR) - L_{\text{内}} \hat{n}_l(kR)}$$

于是于是，问题的关键就是如何计算出 $L_{\text{内}}$ 这玩意，这就真的避不开数值计算了。

事实上求解 $L_{\text{内}}$ 本质上就是数值求解常微分方程

$$\frac{d^2 u_l(r)}{dr^2} + \left[ k^2 - U(r) - \frac{l(l+1)}{r^2} \right] u_l(r) = 0$$

数值求常微分方程的算法倒是不少，但关键在于给一个初值作为迭代的起点。

前面我们提到$U(r)$作为短程势必须以快于$1/r$的速度衰减，下面做一下简单的分类讨论。

对于快于$1/r$但慢于$1/r^2$的势能，我们又可以故技重施，在原点附近狠狠地扔掉小量项，方程变成

$$\frac{d^2 u_l(r)}{dr^2} - \frac{l(l+1)}{r^2} u_l(r) = 0$$

其通解

$$u(r) = C_1 r^{l+1} + C_2 r^{-l}$$

为了波函数不发散，显然$C_2=0$，于是得到关键结论，也就是原点附近满足

$$u(r) \sim r^{l+1} \quad (r \to 0)$$

>（不难验证球贝塞尔原点处的渐进也是同样结论）

于是我们直接在原点附近取个初值$u(h)=h^{l+1}$即可。

而对于其他在原点处强发散的势能，就需要一些更复杂的trick来分析原点附近的渐进行为，比如兰纳-琼斯势

$$V(r) = 4\epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6 \right]$$

在原点附近主导项是一个正比于$1/r^{12}$的玩意，对应着微分方程

$$\frac{d^2 u}{dr^2} = \frac{C}{r^{12}} u$$

尝试使用主导平衡法求其渐进解，假设解的形式为

$$u(r) = e^{S(r)}$$

$$\frac{du}{dr} = S' e^{S}$$

$$\frac{d^2 u}{dr^2} = (S'' + (S')^2) e^{S}$$

$$(S')^2 + S'' = \frac{C}{r^{12}}$$

我们预期 $S(r)$ 及其导数发散得非常快，因此通常满足主平衡条件：$(S')^2 \gg S''$。忽略 $S''$ 项，得到主阶方程

$$(S')^2 \approx \frac{C}{r^{12}}$$

解得主阶项

$$S(r) \approx \mp \frac{\sqrt{C}}{5r^5}$$

这里需要进行一下一致性验证 $(S')^2 \gg S''$ 确保你的假设是可靠的。事实也的确如此。

然后再求一个次级的修正项，设

$$S(r) = \pm \frac{\sqrt{C}}{5r^5} + \phi(r)$$

$$\left( \mp \frac{\sqrt{C}}{r^6} + \phi' \right)^2 + \left( \pm \frac{6\sqrt{C}}{r^7} + \phi'' \right) = \frac{C}{r^{12}}$$

展开并忽略小量项（如 $(\phi')^2$ 和 $\phi''$）

$$\frac{C}{r^{12}} \mp \frac{2\sqrt{C}}{r^6}\phi' \pm \frac{6\sqrt{C}}{r^7} \approx \frac{C}{r^{12}}$$

解得修正项

$$\phi(r) \approx 3 \ln r = \ln(r^3)$$

得到我们想要的渐进解

$$S(r) \approx \mp \frac{\sqrt{C}}{5r^5} + \ln(r^3)$$

$$u(r) \sim e^{\mp \frac{\sqrt{C}}{5r^5} + \ln(r^3)} = r^3 e^{\mp \frac{\sqrt{C}}{5r^5}}$$

也即

$$u(r) \sim c_1 r^3 e^{\frac{\sqrt{C}}{5r^5}} + c_2 r^3 e^{-\frac{\sqrt{C}}{5r^5}}$$

同样的，原点处要求收敛，有$c_1=0$，然后就是一致的思路代入一个初值即可。

### 1.2 关于算法