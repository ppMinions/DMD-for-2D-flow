import numpy as np
import dmd_new as dmd
import data_input_output as data_io
import matplotlib.pyplot as plt
import os

# the working directory
path = "F:\\local_membrane_airfoil\\cylinyder_dmd\\"
os.chdir(path)
if not os.path.exists('./results'):
    os.mkdir('./results')
# the data and results directory
path_in = path +'data\\'
path_out = path + 'results\\'

# Generate the list containing the file name
start_id = 4250  # the id of the start .dat file
end_id = 4995  # the id of the end .dat file
delta_id = 5  # the delta id of the .dat files
file_head = 'flow_0'
file_tail = '.dat'

file_name = []
id_array = np.arange(start_id, end_id+delta_id, delta_id)
for i in id_array:
    file_name_one = file_head + str(i) + file_tail
    file_name.append(file_name_one)
# print(file_name)


n_snapshot = len(file_name)
# the up limit and low limit of the valid lines in the .dat file
start_lines = 16  # line 17 is the first line of the data
end_lines = 13352  # line 13352 is the last line of the data
# flag to subtract mean from snapshots prior to undertaking POD
subtract_mean = False
# the data map extracted in the .dat file
area_x_low = -0.2
area_x_up = 10
area_y_low = -2
area_y_up = 2
# the mode
n_rank = 20
# time step between snapshots
delta_t = 0.1  # the time step is the cfd is 0.02s, and the gap between .dat file is five steps
# =================== Read the Dat file =========================================
print('Start read the .dat files......')

for i in range(n_snapshot):
    data_name = 'data_' + str(i)
    header_name = 'header_' + str(i)
    tail_name = 'tail_' + str(i)
    locals()[data_name], locals()[header_name], locals()[tail_name] = data_io.Read_Dat_File(path_in, file_name[i], start_lines, end_lines)

print('.dat files imported successfully!')
print(data_0)

# ================= Extract data of the specific area ==========================
print('Start extract the data......')

for i in range(n_snapshot):
    data_name = 'data_' + str(i)
    data_p_name = 'data_p_' + str(i)
    data_id_name = 'data_id_' + str(i)
    locals()[data_p_name], locals()[data_id_name] = data_io.Extract_Dat(locals()[data_name], area_x_low, area_x_up, area_y_low, area_y_up)

print('data extracted successfully!')
n_point = data_p_0.shape[0]
print('the points number is ', n_point)
print('the snapshots number is ', n_snapshot)
for i in range(n_snapshot - 1):
    data_id_name = 'data_id_' + str(i)
    if data_id_0.all() != locals()[data_id_name].all():
        print("False")
        print('the different is', i)

# ================== Dynamic Mode Decomposition ===============================
print('Start the DMD......')

for i in range(n_snapshot):
    data_p_name = 'data_p_' + str(i)
    if i == 0:
        dmd_matrix = locals()[data_p_name].reshape(n_point, 1)
    else:
        dmd_matrix = np.hstack((dmd_matrix, locals()[data_p_name].reshape(n_point, 1)))

print('the DMD matrix is generated successfully!')
print('the DMD matrix size is', dmd_matrix.shape)

print('Start calculating mean field ......')
mean_field = np.array(np.zeros(n_point, dtype=np.float64)).reshape((n_point, 1))
for i in range(0, n_snapshot):
    mean_field[:, 0] = mean_field[:, 0] + dmd_matrix[:, i]
mean_field[:, 0] = mean_field[:, 0] / n_snapshot

if subtract_mean == "True":
    print('Subtracting mean from instantaneous fields ......')
    for i in range(n_snapshot):
        dmd_matrix[:, i] = dmd_matrix[:, i] - mean_field[:, 0]

evals, basis, eval_vander, b, energy = dmd.dmd_fit(dmd_matrix, n_rank, "Energy")


print('the SVD is done！')
print('the number of eig values is', evals.size)
# print('the eig values are', evals)
print('the size of eig vectors is', basis.shape)
print('Check the components of the eig vectors......')
for i in range(n_rank):
    if (basis[:, i] == 0).any():
        print('Warning! There exits 0 components in the eig vectors!')
        print('The vector number is', i)
    else:
        print('Check passed! No 0 components in the eig vector')
# print('the eig vectors are', basis)

