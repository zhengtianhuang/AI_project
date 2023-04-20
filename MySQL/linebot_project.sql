-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2023 年 04 月 20 日 10:21
-- 伺服器版本： 10.4.27-MariaDB
-- PHP 版本： 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `linebot_project`
--

-- --------------------------------------------------------

--
-- 資料表結構 `emotion`
--

CREATE TABLE `emotion` (
  `emotion_id` int(11) NOT NULL,
  `emotion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `emotion`
--

INSERT INTO `emotion` (`emotion_id`, `emotion`) VALUES
(1, '開心'),
(2, '生氣'),
(3, '難過'),
(4, '放鬆');

-- --------------------------------------------------------

--
-- 資料表結構 `emotion_record`
--

CREATE TABLE `emotion_record` (
  `pet_id` varchar(50) NOT NULL,
  `emotion_photo` varchar(100) NOT NULL,
  `emotion` varchar(50) NOT NULL,
  `updated_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `emotion_record`
--

INSERT INTO `emotion_record` (`pet_id`, `emotion_photo`, `emotion`, `updated_time`) VALUES
('1', 'happ.jpg', '開心', '2023-04-20 10:36:15'),
('1', 'emoaional.jpg', '放鬆', '2023-04-20 15:30:47'),
('1', 'relaxed.jpg', '放鬆', '2023-04-20 15:31:00'),
('1', 'relaxed.jpg', '放鬆', '2023-04-20 15:58:00');

-- --------------------------------------------------------

--
-- 資料表結構 `pet`
--

CREATE TABLE `pet` (
  `user_id` varchar(50) NOT NULL,
  `pet_name` varchar(50) NOT NULL,
  `pet_photo` varchar(100) DEFAULT NULL,
  `pet_breed` varchar(50) NOT NULL,
  `pet_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `pet`
--

INSERT INTO `pet` (`user_id`, `pet_name`, `pet_photo`, `pet_breed`, `pet_id`) VALUES
('U751dd717d052680824fd250ddb7a7a55', 'Golden', 'cde.png', '黃金獵犬', 1),
('oljimmm', 'jimmy', '5678.png', '吉娃娃', 4),
('U751dd717d052680824fd250ddb7a7a55', 'KOKO', '1234.png', '邊牧', 5),
('KIOLLLL', 'Oreo2', 'okok.png', '大麥町', 8),
('KIOLLLL', 'KIKI', '5678.png', '吉娃娃', 9),
('KIOLLLL', 'coco', '5678.png', '吉娃娃', 10),
('KIOLLLL', 'jj', '5678.png', '吉娃娃', 11),
('KIOLLLL', 'aa', '5678.png', '吉娃娃', 12),
('KIOLLLL', 'cc', '5678.png', '吉娃娃', 14),
('KIOLLLL', 'dd', '5678.png', '土狗', 15),
('KIOLLLL', 'ff', '5678.png', '黑狗', 16),
('KIOLLLL', 'ee', '5678.png', '黃狗', 17),
('KIOLLLL', 'jiok', '5678.png', '黃狗', 18),
('KIOLLLL', 'ji', '5678.png', '黃狗', 19),
('KIOLLLL', 'j', '5678.png', '黃狗', 20),
('KIOLLLL', 'j1234', '5678.png', '黃狗', 21),
('KIOLLLL', 'j2345', '5678.png', '胖狗', 24),
('KIOLLLL', 'lol', '5678.png', '大胖狗', 51);

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `user_id` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `user`
--

INSERT INTO `user` (`user_id`) VALUES
('0000'),
('1'),
('11'),
('12345'),
('123456'),
('188'),
('4040'),
('5'),
('6'),
('aaa'),
('aaaa'),
('abc'),
('ijjm1122'),
('ohya'),
('popo'),
('U751dd717d052680824fd250ddb7a7a55'),
('U8f511f37ee2064e1868f50fb8082dd9f');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `emotion`
--
ALTER TABLE `emotion`
  ADD PRIMARY KEY (`emotion_id`);

--
-- 資料表索引 `pet`
--
ALTER TABLE `pet`
  ADD PRIMARY KEY (`pet_id`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `emotion`
--
ALTER TABLE `emotion`
  MODIFY `emotion_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `pet`
--
ALTER TABLE `pet`
  MODIFY `pet_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
