-- 创建数据库
CREATE DATABASE IF NOT EXISTS db_douban DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_douban;

-- 创建用户表
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入默认管理员账号
INSERT INTO `user` (`username`, `password`) VALUES ('admin', '123');

-- 创建电影数据表
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` varchar(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `rating` float DEFAULT NULL,
  `year` varchar(10) DEFAULT NULL,
  `intro` text,
  `tags` varchar(200) DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `movie_id` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;