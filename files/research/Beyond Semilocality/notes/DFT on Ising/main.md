---
title: "DFT on Transverse Ising"
category: Research Notes
date: 2026-10-18
cover: cover.jpg
summary: "Easy revenge"
---

## 1 / 广义密度泛函与自旋DFT理论

对于一般的量子力学体系，例如自旋体系，如果希望沿用DFT的思路，更自然的选择则是某个局域观测量的期望值，考虑一般形式的量子自旋Hamiltonian

$$
H[\boldsymbol g]
=
H_{\mathrm{int}}
-
\sum_i g_i O_i
$$

也即将Hamiltonian分为构形独立部分$H_int$与外场耦合部分，对于波函数构形，其自然就是DFT能量泛函的正常写法

$$
\hat H[v]
=
\hat H_{\mathrm{int}}
+
\int d^3r\,v_{\mathrm{ext}}(\mathbf r)\hat n(\mathbf r)
$$

$$
\hat H_{\mathrm{int}}=\hat T+\hat V_{ee},
\qquad
n(\mathbf r)=\langle\Psi|\hat n(\mathbf r)|\Psi\rangle.
$$

对应的搜索泛函形式如下

$$
E[v]
=
\inf_\Psi
\left[
\langle\Psi|\hat T+\hat W|\Psi\rangle
+
\int vn_\Psi
\right].
$$

那么对于我们的自旋体系，以TFIM为例，同样可以有

$$
H[\boldsymbol g]
=
-\sum_{i=1}^{N}\sigma_i^z\sigma_{i+1}^z
-
\sum_{i=1}^{N}g_i\sigma_i^x,
\qquad
\sigma_{N+1}^\alpha=\sigma_1^\alpha.
$$

由于横场 $g_i$ 与 $\sigma_i^x$ 线性耦合，我们选取广义密度 $\rho_i=\langle\sigma_i^x\rangle$

更严格地说我们定义的都是系综泛函，之后不会刻意强调。

$$
F[\boldsymbol\rho]
=
\inf_{\Gamma\mapsto\boldsymbol\rho}
\operatorname{Tr}
\left(\Gamma H_{\mathrm{int}}\right),
$$

$$
E_0[\boldsymbol g]
=
\inf_{\boldsymbol\rho}
\left[
F[\boldsymbol\rho]
-
\sum_i g_i\rho_i
\right].
$$

$$
F[\boldsymbol\rho]
=
\sup_{\boldsymbol g}
\left[
E_0[\boldsymbol g]
+
\sum_i g_i\rho_i
\right].
$$



## 2 / LDA＆GGA on Transverse Ising

## 3 / No Go Theorem

## 4 / Fixed Functional（NRC-LDA）

