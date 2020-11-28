import shutil, os, time
import cv2
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
import glob
from PIL import Image
import tensorflow.compat.v1 as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

def detect_objects(image_np, sess, detection_graph, category_index):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    return image_np, np.squeeze(classes).astype(np.int32), np.squeeze(scores), np.squeeze(boxes)

def load_image_into_numpy_array(image):
    try:
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
    except:
        print("NOT LOADED BC")
        return np.array(0)


def main():
    CWD_PATH = os.getcwd()

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    MODEL_NAME = 'ssd_resnet50_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03'
    PATH_TO_CKPT = os.path.join(CWD_PATH, 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join(CWD_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90

    # Loading label map
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    # First test on images
    PATH_TO_TEST_IMAGES_DIR = '/Users/chinmayiprasad/Documents/DeepLearning/Project/object_detection/image_no_bags'
    TEST_IMAGE_PATHS = glob.glob(os.path.join(PATH_TO_TEST_IMAGES_DIR + "/*.jpg"))
    IMAGE_SIZE = (12, 8)
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    countBagImages = 0

    count = 0
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            for image_path in TEST_IMAGE_PATHS:
                try:
                    image = Image.open(image_path)
                    image_np = load_image_into_numpy_array(image)
                    image_process, classes, scores, boxes = detect_objects(image_np, sess, detection_graph, category_index)

                    if 1 in set(classes[:5]) and 31 in set(classes):
                        countBagImages += 1

                    classesBag = classes[np.where(scores >= 0.30)]
                    classesPerson = classes[np.where(scores >= 0.75)]
                    if 1 in set(classesPerson) and (31 in set(classesBag) or 27 in set(classesBag)):
                            shutil.copy(image_path,'/Users/chinmayiprasad/Documents/DeepLearning/Project/object_detection/proc_humanNoBag')
                            count += 1
                            print(count)
                            if count % 100 == 0:
                                print(count)
                                plt.figure(figsize=IMAGE_SIZE)
                                plt.imshow(image_process)
                except Exception as e:
                    print("Skipping {} and {}".format(image_path, e))
                    time.sleep(1.5)

if __name__ == '__main__':
    main()