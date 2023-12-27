from datetime import datetime, timedelta

t = datetime.today().strftime('%Y-%m-%d')
#t = datetime.today().strftime('%Y-%m-%d')
x = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
xx = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')
z = datetime.strftime(datetime.now() - timedelta(3), '%Y-%m-%d')
zz = datetime.strftime(datetime.now() - timedelta(4), '%Y-%m-%d')
w = datetime.strftime(datetime.now() - timedelta(5), '%Y-%m-%d')
ww = datetime.strftime(datetime.now() - timedelta(6), '%Y-%m-%d')
y = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
yy = datetime.strftime(datetime.now() - timedelta(31), '%Y-%m-%d')

offset = 5
length = 2
p1 = t[0:4]
p2 = t[offset:offset+length]
p3 = t[-2:]
p = p1+p2+p3

#print(t)
##print(pm)
##print(p2a)
##print(len(str(p2a)))
##print(pa)
##
##print(p2b)
##print(p2c)
##print(p2d)

#------------------------bulan lalu
pyy1 = yy[0:4]

offset = 5
length = 2
pyy2 = yy[offset:offset+length]

pyy3 = yy[-2:]

pyy = pyy1+pyy2+pyy3

#------------------------tanggal minggu lalu
py1 = y[0:4]

offset = 5
length = 2
py2 = y[offset:offset+length]

py3 = y[-2:]

py = py1+py2+py3

#------------------------tanggal kemarin
px1 = x[0:4]

offset = 5
length = 2
px2 = x[offset:offset+length]

px3 = x[-2:]

px = px1+px2+px3

#------------------------tanggal 2 hari lalu
pxx1 = xx[0:4]

offset = 5
length = 2
pxx2 = xx[offset:offset+length]

pxx3 = xx[-2:]

pxx = pxx1+pxx2+pxx3

#------------------------tanggal 3 hari lalu
pz1 = z[0:4]

offset = 5
length = 2
pz2 = z[offset:offset+length]

pz3 = z[-2:]

pz = pz1+pz2+pz3

#------------------------tanggal 4 hari lalu
pzz1 = zz[0:4]

offset = 5
length = 2
pzz2 = zz[offset:offset+length]

pzz3 = zz[-2:]

pzz = pzz1+pzz2+pzz3

#------------------------tanggal 5 hari lalu
pw1 = w[0:4]

offset = 5
length = 2
pw2 = w[offset:offset+length]

pw3 = w[-2:]

pw = pw1+pw2+pw3

#------------------------tanggal 6 hari lalu
pww1 = ww[0:4]

offset = 5
length = 2
pww2 = ww[offset:offset+length]

pww3 = ww[-2:]

pww = pww1+pww2+pww3
##print(p1)
##print(p2)
##print(p3)
##print(p)

#tabels = ['p_1_7'
#         ]


#text_file = open("riza/partition.sql", "w")
text_file = open("query_part_today_4.sql", "w")

