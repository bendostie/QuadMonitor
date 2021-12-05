sudo mysql -u root -p
SHOW DATABASES;

CREATE USER 'SetupUser'@localhost IDENTIFIED BY 'Turtle2';
CREATE USER 'WebUser' IDENTIFIED BY 'Turtle2';
CREATE USER 'ServerUser'@localhost IDENTIFIED BY 'Turtle2';
SELECT User FROM mysql.user;
GRANT ALL PRIVILEGES ON *.* TO 'SetupUser'@localhost IDENTIFIED BY 'Turtle2';
GRANT SELECT ON QuadMonitor.readings TO 'WebUser';
GRANT INSERT ON QuadMonitor.readings TO 'ServerUser'@localhost;
FLUSH PRIVILEGES;