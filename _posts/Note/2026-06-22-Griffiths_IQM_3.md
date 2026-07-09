---
title: "Scattering"
date: 2026-06-22 11:40
categories:
  - Note
tags:
  - Theoretical Physics
  - Quantum Mechanics
  - Textbook Notes
cover: /assets/images/Note/Griffiths_IQM/cover3.jpg
excerpt: "Don't Wanna Cry，泪非所愿"
---

本文为Griffiths《Introduction to Quantum Mechanics》第十章笔记。

## 1. Introduction

尝试给波函数定义一个叫概率流 $\mathbf{J}$ 的东西，满足流守恒方程

$$\frac{\partial \rho}{\partial t} + \nabla \cdot \mathbf{J} = 0$$

不难知道它的定义式应该可以写成

$$\mathbf{J} = \frac{\hbar}{2mi} \left[ \psi^* \nabla \psi - \psi \nabla \psi^* \right] = \frac{\hbar}{m} \text{Im} \left( \psi^* \nabla \psi \right)$$

如果我们求一下束缚态的概率流，不难发现其结果都是0（束缚态定态波函数总能写成实数）

$$\psi \text{ 是实数} \implies \nabla \psi = \nabla \psi^* \implies \mathbf{J} = \frac{\hbar}{2mi}(\psi \nabla \psi - \psi \nabla \psi) = 0$$

而对于动量的本征态，如果我们尝试求解，会发现

$$\mathbf{J} = |A|^2 \frac{\hbar \mathbf{k}}{m} \neq 0$$

这其实依然可以从系综的角度理解，虽然定态上看每一点的概率密度始终不变，但总是有很多高斯波包以同样的速度流过。而对于束缚态，由于束缚态必定有时间反演对称，因此平均下来总是0。

好了扯远了，这一章要讲散射理论。在中心势场下，解出来的本征波函数是这样的（取振幅为1，懒得归一化）

$$\psi(\mathbf{r}) \approx \underbrace{e^{ikz}}_{\text{入射平面波}} + \underbrace{f(\theta) \frac{e^{ikr}}{r}}_{\text{散射球面波}}$$

啊倒也不是解出来是这样，这其实本质上是个特解（正如平面波$e^{ikz}$是无势场下的一个特解一样），只是的确符合均匀入射粒子的情况。

没错，我们依然可以用最喜欢的系综思想来描述，这其实就是一堆以相同能量入射的高斯波包的系综。

尝试用概率流密度来分析一波，例如其入射粒子流密度，显然是

$$J_{\text{inc}} = \frac{\hbar k}{m} = v$$

在远离中心的径向方向（$r \to \infty$）上，主要考虑梯度的径向部分 $\nabla_r = \frac{\partial}{\partial r}$。将散射球面波 $\psi_{\text{scat}} = f(\theta) \frac{e^{ikr}}{r}$ 代入公式，可得散射粒子流密度

$$J_{\text{scat}} \approx \frac{\hbar k}{m} \frac{|f(\theta)|^2}{r^2} = v \frac{|f(\theta)|^2}{r^2}$$

单位时间内通过该面积的散射粒子数（即通过该立体角的粒子数）为

$$dN = J_{\text{scat}} \cdot dA = \left( v \frac{|f(\theta)|^2}{r^2} \right) \cdot (r^2 d\Omega) = v |f(\theta)|^2 d\Omega$$

联系宏观上微分散射截面的定义，不难发现

$$\frac{d\sigma}{d\Omega} = \frac{1}{J_{\text{inc}}} \frac{dN}{d\Omega} = \frac{1}{v} \cdot (v |f(\theta)|^2) = |f(\theta)|^2$$

## 2. 短程低能散射：Partial Wave Analysis

令 $k^2 = \frac{2mE}{\hbar^2}$ 且 $U(r) = \frac{2mV(r)}{\hbar^2}$，定态薛定谔方程化简为

$$\left[ \nabla^2 + k^2 - U(r) \right] \psi(\mathbf{r}) = 0$$

这种形式一眼看过去肯定可以分离变量成径向乘上球谐函数的形式，于是得到其径向方程（相当于塞进一个势能项的球贝塞尔方程）

$$\frac{d^2 R_l}{dr^2} + \frac{2}{r}\frac{dR_l}{dr} + \left[ k^2 - \frac{l(l+1)}{r^2} - U(r) \right] R_l = 0$$

