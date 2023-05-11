'''
@File    :   fishNet.py
@Time    :   2023/02/12 17:06:41
@Author  :   Haowei Mu
@Version :   1.0
@Contact :   haoweimu@smail.nju.edu.cn; 18153993665
@Desc    :   ZheNong Tech
https://gdal.org/programs/gdalwarp.html
'''

# here put the import lib
import os
import datetime
import time
from osgeo import gdal
import argparse

# gdal_translate 0110-LX-2K.tif withmask222.tif -outsize 2% 2% -b 1 -b 2 -b 3 -mask 4 -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR -co NUM_THREADS=ALL_CPUS --config GDAL_TIFF_INTERNAL_MASK YES
def img_thum(tif_file_name, curr_tif_path, thumbnail_file_name, thumbnail_tif_path):

    gdal.UseExceptions()
    print(tif_file_name + "  缩略图  时间：" + str(datetime.datetime.now()))
    start = time.time()
    # Define the input and output file paths
    input_file = curr_tif_path
    output_file = os.path.join(thumbnail_tif_path, thumbnail_file_name + '.tif')

    # Open the input file using GDAL
    input_ds = gdal.Open(input_file)

    # Get the dimensions of the input image
    width = input_ds.RasterXSize
    height = input_ds.RasterYSize

    # Calculate the aspect ratio of the input image
    aspect_ratio = float(width) / float(height)

    # Set the maximum size of the thumbnail image
    max_size = 2048

    # Calculate the dimensions of the thumbnail image
    if width > height:
        thumbnail_width = max_size
        thumbnail_height = int(thumbnail_width / aspect_ratio)
    else:
        thumbnail_height = max_size
        thumbnail_width = int(thumbnail_height * aspect_ratio)
    
    # options = {
    #     'config':['GDAL_TIFF_INTERNAL_MASK', 'YES']
    # }

    config = gdal.SetConfigOption('GDAL_TIFF_INTERNAL_MASK', 'YES')
    options = gdal.TranslateOptions(width=thumbnail_width, height=thumbnail_height, bandList=[1, 2, 3], creationOptions=['COMPRESS=JPEG', 'PHOTOMETRIC=YCBCR', 'NUM_THREADS=ALL_CPUS'], maskBand=4, options=config) 
    # Generate the thumbnail image using GDAL
    gdal.Translate(output_file, input_ds,  options=options)

    # Close the input dataset
    input_ds = None
    end = time.time()
    print(f"********缩略图创建成功! 时间：%s, 耗时为： %s" %(str(datetime.datetime.now()), end - start))

if __name__ == '__main__':
    # tif_file_name, curr_tif_path, thumbnail_file_name, thumbnail_tif_path
    parser = argparse.ArgumentParser("缩略图使用参数设置。")
    parser.add_argument('--tif_file_name', default='0413FM1-2K', type=str)
    parser.add_argument('--curr_tif_path', default='/media/data2/zhenongGeo/testdatas/cogtest/out-file/0413FM1-2K.tif', type=str)
    parser.add_argument('--thumbnail_file_name', default='TN-O-0413FM1-2K', type=str)
    parser.add_argument('--thumbnail_tif_path', default='/media/data2/zhenongGeo/testdatas/cogtest/thumbnail/', type=str)
    args = parser.parse_args()

    img_thum(args.tif_file_name, args.curr_tif_path, args.thumbnail_file_name, args.thumbnail_tif_path)
# python geotools/img_thum.py