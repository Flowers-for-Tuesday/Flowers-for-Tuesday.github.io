---
title: "物理学本科生应该知道的微分几何"
date: 2026-06-05 8:40
cover: cover.jpg
summary: "所以接下来只能一个人加油了，Asuka。"
---

一篇写得比较零散的介绍，也没怎么追求形式上的严谨，不过不会涉及广相等超过四大力学的内容，所以请放心阅读））

参考的材料也很杂，列出主要的几本

[1] 微分几何入门与广义相对论 (梁灿彬, 周彬)

[2] Mathematical Methods of Classical Mechanics (V. I. Arnold)

[3] 电动力学 (刘川)

以及刘川老师和刘雄军老师电动力学课程的讲义 

如果你愿意的话，其实可以不恰当地把学习微分几何看成是学习外语，毕竟其本质是一类数学描述形式，虽然的确提供了新的视角，但我们其实很难单纯从物理体系数学描述上的简洁与否断言其深刻与否 。说人话就是最好不要对其有超越形式的期待。

另，以下默认Einstein求和约定

## 1 / 微分形式

不妨先不引入流形的概念，在简单的$\mathbb{R}^n$中讨论。

设在 $\mathbb{R}^n$ 中，我们有标准的直角坐标系 $(x^1, x^2, \dots, x^n)$，定义有一个标量函数$f(x^1, \dots, x^n)$。

取其全微分 $df = \frac{\partial f}{\partial x^1} dx^1 + \dots + \frac{\partial f}{\partial x^n} dx^n$。这个形式下可以把 $(dx^1, dx^2, \dots, dx^n)$ 视作一组新的基底，而把$df$视作定义于这个空间之上的一个向量。由于基底是一阶微分故而称这类向量为1-形式。其同样可以理解为是把原空间上的一个切向量$(dx^1, dx^2, \dots, dx^n)$映射为一个实数。

用点术语就是点 $p$ 处的 1-形式（或称余切向量）被严格定义为切空间 $T_pM$ 到实数域 $\mathbb{R}$ 的线性映射

$$\omega_p : T_pM \to \mathbb{R}$$

对于1-形式，基底$(dx^1, dx^2, \dots, dx^n)$的完备性似乎不证自明，也就是任意一个这种映射都可以在这个基底下表述出来。证明也并不难，故略过。

类似的这一概念可以扩展，例如2-形式就是接收同一个点上的两个切向量，并将其映射为一个实数。也即

$$\omega_p : T_pM \times T_pM \to \mathbb{R}$$

我们希望同样地把这类映射在一个类似的线性空间中表达，而这么做的前提就是先找到一组基底。为此我们定义外乘积操作，试着把两个1-形式的基底映射为一个2-形式的基底，这里用张量积的反对称化来进行定义

$$dx^i \wedge dx^j = dx^i \otimes dx^j - dx^j \otimes dx^i$$

其作用于两个向量的效果是一个行列式

$$(dx^i \wedge dx^j)(u, v) = \begin{vmatrix} dx^i(u) & dx^i(v) \\ dx^j(u) & dx^j(v) \end{vmatrix} = \begin{vmatrix} u^i & v^i \\ u^j & v^j \end{vmatrix} = u^i v^j - u^j v^i$$

不难验证，由此作为基底定义出来的 2-形式 $\omega_p$ 是一个双线性且反对称的映射。也就是说，其并非完备地能表示所有双线性映射。（换句话说其张成的空间只有 $\frac{n(n-1)}{2}$维而非我们期待的$n^2$维）。

这么定义的好处是我们很容易找到一种1-形式到2-形式的映射。我们知道0-形式的标量函数$f$到1-形式的运算就是简单的微分操作。但如果想接着构造2-形式，对$df$取微分就显得有些意义不明。所以更好的想法是引入新的运算外微分d（尽管我们依然使用同一个符号，但读者应该清楚这已经是完全不同的概念了），其作用为把k-形式映射到k+1形式

$$d: \Lambda^k(M) \to \Lambda^{k+1}(M)$$

而具体的构造方式就是，k-形式在其基底k维边界的累积，就等同于其对于其映射的k+1形式作用在对应k+1维基底的值。

