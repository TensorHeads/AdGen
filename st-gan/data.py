import numpy as np
import tensorflow as tf
import os,time
import warp

# load data
def load(opt,test=False):
	path = "./my_data"	# change default path if needed, not recommended 

	if test:
		images_0 = np.load("{0}/images_test_new_128.npy".format(path))
		images_1 = np.load("{0}/humansWbag_test.npy".format(path))
	else:
		images_0 = np.load("{0}/images_train_new_128.npy".format(path))
		images_1 = np.load("{0}/humansWbag_train.npy".format(path))
	
	bags = np.load("{0}/bags_128.npy".format(path))
	print(bags.shape)
	print(images_0.shape)
	print(images_1.shape)
	D = {
		"image0": images_0,
		"image1": images_1,
		"bags": bags,
	}
	return D

# make training batch
def makeBatch(opt,data,PH):
	N0 = len(data["image0"])
	N1 = len(data["image1"])
	NG = len(data["bags"])
	randIdx0 = np.random.randint(N0,size=[opt.batchSize])
	randIdx1 = np.random.randint(N1,size=[opt.batchSize])
	randIdxG = np.random.randint(NG,size=[opt.batchSize])
	# put data in placeholders
	[imageBGfakeData,imageRealData,imageFGfake] = PH
	batch = {
		imageBGfakeData: data["image0"][randIdx0]/255.0,
		imageRealData: data["image1"][randIdx1]/255.0,
		imageFGfake: data["bags"][randIdxG]/255.0,
	}
	return batch

# make test batch
def makeBatchEval(opt,testImage,bags,PH):
	idxG = np.arange(opt.batchSize)
	# put data in placeholders
	[imageBG,imageFG] = PH
	batch = {
		imageBG: np.tile(testImage,[opt.batchSize,1,1,1]),
		imageFG: bags[idxG]/255.0,
	}
	return batch

# generate perturbed image
def perturbBG(opt,imageData):
	rot = opt.pertBG*tf.random_normal([opt.batchSize])
	tx = opt.pertBG*tf.random_normal([opt.batchSize])
	ty = opt.pertBG*tf.random_normal([opt.batchSize])
	O = tf.zeros([opt.batchSize])
	pPertBG = tf.stack([tx,rot,O,O,ty,-rot,O,O],axis=1) if opt.warpType=="homography" else \
			  tf.stack([O,rot,tx,-rot,O,ty],axis=1) if opt.warpType=="affine" else None
	pPertBGmtrx = warp.vec2mtrx(opt,pPertBG)
	imageData = tf.dtypes.cast(imageData,np.float64)
	image = warp.transformCropImage(opt,imageData,pPertBGmtrx)
	return image

history = [None,0,True]
# update history and group fake samples
def updateHistory(opt,newFake):
	if history[0] is None:
		history[0] = np.ones([opt.histQsize,opt.H,opt.W,3],dtype=np.float32)
		history[0][:opt.batchSize] = newFake
		history[1] = opt.batchSize
		return newFake
	else:
		randIdx = np.random.permutation(opt.batchSize)
		storeIdx = randIdx[:opt.histSize]
		useIdx = randIdx[opt.histSize:]
		# group fake samples
		hi,growing = history[1],history[2]
		extractIdx = np.random.permutation(hi if growing else opt.histQsize)[:opt.histSize]
		groupFake = np.concatenate([history[0][extractIdx],newFake[useIdx]],axis=0)
		hinew = hi+opt.batchSize-opt.histSize
		history[0][hi:hinew] = newFake[storeIdx]
		history[1] = hinew
		if hinew==opt.histQsize:
			history[1] = 0
			history[2] = False
		return groupFake
