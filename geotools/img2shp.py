import argparse
import os
import datetime

import multiprocessing as mp

from osgeo import gdal, osr, ogr

'''
combine_path    1   合并文件路径
output_path     2   输出结果路径
'''
def img2vector(combine_path, output_path):
    tif_path = combine_path

    dataset = gdal.Open(tif_path)

    porj = dataset.GetProjection()
    srcband = dataset.GetRasterBand(1)
    srcband.SetNoDataValue(0)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    
    shp_path = output_path
    outDatasource = driver.CreateDataSource(shp_path)
    
    srs = osr.SpatialReference()
    srs.ImportFromWkt(porj)
    outLayer = outDatasource.CreateLayer("polygonized", srs=srs)
    
    oFieldID = ogr.FieldDefn('DN', ogr.OFTInteger)
    outLayer.CreateField(oFieldID, 1)
    gdal.Polygonize(srcband, srcband, outLayer, 0 , [], callback=None )
    outDatasource.Destroy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("gdal使用参数设置。")
    parser.add_argument('--tifinput', type=str, default='/media/data1/rapeseed/predImgs/jindong/pred/preddir', help='输入预测数据保存位置')
    parser.add_argument('--shpoutput', type=str, default='/media/data1/rapeseed/predImgs/jindong/pred/preddir/shp', help='输出数据保存位置')
    parser.add_argument('--process', type=int, default=8, help='启动线程数量，大于 1 则为多线程进行')
    args = parser.parse_args()

    cpu_count = mp.cpu_count() # 获取CPU总线程数
    if args.process > cpu_count:
        print("线程数超过CPU的总线程，请设置小于 " + str(cpu_count) + " 线程数")
        exit()
    print("参数设置：" + str(args))
    
    if not os.path.exists(args.shpoutput):
        os.mkdir(args.shpoutput)
    start = datetime.datetime.now()
    pool = mp.Pool(processes=args.process)
    print("执行转换SHP文件任务ing")
    
    imgfiles = os.listdir(args.tifinput)
    for imgfile in imgfiles:
        if not imgfile.endswith('.tif'): 
            continue
        predtif = os.path.join(args.tifinput, imgfile)
        basename = imgfile.split('.tif')[0]
        predshp = os.path.join(args.shpoutput, basename + '.shp')
        pool.apply_async(img2vector, (predtif, predshp, ))
    pool.close()
    pool.join()
    print("总耗时为：" + str(datetime.datetime.now() - start))