docker exec prestashop-db mysqldump --password=prestashop prestashop > drop.sql
tar --exclude='../Prestashop/mysql' --exclude='../Prestashop/var' --exclude='../Prestashop/vendor' -zcvf backup.tgz ../Prestashop ../drop.sql
rm drop.sql