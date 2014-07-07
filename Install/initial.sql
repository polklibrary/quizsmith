-- phpMyAdmin SQL Dump
-- version 2.11.8.1
-- http://www.phpmyadmin.net
--
-- Host: uwosh.edu
-- Generation Time: Jul 02, 2014 at 09:10 AM
-- Server version: 5.0.95
-- PHP Version: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `quizsmith`
--

-- --------------------------------------------------------

--
-- Table structure for table `answers`
--

CREATE TABLE IF NOT EXISTS `answers` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `question_sets_id` int(11) unsigned NOT NULL,
  `answer` varchar(255) collate utf8_unicode_ci NOT NULL,
  `is_correct` tinyint(1) default '0',
  `position` int(2) NOT NULL default '98',
  PRIMARY KEY  (`id`),
  KEY `FK_ANSWERGROUPS` (`question_sets_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=97 ;

--
-- Dumping data for table `answers`
--

INSERT INTO `answers` (`id`, `question_sets_id`, `answer`, `is_correct`, `position`) VALUES
(1, 1, 'Nile - Kagera', 1, 98),
(2, 1, 'Amazon - Ucayali - ApurÃ­mac', 0, 98),
(3, 1, 'Yangtze', 0, 98),
(4, 1, 'Mississippi-Missouri-Jefferson', 0, 98),
(5, 2, 'China', 1, 98),
(6, 2, 'India', 0, 98),
(7, 2, 'United States', 0, 98),
(8, 2, 'Indonesia', 0, 98),
(9, 3, 'Russia', 1, 98),
(10, 3, 'China', 0, 98),
(11, 3, 'Canada', 0, 98),
(12, 3, 'United States', 0, 98),
(13, 4, 'Singapore', 1, 98),
(14, 4, 'Bahrain', 0, 98),
(15, 4, 'Bangladesh', 0, 98),
(16, 5, 'Shanghai, China', 1, 98),
(17, 5, 'Lagos, Nigeria', 0, 98),
(18, 5, 'Karachi, Pakistan', 0, 98),
(19, 5, 'Istanbul, Turkey', 0, 98),
(20, 6, 'Chile', 1, 98),
(21, 6, 'Argentina', 0, 98),
(22, 6, 'Australia', 0, 98),
(23, 6, 'New Zealand', 0, 98),
(24, 7, 'Kirabati', 1, 98),
(25, 7, 'Tonga', 0, 98),
(26, 7, 'Samoa', 0, 98),
(27, 7, 'Chile', 0, 98),
(28, 8, 'Malaysia', 1, 98),
(29, 8, 'Uganda', 0, 98),
(30, 8, 'Indonesia', 0, 98),
(31, 8, 'Ecuador', 0, 98),
(32, 8, 'Colombia', 0, 98),
(33, 8, 'Somalia', 0, 98),
(34, 9, 'Pacific Ocean', 1, 98),
(35, 9, 'Atlantic Ocean', 0, 98),
(36, 9, 'Indian Ocean', 0, 98),
(37, 9, 'Southern Ocean', 0, 98),
(38, 10, 'False', 1, 98),
(39, 10, 'True', 0, 98),
(40, 11, 'True', 1, 98),
(41, 11, 'False', 0, 98),
(42, 12, 'Sydney, Australia', 1, 98),
(43, 12, 'Alexandria, Egypt', 0, 98),
(44, 12, 'Buenos Aires, Argentina', 0, 98),
(45, 12, 'Sofia, Bulgaria', 0, 98),
(46, 13, 'China', 1, 98),
(47, 13, 'South Africa', 0, 98),
(48, 13, 'Nepal', 0, 98),
(49, 13, 'Guatemala', 0, 98),
(50, 14, 'India', 1, 98),
(51, 14, 'Pakistan', 0, 98),
(52, 14, 'Bangladesh', 0, 98),
(53, 14, 'Iran', 0, 98),
(54, 15, 'Jordan', 1, 98),
(55, 15, 'Syria', 0, 98),
(56, 15, 'Lebanon', 0, 98),
(57, 15, 'Israel', 0, 98),
(58, 15, 'Egypt', 0, 98);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `name` varchar(255) collate utf8_unicode_ci NOT NULL,
  `category_intro` text collate utf8_unicode_ci NOT NULL,
  `can_anonymous_view_intro` tinyint(1) default '0',
  `playable_questions` int(11) unsigned NOT NULL,
  `question_time_allowed` int(11) default '30',
  `wrong_answer_time_penalty` int(11) default '15',
  `max_wrong_answer_allowed` int(11) default '2',
  `transition_in` int(11) unsigned NOT NULL,
  `transition_out` int(11) unsigned NOT NULL,
  `position` int(2) unsigned NOT NULL,
  `d2l_folder` varchar(255) collate utf8_unicode_ci NOT NULL,
  `assessments` text collate utf8_unicode_ci NOT NULL,
  `created` timestamp NOT NULL default '0000-00-00 00:00:00',
  `modified` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`),
  KEY `FK_IN_TRANSITIONS` (`transition_in`),
  KEY `FK_OUT_TRANSITIONS` (`transition_out`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `category_intro`, `can_anonymous_view_intro`, `playable_questions`, `question_time_allowed`, `wrong_answer_time_penalty`, `max_wrong_answer_allowed`, `transition_in`, `transition_out`, `position`, `d2l_folder`, `assessments`, `created`, `modified`) VALUES
