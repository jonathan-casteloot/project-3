#!/bin/bash

sudo mysql -uroot <<MYSQL_SCRIPT
DROP DATABASE fao;
DROP USER 'django_admin'@'localhost';
MYSQL_SCRIPT
