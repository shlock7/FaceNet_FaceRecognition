import tensorflow as tf
import detect_face
import cv2
from cal_128XVector_user_facenet import cal_128_vector,saver_data_to_csv,build_facenet_model
import numpy as np

#实时监测人脸  取出人脸的ROI
def collect_frame():
    minsize = 20
    threshold = [0.6, 0.7, 0.7]
    factor = 0.709  # scale factor
    image=None
    #########################build mtcnn########################
    with tf.Graph().as_default():
        sess = tf.Session()
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, './model/')
    capture = cv2.VideoCapture(0)
    while (capture.isOpened()):
        ret, frame = capture.read()
        bounding_box, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)

        nb_faces = bounding_box.shape[0]  # 人脸检测的个数
        # 标记人脸
        for face_position in bounding_box:
            rect = face_position.astype(int)
            image=frame[rect[1]-20:rect[3]+20,rect[0]-20:rect[2]+20]
            cv2.imshow('output',image)
            # 矩形框
            cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 255), 2, 1)
            #cv2.circle(frame,(rect[0], rect[1]),2,(0,0,255),2,1)
            cv2.putText(frame, "faces:%d" % (nb_faces), (10, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 4)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xff == 27:
            break
    capture.release()
    cv2.destroyAllWindows()
    return image

#图片生成128向量  保存到 csv文件中去
def image_to_csv(image,label,csv_dir):
    #调用facenet 模型
    sess, images_placeholder, phase_train_placeholder, embeddings = build_facenet_model()
    #计算128 vector
    array = cal_128_vector(image, sess, images_placeholder, phase_train_placeholder, embeddings)
    saver_data_to_csv(array,label,csv_dir)


def face_from_local(file_dir,csv_dir = './data/data.csv'):
    minsize = 20
    threshold = [0.6, 0.7, 0.7]
    factor = 0.709  # scale factor
    image=None
    ##
    with tf.Graph().as_default():
        sess = tf.Session()
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, './model/')
 
    frame = cv2.imread(file_dir)
    print(frame.shape)
    # 根据图片的尺寸对图片进行缩放，图片尺寸过大会导致识别不准确
    if frame.shape[0]>2000:
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
    elif frame.shape[0]>1000:
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    print(frame.shape)
    bounding_box, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)

    nb_faces = bounding_box.shape[0]  # 人脸检测的个数
    # 如果监测到人连个数大于1是无法录入的，这时直接返回一个False
    if nb_faces > 1:
        return False
    # 标记人脸
    for face_position in bounding_box:
        rect = face_position.astype(int)
        image=frame[rect[1]-20:rect[3]+20,rect[0]-20:rect[2]+20]
        # cv2.imshow('output',image)
        # 矩形框
        cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 255), 2, 1)
        #cv2.circle(frame,(rect[0], rect[1]),2,(0,0,255),2,1)
        cv2.putText(frame, "faces:%d" % (nb_faces), (10, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 4)
    
    # 保存人脸数据要加判定，放到main.py中实现
    # image_to_csv(image, label=name, csv_dir=csv_dir)
    cv2.imshow('src_picture', frame)
    cv2.imshow("Face",image)
    cv2.waitKey(0)
    return image

def collect_frame_to_csv(name,csv_dir = './data/data.csv'):
    image = collect_frame()
    image_to_csv(image, label=name, csv_dir=csv_dir)

if __name__=="__main__":
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as session:  # 解决GPU缓存不足报错
        # name = input("please input your name:")
        # collect_frame_to_csv(name)
        res = face_from_local("./data/djz.jpg")
        # print(type(res))
        # a = np.ndarray(1)
        # print(a)
        # print(type(a))
        # print(type(a) == type(res))
        # image_to_csv(res, label='test_local', csv_dir='./data/data.csv')