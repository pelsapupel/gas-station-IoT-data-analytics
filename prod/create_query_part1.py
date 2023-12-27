from datetime import datetime, timedelta

t = datetime.today().strftime('%Y-%m-%d')
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

#print(p1,'-',p2,'-',p3)
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
#print(p)

#tabels = ['p_1_7'
#         ]


#text_file = open("riza/partition.sql", "w")
text_file = open("query_part_today_1.sql", "w")

#add partition
#for tabel in range(len(tabels)):
y=str("""

DELETE
FROM master.`pertamina_log_table`
WHERE (TIME_TO_SEC(TIMEDIFF(NOW(),`time_create_table_start`)) / 3600) > 72
;


--------------------------------------------------------------------------------------------------
--                 Dashboard 5 - Tipe pembayaran (resume - pie, tabel all transaksi)                       --
--------------------------------------------------------------------------------------------------
insert into master.pertamina_log_table (table_name,time_create_table_start)
values ('datamart_part.p_5_1_"""+p+"""',now());

set @last_id = LAST_INSERT_ID();

drop table if exists staging.p_5_1_"""+p+"""_temp;

CREATE table staging.p_5_1_"""+p+"""_temp like datamart_part.p_5_1_default;


replace into staging.p_5_1_"""+p+"""_temp
SELECT 
site_id,grade_name_std,
DATETIME,MAX(max_transaction_datetime)AS max_transaction_datetime,
MAX(insert_date_mysql) AS max_insert_date_mysql,
payment_desc,bank_id,bank_name,
SUM(delivery_value) AS delivery_value,
SUM(delivery_volume) AS delivery_volume,
COUNT(*) AS jml_trx
FROM (SELECT site_id,
	grade_name_std,
	transaction_id,
	payment_type_id,DATETIME,
	completed_ts AS max_transaction_datetime,
	insert_date_mysql,
	payment_desc,
	bank_id,
	CASE WHEN bank_name LIKE 'MY%' AND bank_name LIKE '%PERTAMINA' THEN 'My Pertamina'
		WHEN bank_name LIKE 'LINK%' AND bank_name LIKE '%AJA'  THEN 'Link Aja'
	ELSE bank_name
	END AS bank_name,
	delivery_value,
	 delivery_volume,
	 keterangan
	FROM
	(SELECT 
	site_id,
	 grade_name_std,
	transaction_id,
	payment_type_id,DATETIME,
	completed_ts,
	insert_date_mysql,
	CASE
	WHEN payment_type_id IN (0,1) THEN "Cash"
	ELSE "Non Cash"
	END AS payment_desc,
	bank_id,
	CASE
	WHEN TRIM(bank_name)='' THEN 
		CASE
		WHEN LOWER(TRIM(payment_type_desc))='cash' THEN 'unknown'
		WHEN LOWER(TRIM(payment_type_desc))='none' THEN 'unknown'
		WHEN TRIM(payment_type_desc)='' THEN 'unknown'
		WHEN TRIM(payment_type_desc)IS NULL THEN 'unknown'
		ELSE payment_type_desc
		END
	WHEN TRIM(bank_name)IS NULL THEN
		CASE
		WHEN LOWER(TRIM(payment_type_desc))='cash' THEN 'unknown'
		WHEN LOWER(TRIM(payment_type_desc))='none' THEN 'unknown'
		WHEN TRIM(payment_type_desc)='' THEN 'unknown'
		WHEN TRIM(payment_type_desc)IS NULL THEN 'unknown'
		ELSE payment_type_desc
		END
	WHEN LOWER(TRIM(bank_name))='none' THEN
		CASE
		WHEN LOWER(TRIM(payment_type_desc))='cash' THEN 'unknown'
		WHEN LOWER(TRIM(payment_type_desc))='none' THEN 'unknown'
		WHEN TRIM(payment_type_desc)='' THEN 'unknown'
		WHEN TRIM(payment_type_desc)IS NULL THEN 'unknown'
		ELSE payment_type_desc
		END
	WHEN LOWER(TRIM(bank_name))='isibensin' THEN
		CASE
		WHEN LOWER(TRIM(payment_type_desc))='cash' THEN 'unknown'
		WHEN LOWER(TRIM(payment_type_desc))='none' THEN 'unknown'
		WHEN TRIM(payment_type_desc)='' THEN 'unknown'
		WHEN TRIM(payment_type_desc)IS NULL THEN 'unknown'
		ELSE payment_type_desc
		END
	ELSE bank_name
	END AS bank_name,
	delivery_value,
	 delivery_volume,
	 keterangan
	FROM
	(SELECT 
	COALESCE(site_id,'') AS site_id,
	COALESCE(delivery_id,0) AS delivery_id,
	COALESCE(grade_name_std,'') AS grade_name_std,
	COALESCE(transaction_id,0) AS transaction_id,
	COALESCE(date_completed_ts,'0000-00-00') AS DATETIME,
	completed_ts,
	insert_date_mysql_trx as insert_date_mysql,
	COALESCE(payment_type_id,0) AS payment_type_id,
	COALESCE(bank_id,0) AS bank_id,
	COALESCE(bank_name,'') AS bank_name,
	COALESCE(payment_type_desc,'') AS payment_type_desc,
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
        WHEN DATEDIFF(insert_date_mysql_trx, completed_ts) > 40 THEN 'Late Date'
        END AS KETERANGAN
	FROM datalake.master_spbu_transaksi_payment WHERE date_completed_ts = '"""+p1+"""-"""+p2+"""-"""+p3+"""' AND grade_name_std NOT IN ('PERTAMAX_RACING','PERTAMAX_PLUS','SOLAR_INDUSTRI', 'BIO_SOLAR_INDUSTRI')) AS e 
	 ) AS f ) AS g
	WHERE keterangan IS NULL
	GROUP BY 
site_id,grade_name_std,DATETIME,payment_desc,bank_id,bank_name;



update staging.p_5_1_"""+p+"""_temp
set staging.p_5_1_"""+p+"""_temp.bank_name = '' 
where staging.p_5_1_"""+p+"""_temp.payment_desc='Cash';


rename table datamart_part.p_5_1_"""+p+""" to staging.p_5_1_"""+p+"""_old,
staging.p_5_1_"""+p+"""_temp to datamart_part.p_5_1_"""+p+""";


drop table if exists staging.p_5_1_"""+p+"""_old;


update master.pertamina_log_table
set time_create_table_end = now(), time_to_create = TIMEDIFF(now(),time_create_table_start)
where id = @last_id;

--------------------------------------------------------------------------------------------------
--                            dashboard 1 - map, donut(tipe pembayaran)                         --
--------------------------------------------------------------------------------------------------
insert into master.pertamina_log_table (table_name,time_create_table_start)
values ('datamart_part.p_1_1_map_"""+p+"""',now());

set @last_id = LAST_INSERT_ID();

drop table if exists staging.pertamina_dashboard_1_map_data_period_stg_a1_"""+p+""";

CREATE table staging.pertamina_dashboard_1_map_data_period_stg_a1_"""+p+"""
SELECT
site_id, datetime,
	sum(delivery_value) as total_revenue, 
	sum(delivery_volume) as volume_terjual,
	max(max_transaction_datetime) as max_transaction_datetime
	from datamart_part.p_5_1_"""+p+"""
	group by site_id,
	datetime
;

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

drop table if exists staging.pertamina_dashboard_1_map_data_period_stg_b_"""+p+""";

CREATE table staging.pertamina_dashboard_1_map_data_period_stg_b_"""+p+"""
SELECT
site_id,datetime,
sum(delivery_value) as total_revenue_cash
from datamart_part.p_5_1_"""+p+""" where payment_desc ='Cash'
group by site_id,
datetime
;

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

drop table if exists staging.pertamina_dashboard_1_map_data_period_stg_c_"""+p+""";

CREATE table staging.pertamina_dashboard_1_map_data_period_stg_c_"""+p+"""
SELECT
site_id, datetime,
sum(delivery_value) as total_revenue_non_cash
from datamart_part.p_5_1_"""+p+""" where payment_desc ='Non Cash' 
group by site_id,
datetime
;

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

drop table if exists staging.p_1_1_map_"""+p+"""_temp;

CREATE table staging.p_1_1_map_"""+p+"""_temp like datamart_part.p_1_1_map_"""+p+""";

replace into staging.p_1_1_map_"""+p+"""_temp
SELECT
coalesce(a.site_id,'') as site_id,
coalesce(a.datetime,'0000-00-00') as datetime,
a.max_transaction_datetime,
coalesce(a.total_revenue,0) as total_revenue,
coalesce(a.volume_terjual,0) as volume_terjual,
coalesce(e.total_revenue_cash,0) as total_revenue_cash,
case
when coalesce(e.total_revenue_cash,0)<>0 then
(round((e.total_revenue_cash/a.total_revenue)*100,2))
when coalesce(a.total_revenue,0)=0 then 0
else 0
end as percent_revenue_cash,
coalesce(f.total_revenue_non_cash,0) as total_revenue_non_cash,
case
when coalesce(f.total_revenue_non_cash,0)<>0 then
(round((f.total_revenue_non_cash/a.total_revenue)*100,2))
when coalesce(a.total_revenue,0)=0 then 0
else 0
end as percent_revenue_non_cash
FROM 
	(select * from staging.pertamina_dashboard_1_map_data_period_stg_a1_"""+p+""")as a
left JOIN
	(select * from staging.pertamina_dashboard_1_map_data_period_stg_b_"""+p+"""
	)as e 
	ON a.site_id = e.site_id and a.datetime = e.datetime
left JOIN
	(select * from staging.pertamina_dashboard_1_map_data_period_stg_c_"""+p+"""
	)as f 
	ON a.site_id = f.site_id and a.datetime = f.datetime
;


rename table datamart_part.p_1_1_map_"""+p+""" to staging.p_1_1_map_"""+p+"""_old,
staging.p_1_1_map_"""+p+"""_temp to datamart_part.p_1_1_map_"""+p+""";

drop table if exists staging.p_1_1_map_"""+p+"""_old;
drop table if exists staging.pertamina_dashboard_1_map_data_period_stg_a1_"""+p+""";
drop table if exists staging.pertamina_dashboard_1_map_data_period_stg_b_"""+p+""";
drop table if exists staging.pertamina_dashboard_1_map_data_period_stg_c_"""+p+""";


update master.pertamina_log_table
set time_create_table_end = now(), time_to_create = TIMEDIFF(now(),time_create_table_start)
where id = @last_id;



--------------------------------------------------------------------------------------------------
--                    dashboard 9_1 - Summary Jumlah Transaksi SPBU                   --
--------------------------------------------------------------------------------------------------
insert into master.pertamina_log_table (table_name,time_create_table_start)
values ('datamart_part.p_9_1_"""+p+"""',now());


drop table if exists staging.p_9_1_"""+p+"""_temp;

CREATE table staging.p_9_1_"""+p+"""_temp like datamart_part.p_9_1_"""+p+""";

replace into staging.p_9_1_"""+p+"""_temp
SELECT 
site_id,  
DATETIME,
MAX(completed_ts) AS max_transaction_datetime,
grade_name_std AS produk,
delivery_type,
vehicle_type,
customer_type,
agency_type,
COUNT(DISTINCT(CASE WHEN TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '' THEN vehicle_number END)) AS jml_kendaraan_terdata,
COUNT(*) AS jml_trx,
COUNT(CASE WHEN TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '' THEN vehicle_number END) AS jml_trx_dg_no_kendaraan,
COUNT(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = ''  THEN vehicle_number END) AS jml_trx_tanpa_no_kendaraan,
COUNT(CASE WHEN odometer <> '' or agency_type <> '' THEN odometer END) AS jml_trx_dg_no_HP,
COUNT(CASE WHEN odometer = ''  and agency_type = ''  THEN odometer END) AS jml_trx_tanpa_no_HP,
SUM(delivery_value) AS revenue_total,
SUM(CASE WHEN TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '' THEN delivery_value ELSE 0 END) AS revenue_dg_nopol,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' THEN delivery_value ELSE 0 END) AS revenue_no_nopol,
SUM(delivery_volume) AS volume_penjualan_total,
SUM(CASE WHEN TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '' THEN delivery_volume ELSE 0 END) AS volume_dg_nopol,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' THEN delivery_volume ELSE 0 END) AS volume_no_nopol,
COUNT(DISTINCT(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 60 THEN vehicle_number END)) AS jml_kendaraan_terdata_60,
COUNT(CASE WHEN delivery_volume > 60 THEN vehicle_number END) AS jml_trx_60,
COUNT(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 60 THEN vehicle_number END) AS jml_trx_dg_no_kendaraan_60,
COUNT(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = ''  AND delivery_volume > 60 THEN vehicle_number END) AS jml_trx_tanpa_no_kendaraan_60,
COUNT(CASE WHEN (odometer <> '' or agency_type <> '') AND delivery_volume > 60 THEN odometer END) AS jml_trx_dg_no_HP_60,
COUNT(CASE WHEN odometer = ''  and agency_type = ''  AND delivery_volume > 60 THEN odometer END) AS jml_trx_tanpa_no_HP_60,
SUM(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 60 THEN delivery_value ELSE 0 END) AS revenue_dg_nopol_60,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' AND delivery_volume > 60 THEN delivery_value ELSE 0 END) AS revenue_no_nopol_60,
SUM(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 60 THEN delivery_volume ELSE 0 END) AS volume_dg_nopol_60,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' AND delivery_volume > 60 THEN delivery_volume ELSE 0 END) AS volume_no_nopol_60,
COUNT(DISTINCT(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 80 THEN vehicle_number END)) AS jml_kendaraan_terdata_80,
COUNT(CASE WHEN delivery_volume > 80 THEN vehicle_number END) AS jml_trx_80,
COUNT(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 80 THEN vehicle_number END) AS jml_trx_dg_no_kendaraan_80,
COUNT(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' AND delivery_volume > 80 THEN vehicle_number END) AS jml_trx_tanpa_no_kendaraan_80,
COUNT(CASE WHEN (odometer <> '' or agency_type <> '') AND delivery_volume > 80 THEN odometer END) AS jml_trx_dg_no_HP_80,
COUNT(CASE WHEN odometer = ''  and agency_type = ''  AND delivery_volume > 80 THEN odometer END) AS jml_trx_tanpa_no_HP_80,
SUM(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 80 THEN delivery_value ELSE 0 END) AS revenue_dg_nopol_80,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' AND delivery_volume > 80 THEN delivery_value ELSE 0 END) AS revenue_no_nopol_80,
SUM(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 80 THEN delivery_volume ELSE 0 END) AS volume_dg_nopol_80,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' AND delivery_volume > 80 THEN delivery_volume ELSE 0 END) AS volume_no_nopol_80,
COUNT(DISTINCT(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 200 THEN vehicle_number END)) AS jml_kendaraan_terdata_200,
COUNT(CASE WHEN delivery_volume > 200 THEN vehicle_number END) AS jml_trx_200,
COUNT(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 200 THEN vehicle_number END) AS jml_trx_dg_no_kendaraan_200,
COUNT(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = ''  AND delivery_volume > 200 THEN vehicle_number END) AS jml_trx_tanpa_no_kendaraan_200,
COUNT(CASE WHEN (odometer <> '' or agency_type <> '') AND delivery_volume > 200 THEN odometer END) AS jml_trx_dg_no_HP_200,
COUNT(CASE WHEN odometer = ''  and agency_type = ''  AND delivery_volume > 200 THEN odometer END) AS jml_trx_tanpa_no_HP_200,
SUM(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 200 THEN delivery_value ELSE 0 END) AS revenue_dg_nopol_200,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' AND delivery_volume > 200 THEN delivery_value ELSE 0 END) AS revenue_no_nopol_200,
SUM(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 200 THEN delivery_volume ELSE 0 END) AS volume_dg_nopol_200,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' AND delivery_volume > 200 THEN delivery_volume ELSE 0 END) AS volume_no_nopol_200,
COUNT(DISTINCT(CASE WHEN TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '' AND delivery_volume > 1000 THEN vehicle_number END)) AS jml_kendaraan_terdata_1000,
COUNT(CASE WHEN delivery_volume > 1000 THEN vehicle_number END) AS jml_trx_1000,
COUNT(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 1000 THEN vehicle_number END) AS jml_trx_dg_no_kendaraan_1000,
COUNT(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = ''  AND delivery_volume > 1000 THEN vehicle_number END) AS jml_trx_tanpa_no_kendaraan_1000,
COUNT(CASE WHEN (odometer <> '' or agency_type <> '') AND delivery_volume > 1000 THEN odometer END) AS jml_trx_dg_no_HP_1000,
COUNT(CASE WHEN odometer = ''  and agency_type = ''  AND delivery_volume > 1000 THEN odometer END) AS jml_trx_tanpa_no_HP_1000,
SUM(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 1000 THEN delivery_value ELSE 0 END) AS revenue_dg_nopol_1000,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' AND delivery_volume > 1000 THEN delivery_value ELSE 0 END) AS revenue_no_nopol_1000,
SUM(CASE WHEN (TRIM(vehicle_number) <> '' or TRIM(agency_name) <> '') AND delivery_volume > 1000 THEN delivery_volume ELSE 0 END) AS volume_dg_nopol_1000,
SUM(CASE WHEN TRIM(vehicle_number) = '' and TRIM(agency_name) = '' AND delivery_volume > 1000 THEN delivery_volume ELSE 0 END) AS volume_no_nopol_1000
FROM
(SELECT 
	COALESCE(site_id,'') AS site_id,  
	COALESCE(delivery_id,0) AS delivery_id,
	COALESCE(date_completed_ts, '0000-00-00') AS DATETIME,	
	completed_ts,
	COALESCE(grade_name_std, '') AS grade_name_std,
	COALESCE(vehicle_number, '') AS vehicle_number,
	COALESCE(odometer, '') AS odometer,
	COALESCE(delivery_value, 0) AS delivery_value,
	COALESCE(delivery_volume,0) AS delivery_volume,
	COALESCE(delivery_type,0) AS delivery_type,
	COALESCE(del_sell_price,0) AS del_sell_price,
	COALESCE(vehicle_type,'') AS vehicle_type,
	COALESCE(customer_type,'') AS customer_type,
	COALESCE(agency_type,'') AS agency_type,
	COALESCE(agency_name,'') AS agency_name,
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
        END AS KETERANGAN
	FROM datalake.`master_spbu_transaksi_payment` WHERE date_completed_ts = '"""+p1+"""-"""+p2+"""-"""+p3+"""' AND grade_name_std NOT IN ('PERTAMAX_RACING','PERTAMAX_PLUS','SOLAR_INDUSTRI')) AS e
WHERE keterangan IS NULL
GROUP BY site_id,grade_name_std,delivery_type,customer_type,vehicle_type,agency_type,DATETIME
;

rename table datamart_part.p_9_1_"""+p+""" to staging.p_9_1_"""+p+"""_old,
staging.p_9_1_"""+p+"""_temp to datamart_part.p_9_1_"""+p+""";


drop table if exists staging.p_9_1_"""+p+"""_old;

update master.pertamina_log_table
set time_create_table_end = now()
ORDER BY id DESC LIMIT 1;

update master.pertamina_log_table
set time_to_create = TIMEDIFF(time_create_table_end,time_create_table_start)
ORDER BY id DESC LIMIT 1;



--------------------------------------------------------------------------------------------------
--                                            pertamina_dashboard_notification                                      --
--------------------------------------------------------------------------------------------------

insert into master.pertamina_log_table (table_name,time_create_table_start)
values ('datamart_part.p_6_1_notif_"""+p+"""',now());

set @last_id = LAST_INSERT_ID();


drop table if exists staging.p_6_1_notif_"""+p+"""_temp;

CREATE table staging.p_6_1_notif_"""+p+"""_temp like datamart_part.p_6_1_notif_"""+p+""";


replace into staging.p_6_1_notif_"""+p+"""_temp
SELECT delivery_id,
site_id,
DATETIME,
jam,
grade_name_std,
hose_id,
hose_number,
pump_id,
pump_name,
delivery_type,
delivery_volume,
delivery_value,
del_sell_price,
vehicle_number,
odometer,
vehicle_type,
customer_type,
phone_number,
attendant_name,
hose_meter_value,
start_totalizer_value,
end_totalizer_value,
hose_meter_volume,
start_totalizer_volume,
end_totalizer_volume,
insert_date_mysql_trx
FROM
	(SELECT 
	delivery_id,
	site_id,
	date_completed_ts AS DATETIME,
	time_completed_ts AS jam,
	completed_ts,
	grade_name_std,
	hose_id,
	hose_number,
	pump_id,
	pump_name,
	delivery_type,
	delivery_volume,
	delivery_value,
	del_sell_price,
	vehicle_number,
	odometer,
	attendant_name,
	hose_meter_value,
	start_totalizer_value,
	end_totalizer_value,
	hose_meter_volume,
	start_totalizer_volume,
	end_totalizer_volume,
	insert_date_mysql_trx,
	COALESCE(vehicle_type,'') AS vehicle_type,
	COALESCE(customer_type,'') AS customer_type,
	COALESCE(phone_number,'') AS phone_number,
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
	WHEN DATEDIFF(insert_date_mysql_trx, completed_ts) > 40 THEN 'Late Date'
	END AS KETERANGAN
	FROM datalake.master_spbu_transaksi_payment WHERE date_completed_ts = '"""+p1+"""-"""+p2+"""-"""+p3+"""-' AND grade_name_std NOT IN ('PERTAMAX_RACING','PERTAMAX_PLUS','SOLAR_INDUSTRI') AND delivery_volume> 200) AS e
WHERE KETERANGAN IS NULL;


rename table datamart_part.p_6_1_notif_"""+p+""" to staging.p_6_1_notif_"""+p+"""_old,
staging.p_6_1_notif_"""+p+"""_temp to datamart_part.p_6_1_notif_"""+p+""";


drop table if exists staging.p_6_1_notif_"""+p+"""_old;


update master.pertamina_log_table
set time_create_table_end = now(), time_to_create = TIMEDIFF(now(),time_create_table_start)
where id = @last_id;


--------------------------------------------------------------------------------------------------
--                              pertamina_dashboard_map_bph                                      --
--------------------------------------------------------------------------------------------------

insert into master.pertamina_log_table (table_name,time_create_table_start)
values ('datamart_part.p_1_2_map_bph_"""+p+"""',now());

set @last_id = LAST_INSERT_ID();


drop table if exists staging.p_1_2_map_bph_"""+p+"""_temp;

CREATE table staging.p_1_2_map_bph_"""+p+"""_temp like datamart_part.p_1_2_map_bph_"""+p+""";

REPLACE INTO staging.p_1_2_map_bph_"""+p+"""_temp
SELECT b.site_id,
COALESCE(grade_name_std,'') AS grade_name_std,
address,
longitude,
latitude,
CASE WHEN DATETIME IS NULL THEN '"""+p1+"""-"""+p2+"""-"""+p3+"""'
ELSE DATETIME END AS DATETIME,
max_transaction_datetime,
jml_trx,
jml_trx_dg_nopol,
jml_trx_no_nopol,
jml_trx_anomali,
vol_trx,
vol_trx_dg_nopol,
vol_trx_no_nopol,
vol_trx_anomali,
revenue,
revenue_dg_nopol,
revenue_no_nopol,
revenue_anomali,
CASE WHEN jml_trx_anomali <> 0 THEN 'Anomali'
WHEN max_transaction_datetime IS NOT NULL THEN 'Beroperasi'
ELSE 'Offline' END AS STATUS,
status_spbu,
NOW() AS datetime_created
 FROM
 (SELECT `code_spbu` AS site_id, 
	`address`,
	`longitude`,
	`latitude`,
	CASE WHEN uat = '0' THEN 'Inactive'
	WHEN uat = '1' THEN 'BAST'
	WHEN uat = '2' THEN 'Partial Integrasi'
	WHEN uat = '3' THEN 'Full Integrasi'
	END AS status_spbu
	FROM master.`pertamina_master_spbu`  ) AS b
LEFT JOIN
	(SELECT a1.site_id,
	a1.grade_name_std,
	a1.datetime,
	a1.`max_transaction_datetime`,
	COALESCE(vol_trx,0) - COALESCE(vol_trx_anomali,0) AS vol_trx,
	coalesce(volume_dg_nopol,0) as vol_trx_dg_nopol,
	COALESCE(`volume_no_nopol`,0) AS `vol_trx_no_nopol`,
	COALESCE(vol_trx_anomali,0) AS vol_trx_anomali,
	COALESCE(jml_trx,0) - COALESCE(jml_trx_anomali,0) AS jml_trx,
	COALESCE(`jml_trx_dg_no_kendaraan`,0) AS `jml_trx_dg_nopol`,
	COALESCE(`jml_trx_tanpa_no_kendaraan`,0) AS `jml_trx_no_nopol`,
	COALESCE(jml_trx_anomali,0) AS jml_trx_anomali,
	COALESCE(revenue,0) - COALESCE(revenue_anomali,0) AS revenue,
	COALESCE(`revenue_dg_nopol`,0) AS `revenue_dg_nopol`,
	COALESCE(`revenue_no_nopol`,0) AS `revenue_no_nopol`,
	COALESCE(revenue_anomali,0) AS revenue_anomali
	FROM
	(SELECT site_id, produk as grade_name_std,
	`datetime`,
	max(`max_transaction_datetime`) as `max_transaction_datetime`,
	sum(`volume_penjualan`) as vol_trx,
	sum(`volume_dg_nopol`) as volume_dg_nopol,
	sum(`volume_no_nopol`) as `volume_no_nopol`,
	sum(jml_trx) as jml_trx,
	sum(`jml_trx_dg_no_kendaraan`) as `jml_trx_dg_no_kendaraan`,
	sum(`jml_trx_tanpa_no_kendaraan`) as `jml_trx_tanpa_no_kendaraan`,
	sum(revenue) as revenue,
	sum(`revenue_dg_nopol`) as `revenue_dg_nopol`,
	sum(`revenue_no_nopol`) as `revenue_no_nopol`
	FROM datamart_part.p_9_1_"""+p+"""
        group by site_id, produk) AS a1
	LEFT JOIN
	(SELECT `site_id`,grade_name_std,
	`datetime`,
	SUM(`delivery_volume`) AS vol_trx_anomali,
	COUNT(*) AS jml_trx_anomali,
	SUM(`delivery_value`) AS revenue_anomali
	FROM datamart_part.p_6_1_notif_"""+p+"""
	GROUP BY site_id,grade_name_std,DATETIME) AS b1
	ON a1.site_id = b1.site_id
	AND a1.grade_name_std = b1.grade_name_std) AS a
	ON a.site_id = b.site_id
	;
 
rename table datamart_part.p_1_2_map_bph_"""+p+""" to staging.p_1_2_map_bph_"""+p+"""_old,
staging.p_1_2_map_bph_"""+p+"""_temp to datamart_part.p_1_2_map_bph_"""+p+""";


drop table if exists staging.p_1_2_map_bph_"""+p+"""_old;


update master.pertamina_log_table
set time_create_table_end = now(), time_to_create = TIMEDIFF(now(),time_create_table_start)
where id = @last_id;




"""),
text_file.write("%s" % y)


text_file.close()

#print(y)