可能有点抽象，，试着用1-形式到2-形式进行举例，假设在$\mathbb{R}^2$上有一个 1-形式

$$\omega = P(x,y)\,dx + Q(x,y)\,dy$$

如果把 1-形式沿边界累加，那么其得到的正好就是对应2-形式$d\omega$作用在面元上的值。

$$\oint_{\partial \Omega} \omega = d\omega = \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dx \wedge dy $$

不难验证这么定义出来的2-形式肯定满足双线性反对称，另一个层面说明了前面使用外乘积基底的完备性。

在这个定义下无边界原理$dd=0$显得不证自明了，因为k形式的外微分定义递推到k+2形式就意味着微元内部相交边界的积分正好一对一对消。

当然必须承认这里的定义是取巧的，因为这相当于直接从Stokes定理

$$\int_{\partial \Omega} \omega = \int_{\Omega} d\omega$$

反过来定义外微分形式。一般教材对外微分的定义是通过几条公理体系得到其计算形式的。但考虑到两种定义的等价性，个人认为本文采用的定义或许更易被接受（大概

## 2 / 流形与张量场

注意到先前的讨论尽管在平直的$\mathbb{R}^n$中讨论，但并没怎么用到其性质。这意味着完全可以合理地把整套理论搬到比较复杂的流形中（例如球面$S^2$），一点值得注意的区别是此时切空间和原空间不再共享同一基底。我们定义此时切空间的基底为 $\left\{ \frac{\partial}{\partial x^1}, \dots, \frac{\partial}{\partial x^n} \right\}$ ，也就是说一个切向量可以如下形式表示

$$v = \sum_{i=1}^n v^i \frac{\partial}{\partial x^i}$$

用这套坐标的好处在于坐标变化下的零成本，能直接套用链式法则进行变换。假设一个向量 $v$，在旧坐标下表示为 $v = \sum_{j} v_x^j \frac{\partial}{\partial x^j}$，在新坐标下表示为 $v = \sum_{i} v_y^i \frac{\partial}{\partial y^i}$。显然有

$$v = \sum_{i} v_y^i \left( \sum_{j} \frac{\partial x^j}{\partial y^i} \frac{\partial}{\partial x^j} \right) = \sum_{j} \left( \sum_{i} v_y^i \frac{\partial x^j}{\partial y^i} \right) \frac{\partial}{\partial x^j}$$

对应项系数必须相等

$$v_x^j = \sum_{i} \frac{\partial x^j}{\partial y^i} v_y^i$$

放过来验证了这套基底的合理性。与此相应的，前面提到的1-形式线性泛函的空间（也即余切空间）的向量，依然采用相同的基底$(dx^1, dx^2, \dots, dx^n)$，可以验证这套基底同样天然满足的坐标变换的一致性，无需额外引入坐标变换规则。

可以直观想象的是，这两类空间在坐标变换中存在本质差异。由于真实流形及其上的切空间/余切空间不依赖于坐标本身，由此在基底向量变化下，对应坐标也发生改变。

以最简单的平直空间上的变换$x_1' = 2x_1$为例，如果流形上一点同时定义了切向量$V$和线性泛函$df$，对应的基底分别为 

$$\mathbf{e}_1 = \frac{\partial}{\partial x}， \mathbf{e}^1 = dx$$

则变换后

