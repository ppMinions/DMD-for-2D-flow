# module dmd_m

# import libraries
import numpy as np


def dmd_fit(X, n_rank, sort_by):
    Y = X[:, 1:]
    X = X[:, :-1]

    # ===== Dynamic Mode Decomposition Computation ======
    U, S, Vh = np.linalg.svd(X, full_matrices=True)  # 对数据矩阵1进行奇异值分解
    # print(U.shape)
    # print(Vh.shape)
    if n_rank is not None:  # 提取前n_rank模态
        U = U[:, :n_rank]
        S = S[:n_rank]
        S = np.diag(S)  # 生成对角矩阵
        Vh = Vh[:n_rank, :]
        # print(U.shape)
        # print(Vh.shape)
    # Compute the DMD matrix using the pseudo_inverse of X
    Atilde = np.linalg.multi_dot([U.T, Y, Vh.T, np.linalg.inv(S)])
    #Atilde = U.T.dot(Y).dot(Vh.T) / S  # 低阶转化矩阵
    # print(Atilde.shape)

    # Eigen_solve gives modes and eigenvalues
    evals, mode = np.linalg.eig(Atilde)  # 对低阶转化矩阵进行特征值分解
    # print(evals)
    # print(evals.size)
    # print(mode.shape)
    basis = np.linalg.multi_dot([Y, Vh.T, np.linalg.inv(S), mode])
    #basis = (Y.dot(Vh.T) / S).dot(mode)  # 重构转化矩阵的特征向量phi
        # print(basis.shape)
    # basis = Y.dot(Vh.T)/S

    eval_vander = np.vander(evals, increasing=True)  # 根据特征值生成范德蒙矩阵
    b = np.dot(np.linalg.pinv(basis), X[:, 0])
    #b = np.linalg.pinv(basis).dot(X[:, 0])  # 求解初始模态向量

    # Energy of the mode
    energy_mode = np.zeros(n_rank)
    for i in range(n_rank):
        temp_energy = b[i]*np.dot(basis[:, i].reshape((basis.shape[0], 1)),
                                 eval_vander[i, :].reshape((1, eval_vander.shape[1])))
        temp_energy = temp_energy.real
        energy_mode[i] = sum(sum(temp_energy**2))


    if evals is None or basis is None:
        raise RuntimeError("DMD modes have not yet been computed.")
    if sort_by == 'no':
        inds = np.arange(0, evals.size, 1)
    elif sort_by == "LM":
        inds = np.argsort(np.abs(evals))[::-1]  # 将特征值按绝对值由大到小进行排序，返回索引序列
    elif sort_by == "Energy":
        inds = np.argsort(energy_mode)[::-1]
    else:
        raise NotImplementedError("Cannot sort by " + sortby)

    evals = evals[inds]  # 对特征值顺序进行重新整理
    basis = basis[:, inds]  # 对每一列的模态进行排序
    return evals, basis, eval_vander, b, energy_mode