令$u_l(r) = r R_l(r)$，可得

$$\frac{d^2 u_l(r)}{dr^2} + \left[ k^2 - U(r) - \frac{l(l+1)}{r^2} \right] u_l(r) = 0$$

当 $r \to \infty$ 时，$U(r) \to 0$，径向薛定谔方程在远处的形式退化为自由方程（Riccati-Bessel函数）

吐槽一下怎么有这么多贝塞尔方程和贝塞尔函数。。。

$$\frac{d^2 u_l(r)}{dr^2} + \left[ k^2 - \frac{l(l+1)}{r^2} \right] u_l(r) \approx 0$$

但这毕竟只是简单的变量替换，本质上不是新的方程，通解为球贝塞尔函数的变形

$$u_l(r) = C_1 krj_l(kr) + C_2 kry_l(kr)$$

考虑到我们求的是无穷远处的近似解，这两个函数的渐进展开为

$$j_l(x) \approx \frac{1}{x} \sin\left( x - \frac{l\pi}{2} \right) \quad (x \to \infty)$$

$$y_l(x) \approx -\frac{1}{x} \cos\left( x - \frac{l\pi}{2} \right) \quad (x \to \infty)$$

于是不妨直接将解写作

$$u_l(r) = C_l \sin\left( kr - \frac{l\pi}{2} +\delta_l \right)$$

相移 $\delta_l$ 是一个与角量子数$l$有关的量。

故总波函数可写作（只求关于$z$轴对称的解，因此磁量子数$m=0$）

$$\psi(r, \theta) \xrightarrow{r \to \infty} \sum_{l=0}^{\infty} \frac{C_l}{2ir} \left[ e^{i\left(kr - \frac{l\pi}{2} + \delta_l\right)} - e^{-i\left(kr - \frac{l\pi}{2} + \delta_l\right)} \right] P_l(\cos\theta)$$

另，自由平面波由于也是亥姆霍兹方程的解，故肯定也可以用球贝塞尔函数加球谐函数进行展开，其展开结果为

$$e^{ikz} = e^{ikr\cos\theta} = \sum_{l=0}^{\infty} (2l+1) i^l j_l(kr) P_l(\cos\theta)$$

利用

$$j_l(kr) \xrightarrow{r \to \infty} \frac{1}{2ikr} \left[ e^{i\left(kr - \frac{l\pi}{2}\right)} - e^{-i\left(kr - \frac{l\pi}{2}\right)} \right]$$

可得自由平面波在远处的渐近形式

$$e^{ikz} \xrightarrow{r \to \infty} \sum_{l=0}^{\infty} (2l+1) i^l \frac{1}{2ikr} \left[ e^{i\left(kr - \frac{l\pi}{2}\right)} - e^{-i\left(kr - \frac{l\pi}{2}\right)} \right] P_l(\cos\theta)$$

联系我们先前提到的远场通解形式（严格来说是特解，因为只有一个方向）

$$\psi(r, \theta) \approx e^{ikz} + f(\theta)\frac{e^{ikr}}{r}$$

左右分别代入我们前面求出的式子，即

$$\sum_{l=0}^{\infty} \frac{C_l}{2ir} \left[ e^{i\left(kr - \frac{l\pi}{2} + \delta_l\right)} - e^{-i\left(kr - \frac{l\pi}{2} + \delta_l\right)} \right] P_l = \sum_{l=0}^{\infty} (2l+1) i^l \frac{1}{2ikr} \left[ e^{i\left(kr - \frac{l\pi}{2}\right)} - e^{-i\left(kr - \frac{l\pi}{2}\right)} \right] P_l + f(\theta)\frac{e^{ikr}}{r}$$

对比 $e^{-ikr}$ 系数得到方程

$$\frac{C_l}{2ir} e^{-i\delta_l} = (2l+1) e^{i\frac{l\pi}{2}} \frac{1}{2ikr}$$

从而解得系数 $C_l$

$$C_l = \frac{2l+1}{k} i^l e^{i\delta_l}$$

代入后对比 $e^{ikr}$ 系数得到方程

$$\sum_{l=0}^{\infty} \frac{2l+1}{2ik} i^l e^{2i\delta_l} e^{-i\frac{l\pi}{2}} P_l(\cos\theta) = \sum_{l=0}^{\infty} \frac{2l+1}{2ik} i^l e^{-i\frac{l\pi}{2}} P_l(\cos\theta) + f(\theta)$$

