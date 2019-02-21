-- MySQL dump 10.13  Distrib 5.6.41, for macos10.13 (x86_64)
--
-- Host: localhost    Database: autoscaling
-- ------------------------------------------------------
-- Server version	5.6.41

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
-- Table structure for table `hosts`
--

DROP TABLE IF EXISTS `hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hosts` (
  `hostname` varchar(200) DEFAULT NULL COMMENT '主机名',
  `region` varchar(20) DEFAULT '' COMMENT '数据中心名',
  `size` varchar(20) NOT NULL COMMENT '机器规格',
  `hostid` bigint(20) DEFAULT NULL COMMENT '主机id',
  `snapshotid` bigint(20) DEFAULT NULL COMMENT '快照id',
  `public` varchar(20) DEFAULT '' COMMENT '外网ip',
  `private` varchar(20) DEFAULT NULL COMMENT '内网ip',
  `group` varchar(11) NOT NULL DEFAULT '' COMMENT '组id',
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tags` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qps`
--

DROP TABLE IF EXISTS `qps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qps` (
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `servername` varchar(1000) DEFAULT NULL COMMENT '被统计的 qps域名',
  `SecondsSinceLast` int(11) DEFAULT NULL COMMENT 'qps统计的时间长度,单位秒',
  `AverageReqTimeSec` float(6,4) DEFAULT NULL COMMENT '平均请求时间',
  `RequestCount` int(11) DEFAULT NULL COMMENT '单位时间总请求数,当调用api后会重置',
  `RequestsPerSecs` float(6,4) DEFAULT NULL COMMENT '每秒请求数',
  `5xxnum` int(11) DEFAULT NULL COMMENT '单位时间出现500次数,调用查看接口后重置',
  `group` varchar(50) DEFAULT NULL COMMENT '组,即属于哪台负载后面的机器',
  `ServerNumber` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-21 17:22:45