$$\mathbf{e}_1' = \frac{\partial}{\partial x'} = \frac{\partial x}{\partial x'} \frac{\partial}{\partial x} = 2 \frac{\partial}{\partial x} = 2\mathbf{e}_1$$

$$\mathbf{e}'^1 = dx' = d\left(\frac{1}{2}x\right) = \frac{1}{2} dx = \frac{1}{2}\mathbf{e}^1$$

故切向量的分量 $v^1$ 变成了原来的 $1/2$（即逆变），线性泛函的分量 $f_1$变成了原来的 $2$ 倍（即协变）。

基于以上的视角，我们完全可以定义一种更加普遍的映射，假设 $M$ 是一个 $n$ 维光滑流形，$p \in M$ 为流形上的一点。$T_pM$ 是其切空间，$T^*_pM$ 是其余切空间。可以定义 点 $p$ 处的 $(r, s)$ 型张量$T$，是一个吃入 $r$ 个余切向量（1-形式）和 $s$ 个切向量，输出一个实数的映射

$$T: \underbrace{T^*_pM \times \dots \times T^*_pM}_{r \text{ 个}} \times \underbrace{T_pM \times \dots \times T_pM}_{s \text{ 个}} \to \mathbb{R}$$

换言之，$(r, s)$ 型张量 $T$ 可以由两类基底的张量积展开为

$$T = \sum_{i_1 \dots i_r} \sum_{j_1 \dots j_s} T^{i_1 \dots i_r}_{j_1 \dots j_s} \; \frac{\partial}{\partial x^{i_1}} \otimes \dots \otimes \frac{\partial}{\partial x^{i_r}} \otimes dx^{j_1} \otimes \dots \otimes dx^{j_s}$$

满足普适的坐标变换规则

$$\tilde{T}^{a_1 \dots a_r}_{b_1 \dots b_s} = \sum_{i_1 \dots i_r} \sum_{j_1 \dots j_s} T^{i_1 \dots i_r}_{j_1 \dots j_s} \left( \frac{\partial y^{a_1}}{\partial x^{i_1}} \dots \frac{\partial y^{a_r}}{\partial x^{i_r}} \right) \left( \frac{\partial x^{j_1}}{\partial y^{b_1}} \dots \frac{\partial x^{j_s}}{\partial y^{b_s}} \right)$$

张量场的概念，即在流形上每一点都定义相同的映射规则，切空间和余切空间由此都可以视作特殊的张量场（分别为(1, 0) 型和(0, 1) 型）。

不过这种广义定义下的形式包含的映射要比先前的外乘积基底定义的形式更大，这也很好理解，例如2-形式空间的张量定义是

$$dx^i \wedge dx^j = dx^i \otimes dx^j - dx^j \otimes dx^i$$

属于满足 $T_{ij} = -T_{ji}$ 的反对称子空间，而非所有(0，2)形式的映射。

## 3 / 度规与张量分析

为了给坐标描述下的流形引入类似距离的概念，需要额外引入度规，毕竟坐标差值与距离之间的关系仍需要人为地进行定义（你需要理解这并不是一件先验的事情，不应该让欧式几何的视角先入为主）

三维为例，平直空间的度规自然定义为

$$ds^2 = dx^2 + dy^2 + dz^2 = \delta_{ij} dx^i dx^j$$

用以表示三个坐标分量的地位完全一致且正交。

更一般地，在局部坐标系 $(x^1, \dots, x^n)$ 下，切基底为 $\mathbf{e}_i = \frac{\partial}{\partial x^i}$。度规张量 $g$ 的分量 $g_{ij}(x)$ 定义为基底算子之间的内积（不难看出是一个$(0,2)$ 型张量场）

$$g_{ij}(x) \equiv g\left(\frac{\partial}{\partial x^i}, \frac{\partial}{\partial x^j}\right)$$

则任意两个切向量 $U = u^i \frac{\partial}{\partial x^i}$ 和 $V = v^j \frac{\partial}{\partial x^j}$ 的内积为

$$g(U, V) = g_{ij} u^i v^j$$

由此微分弧长可以定义为（注意是定义不是计算）

$$ds^2 = \left\langle \sum_i dx^i \frac{\partial}{\partial x^i}, \sum_j dx^j \frac{\partial}{\partial x^j} \right\rangle = g_{ij}(x) dx^i dx^j$$

角度可被定义为

$$\cos \theta \equiv \frac{g_p(u, v)}{\Vert{}u\Vert{} \Vert{}v\Vert{}} = \frac{g_p(u, v)}{\sqrt{g_p(u, u)} \sqrt{g_p(v, v)}}$$

也就是说度规同时定义了基底坐标下的距离和角度的概念。不难看出这样的度规$g_p$ 本质上是切空间 $T_pM$ 上的一个双线性形式

$$g_p: T_pM \times T_pM \to \mathbb{R}$$

而一旦我们定义了流形在一种坐标下的度规，其余坐标的度规规则自然也随之确定，用以确保距离概念的一致性。例如当你从一个已经确定度规的坐标系 $x^\mu$，变换到新坐标系 $y^\alpha$ 时，新坐标的度规自然满足变换

$$g'_{\alpha\beta}(y) = \sum_{\mu, \nu} g_{\mu\nu}(x(y)) \frac{\partial x^\mu}{\partial y^\alpha} \frac{\partial x^\nu}{\partial y^\beta}$$

以确保微分弧长的不变性

$$ds^2 = g_{\mu\nu} dx^\mu dx^\nu = g'_{\alpha\beta} dy^\alpha dy^\beta$$

另外会发现度规张量是一个对称张量（$g_{ij} = g_{ji}$），这意外着它与2-形式虽然都是(0,2)形但彼此独立。

以及可以类似的可以定义逆度规 $g^{ij}$，即余切空间上两个 $1$-形式 $\alpha, \beta$的内积

$$\langle \alpha, \beta \rangle^* = g^{ij} \alpha_i \beta_j$$

不过，其实还有另一种视角。把度规视作从一个切向量到1-形式的映射方式，毕竟没人阻止你这么做。若 $v = v^j \frac{\partial}{\partial x^j}$，那么对应的 $1$-形式 $\alpha_v = v_i dx^i$ 的分量就是

$$v_i = g_{ij} v^j$$

由于度规张量是可逆的，所以可以通过逆度规得到逆变换，满足

$$g^{ij} g_{jk} = \delta^i_k$$

由此得到的切向量和1-形式满足关系

$$\alpha_v(w) \equiv g(v, w)$$

也可以把这种映射用新的符号$\sharp$和$\flat$ 来表示，其符号来源是音乐记谱的升降号

$$ a = v^\flat , v = a^\sharp  $$

尽管d-form的形式数学上已经很自然，但奈何总有人希望将其转化为向量的形式，这种对应自然可以很随意，但最好还是有那么一些基本物理对应方便我们理解（也就是度规）。最直接的例子就是梯度散度旋度。

以梯度为例，其对应0-form下的stokes公式，对一条有向曲线 $\gamma:[a,b]\to M$，广义 Stokes 给出

$$ \int_\gamma df = \int_{\partial\gamma}f = f(\gamma(b))-f(\gamma(a)) $$

引入度规下的对应：

$$ \operatorname{grad}f=(df)^\sharp $$

于是直接等价有

$$\int_\gamma \operatorname{grad}f\cdot d\mathbf l = f(B)-f(A)$$

啊就是说$df$的确作为1-form是数学上客观简洁的形式，是一个更接近本质的存在，但你要在什么具体的语境下解释就是你自己的事了。例如在真实度规对应距离$dl$的语境下你找到的翻译就是$(df)^\sharp$，或者写成展开

$$\operatorname{grad}f = g^{ij}\frac{\partial f}{\partial x^j} \frac{\partial}{\partial x^i}$$

所以类似的有旋度，取向量场$ X\in\Gamma(TM)$，其对应的1-form是$X^\flat$，根据stokes公式有绝对没问题的

$$ \int_{\partial S}X^\flat = \int_SdX^\flat $$

度规语境下左边就是熟悉的环流

$$ \int_{\partial S}X^\flat = \oint_{\partial S}g(X,\dot\gamma)\,dt = \oint_{\partial S}X\cdot d\mathbf l$$

而右侧为了写成某个向量形式在对应区域的面积分，这个向量对应的只能写作

$$ \operatorname{curl}X = (*dX^\flat)^\sharp $$

或者写成更类人形的

$$ (\operatorname{curl}X)^i = \frac1{\sqrt g} \varepsilon^{ijk} \partial_j \left( g_{k\ell}X^\ell \right)$$

但读者应该意识到从微分形式到向量的这一过程一定程度取决于你所考虑的流形的维度，它们是没法具体用同一套映射规则的。例如我们没办法把这里旋度的定义直接挪用到四维中（当然不妨碍我们取寻找一个类似的量）。所以既然我们采用了流形的语言，就应该认识到微分形式这类无需翻译的形式是更加本质的东西。

散度公式留给读者作为练习）

## 4 / 联络与导数

在流形上定义导数是有一点困难的，啊当然0阶张量的比较是trivial的，比较每个点上的值有明确的对应关系。但比较切向量或者微分形式就显得不那么显然，原因是你没法直接把两个点上的切向量或微分形式一一对应进行比较。以切向量为例，假设 $\gamma(t)$ 是一条曲线，$Y$ 是一个向量场。

一般来说我们可能希望定义

$$
\frac{d}{dt}Y_{\gamma(t)} = \lim_{h\to0} \frac{Y_{\gamma(t+h)}-Y_{\gamma(t)}}{h}
$$

但不难注意到这两个向量分别属于不同点处的切空间，减法是没办法良定义的，用球面为例就可以轻松理解。（平直欧式空间的话由于有简单的仿射结构，所以大多时候就直接不过脑子地拿来用了，非要说的话还是有微妙的不严谨性的）

$$
Y_{\gamma(t+h)}\in T_{\gamma(t+h)}M \ , \quad Y_{\gamma(t)}\in T_{\gamma(t)}M
$$

所以这时候得人工对切空间进行对齐，也就是引入联络的概念，尝试给出沿 $\gamma$ 的平行移动映射

$$
P_{\gamma(t)\to p}: T_{\gamma(t)}M\to T_pM
$$

此时 $P_{\gamma(t)\to p}(Y_{\gamma(t)})$ 和 $Y_p$ 都属于同一个向量空间 $T_pM$，才有相减取极限

$$
(\nabla_XY)_p = \lim_{t\to0} \frac{P_{\gamma(t)\to p}Y_{\gamma(t)}-Y_p}{t}
$$

其中 $X$ 为路径 $\gamma(t)$ 在 $t=0$ 处对应的切向量。

展开来就是

$$
\begin{aligned}
\nabla_XY &= \nabla_{X^i\partial_i}(Y^j\partial_j) \\
&= X^i\nabla_{\partial_i}(Y^j\partial_j) \\
&= X^i\left[(\partial_iY^j)\partial_j + Y^j\nabla_{\partial_i}\partial_j\right]
\end{aligned}
$$

引入Christoffel 符号 $\Gamma^k_{ij}$

$$
\nabla_{\partial_i}\partial_j = \Gamma^k_{ij}\partial_k
$$

于是就变成

$$
(\nabla_XY)^k = X^i\partial_iY^k + \Gamma^k_{ij}X^iY^j
$$

所以关键就在于联络 $P$ 本身应该如何定义，对于度规定义良好的体系，一般的方法是采用Levi-Civita 联络，其规定导数满足度规相容和无挠性

$$
\nabla g=0
$$

$$
\nabla_XY-\nabla_YX=[X,Y]
$$

由此的联络可唯一确定，但这并不以为着好算，其对应具体的Christoffel 符号为

$$
\Gamma^k_{ij} = \frac12g^{k\ell}\left(\partial_i g_{j\ell} + \partial_jg_{i\ell} - \partial_\ell g_{ij}\right)
$$

由此会发现度规这个东西是和空间的弯曲有之间联系的，毕竟平庸的度规下平直空间的变换就没那么多麻烦事。但这篇文章就不打算接着介绍曲率的概念。值得一提的是联络本身倒并不一定要依赖度规，如果空间中存在一个辅助的向量场 $X$，注意到一个光滑向量场本身就可以生成流形上的局部运动，这个运动是流形整体的运动（而非单一路径），由此在整体的运动下下一时刻流形的点包括切向量包括微分形式也就都是与原时刻流形一一对应，联络也就自然确定下来。也即

$$
(\mathcal L_XY)_p = \lim_{t\to0} \frac{(d\Phi_{-t})_{\Phi_t(p)}Y_{\Phi_t(p)}-Y_p}{t}
$$

可以证明

$$
\mathcal L_XY = [X,Y] = \left(X^i\frac{\partial Y^k}{\partial x^i} - Y^i\frac{\partial X^k}{\partial x^i}\right)\partial_k
$$

嗯，那么以上。

## e.g.1 / 狭相の电动力学

## e.g.2 / 哈密顿力学和一点辛几何

待施工）））
