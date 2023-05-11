# 自动转换COG、提取轮廓、生成缩略图的需求V3

# 一、定义
# 1、所有目录都是前带/后不带/
# 2、save_root_dir:数据存储根目录（如：/data/docker/minio/data）
# 3、doc_base_dir:归档基目录（如：/cloud/save1/330703/project/1/1/raster-image）
# 4、tif_file_name：当前要处理的tif文件名全名（文件名全名含扩展名，文件名部分不含扩展名，下同），比如：EF-1-1-FM-20230406-2K-1.tif
# 5、update_api_url：状态更新API地址（POST方式）
# 6、data_id：当前数据Id
# 7、prev_progress：基础进度（%）
# 8、progress_weight：本次计算进度权重（%）

# 二、输入参数
# 1、save_root_dir
# 2、doc_base_dir
# 3、tif_file_name
# 4、update_api_urldb_name
# 5、data_id
# 6、prev_progress
# 7、progress_weight

import os
import sys
import requests
import logging
import datetime

from osgeo import gdal

from geotools.img_thum import img_thum
from geotools.img_boundary import img_boundary
from geotools.img_cog import img_cog

def main(argv = None):

    log_path = os.path.join('/usr/local', 'tif-log')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    # logger
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler(log_path + "/log.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    

    # argv
    save_root_dir = None
    doc_base_dir = None
    tif_file_name = None
    update_api_url = None
    data_id = None

    
    gdal.AllRegister()
    if argv is None:
        argv = sys.argv
    argv = gdal.GeneralCmdLineProcessor( argv )
    if argv is None:
        sys.exit(0)

    save_root_dir = argv[1]
    doc_base_dir = argv[2]
    tif_file_name = argv[3]
    update_api_url = argv[4]
    data_id = argv[5]

    if doc_base_dir[0] == '/':
        doc_base_dir = doc_base_dir[1:]

    curr_doc_dir = os.path.join(save_root_dir, doc_base_dir)
    


    # 当前要处理的tif文件路径
    curr_tif_path = os.path.join(curr_doc_dir, "out-file", tif_file_name) # curr_doc_dir/out-file/tif_file_name

    baseTifName = (tif_file_name).replace(".tif","")
    baseTifName = baseTifName.split("-")

    # ####生成缩略图
    # 计算缩略图存储文件名部分
    
    baseTifName[0] = "TN"
    thumbnail_file_name = "-".join(baseTifName) # 取文件名部分并把开头的PT-替换成TN- 比如：TN-1-1-FM-20230406-2K-1
    thumbnail_tif_path = os.path.join(curr_doc_dir, 'thumbnail')
    
    if not os.path.exists(thumbnail_tif_path):
        os.mkdir(thumbnail_tif_path)

    try:
        # 生成缩略图的代码
        # 保存缩略图到thumbnail_tif_path
        # 计算并更新进度值：假定本步骤计算时间在本次计算总时间中占20%（这需要实测得到比较准确的值）
        curr_progress = 40
        logger.info("开始执行缩略图任务")
        img_thum(tif_file_name, curr_tif_path, thumbnail_file_name, thumbnail_tif_path)
        logger.info("缩略图结束已任务")
        # 调用参数
        data = {"dataId": data_id, "progress": curr_progress}
        requests.post(update_api_url, json=data)
        # 以post方式调用update_api_url
    except Exception as ex:
        # 错误消息
        errMsg = (f"影像%s生成缩略图错误：%s"%(tif_file_name, ex))
        logger.error(errMsg)
        # print(errMsg)

        # 调用参数
        data = {"dataId": data_id, "errorMessage": errMsg}
        requests.post(update_api_url, json=data)
        # 以post方式调用update_api_url
        return
    
    # ####提取影像轮廓
    # 计算影像轮廓存储文件名部分
    baseTifName[0] = "EF"
    outline_file_name = "-".join(baseTifName) # 取文件名部分并把开头的PT-替换成EF- #比如：EF-1-1-FM-20230406-2K-1
    # shp文件组
    outline_shp_path = os.path.join(curr_doc_dir, "edge-file")
    if not os.path.exists(outline_shp_path):
        os.mkdir(outline_shp_path)
    # gdal.UseExceptions()
    try:
        # 提取影像轮廓的代码
        # 转换成shp文件组outline_shp_path保存
        # 计算并更新进度值：假定本步骤计算时间在本次计算总时间中占40%（这需要实测得到比较准确的值）
        curr_progress =  20
        logger.info("开始执行轮廓提取任务")
        img_boundary(tif_file_name, curr_tif_path, outline_file_name, outline_shp_path)
        logger.info("轮廓提取任务已结束")
        # 调用参数
        data = {"dataId": data_id, "progress": curr_progress}
        # 以post方式调用update_api_url
        requests.post(update_api_url, json=data)
    except Exception as ex:
        # 错误消息
        errMsg = (f"影像%s提取轮廓错误：%s"%(tif_file_name, ex))
        logger.error(errMsg)
        # print(errMsg)

        # 调用参数
        data = {"dataId": data_id, "errorMessage": errMsg}
        # 以post方式调用update_api_url
        requests.post(update_api_url, json=data)
        return

    # ####转换成COG格式
    # 计算COG存储文件名部分
    baseTifName[0] = "CG"
    cog_file_name = "-".join(baseTifName) # 取文件名部分并把开头的PT-替换成CG- 比如：CG-1-1-FM-20230406-2K-1
    cog_tif_path = os.path.join(curr_doc_dir, "cog-file")
    if not os.path.exists(cog_tif_path):
        os.mkdir(cog_tif_path)
    try:
        # 转换cog的代码
        # 保存转换好的cog文件到cog_tif_path
        # 计算并更新进度值：假定本步骤计算时间在本次计算总时间中占40%（这需要实测得到比较准确的值）
        curr_progress = 40
        logger.info("开始执行COG任务")
        img_cog(tif_file_name, curr_tif_path, cog_file_name, cog_tif_path)
        logger.info("COG任务已结束")
        # 调用参数
        data = {"dataId": data_id, "progress": curr_progress}
        # 以post方式调用update_api_url
        requests.post(update_api_url, json=data)
    except Exception as ex:
        # 错误消`息
        errMsg = (f"影像%s转换COG格式错误：%s"%(tif_file_name, ex))
        logger.error(errMsg)
        # print(errMsg)
        # 调用参数
        data = {"dataId": data_id, "errorMessage": errMsg}
        # 以post方式调用update_api_url
        requests.post(update_api_url, json=data)
        return

if __name__ == '__main__':
    sys.exit(main())

# python zn_img2cog.py /media/data2/zhenongGeo/testdatas cogtest PT-0413FM1-2K.tif http://localhost 10