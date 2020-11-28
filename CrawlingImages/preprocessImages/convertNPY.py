import glob
import cv2
import numpy as np

input_path = "/content/proc_images"
inp_path_2 = "/content/proc_images_batch2"
output_path = "/content/drive/My Drive/DL_Data/STGAN_CrawledHumans"

L = glob.glob(input_path+"/*.jpg")
L.extend(glob.glob(inp_path_2+"/*.jpg"))

count_train = int(len(L) * 0.9)
count_test = len(L) - count_train

print(count_test, count_train)
train_L = L[:count_train]
train_images = np.ones([count_train,128,128,3],dtype=np.uint8)
for i in range(len(train_L)):
  img = cv2.imread(train_L[i])
  img_resized = cv2.resize(img, interpolation=cv2.INTER_CUBIC, dsize=(128, 128))
  train_images[i] = img_resized
np.save("{0}/humansWbag_backRemoved_train.npy".format(output_path),train_images)


test_L = L[count_train:]
test_images = np.ones([count_test,128,128,3],dtype=np.uint8)
for i in range(len(test_L)):
  img = cv2.imread(test_L[i])
  img_resized = cv2.resize(img, interpolation=cv2.INTER_CUBIC, dsize=(128, 128))
  test_images[i] = img_resized
np.save("{0}/humansWbag_backRemoved_test.npy".format(output_path),test_images)