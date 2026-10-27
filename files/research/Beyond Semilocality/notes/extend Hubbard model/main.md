---
title: "论文笔记 / extend Hubbard model的临界性分析"
category: Research Notes
date: 2026-10-24
cover: cover.jpg
summary: "真正严肃的哲学问题只有一个。"
---

# Beyond Semilocality: Quantum-Critical Constraints and Corrections for Density Functionals

**理论研究框架、两项条件性定理、LDA/GGA 修正与双模型验证方案**  
**版本：** 研究设计稿 v1.0（2026-10-19）  
**性质：** 供推导、计算和论文组织使用的研究备忘录；所有“预期结果”均是待验证的理论预测，不是已有数值成果。

> **一句话目标**：证明固定有限范围、光滑的半局域泛函不能精确描述某类非高斯量子临界点的**静态响应 Hessian**；再证明正确的临界非局域修正在**临界点外的特定标度窗口**具有渐近优势，最终在横场 Ising 链与键二聚化扩展 Hubbard 链中，以相同参数预算和样本外测试验证 LDA/GGA 修正的实际预测能力。

---

## 摘要

强关联体系中的局域近似失效与量子临界性引起的泛函失效不是同一问题。本文研究与临界序参量线性耦合的局域观测量之 Legendre 密度泛函。在适当可微及可逆的物理子空间中，精确泛函 Hessian 等于正的零频静态响应的逆：$K=\Gamma^{(2)}=\kappa^{-1}$。若非高斯量子临界点在临界波矢 $Q$ 附近具有 $\kappa(Q+k,0)\sim A_\kappa |k|^{-p}$，$p=2-\eta\in(0,2)$，则临界方向的精确 Hessian 必须具有非解析的 $K(Q+k)\sim A_K|k|^p$。在参考体系逆响应解析的条件下，Hxc 部分必须承载相同非解析结构。

据此给出 **Theorem 1（Critical no-go）**：固定有限邻域、二阶可微的半局域泛函不能精确重现该 Hessian；对于稳定、规则、经充分调谐的近似，其临界长波长 Hessian 相对误差仍趋向 $100\%$，相应静态响应误差不能任意小。再提出 **Theorem 2（Near-critical asymptotic advantage）**：在接近但不等于临界点、相关长度 $\xi\to\infty$ 的路径上，若基线泛函的质量项 $r_{\rm sl}=O(\xi^{-p})$、梯度系数一致有界，则在 $k=\xi^{-s}$、$0<s<1$ 的标度窗口，基线 Hessian 与精确值之比趋于零；正确振幅的 $|k|^p$ 修正使该比值趋于一，从而产生可以严格比较的渐近优势。这不是“所有非临界参数处均更优”的无条件定理。

随后构造能量层面的 **LDA+C/GGA+C** 及带有限 $\xi$ 屏蔽的修正，直接推导对应泛函势、Hessian 和自洽求解形式。首先在以纵向磁化为基本变量的横场 Ising 链中检验，再转移到以 CDW 电荷密度为基本变量的键二聚化扩展 Hubbard 链。实验采取冻结基线、共同质量校准、相同新增参数量、错误指数对照与跨尺寸／跨动量／跨模型独立测试，以排除“仅因参数更多而拟合更好”的解释。

---

## 0. 研究边界：必须区分三种结论

| 层次 | 可以提出什么结论 | 不能由此推出什么 |
|---|---|---|
| 精确 Hessian | 临界点附近某一参考密度的二阶曲率具有规定的非解析动量标度 | 已知整个 $\Gamma[\phi]$ 的全局形式 |
| 有限范围 no-go | 固定有限邻域、光滑的近似不能精确再现指定的非整数幂**静态响应** | LDA/GGA 在临界点必然给出错误的每个基态能量或密度 |
| 修正方案 | 在明确的条件及标度窗口中恢复主导曲率和响应，可能改善自洽预测 | 分数阶核会无条件改善所有非临界态、非线性响应和动力学谱 |

本文的主要观测对象是 **零频静态**响应，不能把等时结构因子直接当作静态 susceptibility；所有结论均需明确临界算符通道、系统尺寸、外场符号及参考体系是否解析。

---

# Part I — 统一精确泛函与临界约束

## 1. 广义密度与 Legendre 对偶：横场 Ising 与 Hubbard 的共同语言

令 $g$ 表示 Hamiltonian 的内禀控制参数，$h_i$ 为外加测试源：

$$
\hat H_g[\mathbf h]=\hat H_g^{(0)}-\sum_i h_i\hat O_i,
\qquad \phi_i=\langle \hat O_i\rangle_{\mathbf h}.
$$

固定 $g$，定义 $E_g[\mathbf h]$、$W_g[\mathbf h]=-E_g[\mathbf h]$ 以及凸共轭：

$$
\Gamma_g[\boldsymbol\phi]
=\sup_{\mathbf h}\left\{\sum_i h_i\phi_i-W_g[\mathbf h]\right\}.
\tag{1}
$$

在局部密度—势对应关系可逆、二阶导数存在的子空间中，

$$
\frac{\partial\Gamma_g}{\partial\phi_i}=h_i,
\qquad
\kappa_{ij}=\frac{\partial\phi_i}{\partial h_j},
\qquad
\boxed{K_g\equiv\Gamma_g^{(2)}=\boldsymbol\kappa^{-1}}.
\tag{2}
$$

正源约定下，$\kappa\succeq0$。电子传统记号使用 $H[v]=H_0+\sum_i v_i n_i$，于是 $h=-v$、$\chi=\partial n/\partial v=-\kappa$，即

$$
F^{(2)}=-\chi^{-1}=\kappa^{-1}.
\tag{3}
$$

**KS／参考体系分解：** 写 $\Gamma=\Gamma_{\rm ref}+E_{\rm Hxc}$，则

$$
\boxed{f_{\rm Hxc}=K-K_{\rm ref}
=\kappa^{-1}-\kappa_{\rm ref}^{-1}}
\tag{4}
$$

