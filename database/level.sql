CREATE DATABASE IF NOT EXISTS `userlevels`;
USE `userlevels`;

CREATE TABLE IF NOT EXISTS `users` (
  `guild_id` bigint NOT NULL,
  `client_id` bigint NOT NULL,
  `user_xp` int NOT NULL DEFAULT '0',
  `user_level` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;