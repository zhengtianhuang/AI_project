-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2023 年 05 月 04 日 07:47
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
-- 資料表結構 `emotions`
--

CREATE TABLE `emotions` (
  `emotion_id` int(11) NOT NULL,
  `emotion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `emotions`
--

INSERT INTO `emotions` (`emotion_id`, `emotion`) VALUES
(0, '生氣'),
(1, '開心'),
(2, '放鬆'),
(3, '難過');

-- --------------------------------------------------------

--
-- 資料表結構 `pets`
--

CREATE TABLE `pets` (
  `user_id` varchar(50) NOT NULL,
  `pet_name` varchar(50) NOT NULL,
  `pet_photo` varchar(100) NOT NULL,
  `pet_breed` varchar(50) NOT NULL,
  `created_time` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `pet_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `pets`
--

INSERT INTO `pets` (`user_id`, `pet_name`, `pet_photo`, `pet_breed`, `created_time`, `updated_time`, `pet_id`) VALUES
('1099', 'piggy', '5678.png', '吉娃娃', '2023-04-18 15:23:00', '0000-00-00 00:00:00', 2),
('POPO', 'Lion', 'iiii.png', '貴賓狗', '2023-04-18 15:46:41', '0000-00-00 00:00:00', 3),
('oljimmm', 'jimmy', '5678.png', '吉娃娃', '2023-04-18 15:25:31', '0000-00-00 00:00:00', 4),
('123', 'nini2', '2.jpg', 'black', '2023-04-19 15:02:15', '2023-04-19 15:03:52', 6),
('U751dd717d052680824fd250ddb7a7a55', '大白', '18088873756307-1683177795.jpg', '薩摩耶犬', '2023-05-04 13:23:18', '2023-05-04 13:23:18', 8),
('U751dd717d052680824fd250ddb7a7a55', 'Collie', '18088876386728-1683177841.jpg', '邊境牧羊犬', '2023-05-04 13:24:06', '2023-05-04 13:24:06', 9);

-- --------------------------------------------------------

--
-- 資料表結構 `pets_emotions`
--

CREATE TABLE `pets_emotions` (
  `pet_emotion_id` int(11) NOT NULL,
  `pet_id` int(11) NOT NULL,
  `pet_emotion` int(11) NOT NULL,
  `updated_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `pets_emotions`
--

INSERT INTO `pets_emotions` (`pet_emotion_id`, `pet_id`, `pet_emotion`, `updated_time`) VALUES
(2, 1, 2, '2023-05-03 15:34:48'),
(4, 5, 4, '2023-05-03 22:56:27'),
(5, 3, 1, '2023-05-03 23:07:00'),
(6, 6, 1, '2023-05-03 23:07:49'),
(7, 7, 2, '2023-05-04 13:17:34'),
(8, 8, 0, '2023-05-04 13:40:41'),
(9, 9, 2, '2023-05-04 13:35:39');

-- --------------------------------------------------------

--
-- 資料表結構 `users`
--

CREATE TABLE `users` (
  `user_id` varchar(100) NOT NULL,
  `created_time` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `users`
--

INSERT INTO `users` (`user_id`, `created_time`, `updated_time`) VALUES
('12345', '2023-04-16 17:50:49', '2023-04-16 17:50:49'),
('123456', '2023-04-17 13:30:03', '2023-04-17 13:30:03'),
('4040', '2023-04-17 13:34:43', '2023-04-17 13:34:43'),
('aaa', '2023-04-18 15:25:31', '2023-04-18 15:25:31'),
('abc', '2023-04-16 17:46:53', '2023-04-16 17:46:53'),
('ijjm1122', '2023-04-18 15:46:41', '2023-04-18 15:46:41'),
('ohya', '2023-04-17 13:37:17', '2023-04-17 13:37:17'),
('popo', '2023-04-18 10:03:42', '2023-04-18 10:03:42'),
('U751dd717d052680824fd250ddb7a7a55', '2023-04-17 16:17:18', '2023-04-17 16:17:18'),
('U8f511f37ee2064e1868f50fb8082dd9f', '2023-04-17 13:50:42', '2023-04-17 13:50:42');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `emotions`
--
ALTER TABLE `emotions`
  ADD PRIMARY KEY (`emotion_id`);

--
-- 資料表索引 `pets`
--
ALTER TABLE `pets`
  ADD PRIMARY KEY (`pet_id`);

--
-- 資料表索引 `pets_emotions`
--
ALTER TABLE `pets_emotions`
  ADD PRIMARY KEY (`pet_emotion_id`);

--
-- 資料表索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `emotions`
--
ALTER TABLE `emotions`
  MODIFY `emotion_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `pets`
--
ALTER TABLE `pets`
  MODIFY `pet_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `pets_emotions`
--
ALTER TABLE `pets_emotions`
  MODIFY `pet_emotion_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