(1, 'World Geography Trivia', '<h1>How well do you know world geography? &nbsp;</h1>\r\n<p>This quiz tests your knowledge of <a href="https://flic.kr/p/8FnV8" target="_blank" style="float: right;"> <img src="https://farm1.staticflickr.com/43/86898565_563dab2319_m.jpg" width="240" height="219" /> <br />https://flic.kr/p/8FnV8</a></p>\r\n<ul>\r\n<li>Countries &amp; Cities</li>\r\n<li>Oceans &amp; Rivers</li>\r\n<li>Landmarks</li>\r\n</ul>\r\n<p style="text-align: left;">(This is a demo content module. &nbsp;All text content is drawn from Wikipedia and licensed under Creative Commons Attribute-ShareAlike. &nbsp;All photos are from Flickr and licensed under various Creative Commons terms.)</p>\r\n<p style="text-align: left;"></p>', 0, 5, 30, 5, 2, 1, 1, 99, '', '[{"start": 85, "end": 100, "id": "85-100", "text": "Wow, you are a geography pro!"}, {"start": 70, "end": 85, "id": "70-85", "text": "Nice job!"}, {"start": 50, "end": 70, "id": "50-70", "text": "That''s a start, but you could do better!"}, {"start": 0, "end": 50, "id": "0-50", "text": "Not so good...have you ever seen a globe?"}]', '2014-03-13 11:34:23', '2014-03-14 13:54:56');

-- --------------------------------------------------------

--
-- Table structure for table `categories_local_groups`
--

