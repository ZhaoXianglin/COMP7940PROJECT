-- phpMyAdmin SQL Dump
-- version 4.9.3
-- https://www.phpmyadmin.net/
--
-- 主机： localhost:8889
-- 生成日期： 2021-04-21 14:22:08
-- 服务器版本： 5.7.26
-- PHP 版本： 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `comp7940`
--
CREATE DATABASE IF NOT EXISTS `comp7940` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `comp7940`;

-- --------------------------------------------------------

--
-- 表的结构 `sport_rec`
--

CREATE TABLE `sport_rec` (
  `id` int(11) NOT NULL,
  `userid` varchar(32) NOT NULL,
  `username` varchar(128) NOT NULL,
  `jing` double NOT NULL,
  `wei` double NOT NULL,
  `rectime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户打卡记录';

--
-- 转储表的索引
--

--
-- 表的索引 `sport_rec`
--
ALTER TABLE `sport_rec`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `sport_rec`
--
ALTER TABLE `sport_rec`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
