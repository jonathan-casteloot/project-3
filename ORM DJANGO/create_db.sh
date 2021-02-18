#!/bin/bash

sudo mysql -uroot <<MYSQL_SCRIPT
CREATE DATABASE fao;
CREATE USER 'django_admin'@'localhost' IDENTIFIED BY 'Tkf821!jc';
GRANT ALL PRIVILEGES ON fao.* TO 'django_admin'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT
