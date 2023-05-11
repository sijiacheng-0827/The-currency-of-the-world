from osgeo import gdal, ogr

import sys
import os.path

def Usage():
    print("""
gdal_sieve [-q] [-st threshold] [-4] [-8] [-o name=value]
           srcfile [-nomask] [-mask filename] [-of format] [dstfile]
""")
    sys.exit(1)
    
# =============================================================================
# 	Mainline
# =============================================================================

threshold = 5000
connectedness = 4
options = []
quiet_flag = 0
src_filename = None

dst_filename = None
format = 'GTiff'

mask = 'default' 

gdal.AllRegister()
argv = gdal.GeneralCmdLineProcessor( sys.argv )
if argv is None:
    sys.exit( 0 )

# Parse command line arguments.
i = 1
while i < len(argv):
    arg = argv[i]

    if arg == '-of':
        i = i + 1
        format = argv[i]

    elif arg == '-4':
        connectedness = 4
        
    elif arg == '-8':
        connectedness = 8
        
    elif arg == '-q' or arg == '-quiet':
        quiet_flag = 1
        
    elif arg == '-st':
        i = i + 1
        threshold = int(argv[i])
        
    elif arg == '-nomask':
        mask = 'none'
        
    elif arg == '-mask':
        i = i + 1
        mask = argv[i]
        
    elif arg == '-mask':
        i = i + 1
        mask = argv[i]
        
    elif arg[:2] == '-h':
        Usage()
        
    elif src_filename is None:
        src_filename = argv[i]

    elif dst_filename is None:
        dst_filename = argv[i]

    else:
        Usage()

    i = i + 1

if src_filename is None:
    Usage()
    
# =============================================================================
# 	Verify we have next gen bindings with the sievefilter method.
# =============================================================================
try:
    gdal.SieveFilter
except:
    print('')
    print('gdal.SieveFilter() not available.  You are likely using "old gen"')
    print('bindings or an older version of the next gen bindings.')
    print('')
    sys.exit(1)

# =============================================================================
#	Open source file
# =============================================================================

if dst_filename is None:
    src_ds = gdal.Open( src_filename, gdal.GA_Update )
else:
    src_ds = gdal.Open( src_filename, gdal.GA_ReadOnly )
    
if src_ds is None:
    print('Unable to open ', src_filename)
    sys.exit(1)

srcband = src_ds.GetRasterBand(1)

if mask == 'default':
    maskband = srcband.GetMaskBand()
elif mask == 'none':
    maskband = None
else:
    mask_ds = gdal.Open( mask )
    maskband = mask_ds.GetRasterBand(1)

# =============================================================================
#       Create output file if one is specified.
# =============================================================================

if dst_filename is not None:

    drv = gdal.GetDriverByName(format)
    dst_ds = drv.Create( dst_filename,src_ds.RasterXSize, src_ds.RasterYSize,1,
                         srcband.DataType )
    wkt = src_ds.GetProjection()
    if wkt != '':
        dst_ds.SetProjection( wkt )
    dst_ds.SetGeoTransform( src_ds.GetGeoTransform() )
    
    dstband = dst_ds.GetRasterBand(1)
else:
    dstband = srcband

# =============================================================================
#	Invoke algorithm.
# =============================================================================

if quiet_flag:
    prog_func = None
else:
    prog_func = gdal.TermProgress

result = gdal.SieveFilter( srcband, maskband, dstband,
                           threshold, connectedness, 
                           callback = prog_func )

# def gdal_sieve(src_filename, threshold=255):
#     """
#     基于python GDAL栅格滤波
#     :param src_filename: 输入需要处理的文件
#     :param threshold: 滤波的值大小
#     :return:
#     """
#     # 4表示对角像素不被视为直接相邻用于多边形成员资格，8表示对角像素不相邻
#     connectedness = 8
#     gdal.AllRegister()
#     print('需要处理滤波的栅格文件:{},阈值(分辨率):{}'.format(src_filename, threshold))
#     dataset = gdal.Open(src_filename, gdal.GA_Update)
#     # 获取需要处理的源栅格波段
#     src_band = dataset.GetRasterBand(1)
#     mask_band = src_band.GetMaskBand()
#     dst_band = src_band
#     prog_func = gdal.TermProgress_nocb
#     # 调用gdal滤波函数
#     result = gdal.SieveFilter(src_band, mask_band, dst_band, threshold, connectedness, callback=prog_func)
#     print('调用gdal滤波函数执行后返回结果:{}'.format(result))
#     dataset = None