-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        8.0.27 - MySQL Community Server - GPL
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- test 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `test`;

-- 테이블 test.계좌 구조 내보내기
CREATE TABLE IF NOT EXISTS `계좌` (
  `계좌번호` varchar(50) NOT NULL,
  `비밀번호` char(4) NOT NULL,
  `계좌종류` char(2) NOT NULL,
  `이체한도` bigint NOT NULL,
  `발급은행지점` varchar(20) NOT NULL,
  `계좌개설날짜` date NOT NULL,
  `예금금융상품ID` int DEFAULT NULL,
  `적금금융상품ID` int DEFAULT NULL,
  `대출금융상품ID` int DEFAULT NULL,
  `펀드금융상품ID` int DEFAULT NULL,
  `관리자번호` int NOT NULL,
  `주민등록번호` varchar(30) NOT NULL,
  PRIMARY KEY (`계좌번호`),
  KEY `계좌_ibfk_2` (`적금금융상품ID`),
  KEY `계좌_ibfk_3` (`대출금융상품ID`),
  KEY `계좌_ibfk_1` (`예금금융상품ID`),
  KEY `계좌_ibfk_5` (`관리자번호`),
  KEY `계좌_ibfk_6` (`주민등록번호`),
  KEY `계좌_ibfk_4` (`펀드금융상품ID`),
  CONSTRAINT `계좌_ibfk_1` FOREIGN KEY (`예금금융상품ID`) REFERENCES `예금` (`금융상품ID`),
  CONSTRAINT `계좌_ibfk_2` FOREIGN KEY (`적금금융상품ID`) REFERENCES `적금` (`금융상품ID`),
  CONSTRAINT `계좌_ibfk_3` FOREIGN KEY (`대출금융상품ID`) REFERENCES `대출` (`금융상품ID`),
  CONSTRAINT `계좌_ibfk_4` FOREIGN KEY (`펀드금융상품ID`) REFERENCES `펀드` (`금융상품ID`),
  CONSTRAINT `계좌_ibfk_5` FOREIGN KEY (`관리자번호`) REFERENCES `관리자` (`관리자번호`),
  CONSTRAINT `계좌_ibfk_6` FOREIGN KEY (`주민등록번호`) REFERENCES `사용자` (`주민등록번호`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.계좌:~20 rows (대략적) 내보내기
/*!40000 ALTER TABLE `계좌` DISABLE KEYS */;
INSERT INTO `계좌` (`계좌번호`, `비밀번호`, `계좌종류`, `이체한도`, `발급은행지점`, `계좌개설날짜`, `예금금융상품ID`, `적금금융상품ID`, `대출금융상품ID`, `펀드금융상품ID`, `관리자번호`, `주민등록번호`) VALUES
	('000000001', '0000', '예금', 300000, '부천', '2021-11-30', 1000, NULL, NULL, NULL, 1, '200001011111111'),
	('000000002', '0000', '예금', 300000, '서울', '2019-01-01', 1001, NULL, NULL, NULL, 2, '200001011111111'),
	('000000003', '0000', '적금', 400000, '안양', '2020-09-08', NULL, 2002, NULL, NULL, 4, '200001011111111'),
	('000000004', '0000', '대출', 20000000, '부천', '2001-01-01', NULL, NULL, 3003, NULL, 5, '200001011111111'),
	('000000005', '1111', '적금', 2000000, '용인', '2020-03-11', NULL, 2000, NULL, NULL, 1, '200001021111111'),
	('000000006', '1111', '적금', 400000, '용인', '2021-01-01', NULL, 2003, NULL, NULL, 7, '200001021111111'),
	('000000007', '1111', '대출', 200000, '용인', '2009-10-11', NULL, NULL, 3001, NULL, 3, '200001021111111'),
	('000000008', '1111', '펀드', 5000000, '용인', '2022-03-12', NULL, NULL, NULL, 4000, 1, '200001021111111'),
	('000000009', '1111', '펀드', 400000, '용인', '2008-10-09', NULL, NULL, NULL, 4001, 3, '200001021111111'),
	('000000010', '2222', '대출', 900000, '서울', '2003-01-02', NULL, NULL, 3002, NULL, 5, '199901012222222'),
	('000000011', '2223', '대출', 2000000, '서울', '2020-05-02', NULL, NULL, 3001, NULL, 3, '199901012222222'),
	('000000012', '2224', '적금', 1500000, '수원', '2021-01-01', NULL, 2001, NULL, NULL, 2, '199901012222222'),
	('000000013', '2222', '적금', 300000, '안양', '2020-03-04', NULL, 2000, NULL, NULL, 1, '199901012222222'),
	('000000014', '3333', '예금', 350000, '부천', '2021-04-05', 1002, NULL, NULL, NULL, 3, '199601011111111'),
	('000000015', '3331', '예금', 400000, '부천', '2020-08-07', 1003, NULL, NULL, NULL, 6, '199601011111111'),
	('000000016', '3333', '대출', 450000, '대전', '2020-03-01', NULL, NULL, 3000, NULL, 2, '199601011111111'),
	('000000017', '3334', '펀드', 4500000, '부천', '2023-01-02', NULL, NULL, NULL, 4001, 3, '199601011111111'),
	('000000018', '3335', '펀드', 5000000, '부천', '2020-03-01', NULL, NULL, NULL, 4002, 5, '199601011111111'),
	('000000019', '2222', '대출', 4000000, '부천', '2020-09-03', NULL, NULL, 3001, NULL, 3, '199901012222222'),
	('000000020', '2222', '예금', 450000, '부천', '2021-01-02', 1000, NULL, NULL, NULL, 1, '199901012222222');
/*!40000 ALTER TABLE `계좌` ENABLE KEYS */;

-- 테이블 test.계좌_입출금내역 구조 내보내기
CREATE TABLE IF NOT EXISTS `계좌_입출금내역` (
  `입금내역` bigint DEFAULT '0',
  `출금내역` bigint DEFAULT '0',
  `계좌번호` varchar(50) NOT NULL,
  `순서` bigint NOT NULL DEFAULT '0',
  PRIMARY KEY (`순서`,`계좌번호`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.계좌_입출금내역:~21 rows (대략적) 내보내기
/*!40000 ALTER TABLE `계좌_입출금내역` DISABLE KEYS */;
INSERT INTO `계좌_입출금내역` (`입금내역`, `출금내역`, `계좌번호`, `순서`) VALUES
	(0, 0, '000000001', 0),
	(0, 0, '000000002', 0),
	(0, 0, '000000003', 0),
	(0, 0, '000000004', 0),
	(0, 0, '000000005', 0),
	(0, 0, '000000006', 0),
	(0, 0, '000000007', 0),
	(0, 0, '000000008', 0),
	(0, 0, '000000009', 0),
	(0, 0, '000000010', 0),
	(0, 0, '000000011', 0),
	(0, 0, '000000012', 0),
	(0, 0, '000000013', 0),
	(0, 0, '000000014', 0),
	(0, 0, '000000015', 0),
	(0, 0, '000000016', 0),
	(0, 0, '000000017', 0),
	(0, 0, '000000018', 0),
	(0, 0, '000000019', 0),
	(0, 0, '000000020', 0),
	(160000, 3000, '000000001', 1),
	(300000, 0, '000000002', 1),
	(0, 10000, '000000002', 2);
/*!40000 ALTER TABLE `계좌_입출금내역` ENABLE KEYS */;

-- 테이블 test.관리자 구조 내보내기
CREATE TABLE IF NOT EXISTS `관리자` (
  `관리자번호` int NOT NULL,
  `담당부서` varchar(20) NOT NULL,
  `소속은행지점` varchar(20) NOT NULL,
  PRIMARY KEY (`관리자번호`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.관리자:~8 rows (대략적) 내보내기
/*!40000 ALTER TABLE `관리자` DISABLE KEYS */;
INSERT INTO `관리자` (`관리자번호`, `담당부서`, `소속은행지점`) VALUES
	(1, '예금', '부천'),
	(2, '예금', '서울'),
	(3, '적금', '수원'),
	(4, '적금', '대전'),
	(5, '대출', '용인'),
	(6, '대출', '안양'),
	(7, '펀드', '인천'),
	(8, '펀드', '부산');
/*!40000 ALTER TABLE `관리자` ENABLE KEYS */;

-- 테이블 test.대출 구조 내보내기
CREATE TABLE IF NOT EXISTS `대출` (
  `금융상품ID` int NOT NULL,
  `담보종류` varchar(50) NOT NULL,
  `적용금리` decimal(10,2) NOT NULL,
  `만기일` date NOT NULL,
  `대출한도` bigint NOT NULL,
  `운영책임자` int NOT NULL,
  PRIMARY KEY (`금융상품ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.대출:~4 rows (대략적) 내보내기
/*!40000 ALTER TABLE `대출` DISABLE KEYS */;
INSERT INTO `대출` (`금융상품ID`, `담보종류`, `적용금리`, `만기일`, `대출한도`, `운영책임자`) VALUES
	(3000, '주택', 0.01, '2025-09-05', 40000000, 2),
	(3001, '자동차', 0.03, '2024-05-06', 5000000, 3),
	(3002, '주택', 0.02, '2023-01-01', 1000000, 5),
	(3003, '주택', 0.05, '2030-04-01', 3000000, 5),
	(3004, '토지', 0.04, '2025-01-02', 40000000, 4);
/*!40000 ALTER TABLE `대출` ENABLE KEYS */;

-- 테이블 test.사용자 구조 내보내기
CREATE TABLE IF NOT EXISTS `사용자` (
  `성` varchar(2) NOT NULL,
  `이름` varchar(3) NOT NULL,
  `주민등록번호` varchar(30) NOT NULL,
  `담보` varchar(50) DEFAULT NULL,
  `신용등급` int DEFAULT NULL,
  PRIMARY KEY (`주민등록번호`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.사용자:~4 rows (대략적) 내보내기
/*!40000 ALTER TABLE `사용자` DISABLE KEYS */;
INSERT INTO `사용자` (`성`, `이름`, `주민등록번호`, `담보`, `신용등급`) VALUES
	('이', '영희', '199502031111111', '주택', 3),
	('이', '준영', '199601011111111', '토지', 3),
	('김', '철수', '199901012222222', '주택', 2),
	('이', '선민', '200001011111111', '주택', 1),
	('엄', '찬영', '200001021111111', '자동차', 1);
/*!40000 ALTER TABLE `사용자` ENABLE KEYS */;

-- 테이블 test.사용자_계좌번호 구조 내보내기
CREATE TABLE IF NOT EXISTS `사용자_계좌번호` (
  `계좌번호` varchar(50) NOT NULL,
  `주민등록번호` varchar(30) NOT NULL,
  PRIMARY KEY (`계좌번호`,`주민등록번호`),
  KEY `사용자_계좌번호_ibfk_1` (`주민등록번호`),
  CONSTRAINT `사용자_계좌번호_ibfk_1` FOREIGN KEY (`주민등록번호`) REFERENCES `사용자` (`주민등록번호`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.사용자_계좌번호:~20 rows (대략적) 내보내기
/*!40000 ALTER TABLE `사용자_계좌번호` DISABLE KEYS */;
INSERT INTO `사용자_계좌번호` (`계좌번호`, `주민등록번호`) VALUES
	('000000014', '199601011111111'),
	('000000015', '199601011111111'),
	('000000016', '199601011111111'),
	('000000017', '199601011111111'),
	('000000018', '199601011111111'),
	('000000010', '199901012222222'),
	('000000011', '199901012222222'),
	('000000012', '199901012222222'),
	('000000013', '199901012222222'),
	('000000019', '199901012222222'),
	('000000020', '199901012222222'),
	('000000001', '200001011111111'),
	('000000002', '200001011111111'),
	('000000003', '200001011111111'),
	('000000004', '200001011111111'),
	('000000005', '200001021111111'),
	('000000006', '200001021111111'),
	('000000007', '200001021111111'),
	('000000008', '200001021111111'),
	('000000009', '200001021111111');
/*!40000 ALTER TABLE `사용자_계좌번호` ENABLE KEYS */;

-- 테이블 test.사용자_전화번호 구조 내보내기
CREATE TABLE IF NOT EXISTS `사용자_전화번호` (
  `전화번호` varchar(30) NOT NULL,
  `주민등록번호` varchar(30) NOT NULL,
  PRIMARY KEY (`전화번호`,`주민등록번호`),
  KEY `사용자_전화번호_ibfk_1` (`주민등록번호`),
  CONSTRAINT `사용자_전화번호_ibfk_1` FOREIGN KEY (`주민등록번호`) REFERENCES `사용자` (`주민등록번호`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.사용자_전화번호:~7 rows (대략적) 내보내기
/*!40000 ALTER TABLE `사용자_전화번호` DISABLE KEYS */;
INSERT INTO `사용자_전화번호` (`전화번호`, `주민등록번호`) VALUES
	('01099990000', '199502031111111'),
	('01099999998', '199502031111111'),
	('01022222222', '199601011111111'),
	('01088888888', '199901012222222'),
	('01099999999', '199901012222222'),
	('01011111111', '200001011111111'),
	('01047675793', '200001011111111'),
	('01051955793', '200001011111111'),
	('01000000000', '200001021111111');
/*!40000 ALTER TABLE `사용자_전화번호` ENABLE KEYS */;

-- 테이블 test.예금 구조 내보내기
CREATE TABLE IF NOT EXISTS `예금` (
  `금융상품ID` int NOT NULL,
  `연금리` decimal(10,2) NOT NULL,
  `운영책임자` int NOT NULL,
  PRIMARY KEY (`금융상품ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.예금:~4 rows (대략적) 내보내기
/*!40000 ALTER TABLE `예금` DISABLE KEYS */;
INSERT INTO `예금` (`금융상품ID`, `연금리`, `운영책임자`) VALUES
	(1000, 0.01, 1),
	(1001, 0.03, 2),
	(1002, 0.30, 3),
	(1003, 0.01, 6),
	(1004, 0.02, 6);
/*!40000 ALTER TABLE `예금` ENABLE KEYS */;

-- 테이블 test.적금 구조 내보내기
CREATE TABLE IF NOT EXISTS `적금` (
  `금융상품ID` int NOT NULL,
  `연금리` decimal(10,2) NOT NULL,
  `월별저축금액` bigint NOT NULL,
  `만기일` date NOT NULL,
  `운영책임자` int NOT NULL,
  PRIMARY KEY (`금융상품ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.적금:~4 rows (대략적) 내보내기
/*!40000 ALTER TABLE `적금` DISABLE KEYS */;
INSERT INTO `적금` (`금융상품ID`, `연금리`, `월별저축금액`, `만기일`, `운영책임자`) VALUES
	(2000, 0.02, 100000, '2022-01-03', 1),
	(2001, 0.03, 200000, '2021-12-30', 2),
	(2002, 0.01, 10000, '2023-01-01', 4),
	(2003, 0.10, 10000000, '2025-01-03', 7);
/*!40000 ALTER TABLE `적금` ENABLE KEYS */;

-- 테이블 test.펀드 구조 내보내기
CREATE TABLE IF NOT EXISTS `펀드` (
  `금융상품ID` int NOT NULL,
  `주식비율` float NOT NULL DEFAULT '0',
  `채권비율` float NOT NULL DEFAULT '1',
  `위험성` char(1) NOT NULL,
  `기대수익률` decimal(10,3) NOT NULL DEFAULT '0.000',
  `운영책임자` int NOT NULL,
  PRIMARY KEY (`금융상품ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 test.펀드:~2 rows (대략적) 내보내기
/*!40000 ALTER TABLE `펀드` DISABLE KEYS */;
INSERT INTO `펀드` (`금융상품ID`, `주식비율`, `채권비율`, `위험성`, `기대수익률`, `운영책임자`) VALUES
	(4000, 0.5, 0.5, '중', 0.070, 1),
	(4001, 0.1, 0.9, '하', 0.010, 3),
	(4002, 0.4, 0.6, '하', 0.020, 5);
/*!40000 ALTER TABLE `펀드` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
