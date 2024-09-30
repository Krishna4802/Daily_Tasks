    docker run -dit -p 3306:3306 --name sql_server ubuntu

    apt update
    apt install default-jre -y
    apt install sudo -y
    sudo apt install mysql-server
    sudo service mysql start
    sudo service mysql status
    sudo apt install postgresql postgresql-contrib -y
    sudo service postgresql start

    
    sudo mysql
    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'fructidor';
    mysql -u root -p
    
    
    ALTER USER 'pgloader_my'@'localhost' IDENTIFIED WITH mysql_native_password BY 'test';
    
    
    docker run -dit -p 3306:3306 -p 5432:5432 --name pg_loader ubuntu
    
    
    CREATE DATABASE SampleDB;
    GO
    
    USE SampleDB;
    GO
    
    CREATE TABLE Employees (
        ID INT PRIMARY KEY,
        Name NVARCHAR(50),
        Position NVARCHAR(50)
    );
    
    INSERT INTO Employees (ID, Name, Position) VALUES
    (1, 'Alice', 'Developer'),
    (2, 'Bob', 'Manager'),
    (3, 'Charlie', 'Analyst');
    GO
    
    
    
    ALTER USER 'migration_user'@'localhost' IDENTIFIED WITH mysql_native_password BY '123';
    
    
    pgloader mysql://migration_user:migration_password@localhost/sample_mysql_db?useSSL=false postgresql://pgloader_pg:123@localhost/new_db
    
    
    
     sudo apt install software-properties-common
     sudo add-apt-repository ppa:dimitri/pgloader
     sudo apt update
     sudo apt install pgloader
     pgloader --version
    
    
    
    apt update
    apt install default-jre -y
    apt-get install wget -y
    apt install vim -y
    apt install sudo -y
    apt install curl -y
    sudo apt update
    sudo apt install sbcl unzip libsqlite3-dev gawk curl make freetds-dev libzip-dev -y
    curl -fsSLO https://github.com/dimitri/pgloader/archive/v3.6.2.tar.gz
    tar xvf v3.6.2.tar.gz
    cd pgloader-3.6.2/
    make pgloader
    sudo mv ./build/bin/pgloader /usr/local/bin/
    pgloader --version
    
    
    
    sudo -u postgres createuser --interactive -P
    
    sudo -u postgres createdb new_db
    
    
    vi /etc/mysql/my.cnf
    sudo service mysql restart
    
    [mysqld]
    default-authentication-plugin=mysql_native_password
    
    
    CREATE USER 'migration_user'@'localhost' IDENTIFIED BY 'migration_password';
    GRANT ALL PRIVILEGES ON sample_mysql_db.* TO 'migration_user'@'localhost';
    FLUSH PRIVILEGES;
    
     
    pgloader --with "batch rows = 1000" mysql://root:123@127.0.0.1:3306/sample_mysql_db postgresql://pgloader_pg:123@localhost:5432/mig_test
    
    pgloader mysql://root:123@127.0.0.1:3306/sample_mysql_db postgresql://pgloader_pg:123@localhost:5432/mig_test  --with "batch rows = 1000"
