
from osgeo import gdal

def spatialRefine(inputfile):
    # 打开栅格文件
    raster = gdal.Open(inputfile)

    # 获取栅格文件的坐标系
    spatialRef = raster.GetProjection()

    # 打印栅格文件的坐标系
    print("Spatial reference of the raster file is:", spatialRef)
    # 如果栅格文件缺少空间参考，则GetProjection()函数将返回空字符串。
    return spatialRef
