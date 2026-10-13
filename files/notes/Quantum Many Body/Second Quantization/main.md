---
title: "少废话，二次量子化！"
date: 2026-10-12
cover: cover.png
summary: "你才是挑战者！"
---

二次量子化本质是极致的线性代数

波函数的语言说到底虽然也是希尔伯特空间的矢量语言，但做得还不够彻底。把连续的函数表象变成进一步离散的粒子数表象，此即二次量子化。

首先把所有包含不同粒子数的波函数 $\Psi(\mathbf{r}_1,\mathbf{r}_2,\mathbf{r}_3,\ldots)$ 统统打包到一个空间，也即Fock空间

$$
\mathcal H_F = \mathcal H_0\oplus\mathcal H_1\oplus\cdots\oplus\mathcal H_N
$$

注意到所有的单粒子波函数可以用某一正交完备本征基底 $\{\phi_i(\mathbf r)\}$ 展开，而多粒子波函数又可以由单粒子基底的直积张成的基底展开（记得归一化，或者说归 $N$ 化？）

$$
|\Psi\rangle = \sum_{i_1,\ldots,i_N} C_{i_1\cdots i_N} |\phi_{i_1}\rangle\otimes\cdots\otimes|\phi_{i_N}\rangle
$$

于是想到干嘛不干脆把 $N$ 粒子的直积基底写成粒子数占据的形式

$$
|n_1,n_2,n_3,\ldots\rangle
$$

$$
|\Psi\rangle = \sum_{\{n_i\}} C_{\{n_i\}} |n_1,n_2,\ldots\rangle
$$

满足 $\sum n_i = N$

ん？什么波函数，你看这哪里有波函数啊，这不是纯纯的矢量吗

不过这么搞有一点点的不严谨，因为实际符合全同粒子对称性/反对称性的空间要比理论上的张量积空间更小。我们需要把基底投影到对应的对称/反对称空间

$$
\mathcal H_N^\pm = P_\pm^{(N)}\mathcal H_1^{\otimes N}
$$

$$
\mathcal F_\pm = \bigoplus_{N=0}^{\infty}\mathcal H_N^\pm
$$

$P_\pm^{(N)}$ 是对称/反对称投影算符

更进一步，要改就改得彻底一点，作用在波函数上的算符那一套也可以扔掉，换成人民群众喜闻乐见的矩阵。由于现在一套粒子数表象就可以完全描述一个态，所以我们对态的操作就变成了纯粹的对粒子数的操作，为此引入产生算符 $\hat a^\dagger$ 和湮灭算符 $\hat a$

以归一化的 $N$ 粒子态 $|\Psi_N\rangle\in\mathcal H_N^\pm$ 为例，我们希望向这个系统中加入一个处于 $|f\rangle$ 的粒子。直观的想法是构造张量积 $|f\rangle\otimes|\Psi_N\rangle$，但这个态未必满足全同粒子的交换对称性。为此产生算符可以定义成以下形式

$$
\hat a_\pm^\dagger(f)|\Psi_N\rangle = \sqrt{N+1}\, P_\pm^{(N+1)} \left(|f\rangle\otimes|\Psi_N\rangle\right)
$$

$\sqrt{N+1}$ 用来补偿整体对称化投影的系数

湮灭算符就定义为其 Hermitian 共轭

$$
\hat a_\pm(f) = \left[\hat a_\pm^\dagger(f)\right]^\dagger
$$

在这种定义下，玻色子和费米子的正则对易关系可得

Boson

$$
[\hat a_i,\hat a_j^\dagger] = \delta_{ij},\qquad
[\hat a_i,\hat a_j] = 0,\qquad
[\hat a_i^\dagger,\hat a_j^\dagger] = 0
$$

$$
[A,B] = AB-BA
$$

Fermion

$$
\{\hat c_i,\hat c_j^\dagger\} = \delta_{ij},\qquad
\{\hat c_i,\hat c_j\} = 0,\qquad
\{\hat c_i^\dagger,\hat c_j^\dagger\} = 0
$$

$$
\{A,B\} = AB+BA
$$

然后你就可以发现了，这玩意写作算符实则就是矩阵，单模式玻色子下，产生、湮灭算符满足：

$$
\hat a|n\rangle = \sqrt{n}|n-1\rangle
$$

$$
\hat a^\dagger|n\rangle = \sqrt{n+1}|n+1\rangle
$$

这不就等同于

$$
\hat a = \begin{pmatrix}
0 & 1 & 0 & 0 & \cdots \\
0 & 0 & \sqrt{2} & 0 & \cdots \\
0 & 0 & 0 & \sqrt{3} & \cdots \\
0 & 0 & 0 & 0 & \ddots \\
\vdots & \vdots & \vdots & \ddots & \ddots
\end{pmatrix}
$$

$$
\hat a^\dagger = \begin{pmatrix}
0 & 0 & 0 & 0 & \cdots \\
1 & 0 & 0 & 0 & \cdots \\
0 & \sqrt{2} & 0 & 0 & \cdots \\
0 & 0 & \sqrt{3} & 0 & \cdots \\
\vdots & \vdots & \vdots & \ddots & \ddots
\end{pmatrix}
$$