对于电子记号等价于 $f_{\rm Hxc}=\chi_s^{-1}-\chi^{-1}$。**必须对完整矩阵求逆，而不是一般地把一个投影响应的倒数当作投影后的逆。** 固定粒子数时需去除均匀外势的 gauge 零模，并在允许的密度扰动子空间中求逆或伪逆。临界点本身可通过有限 $L$、有限 $k$ 的对象定义，再取热力学极限。

## 2. 从 universality class 到泛函 Hessian

设临界局域序参量 $O$ 的 scaling dimension 为 $\Delta_O$，空间维数 $d$、动力学指数 $z$。若该算符的奇异静态响应占主导，则

$$
\kappa_O(Q+k,\omega=0;g_c)
\sim A_\kappa |k|^{-p},
\qquad p=d+z-2\Delta_O.
\tag{5}
$$

对于常用的序参量异常维数定义，$p=2-\eta$。因而

$$
\boxed{K_c(Q+k;g_c)
\sim A_K|k|^p,
\qquad A_K=A_\kappa^{-1}>0.}
\tag{6}
$$

如果参考体系的逆响应在 $Q$ 附近解析，则 $f_{\rm Hxc}$ 必须具有同样的非整数幂奇异部分：

$$
 f_{\rm Hxc}^{\rm sing}(Q+k)\propto|k|^p.
\tag{7}
$$

一维体系中的非局域 Fourier 系数对应

$$
 f_{\rm Hxc}^{\rm sing}(r)
 \propto \frac{\cos(Qr)}{|r|^{1+p}},
 \quad r\to\infty,
\tag{8}
$$

这里省略接触项、解析背景及依赖约定的系数。该尾部属于在指定参考密度处的**二阶核**，不能当作完整泛函的空间展开。

**1+1D Ising：** $z=1$、$\eta=1/4$、$\nu=1$、$p=7/4$。若 $Q=\pi$，则尾部为 $(-1)^r r^{-11/4}$；若 $Q=0$，没有交替因子。作为进一步检验，tricritical Ising 的序参量 $\eta=3/20$ 给出 $p=37/20$。Gaussian $\eta=0$、$p=2$ 则是重要的局域反例：相关长度发散并不必然要求非整数幂核。

---

# Part II — 两项条件性定理

## 3. Theorem 1 — Fixed-range semilocal no-go at a non-Gaussian QCP

### 定理表述

**假设 T1：**

1. 临界点位于单一、稳定且可隔离的密度／序参量通道，且其精确静态逆响应满足
   $K_{\rm exact}(Q+k)=A|k|^p[1+o(1)]$，其中 $A>0$、$0<p<2$；
2. 考察固定有限邻域 $R$ 的半局域修正泛函，局域能量密度在参考态附近至少 $C^2$，其 Hessian 系数在热力学极限有规则的尺寸无关极限；
3. 非相互作用／KS 参考体系在该通道的逆响应解析，且不存在抵消非解析项的参考临界奇异性；
4. 对 $k=0$ 的两侧采用稳定且非负的有效曲率；对于多通道系统，非临界块可逆，并使用正确的临界有效曲率（例如 Schur complement）。

**结论 T1：** 任何上述固定范围半局域修正与解析参考泛函构成的总 Hessian 都不能在 $k=0$ 的开邻域精确等于 $K_{\rm exact}$。更强地，定义

$$
\mathcal E_K(k)
=\left|\frac{K_{\rm sl}(Q+k)}{K_{\rm exact}(Q+k)}-1\right|.
\tag{9}
$$

若近似的零动量曲率 $r=K_{\rm sl}(Q)>0$，则 $\mathcal E_K\to\infty$。若 $r=0$ 且其首个非零的稳定解析项为 $b_{2m}k^{2m}$，$m\ge1$，则

$$
\boxed{\lim_{k\to0}\mathcal E_K(k)=1.}
\tag{10}
$$

因此这一泛函类无法使**整个临界长波长极限**的相对 Hessian 误差任意小。

对响应 $\kappa=K^{-1}$：若 $r>0$，则 $|\kappa_{\rm sl}/\kappa_{\rm exact}-1|\to1$；若 $r=0$ 且 $b_{2m}>0$，则该相对响应误差发散。

### 证明要点

半局域形式

$$
E_{\rm Hxc}^{(R)}[\phi]
=\sum_i\varepsilon_R(\phi_{i-R},\ldots,\phi_{i+R})
\tag{11}
$$

意味着每个局域项无法同时依赖距离超过 $2R$ 的两个格点，因此

$$
 f_{ij}^{(R)}=0\quad(|i-j|>2R),
\qquad
 f^{(R)}(q)=\sum_{r=-2R}^{2R}f_r e^{iqr}.
\tag{12}
$$

右侧是有限三角多项式，必然解析；加上解析参考曲率后仍解析。稳定的非负单通道函数若在 $k=0$ 取零，其首个非零 Taylor 项必须为偶次幂 $k^{2m}$。而 $0<p<2$ 的 $|k|^p$ 非解析，故无法相等；并且

$$
\frac{K_{\rm sl}(Q+k)}{K_{\rm exact}(Q+k)}
\sim\frac{b_{2m}}{A}|k|^{2m-p}\longrightarrow0.
\tag{13}
$$

若 $r>0$，该比值反而 $\sim r/(A|k|^p)\to\infty$。证毕。

**定理范围：** 它不禁止有限体系上的高精度近似，也不禁止正确的单点能量、基态密度或某一相变位置；不适用于非光滑泛函、随系统尺寸增长的邻域、非解析参考体系或 $p=2$ 的 Gaussian 情形。相对于既有场论与 Legendre 理论，本证明本身可能属于直接推论；论文的真正新意应体现在量化的 DFT 后果及修正策略。

## 4. Theorem 2 — Near-critical asymptotic advantage in a scaling window

