import cv2
import os


def readVideo(inputFile, outputPath):
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    cap = cv2.VideoCapture(inputFile)
    if cap.isOpened() is False:
        raise Exception("文件读取失败")
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    #获取视频的宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))   #获取视频的高度
    fps = cap.get(cv2.CAP_PROP_FPS)    #获取视频的帧率
    frames = 0
    while(True):
        ret, frame = cap.read()
        if ret is False:
            return
        frames += 1
        cv2.imwrite(outputPath + str(frames) + '.jpg', frame)

def writeVideo(inputPath, outputFile):
    images = os.listdir(inputPath)
    images.sort()
    cap = cv2.VideoWriter(outputFile, 0x7634706d, 25, (2560, 1440), True)
    for image in images:
        frame = cv2.imread(inputPath + image)
        cap.write(frame)
    
    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    readVideo('/home/haowei/pv/captrue/20230504T000503Z_20230504T000513Z.mp4', '/home/haowei/pv/captrue/20230504T000503Z_20230504T000513Z/')
    # writeVideo('/home/haowei/pv/pre_color/20230504T000503Z_20230504T000513Z_COLOR/', '/home/haowei/pv/new/20230504T000503Z_20230504T000513Z_COLOR.mp4')
# /home/haowei/pv/captrue
        
