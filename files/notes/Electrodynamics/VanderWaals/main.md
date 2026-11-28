---
title: "Van der Waals force"
date: 2026-11-01
cover: cover.jpeg
summary: "天黑请闭眼"
---

刘雄军老师电动力学课上的扩展内容，作为期中复习笔记简单写一下。

## 0 / prerequisite

前置知识主要是关于多极矩的内容。

基本思想就是电势的远场展开

$$
\phi(\mathbf r)
=
\frac1{4\pi\varepsilon_0}
\int
\frac{\rho(\mathbf r')}
{|\mathbf r-\mathbf r'|}
d^3r'
$$

$$
\frac1{|\mathbf r-\mathbf r'|}
={}
\frac1r
+\frac{\hat{\mathbf r}\cdot\mathbf r'}{r^2}
+
\frac{
3(\hat{\mathbf r}\cdot\mathbf r')^2-r'^2
}{2r^3}
+
\frac{
5(\hat{\mathbf r}\cdot\mathbf r')^3
-3r'^2(\hat{\mathbf r}\cdot\mathbf r')
}{2r^4}
+\cdots
$$

保留前三项分别就是零级矩，偶极矩，四极矩（一个对称无迹张量）和对应势能分量

$$
\begin{aligned}
Q
&= \int \rho(\mathbf r')\,d^3r',
&\qquad
\phi^{(0)}(\mathbf r)
&= \frac{Q}{4\pi\varepsilon_0 r},
\\[8pt]
\mathbf p
&= \int \rho(\mathbf r')\mathbf r'\,d^3r',
&\qquad
\phi^{(1)}(\mathbf r)
&= \frac{1}{4\pi\varepsilon_0}
   \frac{\mathbf p\cdot\hat{\mathbf r}}{r^2},
\\[8pt]
Q_{ij}
&= \int \rho(\mathbf r')
   \left(3x_i'x_j'-r'^2\delta_{ij}\right)d^3r',
&\qquad
\phi^{(2)}(\mathbf r)
&= \frac{1}{4\pi\varepsilon_0}
   \frac{Q_{ij}\hat r_i\hat r_j}{2r^3}.
\end{aligned}
$$

以及换个视角，进行外场下的势能展开

$$
U
=
\int\rho(\mathbf r)
\phi_{\mathrm{ext}}(\mathbf r)d^3r
$$

$$
\phi_{\mathrm{ext}}(\mathbf r)
={}
\phi_{\mathrm{ext}}(0)
+x_i\partial_i\phi_{\mathrm{ext}}(0)
+\frac12x_ix_j
\partial_i\partial_j\phi_{\mathrm{ext}}(0)
+\frac1{3!}x_ix_jx_k
\partial_i\partial_j\partial_k
\phi_{\mathrm{ext}}(0)
+\cdots
$$

同样保留前三项

$$
U={}
Q\phi_{\mathrm{ext}}(0)
+
p_i\partial_i\phi_{\mathrm{ext}}(0)
+\frac12M_{ij}\partial_i\partial_j
\phi_{\mathrm{ext}}(0)
+\cdots
$$

$$
U^{(0)}=Q\phi_{\mathrm{ext}}(0)
$$

$$
U^{(1)}
=
p_i\partial_i\phi_{\mathrm{ext}}
=
-\mathbf p\cdot\mathbf E_{\mathrm{ext}}
$$

$$
U^{(2)}
=
\frac12M_{ij}
\partial_i\partial_j\phi_{\mathrm{ext}}
=
\frac16Q_{ij}
\partial_i\partial_j\phi_{\mathrm{ext}}
+
\frac16M_{kk}\nabla^2\phi_{\mathrm{ext}}
=
\frac16Q_{ij}
\partial_i\partial_j\phi_{\mathrm{ext}}
$$

其中利用到了关系 $Q_{ij}=3M_{ij}-M_{kk}\delta_{ij}$

以及偶极-偶极相互作用

$$
U_{AB}=-\mathbf p_B\cdot\mathbf E_A
=
\frac{1}{4\pi\varepsilon_0R^3}
\left[
\mathbf p_A\cdot\mathbf p_B
-
3(\mathbf p_A\cdot\hat{\mathbf R})
(\mathbf p_B\cdot\hat{\mathbf R})
\right]
$$

> 记住这里的$R^3$反比

当然，以上内容属于老生常谈了，比较有趣的视角是用球谐函数来写，这来源于勒德朗多项式的生成函数

$$
\frac1{\sqrt{1-2tx+t^2}}
=
\sum_{l=0}^{\infty}t^lP_l(x)
$$

于是读者敏锐地发现可以把原先的势能多级展开写作

$$
\frac1{|\mathbf r-\mathbf r'|}
=
\frac1r
\frac1{\sqrt{1-2(r'/r)\cos\gamma+(r'/r)^2}}
=
\sum_{l=0}^{\infty}
\frac{r'^l}{r^{l+1}}P_l(\cos\gamma)
$$

然后代入勒德朗多项式的前几项之后就会发现和原先的展开没什么区别）

$$
\frac1{|\mathbf r-\mathbf r'|}
={}\frac1r
+\frac{r'}{r^2}\cos\gamma
+\frac{r'^2}{2r^3}(3\cos^2\gamma-1)
+\frac{r'^3}{2r^4}(5\cos^3\gamma-3\cos\gamma)
+\cdots
$$

这里需要更进一步，用球谐函数的加法公式

$$
P_l(\cos\gamma)
=
\frac{4\pi}{2l+1}
\sum_{m=-l}^{l}
Y_{lm}(\hat{\mathbf r})
Y_{lm}^{*}(\hat{\mathbf r}')
$$

得到

$$
\phi(\mathbf r)
=
\frac{1}{4\pi\varepsilon_0}
\sum_{l=0}^{\infty}
\sum_{m=-l}^{l}
\frac{4\pi}{2l+1}
\frac{q_{lm}}{r^{l+1}}
Y_{lm}(\hat{\mathbf r})
$$

$$
q_{lm}
=
\int
\rho(\mathbf r')
r'^lY_{lm}^{*}(\hat{\mathbf r}')
\,d^3r'
$$

其中 $q_{lm}$就是第 $l,m$ 个球谐多极矩，好处是规避了复杂的张量运算。不难由此意识到多极矩展开本质上就是一类特殊的本征函数展开。（笛卡尔基底下虽然看着还行，但真的算起来是很恶心的，球谐其实是更自然的选择）

如果试着把这两种展开方式逐项对比，可以得到两种偶极矩的转换

$$
\phi(\mathbf r)
=
\frac1{4\pi\varepsilon_0}
\Bigg[

\frac{4\pi q_{00}Y_{00}}{r}
+
\frac{4\pi}{3r^2}
\sum_{m=-1}^{1}q_{1m}Y_{1m}
+
\frac{4\pi}{5r^3}
\sum_{m=-2}^{2}q_{2m}Y_{2m}
+\cdots
\Bigg]
$$

$$
\phi(\mathbf r)
=
\frac1{4\pi\varepsilon_0}
\Bigg[
\frac Qr+
\frac{\mathbf p\cdot\hat{\mathbf r}}{r^2}
+
\frac{Q_{ij}\hat r_i\hat r_j}{2r^3}
+\cdots
\Bigg]
$$


## 1 / 正文

范德瓦尔斯力作为一种电磁力，其来源于原子偶极矩的涨落。以两个中性原子$A$和$B$为例，在其基态肯定有平均偶极矩为0，也即

$$
\langle0_A|\hat{\mathbf d}_A|0_A\rangle=0
$$

$$
\langle0_B|\hat{\mathbf d}_B|0_B\rangle=0
$$

但其仍然可能有偶极矩的涨落$\langle0|\hat{\mathbf d}^{\,2}|0\rangle>0$，这也就意味着两个原子的偶极相互作用平均下来不见得会相互抵消掉，为此我们来进行一点详细的计算验证。

尽管电动力学能给出定性的结论，但为了严谨下面就直接用二阶微扰论来推了，定义相应的偶极矩算符$\hat{\mathbf d}_A$，$\hat{\mathbf d}_B$ ，那么对应的有偶极作用势能（定义$D_{ij}=\delta_{ij}-3n_in_j$）

$$
\hat V_{dd}
=
\frac{\kappa}{r^3}
\left[
\hat{\mathbf d}_A\cdot\hat{\mathbf d}_B
-
3(\hat{\mathbf d}_A\cdot\mathbf n)
(\hat{\mathbf d}_B\cdot\mathbf n)
\right]
=
\frac{\kappa}{r^3}
D_{ij}\hat d_A^i\hat d_B^j
$$

把这一项视作修正的哈密顿量，那么根据一阶微扰论

$$
E^{(1)}
=
\frac{\kappa}{r^3}
D_{ij}
\langle0|\hat d_A^i\hat d_B^j|0\rangle
=
\frac{\kappa}{r^3}
D_{ij}
\langle0_A|\hat d_A^i|0_A\rangle
\langle0_B|\hat d_B^j|0_B\rangle
\
=
0
$$

也即一阶微扰能量为0，原因就是粒子没有平均偶极矩，而二阶微扰下（当然这个式子需要满足基态非简并，我们姑且认为其成立）

$$
E^{(2)}
=
\sum_{N\neq0}
\frac{
|\langle N|\hat V_{dd}|0\rangle|^2
}{
E_0-E_N
}
$$

其中 $|N\rangle$ 是未微扰体系（也即无相互作用体系）的激发态。

注意到无相互作用体系有$|N\rangle=|n_A\rangle\otimes|m_B\rangle$，$E_N=E_{nA}+E_{mB}$，于是干脆定义

$$
\omega_{An}
=
\frac{E_{nA}-E_{0A}}{\hbar}>0
$$

$$
\omega_{Bm}
=
\frac{E_{mB}-E_{0B}}{\hbar}>0
$$

$$
E_N-E_0
=
\hbar(\omega_{An}+\omega_{Bm})
$$

代入二阶微扰的能量公式里得到London色散势能的表达式

$$
E^{(2)}
=
-\frac{\kappa^2}{\hbar r^6}
\sum_{n,m}
\frac{
\left|
D_{ij}
\langle n_A|\hat d_A^i|0_A\rangle
\langle m_B|\hat d_B^j|0_B\rangle
\right|^2
}{
\omega_{An}+\omega_{Bm}
}
$$

由此其实就已经有一些定性的结论，例如$E^{(2)}\propto-\frac1{r^6}$，相互作用能为负且距离依赖是 $r^{-6}$

这个势能肯定和 $\hat{n}$ 的选取无关，事实上很容易计算

$$
D_{ij}D_{ij}
=(\delta_{ij}-3n_in_j)(\delta_{ij}-3n_in_j)
=3-6n_in_i+9(n_in_i)^2
=6
$$

不妨认为我们考虑的情形下，基态是简并且各向同性的（例如氢原子的1s基态），这意味着



## 2 / 换个视角

## e.g.1 / Lorenz振子