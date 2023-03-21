import numpy as np
import cv2
import os

# загрузить модель с диска
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

# инициализация списка имен классов которые можно распознать
CLASSES = ["1. aeroplane", "2. bicycle", "3. bird", "4. boat",
           "5. bottle", "6. bus", "7. car", "8. cat", "9. chair", "10. cow", "11. dining table",
           "12. dog", "13. horse", "14. motorbike", "15. person", "16. potted plant", "17. sheep",
           "18. sofa", "19. train",]

# расширения файлов, которые возможно распознатьфвв
SUFFIXES = ['.jpg', '.jpeg', '.png', '.raw', '.gif']
img_list = []


# функция распознавания объектов
def detection(d_image, required_confidence, objects):
    global img_list
    # загрузить изображенние и создать для него input blob
    # ресайзингом его в 300x300 пикселей a потом нормализируя
    image = cv2.imdecode(np.fromfile(d_image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # прогнать blob через сеть и получить распознанные объекты и предполагаему точность
    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        # узнать точность
        confidence = detections[0, 0, i, 2]

        # убедиться что точность больше необходимой
        if confidence >= required_confidence:
            # извлечь индекс класса из "detections",
            idx = int(detections[0, 0, i, 1])
            if idx in objects:
                # напечатать объект и точность
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                return [d_image, label]


#path = str(input("Write directory of your images: "))


def choose():
    print('Choose which objects must be in the picture and write their numbers, when you are done write "-1":')
    for CLASS in CLASSES:
        print(CLASSES.index(CLASS) + 1, ". ", CLASS)

    obj = []
    parameter = 1
    while parameter >= 0:
        parameter = int(input())
        if parameter > len(CLASSES):
            print("NO SUCH OBJECT")
            continue
        if parameter >= 0:
            obj.append(parameter - 1)
    return obj
#obj = choose()

#conf = float(input("Needed confidence (from 0 to 1): "))


def main_cycle(path, obj, conf=0.7):
    imgl = []
    for dirs, folders, files in os.walk(path):
        for file in files:
            img, suff = os.path.splitext(os.path.join(dirs, file))
            if suff in SUFFIXES:
                dt = detection(img + suff, conf, obj)
                if dt != None:
                    imgl.append(dt)
        break
    return imgl


#print(main_cycle(path, obj, conf))
#print(img_list)