### 先定义要比较的“临界点外”极限

只从对称侧接近临界点，取 $g\ne g_c$、相关长度 $\xi(g)\to\infty$，设

$$
K_{\rm exact}(k,g)
=A\xi^{-p}\Psi(k\xi)[1+o(1)],
\qquad
\Psi(y)\sim |y|^p\quad(|y|\to\infty),
\tag{14}
$$

其中非普适动量尺度已纳入 $\xi$ 和 $A$。我们研究的并非固定 $g\ne g_c$ 时 $k\to0$，而是双重极限路径

$$
\boxed{k(\xi)=\xi^{-s},\qquad 0<s<1,}
\tag{15}
$$

所以 $k\to0$ 但 $k\xi\to\infty$：始终在**非临界参数的临界标度窗口** $\xi^{-1}\ll |k|\ll a^{-1}$。

### 定理表述

**额外假设 T2：** 在上述路径上，经共同临界质量项校准的固定范围基线，其有效曲率具有一致的解析展开

$$
 K_{\rm sl}(k,g)
 =r_{\rm sl}(g)+b_{\rm sl}(g)k^2+O(k^4),
\quad
 |r_{\rm sl}(g)|\le C_r\xi^{-p},
\quad |b_{\rm sl}(g)|\le C_b,
\tag{16}
$$

且 $O(k^4)$ 余项系数有一致上界；所有参与比较的有效曲率保持适当稳定性。

**结论 T2(a)：** 对 $0<p<2$、$0<s<1$，

$$
\boxed{
\left|\frac{K_{\rm sl}(\xi^{-s},g)}
{K_{\rm exact}(\xi^{-s},g)}\right|
\le O(\xi^{-p(1-s)})
+O(\xi^{-s(2-p)})\longrightarrow0.
}
\tag{17}
$$

因此其 Hessian 相对误差趋于 $1$。如果未进行质量校准，$r_{\rm sl}$ 不满足该上界，则基线可能以另一种方式更严重地失配；这不由式 (17) 自动覆盖。

**结论 T2(b)：** 若增加具有**正确振幅**的普适项，

$$
K_{\rm corr}(k,g)
=K_{\rm sl}(k,g)+A|k|^p
\tag{18}
$$

则沿相同路径，

$$
\boxed{
\frac{K_{\rm corr}(\xi^{-s},g)}
{K_{\rm exact}(\xi^{-s},g)}\longrightarrow1,
\qquad
\mathcal E_K^{\rm corr}\longrightarrow0.
}
\tag{19}
$$

因此对任意指定的足够小的相对误差阈值，足够接近临界点的该标度路径上，修正后的曲率误差最终严格小于上述基线误差。若两个曲率均为正，则相应响应比值也趋于 $1$。

### 证明要点

式 (14)–(15) 导致 $K_{\rm exact}(\xi^{-s},g)=A\xi^{-sp}[1+o(1)]$。逐项估计基线的质量项与梯度项：

$$
\frac{\xi^{-p}}{\xi^{-sp}}=\xi^{-p(1-s)},
\qquad
\frac{\xi^{-2s}}{\xi^{-sp}}=\xi^{-s(2-p)}.
\tag{20}
$$

两者趋零，得式 (17)；加上 $A\xi^{-sp}$ 后得到式 (19)。证毕。

### T2 的准确解释和局限

- **这是一项有条件的、针对特定双重极限的渐近结果，不是“临界点外处处更好”的定理。**
- 如果允许基线梯度系数随 $\xi$ 奇异发散，式 (16) 不成立。若想覆盖这类体系，需要另行研究固定次数解析函数空间对 $x^p$ 的一致逼近下界。
- 式 (18) 在有限 $\xi$ 的极小 $k$ 区域保留非解析 cusp，未必物理正确；实际使用应换成后述的 **screened fractional correction**。它与 $A|k|^p$ 在 $k\xi\gg1$ 的标度窗口具有相同渐近结果。
- T2 的结论不自动适用于有限场下的非线性状态方程、自洽密度或全部基态能量；这些需要独立计算。

### 远离临界点的稳定性命题，而非无条件优越性

若 $K_{\rm exact}\succeq mI$、$m>0$，并有 $\|K_{\rm corr}-K_{\rm exact}\|\le\epsilon<m$，则 resolvent identity 给出

$$
\boxed{
\|K_{\rm corr}^{-1}-K_{\rm exact}^{-1}\|
\le\frac{\epsilon}{m(m-\epsilon)}.
}
\tag{21}
$$

这是**稳定性及误差控制界**。只有额外证明修正降低了 $\epsilon$，才能声称对固定非临界参数而言比原近似更好。实用泛函可在远离临界区时平滑关闭临界修正，以保留基线表现。

---

# Part III — 由理论约束构造可自洽能量泛函

## 5. 共同原则：先修改总 Hessian，再得到 Hxc 修正

设冻结的基线为

$$
\Gamma_{\rm base}[\phi;g]
=\Gamma_{\rm ref}[\phi;g]
+E_{\rm Hxc}^{\rm base}[\phi;g].
\tag{22}
$$

“冻结”指：在预先定义的训练阶段确定架构与系数，测试阶段不重新拟合；若内禀参数 $g$ 改变，允许使用**事先确定、无测试泄漏的**参数化 $g\mapsto\theta(g)$，不能事后针对每个测试样本重新优化。

将临界模式标量化为 $\varphi_j$；对于 Hubbard CDW，可取 $\varphi_j=(-1)^j(n_j-1)$。令 $\delta\varphi_j=\varphi_j-\varphi_j^0$，Fourier 约定 $\delta\varphi_k=\sum_j e^{-ikj}\delta\varphi_j$。定义

$$
\boxed{
\Gamma_{\rm improved}
=\Gamma_{\rm base}
+\frac1{2L}\sum_k\Delta K(k;g,L)
|\delta\varphi_k|^2.
}
\tag{23}
$$

