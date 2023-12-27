#!/bin/bash
. ~/etc/db
. ~/etc/job

export SQL=query_part_today_1.sql
export LOG=~/log/$(basename ${SQL} .sql).log
touch ${LOG}

cd ${WORKDIR}
echo $(date) $SQL starting >> ${LOG}

flock -xn "${SQL}" -c "mysql -A -h 10.1.3.23 -u engineer -p'XXXXXX' staging < ~/query_part_today_1.sql >> ${LOG} 2>&1"

echo $(date) $SQL end >> ${LOG}

#!/bin/bash
. ~/etc/db
. ~/etc/job

export SQL=move_query_part_today_1.sql
export LOG=~/log/$(basename ${SQL} .sql).log
touch ${LOG}

cd ${WORKDIR}
echo $(date) $SQL starting >> ${LOG}

flock -xn "${SQL}" -c "mysql -A -h 10.1.3.25 -u engineer -p'XXXXXX' staging < ~/move_query_part_today_1.sql >> ${LOG} 2>&1"

echo $(date) $SQL end >> ${LOG}
