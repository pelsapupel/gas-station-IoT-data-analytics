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
	FROM datalake.master_spbu_transaksi_payment WHERE date_completed_ts = '2023-02-14' AND grade_name_std NOT IN ('PERTAMAX_RACING','PERTAMAX_PLUS','SOLAR_INDUSTRI', 'BIO_SOLAR_INDUSTRI')) AS e 
	 ) AS f ) AS g
	WHERE keterangan IS NULL
	GROUP BY 
site_id,grade_name_std,DATETIME,payment_desc,bank_id,bank_name;