$$\sum_{l=0}^{\infty} \frac{2l+1}{2ik} e^{2i\delta_l} P_l(\cos\theta) = \sum_{l=0}^{\infty} \frac{2l+1}{2ik} P_l(\cos\theta) + f(\theta)$$

$$f(\theta) = \sum_{l=0}^{\infty} \frac{2l+1}{2ik} \left( e^{2i\delta_l} - 1 \right) P_l(\cos\theta)$$

$$f(\theta) = \sum_{l=0}^{\infty} \frac{2l+1}{k} e^{i\delta_l} \sin\delta_l P_l(\cos\theta)$$

此即散射振幅标准公式，也即经典意义上的微分散射截面。

总散射截面是对全立体角进行积分

$$\sigma = \int_{0}^{2\pi} d\phi \int_{0}^{\pi} |f(\theta)|^2 \sin\theta d\theta = 2\pi \int_{-1}^{1} |f(\theta)|^2 d(\cos\theta)$$

利用

$$\int_{-1}^{1} P_l(\cos\theta) P_{l'}(\cos\theta) d(\cos\theta) = \frac{2}{2l+1} \delta_{ll'}$$

可得

$$\sigma = 2\pi \sum_{l=0}^{\infty} \left( \frac{2l+1}{k} \sin\delta_l \right)^2 \cdot \frac{2}{2l+1}$$

$$\sigma = \frac{4\pi}{k^2} \sum_{l=0}^{\infty} (2l+1) \sin^2\delta_l$$

此即分波法得到的总散射截面计算公式。

这里自己又想多说两句了，我们用系数对齐求出了一堆东西，好像很有意义对吧。实际上呢，这件事情的本质只是用通解的基底表示特解而已。至于求散射截面等物理量，说到底这和定义没什么区别，我们之所以求它，是因为它可测量，可被验证，说到底是因为人类的局限性才得以有其真正的价值，否则本质上就是数学上的游戏而已。

另外，以上推导看似行云流水，实则有以下几个不可忽略的问题。

第一个问题是相位问题，回看径向方程

$$\frac{d^2 R_l}{dr^2} + \frac{2}{r}\frac{dR_l}{dr} + \left[ k^2 - \frac{l(l+1)}{r^2} - U(r) \right] R_l = 0$$

我们认为$U(r)$在无穷远衰减，剩余一个球贝塞尔方程，但事实上这至少要求$U(r)$衰减速度比 $\frac{l(l+1)}{r^2}$ 要更快。否则我们没理由认为无穷远处满足的是球贝塞尔方程。

但其实是不是球贝塞尔函数并不是问题的关键，事实上我们回看方程

$$\frac{d^2 u_l(r)}{dr^2} + \left[ k^2 - \frac{l(l+1)}{r^2} \right] u_l(r) \approx 0$$

直接近似到零阶

$$\frac{d^2 u_l(r)}{dr^2} + k^2  u_l(r) \approx 0$$

这得到的就是一个纯振荡。任何衰减的势能在无穷远处肯定都是这样的结果，$R_l(r)$ 肯定会以$1/r$的速率衰减，这也是不争的事实。等等，那我们刚才一通操作实在干嘛？势能的作用究竟体现在哪？答案其实是在$\delta_l$。

球贝塞尔的渐进展开是

$$j_l(x) \approx \frac{1}{x} \sin\left( x - \frac{l\pi}{2} \right) \quad (x \to \infty)$$

$$y_l(x) \approx -\frac{1}{x} \cos\left( x - \frac{l\pi}{2} \right) \quad (x \to \infty)$$

这启示我们，如果势能以$1/r^2$的速度衰减，那么相位的变化是收敛成一个定值的。更快的衰减肯定也是同理。事实上我们可以使用WKB近似进行分析

