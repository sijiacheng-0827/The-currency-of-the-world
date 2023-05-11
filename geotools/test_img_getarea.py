import argparse

from osgeo import ogr

def getarea(inputfile):
    vector = ogr.Open(inputfile)

    # 获取第一个图层
    layer = vector.GetLayer()

    # 定义投影
    spatialRef = layer.GetSpatialRef()

    # 定义面积单位
    areaUnit = spatialRef.GetLinearUnitsName()

    # 初始化总面积计数器
    totalArea = 0

    # 遍历所有要素并计算面积
    for feature in layer:
        geometry = feature.GetGeometryRef()
        area = geometry.GetArea()
        totalArea += area

    # 打印总面积
    print("Total area of all features in the vector file is:", totalArea, areaUnit)
    return totalArea, areaUnit


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputFile', default='', type=str, help='输入文件路径')
    args = parser.parse_args()

    totalArea, areaUnit = getarea(args.inputFile)
    print(args.inputFile + ' 的面积为: ' + totalArea + ' 面积单位为: ' + areaUnit)

# python geotools/img_getarea.py