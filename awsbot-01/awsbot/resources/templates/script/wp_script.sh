#!/bin/bash  
sudo su  
yum update -y  
yum install httpd php php-mysql -y  
cd /var/www/html  
echo "healthy" > healthy.html  
wget https://wordpress.org/latest.tar.gz  
tar -xzf latest.tar.gz  
cp -r wordpress/* /var/www/html/  
rm -rf wordpress  
rm -rf latest.tar.gz  
chmod -R 755 wp-content  
chown -R apache:apache wp-content  
wget https://s3.amazonaws.com/bucketforwordpresslab-donotdelete/htaccess.txt  
mv htaccess.txt .htaccess
amazon-linux-extras install php7.2 -y
service httpd start  
chkconfig httpd on
