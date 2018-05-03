# Usage:
# Input: 
# - imsize: the dimension of the input image (three dimension) -- default value is [64,128,96]
# - layer name where the feature in: indicate which layer the queried feature is in, predefined in layer_names
# - index of the feature in x dimension (from 0): the x index of the queried feature
# - index of the feature in y dimension (from 0): the y index of the queried feature
# - index of the feature in z dimension (from 0): the z index of the queried feature

# Output:
# - receptive size: size of the receptive filed
# - center: center of the receptive field
# - receptive field (left closed right open as in python index rule): range of the receptive field in the original image space (interval is left close and right open interval)

# Build-in parameters:
# [kernel size, stride, padding]
# Three dimensions can be different while the kernel is the same for each dimension
# Each kernel requires the following parameters:
# - k_i: kernel size
# - s_i: stride
# - p_i: padding (if padding is uneven, right padding will higher than left padding; "SAME" option in tensorflow)
# 
# Each layer i requires the following parameters to be fully represented: 
# - n_i: number of feature (data layer has n_1 = imagesize )
# - j_i: distance (projected to image pixel distance) between center of two adjacent features
# - r_i: receptive field of a feature in layer i
# - start_i: center position of the first feature's receptive field in layer i (idx start from 0, negative means the center fall into padding) 

import math
# predefined neural network, change the imsize accordingly
convnet =   [[3,1,1],[2,2,0],[3,1,1],[3,1,1],[2,2,0],[3,1,1],[3,1,1],[2,2,0],[3,1,1],[3,1,1]]
layer_names = ['conv1','pool1','conv2a','conv2b','pool2','conv3a','conv3b','pool3','conv4a', 'conv4b']
imsize = [64,128,96]

def outFromIn(conv, layerIn):
  n_in = layerIn[0]
  j_in = layerIn[1]
  r_in = layerIn[2]
  start_in = layerIn[3]
  k = conv[0]
  s = conv[1]
  p = conv[2]
  
  n_out = math.floor((n_in - k + 2*p)/s) + 1
  actualP = (n_out-1)*s - n_in + k 
  pR = math.ceil(actualP/2)
  pL = math.floor(actualP/2)
  
  j_out = j_in * s
  r_out = r_in + (k - 1)*j_in
  start_out = start_in + ((k-1)/2 - pL)*j_in
  return n_out, j_out, r_out, start_out
  
def printLayer(layerx, layery, layerz, layer_name):
  # the j_i, r_i and start_i should be the same for three dimensions since the initial values are the same and the kernel is the same
  assert((layerx[1] == layery[1]) &(layerx[1] == layerz[1]))
  assert((layerx[2] == layery[2]) &(layerx[2] == layerz[2]))
  assert((layerx[3] == layery[3]) &(layerx[3] == layerz[3]))
  print(layer_name + ":")
  print("\t size of feature map: (%d, %d, %d) \n \t jump: %s \n \t receptive size: %s \t start: %s " % (layerx[0], layery[0], layerz[0], layerx[1], layerx[2], layerx[3]))
 
layerInfosX = []
layerInfosY = []
layerInfosZ = []
if __name__ == '__main__':
#first layer is the data layer (image) with n_0 = image size; j_0 = 1; r_0 = 1; and start_0 = 0.5
  print ("-------Net summary------")
  currentLayerx = [imsize[0], 1, 1, 0.5]
  currentLayery = [imsize[1], 1, 1, 0.5]
  currentLayerz = [imsize[2], 1, 1, 0.5]
  printLayer(currentLayerx, currentLayery, currentLayerz, "input image")
  for i in range(len(convnet)):
    currentLayerx = outFromIn(convnet[i], currentLayerx)
    currentLayery = outFromIn(convnet[i], currentLayery)
    currentLayerz = outFromIn(convnet[i], currentLayerz)
    layerInfosX.append(currentLayerx)
    layerInfosY.append(currentLayery)
    layerInfosZ.append(currentLayerz)
    printLayer(currentLayerx, currentLayery, currentLayerz, layer_names[i])
  print ("------------------------")
  layer_name = raw_input ("Layer name where the feature in (e.g., conv4b): ")
  layer_idx = layer_names.index(layer_name)
  idx_x = int(raw_input ("index of the feature in x dimension (from 0): "))
  idx_y = int(raw_input ("index of the feature in y dimension (from 0): "))
  idx_z = int(raw_input ("index of the feature in z dimension (from 0): "))
  
  nx = layerInfosX[layer_idx][0]
  ny = layerInfosY[layer_idx][0]
  nz = layerInfosZ[layer_idx][0]
  # j, r and start are the same for three dimensions
  j = layerInfosX[layer_idx][1]
  r = layerInfosX[layer_idx][2]
  start = layerInfosX[layer_idx][3]
  assert(idx_x < nx)
  assert(idx_y < ny)
  assert(idx_z < nz)
  
  print ("receptive size: (%s, %s, %s)" % (r, r, r))
  print ("center: (%s, %s, %s)" % (start+idx_x*j, start+idx_y*j, start+idx_z*j))
  print ("receptive field (left closed right open interval as in python index rule): (%d:%d, %d:%d, %d:%d)" % (math.floor(start+idx_x*j - r/2.0),
    math.floor(start+idx_x*j + r/2.0), math.floor(start+idx_y*j - r/2.0), math.floor(start+idx_y*j + r/2.0), \
    math.floor(start+idx_z*j - r/2.0), math.floor(start+idx_z*j + r/2.0)))