于是同一个能量泛函生成非局域势和 Hessian：

$$
\Delta h_j
=\frac{\partial\Delta\Gamma}{\partial\varphi_j}
=\frac1L\sum_k e^{ikj}\Delta K(k)\delta\varphi_k,
\qquad
\Delta K=\Delta\Gamma^{(2)}.
\tag{24}
$$

电子体系将 $\Delta h_j$ 按 $h=-v$ 及 $\varphi_j=(-1)^j\delta n_j$ 转换为 Hxc 势；在普通电子 DFT 极小化中应直接使用 $\delta\Delta E/\delta n_j$，避免符号混乱。

**必须保证：** $\Delta K(k)$ 为实偶函数／Hermitian 矩阵，遵守粒子数约束与晶胞对称性，修正后总 Hessian 在稳定物理子空间非负；所有参数通过独立样本或理论输入确定。

## 6. LDA、GGA 与修正公式

### 6.1 作为基线的 LDA 和晶格 GGA

标量基本变量的示例：

$$
E_{\rm Hxc}^{\rm LDA}[\varphi]
=\sum_j e_{\rm Hxc}^{\rm hom}(\varphi_j;g),
\tag{25}
$$

$$
E_{\rm Hxc}^{\rm GGA}[\varphi]
=E_{\rm Hxc}^{\rm LDA}[\varphi]
+\frac{b(g)}2\sum_j(\varphi_{j+1}-\varphi_j)^2.
\tag{26}
$$

这是**晶格局域／邻近梯度**形式；真实电子 Hubbard 模型中的 LDA/GGA 可以写在 $n_j$ 上、对二聚化 $A/B$ 亚格子采用对称允许的系数，且精确 Hartree 最近邻项应单独处理而非被误认为临界修正。

在均匀参考态，LDA Hxc Hessian 为常数；GGA 多出 $4b\sin^2(k/2)$。二者若加上解析的参考逆响应，总 Hessian 在临界模式仍为解析的 $r+c_2k^2+\cdots$。

### 6.2 临界目标曲率与严格的差分修正

定义 $\Omega(k)=2|\sin(k/2)|$、$p=7/4$。临界目标：

$$
K_{\rm target}(k;g_c)
=A\Omega(k)^p+B\Omega(k)^2+\cdots,
\qquad K_{\rm target}(0;g_c)=0.
\tag{27}
$$

给定平滑窗口 $W(k)$（$W(0)=1$，只修改临界区域），采用最直接的曲率差分：

$$
\boxed{
\Delta K(k)=W(k)[K_{\rm target}(k)-K_{\rm base}(k)].
}
\tag{28}
$$

则在 $W=1$ 区域，修正后的总 Hessian 等于 $K_{\rm target}$。这避免重复添加已有的质量项、梯度项及 KS 动能贡献。实际有限 $L$ 的目标不能机械设为 $K_L(0)=0$，应匹配 $K_L(0)\propto L^{-p}$ 与有限尺寸标度函数。

### 6.3 实际优先实现的 Screened Critical Correction

在临界点外，为避免在有限 $\xi$ 时产生不应存在的 $k=0$ 分数幂 cusp，采用

$$
\boxed{
S_p(k;\xi)
=\left[\xi^{-2}+\Omega(k)^2\right]^{p/2}-\xi^{-p}.
}
\tag{29}
$$

它满足

$$
S_p(k;\infty)\sim |k|^p,
\qquad
S_p(k;\xi)=\frac p2\xi^{2-p}k^2+O(k^4)
\quad (k\xi\ll1),
\tag{30}
$$

且在 $k\xi\gg1$ 主导行为为 $|k|^p$。但 **$S_p$ 只是启发式 crossover，不是已证明的精确 Ising scaling function。**

一种简单、统一且可以公平比较的实现是

$$
\boxed{
\begin{aligned}
\Delta K_{\rm scr}(k;g,L)
=W(k)\Big\{&r_{\rm tar}(g,L)-r_{\rm base}(g,L)\\
&+s(g)\,A(g)S_p(k;\xi_g)\Big\},
\end{aligned}
}
\tag{31}
$$

其中 $r_{\rm tar}$ 是独立确定的临界通道零模曲率目标，$s(g)\to1$（趋临界点）且可在远离临界区平滑变为零。更高精度的版本用 $K_{\rm target}-K_{\rm base}$ 替换大括号中的简化形式，以显式避免短程重复计数。若 $r_{\rm tar}$ 从被测试的精确 $\kappa(0)$ 中获取，则那一测试不再是独立预测；必须在数据划分中注明。

**统一修正：**

$$
\boxed{
E_{\rm Hxc}^{\rm LDA+C}
=E_{\rm Hxc}^{\rm LDA}+\Delta\Gamma_{\rm scr},
\qquad
E_{\rm Hxc}^{\rm GGA+C}
=E_{\rm Hxc}^{\rm GGA}+\Delta\Gamma_{\rm scr}.
}
\tag{32}
$$

相同 $p$、窗口、质量校准规则和新增参数预算，分别比较不同冻结基线。

## 7. 超出 Hessian：非线性状态方程（扩展，不列为两项定理的前提）

对于 1+1D Ising 纵向序参量，热力学临界状态方程

$$
 m(h)\sim\operatorname{sgn}(h)|h|^{1/15}
\quad\Longleftrightarrow\quad
\gamma(m)-\gamma(0)\sim B|m|^{16}.
\tag{33}
$$

仅仅把 $|k|^{7/4}$ 写入二次 Hessian **不保证** 式 (33)。若原 LDA/GGA 保留主导 $m^4$ 项，单独加一个 $m^{16}$ 并不能修复状态方程；必须校正**受限有效势整体的低阶结构**，同时避免与二次临界修正重复计数。建议将 $m(h)$／$\gamma(m)$ 作为独立验证，并在 Hessian 方案成功后才开发非线性泛函修正。

