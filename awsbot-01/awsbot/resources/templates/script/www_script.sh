#!/bin/bash
yum update -y
yum install httpd -y
service httpd start
chkconfig httpd on
cd /var/www/html
echo "<html><h1>%s : If you see This. Apache Httpd is Up and Running!</h1></html>" > index.html