CREATE TABLE IF NOT EXISTS `categories_local_groups` (
  `associated_table_id` int(11) unsigned NOT NULL,
  `groups_id` int(11) unsigned NOT NULL,
  `play` tinyint(1) NOT NULL default '0',
  `edit` tinyint(1) NOT NULL default '0',
  `review` tinyint(4) NOT NULL default '0',
  PRIMARY KEY  (`associated_table_id`,`groups_id`),
  KEY `FK_CG_GROUPS` (`groups_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `categories_local_groups`
--

INSERT INTO `categories_local_groups` (`associated_table_id`, `groups_id`, `play`, `edit`, `review`) VALUES
(1, 1, 1, 1, 0),
(1, 2, 1, 1, 0),
(1, 3, 1, 1, 0),
(1, 4, 1, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE IF NOT EXISTS `groups` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `name` varchar(25) collate utf8_unicode_ci default NULL,
  `description` varchar(55) collate utf8_unicode_ci default NULL,
  `play` tinyint(1) NOT NULL default '0',
  `edit` tinyint(1) NOT NULL default '0',
  `review` tinyint(4) NOT NULL default '0',
  `use_admin_panel` tinyint(1) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=6 ;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`id`, `name`, `description`, `play`, `edit`, `review`, `use_admin_panel`) VALUES
(1, 'Administrators', 'Group for site administrators.', 1, 1, 1, 1),
(2, 'Global Editor', 'Group for editors of all content.', 1, 1, 0, 0),
(3, 'Players', 'Group for trivia players.', 1, 0, 0, 0),
(4, 'Test Player', 'Group for editors to test as players.', 1, 0, 0, 0),
(5, 'Example Sub-Editor', 'Example of a specific category editor', 0, 1, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `groups_assignments`
--

CREATE TABLE IF NOT EXISTS `groups_assignments` (
  `groups_id` int(11) NOT NULL,
  `categories_id` int(11) NOT NULL,
  KEY `FK_GA_GROUPS` (`groups_id`),
  KEY `FK_GA_CATEGORIES` (`categories_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `groups_assignments`
--


-- --------------------------------------------------------

--
-- Table structure for table `properties`
--

CREATE TABLE IF NOT EXISTS `properties` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `prop_name` varchar(55) collate utf8_unicode_ci NOT NULL,
  `prop_value` text collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=11 ;

--
-- Dumping data for table `properties`
--

INSERT INTO `properties` (`id`, `prop_name`, `prop_value`) VALUES
(1, 'ACTIVE_THEME', 'ANVIL'),
(2, 'MAILER_TO_SUBJECT', 'ANVIL - ${CATEGORY} - Submission'),
(3, 'MAILER_GLOBAL_FROM_ADDRESS', 'librarytechnology@uwosh.edu'),
(4, 'MAILER_FEEDBACK_ADDRESS', 'librarytechnology@uwosh.edu'),
(5, 'MAILER_BODY', 'Attached is your Submission'),
(6, 'LEADERBOARD_ARCHIVE_DATE', '2013-8-13'),
(7, 'ANALYTICS', ''),
(8, 'MAILER_HELP_ADDRESS', 'librarytechnology@uwosh.edu'),
(9, 'CREDITS', '[{"type": "title", "id": 0, "value": "Information Literacy Librarian"}, {"type": "name", "id": 1, "value": "Ted Mulvey "}, {"type": "email", "id": 2, "value": "mulveyt@uwosh.edu"}, {"type": "title", "id": 3, "value": "Web Developer"}, {"type": "name", "id": 4, "value": "David Hietpas"}, {"type": "email", "id": 5, "value": "hietpasd@uwosh.edu"}, {"type": "title", "id": 6, "value": "Module Creators"}, {"type": "name", "id": 7, "value": "Erin McArthur"}, {"type": "name", "id": 8, "value": "Ted Mulvey"}, {"type": "title", "id": 9, "value": "The Think Tank"}, {"type": "name", "id": 10, "value": "Jeff Brunner"}, {"type": "name", "id": 11, "value": "Crystal Buss"}, {"type": "name", "id": 12, "value": "Marisa Finkey"}, {"type": "name", "id": 13, "value": "Stephen Katz"}, {"type": "name", "id": 14, "value": "Maccabee Levine"}, {"type": "name", "id": 15, "value": "Erin McArthur"}, {"type": "name", "id": 16, "value": "Sarah Neises"}, {"type": "name", "id": 17, "value": "Joshua Ranger"}, {"type": "title", "id": 18, "value": "Special Thank You"}, {"type": "name", "id": 19, "value": "Sam Looker"}, {"type": "name", "id": 20, "value": "Dan Petersen"}, {"type": "name", "id": 21, "value": "T. Kim Nguyen"}, {"type": "title", "id": 22, "value": "University of Wisconsin Oshkosh"}, {"type": "name", "id": 23, "value": "Polk Library"}]'),
(10, 'LEADERBOARD_HOF', '[{"index": 0, "players": [{"index": 0, "score": "9393", "name": "Amazin_Nate"}, {"index": 1, "score": "9003", "name": "CatCrazy"}, {"index": 2, "score": "8797", "name": "Jordan"}, {"index": 3, "score": "4454", "name": "Swaggy"}], "title": "Fall 2013"}]');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE IF NOT EXISTS `questions` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `question_sets_id` int(11) unsigned NOT NULL,
  `question` text collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `FK_QUESTIONGROUPS` (`question_sets_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=31 ;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `question_sets_id`, `question`) VALUES
(1, 1, '<p>What is the longest river in the world?</p>'),
(2, 2, '<p>What country has the largest population?</p>'),
(3, 2, '<p>More people live in this country than any other:</p>'),
(4, 3, '<p>What''s the largest country by area?</p>'),
(5, 3, '<p>This is the largest country in the world, with an area greater than 17 million square kilometers.</p>'),
(6, 4, '<p>What country with over 1 million residents has the greatest population density?</p>'),
(7, 5, '<p>What is the largest city in the world, defined by population?</p>'),
(8, 5, '<p>What is the largest city proper, defined by population?</p>'),
(9, 6, '<p>Which of the following countries has the southernmost point on land?</p>'),
(10, 6, '<p>Which of these countries'' land streches the farthest south?</p>'),
(11, 7, '<p>What country has the westernmost point on land in the southern hemisphere?</p>'),
(12, 8, '<p>Which of the following countries does the Equator *not* pass through?</p>'),
(13, 9, '<p>Which ocean features the Mariana Trench, the deepest part of the world''s oceans?</p>'),
(14, 9, '<p>The Mariana Trench, the deepest part of the world''s oceans, is located in:</p>'),
(15, 10, '<p>True or false: the Sargasso Sea is a region in the Pacific Ocean.</p>'),
(16, 11, '<p>True or false: there are over 10 countries that begin with the letter ''A''.</p>'),
(17, 12, '<p><img src="http://farm3.staticflickr.com/2123/2278915446_295864dbe3.jpg" width="451" height="300" style="margin-left: auto; margin-right: auto; display: block;" /></p>\r\n<p>https://flic.kr/p/4to3aC</p>\r\n<p>This building is located in:</p>'),
(18, 13, '<p><img src="http://farm8.staticflickr.com/7363/10129737315_24a15bf7b3.jpg" width="500" height="333" style="margin-left: auto; margin-right: auto; display: block;" /></p>\r\n<p>https://flic.kr/p/gr8xZn</p>\r\n<p></p>\r\n<p>This structure is located in:</p>'),
(19, 14, '<p><img src="http://farm3.staticflickr.com/2665/3954851233_4beb2f6d07.jpg" width="401" height="300" style="margin-left: auto; margin-right: auto; display: block;" /></p>\r\n<p>https://flic.kr/p/72tDue</p>\r\n<p>This monument is located in:</p>\r\n<p></p>'),
(20, 15, '<p><img src="http://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Al_Khazneh.jpg/384px-Al_Khazneh.jpg" width="241" height="300" style="margin-left: auto; margin-right: auto; display: block;" /></p>\r\n<p>http://en.wikipedia.org/wiki/File:Al_Khazneh.jpg</p>\r\n<p>Petra, an archaeological city featured (fictionally) in Indiana Jones and the Last Crusade, is located in:</p>');

-- --------------------------------------------------------

--
-- Table structure for table `question_sets`
--

CREATE TABLE IF NOT EXISTS `question_sets` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `category_id` int(11) unsigned NOT NULL,
  `answer_help` text collate utf8_unicode_ci NOT NULL,
  `created` timestamp NOT NULL default '0000-00-00 00:00:00',
  `modified` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`),
  KEY `FK_CATEGORIES` (`category_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=27 ;

--
-- Dumping data for table `question_sets`
--

INSERT INTO `question_sets` (`id`, `category_id`, `answer_help`, `created`, `modified`) VALUES
(1, 1, '<p>The Nile river is 6,660 km (4,132 miles) in length. &nbsp;The Amazon (6,400 km), Yangtze (6,300 km) and Mississippi (6,275 km) are slightly shorter.</p>\r\n<p>http://en.wikipedia.org/wiki/List_of_rivers_by_length</p>', '2014-03-13 11:44:52', '2014-03-13 11:44:52'),
(2, 1, '<p>Over 1.3 billion people live in China. &nbsp;India is a close second with over 1.2 billion. &nbsp;The United States and Indonesia have populations of 317 million and 250 million respectively.</p>\r\n<p>Source:&nbsp;http://en.wikipedia.org/wiki/List_of_countries_by_population (accessed on March 13, 2014).</p>', '2014-03-13 11:55:46', '2014-03-13 11:55:46'),
(3, 1, '<p>Russia, at over 17 million kilometers squared, is the largest country in the world. &nbsp;Canada, China and the United States each have between 9 and 10 million.</p>\r\n<p>Source: http://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area</p>\r\n<p>&nbsp;</p>', '2014-03-13 11:59:12', '2014-03-13 11:59:12'),
(4, 1, '<p>Singapore, with 5.4 million residents, has the highest population density (among countries with population above one million), at 7,669 per square kilometer. &nbsp;</p>', '2014-03-13 12:05:10', '2014-03-13 12:05:10'),
(5, 1, '<p>Shanghai is the world''s largest "city proper" as defined by Wikipedia, with a population over 17.8 million. &nbsp;Lagos, Karachi and Istanbul are the next three largest by population.</p>\r\n<p>Source:&nbsp;http://en.wikipedia.org/wiki/List_of_cities_proper_by_population</p>', '2014-03-13 12:11:24', '2014-03-13 12:11:24'),
(6, 1, '<p>Chile reaches a southernmost latitude of 56&deg;30'' south, the farthest south of any country.</p>', '2014-03-13 12:15:52', '2014-03-13 12:15:52'),
(7, 1, '<p>Kiribati''s Banaba Island has a westernmost longitude of 169&deg;32''13"E, the farthest in west in the southern hemisphere.</p>', '2014-03-13 12:21:23', '2014-03-13 12:21:23'),
(8, 1, '<p>Malaysia is just north of the Equator; its southernmost point is Cape Piai at 1&deg;16'' N.</p>\r\n<p>Sources:&nbsp;</p>\r\n<p>http://en.wikipedia.org/wiki/Equator#Equatorial_countries_and_territories</p>\r\n<p>http://en.wikipedia.org/wiki/Extreme_points_of_Asia</p>', '2014-03-13 15:12:02', '2014-03-13 15:12:02'),
(9, 1, '<p>The Mariana Trench is located east of Guam in the Pacific Ocean.</p>', '2014-03-13 15:14:51', '2014-03-13 15:14:51'),
(10, 1, '<p>The Sargasso Sea is a region in the North Atlantic Ocean.</p>\r\n<p>Source:&nbsp;http://en.wikipedia.org/wiki/Sargasso_Sea</p>', '2014-03-13 15:23:48', '2014-03-13 15:23:48'),
(11, 1, '<p>There are twelve countries (plus six terratorial dependencies) that begin with the letter A.</p>\r\n<p>http://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area</p>', '2014-03-13 15:26:58', '2014-03-13 15:26:58'),
(12, 1, '<p>The Sydney Opera House is located in Sydney, Australia. &nbsp;The other cities all house opera houses as well.</p>\r\n<p>http://en.wikipedia.org/wiki/Sydney_Opera_House</p>\r\n<p>http://en.wikipedia.org/wiki/List_of_opera_houses</p>\r\n<p>https://flic.kr/p/4to3aC</p>\r\n<p></p>', '2014-03-13 15:35:45', '2014-03-13 15:35:45'),
(13, 1, '<p>The Great Wall of China measures over 21,000 km, including all of its branches. &nbsp;Construction began in the 7th century BC.</p>\r\n<p>http://en.wikipedia.org/wiki/Great_Wall_of_China</p>\r\n<p>https://flic.kr/p/gr8xZn</p>', '2014-03-13 15:41:44', '2014-03-13 15:41:44'),
(14, 1, '<p>The Taj Mahal is a mausoleum located in Agra, India.</p>\r\n<p>http://en.wikipedia.org/wiki/Taj_Mahal</p>\r\n<p>https://flic.kr/p/72tDue</p>', '2014-03-13 15:45:03', '2014-03-13 15:45:03'),
(15, 1, '<p>Petra, in Jordan, was possibly built as early as 300 BCE.</p>\r\n<p>Source: http://en.wikipedia.org/wiki/Petra</p>', '2014-03-13 15:50:42', '2014-03-13 15:50:42');

-- --------------------------------------------------------

--
-- Table structure for table `tests`
--

CREATE TABLE IF NOT EXISTS `tests` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `alias` varchar(25) collate utf8_unicode_ci default NULL,
  `category` varchar(255) collate utf8_unicode_ci NOT NULL,
  `d2l_folder` varchar(255) collate utf8_unicode_ci NOT NULL,
  `completed` tinyint(1) default '0',
  `total_percentage` float NOT NULL,
  `base_competitive` int(11) NOT NULL,
  `bonus_competitive` int(11) NOT NULL,
  `total_competitive` int(11) NOT NULL,
  `time_remaining` float NOT NULL,
  `time_spent` float NOT NULL,
  `question_time_allowed` int(11) NOT NULL,
  `wrong_answer_time_penalty` int(11) NOT NULL,
  `max_wrong_answer_allowed` int(11) NOT NULL,
  `used_accessibility_view` tinyint(1) default '0',
  `created` timestamp NOT NULL default '0000-00-00 00:00:00',
  `modified` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=32 ;

--
-- Dumping data for table `tests`
--


-- --------------------------------------------------------

--
-- Table structure for table `tests_results`
--

CREATE TABLE IF NOT EXISTS `tests_results` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `tests_id` int(11) unsigned NOT NULL,
  `question_sets_id` int(11) unsigned NOT NULL,
  `question` text collate utf8_unicode_ci NOT NULL,
  `correctly_answered` tinyint(1) default '0',
  `wrong_attempts` int(11) NOT NULL,
  `duration` float NOT NULL,
  `answer_choices` text collate utf8_unicode_ci NOT NULL,
  `attempted` tinyint(1) default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_TR_TESTS` (`tests_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=181 ;

--
-- Dumping data for table `tests_results`
--


-- --------------------------------------------------------

--
-- Table structure for table `transitions`
--

CREATE TABLE IF NOT EXISTS `transitions` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `name` varchar(55) collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=10 ;

--
-- Dumping data for table `transitions`
--

INSERT INTO `transitions` (`id`, `name`) VALUES
(1, 'Random'),
(2, 'Slide Left'),
(3, 'Slide Right'),
(4, 'Slide Up'),
(5, 'Slide Down'),
(6, 'Blinds'),
(7, 'Implode|Explode'),
(8, 'Fade In|Out'),
(9, 'Inflate|Deflate');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `is_local` tinyint(1) default '0',
  `email` varchar(25) collate utf8_unicode_ci default NULL,
  `password` varchar(255) collate utf8_unicode_ci default NULL,
  `fullname` varchar(55) collate utf8_unicode_ci default NULL,
  `alias` varchar(25) collate utf8_unicode_ci default NULL,
  `current_test` int(11) NOT NULL,
  `current_question` int(11) NOT NULL,
  `needs_accessibility` tinyint(1) NOT NULL default '0',
  `last_active` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `alias` (`alias`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=14 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `is_local`, `email`, `password`, `fullname`, `alias`, `current_test`, `current_question`, `needs_accessibility`, `last_active`) VALUES
(1, 1, 'admin@test.com', 'db14b0f8d5648b050798c34719946c395c325e5efc459079e0d78773fe76151e10d30f957c03a1c6', NULL, 'ExampleAdmin', 30, 19, 0, '2014-07-02 09:08:56'),
(2, 1, 'editor@test.com', '270b3c246f33adb5745d48dd3e24ca1e728189a7e1c304e9e6c5a022f6390d55757645fec9003305', NULL, 'ExampleEditor', 17, 15, 0, '2014-06-04 07:51:14');

-- --------------------------------------------------------

--
-- Table structure for table `users_groups`
--

CREATE TABLE IF NOT EXISTS `users_groups` (
  `users_id` int(11) unsigned NOT NULL,
  `groups_id` int(11) unsigned NOT NULL,
  PRIMARY KEY  (`users_id`,`groups_id`),
  KEY `FK_UG_GROUPS` (`groups_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `users_groups`
--

INSERT INTO `users_groups` (`users_id`, `groups_id`) VALUES
(1, 1),
(2, 2),
(1, 3),
(2, 3);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `answers`
--
ALTER TABLE `answers`
  ADD CONSTRAINT `FK_ANSWERGROUPS` FOREIGN KEY (`question_sets_id`) REFERENCES `question_sets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `FK_IN_TRANSITIONS` FOREIGN KEY (`transition_in`) REFERENCES `transitions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_OUT_TRANSITIONS` FOREIGN KEY (`transition_out`) REFERENCES `transitions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `categories_local_groups`
--
ALTER TABLE `categories_local_groups`
  ADD CONSTRAINT `FK_CG_CATEGORIES` FOREIGN KEY (`associated_table_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_CG_GROUPS` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `FK_QUESTIONGROUPS` FOREIGN KEY (`question_sets_id`) REFERENCES `question_sets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `question_sets`
--
ALTER TABLE `question_sets`
  ADD CONSTRAINT `FK_CATEGORIES` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tests_results`
--
ALTER TABLE `tests_results`
  ADD CONSTRAINT `FK_TR_TESTS` FOREIGN KEY (`tests_id`) REFERENCES `tests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `users_groups`
--
ALTER TABLE `users_groups`
  ADD CONSTRAINT `FK_UG_GROUPS` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_UG_USERS` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