## 8. 振幅如何避免“多加一个参数当然更好”的质疑？

对 $z=1$ Ising 临界算符，在算符和 Fourier 归一化一致时，可独立测量等时关联振幅与临界速度：

$$
\langle O(x,0)O(0,0)\rangle_c
\sim C_O|x|^{-1/4},\qquad v.
\tag{34}
$$

相应时空 CFT 两点函数 $C_O(x^2+v^2\tau^2)^{-1/8}$ 的**正则化二维 Fourier 变换**给出

$$
\kappa(k,0)
\sim\frac{C_O}{v}\mathcal C_{\rm I}|k|^{-7/4},
\quad
\mathcal C_{\rm I}
=2^{7/4}\pi\frac{\Gamma(7/8)}{\Gamma(1/8)},
\tag{35}
$$

因此

$$
\boxed{A_K^{\rm pred}=\frac{v}{C_O\mathcal C_{\rm I}}.}
\tag{36}
$$

由于 $\tau$ 方向积分在某些顺序下不是普通绝对收敛积分，应理解为带 IR 正则化的零频二维 Fourier 变换，不能先对无限时间区间做不受控逐点积分。微观格点到低能算符的归一化、Hubbard 晶胞因子与振幅需要一致核对。

式 (36) 让**指数和主导振幅**都有机会通过与目标静态响应不同的数据获得；再把 DMRG static response 留作独立测试。这比直接拟合相同响应曲线更强。

---

# Part IV — 两个具体模型的数值验证

## 9. 模型 A：横场 Ising —— 廉价、可控的理论检验场

### 9.1 Hamiltonian 与基本变量

$$
\boxed{
H_{\rm I}
=-J\sum_j\sigma_j^z\sigma_{j+1}^z
-g\sum_j\sigma_j^x
-\sum_j h_j\sigma_j^z.
}
\tag{37}
$$

选取 $J=1$，在 $h_j=0$ 的对称侧 $g>1$ 向 $g_c=1$ 接近。**基本变量必须选纵向磁化** $m_j=\langle\sigma_j^z\rangle$（序参量，$Q=0$），因为此前 Mao 等人的 Ising LDA/GGA 采用的是**横场方向极化**；后者对应不同的临界算符，不能直接套用 $7/4$ 预言，也不能不加修改直接复用其 LDA/GGA 参数。

独立自旋参考体系

$$
H_{\rm ref}=-g\sum_j\sigma_j^x-\sum_j h_j^s\sigma_j^z,
\quad
\boxed{\Gamma_{\rm ref}[m]=-g\sum_j\sqrt{1-m_j^2}}.
\tag{38}
$$

因此

$$
K_{\rm ref}(m=0,k)=g,
\tag{39}
$$

严格局域且解析。这个模型可以最干净地展示临界非解析成分必须进入相互作用修正泛函。

### 9.2 LDA/GGA 基线如何构造？

- **LDA：** 从固定 $g$ 的均匀纵向场 $h$ 扫描获得 $e_0(h;g)$ 与 $m(h;g)$，做一致的 Legendre 变换得到每格点的均匀泛函 $\gamma_{\rm hom}(m;g)$；定义 $e_{\rm Hxc}^{\rm LDA}(m;g)=\gamma_{\rm hom}(m;g)+g\sqrt{1-m^2}$。在测试阶段冻结这种参数化。即使采用精确均匀输入，LDA 也不能因此拥有正确的**空间**临界响应。
- **GGA：** 在相同的 LDA 上加入 $\frac12b(g)\sum_j(m_{j+1}-m_j)^2$，通过预先指定的非均匀训练集确定 $b(g)$。保持 $m\mapsto-m$ 的 $\mathbb Z_2$ 对称性。
- **共同修正：** 对 LDA/GGA 应用式 (23)–(32)，在测试时不重新拟合基线及窗口。

### 9.3 精确基准和计算任务

1. **ED 单元测试：** $L=8,10,12$；用 $\pm h$ 有限差分、基态能量曲率与激发态 Lehmann 公式交叉验证 $\kappa$，确认 $K=\kappa^{-1}$。
2. **临界点：** $g=J$，采用 $L=32,48,64,96,128$（资源允许可扩至 $192,256$），逐步增加 MPS bond dimension，独立验证 $C_{zz}(r)\sim r^{-1/4}$、纠缠标度 $c=1/2$。
3. **静态响应：** 在 $H\to H-\lambda\sum_j\cos(kj)\sigma_j^z$ 下做 $\pm\lambda$ 基态计算，$\lambda\to0$，得到 $\kappa(k)$；检查 $\kappa(0,L)\sim L^{7/4}$。
4. **动量矩阵：** 周期边界适合严格动量；开放边界可用于较便宜的有限尺寸基准，但不能不经边界修正就把平面波投影响应视为严格 $\kappa(k)$。
5. **修正测试：** 计算 LDA、GGA、梯度对照、错误幂律与正确 $7/4$ 修正的自洽磁化和响应；测试更大 $L$、更小 $k$、不同空间形状的 $h_j$ 与 $g>J$ 的 crossover。

### 9.4 预期结果与判据

| 观测 | 精确理论预期 | 要求修正泛函证明什么 |
|---|---|---|
| 临界 $\kappa(k)$ | $\propto |k|^{-7/4}$ | 未拟合小动量处的响应比值趋向 1 |
| 临界 $K(k)$ | $\propto |k|^{7/4}$ | 正确非解析结构；不能只看人为写入的指数 |
| 冻结 GGA | 调到临界后通常 $K\sim k^2$ | 渐近失配与 Theorem 1 一致 |
| $g>J$ 标度窗口 | $\xi^{-1}\ll k\ll1$ 近似临界幂律 | Theorem 2 的误差比值趋势 |
| 有限 $\xi$ 极小 $k$ | 解析 crossover | 屏蔽分数阶核避免虚假 cusp |
| 有限纵向场 | $m(h)\sim h^{1/15}$（热力学临界标度区） | 仅 Hessian 修正不保证此项；属于独立诊断 |

