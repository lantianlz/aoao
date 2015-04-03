-- MySQL dump 10.10
--
-- Host: localhost    Database: account_aoaoxc
-- ------------------------------------------------------
-- Server version	5.0.20a-nt

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_activeday`
--

DROP TABLE IF EXISTS `account_activeday`;
CREATE TABLE `account_activeday` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` varchar(32) NOT NULL,
  `active_day` date NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id_2` (`user_id`,`active_day`),
  KEY `account_activeday_4c5200c4` (`active_day`),
  KEY `user_id` USING BTREE (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_activeday`
--


/*!40000 ALTER TABLE `account_activeday` DISABLE KEYS */;
LOCK TABLES `account_activeday` WRITE;
INSERT INTO `account_activeday` VALUES (6,'7da29b4fac2a11e48af5fc6ed31ca809','2015-02-04'),(1,'8912414fa06a11e49380ebdad3994e31','2015-01-20'),(2,'8912414fa06a11e49380ebdad3994e31','2015-01-26'),(3,'8912414fa06a11e49380ebdad3994e31','2015-01-27'),(4,'8912414fa06a11e49380ebdad3994e31','2015-01-28'),(5,'8912414fa06a11e49380ebdad3994e31','2015-02-04'),(7,'8912414fa06a11e49380ebdad3994e31','2015-02-12'),(8,'8912414fa06a11e49380ebdad3994e31','2015-03-26');
UNLOCK TABLES;
/*!40000 ALTER TABLE `account_activeday` ENABLE KEYS */;

--
-- Table structure for table `account_blacklist`
--

DROP TABLE IF EXISTS `account_blacklist`;
CREATE TABLE `account_blacklist` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` varchar(32) NOT NULL,
  `type` int(11) NOT NULL,
  `state` tinyint(1) NOT NULL,
  `expire_time` datetime NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `account_blacklist_403f60f` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_blacklist`
--


/*!40000 ALTER TABLE `account_blacklist` DISABLE KEYS */;
LOCK TABLES `account_blacklist` WRITE;
UNLOCK TABLES;
/*!40000 ALTER TABLE `account_blacklist` ENABLE KEYS */;

--
-- Table structure for table `account_externaltoken`
--

