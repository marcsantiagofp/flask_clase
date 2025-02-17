-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 17-02-2025 a las 16:13:23
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `flask_app`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `log`
--

CREATE TABLE `log` (
  `id` int(11) NOT NULL,
  `matricula` varchar(120) NOT NULL,
  `fecha_entrada` datetime NOT NULL,
  `fecha_salida` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parking`
--

CREATE TABLE `parking` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `parking`
--

INSERT INTO `parking` (`id`, `nombre`) VALUES
(1, 'Parking 1'),
(2, 'Parking 2');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plaza`
--

CREATE TABLE `plaza` (
  `id` int(11) NOT NULL,
  `parking_id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `estado` enum('libre','ocupada','reservada') DEFAULT 'libre',
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `plaza`
--

INSERT INTO `plaza` (`id`, `parking_id`, `numero`, `estado`, `user_id`) VALUES
(1, 1, 1, 'reservada', 5),
(2, 1, 2, 'reservada', 5),
(3, 1, 3, 'libre', NULL),
(4, 1, 4, 'libre', NULL),
(5, 1, 5, 'libre', NULL),
(6, 1, 6, 'libre', NULL),
(7, 1, 7, 'libre', NULL),
(8, 1, 8, 'libre', NULL),
(9, 1, 9, 'libre', NULL),
(10, 1, 10, 'libre', NULL),
(11, 1, 11, 'libre', NULL),
(12, 1, 12, 'libre', NULL),
(13, 1, 13, 'reservada', 5),
(14, 1, 14, 'libre', NULL),
(15, 1, 15, 'reservada', 5),
(16, 1, 16, 'libre', NULL),
(17, 2, 17, 'reservada', 5),
(18, 2, 18, 'libre', NULL),
(19, 2, 19, 'libre', NULL),
(20, 2, 20, 'libre', NULL),
(21, 2, 21, 'libre', NULL),
(22, 2, 22, 'libre', NULL),
(23, 2, 23, 'libre', NULL),
(24, 2, 24, 'libre', NULL),
(25, 2, 25, 'libre', NULL),
(26, 2, 26, 'libre', NULL),
(27, 2, 27, 'libre', NULL),
(28, 2, 28, 'libre', NULL),
(29, 2, 29, 'libre', NULL),
(30, 2, 30, 'libre', NULL),
(31, 2, 31, 'libre', NULL),
(32, 2, 32, 'libre', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `username`, `apellido`, `telefono`, `password`, `email`, `created_at`) VALUES
(5, 'Marc', 'Santiago', '123456789', 'scrypt:32768:8:1$r73ELIU9IrJoybiE$caaa3644285f95f86a11227433718542ebed3401a1f2eac25b9e3db4dce076291fc2021de8b1115f0f06a7cda2a3ed6c717510669321e9240e01376045de572e', 'marc@gmail.com', '2025-01-13 16:15:10'),
(6, 'Iago', 'Medina', '666666666', 'scrypt:32768:8:1$H5LRqqOUwQGnD3II$5b16126a428d6a9808bafb596f037236d5683a3d3a2a68c39c2dc2e50bb258d0f8cf846d9d198949a30794889f1e41f93e17b5416ef0057f2123d21f40e60f5e', 'iago@gmail.com', '2025-01-30 18:27:38');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
--

CREATE TABLE `vehiculo` (
  `id` int(11) NOT NULL,
  `marca` varchar(120) DEFAULT NULL,
  `modelo` varchar(120) DEFAULT NULL,
  `matricula` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo` varchar(120) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `vehiculo`
--

INSERT INTO `vehiculo` (`id`, `marca`, `modelo`, `matricula`, `tipo`, `user_id`) VALUES
(1, 'Seat', 'Leon', '1234 aaa', 'coche', 5);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `log`
--
ALTER TABLE `log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `matricula` (`matricula`);

--
-- Indices de la tabla `parking`
--
ALTER TABLE `parking`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `plaza`
--
ALTER TABLE `plaza`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parking_id` (`parking_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_matricula` (`matricula`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `log`
--
ALTER TABLE `log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `parking`
--
ALTER TABLE `parking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `plaza`
--
ALTER TABLE `plaza`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `log`
--
ALTER TABLE `log`
  ADD CONSTRAINT `log_ibfk_1` FOREIGN KEY (`matricula`) REFERENCES `vehiculo` (`matricula`) ON DELETE CASCADE;

--
-- Filtros para la tabla `plaza`
--
ALTER TABLE `plaza`
  ADD CONSTRAINT `plaza_ibfk_1` FOREIGN KEY (`parking_id`) REFERENCES `parking` (`id`),
  ADD CONSTRAINT `plaza_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD CONSTRAINT `vehiculo_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