# ---------------- Plot and output the distribution of the eig values ------------------------
plt.figure(figsize=(10, 10))
plt.scatter(evals.real, evals.imag)
plt.xlim((-1, 1))
plt.ylim((-1, 1))
plt.xlabel('the real value of the eig')
plt.ylabel('the image value of the eig')
plt.title('the distribution of the eig values')

print('Output the eig values of the DMD')
eig_array = np.vstack((evals.real, evals.imag))
np.savetxt(path_out+'eig_value.csv', eig_array.T, delimiter=',')
print('the eig values is output to the results file successfully!')

# ------------------- Plot and output the frequency and the damping of the modes -------------------
mu = (np.log(evals))/delta_t
gamma = mu.real  # 得到模态衰减率
omega = mu.imag  # 得到模态频率
plt.figure(figsize=(10, 10))
plt.scatter(gamma, omega)
plt.xlabel('the damping of the mode')
plt.ylabel('the frequency of the mode')
plt.title('the damping and the frequency of the mode')

# ------------------- Plot and output the frequency and energy the modes -------------------------
plt.figure(figsize=(10, 10))
# plt.scatter(np.arange(1, n_rank+1, 1), energy)
plt.scatter(omega, energy)
plt.xlabel('omega')
plt.ylabel('the energy of the mode')
plt.title('Energy-omega')

print('Output the damping, frequency, and the energy of the DMD')
dmd_data_array = np.vstack((gamma, omega, energy))
np.savetxt(path_out+'dmd_data.csv', dmd_data_array.T, delimiter=',')
print('the damping, frequency, and the energy of the DMD are output to the results file successfully!')

#plt.show()


b_diag = np.diag(b)  # 得到初始模态矩阵
# A_low = np.dot(np.dot(basis, b_diag), eval_vander)  # 得到降阶后的数据矩阵

for i in range(n_rank):
    mode_name = 'mode_' + str(i)
    locals()[mode_name] = np.real(basis[:, i])
# 输出模态向量矩阵
# np.savetxt(path_out+'phi.csv', basis, delimiter=',')

# print(mode_0, mode_2)


# ==================== Pro-processing of the data ==============================
print('Start the pro-processing of the data......')


print('Start the replace......')
'''
# mode 1
new_mode_1 = np.zeros((data_0.shape[0], data_0.shape[1]))
new_mode_1[:, 0] = data_0[:, 0]
new_mode_1[:, 1] = data_0[:, 1]
for i in range(data_0.shape[0]):
    for j in range(mode_0.shape[0]):
        if i == data_id_0[j]:
            new_mode_1[i, 2] = mode_0[j]
    if new_mode_1[i, 2] == 0:
        new_mode_1[i, 2] = data_0[i, 2]


# mode 2
new_mode_2 = np.zeros((data_0.shape[0], data_0.shape[1]))
new_mode_2[:, 0] = data_0[:, 0]
new_mode_2[:, 1] = data_0[:, 1]
for i in range(data_0.shape[0]):
    for j in range(mode_2.shape[0]):
        if i == data_id_0[j]:
            new_mode_2[i, 2] = mode_2[j]
    if new_mode_2[i, 2] == 0:
        new_mode_2[i, 2] = data_0[i, 2]
'''

for i in range(n_rank):
    mode_name = 'mode_' + str(i)
    new_mode_name = 'new_mode_' + str(i)
    locals()[new_mode_name] = data_io.Replace_Dat(data_0, locals()[mode_name], data_id_0)


print('Replace is successful!')

print('Start writing to the specific path......')

data_io.Write_Dat_File(path_out, 'mode_file_1.dat', new_mode_0, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_2.dat', new_mode_1, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_3.dat', new_mode_2, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_4.dat', new_mode_3, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_5.dat', new_mode_4, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_6.dat', new_mode_5, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_7.dat', new_mode_6, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_8.dat', new_mode_7, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_9.dat', new_mode_8, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_10.dat', new_mode_9, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_11.dat', new_mode_10, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_12.dat', new_mode_11, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_13.dat', new_mode_12, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_14.dat', new_mode_13, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_15.dat', new_mode_14, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_16.dat', new_mode_15, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_17.dat', new_mode_16, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_18.dat', new_mode_17, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_19.dat', new_mode_18, header_1, tail_1)
data_io.Write_Dat_File(path_out, 'mode_file_20.dat', new_mode_19, header_1, tail_1)

print(f"{path}file is saved successfully!")














