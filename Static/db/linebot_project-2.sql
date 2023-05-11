-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2023 年 05 月 10 日 07:40
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
  `id` int(11) NOT NULL,
  `emotion` varchar(50) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `emotion`
--

INSERT INTO `emotion` (`id`, `emotion`, `created_time`, `updated_time`) VALUES
(1, '生氣', '2023-05-08 03:19:12', '2023-05-10 05:39:08'),
(2, '開心', '2023-05-08 03:19:12', '2023-05-10 05:39:13'),
(3, '放鬆', '2023-05-08 03:19:12', '2023-05-10 05:39:19'),
(4, '難過', '2023-05-08 03:19:12', '2023-05-10 05:39:46');

-- --------------------------------------------------------

--
-- 資料表結構 `emotion_record`
--

CREATE TABLE `emotion_record` (
  `id` int(11) NOT NULL,
  `pet_id` varchar(50) NOT NULL,
  `emotion_photo` varchar(100) DEFAULT NULL,
  `emotion_id` varchar(50) NOT NULL,
  `updated_time` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `emotion_record`
--

INSERT INTO `emotion_record` (`id`, `pet_id`, `emotion_photo`, `emotion_id`, `updated_time`, `created_time`) VALUES
(7, '57', NULL, '1', '2023-05-10 11:28:02', '2023-05-10 03:28:02');

-- --------------------------------------------------------

--
-- 資料表結構 `pet`
--

CREATE TABLE `pet` (
  `id` int(11) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `pet_name` varchar(50) NOT NULL,
  `pet_photo` varchar(100) DEFAULT NULL,
  `pet_breed` varchar(50) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `pet`
--

INSERT INTO `pet` (`id`, `user_id`, `pet_name`, `pet_photo`, `pet_breed`, `created_time`, `updated_time`) VALUES
(57, '26', '狗狗', '182512277102302119-1683620990.jpg', '未知', '2023-05-09 08:29:51', '2023-05-09 08:29:51');

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `line_user_id` varchar(100) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `user`
--

INSERT INTO `user` (`id`, `line_user_id`, `created_time`, `updated_time`) VALUES
(26, 'U751dd717d052680824fd250ddb7a7a55', '2023-05-09 08:29:51', '2023-05-09 08:29:51'),
(27, 'U99b18d2a7c6d406533eef42acaf65b56', '2023-05-10 03:35:48', '2023-05-10 03:35:48');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `emotion`
--
ALTER TABLE `emotion`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `emotion_record`
--
ALTER TABLE `emotion_record`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `pet`
--
ALTER TABLE `pet`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_2` (`id`),
  ADD KEY `id_3` (`id`),
  ADD KEY `id` (`id`),
  ADD KEY `id_4` (`id`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `line_user_id_2` (`line_user_id`),
  ADD KEY `line_user_id` (`line_user_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `emotion`
--
ALTER TABLE `emotion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `emotion_record`
--
ALTER TABLE `emotion_record`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `pet`
--
ALTER TABLE `pet`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