多粒子态同理，同样能够写成作用于整个 Fock 空间的矩阵。另外注意到

$$
\hat a^\dagger\hat a = \begin{pmatrix}
0 & 0 & 0 & 0 & \cdots \\
0 & 1 & 0 & 0 & \cdots \\
0 & 0 & 2 & 0 & \cdots \\
0 & 0 & 0 & 3 & \cdots \\
\vdots & \vdots & \vdots & \vdots & \ddots
\end{pmatrix}
$$

干脆定义

$$
\hat n = \hat a^\dagger\hat a
$$

作为粒子数算符，显然的，这个矩阵的本征态就是Fock空间的本征基底。

有了产生湮灭算符，所有波函数表象下的算符都可转化为粒子数表象下的矩阵，事实上这件事在波函数的视角下也是经常干的，考虑第一量子化中的单粒子算符 $\hat h$，引入单粒子矩阵元

$$
h_{ij} = \langle\phi_i|\hat h|\phi_j\rangle
$$

直接有

$$
\hat h = \sum_{ij} h_{ij}|\phi_i\rangle\langle\phi_j|
$$

算符 $|\phi_i\rangle\langle\phi_j|$ 的作用等效地可以视作波函数中单粒子波函数成分的跃迁 $|\phi_j\rangle\longrightarrow|\phi_i\rangle$，如果展开的基底就是二次量子化选取的基底，那么在粒子数表象中等效有

$$
\hat A = \sum_{ij} h_{ij}\hat a_i^\dagger\hat a_j
$$

例如单粒子的Hamiltonian，动能算符

$$
\hat T = \sum_{p=1}^N \frac{\hat{\mathbf p}_p^2}{2m}
$$

如果选择动量本征态作为单粒子基底，就得到

$$
\hat T = \sum_{\mathbf k} \frac{\hbar^2k^2}{2m} \hat a_{\mathbf k}^\dagger\hat a_{\mathbf k}
$$

作用在多体粒子波函数上的算符，这个对应其实没有那么显然，但可以证明的是，

$$
\hat H_F = \sum_{ij} h_{ij}\hat a_i^\dagger\hat a_j
$$

在 $N$ 粒子空间上的作用，等价于

$$
\hat H_N = \sum_{p=1}^N \hat h(p)
$$

例如两体相互作用算符

$$
\hat V = \sum_{p<q} V(\mathbf r_p,\mathbf r_q) = \frac{1}{2}\sum_{p\ne q} \hat V(p,q)
$$

定义单粒子跃迁算符 $\hat E_{ik} = |\phi_i\rangle\langle\phi_k|$，其可以张成单粒子算符空间，那么两个单粒子算符的张量积便可以展开二体算符

$$
\begin{aligned}
\hat V &= \sum_{ijkl} V_{ij;kl}\hat E_{ik}\otimes\hat E_{jl} \\
&= \frac{1}{2}\sum_{ijkl} V_{ij;kl}\sum_{p\ne q} \hat E_{ik}(p)\hat E_{jl}(q)
\end{aligned}
$$

$$
V_{ij;kl} = \langle\phi_i\phi_j|\hat V|\phi_k\phi_l\rangle
$$

其中又有

$$
\sum_{p\ne q} \hat E_{ik}(p)\hat E_{jl}(q) = \hat a_i^\dagger\hat a_j^\dagger\hat a_l\hat a_k
$$

于是二次量子化下有

$$
\hat V_F = \frac{1}{2}\sum_{ijkl} V_{ij;kl}\hat a_i^\dagger\hat a_j^\dagger\hat a_l\hat a_k
$$

另外，虽然会显得有些闲的没事干，但我们可以反过来用离散的本征态反过来表示连续的位置基底，写出倒反天罡的转换

$$
|\mathbf r\rangle = \sum_i |\phi_i\rangle\langle\phi_i|\mathbf r\rangle
$$

于是可以定义位置本征态的产生和湮灭算符（可以用类似的方法定义任意单粒子态的产生和湮灭算符），也即场算符

$$
\begin{aligned}
\hat\psi(\mathbf r) &= \sum_i \phi_i(\mathbf r)\hat a_i, \\
\hat\psi^\dagger(\mathbf r) &= \sum_i \phi_i^*(\mathbf r)\hat a_i^\dagger
\end{aligned}
$$

于是如果你想的话，二体相互作用又可以写成

$$
\begin{aligned}
\hat V_F = {} & \frac{1}{2}\int d^3r\,d^3r'\,
\hat\psi^\dagger(\mathbf r)\hat\psi^\dagger(\mathbf r') \\
& \times V(\mathbf r,\mathbf r')\times\hat\psi(\mathbf r')\hat\psi(\mathbf r)
\end{aligned}
$$

写得有点乱，总之就是这样。

---

另，没人觉得二次量子化这个名字很帅吗
