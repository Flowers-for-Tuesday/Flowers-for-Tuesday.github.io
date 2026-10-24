---
title: "Notes about Path Integral"
date: 2026-10-17
cover: cover.jpeg
summary: "Think I wanna twist the plot this time."
---

量子力学讨论班的一些零散笔记。

## 1 / 欧式路径积分

我们知道实时间作用量和传播子

$$
S_M[x]
=
\int dt
\left[
\frac m2\left(\frac{dx}{dt}\right)^2
-V(x)
\right]
$$

$$
K_M
=
\int\mathcal Dx\,
e^{iS_M[x]/\hbar}
$$

Wick转动令$t=-i\tau$，得到

$$
\begin{aligned}
S_M
&=
\int(-i\,d\tau)
\left[
-\frac m2\left(\frac{dx}{d\tau}\right)^2
-V(x)
\right]\\
&=
i\int d\tau
\left[
\frac m2\left(\frac{dx}{d\tau}\right)^2
+V(x)
\right]
\end{aligned}
$$

$$
S_E[x]
=
\int d\tau
\left[
\frac m2\left(\frac{dx}{d\tau}\right)^2
+V(x)
\right]
$$

$$
S_M=iS_E
$$

由此定义欧式路径积分

$$
e^{iS_M/\hbar}
=
e^{-S_E/\hbar}
$$

$$
K_E(x_f,\tau;x_i,0)
=
\int_{x(0)=x_i}^{x(\tau)=x_f}
\mathcal Dx\,
e^{-S_E[x]/\hbar}
$$

求解这个积分后再进行代换即变成实时间的路径积分。

## 2 / 二次型的精确求解

我们知道路径积分大部分都是没办法严格求解的，不过二次型是个例外，这一点用有限维积分很好解释，考虑积分

$$
I=\int_{\mathbb R^N}d^Nx\,
\exp\left(-\frac12x^TAx\right)
$$

进行对角化分解

$$
A=O^T\Lambda O
$$

$$
\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_N)
$$

做正交变量变换 $y=Ox$，于是

$$
I=\prod_{i=1}^N
\int_{-\infty}^{\infty}dy_i\,
e^{-\lambda_i y_i^2/2}
$$

$$
\int dy_i\,e^{-\lambda_i y_i^2/2}
=
\sqrt{\frac{2\pi}{\lambda_i}}
$$

$$
I=\frac{(2\pi)^{N/2}}{\sqrt{\det A}}
$$

现在开始推广到路径积分。对于欧式路径积分

$$
Z=\int\mathcal D\phi\,e^{-S_E[\phi]/\hbar}
$$

我们这里先把作用量写成最原始的推导过程中的离散形式，这有助于我们找到一个对应方式，以谐振子为例，时间切分 $\epsilon=\frac{T}{N+1}$ 下的离散作用量为

$$
S_{E,N}
=
\frac{m}{2\epsilon}
\sum_{j=0}^{N}(q_{j+1}-q_j)^2
+
\frac{m\omega^2\epsilon}{2}
\sum_{j=1}^{N}q_j^2
$$

转化为二次形式

$$
S_{E,N}
=
\frac{m}{2\epsilon}
\left[
(2+\omega^2\epsilon^2)\sum_{j=1}^Nq_j^2
-
2\sum_{j=1}^{N-1}q_jq_{j+1}
\right]
$$

其对应着矩阵

$$
K_N=
\frac m\epsilon
\begin{pmatrix}
2+\omega^2\epsilon^2&-1&0&\cdots&0\\
-1&2+\omega^2\epsilon^2&-1&\cdots&0\\
0&-1&2+\omega^2\epsilon^2&\ddots&\vdots\\
\vdots&\vdots&\ddots&\ddots&-1\\
0&0&\cdots&-1&2+\omega^2\epsilon^2
\end{pmatrix}
$$

$$
S_{E,N}=\frac12\mathbf q^TK_N\mathbf q
$$

$$
A_N=\frac{K_N}{\hbar}
$$

$$
\int_{\mathbb R^N}d^Nq\,
e^{-S_{E,N}/\hbar}
=
\int_{\mathbb R^N}d^Nq\,
e^{-\frac12\mathbf q^TA_N\mathbf q}
$$

所以整个问题严格可解。

$$
K_E(x_f,T;x_i,0)
={}
\sqrt{\frac{m\omega}{2\pi\hbar\sinh\omega T}}
\times\exp\left[
-\frac{m\omega}{2\hbar\sinh\omega T}
\left(
(x_f^2+x_i^2)\cosh\omega T-2x_ix_f
\right)
\right]
$$

事实上离散矩阵 $K_N$ 对应于连续的微分算符

$$
\hat K
=
-m\frac{d^2}{d\tau^2}+m\omega^2
$$

