import os, shutil
import difflib

'''
inFilePath      1   输入文件地址
outFilePath     2   输出文件地址
'''
def imgName2Date(inFilePath, outFilePath):
    fileName = inFilePath.split('/')[-1]
    fileList = os.listdir(inFilePath)
    bounddir = difflib.get_close_matches("boundary", fileList)
    for name in bounddir:
        dir = os.path.join(inFilePath, name, "image/")
        files = os.listdir(dir)
        newfiles = [(fileName) + '-' + (name[0]).upper() + name[-1] + '-' + (file) for file in files]
        # print(newfiles)
        for (file, newfile) in zip(files, newfiles):
            shutil.copyfile(dir + file, outFilePath + newfile)


'''
inFilePath      1   输入文件地址
outFilePath     2   输出文件地址
'''
def labelName2Date(inFilePath, outFilePath):
    fileName = inFilePath.split('/')[-2]
    # print(fileName)
    
    fileList = os.listdir(inFilePath)
    # print(fileList)
    # bounddir = difflib.get_close_matches("boundary", fileList)
    # for name in fileList:
    #     dir = os.path.join(inFilePath, name, "label/")
    #     files = os.listdir(dir)
    newfiles = [(fileName) + '-B1-' + (file) for file in fileList]
        # print(files)
    for (file, newfile) in zip(fileList, newfiles):
        # print(file, newfile)
        shutil.copyfile(inFilePath + file, outFilePath + newfile)

def rename_sample(inFilePath):
    images = os.path.join(inFilePath, "img/")
    labels = os.path.join(inFilePath, 'label/')
    fileImages = os.listdir(images)
    fileLabels = os.listdir(labels)
    imageArr = []
    labelArr = []
    for image, label in zip(fileImages, fileLabels):
        imageArr.append((image.split('.')[0]))
        labelArr.append((label.split('_')[0]))
    # print(labelArr)
    # print(fileLabels)
    # fileList.sort()
    # fileLabels.sort()
    # filearr = []
    # labelarr = []
    # print(fileList)
    # for (file, label) in zip(fileList, fileLabels):
    # for file in fileList:
    #     newfile = file.split("-")[-1]
    #     # print(file)
    #     # if file.split('.')[0] == label.split('_')[0]:
    #     # filearr.append(file.split('.')[0]) 
    #     # labelarr.append(label.split('_')[0])
    #     os.rename(inFilePath + file, inFilePath + newfile)
    out = list(set(labelArr) & set(imageArr))
    print(len(out))
    # for o in out:
    #     file = os.path.join(images, o + '.tif')
    #     # print(file)
    #     # os.remove(file)
    #     shutil.copyfile(file, inFilePath + "1/" + o + ".tif")

if __name__ == '__main__':
    # imgName2Date("/media/data2/cropland/sampleSets/0410FM1-2K","/media/data2/cropland/1_samples/img/")
    rename_sample("/media/data2/cropland/1_samples/")
# 0216FM-2K  0216-FM-2K-1  0327FM-2K  0327KY-2K  0410FM1-2K