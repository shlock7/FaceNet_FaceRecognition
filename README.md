## 工作环境：

- Windows
- Python3.6
- tensorflow-gpu
- opencv
- tkinter


## 总体功能：
        - Mtcnn   ： 实现人脸检测
        - FaceNet ： 实现相似度计算，用于人脸识别
        - tkinter ： 实现UI界面


## 一、MTcnn实现人脸检测功能
（1）`detect_face.py` 是在网上下载的，该文件实现了MTcnn人脸检测的相关函数
（2）`face_detector_MTcnn.py` 是对`detect_face.py`进行测试：实现了视频流下人脸的检测和定位功能。

## 二、利用faceNet 实现两张图片距离向量的计算
`train_facenet`文件夹是对`facenet`源码的copy，其中包括了训练模型的代码，根据自己的理解加了注释。
（1）`facenet.py` facenet源码，定义了相关函数。
（2）`cal_128XVector_user_facenet.py` 文件是根据`facenet.py`文件里相关函数，计算出两张图片的`distance`：
      1、`build_facenet_model（）`函数： 是建立faceNet模型用的。
      2、`cal_128_vector（）`函数： 就是计算一张图片的`distance`向量  计算结果会产生128维向量。 
      3、`cal_dist（）`函数： 计算两个数组的方差和 ，是根据这个结果来衡量两张图片的相似度。
      4、`save_data_to_csv()`:将采集的图片放到 csv 文件中` label `作为该数据的标签，后面可以通过标签来判别识别的人脸的属性。
      5、`cal_dist_from_csv（）`：输入一个128维的向量，与已经存在csv的数据对比 ，输出结果是该图片向量与CSV文件中相似的图片的`distance`和标签


## 三、collect_frame_to_csv.py 这个文件主要实现了将人脸图像存储到本地csv文件中的功能。
     1、collect_frame( )函数调用MTCNN，调用摄像头实现人脸检测，取出人脸ROI，返回一个图像。没有参数。
     2、image_to_csv( )函数实现了人脸数据的转换和存储，参数分别为图像、标签、csv文件的目录。
     该函数先调用了cal_128XVector_user_facenet.py中的build_facenet_model( )函数建立facenet网络，
     然后调用cal_128_vector( )函数将图片转换为128维向量，最后再调用saver_data_to_csv()函数将向量保存到本地。
     3、face_from_local()函数实现了将本地图像文件中的人脸提取出来，跟collect_frame( )函数相似，
     但要根据图片的尺寸对图片进行缩放，图片尺寸过大会导致识别不准确，并且要确定检测到的人脸数不大于1。

## 四、realtime_detect_face_and_recognition.py  实现视频流中人脸的属性检测 并分类
    调用MTCNN检测人脸，将人脸区域提取出来，调用cal_128_vector()函数将图像转换为128向量，
    然后调用cal_dist_from_csv()函数在本地人脸数据库中找到与当前人脸相似度最高的人，返回距离和标签，
    并将标签输出在画面中。



## 五、main.py
        主程序，增加UI界面，实现人脸识别签到



### 主页面

![image](https://github.com/Nero-iwnl/FaceNet_FaceRecognition/blob/main/programImages/main.png)

### 人脸录入

![image](https://github.com/Nero-iwnl/FaceNet_FaceRecognition/blob/main/programImages/input_name.png)

![image](https://github.com/Nero-iwnl/FaceNet_FaceRecognition/blob/main/programImages/input_face.png)

![image](https://github.com/Nero-iwnl/FaceNet_FaceRecognition/blob/main/programImages/input_local.png)

### 签到

![image](https://github.com/Nero-iwnl/FaceNet_FaceRecognition/blob/main/programImages/sign_in.png)

### 签到记录

![image](https://github.com/Nero-iwnl/FaceNet_FaceRecognition/blob/main/programImages/signinrecord.png)