> **关键风险：** Ising 纵向磁化的“精确均匀 LDA”可在均匀场方面非常好，甚至精确提供状态方程；这并不与其**空间** Hessian no-go 矛盾，反而是一个具有说服力的对照。

---

## 10. 模型 B：键二聚化扩展 Hubbard —— 电子 KS-DFT 的核心检验

### 10.1 Hamiltonian、CDW 模式与数值起点

$$
\boxed{
\begin{aligned}
H_{\rm EH}={}&-\sum_{j\sigma}t_j(c_{j\sigma}^{\dagger}c_{j+1,\sigma}+\mathrm{h.c.})\\
&+U\sum_j(n_{j\uparrow}-\tfrac12)(n_{j\downarrow}-\tfrac12)\\
&+V\sum_j(n_j-1)(n_{j+1}-1)\\
&-\sum_j h_j(n_j-1),\\
t_j={}&t[1+\delta(-1)^j].
\end{aligned}
}
\tag{40}
$$

固定半填充；初步使用 $U/t=4$、$\delta=0.2$，在 $V/t\approx2.5035$ 附近重新定位连续的 PI–CDW Ising 临界点。文献中不同的二聚化参数记法可能不同，代码应直接记录强弱键 $t(1\pm\delta)$ 并复现文献定义。

$$
O_\pi=\sum_j(-1)^j(n_j-1),
\quad Q=\pi,
\quad\varphi_j=(-1)^j(n_j-1).
\tag{41}
$$

在对称 PI 侧，基态平均密度每格点为 1，非相互作用 KS 参考具有 dimerized hopping 和 Peierls band gap

$$
\Delta_s=2|t_1-t_2|=4t|\delta|.
\tag{42}
$$

因此可独立通过两带 Lindhard response 验证 $K_s(Q+k)$ 的解析性，并计算

$$
\boxed{f_{\rm Hxc}=\chi_s^{-1}-\chi^{-1}.}
\tag{43}
$$

若使用电子 Hartree 拆分，最近邻 $V$ 的裸 Hartree Hessian 是短程、解析的，不应错误地把它当成普适临界长程尾。建议将已知的局域 $U$／最近邻 $V$ 贡献与真正需要近似的 $E_{\rm xc}$ 明确分开。

### 10.2 两亚格子矩阵与临界通道

两格点晶胞对应

$$
\boldsymbol\kappa(k)
=\begin{pmatrix}\kappa_{AA}&\kappa_{AB}\\\kappa_{BA}&\kappa_{BB}\end{pmatrix},
\qquad
\mathbf K(k)=\boldsymbol\kappa(k)^{-1}.
\tag{44}
$$

在折叠 BZ 中，原先 $Q=\pi$ 的 CDW 模式位于晶胞动量 $k=0$、近似沿 $(1,-1)/\sqrt2$。若临界方向与背景通道混合，则在临界／背景基中

$$
\boxed{
K_{\rm eff}(k)=K_{cc}(k)-K_{cb}(k)K_{bb}(k)^{-1}K_{bc}(k),
\quad \kappa_{cc}=K_{\rm eff}^{-1}.
}
\tag{45}
$$

应该先对完整矩阵求逆或使用该 Schur complement，再讨论临界有效曲率和修正。只对 $u_c^\dagger\boldsymbol\kappa u_c$ 取倒数通常**不等于** $u_c^\dagger\mathbf K u_c$。

### 10.3 基线 LDA/GGA 与实验实现

- **电子 LDA：** 使用固定 $U,V,\delta$ 的、可积分的局域 Hxc 能量密度，独立训练／校准其参数；Hartree 项单独保留。不得直接将仅对普通 Hubbard $V=0$ 训练的现成模型称作当前 extended Hubbard 的基线。
- **电子 GGA：** 在相同局域基线上加入二聚化晶格允许的邻近密度差项或有限邻域能量密度。能量泛函的输入邻域半径为 $a$ 时，其 Hessian 支撑范围可以达到 $2a$，报告时应区分二者。
- **修正：** 以 $\varphi_j=(-1)^j(n_j-1)$ 的 CDW 慢模式构造非局域二次项，针对完整矩阵或其有效 Schur 曲率设置 $K_{\rm target}$；再求泛函导数实现自洽 KS 更新。

### 10.4 具体计算清单

| 步骤 | 实施方法 | 主要输出 |
|---|---|---|
| H1. 小系统严格测试 | ED：$L=6,8,10,12$；有限场与 Lehmann 交叉验证 | 正确 $\boldsymbol\kappa$、符号、粒子数投影 |
| H2. QCP benchmark | OBC/iDMRG：扫 $V$，验证能隙、$\xi$、纠缠及 CDW 指数 | $V_c$、Ising universality、误差条 |
| H3. $Q=\pi$ 静态响应 | $\pm\lambda O_\pi$ DMRG，改变 $L,D,\lambda$ | $|\kappa(Q,L)|\propto L^{7/4}$ |
| H4. 小动量响应 | 独立的两亚格子正弦/余弦源；PBC 或受控 bulk-response 方法 | $\boldsymbol\kappa(k)$，临界本征值 |
| H5. KS 对照 | 解析两带 Hamiltonian、Lindhard；独立验证间隙和曲率 | $\boldsymbol\kappa_s(k)$ 与解析展开 |
| H6. 泛函比较 | 固定 LDA/GGA、梯度、错误幂律、正确幂律、screened 修正 | 样本外 $K,\kappa,n_i,E_0$ |
| H7. 非临界窗口 | 从 PI 侧改变 $V$，独立测 $\xi$ | $k\xi$ collapse、误差随 $\xi$ 的收敛 |
| H8. 可选扩展 | 第二组 Ising 参数或 tricritical endpoint | 跨参数稳健性／$37/20$ 预言 |

