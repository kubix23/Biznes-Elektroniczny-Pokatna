tar zxvf backup.tgz
mv drop.sql Prestashop/mysql
docker exec prestashop-db mysql -uroot -pprestashop -e "create database prestashop"
docker exec -i prestashop-db bash -c "mysql --password=prestashop prestashop < /var/lib/mysql/drop.sql"
