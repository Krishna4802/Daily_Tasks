    apt update
    apt install default-jre -y
    apt install sudo -y
    sudo apt install mysql-server
    sudo service mysql start
    sudo service mysql status
    
    sudo mysql
    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'fructidor';
    mysql -u root -p