**数值重要性排序：** H3 和 H4 是关键瓶颈。DMRG 主要提供多体静态 $\kappa$ 和临界诊断；KS 响应、矩阵求逆、Fourier 修正及自洽优化不需要新的多体求解器。OBC 得到的简单投影响应一般不能当作严格动量对角响应，应做 PBC 或矩阵／边界控制交叉验证。

### 10.5 预期可以得到的图和物理结论

1. **临界响应的分数幂：** $\kappa_{\rm CDW}(Q+k)\sim |k|^{-7/4}$，$K_c\sim |k|^{7/4}$；参考 KS 逆响应解析，临界非解析性进入 Hxc。
2. **固定范围失效：** 即使 LDA/GGA 通过质量校准给出正确软化，其最小动量渐近 $k^2$ 与 $k^{7/4}$ 不符；Hessian 相对误差向 Theorem 1 预测的极限发展。
3. **临界点外渐近优势：** 在 $V\to V_c^-$、$k=\xi^{-s}$ 的路径上，未经修正曲率比值趋向 0，而正确修正趋向 1；必须验证基线的质量及梯度系数满足 Theorem 2 的假设。
4. **自洽预测的实际价值：** LDA+C/GGA+C 对未经训练的小动量和非均匀外势的密度响应更准确；是否也改善能量和非线性状态方程须实测，不预设结论。

---

# Part V — 公平比较、可证伪性与预期主图

## 11. 为什么“多一个参数效果更好”不是有效证据？

所有比较中的基线先被冻结；质量校准、窗口函数的选择与外部信息预算必须共用或一致记账。最少进行下列**相同新增参数数目**的控制实验：

| 近似 | 共同质量校准以外的新增谱项 | 预期渐近指数 | 作用 |
|---|---|---:|---|
| Fixed LDA / Fixed GGA | 无 | 解析 | 基线 |
| + 梯度项 | $a\Omega(k)^2$ | $2$ | 仅增加一个参数 |
| + 错误非局域幂 | $a\Omega(k)^{3/2}$ | $3/2$ | 排除“随便加长程项即可” |
| + 另一错误指数 | $a\Omega(k)^{9/5}$ | $9/5$ | 检验预言指数选择性 |
| **+ Ising critical correction** | $a\Omega(k)^{7/4}$ | **$7/4$** | 检验 universality 输入 |
| **+ screened critical correction** | $a S_{7/4}(k;\xi)$ | 临界 $7/4$、远离临界解析 | 检验非临界 crossover |

如果某方案使用了更多独立可拟合的 $\xi$、截止尺度、振幅或质量参数，必须在模型复杂度比较中计入，或者把它们作为**独立物理数据**明示，而不能宣称自由参数相同。

### 11.1 单训练点解析对照

理想目标 $K_*(k)=A|k|^p$，令两个**只有一个振幅**的方案都在 $k_0$ 完全拟合。任意指数 $q$ 的方案给出

$$
K_q(k)=A|k_0|^{p-q}|k|^q,
\qquad
\boxed{\frac{K_q(k)}{K_*(k)}
=\left|\frac{k}{k_0}\right|^{q-p}.}
\tag{46}
$$

只有 $q=p$ 在独立的所有 $k$ 上仍然有正确比例。式 (46) 不是 DMRG 成果，而是检验**函数类选择性**的可解析示例。

### 11.2 真正的样本外实验

- **训练集：** 小系统或中等 $k$，少量临界附近参数及受控非均匀外源；先冻结基线。
- **测试集：** 更大的 $L$、更小的 $k$、未训练的 $g/V$、不同外势形状与非线性场强。
- **禁止泄漏：** 不能把目标 $K_{\rm exact}(k)$ 逐点填入修正后，再将这些相同 $k$ 的匹配作为论文主要预测结果。
- **必须报告：** 绝对和相对 Hessian 误差、相对 susceptibility 误差、基态能量误差、密度误差、凸性／稳定性以及实验参数和数值不确定度。

特别推荐绘制

$$
\mathcal A_{\rm model}(k)=\frac{K_{\rm model}(k)}{|k|^{7/4}}.
\tag{47}
$$

精确体系 $\to A_K$，解析调临界基线 $\to0$，正确振幅修正 $\to A_K$。但由于正确指数可能已被写入修正项，**主结论必须来自未拟合振幅、CFT 独立振幅预测、有限 $\xi$ crossover、自洽密度及尺寸外推**。

## 12. 建议的四张 PRL 主图

**Fig. 1 — Exact constraint and no-go.** 展示 $K_{\rm exact}\sim k^{7/4}$ 与固定有限范围解析 $K_{\rm sl}\sim k^2$，以及 Theorem 1 的相对误差极限；用简短理论示意图而不是大量原始数据。

**Fig. 2 — Near-critical theorem and crossover.** 以 $k\xi$ 为横轴，比较精确逆响应、冻结半局域基线和 screened critical correction；用多组 $\xi$ 或 $k=\xi^{-s}$ 路径检验 Theorem 2 的渐近优势。

**Fig. 3 — Ising proof of principle.** 相同参数预算下的 LDA/GGA、普通梯度、错误指数、正确指数修正；包括样本外响应、独立振幅预测与至少一种非均匀外势自洽测试。

**Fig. 4 — Electronic Hubbard realization.** 两亚格子 interacting/KS/Hxc 曲率分解、对应 Ising $7/4$ 结构和经过同样规则修正的固定 LDA/GGA 自洽验证。图中标明哪些参数从 Ising 普适性转移、哪些必须为 Hubbard 独立确定。

## 13. 项目成功、部分成功与失败的判据

