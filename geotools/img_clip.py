import os
import time
import argparse
import datetime
import multiprocessing as mp
import numpy as np

from osgeo import gdal


'''
imgfile         1   输入文件
out_file        2   输出文件
offset_x        3   当前剪切图像x轴坐标
offset_y        4   当前剪切图像y轴坐标
clip_size       5   剪切图片大小设置
RGB             6   RGB通道设置
'''
def img2tile(imgfile, out_file, offset_x, offset_y, clip_size=1024, RGB=None):
    '''
    RGB is list, example [4,3,2]
    '''
    in_ds = gdal.Open(imgfile)
    bands_num = in_ds.RasterCount
    in_bands = []
    out_bands = []
    if RGB is None:
        for  band in range(1, bands_num + 1):
            in_band = in_ds.GetRasterBand(band)
            in_bands.append(in_band)
            im_width = in_ds.RasterXSize-1
            im_height = in_ds.RasterYSize-1
            # if im_width < offset_x + clip_size or im_height < offset_y + clip_size:
            #     return
            if im_width - offset_x < clip_size and im_height - offset_y < clip_size:
                out_band = np.zeros([clip_size, clip_size])
                out_band1 = in_band.ReadAsArray(offset_x, offset_y, im_width - offset_x, im_height - offset_y)
                out_band[:out_band1.shape[0],:out_band1.shape[1]] = out_band1[:,:]
            elif im_width - offset_x < clip_size:
                out_band = np.zeros([clip_size, clip_size])
                out_band1 = in_band.ReadAsArray(offset_x, offset_y, im_width - offset_x, clip_size)
                out_band[:out_band1.shape[0],:out_band1.shape[1]] = out_band1[:,:]
            elif im_height - offset_y < clip_size:
                out_band = np.zeros([clip_size, clip_size])
                out_band1 = in_band.ReadAsArray(offset_x, offset_y, clip_size, im_height - offset_y)
                out_band[:out_band1.shape[0],:out_band1.shape[1]] = out_band1[:,:]
            else:
                out_band = in_band.ReadAsArray(offset_x, offset_y, clip_size, clip_size)
            out_bands.append(out_band)
    else:
        bands_num = 3
        for band in RGB:
            in_band = in_ds.GetRasterBand(band)
            in_bands.append(in_band)
            im_width = in_ds.RasterXSize-1
            im_height = in_ds.RasterYSize-1
            if im_width-offset_x <clip_size and im_height-offset_y < clip_size:
                out_band = np.zeros([clip_size,clip_size])
                out_band1 = in_band.ReadAsArray(offset_x, offset_y, im_width-offset_x, im_height-offset_y)
                out_band[:out_band1.shape[0],:out_band1.shape[1]] = out_band1[:,:]
            elif im_width-offset_x <clip_size:
                out_band = np.zeros([clip_size,clip_size])
                out_band1 = in_band.ReadAsArray(offset_x, offset_y, im_width-offset_x, clip_size)
                out_band[:out_band1.shape[0],:out_band1.shape[1]] = out_band1[:,:]
            elif im_height-offset_y < clip_size:
                out_band = np.zeros([clip_size,clip_size])
                out_band1 = in_band.ReadAsArray(offset_x, offset_y, clip_size, im_height-offset_y)
                out_band[:out_band1.shape[0],:out_band1.shape[1]] = out_band1[:,:]
            else:
                out_band = in_band.ReadAsArray(offset_x, offset_y, clip_size, clip_size)
            out_bands.append(out_band)

    gtif_driver = gdal.GetDriverByName("GTiff")
    out_ds = gtif_driver.Create(out_file, clip_size, clip_size, bands_num, in_bands[0].DataType)
    ori_transform = in_ds.GetGeoTransform()

    top_left_x = ori_transform[0]  # x
    w_e_pixel_resolution = ori_transform[1] # pixel size of weight
    top_left_y = ori_transform[3] # y
    n_s_pixel_resolution = ori_transform[5] # pixel size of high

    top_left_x = top_left_x + offset_x * w_e_pixel_resolution
    top_left_y = top_left_y + offset_y * n_s_pixel_resolution

    dst_transform = (top_left_x, ori_transform[1], ori_transform[2], top_left_y, ori_transform[4], ori_transform[5])

    out_ds.SetGeoTransform(dst_transform)
    out_ds.SetProjection(in_ds.GetProjection())
    for num,out_band in enumerate(out_bands):
        num = num + 1
        out_ds.GetRasterBand(num).WriteArray(out_band)
    out_ds.FlushCache()
    del out_ds