$$
\frac12\mathbf q^TK_N\mathbf q
\xrightarrow{N\to\infty}
\frac12\int_0^Td\tau\,q(\tau)\hat Kq(\tau)
$$

之前自己一直认为路径积分有滥用符号的嫌疑，把本应该是离散形式的积分变量都塞到了作用量中。现在看完全可以换个视角，把一整条路径视作高维空间的一个点，作用量视作定义在这个点上的函数，如此看反而更符合自己的数学直觉。强行去思考“路径”的积分总容易令人误解。

## 3 / 路径积分视角下的本征态

尽管由上述方式我们求得了谐振子的严格传播子，但这不意味着我们可以直接得到与波函数理论一样的本征函数与本征能级。

$$
E_n=\hbar\omega\left(n+\frac12\right),
\qquad n=0,1,2,\ldots
$$

为了从传播子得到量子化，引入正则配分函数

$$
Z(\beta)=\operatorname{Tr}e^{-\beta H}
$$

由谱分解，如果哈密顿量能够量子化，那么应该有能量本征基底下的

$$
Z(\beta)=\sum_ne^{-\beta E_n}
$$

另一方面，注意到位置本征基底下

$$
Z(\beta)
=
\int_{-\infty}^{\infty}dx\,
\langle x|e^{-HT/\hbar}|x\rangle
=
\int_{-\infty}^{\infty}dx\,
K_E(x,\beta\hbar;x,0)
$$

$$
T=\beta\hbar
$$

相当于对所有首尾相接的路径积分，也就是周期欧氏路径积分

$$
Z(\beta)
=
\int_{x(0)=x(\beta\hbar)}
\mathcal Dx\,e^{-S_E[x]/\hbar}
$$

就拿刚刚解出来的谐振子当例子，我们可以严格求解整个配分函数

$$
S_{\mathrm{cl}}(x,x;T)
=
m\omega x^2\tanh\left(\frac{\omega T}{2}\right)
$$

$$
K_E(x,T;x,0)
=
\sqrt{\frac{m\omega}{2\pi\hbar\sinh(\omega T)}}
\exp\left[
-\frac{m\omega x^2}{\hbar}
\tanh\left(\frac{\omega T}{2}\right)
\right]
$$

$$
Z(\beta)
={}
\sqrt{\frac{m\omega}{2\pi\hbar\sinh(\omega T)}}
\times
\int_{-\infty}^{\infty}dx\,
\exp\left[
-\frac{m\omega}{\hbar}
\tanh\left(\frac{\omega T}{2}\right)x^2
\right]
$$

$$
Z(\beta)=
\sqrt{
\frac{1}{
2\sinh(\omega T)\tanh(\omega T/2)
}
}
$$

$$
Z(\beta)=
\frac1{2\sinh(\beta\hbar\omega/2)}
$$

利用级数展开，成功导出能级

$$
Z(\beta)
=
e^{-\beta\hbar\omega/2}
\sum_{n=0}^{\infty}e^{-n\beta\hbar\omega}
=
\sum_{n=0}^{\infty}
e^{-\beta\hbar\omega(n+1/2)}
$$

$$
E_n=\hbar\omega\left(n+\frac12\right),
\qquad n=0,1,2,\ldots
$$

类似的我们会试着去求一下本征波函数，其实注意到

$$
\int dx_a\,
K(x_b,T;x_a,0)\psi_n(x_a)
=
e^{-iE_nT/\hbar}\psi_n(x_b).
$$

这说明 $\psi_n(x)$ 其实是传播核 $K$ 的一个本征函数。换个形式写成谱分解

$$
K(x_b,t_b;x_a,t_a)
=
\sum_n
\langle x_b|n\rangle
e^{-iE_nT/\hbar}
\langle n|x_a\rangle.
$$

$$
K(x_b,x_a;T)
=
\sum_n
\psi_n(x_b)
\psi_n^*(x_a)
e^{-iE_nT/\hbar}.
$$

可以对时间做 Fourier 变换，定义Green 函数

$$
G_E(x_b,x_a)
=
\frac{1}{i\hbar}
\int_0^\infty dT\,
e^{i(E+i0)T/\hbar}
K(x_b,x_a;T).
$$

$$
G_E
=
\sum_n
\psi_n(x_b)\psi_n^*(x_a)
\frac{1}{E-E_n+i0}.
$$

$$
G_E(x_b,x_a)
=
\sum_n
\frac{
\psi_n(x_b)\psi_n^*(x_a)
}{
E-E_n+i0
}.
$$

当 $E\to E_n$ ，Green 函数出现极点，而极点的留数正比于 $\psi_n(x_b)\psi_n^*(x_a).$

所以从路径积分传播子做能量变换以后，定态波函数可由此提取出来。欧式积分的方法其实也可以做，不过用到路径积分求解波函数的情形毕竟还是少数，这里不多写。