| 结果 | 对课题意味着什么 |
|---|---|
| Ising 中 no-go 与修正的响应和跨尺度检验都成立，Hubbard 尚未完成 | 形成独立的广义泛函方法论文基础；不声称电子 KS-DFT 已验证 |
| Ising 与 Hubbard 都有 $7/4$，但改进仅限拟合时使用的 Hessian | 证明结构约束存在，不足以宣称修正泛函有实际预测力 |
| 两模型中对未拟合 $k,L,g$ 的响应、独立振幅或交叉函数有优势 | 强有力的跨模型、跨尺度方法学结果 |
| 改善响应但恶化能量、非线性响应或稳定性 | 说明二阶修正范围有限，须加入稳定化与有效势校正 |
| Hubbard 的 KS 逆响应出现无法忽略的非解析抵消 | 现有电子 Hxc 继承论证需修改；不能机械套用 Ising 模型结果 |
| 基线的梯度系数随 $\xi$ 奇异增长 | Theorem 2 条件不成立；应研究更广义的可逼近性，而不能报告其预测得到确认 |

---

# Part VI — 数值实现细节与工作包

## 14. 复现性与收敛要求

**外场响应。** 在 $H=H_0-\lambda O$ 下，$\kappa=\partial\langle O\rangle/\partial\lambda$。用 $\pm\lambda$ 中央差分与能量二阶导数交叉验证，报告 $\lambda\to0$ 外推。Ising 临界纵向场具有 $y_h=15/8$，应控制 $|\lambda|L^{15/8}$ 的有限尺度效应。

**等时相关与静态响应不同。** Ising 序参量等时关联 $C(r,0)\sim r^{-1/4}$，而零频静态 susceptibility 为 $\kappa(k,0)\sim|k|^{-7/4}$；后者还包含虚时间积分。不能拿等时结构因子的 Fourier 变换替代静态响应。

**MPS 收敛。** 每个关键 $L,g,k$ 至少变动 bond dimension $D$，检查 discarded weight、能量、密度和**响应本身**的收敛。大 $L$ 下先以少数 $k$ 检验响应算法，再进行规模化计算。

**边界与矩阵反演。** 对称非临界背景通道必须被正确消去；OBC 下不要直接假设 Fourier 对角化；电子模型固定 $N$ 时投影掉 uniform gauge mode。临界响应的正定矩阵可能高度病态，优先拟合临界特征通道并在不同 $L$ 上做矩阵条件数检查。

**误差条。** 报告场幅、截断误差、系统尺寸、临界点定位、拟合窗口和静态逆响应噪声的贡献。区分数据置信区间与 universality 输入本身的理论指数。

## 15. 优先工作包（按依赖关系而非按模型数量）

| 工作包 | 必须产出 | 通过后再推进 |
|---|---|---|
| WP-T1 | Theorem 1 的严谨假设、证明和矩阵注释 | 开始设计修正项 |
| WP-T2 | Theorem 2 的双重极限、误差界和反例范围 | 设计非临界扫描路径 |
| WP-I1 | Ising ED/DMRG 静态响应与纵向 LDA/GGA | 公平参数对照 |
| WP-I2 | 纵向 Ising 的修正泛函及样本外验证 | 跨模型转移 |
| WP-H1 | Hubbard QCP、$\boldsymbol\kappa$ 与 $\boldsymbol\kappa_s$ | 构造精确 Hxc 目标 |
| WP-H2 | Hubbard 固定 LDA/GGA+C 自洽预测 | 撰写电子 DFT 主结论 |
| WP-X | 独立 CFT 振幅、tricritical 或非线性 EOS | PRL 强化材料，非前期硬依赖 |

---

## 参考文献与直接相关工作

1. **J. Mao, H. Tang, W. Duan, Z. Liu**, “Testing density functional theory in a quantum Ising chain,” *Physical Review B* **104**, 155145 (2021). https://doi.org/10.1103/PhysRevB.104.155145 ；**注意基本变量是横向极化**，不能与本文的纵向序参量直接混用。
2. **E. Costa, R. Fazio, S. Pilati**, “Deep learning nonlocal and scalable energy functionals for quantum Ising models,” *Physical Review B* **108**, 125113 (2023). https://doi.org/10.1103/PhysRevB.108.125113 。非局域泛函、可扩展网络及量子临界区误差研究。
3. **E. Cronin, R. Tiwari, S. Sanvito**, “Machine learning semilocal exchange-correlation functionals for Kohn-Sham density functional theory of the Hubbard model,” *Physical Review B* **112**, 195103 (2025). https://doi.org/10.1103/vm99-khkz 。有限邻域 Hubbard KS-LDFT、Hxc 势与 polarizability 的主要对照。
4. **S. Ejima, F. H. L. Essler, F. Lange, H. Fehske**, “Ising tricriticality in the extended Hubbard model with bond dimerization,” *Physical Review B* **93**, 235118 (2016). https://doi.org/10.1103/PhysRevB.93.235118 。PI–CDW Ising 线、tricritical Ising 端点与 DMRG 基准。
5. **U. Schollwöck**, “The density-matrix renormalization group in the age of matrix product states,” *Annals of Physics* **326**, 96–192 (2011). https://doi.org/10.1016/j.aop.2010.09.012 。DMRG/MPS 的方法学基础。
6. **M. Penz, R. van Leeuwen**, “Density-Functional Theory on Graphs,” *Journal of Chemical Physics* **155**, 244111 (2021). https://arxiv.org/abs/2106.15370 。有限格点 DFT、密度—势映射及可表象性问题。
7. **S. Sachdev**, *Quantum Phase Transitions*, 2nd ed., Cambridge University Press (2011). 普适标度、序参量响应及状态方程。

### 最终工作定位（建议写入论文 Introduction）

> **This project identifies a response-level obstruction to fixed-range semilocal density functionals at non-Gaussian quantum criticality, proves a conditional near-critical asymptotic advantage of universality-constrained corrections, and tests their predictive utility in both generalized spin DFT and electronic Kohn–Sham lattice DFT.**

以上命题均应保持三个边界：**只对明确的临界算符通道讨论 Hessian；只在明确假设下证明渐近优势；只把独立测试得到的改善称为泛函预测能力。**


