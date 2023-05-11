
import os
import os.path as osp
from datetime import datetime
from osgeo import gdal, ogr, osr, gdalconst
import time
import argparse

def getBounds(inputImg,outBounds):
    dataset = gdal.Open(inputImg)
    oDriver = ogr.GetDriverByName('ESRI Shapefile')
    oDS = oDriver.CreateDataSource(outBounds)
    srs = osr.SpatialReference(wkt=dataset.GetProjection())
    geocd = dataset.GetGeoTransform()
    oLayer = oDS.CreateLayer("polygon", srs, ogr.wkbPolygon)
    oDefn = oLayer.GetLayerDefn()
    row = dataset.RasterXSize
    line = dataset.RasterYSize
    geoxmin = geocd[0]
    geoymin = geocd[3]
    geoxmax = geocd[0] + (row) * geocd[1] + (line) * geocd[2]
    geoymax = geocd[3] + (row) * geocd[4] + (line) * geocd[5]
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(geoxmin, geoymin)
    ring.AddPoint(geoxmax, geoymin)
    ring.AddPoint(geoxmax, geoymax)
    ring.AddPoint(geoxmin, geoymax)
    ring.CloseRings()
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    outfeat = ogr.Feature(oDefn)
    outfeat.SetGeometry(poly)
    oLayer.CreateFeature(outfeat)
    outfeat = None
    oDS.Destroy()

def RasterToVector(tiffile, shpfile, maskfile = None):
    dataset = gdal.Open(tiffile)
    porj = dataset.GetProjection()
    srcband = dataset.GetRasterBand(1)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    srcband.SetNoDataValue(0)
    if os.path.exists(shpfile):
        driver.DeleteDataSource(shpfile)
    outDatasource = driver.CreateDataSource(shpfile)
    srs = osr.SpatialReference()
    srs.ImportFromWkt(porj)
    outLayer = outDatasource.CreateLayer("polygonized", srs = srs)
    oFieldID = ogr.FieldDefn('DN',ogr.OFTInteger)
    outLayer.CreateField(oFieldID, 1)
    gdal.Polygonize(srcband, srcband, outLayer,0 , [], callback=None )
    outDatasource.Destroy()


# gdal_translate -co compress=lzw -b 1 -ot byte -scale 1 1 0110-LX-2K.tif 0110-LX-2K.tif
def img_boundary(tif_file_name, curr_tif_path, outline_file_name, outline_shp_path):

    # # screen -L -Logfile inputdir2.log python img2cog.py --inputdir=/home/haowei/Zhenong/inputdir2
    gdal.UseExceptions()

    print(tif_file_name + "  轮廓图  时间：" + str(datetime.now()))
    start = time.time()
    # *******************************************step2 创建轮廓
    Outlinefile = osp.join(outline_shp_path, outline_file_name +'.shp')

    outlineImg = osp.join(outline_shp_path, outline_file_name + '.tif')
    options = gdal.TranslateOptions(bandList=[1], outputType=gdalconst.GDT_Byte, creationOptions=['compress=lzw', 'NUM_THREADS=ALL_CPUS'], scaleParams=['0', '1'])
    gdal.Translate(outlineImg, curr_tif_path, options=options)

    RasterToVector(outlineImg, Outlinefile, maskfile = None)
    end = time.time()
    print(f"********轮廓创建成功! 时间：%s, 耗时为： %s" %(str(datetime.now()), end - start))

if __name__ == "__main__":
    # tif_file_name, curr_tif_path, thumbnail_tif_path, thumbnail_file_name, outline_shp_path, outline_file_name
    parser = argparse.ArgumentParser("缩略图使用参数设置。")
    parser.add_argument('--tif_file_name', default='0413FM1-2K', type=str)
    parser.add_argument('--curr_tif_path', default='/media/data2/zhenongGeo/testdatas/cogtest/out-file/0413FM1-2K.tif', type=str)
    parser.add_argument('--outline_shp_path', default='/media/data2/zhenongGeo/testdatas/cogtest/edge-file/', type=str)
    parser.add_argument('--outline_file_name', default='EF-N-0413FM1-2K', type=str)
    args = parser.parse_args()

    img_boundary(args.tif_file_name, args.curr_tif_path, args.outline_file_name, args.outline_shp_path)

# python geotools/img_boundary.py
