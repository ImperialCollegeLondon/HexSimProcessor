# from HexSimProcessorFast import *
from hexSimProcessor import *
from pathlib import Path
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import tifffile as tif
import numpy as np
import time

# import cProfile

plt.close('all')
isPlot = True
N = 10  # number of iterations
Nsize = 512

''' Initialize '''
# h=HexSimProcessor
h = hexSimProcessor()
h.debug = False
h.cleanup = True
h.N = (Nsize // 2) * 2

''' Read Image '''
data_folder = Path("C:/Users/hgong/Documents/simDATA/")
filename = str(data_folder / "SIMdata_2019-11-05_15-21-42/SIMdata_2019-11-05_15-21-42.tif")
filename = "./SIMdata_2019-11-05_15-21-42.tif"
img1 = tif.imread(filename)

if Nsize != 512:
    img1 = np.single(img1[:, 256 - Nsize // 2: 256 + Nsize // 2, 256 - Nsize // 2: 256 + Nsize // 2])
else:
    img1 = np.single(img1)

if isPlot:
    plt.figure()
    plt.imshow(np.sum(img1, 0), cmap=cm.gray)

''' Calibration '''
start_time = time.time()
h.calibrate(img1)
elapsed_time = time.time() - start_time
print(f'Calibration time: {elapsed_time:5f}s ')

''' Recontruction '''

''' FFTW '''
start_time = time.time()
for i in range(0, 10):
    imga = h.reconstruct_fftw(img1)
elapsed_time = time.time() - start_time
print(f'FFTW Reconstruction time: {elapsed_time / 10:5f}s ')

''' FFTW '''
start_time = time.time()
for i in range(0, N):
    imga = h.reconstruct_rfftw(img1)
elapsed_time = time.time() - start_time
print(f'FFTW Reconstruction time: {elapsed_time / N:5f}s ')
if isPlot:
    plt.figure()
    plt.imshow(imga, cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

''' rFTTFW '''
start_time = time.time()
for i in range(0, N):
    imgb = h.reconstruct_rfftw(img1)
elapsed_time = time.time() - start_time
print(f'rFFTW Reconstruction time: {elapsed_time / N:5f}s ')
if isPlot:
    plt.figure()
    plt.imshow(imgb, cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

''' ocv '''
start_time = time.time()
for i in range(0, N):
    imgb = h.reconstruct_ocv(img1)
elapsed_time = time.time() - start_time
print(f'ocv Reconstruction time: {elapsed_time / N:5f}s ')
if isPlot:
    plt.figure()
    plt.imshow(imgb, cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

''' ocvU '''
start_time = time.time()
for i in range(0, N):
    imgb = h.reconstruct_ocvU(img1)
elapsed_time = time.time() - start_time
print(f'ocvU Reconstruction time: {elapsed_time / N:5f}s ')
if isPlot:
    plt.figure()
    plt.imshow(imgb.get(), cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

# ''' CuPy '''
# start_time = time.time()
# for i in range(0, N):
#     imgb = h.reconstruct_cupy(img1)
# elapsed_time = time.time() - start_time
# print(f'CuPy Reconstruction time: {elapsed_time / N:5f}s ')
# if isPlot:
#     plt.figure()
#     plt.imshow(imgb.get(), cmap=cm.gray)

''' FFTW '''
start_time = time.time()
for i in range(0, 7 * N):
    imga = h.reconstructframe_fftw(img1[i % 7, :, :], i % 7)
elapsed_time = time.time() - start_time
print(f'FFTW Reconstructframe time: {elapsed_time / (7 * N):5f}s ')
if isPlot:
    plt.figure()
    plt.imshow(imga, cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

''' rFFTW '''
start_time = time.time()
for i in range(0, 7 * N):
    imga = h.reconstructframe_rfftw(img1[i % 7, :, :], i % 7)
elapsed_time = time.time() - start_time
print(f'rFFTW Reconstructframe time: {elapsed_time / (7 * N):5f}s ')
if isPlot:
    plt.figure()
    plt.imshow(imga, cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

''' ocv '''
start_time = time.time()
for i in range(0, 7 * N):
    imga = h.reconstructframe_ocv(img1[i % 7, :, :], i % 7)
elapsed_time = time.time() - start_time
print(f'ocv Reconstruction time: {elapsed_time / (7 * N):5f}s ')
if isPlot:
    plt.figure()
    plt.imshow(imga, cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

''' ocvU '''
start_time = time.time()
for i in range(0, 7 * N):
    imga = h.reconstructframe_ocvU(img1[i % 7, :, :], i % 7)
elapsed_time = time.time() - start_time
print(f'ocvU Reconstruction time: {elapsed_time / (7 * N):5f}s ')
if isPlot:
    plt.figure()
    plt.imshow(imga.get(), cmap=cm.hot, clim=(0.0, 0.7*imga.get().max()))

# ''' CuPy '''
# start_time = time.time()
# for i in range(0, 7 * N):
#     imga = h.reconstructframe_cupy(img1[i % 7, :, :], i % 7)
# elapsed_time = time.time() - start_time
# print(f'CuPy Reconstructframe time: {elapsed_time / (7 * N):5f}s ')
# if isPlot:
#     plt.figure()
#     plt.imshow(imga.get(), cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

''' Read image stack'''
filename = str("./Raw_img_stack_512_inplane_comp6.tif")
img2 = tif.imread(filename)
if Nsize != 512:
    img2 = np.single(img2[:, 256 - Nsize // 2: 256 + Nsize // 2, 256 - Nsize // 2: 256 + Nsize // 2])
else:
    img2 = np.single(img2)

start_time = time.time()
h.cleanup = False
h.calibrate(img2[140:147, :, :])
elapsed_time = time.time() - start_time
print(f'Calibration time: {elapsed_time:5f}s ')
imga = h.reconstruct_rfftw(img2[140:147, :, :])
if isPlot:
    plt.figure()
    plt.imshow(imga, cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

start_time = time.time()
imgout = h.batchreconstruct(img2)
elapsed_time = time.time() - start_time
print(f'Reconstruction time: {elapsed_time:5f}s ')

if isPlot:
    plt.figure()
    plt.imshow(imgout[20, :, :], cmap=cm.hot, clim=(0.0, 0.7*imga.max()))

# ''' Batch process GPU '''
# start_time = time.time()
# imgout = h.batchreconstructcompact_cupy(img2)
# elapsed_time = time.time() - start_time
# print(f'Batch Reconstruction time(CuPy): {elapsed_time:5f}s ')


plt.show()