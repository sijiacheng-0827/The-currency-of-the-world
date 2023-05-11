# here put the import lib
import os
import os.path as osp
import datetime
from osgeo import gdal
import argparse
import time
# gdal_translate 0224-KY0221-2K.tif  0224-KY0221-2K.tif  -of COG -co COMPRESS=JPEG -co QUALITY=100  -co BIGTIFF=YES -co OVERVIEW_COMPRESS=JPEG -co OVERVIEW_QUALITY=100
def img_cog(tif_file_name, curr_tif_path, cog_file_name, cog_tif_path):

    gdal.UseExceptions()
    print(tif_file_name + "  COG   时间：" + str(datetime.datetime.now()))
    # Define the input and output file paths
    start = time.time()
    input_file = curr_tif_path
    output_file = osp.join(cog_tif_path, cog_file_name + '.tif')

    # Open the input file using GDAL
    input_ds = gdal.Open(input_file)

    # Set the creation options for the output COG file
    config = gdal.SetConfigOption("GDAL_NUM_THREADS", "ALL_CPUS")
    options = gdal.TranslateOptions(format="COG", bandList=[1, 2, 3], creationOptions=["COMPRESS=JPEG", "QUALITY=100", "OVERVIEW_COMPRESS=JPEG", "OVERVIEW_QUALITY=100", "BIGTIFF=YES"], maskBand='4', options=config) 
    # Create the output COG file using GDAL
    gdal.Translate(output_file, input_ds, options=options)

    # Close the input dataset
    input_ds = None
    end = time.time()
    print(f"********COG创建成功! 时间：%s, 总耗时为: %s"%(str(datetime.datetime.now()), end - start))
    # gdalwarp -of COG *.tif ../mosaic_cog.tif -co COMPRESS=JPEG -co QUALITY=100 -co BIGTIFF=YES --config GDAL_NUM_THREADS ALL_CPUS

if __name__ == "__main__":
    # tif_file_name, curr_tif_path, thumbnail_file_name, thumbnail_tif_path
    parser = argparse.ArgumentParser("缩略图使用参数设置。")
    parser.add_argument('--tif_file_name', default='0413FM1-2K', type=str)
    parser.add_argument('--curr_tif_path', default='/media/data2/zhenongGeo/testdatas/cogtest/out-file/0413FM1-2K.tif', type=str)
    parser.add_argument('--cog_file_name', default='CG-0413FM1-2K', type=str)
    parser.add_argument('--cog_tif_path', default='/media/data2/zhenongGeo/testdatas/cogtest/cog-file/', type=str)
    args = parser.parse_args()

    img_cog(args.tif_file_name, args.curr_tif_path, args.cog_file_name, args.cog_tif_path)
# python geotools/img_cog.py