def single_img2tile(baseTifName, inputFile, outputDir, clipsize, stride, RGB=None):
    if (inputFile.split('.')[-1]) != 'tif':
        raise Exception('文件格式错误')
    # basename = inputFile.split('/')[-1]
    tileoutdir = os.path.join(outputDir, baseTifName)
    if not os.path.exists(tileoutdir):
        os.mkdir(tileoutdir)
    geoimg = gdal.Open(inputFile)
    im_w = geoimg.RasterXSize
    im_h = geoimg.RasterYSize
    tile_name = 1
    print(baseTifName + "********开始切片 时间：" + str(datetime.datetime.now()))
    start_time = time.time()
    for x in range(0, im_w - clipsize, stride):
        for y in range(0, im_h - clipsize, stride):
            out_file = os.path.join(tileoutdir, str(tile_name)+".tif")
            img2tile(inputFile, out_file, x, y, clipsize, RGB=RGB)
            tile_name = tile_name + 1
    end_time = time.time()
    print('geotool process tile is: ', tile_name)
    print(baseTifName + "********切片完成 时间：" + str(datetime.datetime.now()) + "       切片耗时为：" + str(end_time - start_time))

'''
args        1   超参数设置
imgfile     2   检测到的输入图像文件夹下的文件
'''
def multi_img2tile(args, imgfile):
    # gdal.UseExceptions()
    if os.path.splitext(imgfile)[1] == '.tif':
        basename = imgfile.split('.tif')[0]
        geoimg = gdal.Open(os.path.join(args.imageDir, imgfile))
    
        im_width = geoimg.RasterXSize
        im_height = geoimg.RasterYSize

        tileoutdir = os.path.join(args.outputDir,'tiledir',basename)
        if not os.path.exists(tileoutdir):
            os.makedirs(tileoutdir)

        print(basename + "********开始切片 时间：" + str(time.time()))
        tile_name = len(os.listdir(tileoutdir)) + 1
        start_num = tile_name
        # print(basename)
        for y in range(0, im_height - args.stride, args.stride):
            for x in range(0, im_width - args.stride, args.stride):
                out_file = os.path.join(tileoutdir, str(tile_name)+".tif")
                # try:
                img2tile(os.path.join(args.imageDir, imgfile), out_file, x, y, args.clipsize,RGB=args.RGB)
                # except Exception as e:
                #     print(basename + " 切割错误，错误原因为：" + e)
                tile_name = tile_name + 1
        print('geotool process tile is: ',tile_name-start_num)
        print(basename + "********切片完成 时间：" + str(time.time()))


if __name__ == "__main__":

    parser = argparse.ArgumentParser("gdal使用参数设置。")
    parser.add_argument('--imageDir', type=str, default='/media/data1/cropland/', help='原始数据文件夹')
    parser.add_argument('--outputDir', type=str, default='/media/data1/cropland/predImg/pred/', help='输出数据保存位置')
    parser.add_argument('--process', type=int, default=4, help='启动线程数量，大于 1 则为进程数进行')
    parser.add_argument('--RGB', default=None, help='para si list,example [3,2,1]')
    parser.add_argument('--stride', default=1024, help='切割步长，小于切割尺寸为重叠采样')
    parser.add_argument('--clipsize', type=int, default=1024, help='采样尺寸')
    args = parser.parse_args()

    cpu_count = mp.cpu_count() # 获取CPU总线程数
    if args.process > cpu_count:
        print("线程数超过CPU的总进程，请设置小于 " + str(cpu_count) + " 进程数")
        exit()
    print("参数设置：" + str(args))
    
    if os.path.exists(args.outputDir) is False:
        os.mkdir(args.outputDir)
    start = time.time()
    pool = mp.Pool(processes=args.process)

    print("执行切割任务ing")
    imgfiles = os.listdir(args.imageDir)
    for imgfile in imgfiles:
        pool.apply_async(multi_img2tile, (args, imgfile, ))
    
    pool.close()
    pool.join()
    print("总耗时为：" + str(time.time() - start))