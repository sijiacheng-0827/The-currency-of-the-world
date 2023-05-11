import subprocess
import argparse
import datetime
import time
import os


import multiprocessing as mp

def predocker(inputDir, outputDir):
    command = ["docker", "run", "--gpus", "all", "-d", "-v", inputDir + ":/workspace/input_path","-v", outputDir + ":/workspace/output_path", "deepai/gd:v1.0"]
    print(' '.join(command))
    subprocess.call(command)
    inputNums = len(os.listdir(inputDir))
    outputNums = len(os.listdir(outputDir))
    print(inputNums, outputNums)
    while inputNums != outputNums:
        print(inputNums, outputNums)
        time.sleep(200)
        outputNums = len(os.listdir(outputDir))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert shp to semantic segmentation datasets')
    parser.add_argument('--inputDir', default='/media/data1/cropland/predImg/pred/tiledir' ,help='inputDir path' )
    parser.add_argument('--outputDir', default='/media/data1/cropland/predImg/pred/preddir/', help='outputDir path')
    parser.add_argument('--process', type=int, default=3, help='启动线程数量，大于 1 则为多线程进行')
    args = parser.parse_args()


    cpu_count = mp.cpu_count() # 获取CPU总线程数
    if args.process > cpu_count:
        print("线程数超过CPU的总进程，请设置小于 " + str(cpu_count) + " 进程数")
        exit()
    print("参数设置：" + str(args))

    start = datetime.datetime.now()
    pool = mp.Pool(processes=args.process)

    print("执行预测任务ing")
    if os.path.exists(args.outputDir) is False: os.mkdir(args.outputDir)
    imgfiles = os.listdir(args.inputDir)
    for imgfile in imgfiles:
        if os.path.exists(args.outputDir + imgfile) is False: os.mkdir(args.outputDir + imgfile)
        tiledir = os.path.join(args.inputDir, imgfile)
        preddir = os.path.join(args.outputDir, imgfile)
        # print(tiledir, preddir)
        pool.apply_async(predocker, (tiledir, preddir, ))
    
    pool.close()
    pool.join()
    print("总耗时为：" + str(datetime.datetime.now() - start))