$$\phi(r) = \int^r k(r') dr' = \int^r \sqrt{\frac{2m}{\hbar^2}(E - V(r'))} dr'$$

相位差 $\Delta \phi$，就是有势场时的总相位减去无势场时的总相位

$$\Delta \phi = \phi(r) - \phi_0(r) = \int^r \left[ k(r') - k_0 \right] dr'$$

散射对应的高能情况（高能是相较于势能的束缚态基态能级而言）下，将 $k(r') = k_0 \sqrt{1 - \frac{V(r')}{E}}$ 按照前面相同的办法在 $V \ll E$ 处进行一阶泰勒展开

$$k(r') - k_0 \approx - \frac{V(r')}{\hbar v}$$

$$\Delta \phi = - \int^r \frac{V(r')}{\hbar v} dr'$$

这意味着只有当势能以比$1/r$更快的速度衰减，$\Delta \phi$才不至于发散。

换言之对于方程

$$\frac{d^2 u_l(r)}{dr^2} + \left[ k^2 - U(r) - \frac{l(l+1)}{r^2} \right] u_l(r) = 0$$

如果是$1/r$形式的势能，那么虽然远场下依然几乎是$e^{ikr}$形式的振荡，但是其相位累计并不会在远程收敛，$\delta_l$始终是$r$的函数。于是前面的一系列操作彻底失效。

而对于其他短程势，即使通解没法写成球贝塞尔函数，但是渐进展开确实一致的，都满足

$$\text{未知势能的解 } R_l(r) \xrightarrow{r \to \infty} \frac{C}{r} \sin\left( kr - \delta_l \right)$$

第二个问题，虽然我们成功把散射截面用不同角量子数波函数的相移$\delta_l$成功表示了出来，但这并不意味着相移本身是一个容易求出来的东西。

以刚性硬球散射为例，其波函数边界条件为 $u_l(R) = 0$。外区（$r > R$）： 势能严格为 0，方程退化为自由方程，其严格通解正如我们前面推导的，是 Riccati-Bessel 函数的任意线性组合

$$u_l(r) = C_1 \hat{j}_l(kr) + C_2 \hat{n}_l(kr)$$

为了引入相移，我们通常将系数重写为含有 $\delta_l$ 的参数化形式

$$u_l(r) \propto \cos\delta_l \hat{j}_l(kr) - \sin\delta_l \hat{n}_l(kr)$$

这么假设可以使其满足无穷远渐进的 $\sin(kr - \frac{l\pi}{2} + \delta_l)$ 形式

在 $r=R$ 处，内外区波函数必须连续。

$$\cos\delta_l \hat{j}_l(kR) - \sin\delta_l \hat{n}_l(kR) = 0$$

移项对齐得

$$\tan\delta_l = \frac{\hat{j}_l(kR)}{\hat{n}_l(kR)} = \frac{j_l(kR)}{-n_l(kR)}$$

这属于少数我们可以的的确确写出来相移表达式的模型。多数势场大多还是需要通过数值计算的方式求出相移，我们又知道

$$f(\theta) = \sum_{l=0}^{\infty} \frac{2l+1}{k} e^{i\delta_l} \sin\delta_l P_l(\cos\theta)$$

$$\sigma = \frac{4\pi}{k^2} \sum_{l=0}^{\infty} (2l+1) \sin^2\delta_l$$

因为数值计算很麻烦，所以我们希望求和号 $\sum_{l=0}^{\infty}$ 在项数很少（比如只有 $l=0$ 或 $l=1$）时就截止。否则计算成千上万个相移 $\delta_l$的成本太高了。

做个简单的估算，我们知道粒子角动量为

$$L = p \cdot b = \hbar k \cdot b$$

又因为角动量被量子化为 $L =\sqrt{l(l+1)}\hbar \approx \hbar l$，若给势场定一个有效半径$R$反映收敛速度

$$\hbar k \cdot b \approx \hbar l \implies b \approx \frac{l}{k}$$

这意味着角量子数大于$kR$的波函数其实就等价于以大于有效半径入射的粒子，这样的粒子几乎不会被散射。也就是说它们的相移 $\delta_l$ 约等于零。这意味着其对微分散射截面$f(\theta)$的贡献几乎全部集中在$\theta = 0$处，当计算其他角度的微分散射截面时，自然只需要截取前几项即可。这也是为什么说分波法适用于短程低能散射。

根据这个思路，我们完全可以在每个人为设定的$R$处进行势能截断

$$V_{\text{截断}}(r) = \begin{cases} V(r), & r \le R \\ 0, & r > R \end{cases}$$

只考虑前几项波函数，这样算出来的微分散射截面除了在$\theta=0$附近之外，和真实的几乎没什么差别。

后续内容出门右转Thijssen的计算物理笔记。

## 3. The Born Approximation

