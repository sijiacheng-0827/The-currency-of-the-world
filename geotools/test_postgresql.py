import psycopg2
import geopandas as gpd

# 创建连接
conn = psycopg2.connect(database="zhenongdb", user="postgres", password="123456", host="192.168.0.19", port=5432)
cur = conn.cursor()

# 创建表格
# cur.execute("CREATE TABLE zhenonggeom (id serial PRIMARY KEY, geom geometry);")
# conn.commit()

# 读取矢量文件
gdf = gpd.read_file("/media/data2/rapeseed/predImgs/jindong/pred/preddir/0410FM1-2K.shp")

# 将数据插入表格中
for i, row in gdf.iterrows():
    # print((i))
    # cur.execute(f"INSERT INTO geom VALUES (ST_GeomFromText('{row['geometry'].wkt}', 4326));")
    cur.execute("INSERT INTO geom VALUES (ST_GeomFromText(" + (row['geometry']).wkt + ", 4326));")
    # -- shp2pgsql -d 0316FM-2K.shp zhenonggeom | psql -h localhost -U postgres -d zhenongdb -p 5432
    # -- pgsql2shp -f highway_nhs_select.shp -h localhost -p 5432 -u postgres -P haowei123 geobase "select * from highway_nhs_select"

conn.commit()

# 关闭连接
conn.close()