DROP TABLE IF EXISTS `account_externaltoken`;
CREATE TABLE `account_externaltoken` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` varchar(32) NOT NULL,
  `source` varchar(16) NOT NULL,
  `access_token` varchar(255) NOT NULL,
  `refresh_token` varchar(255) default NULL,
  `external_user_id` varchar(128) NOT NULL,
  `union_id` varchar(128) default NULL,
  `app_id` varchar(128) default NULL,
  `nick` varchar(64) default NULL,
  `user_url` varchar(128) default NULL,
  `expire_time` datetime NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `state` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `source` (`source`,`access_token`),
  UNIQUE KEY `source_2` (`source`,`external_user_id`),
  KEY `account_externaltoken_403f60f` (`user_id`),
  KEY `account_externaltoken_48ee9dea` (`source`),
  KEY `account_externaltoken_19b8add5` (`access_token`),
  KEY `account_externaltoken_22b264ec` (`external_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_externaltoken`
--


/*!40000 ALTER TABLE `account_externaltoken` DISABLE KEYS */;
LOCK TABLES `account_externaltoken` WRITE;
INSERT INTO `account_externaltoken` VALUES (1,'8912414fa06a11e49380ebdad3994e31','weixin','OezXcEiiBSKSxW0eoylIeHkwic8NI9z9FqxetdW7pXA8CDrfLdpMWE4nLba6h-juGwt7E3Y4S70SA4QvCW3_B9EAgbPGa394nbdlG_uhCjXxX4hBVrN1BK7Bt7haEKfZt6596goYMZrzAitxJhbjWg',NULL,'oZy3hskE524Y2QbLgY2h3VnI3Im8',NULL,'wx0d227d4f9b19658a','简单的快乐','','2015-02-12 13:17:47','2015-01-20 14:06:55','2015-02-12 11:17:47',1);
UNLOCK TABLES;
/*!40000 ALTER TABLE `account_externaltoken` ENABLE KEYS */;

--
-- Table structure for table `account_lastactive`
--

DROP TABLE IF EXISTS `account_lastactive`;
CREATE TABLE `account_lastactive` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` varchar(32) NOT NULL,
  `ip` varchar(32) default NULL,
  `last_active_time` datetime NOT NULL,
  `last_active_source` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `account_lastactive_51c21344` (`last_active_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_lastactive`
--


/*!40000 ALTER TABLE `account_lastactive` DISABLE KEYS */;
LOCK TABLES `account_lastactive` WRITE;
INSERT INTO `account_lastactive` VALUES (1,'8912414fa06a11e49380ebdad3994e31','192.168.99.106','2015-03-26 15:45:31',0),(2,'7da29b4fac2a11e48af5fc6ed31ca809','192.168.99.106','2015-02-04 12:59:59',0);
UNLOCK TABLES;
/*!40000 ALTER TABLE `account_lastactive` ENABLE KEYS */;

--
-- Table structure for table `account_profile`
--

DROP TABLE IF EXISTS `account_profile`;
CREATE TABLE `account_profile` (
  `auto_id` int(11) NOT NULL auto_increment,
  `id` varchar(32) NOT NULL,
  `nick` varchar(32) NOT NULL,
  `domain` varchar(32) default NULL,
  `birthday` date NOT NULL,
  `gender` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `avatar` varchar(256) NOT NULL,
  `email_verified` tinyint(1) NOT NULL,
  `mobile_verified` tinyint(1) NOT NULL,
  `ip` varchar(32) default NULL,
  `des` varchar(256) default NULL,
  `source` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY  (`auto_id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `nick` (`nick`),
  UNIQUE KEY `domain` (`domain`),
  KEY `account_profile_58c1bcbc` (`birthday`),
  KEY `account_profile_35c2d6e` (`gender`),
  KEY `account_profile_586a73b5` (`city_id`),
  KEY `account_profile_1b05a784` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_profile`
--


/*!40000 ALTER TABLE `account_profile` DISABLE KEYS */;
LOCK TABLES `account_profile` WRITE;
INSERT INTO `account_profile` VALUES (1,'8912414fa06a11e49380ebdad3994e31','简单的快乐',NULL,'2000-01-01',1,0,'http://img0.aoaoxc.com/weixin_avatar_95719bb0a60711e4a790915fd475f278',0,0,'192.168.1.2',NULL,1,'2015-01-20 14:06:55'),(2,'7da29b4fac2a11e48af5fc6ed31ca809','精典汽车管理员',NULL,'2000-01-01',0,0,'',0,0,'192.168.99.106',NULL,0,'2015-02-04 12:58:42'),(3,'cc659c9eac2b11e49076fc6ed31ca809','aaa',NULL,'2000-01-01',0,0,'',0,0,'192.168.99.106',NULL,0,'2015-02-04 13:08:04');
UNLOCK TABLES;
/*!40000 ALTER TABLE `account_profile` ENABLE KEYS */;

--
-- Table structure for table `account_user`
--

DROP TABLE IF EXISTS `account_user`;
CREATE TABLE `account_user` (
  `auto_id` int(11) NOT NULL auto_increment,
  `id` varchar(32) NOT NULL,
  `email` varchar(64) NOT NULL,
  `mobilenumber` varchar(32) default NULL,
  `username` varchar(32) default NULL,
  `password` varchar(128) NOT NULL,
  `state` int(11) NOT NULL,
  `last_login` datetime NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY  (`auto_id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobilenumber` (`mobilenumber`),
  UNIQUE KEY `username` (`username`),
  KEY `account_user_355bfc27` (`state`),
  KEY `account_user_356323a1` (`last_login`),
  KEY `account_user_1b05a784` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_user`
--


/*!40000 ALTER TABLE `account_user` DISABLE KEYS */;
LOCK TABLES `account_user` WRITE;
INSERT INTO `account_user` VALUES (1,'8912414fa06a11e49380ebdad3994e31','weixin_1421734015432@mraoaoxc.com',NULL,NULL,'f82e41fcf30c759f7f161e9ee9d38d9f',1,'2015-03-26 14:44:55','2015-01-20 14:06:55'),(2,'7da29b4fac2a11e48af5fc6ed31ca809','jd001@aoaoxc.com',NULL,NULL,'5e2b7e7a8bb7e5a0a4586ac15fc220ef',1,'2015-02-04 12:59:59','2015-02-04 12:58:42'),(3,'cc659c9eac2b11e49076fc6ed31ca809','test@a.com',NULL,NULL,'87541c0616a4abc5a0f7d1555f3b9ad4',1,'2015-02-04 13:08:04','2015-02-04 13:08:04');
UNLOCK TABLES;
/*!40000 ALTER TABLE `account_user` ENABLE KEYS */;

--
-- Table structure for table `account_userchangelog`
--

DROP TABLE IF EXISTS `account_userchangelog`;
CREATE TABLE `account_userchangelog` (
  `id` int(11) NOT NULL auto_increment,
  `change_type` int(11) NOT NULL,
  `befor` varchar(64) NOT NULL,
  `after` varchar(64) NOT NULL,
  `ip` varchar(32) default NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `account_userchangelog_ad0a036` (`befor`),
  KEY `account_userchangelog_2e98f6d4` (`after`),
  KEY `account_userchangelog_1b05a784` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_userchangelog`
--


/*!40000 ALTER TABLE `account_userchangelog` DISABLE KEYS */;
LOCK TABLES `account_userchangelog` WRITE;
UNLOCK TABLES;
/*!40000 ALTER TABLE `account_userchangelog` ENABLE KEYS */;

--
-- Table structure for table `account_usercount`
--

DROP TABLE IF EXISTS `account_usercount`;
CREATE TABLE `account_usercount` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` varchar(32) NOT NULL,
  `user_journey_count` int(11) NOT NULL,
  `user_answer_count` int(11) NOT NULL,
  `user_liked_count` int(11) NOT NULL,
  `following_count` int(11) NOT NULL,
  `follower_count` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `account_usercount_3cee4d53` (`user_journey_count`),
  KEY `account_usercount_4fa14630` (`user_answer_count`),
  KEY `account_usercount_e7a73c4` (`user_liked_count`),
  KEY `account_usercount_6fcbab0b` (`following_count`),
  KEY `account_usercount_334f5d3b` (`follower_count`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_usercount`
--


/*!40000 ALTER TABLE `account_usercount` DISABLE KEYS */;
LOCK TABLES `account_usercount` WRITE;
UNLOCK TABLES;
/*!40000 ALTER TABLE `account_usercount` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