#add partition
#for tabel in range(len(tabels)):
y=str("""

DELETE
FROM master.`pertamina_log_table_4`
WHERE (TIME_TO_SEC(TIMEDIFF(NOW(),`time_create_table_start`)) / 3600) > 72
;


--------------------------------------------------------------------------------------------------
--            dashboard 1 & 7 - penjualan per jam  (BAR chart, line chart-per produk)           --
--------------------------------------------------------------------------------------------------
insert into master.pertamina_log_table_4 (table_name,time_create_table_start)
values ('datamart_part.p_1_7_"""+p+"""',now());

set @last_id = LAST_INSERT_ID();

drop table if exists staging.p_1_7_"""+p+"""_temp;

CREATE table staging.p_1_7_"""+p+"""_temp like datamart_part.p_1_7_"""+p+""";

replace into staging.p_1_7_"""+p+"""_temp
SELECT site_id,
grade_name_std, 
DATETIME,
MAX(completed_ts) AS max_transaction_datetime,
HOUR,
SUM(delivery_volume) AS volume_terjual
FROM  	
	(SELECT
	COALESCE(site_id,'') AS site_id,
	COALESCE(grade_name_std,'') AS grade_name_std, 
	COALESCE(date_completed_ts,'0000-00-00') AS DATETIME,
	completed_ts,
	COALESCE(hour_completed_ts,0)AS HOUR,
	COALESCE(delivery_value,0) AS delivery_value,
	COALESCE(delivery_volume,0) AS delivery_volume,
	COALESCE(delivery_type,0) AS delivery_type,
	COALESCE(del_sell_price,0) AS del_sell_price,
	CASE
        WHEN delivery_type = 14 THEN 'Offline'
        WHEN delivery_type <> 14 
            AND (del_sell_price < 5150 OR del_sell_price > 44500) THEN 'Invalid Price'
        WHEN delivery_type <> 14 
            AND ((delivery_volume * del_sell_price) - delivery_value)  >= 1000000
            AND (((delivery_volume * del_sell_price) - delivery_value) MOD 1000000 = 0) THEN 'Display 6-6-4'
        WHEN delivery_type <> 14 
            AND delivery_value NOT BETWEEN (CEILING(del_sell_price*delivery_volume)-CEILING(del_sell_price*delivery_volume*0.1))
            AND (CEILING(del_sell_price*delivery_volume)+CEILING(del_sell_price*delivery_volume*0.1)) THEN 'Check Volume/Price Setting'
        WHEN delivery_type = 11 AND delivery_volume > 21 THEN 'Pump Test'
        WHEN DATEDIFF(insert_date_mysql, completed_ts) > 40 THEN 'Late Date'
        END AS KETERANGAN
	FROM datalake.pertamina_spbu_all_transaksi WHERE date_completed_ts = '"""+p1+"""-"""+p2+"""-"""+p3+"""' and grade_name_std NOT IN ('PERTAMAX_RACING','PERTAMAX_PLUS','SOLAR_INDUSTRI', 'BIO_SOLAR_INDUSTRI')
	) AS t
WHERE KETERANGAN IS NULL
GROUP BY site_id,
grade_name_std,
DATETIME,
HOUR;

rename table datamart_part.p_1_7_"""+p+""" to staging.p_1_7_"""+p+"""_old,
staging.p_1_7_"""+p+"""_temp to datamart_part.p_1_7_"""+p+""";

drop table if exists staging.p_1_7_"""+p+"""_old;


update master.pertamina_log_table_4
set time_create_table_end = now(), time_to_create = TIMEDIFF(now(),time_create_table_start)
where id = @last_id;

--------------------------------------------------------------------------------------------------
--                    dashboard 1 & 6 - Ketahanan stock (tank meter 1 dan 2)                    --
--------------------------------------------------------------------------------------------------

		
insert into master.pertamina_log_table_4 (table_name,time_create_table_start)
values ('datamart_part.p_1_6_stg1_"""+p+"""',now());

set @last_id = LAST_INSERT_ID();

drop table if exists staging.p_1_6_stg1_"""+p+"""_temp;

CREATE table staging.p_1_6_stg1_"""+p+"""_temp like datamart_part.p_1_6_stg1_"""+p+""";


replace into staging.p_1_6_stg1_"""+p+"""_temp
select
site_id,grade_name_std,datetime,
count(hour) as jam_penjualan, sum(volume_terjual) as total_penjualan,
case when count(hour)<>0 then sum(volume_terjual)/count(hour)
else 0 end as laju_penjualan
from datamart_part.p_1_7_"""+p+"""
group by site_id,grade_name_std, datetime		
;


rename table datamart_part.p_1_6_stg1_"""+p+""" to staging.p_1_6_stg1_"""+p+"""_old,
staging.p_1_6_stg1_"""+p+"""_temp to datamart_part.p_1_6_stg1_"""+p+""";


drop table if exists staging.p_1_6_stg1_"""+p+"""_old;


update master.pertamina_log_table_4
set time_create_table_end = now(), time_to_create = TIMEDIFF(now(),time_create_table_start)
where id = @last_id;


--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------		

insert into master.pertamina_log_table_4 (table_name,time_create_table_start)
values ('datamart_part.p_1_6_stg2_"""+p+"""',now());

set @last_id = LAST_INSERT_ID();


drop table if exists staging.p_1_6_stg2_"""+p+"""_temp;

CREATE table staging.p_1_6_stg2_"""+p+"""_temp like datamart_part.p_1_6_stg2_"""+p+""";

replace into staging.p_1_6_stg2_"""+p+"""_temp
SELECT
b.site_id,b.grade_name_std,
CASE
WHEN b.grade_name_std="BIO_SOLAR" THEN "Gasoil"
WHEN b.grade_name_std="PREMIUM" THEN "Gasoline"
WHEN b.grade_name_std="PERTALITE" THEN "Gasoline"
WHEN b.grade_name_std="PERTAMAX" THEN "Gasoline"
WHEN b.grade_name_std="DEX_LITE" THEN "Gasoil"
WHEN b.grade_name_std="PERTAMINA_DEX" THEN "Gasoil"
WHEN b.grade_name_std="SOLAR" THEN "Gasoil"
WHEN b.grade_name_std="SOLAR_NON_PSO" THEN "Gasoil"
WHEN b.grade_name_std="BIO_SOLAR_INDUSTRI" THEN "Gasoil"
WHEN b.grade_name_std="PERTALITE_KHUSUS" THEN "Gasoline"
WHEN b.grade_name_std="PERTAMAX_GREEN" THEN "Gasoline"
WHEN b.grade_name_std="PERTAMAX_PLUS" THEN "Gasoline"
WHEN b.grade_name_std="PERTAMAX_TURBO" THEN "Gasoline"
WHEN b.grade_name_std="PERTAMAX_RACING" THEN "Gasoline"
WHEN b.grade_name_std="BBG" THEN "UNKNOWN"
WHEN b.grade_name_std="BBG_INDUSTRI" THEN "UNKNOWN"
WHEN b.grade_name_std="BIO_PREMIUM" THEN "Gasoline"
WHEN b.grade_name_std="BIO_PERTAMAX" THEN "Gasoline"
WHEN b.grade_name_std="PERTAMINA_DEX_DRUM_200L" THEN "Gasoil"
WHEN b.grade_name_std="VIGAS" THEN "UNKNOWN"
ELSE "UNKNOWN"
END AS jenis_grade,
b.tank_id,a.deleted,b.tank_name,b.tank_number,
a.capacity,a.tank_type_id,a.tank_probe_status_id,
b.datetime,b.max_datetime,
a.gauge_volume,
a.theoritical_volume
FROM
        (SELECT COALESCE(site_id,'') AS site_id,
        COALESCE(grade_name_std,'') AS grade_name_std,
        COALESCE(tank_id,0) AS tank_id,
        COALESCE(tank_name,'') AS tank_name,
        COALESCE(tank_number,0) AS tank_number,
        COALESCE(date_tank_readings_dt,'0000-00-00') AS DATETIME,
        MAX(tank_readings_dt) AS max_datetime
        FROM datalake.pertamina_spbu_all_pembacaan_tanki
        WHERE date_tank_readings_dt = '"""+p1+"""-"""+p2+"""-"""+p3+"""' AND grade_name_std NOT IN ('PERTAMAX_RACING','PERTAMAX_PLUS','SOLAR_INDUSTRI','BIO_SOLAR_INDUSTRI')
        GROUP BY site_id,grade_name_std,tank_id,tank_name,tank_number,
        date_tank_readings_dt
        ) AS b
        LEFT JOIN
        (SELECT COALESCE(site_id,'') AS site_id,
        COALESCE(grade_name_std,'') AS grade_name_std,
        COALESCE(tank_id,0) AS tank_id,
        COALESCE(tank_name,'') AS tank_name,
        COALESCE(tank_number,0) AS tank_number,
        COALESCE(capacity,0) AS capacity,
        COALESCE(deleted,'') AS deleted,
        COALESCE(tank_probe_status_id,'0') AS tank_probe_status_id,
        COALESCE(tank_type_id,0) AS tank_type_id,
        tank_readings_dt,
        COALESCE(date_tank_readings_dt,'0000-00-00') AS DATETIME,
        -- CASE
         --   WHEN tank_type_id = 1 AND theoritical_volume >=0 THEN COALESCE(theoritical_volume,0)
        --    WHEN tank_type_id = 1 AND theoritical_volume < 0 THEN 0
         --   ELSE COALESCE(gauge_volume,0)
        -- END AS gauge_volume,
        gauge_volume,
        theoritical_volume
        FROM datalake.pertamina_spbu_all_pembacaan_tanki
        WHERE date_tank_readings_dt = '"""+p1+"""-"""+p2+"""-"""+p3+"""' AND grade_name_std NOT IN ('PERTAMAX_RACING','PERTAMAX_PLUS','SOLAR_INDUSTRI','BIO_SOLAR_INDUSTRI')
        ) AS a
        ON a.site_id=b.site_id
        AND a.grade_name_std=b.grade_name_std
        AND a.tank_id=b.tank_id
        AND a.tank_name=b.tank_name
        AND a.tank_number=b.tank_number
        AND a.datetime=b.datetime
        AND a.tank_readings_dt= b.max_datetime
GROUP BY b.site_id,b.grade_name_std,b.tank_id,b.tank_name,b.tank_number,
b.datetime
;

rename table datamart_part.p_1_6_stg2_"""+p+""" to staging.p_1_6_stg2_"""+p+"""_old,
staging.p_1_6_stg2_"""+p+"""_temp to datamart_part.p_1_6_stg2_"""+p+""";


drop table if exists staging.p_1_6_stg2_"""+p+"""_old;


update master.pertamina_log_table_4
set time_create_table_end = now(), time_to_create = TIMEDIFF(now(),time_create_table_start)
where id = @last_id;


--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------		

insert into master.pertamina_log_table_4 (table_name,time_create_table_start)
values ('datamart_part.p_1_6_"""+p+"""',now());

set @last_id = LAST_INSERT_ID();

drop table if exists staging.p_1_6_"""+p+"""_temp1;

CREATE table staging.p_1_6_"""+p+"""_temp1 like datamart_part.p_1_6_"""+p+""";

insert ignore staging.p_1_6_"""+p+"""_temp1
SELECT site_id, grade_name_std,jenis_grade, status_tanki, tank_id, tank_name,tank_number,capacity,tank_type_id,tank_probe_status_id, DATETIME, pembacaan_terakhir,
CASE WHEN ketahanan_stok > 720 AND laju_penjualan < 1 AND grade_name_std IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE') 
OR (ketahanan_stok > 720 AND grade_name_std NOT IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE', 'PERTAMAX_GREEN')) THEN NULL ELSE stock_terakhir END AS stock_terakhir,
stock_terakhir_real,
CASE WHEN ketahanan_stok > 720 AND laju_penjualan <  1 AND grade_name_std IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE') 
OR (ketahanan_stok > 720 AND grade_name_std NOT IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE', 'PERTAMAX_GREEN')) THEN NULL ELSE ullage END AS ullage,
CASE WHEN ketahanan_stok > 720 AND laju_penjualan <  1 AND grade_name_std IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE') 
OR (ketahanan_stok > 720 AND grade_name_std NOT IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE', 'PERTAMAX_GREEN')) THEN NULL ELSE percent_stock END AS percent_stock, datetime_week_before,
CASE WHEN ketahanan_stok > 720 AND laju_penjualan <  1 AND grade_name_std IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE') 
OR (ketahanan_stok > 720 AND grade_name_std NOT IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE', 'PERTAMAX_GREEN')) THEN NULL ELSE laju_penjualan END AS laju_penjualan,
CASE WHEN ketahanan_stok > 720 AND laju_penjualan <  1 AND grade_name_std IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE')  
OR (ketahanan_stok > 720 AND grade_name_std NOT IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE', 'PERTAMAX_GREEN')) THEN NULL ELSE ketahanan_stok END AS ketahanan_stok, ketahanan_stok_real,
CASE WHEN ketahanan_stok > 720 AND laju_penjualan <  1 AND grade_name_std IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE') 
OR (ketahanan_stok > 720 AND grade_name_std NOT IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE', 'PERTAMAX_GREEN')) THEN NULL ELSE jam_penjualan END AS jam_penjualan,
CASE WHEN ketahanan_stok > 720 AND laju_penjualan <  1 AND grade_name_std IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE') 
OR (ketahanan_stok > 720 AND grade_name_std NOT IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE', 'PERTAMAX_GREEN')) THEN NULL ELSE total_penjualan END AS total_penjualan,
CASE WHEN ketahanan_stok > 720 AND laju_penjualan <  1 AND grade_name_std IN ('PERTAMINA_DEX', 'DEX_LITE') AND tank_type_id = 1 THEN t2.KETERANGAN
WHEN (ketahanan_stok > 720 AND laju_penjualan <  1 AND ((grade_name_std IN ('PERTAMAX_TURBO')) OR (grade_name_std IN ('PERTAMINA_DEX', 'DEX_LITE') AND tank_type_id <> 1)))
	OR (ketahanan_stok > 720 AND grade_name_std NOT IN ('PERTAMAX_TURBO', 'PERTAMINA_DEX', 'DEX_LITE', 'PERTAMAX_GREEN')) THEN 'kategori E'
WHEN ketahanan_stok = 0 THEN 'kategori D1'
WHEN ketahanan_stok = 3 THEN 'kategori D2'
WHEN ketahanan_stok = 1 THEN 'kategori D3'
ELSE t2.KETERANGAN END AS KETERANGAN
-- penjualan_totalisator
FROM
(
SELECT site_id, grade_name_std, jenis_grade, status_tanki,tank_id,tank_name,tank_number,capacity,tank_type_id,tank_probe_status_id,
DATETIME, pembacaan_terakhir,
CASE 	WHEN stock_terakhir > 0 AND laju_penjualan = 0 AND stock_terakhir = stock_terakhir_1 AND stock_terakhir = stock_terakhir_2 THEN NULL -- kategori F
	WHEN (tank_probe_status_id = 3 OR stock_terakhir < 0) AND status_tanki <> 1 THEN NULL -- kategori B & C
	ELSE stock_terakhir END AS stock_terakhir, stock_terakhir_real,
CASE 	WHEN stock_terakhir > 0 AND laju_penjualan = 0 AND stock_terakhir = stock_terakhir_1 AND stock_terakhir = stock_terakhir_2 THEN NULL -- kategori F
	WHEN tank_probe_status_id = 3 AND status_tanki <> 1 THEN NULL
	WHEN stock_terakhir <= 0 THEN NULL -- kategori B & C
	ELSE ullage END AS ullage,
CASE 	WHEN stock_terakhir > 0 AND laju_penjualan = 0 AND stock_terakhir = stock_terakhir_1 AND stock_terakhir = stock_terakhir_2 THEN NULL -- kategori F
	WHEN tank_probe_status_id = 3 AND status_tanki <> 1 THEN NULL
	WHEN stock_terakhir <= 0 THEN NULL -- kategori B & C
	ELSE percent_stock END AS percent_stock,
datetime_week_before,
CASE 	WHEN stock_terakhir > 0 AND laju_penjualan = 0 AND stock_terakhir = stock_terakhir_1 AND stock_terakhir = stock_terakhir_2 THEN NULL -- kategori F
	WHEN (tank_probe_status_id = 3 OR stock_terakhir <= 0) AND status_tanki <> 1 THEN NULL -- kategori A & B,C
	ELSE laju_penjualan END AS laju_penjualan, 
CASE 	WHEN stock_terakhir > 0 AND laju_penjualan = 0 AND stock_terakhir = stock_terakhir_1 AND stock_terakhir = stock_terakhir_2 THEN NULL -- kategori F
	WHEN tank_probe_status_id = 3 AND status_tanki <> 1 THEN NULL
	WHEN stock_terakhir <= 0 THEN NULL -- kategori B & C
	WHEN stock_terakhir < 1500 AND laju_penjualan = 0 AND status_tanki = 1 THEN 3 -- kategori D
	WHEN stock_terakhir < 1500 AND laju_penjualan = 0 AND status_tanki <> 1 THEN 0 -- kategori D
	WHEN stock_terakhir < 1500 AND laju_penjualan > 0 AND grade_name_std IN ('PREMIUM','PERTALITE','BIO_SOLAR', 'PERTALITE_KHUSUS') THEN 1 -- kategori D
	WHEN stock_terakhir < 1000 AND laju_penjualan > 0 AND grade_name_std = 'PERTAMAX' THEN 1 -- kategori D
	WHEN laju_penjualan <> 0 AND (tank_probe_status_id <> 3 OR status_tanki = 1) THEN COALESCE((stock_terakhir/laju_penjualan),0)
	ELSE NULL END AS ketahanan_stok,
CASE WHEN laju_penjualan<>0 THEN COALESCE((stock_terakhir_real/laju_penjualan),0)
WHEN stock_terakhir_real <= 0 THEN 0
ELSE NULL END AS ketahanan_stok_real,
CASE 	WHEN stock_terakhir > 0 AND laju_penjualan = 0 AND stock_terakhir = stock_terakhir_1 AND stock_terakhir = stock_terakhir_2 AND stock_terakhir = stock_terakhir_3 THEN NULL -- kategori F
	WHEN (tank_probe_status_id = 3 OR stock_terakhir <= 0) AND status_tanki <> 1 THEN NULL -- kategori A & B,C
	ELSE jam_penjualan END AS jam_penjualan, jam_penjualan as jam_penjualan_real,
CASE 	WHEN stock_terakhir > 0 AND laju_penjualan = 0 AND stock_terakhir = stock_terakhir_1 AND stock_terakhir = stock_terakhir_2 AND stock_terakhir = stock_terakhir_3 THEN NULL -- kategori F
	WHEN (tank_probe_status_id = 3 OR stock_terakhir <= 0) AND status_tanki <> 1 THEN NULL -- kategori B & C
	ELSE total_penjualan END AS total_penjualan, total_penjualan as total_penjualan_real,
max_delivery_datetime,
vol_trx_dispenser_today,
stock_terakhir_1,
stock_terakhir_2,
stock_terakhir_3,
CASE 
WHEN (tank_type_id <> 1 OR (tank_type_id = 1 AND capacity > 10000)) AND stock_terakhir > 0 AND laju_penjualan = 0 
	AND stock_terakhir = stock_terakhir_1 AND stock_terakhir = stock_terakhir_2 AND stock_terakhir = stock_terakhir_3 THEN 'kategori F'
WHEN stock_terakhir <= 0 AND (tank_type_id <> 1 OR (tank_type_id = 1 AND capacity > 10000)) THEN 'kategori B,C'
WHEN tank_probe_status_id = 3 AND (tank_type_id <> 1 OR (tank_type_id = 1 AND capacity > 10000)) THEN 'kategori A'
WHEN tank_type_id = 1 AND capacity <= 10000 AND stock_terakhir > 0 AND vol_trx_dispenser_today IS NOT NULL THEN 'PST 1'
WHEN tank_type_id = 1 AND capacity <= 10000 AND (stock_terakhir < 0 OR stock_terakhir = stock_terakhir_real) AND vol_trx_dispenser_today IS NULL THEN 'PST 2'
WHEN tank_type_id = 1 AND capacity <= 10000 AND stock_terakhir <= 0 AND vol_trx_dispenser_today IS NOT NULL THEN 'PST 3'
ELSE 'normal'
END AS KETERANGAN
-- penjualan_totalisator
FROM
(
SELECT
site_id, site_pst,tank_pst,grade_name_std,jenis_grade,status_tanki,tank_id,tank_name,tank_number,capacity,tank_type_id,tank_probe_status_id,
DATETIME,pembacaan_terakhir,
CASE WHEN status_tanki = 1 AND vol_trx_dispenser_today IS NOT NULL THEN stock_terakhir-vol_trx_dispenser_today -- rules 1 tank PST (stock) >> kemungkinan tambah kolom tank di datamart 1_7
ELSE stock_terakhir END AS stock_terakhir,
CASE WHEN stock_terakhir < 0 THEN 0
ELSE stock_terakhir END AS stock_terakhir_real,
stock_terakhir_1,
stock_terakhir_2,
stock_terakhir_3,
(capacity-stock_terakhir) AS ullage,
CASE WHEN capacity<>0 THEN(stock_terakhir/capacity)*100
ELSE 0 END AS percent_stock,
datetime_week_before,
-- month_before,
CASE WHEN status_tanki =1 AND vol_trx_dispenser_today IS NOT NULL  AND laju_penjualan_dispenser IS NOT NULL THEN laju_penjualan_dispenser
WHEN status_tanki =1  AND vol_trx_dispenser_today IS NULL AND max_delivery_datetime IS NOT NULL AND jam_penjualan_pst <> 0 THEN total_penjualan_pst/jam_penjualan_pst
WHEN laju_penjualan IS NOT NULL THEN laju_penjualan
WHEN laju_penjualan IS NULL AND laju_penjualan_atg IS NOT NULL THEN laju_penjualan_atg 
WHEN laju_penjualan IS NULL AND laju_penjualan_atg IS NULL AND laju_penjualan_dispenser IS NOT NULL THEN laju_penjualan_dispenser
WHEN (laju_penjualan IS NULL AND laju_penjualan_atg IS NULL AND laju_penjualan_dispenser IS NULL ) THEN laju_penjualan_shipment
ELSE NULL END AS laju_penjualan,
CASE WHEN status_tanki =1 AND  vol_trx_dispenser_today IS NOT NULL  AND laju_penjualan_dispenser IS NOT NULL THEN jam_penjualan_avg
WHEN status_tanki =1 AND vol_trx_dispenser_today IS NULL AND max_delivery_datetime IS NOT NULL THEN jam_penjualan_pst
WHEN laju_penjualan IS NOT NULL THEN jam_penjualan
WHEN laju_penjualan IS NULL AND laju_penjualan_atg IS NOT NULL THEN 168
WHEN laju_penjualan IS NULL AND laju_penjualan_atg IS NULL AND laju_penjualan_dispenser IS NOT NULL THEN jam_penjualan_avg
WHEN (laju_penjualan IS NULL AND laju_penjualan_atg IS NULL AND laju_penjualan_dispenser IS NULL) THEN 168
ELSE NULL END AS jam_penjualan,
CASE WHEN status_tanki =1 AND vol_trx_dispenser_today IS NOT NULL  AND laju_penjualan_dispenser IS NOT NULL THEN vol_trx_dispenser
WHEN status_tanki =1  AND vol_trx_dispenser_today IS NULL AND max_delivery_datetime IS NOT NULL THEN total_penjualan_pst
WHEN laju_penjualan IS NOT NULL THEN total_penjualan
WHEN laju_penjualan IS NULL AND laju_penjualan_atg IS NOT NULL THEN total_penjualan_atg
WHEN laju_penjualan IS NULL AND laju_penjualan_atg IS NULL AND laju_penjualan_dispenser IS NOT NULL THEN vol_trx_dispenser
WHEN (laju_penjualan IS NULL AND laju_penjualan_atg IS NULL AND laju_penjualan_dispenser IS NULL) THEN total_penjualan_shipment
ELSE NULL END AS total_penjualan,
max_delivery_datetime,
vol_trx_dispenser_today
-- penjualan_totalisator
FROM
(
SELECT
	a.site_id,q.site_id AS site_pst,q.device_info AS tank_pst,
	CASE 
	WHEN q.device_type IS NOT NULL AND a.tank_type_id = 2 THEN '0'
	WHEN q.device_type IS NOT NULL AND a.tank_type_id <> 2 AND a.gauge_volume = a.theoritical_volume THEN '0'
	WHEN a.tank_type_id = 1 AND a.gauge_volume <> a.theoritical_volume THEN '1'
	ELSE 0 END AS status_tanki,
	a.grade_name_std,a.jenis_grade,a.tank_id,a.tank_name,a.tank_number,a.capacity,a.tank_type_id,
	a.tank_probe_status_id,a.datetime,a.max_datetime AS pembacaan_terakhir,
	CASE WHEN a.tank_type_id = 2 THEN a.gauge_volume 
	WHEN a.tank_type_id <> 2 AND a.gauge_volume = a.theoritical_volume THEN a.gauge_volume
	WHEN a.tank_type_id <> 2 AND a.gauge_volume <> a.theoritical_volume THEN a.theoritical_volume
	END AS stock_terakhir, 
	CASE WHEN a.tank_type_id = 2 THEN u.gauge_volume 
	WHEN a.tank_type_id <>2 AND u.gauge_volume = u.theoritical_volume THEN u.gauge_volume
	WHEN a.tank_type_id <> 2 AND u.gauge_volume <> u.theoritical_volume THEN u.theoritical_volume
	END AS stock_terakhir_1,
	CASE WHEN a.tank_type_id = 2 THEN v.gauge_volume 
	WHEN a.tank_type_id <>2 AND v.gauge_volume = v.theoritical_volume THEN v.gauge_volume
	WHEN a.tank_type_id <> 2 AND v.gauge_volume <> v.theoritical_volume THEN v.theoritical_volume
	END AS stock_terakhir_2,
	CASE WHEN a.tank_type_id = 2 THEN w.gauge_volume 
	WHEN a.tank_type_id <>2 AND w.gauge_volume = w.theoritical_volume THEN w.gauge_volume
	WHEN a.tank_type_id <> 2 AND w.gauge_volume <> w.theoritical_volume THEN w.theoritical_volume
	END AS stock_terakhir_3,
	COALESCE(a.datetime,'0000-00-00')- INTERVAL 7 DAY AS datetime_week_before,
	DATE(t.max_datetime) AS max_delivery_datetime,
	s.vol_trx_dispenser AS vol_trx_dispenser_today,
	CASE WHEN q.device_type IS NOT NULL AND a.tank_type_id <> 2 AND a.gauge_volume <> a.theoritical_volume 
	AND s.vol_trx_dispenser IS NULL AND t.max_datetime IS NOT NULL THEN DATEDIFF(a.datetime,t.max_datetime)* 24
	ELSE NULL END AS jam_penjualan_pst,
	CASE WHEN q.device_type IS NOT NULL AND a.tank_type_id <> 2 AND a.gauge_volume <> a.theoritical_volume 
	AND s.vol_trx_dispenser IS NULL AND t.max_datetime IS NOT NULL AND t.drop_volume > a.theoritical_volume THEN t.drop_volume - a.theoritical_volume
	ELSE NULL END AS total_penjualan_pst,
	h.jam_penjualan,
	COALESCE(b.jam_penjualan,0) AS jam_penjualan_avg,
	COALESCE(i.jam_penjualan,0)  AS jam_penjualan_atg,
	o.vol_trx_dispenser AS total_penjualan,
	COALESCE(b.total_penjualan,0) AS total_penjualan_avg,
	COALESCE(i.vol_trx_atg,0) AS total_penjualan_atg,
	CASE WHEN h.jam_penjualan <> 0 THEN o.vol_trx_dispenser/h.jam_penjualan
	ELSE NULL END AS laju_penjualan,
        CASE WHEN COALESCE(b.jam_penjualan,0) <> 0 THEN COALESCE(b.total_penjualan,0) / COALESCE(b.jam_penjualan,0)
	ELSE NULL END AS laju_penjualan_avg,
	CASE WHEN COALESCE(i.jam_penjualan,0) <> 0 THEN COALESCE(i.vol_trx_atg,0) / 168
	ELSE NULL END AS laju_penjualan_atg,
	COALESCE(i.vol_trx_dispenser,0) AS vol_trx_dispenser,
	CASE WHEN COALESCE(b.jam_penjualan,0)  <> 0 THEN COALESCE(i.vol_trx_dispenser,0)/COALESCE(b.jam_penjualan,0) 
	ELSE NULL END AS laju_penjualan_dispenser,
	CASE WHEN aa.total_penjualan IS NOT NULL THEN aa.total_penjualan/168
	WHEN z.total_penjualan IS NOT NULL THEN z.total_penjualan/ 168
	ELSE NULL
	END AS laju_penjualan_shipment,
	CASE WHEN aa.total_penjualan IS NOT NULL THEN aa.total_penjualan
	WHEN z.total_penjualan IS NOT NULL THEN z.total_penjualan
	ELSE NULL
	END AS total_penjualan_shipment
	FROM
		(SELECT * FROM datamart_part.p_1_6_stg2_"""+p+"""
		WHERE deleted = 0)AS a 
	LEFT JOIN
		(SELECT site_id,`grade_name_std`,SUM(`jam_penjualan`) AS jam_penjualan,
		SUM(`total_penjualan`) AS total_penjualan FROM datamart.`pertamina_dashboard_1_6_stg1`
		WHERE DATETIME BETWEEN '"""+py1+"""-"""+py2+"""-"""+py3+"""' AND '"""+px1+"""-"""+px2+"""-"""+px3+"""'
		GROUP BY site_id, grade_name_std)AS b
		ON a.site_id=b.site_id
		AND a.grade_name_std=b.grade_name_std
	LEFT JOIN
		(SELECT * FROM datamart_part.p_1_6_stg1_"""+py+""") AS h
		ON a.site_id=h.site_id
		AND a.grade_name_std=h.grade_name_std
		AND a.datetime- INTERVAL 7 DAY=h.datetime
	LEFT JOIN
		(SELECT site_id, grade_name_std, tank_id, tank_name, 
		SUM(jam_penjualan) AS jam_penjualan,
		SUM(vol_trx_atg) AS vol_trx_atg,
		SUM(vol_trx_dispenser) AS vol_trx_dispenser
		FROM
		(SELECT
		site_id,grade_name_std,DATETIME,tank_id,tank_name,
		24 AS jam_penjualan, 
		vol_trx_atg, vol_trx_dispenser
		FROM datamart.`pertamina_dashboard_8_1_volume_atg_vs_pump`
		WHERE DATETIME BETWEEN '"""+py1+"""-"""+py2+"""-"""+py3+"""' AND '"""+px1+"""-"""+px2+"""-"""+px3+"""') AS t
		GROUP BY site_id, grade_name_std, tank_id, tank_name) AS i
		ON a.site_id = i.site_id
		AND a.grade_name_std = i.grade_name_std
		AND a.tank_id = i.tank_id
		AND a.tank_name = i.tank_name
	LEFT JOIN
		(SELECT
		site_id,grade_name_std,DATETIME,tank_id,tank_name,
		24 AS jam_penjualan, 
		vol_trx_atg, vol_trx_dispenser
		FROM datamart_part.p_8_1_atg_pump_"""+py+""") AS o
		ON a.site_id = o.site_id
		AND a.grade_name_std = o.grade_name_std
		AND a.datetime- INTERVAL 7 DAY=o.datetime
		AND a.tank_id = o.tank_id
		AND a.tank_name = o.tank_name
	LEFT JOIN 
		(SELECT * FROM master.`pertamina_master_tanki_PST`) q
		ON a.site_id = q.site_id
		AND a.tank_id= q.device_id 
		AND a.tank_number = q.device_no
		AND a.tank_name = q.device_info
	LEFT JOIN
	(SELECT
		site_id,grade_name_std,DATETIME,tank_id,tank_name,
		24 AS jam_penjualan, 
		vol_trx_atg, vol_trx_dispenser
		FROM datamart_part.p_8_1_atg_pump_"""+px+""") AS s
		ON a.site_id = s.site_id
		AND a.grade_name_std = s.grade_name_std
		AND a.datetime- INTERVAL 1 DAY=s.datetime
		AND a.tank_id = s.tank_id
		AND a.tank_name = s.tank_name
	LEFT JOIN
		(SELECT	site_id,grade_name_std, tank_id,tank_name,MAX(`date_record_entry_ts`) AS max_datetime,drop_volume
		FROM
		(SELECT	site_id,grade_name_std,tank_id,tank_name,`date_record_entry_ts`,
		LAST_VALUE(drop_volume) OVER (PARTITION BY site_id,grade_name_std,tank_id
		ORDER BY row_num  RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING ) AS drop_volume 
		FROM
		(SELECT	site_id,grade_name_std,tank_id,tank_name,`date_record_entry_ts`,drop_volume,
		ROW_NUMBER() OVER (PARTITION BY site_id,grade_name_std,tank_id ORDER BY `date_record_entry_ts`) AS row_num
		FROM datalake.`pertamina_spbu_all_delivery`
		WHERE `date_record_entry_ts` BETWEEN '"""+pyy1+"""-"""+pyy2+"""-"""+pyy3+"""' AND '"""+p1+"""-"""+p2+"""-"""+p3+"""') AS t ) AS t1
		GROUP BY site_id,grade_name_std,tank_id,tank_name) AS t
		ON a.site_id = t.site_id
		AND a.grade_name_std = t.grade_name_std
		AND a.tank_id = t.tank_id
		AND a.tank_name = t.tank_name
	    LEFT JOIN 
		(SELECT * FROM datamart_part.p_1_6_stg2_"""+px+""" WHERE deleted = 0)AS u 
		ON a.site_id = u.site_id
		AND a.grade_name_std = u.grade_name_std
		AND a.datetime - INTERVAL 1 DAY=u.datetime
		AND a.tank_id = u.tank_id
		AND a.tank_name = u.tank_name
	LEFT JOIN 
		(SELECT * FROM datamart_part.p_1_6_stg2_"""+pxx+""" WHERE deleted = 0)AS v 
		ON a.site_id = v.site_id
		AND a.grade_name_std = v.grade_name_std
		AND a.datetime - INTERVAL 2 DAY=v.datetime
		AND a.tank_id = v.tank_id
		AND a.tank_name = v.tank_name
	LEFT JOIN 
		(SELECT * FROM datamart_part.p_1_6_stg2_"""+pz+""" WHERE deleted = 0)AS w 
		ON a.site_id = w.site_id
		AND a.grade_name_std = w.grade_name_std
		AND a.datetime - INTERVAL 3 DAY=w.datetime
		AND a.tank_id = w.tank_id
		AND a.tank_name = w.tank_name
	LEFT JOIN
		(SELECT t2.site_id, t2.grade_name_std,t2.jml_tanki,t1.lo_qty/COALESCE(t2.jml_tanki,1) AS total_penjualan FROM
		(SELECT site_id, grade_name_std, COUNT(*) AS jml_tanki
		FROM datamart_part.p_1_6_stg2_"""+p+""" 
		GROUP BY site_id, grade_name_std) AS t2
		LEFT JOIN
		(SELECT spbu_number, lo_produk_std, SUM(lo_qty)*1000 AS lo_qty FROM datamart.`pertamina_dashboard_10_3_shipment`
		WHERE date_gateout_time BETWEEN '"""+py1+"""-"""+py2+"""-"""+py3+"""' AND '"""+px1+"""-"""+px2+"""-"""+px3+"""'
		GROUP BY spbu_number,lo_produk_std ) AS t1
		ON t1.spbu_number = t2.site_id
		AND t1.lo_produk_std = t2.grade_name_std) AS z
		ON a.site_id = z.site_id
		AND a.grade_name_std = z.grade_name_std
	LEFT JOIN
		(SELECT t2.site_id, t2.grade_name_std,t2.jml_tanki,t1.lo_qty/COALESCE(t2.jml_tanki,1) AS total_penjualan FROM
		(SELECT site_id, grade_name_std, COUNT(*) AS jml_tanki
		FROM datamart_part.p_1_6_stg2_"""+p+""" 
		GROUP BY site_id, grade_name_std) AS t2
		LEFT JOIN
		(SELECT `site_id`, `grade_name_std`, SUM(quantity) AS lo_qty FROM datamart.`pertamina_dashboard_10_4_sap_lo`
		WHERE `DATETIME` BETWEEN '"""+py1+"""-"""+py2+"""-"""+py3+"""' AND '"""+px1+"""-"""+px2+"""-"""+px3+"""'
		GROUP BY `site_id`,`grade_name_std` ) AS t1
		ON t1.`site_id` = t2.site_id
		AND t1.`grade_name_std` = t2.grade_name_std) AS aa
		ON a.site_id = aa.site_id
		AND a.grade_name_std = aa.grade_name_std
	GROUP BY 
	a.site_id,
	a.grade_name_std, 
	a.datetime,
	a.tank_id,
	a.tank_name,
	a.tank_number	
) AS t ) AS t1) AS t2
;

delete from staging.p_1_6_"""+p+"""_temp1
where (site_id IN ('3440317','3445304')
AND grade_name_std = 'bio_solar')
OR (site_id in ('3340201','3440306','3440309','3445309','3446404','3346401','3446129')
and grade_name_std = 'premium')
;

UPDATE staging.p_1_6_"""+p+"""_temp1
SET grade_name_std = REPLACE(grade_name_std , '_',' ' );

drop table if exists staging.p_1_6_"""+p+"""_temp;

CREATE table staging.p_1_6_"""+p+"""_temp like datamart_part.p_1_6_"""+p+""";

replace into staging.p_1_6_"""+p+"""_temp
select * from staging.p_1_6_"""+p+"""_temp1;

rename table datamart_part.p_1_6_"""+p+""" to staging.p_1_6_"""+p+"""_old,
staging.p_1_6_"""+p+"""_temp to datamart_part.p_1_6_"""+p+""";


drop table if exists staging.p_1_6_"""+p+"""_old;
drop table if exists staging.p_1_6_"""+p+"""_temp1;

update master.pertamina_log_table_4
set time_create_table_end = now(), time_to_create = TIMEDIFF(now(),time_create_table_start)
where id = @last_id;


--------------------------------------------------------------------------------------------------
--                    dashboard 1 & 8 - kategori Coverage Hour                  --
--------------------------------------------------------------------------------------------------

		
insert into master.pertamina_log_table_4 (table_name,time_create_table_start)
values ('datamart_part.p_1_8_"""+p+"""',now());

set @last_id = LAST_INSERT_ID();

drop table if exists staging.p_1_8_"""+p+"""_temp;

CREATE table staging.p_1_8_"""+p+"""_temp like datamart_part.p_1_8_"""+p+""";

replace into staging.p_1_8_"""+p+"""_temp
SELECT 
`site_id`,
`grade_name_std`,
`jenis_grade`,
DATETIME,
pembacaan_terakhir,
stock_terakhir,
`laju_penjualan`,
jam_penjualan,
total_penjualan,
keterangan,
coverage_hour,
waktu_tempuh,
kategori
from
	(SELECT 
	`site_id`,
	status_tanki,
	`grade_name_std`,
	`jenis_grade`,
	DATETIME,
	pembacaan_terakhir,
	stock_terakhir,
	`laju_penjualan`,
	jam_penjualan,
	total_penjualan,
	keterangan,
	coverage_hour,
	waktu_tempuh,
	CASE
	WHEN coverage_hour <= 1 THEN 'kritis'
	WHEN coverage_hour < waktu_tempuh THEN 'kritis'
	WHEN coverage_hour > (waktu_tempuh + 3 ) THEN 'aman'
	WHEN coverage_hour IS NULL AND grade_name_std IN ('PERTAMAX TURBO','PERTAMINA DEX')
		AND volume_terjual_today IS NOT NULL THEN 'aman'
	WHEN coverage_hour > waktu_tempuh THEN 'warning'
	WHEN coverage_hour IS NULL THEN 'warning'
	WHEN coverage_hour > waktu_tempuh AND coverage_hour <= (waktu_tempuh + 3 ) THEN 'warning' 
	END AS kategori
	FROM
		(SELECT a.`site_id`,
		status_tanki,
		a.`grade_name_std`,
		`jenis_grade`,
		a.`datetime`,
		pembacaan_terakhir,
		stock_terakhir,
		`laju_penjualan`,
		jam_penjualan,
		total_penjualan,
		keterangan,
		coverage_hour_spbu AS coverage_hour,
		volume_terjual AS volume_terjual_today,
		CASE WHEN b.waktu_tempuh IS NULL AND d.avg_waktu_tempuh IS NOT NULL THEN d.avg_waktu_tempuh
		WHEN b.waktu_tempuh IS NULL AND d.avg_waktu_tempuh IS NULL THEN e.avg_waktu_tempuh_city
		ELSE b.waktu_tempuh
		END AS waktu_tempuh
		FROM 
	(SELECT `site_id`,
	ROUND(AVG(status_tanki)) as status_tanki,
	`grade_name_std`,
	`jenis_grade`,
	`datetime`,
	MAX(pembacaan_terakhir) AS pembacaan_terakhir,
	SUM(`stock_terakhir`) AS stock_terakhir,
	CASE WHEN SUM(jam_penjualan) <> 0 THEN SUM(total_penjualan)/ SUM(jam_penjualan) END AS`laju_penjualan`,
	SUM(jam_penjualan) AS jam_penjualan,
	SUM(total_penjualan) AS total_penjualan,
	CASE WHEN SUM(stock_terakhir) < 1500 AND SUM(laju_penjualan) = 0 AND capacity > 10000 AND ROUND(AVG(status_tanki)) = 1 THEN 'kategori D2'
		WHEN SUM(stock_terakhir) < 1500 AND SUM(laju_penjualan) = 0 AND ROUND(AVG(status_tanki)) <> 1 THEN 'kategori D1'
		WHEN SUM(stock_terakhir) < 1500 AND grade_name_std IN ('PREMIUM','PERTALITE','BIO SOLAR', 'PERTALITE KHUSUS')  THEN 'kategori D3'
		WHEN SUM(stock_terakhir) < 1000 AND grade_name_std = 'PERTAMAX'  THEN 'kategori D3'
		WHEN SUM(stock_terakhir) IS NOT NULL THEN keterangan
		ELSE keterangan  END AS KETERANGAN,
	CASE WHEN SUM(stock_terakhir) < 1500 AND SUM(laju_penjualan) = 0 AND capacity > 10000 AND AVG(status_tanki) = 1 THEN 3
		WHEN SUM(stock_terakhir) < 1500 AND SUM(laju_penjualan) = 0 AND AVG(status_tanki) <> 1 THEN 0
		WHEN SUM(stock_terakhir) < 1500 AND stock_terakhir > 0 AND grade_name_std IN ('PREMIUM','PERTALITE','BIO SOLAR', 'PERTALITE KHUSUS')  THEN 1
		WHEN SUM(stock_terakhir) < 1000 AND grade_name_std = 'PERTAMAX' THEN 1
		WHEN SUM(jam_penjualan) <> 0 AND (SUM(total_penjualan)/ SUM(jam_penjualan)) <> 0 THEN SUM(stock_terakhir)/(SUM(total_penjualan)/ SUM(jam_penjualan))
	END AS coverage_hour_spbu
	FROM datamart_part.p_1_6_"""+p+"""
	GROUP BY site_id, grade_name_std
	) a
	LEFT JOIN
	(SELECT `plant`,`plant_desc`,`code_spbu`, REPLACE(material , '_',' ' ) AS grade_name_std , MAX(`waktu_tempuh`) AS waktu_tempuh 
	FROM master.`pertamina_master_waktu_tempuh`
	GROUP BY `code_spbu`,`material`) b
	ON a.site_id = b.code_spbu
	AND a.grade_name_std = b.grade_name_std
	LEFT JOIN
	(SELECT code_spbu, city FROM master.`pertamina_master_spbu`) c
	ON a.site_id = c.code_spbu
	LEFT JOIN
	(SELECT a.grade_name_std, c.city, AVG(b.waktu_tempuh) AS avg_waktu_tempuh FROM datamart_part.p_1_6_"""+p+""" a 
	LEFT JOIN master.`pertamina_master_waktu_tempuh` b
	ON a.site_id = b.code_spbu
	LEFT JOIN master.`pertamina_master_spbu` c
	ON a.site_id = c.code_spbu
	GROUP BY c.city, a.grade_name_std) d
	ON a.grade_name_std = d.grade_name_std
	AND c.city = d.city
	LEFT JOIN
	(SELECT a.grade_name_std, c.city, AVG(b.waktu_tempuh) AS avg_waktu_tempuh_city FROM datamart_part.p_1_6_"""+p+""" a 
	LEFT JOIN master.`pertamina_master_waktu_tempuh` b
	ON a.site_id = b.code_spbu
	LEFT JOIN master.`pertamina_master_spbu` c
	ON a.site_id = c.code_spbu
	GROUP BY c.city ) e
	ON c.city = e.city
	LEFT JOIN
	(SELECT `site_id`,REPLACE(grade_name_std , '_',' ' ) AS grade_name_std ,`datetime`,`volume_terjual` FROM datamart_part.p_1_3_"""+p+""") f
	ON a.site_id = f.site_id
	AND a.grade_name_std =  f.grade_name_std
	AND a.datetime = f.datetime
	) t) t1;


rename table datamart_part.p_1_8_"""+p+""" to staging.p_1_8_"""+p+"""_old,
staging.p_1_8_"""+p+"""_temp to datamart_part.p_1_8_"""+p+""";


drop table if exists staging.p_1_8_"""+p+"""_old;


update master.pertamina_log_table_4
set time_create_table_end = now(), time_to_create = TIMEDIFF(now(),time_create_table_start)
where id = @last_id;



"""),
text_file.write("%s" % y)


text_file.close()

#print(y)


