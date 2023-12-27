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
				(SELECT * FROM datamart_part.p_1_6_stg2_20231211
				WHERE deleted = 0)AS a 
			LEFT JOIN
				(SELECT site_id,`grade_name_std`,SUM(`jam_penjualan`) AS jam_penjualan,
				SUM(`total_penjualan`) AS total_penjualan FROM datamart.`pertamina_dashboard_1_6_stg1`
				WHERE DATETIME BETWEEN '2023-12-04' AND '2023-12-10'
				GROUP BY site_id, grade_name_std)AS b
				ON a.site_id=b.site_id
				AND a.grade_name_std=b.grade_name_std
			LEFT JOIN
				(SELECT * FROM datamart_part.p_1_6_stg1_20231204) AS h
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
				WHERE DATETIME BETWEEN '2023-12-04' AND '2023-12-10') AS t
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
				FROM datamart_part.p_8_1_atg_pump_20231204) AS o
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
				FROM datamart_part.p_8_1_atg_pump_20231210) AS s
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
				WHERE `date_record_entry_ts` BETWEEN '2023-11-10' AND '2023-12-11') AS t ) AS t1
				GROUP BY site_id,grade_name_std,tank_id,tank_name) AS t
				ON a.site_id = t.site_id
				AND a.grade_name_std = t.grade_name_std
				AND a.tank_id = t.tank_id
				AND a.tank_name = t.tank_name
				LEFT JOIN 
				(SELECT * FROM datamart_part.p_1_6_stg2_20231210 WHERE deleted = 0)AS u 
				ON a.site_id = u.site_id
				AND a.grade_name_std = u.grade_name_std
				AND a.datetime - INTERVAL 1 DAY=u.datetime
				AND a.tank_id = u.tank_id
				AND a.tank_name = u.tank_name
			LEFT JOIN 
				(SELECT * FROM datamart_part.p_1_6_stg2_20231209 WHERE deleted = 0)AS v 
				ON a.site_id = v.site_id
				AND a.grade_name_std = v.grade_name_std
				AND a.datetime - INTERVAL 2 DAY=v.datetime
				AND a.tank_id = v.tank_id
				AND a.tank_name = v.tank_name
			LEFT JOIN 
				(SELECT * FROM datamart_part.p_1_6_stg2_20231208 WHERE deleted = 0)AS w 
				ON a.site_id = w.site_id
				AND a.grade_name_std = w.grade_name_std
				AND a.datetime - INTERVAL 3 DAY=w.datetime
				AND a.tank_id = w.tank_id
				AND a.tank_name = w.tank_name
			LEFT JOIN
				(SELECT t2.site_id, t2.grade_name_std,t2.jml_tanki,t1.lo_qty/COALESCE(t2.jml_tanki,1) AS total_penjualan FROM
				(SELECT site_id, grade_name_std, COUNT(*) AS jml_tanki
				FROM datamart_part.p_1_6_stg2_20231211 
				GROUP BY site_id, grade_name_std) AS t2
				LEFT JOIN
				(SELECT spbu_number, lo_produk_std, SUM(lo_qty)*1000 AS lo_qty FROM datamart.`pertamina_dashboard_10_3_shipment`
				WHERE date_gateout_time BETWEEN '2023-12-04' AND '2023-12-10'
				GROUP BY spbu_number,lo_produk_std ) AS t1
				ON t1.spbu_number = t2.site_id
				AND t1.lo_produk_std = t2.grade_name_std) AS z
				ON a.site_id = z.site_id
				AND a.grade_name_std = z.grade_name_std
			LEFT JOIN
				(SELECT t2.site_id, t2.grade_name_std,t2.jml_tanki,t1.lo_qty/COALESCE(t2.jml_tanki,1) AS total_penjualan FROM
				(SELECT site_id, grade_name_std, COUNT(*) AS jml_tanki
				FROM datamart_part.p_1_6_stg2_20231211 
				GROUP BY site_id, grade_name_std) AS t2
				LEFT JOIN
				(SELECT `site_id`, `grade_name_std`, SUM(quantity) AS lo_qty FROM datamart.`pertamina_dashboard_10_4_sap_lo`
				WHERE `DATETIME` BETWEEN '2023-12-04' AND '2023-12-10'
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