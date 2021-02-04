-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 04 Şub 2021, 18:02:46
-- Sunucu sürümü: 10.4.16-MariaDB
-- PHP Sürümü: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `brainsoup`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `about`
--

CREATE TABLE `about` (
  `title` varchar(250) COLLATE utf8mb4_turkish_ci NOT NULL,
  `detail` varchar(400) COLLATE utf8mb4_turkish_ci NOT NULL,
  `whyus` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `doctor` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `brain` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `cloud` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `about`
--

INSERT INTO `about` (`title`, `detail`, `whyus`, `doctor`, `brain`, `cloud`, `id`) VALUES
('BRAİNSOUP WEB ASİSTANINA HOŞ GELDİNİZ', 'Beyin Tümörü Tespiti İçin MR Sonuçlarına Göre Doktorlara Yardımcı Olan Bir Web Asistandır.', 'Türkiyenin en iyi Yapay Zeka destekli beyin tümörü tespiti yapabilen web asistanıdır.Gerçek hastane verileriyle sistemimizi eğittiğimiz için size en doğru sonuçları gösteriyoruz.  ', 'Son Teknoloji Yapay Zekamızla doktorlara yardımcı oluyoruz', 'Beyin MR sonuçlarınızı yapay zeka programlarımızla inceliyoruz.Hastaneye gitmenize gerek kalmadan ön tanınızı koyuyoruz', 'Bulut desteğimiz sayesinde her hangi bir aplikasyonu indirmenize gerek kalmaksızın sistemimizi kullanabilirsiniz.', 1);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(75) COLLATE utf8mb4_turkish_ci NOT NULL,
  `password` varchar(150) COLLATE utf8mb4_turkish_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`, `email`) VALUES
(1, 'admin', 'admin', 'ugurilgin94@gmail.com');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `email` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `phone` varchar(30) COLLATE utf8mb4_turkish_ci NOT NULL,
  `adress` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `twitter` varchar(250) COLLATE utf8mb4_turkish_ci NOT NULL,
  `facebook` varchar(250) COLLATE utf8mb4_turkish_ci NOT NULL,
  `instagram` varchar(250) COLLATE utf8mb4_turkish_ci NOT NULL,
  `skype` varchar(250) COLLATE utf8mb4_turkish_ci NOT NULL,
  `linkedin` varchar(250) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `contact`
--

INSERT INTO `contact` (`id`, `email`, `phone`, `adress`, `twitter`, `facebook`, `instagram`, `skype`, `linkedin`) VALUES
(1, 'ugurilgin94@gmail.com', '(111)-111-1111', 'Çorlu,Tekirdağ', '#', '#', '#', '#', '#');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `email`
--

CREATE TABLE `email` (
  `id` int(11) NOT NULL,
  `fullname` varchar(200) COLLATE utf8mb4_turkish_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_turkish_ci NOT NULL,
  `subject` varchar(250) COLLATE utf8mb4_turkish_ci NOT NULL,
  `message` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `date` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ban` varchar(1) COLLATE utf8mb4_turkish_ci NOT NULL,
  `status` varchar(1) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `email`
--

INSERT INTO `email` (`id`, `fullname`, `email`, `subject`, `message`, `date`, `ban`, `status`) VALUES
(1, 'Uğur Ilgın', 'ugurilgin94@gmail.com', 'Test', 'Test Mesajım', '2021-01-03', '0', '1'),
(2, 'Mehmet', 'mehmeto@zgmail.com', 'Beyin Tümörü Yardım', 'dsggsfgfd', '2021-01-03', '0', '1'),
(3, 'Mehmet İkinci', 'mehmeto@zgmail.com', 'Beyin Tümörü Yardım', 'dsggsfgfd', '2021-01-03', '0', '1'),
(4, 'Admin', 'admin@admin.com', 'Help Doctor', 'Help', '2021-01-03', '0', '1'),
(5, 'Test ', 'test@admin.com', 'Test', 'Test', '2021-01-03', '0', '0'),
(6, 'Brain Soup', 'br@bra.com', 'Hello I am Brain Soup', 'Hello I am Brain Soup', '2021-01-03', '0', '1'),
(7, 'George Washington', 'usa@usa.com', 'Hello I am the first president of USA ', 'Hello I am Brain Soup', '2021-01-03', '0', '1'),
(8, 'Hacı Ahmet', 'usa@usa.com', 'Lütfen Cevap Verin', 'Lütfen Cevap Verin', '2021-01-03', '0', '1'),
(9, 'Mustafa Ali', 'musti@musti.com', 'Lütfen Cevap Verin Mesajıma', 'Lütfen Cevap Verin', '2021-01-03', '0', '1'),
(10, 'Spartacus', 'sq@musti.com', 'I am Spartacus', 'Lütfen Cevap Verin', '2021-01-03', '0', '1'),
(11, 'Hello ', 'sq@musti.com', 'Hello', 'Lütfen Cevap Verin', '2021-01-03', '0', '1'),
(12, 'Merhaba Yeni Mesaj', 'aa@aa.com', 'Merhaba Yeni Mesaj', 'Merhaba Yeni Mesaj', '2021-01-05', '0', '0');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `employee`
--

CREATE TABLE `employee` (
  `id` int(11) NOT NULL,
  `name` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `surname` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `position` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `short` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `about` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `image` varchar(500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `twitter` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `facebook` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `instagram` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `linkedin` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ban` varchar(2) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `employee`
--

INSERT INTO `employee` (`id`, `name`, `surname`, `position`, `short`, `about`, `image`, `twitter`, `facebook`, `instagram`, `linkedin`, `ban`) VALUES
(1, 'Uğur', 'Ilgın', 'Takım Lideri & Programmer', 'Yapay zeka uygulamamızı yapan mühendisimizdir.  ', 'I am experienced in Programming(Mobile and Desktop and Web ) and Penetraion Testing .I created project over 10 and I worked many project about desktop and mobile app.I learned too much information about Cyber Security from Cybrary ,Udemy,Edx,Coursera etc.I love Computer Programming since I was a teenager.I created first game at High School.I hacked many vulnerable machine on Hackthebox and Vulnhub etc at University .After that day I try to improve my skills everytime.\r\n\r\n  ', 'assets/img/doctors/doctors-1.jpg', '#', 'https://www.facebook.com/profile.php?id=1627833141', 'https://www.instagram.com/ilginugurr/', 'https://www.linkedin.com/in/ugur-ilgin/', '0'),
(2, 'Beyin Tümörü', ' Algılayan AI', 'Beyin ve Sinir Cerrahi', 'Doktorlarımıza yardımcı olan web asistanımızdır', 'Doktorlarımıza yardımcı olan web asistanımızdır', 'assets/img/doctors/doctors-2.jpg', '#', '#', '#', '#', '0'),
(3, 'Test', 'Test', 'Test', '   Test ', '   Test ', 'AI4H_Heart_16x9.jpg', 'Test', 'Test', 'Test', 'Test', '0'),
(4, 'Uğur Ilgın', ' Ilgın', 'Test', ' ', ' ', 'AI4H_Heart_16x9.jpg', '', '', '', '', '1');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `patients`
--

CREATE TABLE `patients` (
  `id` int(11) NOT NULL,
  `TC` varchar(11) COLLATE utf8mb4_turkish_ci NOT NULL,
  `name` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `surname` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_turkish_ci NOT NULL,
  `birthdate` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `date` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `doctor` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ban` varchar(1) COLLATE utf8mb4_turkish_ci NOT NULL,
  `cinsiyet` varchar(10) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `patients`
--

INSERT INTO `patients` (`id`, `TC`, `name`, `surname`, `email`, `birthdate`, `date`, `doctor`, `ban`, `cinsiyet`) VALUES
(1, '12345678901', 'Test', 'Hasta', 'test@gmail.com', '1980-06-01', '2020-11-27', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Erkek'),
(2, '11111213231', 'Mehmet', 'Ali', 'memo@gmail.com', '2012-01-19', '2020-11-27', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Erkek'),
(3, '11111213238', 'Sonay', 'Soner', 'son@son.com', '1990-12-16', '2020-12-17', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Erkek'),
(4, '82345678901', 'Ayşe', 'Fatma', 'ayse@hh.com', '1960-12-16', '2020-12-18', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Kadın'),
(5, '92345678901', 'Hayriye', 'Cantaş', 'hayriye@hayrie.com', '1954-06-18', '2020-12-18', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Kadın'),
(6, '98345678901', 'Dede', 'Korkut', 'dede@dede.com', '1950-07-15', '2020-12-18', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Erkek'),
(7, '99345678901', 'Ahsen', 'Beyoğlu', 'ahsen@ahsen.com', '2000-06-18', '2020-12-18', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Kadın'),
(8, '92345978901', 'Hacı Ahmet', 'Çelebi', 'hagi@ggg.com', '1970-10-05', '2020-12-18', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Erkek'),
(9, '92945678908', 'Mustafa Ali', 'Dal', 'musti@hotmail.com', '1960-12-08', '2020-12-18', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Erkek'),
(10, '78375678901', 'Nurcan', 'Dal', 'nurcdal@hotmail.com', '1965-10-05', '2020-12-18', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Kadın'),
(11, '12348678908', 'New2', 'New', 'newugurilgin94@gmail.com', '1980-06-09', '2021-01-05', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '1', 'Erkek'),
(12, '88111111199', 'Yeni ', 'Hasta', 'yenihasta@hotmail.com', '2021-02-18', '2021-02-04', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '0', 'Kadın');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `referance`
--

CREATE TABLE `referance` (
  `id` int(11) NOT NULL,
  `name` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `surname` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `image` varchar(500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `position` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `comment` varchar(500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ban` varchar(1) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `referance`
--

INSERT INTO `referance` (`id`, `name`, `surname`, `image`, `position`, `comment`, `ban`) VALUES
(1, '1Saul', '2Goodman', '0assets/img/testimonials/testimonials-1.jpg', '3Ceo & Founder', '4Vay,Bu web asistanının yapay zeka doktorlarını çok beğendim.Keşke Amerikada\'da böyle bir hizmet olsaydı. ', '0'),
(2, 'Sara', 'Wilsson', 'assets/img/testimonials/testimonials-2.jpg', 'Designer', 'Beynimdeki tümörü erkenden tespit edebilen ve bu sayede hayatımı kurtaran BrainSoup Web Asistanına çok teşekkür ederim.\r\n', '0'),
(3, 'Jena', 'Karlis', 'assets/img/testimonials/testimonials-3.jpg', 'Doctor', 'BrainSoup Web Asistanını yardımıyla hastalarıma en hızlı ve en doğru teshişi koyuyorum\r\n', '0'),
(4, 'Test', 'Test', 'AI4H_Heart_16x9.jpg', 'Test', ' ', '0');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `slide`
--

CREATE TABLE `slide` (
  `id` int(11) NOT NULL,
  `image1` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `image2` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `image3` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `image4` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `image5` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `image6` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `image7` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL,
  `image8` varchar(300) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `slide`
--

INSERT INTO `slide` (`id`, `image1`, `image2`, `image3`, `image4`, `image5`, `image6`, `image7`, `image8`) VALUES
(1, 'assets/img/gallery/gallery-1.jpg', 'assets/img/gallery/gallery-2.jpg', 'assets/img/gallery/gallery-3.jpg', 'assets/img/gallery/gallery-4.jpg', 'assets/img/gallery/gallery-5.jpg', 'assets/img/gallery/gallery-6.jpg', 'assets/img/gallery/gallery-7.jpg', 'assets/img/gallery/gallery-8.jpg');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `tumor`
--

CREATE TABLE `tumor` (
  `id` int(11) NOT NULL,
  `TC` varchar(11) COLLATE utf8mb4_turkish_ci NOT NULL,
  `date` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `imgloc` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `tumorloc` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `doctor` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `result` varchar(10) COLLATE utf8mb4_turkish_ci NOT NULL,
  `cinsiyet` varchar(10) COLLATE utf8mb4_turkish_ci NOT NULL,
  `birthdate` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ban` varchar(1) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `tumor`
--

INSERT INTO `tumor` (`id`, `TC`, `date`, `imgloc`, `tumorloc`, `doctor`, `result`, `cinsiyet`, `birthdate`, `ban`) VALUES
(1, '12345678901', '1980-06-01', 'yok', 'yok', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Negatif', 'Erkek', '1980-06-01', '1'),
(2, '11111213231', '2020-01-19', '', '', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Negatif', 'Erkek', '2012-01-19', '0'),
(3, '11111213238', '2020-12-16', '', '', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Pozitif', 'Erkek', '1990-12-16', '0'),
(4, '82345678901', '2020-12-16', '', '', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Negatif', 'Kadın', '1960-12-16', '0'),
(5, '92345678901', '2020-06-18', '', '', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Pozitif', 'Kadın', '1954-06-18', '1'),
(6, '98345678901', '2020-07-15', '', '', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Pozitif', 'Erkek', '1950-07-15', '0'),
(7, '99345678901', '2020-06-18', '', '', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Negatif', 'Kadın', '2000-06-18', '0'),
(8, '92345978901', '2020-10-05', '', '', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Pozitif', 'Erkek', '1970-10-05', '0'),
(9, '92945678908', '2020-12-08', '', '', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Pozitif', 'Erkek', '1960-12-08', '0'),
(10, '78375678901', '2020-10-05', '', '', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Pozitif', 'Kadın', '1965-10-05', '0'),
(11, '12345678901', '2021-01-02', 'uploads/input/be0f15fe0b9367838ba8fac61e25e43ff97c11e155673766fd0013458aceb59e.jpg', 'uploads/output/no/be0f15fe0b9367838ba8fac61e25e43ff97c11e155673766fd0013458aceb59e.jpg', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Negatif', 'Erkek', '1980-06-01', '0'),
(12, '92345678901', '2021-01-05', 'uploads/input/dc98e6bbe7a61b3cc0535ac6a78cb41a74fb95c273bcf4ed5819e4a4ba5754fc.jpg', 'uploads/output/yes/dc98e6bbe7a61b3cc0535ac6a78cb41a74fb95c273bcf4ed5819e4a4ba5754fc.jpg', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Pozitif', 'Kadın', '1954-06-18', '0'),
(13, '12345678901', '2021-01-05', 'uploads/input/020755eb58806f35c1d1997f8c8494f72dcc51353b88bfeaeea159f0d2aaa02d.jpg', 'uploads/output/yes/020755eb58806f35c1d1997f8c8494f72dcc51353b88bfeaeea159f0d2aaa02d.jpg', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Pozitif', 'Erkek', '1980-06-01', '0'),
(14, '00000000000', '2021-01-07', 'uploads/input/7414154ec5cbc831332d65e16365122299cccb23cf14b729d54ed1e5dfd67d14.png', 'uploads/output/yes/7414154ec5cbc831332d65e16365122299cccb23cf14b729d54ed1e5dfd67d14.jpg', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', 'Pozitif', '', '', '0');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(75) COLLATE utf8mb4_turkish_ci NOT NULL,
  `surname` varchar(75) COLLATE utf8mb4_turkish_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_turkish_ci NOT NULL,
  `password` varchar(150) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ban` varchar(1) COLLATE utf8mb4_turkish_ci NOT NULL,
  `user_auth` varchar(80) COLLATE utf8mb4_turkish_ci NOT NULL,
  `admin` varchar(1) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `name`, `surname`, `email`, `password`, `ban`, `user_auth`, `admin`) VALUES
(1, 'Uğur', 'Ilgın', 'ugurilgin94@gmail.com', 'e10adc3949ba59abbe56e057f20f883e', '0', '4277344e78d34f4f80b2e344599e24b168a71fb496d5e178d6e02785bf7ab2d8', '1'),
(3, 'Mehmet', 'Öz', 'mehmeto@zgmail.com', '827ccb0eea8a706c4c34a16891f84e7b', '0', 'b0933a4b83aa8c22bbaaa83b01d9ba5e478f981ea2e8051b1d033e28d3a810f4', '0'),
(4, 'Uğur', 'Ilgın', 'ugurilgin@yandex.com', 'e10adc3949ba59abbe56e057f20f883e', '0', 'e2a9655f622656e014c8a0602ba909cc4cf2e1c0c40d8de8d6bc98a864c5aaa9', '0'),
(5, 'test', 'Dr', 'test@tst.com', '827ccb0eea8a706c4c34a16891f84e7b', '0', 'b069265f43c95ba0d6341f0dff456410eaaf1fba89340cdd2cf2404564f872d9', '0'),
(6, 'Brain', 'Soup', 'brain@gmail.com', 'e10adc3949ba59abbe56e057f20f883e', '0', '87c6c3b1a03406d2a334dbe7cfda14c8518c68af9eda8f9713e2964d9ad512e9', '0'),
(7, '<script>alert(1);</script>', '\'><script>alert(1);</script>', 'ass@aa.com', '827ccb0eea8a706c4c34a16891f84e7b', '0', 'c355cba7421fc254ac6e3ee0f8179ce78da511a2a9727bf51fb5d9fbdd4a8051', '0'),
(8, 'Doktor', 'House', 'drhouse@dr.com', '827ccb0eea8a706c4c34a16891f84e7b', '1', '1203d644519218a3a537764f053bed54b3eee0a0ec441e108321bdc4952c508a', '0'),
(9, 'Yeni', 'Kullanıcı', 'yeni@kullanici.com', 'e10adc3949ba59abbe56e057f20f883e', '0', '22a2bd8ffbd761adfbcd0d125d50b3af62a43fbe883f3cd7526ee635c4c30194', '0'),
(10, 'Uğur Ilgın', ' Ilgın', 'sfsdfsf@dfsa.com', 'e10adc3949ba59abbe56e057f20f883e', '0', '8b67d2a0c1187cb29f77a121a34b5e2db1c729d610e489fbb46a5543da00f4dd', '0');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `whous`
--

CREATE TABLE `whous` (
  `id` int(11) NOT NULL,
  `title` varchar(250) COLLATE utf8mb4_turkish_ci NOT NULL,
  `detail` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `title2` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `detail2` varchar(400) COLLATE utf8mb4_turkish_ci NOT NULL,
  `title3` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `detail3` varchar(400) COLLATE utf8mb4_turkish_ci NOT NULL,
  `title4` varchar(125) COLLATE utf8mb4_turkish_ci NOT NULL,
  `detail4` varchar(400) COLLATE utf8mb4_turkish_ci NOT NULL,
  `videolink` varchar(500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `image` varchar(250) COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `whous`
--

INSERT INTO `whous` (`id`, `title`, `detail`, `title2`, `detail2`, `title3`, `detail3`, `title4`, `detail4`, `videolink`, `image`) VALUES
(1, 'Hakkımızda', 'BrainSoup Web Asistanı olarak doktorların iş yoğunluklarına yardımcı olmak ve hastalarının erken tanı sisteminden faydalanabilmesi için yapay zeka sistemi geliştirdik.Geliştirdiğimiz yapay zeka sistemi yardımıyla sizlere en iyi sağlık hizmetini sunmaktan onur duyarız', 'Yapay Zeka', 'Beyin Tümörü alanında yapay zeka sistemiyle doktorlarımıza yardımcı oluyoruz.', 'Sağlık', 'Sağlığınızı sizden bile daha iyi koruyoruz.', 'Bulut Desteği', 'En iyi serverlarda en hızlı desteği sağlıyoruz.', 'https://www.youtube.com/watch?v=6iUJfwB1kEk', '');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `about`
--
ALTER TABLE `about`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Tablo için indeksler `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `email`
--
ALTER TABLE `email`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `referance`
--
ALTER TABLE `referance`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `slide`
--
ALTER TABLE `slide`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `tumor`
--
ALTER TABLE `tumor`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Tablo için indeksler `whous`
--
ALTER TABLE `whous`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `about`
--
ALTER TABLE `about`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `email`
--
ALTER TABLE `email`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Tablo için AUTO_INCREMENT değeri `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Tablo için AUTO_INCREMENT değeri `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Tablo için AUTO_INCREMENT değeri `referance`
--
ALTER TABLE `referance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Tablo için AUTO_INCREMENT değeri `slide`
--
ALTER TABLE `slide`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `tumor`
--
ALTER TABLE `tumor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Tablo için AUTO_INCREMENT değeri `whous`
--
ALTER TABLE `whous`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
