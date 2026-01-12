/*
 Navicat Premium Dump SQL

 Source Server         : 101.126.23.137-火山服务器
 Source Server Type    : MySQL
 Source Server Version : 80405 (8.4.5)
 Source Host           : 101.126.23.137:3306
 Source Schema         : djangoblog

 Target Server Type    : MySQL
 Target Server Version : 80405 (8.4.5)
 File Encoding         : 65001

 Date: 10/12/2025 09:43:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for accounts_bloguser
-- ----------------------------
DROP TABLE IF EXISTS `accounts_bloguser`;
CREATE TABLE `accounts_bloguser`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `creation_time` datetime(6) NOT NULL,
  `last_modify_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts_bloguser
-- ----------------------------
INSERT INTO `accounts_bloguser` VALUES (1, 'pbkdf2_sha256$1000000$sroq0g0rmuDIKUFCKWOSUG$Fi4AvEXvYKu86vaIT+u7rlj8CB+69P1dSQqCt+6EBF8=', '2025-11-29 18:46:53.733603', 1, 'admin', '', '', 'beckzhang@qq.com', 1, 1, '2025-11-29 16:29:30.188077', '', '', '2025-11-29 16:29:30.188077', '2025-11-29 16:29:30.188077');
INSERT INTO `accounts_bloguser` VALUES (2, 'pbkdf2_sha256$1000000$DmMi5lXMo5wUaX0ZcuBtmM$f4fIdmuL2FDzmOMIaJl1cfieEJmwBwJzLRTWJIbllCs=', NULL, 0, '测试用户', '', '', 'test@test.com', 0, 1, '2025-11-29 16:29:41.020015', '', '', '2025-11-29 16:29:41.020015', '2025-11-29 16:29:41.020015');
INSERT INTO `accounts_bloguser` VALUES (4, '!ZaPUE1IoZxJBnKwZmCm5jxM1AEBssgdy7C59Orsz', NULL, 1, 'newadmin', '', '', 'newadmin@example.com', 1, 1, '2025-11-29 23:44:12.557910', '', '', '2025-11-29 23:44:12.557910', '2025-11-29 23:44:12.557910');

-- ----------------------------
-- Table structure for accounts_bloguser_groups
-- ----------------------------
DROP TABLE IF EXISTS `accounts_bloguser_groups`;
CREATE TABLE `accounts_bloguser_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bloguser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `accounts_bloguser_groups_bloguser_id_group_id_fc37e89b_uniq`(`bloguser_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `accounts_bloguser_groups_group_id_98d76804_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `accounts_bloguser_gr_bloguser_id_a16ccbb7_fk_accounts_` FOREIGN KEY (`bloguser_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `accounts_bloguser_groups_group_id_98d76804_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts_bloguser_groups
-- ----------------------------

-- ----------------------------
-- Table structure for accounts_bloguser_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `accounts_bloguser_user_permissions`;
CREATE TABLE `accounts_bloguser_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bloguser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `accounts_bloguser_user_p_bloguser_id_permission_i_14808777_uniq`(`bloguser_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `accounts_bloguser_us_permission_id_ae5159b9_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `accounts_bloguser_us_bloguser_id_7e1b5742_fk_accounts_` FOREIGN KEY (`bloguser_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `accounts_bloguser_us_permission_id_ae5159b9_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts_bloguser_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 105 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add site', 6, 'add_site');
INSERT INTO `auth_permission` VALUES (22, 'Can change site', 6, 'change_site');
INSERT INTO `auth_permission` VALUES (23, 'Can delete site', 6, 'delete_site');
INSERT INTO `auth_permission` VALUES (24, 'Can view site', 6, 'view_site');
INSERT INTO `auth_permission` VALUES (25, 'Can add Website configuration', 7, 'add_blogsettings');
INSERT INTO `auth_permission` VALUES (26, 'Can change Website configuration', 7, 'change_blogsettings');
INSERT INTO `auth_permission` VALUES (27, 'Can delete Website configuration', 7, 'delete_blogsettings');
INSERT INTO `auth_permission` VALUES (28, 'Can view Website configuration', 7, 'view_blogsettings');
INSERT INTO `auth_permission` VALUES (29, 'Can add link', 8, 'add_links');
INSERT INTO `auth_permission` VALUES (30, 'Can change link', 8, 'change_links');
INSERT INTO `auth_permission` VALUES (31, 'Can delete link', 8, 'delete_links');
INSERT INTO `auth_permission` VALUES (32, 'Can view link', 8, 'view_links');
INSERT INTO `auth_permission` VALUES (33, 'Can add sidebar', 9, 'add_sidebar');
INSERT INTO `auth_permission` VALUES (34, 'Can change sidebar', 9, 'change_sidebar');
INSERT INTO `auth_permission` VALUES (35, 'Can delete sidebar', 9, 'delete_sidebar');
INSERT INTO `auth_permission` VALUES (36, 'Can view sidebar', 9, 'view_sidebar');
INSERT INTO `auth_permission` VALUES (37, 'Can add tag', 10, 'add_tag');
INSERT INTO `auth_permission` VALUES (38, 'Can change tag', 10, 'change_tag');
INSERT INTO `auth_permission` VALUES (39, 'Can delete tag', 10, 'delete_tag');
INSERT INTO `auth_permission` VALUES (40, 'Can view tag', 10, 'view_tag');
INSERT INTO `auth_permission` VALUES (41, 'Can add category', 11, 'add_category');
INSERT INTO `auth_permission` VALUES (42, 'Can change category', 11, 'change_category');
INSERT INTO `auth_permission` VALUES (43, 'Can delete category', 11, 'delete_category');
INSERT INTO `auth_permission` VALUES (44, 'Can view category', 11, 'view_category');
INSERT INTO `auth_permission` VALUES (45, 'Can add article', 12, 'add_article');
INSERT INTO `auth_permission` VALUES (46, 'Can change article', 12, 'change_article');
INSERT INTO `auth_permission` VALUES (47, 'Can delete article', 12, 'delete_article');
INSERT INTO `auth_permission` VALUES (48, 'Can view article', 12, 'view_article');
INSERT INTO `auth_permission` VALUES (49, 'Can add user', 13, 'add_bloguser');
INSERT INTO `auth_permission` VALUES (50, 'Can change user', 13, 'change_bloguser');
INSERT INTO `auth_permission` VALUES (51, 'Can delete user', 13, 'delete_bloguser');
INSERT INTO `auth_permission` VALUES (52, 'Can view user', 13, 'view_bloguser');
INSERT INTO `auth_permission` VALUES (53, 'Can add comment', 14, 'add_comment');
INSERT INTO `auth_permission` VALUES (54, 'Can change comment', 14, 'change_comment');
INSERT INTO `auth_permission` VALUES (55, 'Can delete comment', 14, 'delete_comment');
INSERT INTO `auth_permission` VALUES (56, 'Can view comment', 14, 'view_comment');
INSERT INTO `auth_permission` VALUES (57, 'Can add oauth配置', 15, 'add_oauthconfig');
INSERT INTO `auth_permission` VALUES (58, 'Can change oauth配置', 15, 'change_oauthconfig');
INSERT INTO `auth_permission` VALUES (59, 'Can delete oauth配置', 15, 'delete_oauthconfig');
INSERT INTO `auth_permission` VALUES (60, 'Can view oauth配置', 15, 'view_oauthconfig');
INSERT INTO `auth_permission` VALUES (61, 'Can add oauth user', 16, 'add_oauthuser');
INSERT INTO `auth_permission` VALUES (62, 'Can change oauth user', 16, 'change_oauthuser');
INSERT INTO `auth_permission` VALUES (63, 'Can delete oauth user', 16, 'delete_oauthuser');
INSERT INTO `auth_permission` VALUES (64, 'Can view oauth user', 16, 'view_oauthuser');
INSERT INTO `auth_permission` VALUES (65, 'Can add 命令', 17, 'add_commands');
INSERT INTO `auth_permission` VALUES (66, 'Can change 命令', 17, 'change_commands');
INSERT INTO `auth_permission` VALUES (67, 'Can delete 命令', 17, 'delete_commands');
INSERT INTO `auth_permission` VALUES (68, 'Can view 命令', 17, 'view_commands');
INSERT INTO `auth_permission` VALUES (69, 'Can add 邮件发送log', 18, 'add_emailsendlog');
INSERT INTO `auth_permission` VALUES (70, 'Can change 邮件发送log', 18, 'change_emailsendlog');
INSERT INTO `auth_permission` VALUES (71, 'Can delete 邮件发送log', 18, 'delete_emailsendlog');
INSERT INTO `auth_permission` VALUES (72, 'Can view 邮件发送log', 18, 'view_emailsendlog');
INSERT INTO `auth_permission` VALUES (73, 'Can add OwnTrackLogs', 19, 'add_owntracklog');
INSERT INTO `auth_permission` VALUES (74, 'Can change OwnTrackLogs', 19, 'change_owntracklog');
INSERT INTO `auth_permission` VALUES (75, 'Can delete OwnTrackLogs', 19, 'delete_owntracklog');
INSERT INTO `auth_permission` VALUES (76, 'Can view OwnTrackLogs', 19, 'view_owntracklog');
INSERT INTO `auth_permission` VALUES (77, 'Can add link', 20, 'add_link');
INSERT INTO `auth_permission` VALUES (78, 'Can change link', 20, 'change_link');
INSERT INTO `auth_permission` VALUES (79, 'Can delete link', 20, 'delete_link');
INSERT INTO `auth_permission` VALUES (80, 'Can view link', 20, 'view_link');
INSERT INTO `auth_permission` VALUES (81, 'Can add article version', 21, 'add_articleversion');
INSERT INTO `auth_permission` VALUES (82, 'Can change article version', 21, 'change_articleversion');
INSERT INTO `auth_permission` VALUES (83, 'Can delete article version', 21, 'delete_articleversion');
INSERT INTO `auth_permission` VALUES (84, 'Can view article version', 21, 'view_articleversion');
INSERT INTO `auth_permission` VALUES (85, 'Can add comment', 22, 'add_comment');
INSERT INTO `auth_permission` VALUES (86, 'Can change comment', 22, 'change_comment');
INSERT INTO `auth_permission` VALUES (87, 'Can delete comment', 22, 'delete_comment');
INSERT INTO `auth_permission` VALUES (88, 'Can view comment', 22, 'view_comment');
INSERT INTO `auth_permission` VALUES (89, 'Can add review history', 23, 'add_reviewhistory');
INSERT INTO `auth_permission` VALUES (90, 'Can change review history', 23, 'change_reviewhistory');
INSERT INTO `auth_permission` VALUES (91, 'Can delete review history', 23, 'delete_reviewhistory');
INSERT INTO `auth_permission` VALUES (92, 'Can view review history', 23, 'view_reviewhistory');
INSERT INTO `auth_permission` VALUES (93, 'Can add 审核统计', 24, 'add_moderationstatistics');
INSERT INTO `auth_permission` VALUES (94, 'Can change 审核统计', 24, 'change_moderationstatistics');
INSERT INTO `auth_permission` VALUES (95, 'Can delete 审核统计', 24, 'delete_moderationstatistics');
INSERT INTO `auth_permission` VALUES (96, 'Can view 审核统计', 24, 'view_moderationstatistics');
INSERT INTO `auth_permission` VALUES (97, 'Can add 审核队列', 25, 'add_moderationqueue');
INSERT INTO `auth_permission` VALUES (98, 'Can change 审核队列', 25, 'change_moderationqueue');
INSERT INTO `auth_permission` VALUES (99, 'Can delete 审核队列', 25, 'delete_moderationqueue');
INSERT INTO `auth_permission` VALUES (100, 'Can view 审核队列', 25, 'view_moderationqueue');
INSERT INTO `auth_permission` VALUES (101, 'Can add 审核记录', 26, 'add_moderationrecord');
INSERT INTO `auth_permission` VALUES (102, 'Can change 审核记录', 26, 'change_moderationrecord');
INSERT INTO `auth_permission` VALUES (103, 'Can delete 审核记录', 26, 'delete_moderationrecord');
INSERT INTO `auth_permission` VALUES (104, 'Can view 审核记录', 26, 'view_moderationrecord');

-- ----------------------------
-- Table structure for blog_article
-- ----------------------------
DROP TABLE IF EXISTS `blog_article`;
CREATE TABLE `blog_article`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `comment_status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `views` int UNSIGNED NOT NULL,
  `article_order` int NOT NULL,
  `author_id` bigint NOT NULL,
  `category_id` int NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `excerpt` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `modified_time` datetime(6) NOT NULL,
  `slug` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `creation_time` datetime NULL DEFAULT NULL,
  `approval_comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `approval_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `approved_by_id` bigint NULL DEFAULT NULL,
  `approved_time` datetime(6) NULL DEFAULT NULL,
  `last_modify_time` datetime NULL DEFAULT NULL,
  `pub_time` datetime NULL DEFAULT NULL,
  `show_toc` bit(1) NULL DEFAULT b'0',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `title`(`title` ASC) USING BTREE,
  INDEX `blog_article_author_id_905add38_fk_accounts_bloguser_id`(`author_id` ASC) USING BTREE,
  INDEX `blog_article_category_id_7e38f15e_fk_blog_category_id`(`category_id` ASC) USING BTREE,
  INDEX `blog_article_approved_by_id_4aa9ac0e_fk_accounts_bloguser_id`(`approved_by_id` ASC) USING BTREE,
  CONSTRAINT `blog_article_approved_by_id_4aa9ac0e_fk_accounts_bloguser_id` FOREIGN KEY (`approved_by_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `blog_article_author_id_905add38_fk_accounts_bloguser_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `blog_article_category_id_7e38f15e_fk_blog_category_id` FOREIGN KEY (`category_id`) REFERENCES `blog_category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `blog_article_chk_1` CHECK (`views` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_article
-- ----------------------------
INSERT INTO `blog_article` VALUES (1, 'nice title 1', 'nice content 1', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (2, 'nice title 2', 'nice content 2', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (3, 'nice title 3', 'nice content 3', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (4, 'nice title 4', 'nice content 4', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (5, 'nice title 5', 'nice content 5', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (6, 'nice title 6', 'nice content 6', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (7, 'nice title 7', 'nice content 7', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (8, 'nice title 8', 'nice content 8', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (9, 'nice title 9', 'nice content 9', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (10, 'nice title 10', 'nice content 10', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (11, 'nice title 11', 'nice content 11', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (12, 'nice title 12', 'nice content 12', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (13, 'nice title 13', 'nice content 13', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (14, 'nice title 14', 'nice content 14', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (15, 'nice title 15', 'nice content 15', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (16, 'nice title 16', 'nice content 16', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (17, 'nice title 17', 'nice content 17', 'p', 'o', 'a', 0, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (18, 'nice title 18', 'nice content 18', 'p', 'o', 'a', 1, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');
INSERT INTO `blog_article` VALUES (19, 'nice title 19', 'nice content 19', 'p', 'o', 'a', 4, 0, 2, 2, '2025-11-29 22:01:21.095623', '', '2025-11-29 22:01:21.217454', '', NULL, NULL, 'pending', NULL, NULL, NULL, NULL, b'0');

-- ----------------------------
-- Table structure for blog_article_tags
-- ----------------------------
DROP TABLE IF EXISTS `blog_article_tags`;
CREATE TABLE `blog_article_tags`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `article_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `blog_article_tags_article_id_tag_id_b78a22e9_uniq`(`article_id` ASC, `tag_id` ASC) USING BTREE,
  INDEX `blog_article_tags_tag_id_88eb3ed9_fk_blog_tag_id`(`tag_id` ASC) USING BTREE,
  CONSTRAINT `blog_article_tags_tag_id_88eb3ed9_fk_blog_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `blog_tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 39 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_article_tags
-- ----------------------------
INSERT INTO `blog_article_tags` VALUES (2, 1, 1);
INSERT INTO `blog_article_tags` VALUES (1, 1, 2);
INSERT INTO `blog_article_tags` VALUES (4, 2, 1);
INSERT INTO `blog_article_tags` VALUES (3, 2, 3);
INSERT INTO `blog_article_tags` VALUES (6, 3, 1);
INSERT INTO `blog_article_tags` VALUES (5, 3, 4);
INSERT INTO `blog_article_tags` VALUES (8, 4, 1);
INSERT INTO `blog_article_tags` VALUES (7, 4, 5);
INSERT INTO `blog_article_tags` VALUES (10, 5, 1);
INSERT INTO `blog_article_tags` VALUES (9, 5, 6);
INSERT INTO `blog_article_tags` VALUES (12, 6, 1);
INSERT INTO `blog_article_tags` VALUES (11, 6, 7);
INSERT INTO `blog_article_tags` VALUES (14, 7, 1);
INSERT INTO `blog_article_tags` VALUES (13, 7, 8);
INSERT INTO `blog_article_tags` VALUES (16, 8, 1);
INSERT INTO `blog_article_tags` VALUES (15, 8, 9);
INSERT INTO `blog_article_tags` VALUES (18, 9, 1);
INSERT INTO `blog_article_tags` VALUES (17, 9, 10);
INSERT INTO `blog_article_tags` VALUES (20, 10, 1);
INSERT INTO `blog_article_tags` VALUES (19, 10, 11);
INSERT INTO `blog_article_tags` VALUES (22, 11, 1);
INSERT INTO `blog_article_tags` VALUES (21, 11, 12);
INSERT INTO `blog_article_tags` VALUES (24, 12, 1);
INSERT INTO `blog_article_tags` VALUES (23, 12, 13);
INSERT INTO `blog_article_tags` VALUES (26, 13, 1);
INSERT INTO `blog_article_tags` VALUES (25, 13, 14);
INSERT INTO `blog_article_tags` VALUES (28, 14, 1);
INSERT INTO `blog_article_tags` VALUES (27, 14, 15);
INSERT INTO `blog_article_tags` VALUES (30, 15, 1);
INSERT INTO `blog_article_tags` VALUES (29, 15, 16);
INSERT INTO `blog_article_tags` VALUES (32, 16, 1);
INSERT INTO `blog_article_tags` VALUES (31, 16, 17);
INSERT INTO `blog_article_tags` VALUES (34, 17, 1);
INSERT INTO `blog_article_tags` VALUES (33, 17, 18);
INSERT INTO `blog_article_tags` VALUES (36, 18, 1);
INSERT INTO `blog_article_tags` VALUES (35, 18, 19);
INSERT INTO `blog_article_tags` VALUES (38, 19, 1);
INSERT INTO `blog_article_tags` VALUES (37, 19, 20);

-- ----------------------------
-- Table structure for blog_articleversion
-- ----------------------------
DROP TABLE IF EXISTS `blog_articleversion`;
CREATE TABLE `blog_articleversion`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `article_id` int NOT NULL COMMENT '关联的文章ID',
  `version_number` int NOT NULL COMMENT '版本号，从1开始递增',
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文章标题（版本快照）',
  `body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文章正文（版本快照）',
  `author_id` bigint NOT NULL COMMENT '编辑者ID',
  `edit_summary` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '编辑摘要，说明本次修改内容',
  `creation_time` datetime(6) NOT NULL COMMENT '版本创建时间',
  `is_current` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否为当前版本',
  `change_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'edit' COMMENT '变更类型：create/edit/rollback',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `blog_articleversion_article_version`(`article_id` ASC, `version_number` ASC) USING BTREE,
  INDEX `blog_articleversion_article_id`(`article_id` ASC) USING BTREE,
  INDEX `blog_articleversion_author_id`(`author_id` ASC) USING BTREE,
  INDEX `blog_articleversion_is_current`(`is_current` ASC) USING BTREE,
  INDEX `blog_articleversion_creation_time`(`creation_time` ASC) USING BTREE,
  INDEX `blog_articleversion_article_current`(`article_id` ASC, `is_current` ASC) USING BTREE,
  CONSTRAINT `blog_articleversion_article_id_fk` FOREIGN KEY (`article_id`) REFERENCES `blog_article` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `blog_articleversion_author_id_fk` FOREIGN KEY (`author_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of blog_articleversion
-- ----------------------------

-- ----------------------------
-- Table structure for blog_blogsettings
-- ----------------------------
DROP TABLE IF EXISTS `blog_blogsettings`;
CREATE TABLE `blog_blogsettings`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `site_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `site_description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `site_keywords` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `modified_time` datetime(6) NOT NULL,
  `site_analytics` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `site_copyright` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `site_favicon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `site_logo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `site_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_blogsettings
-- ----------------------------
INSERT INTO `blog_blogsettings` VALUES (1, 'djangoblog', '基于Django的博客系统', 'Django,Python', '2025-11-29 22:01:21.387686', '2025-11-29 22:01:21.445408', '', '', '', '', 'https://example.com');

-- ----------------------------
-- Table structure for blog_category
-- ----------------------------
DROP TABLE IF EXISTS `blog_category`;
CREATE TABLE `blog_category`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `index` int NOT NULL,
  `parent_category_id` int NULL DEFAULT NULL,
  `creation_time` datetime(6) NOT NULL,
  `last_modify_time` datetime(6) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `modified_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE,
  UNIQUE INDEX `blog_category_name_parent_category_id_0ba1ba20_uniq`(`name` ASC, `parent_category_id` ASC) USING BTREE,
  INDEX `blog_category_parent_category_id_f50c3c0c_fk_blog_category_id`(`parent_category_id` ASC) USING BTREE,
  INDEX `blog_category_slug_92643dc5`(`slug` ASC) USING BTREE,
  CONSTRAINT `blog_category_parent_category_id_f50c3c0c_fk_blog_category_id` FOREIGN KEY (`parent_category_id`) REFERENCES `blog_category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_category
-- ----------------------------
INSERT INTO `blog_category` VALUES (1, '我是父类目', 'wo-shi-fu-lei-mu', 0, NULL, '2025-11-29 16:29:41.464722', '2025-11-29 16:29:41.464722', '2025-11-29 22:01:21.719881', '2025-11-29 22:01:21.783897');
INSERT INTO `blog_category` VALUES (2, '子类目', 'zi-lei-mu', 0, 1, '2025-11-29 16:29:41.863609', '2025-11-29 16:29:41.863609', '2025-11-29 22:01:21.719881', '2025-11-29 22:01:21.783897');

-- ----------------------------
-- Table structure for blog_link
-- ----------------------------
DROP TABLE IF EXISTS `blog_link`;
CREATE TABLE `blog_link`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `index` int NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `modified_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_link
-- ----------------------------

-- ----------------------------
-- Table structure for blog_links
-- ----------------------------
DROP TABLE IF EXISTS `blog_links`;
CREATE TABLE `blog_links`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `index` int NOT NULL,
  `modified_time` datetime(6) NOT NULL,
  `url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_links
-- ----------------------------

-- ----------------------------
-- Table structure for blog_sidebar
-- ----------------------------
DROP TABLE IF EXISTS `blog_sidebar`;
CREATE TABLE `blog_sidebar`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sequence` int NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `is_enabled` tinyint(1) NOT NULL,
  `modified_time` datetime(6) NOT NULL,
  `type` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `sequence`(`sequence` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_sidebar
-- ----------------------------

-- ----------------------------
-- Table structure for blog_tag
-- ----------------------------
DROP TABLE IF EXISTS `blog_tag`;
CREATE TABLE `blog_tag`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `modified_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE,
  INDEX `blog_tag_slug_01068d0e`(`slug` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_tag
-- ----------------------------
INSERT INTO `blog_tag` VALUES (1, '标签', 'biao-qian', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (2, '标签1', 'biao-qian-1', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (3, '标签2', 'biao-qian-2', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (4, '标签3', 'biao-qian-3', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (5, '标签4', 'biao-qian-4', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (6, '标签5', 'biao-qian-5', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (7, '标签6', 'biao-qian-6', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (8, '标签7', 'biao-qian-7', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (9, '标签8', 'biao-qian-8', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (10, '标签9', 'biao-qian-9', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (11, '标签10', 'biao-qian-10', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (12, '标签11', 'biao-qian-11', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (13, '标签12', 'biao-qian-12', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (14, '标签13', 'biao-qian-13', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (15, '标签14', 'biao-qian-14', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (16, '标签15', 'biao-qian-15', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (17, '标签16', 'biao-qian-16', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (18, '标签17', 'biao-qian-17', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (19, '标签18', 'biao-qian-18', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');
INSERT INTO `blog_tag` VALUES (20, '标签19', 'biao-qian-19', '2025-11-29 22:01:22.417741', '2025-11-29 22:01:22.477583');

-- ----------------------------
-- Table structure for comments_comment
-- ----------------------------
DROP TABLE IF EXISTS `comments_comment`;
CREATE TABLE `comments_comment`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_enable` tinyint(1) NOT NULL,
  `article_id` int NOT NULL,
  `author_id` bigint NOT NULL,
  `parent_comment_id` bigint NULL DEFAULT NULL,
  `creation_time` datetime(6) NOT NULL,
  `last_modify_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `comments_comment_article_id_94fe60a2_fk_blog_article_id`(`article_id` ASC) USING BTREE,
  INDEX `comments_comment_author_id_334ce9e2_fk_accounts_bloguser_id`(`author_id` ASC) USING BTREE,
  INDEX `comments_comment_parent_comment_id_71289d4a_fk_comments_`(`parent_comment_id` ASC) USING BTREE,
  CONSTRAINT `comments_comment_author_id_334ce9e2_fk_accounts_bloguser_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comments_comment_parent_comment_id_71289d4a_fk_comments_` FOREIGN KEY (`parent_comment_id`) REFERENCES `comments_comment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comments_comment
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_accounts_bloguser_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_bloguser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (13, 'accounts', 'bloguser');
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (12, 'blog', 'article');
INSERT INTO `django_content_type` VALUES (21, 'blog', 'articleversion');
INSERT INTO `django_content_type` VALUES (7, 'blog', 'blogsettings');
INSERT INTO `django_content_type` VALUES (11, 'blog', 'category');
INSERT INTO `django_content_type` VALUES (22, 'blog', 'comment');
INSERT INTO `django_content_type` VALUES (20, 'blog', 'link');
INSERT INTO `django_content_type` VALUES (8, 'blog', 'links');
INSERT INTO `django_content_type` VALUES (9, 'blog', 'sidebar');
INSERT INTO `django_content_type` VALUES (10, 'blog', 'tag');
INSERT INTO `django_content_type` VALUES (14, 'comments', 'comment');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (25, 'moderation', 'moderationqueue');
INSERT INTO `django_content_type` VALUES (26, 'moderation', 'moderationrecord');
INSERT INTO `django_content_type` VALUES (24, 'moderation', 'moderationstatistics');
INSERT INTO `django_content_type` VALUES (15, 'oauth', 'oauthconfig');
INSERT INTO `django_content_type` VALUES (16, 'oauth', 'oauthuser');
INSERT INTO `django_content_type` VALUES (19, 'owntracks', 'owntracklog');
INSERT INTO `django_content_type` VALUES (17, 'servermanager', 'commands');
INSERT INTO `django_content_type` VALUES (18, 'servermanager', 'emailsendlog');
INSERT INTO `django_content_type` VALUES (23, 'servermanager', 'reviewhistory');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (6, 'sites', 'site');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 43 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-11-29 16:28:39.145900');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2025-11-29 16:28:39.337598');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2025-11-29 16:28:39.772378');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2025-11-29 16:28:39.851135');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2025-11-29 16:28:39.878281');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2025-11-29 16:28:39.905100');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2025-11-29 16:28:39.931125');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2025-11-29 16:28:39.951133');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2025-11-29 16:28:39.979543');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2025-11-29 16:28:40.005146');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2025-11-29 16:28:40.031577');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0010_alter_group_name_max_length', '2025-11-29 16:28:40.087062');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0011_update_proxy_permissions', '2025-11-29 16:28:40.170217');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2025-11-29 16:28:40.200906');
INSERT INTO `django_migrations` VALUES (15, 'accounts', '0001_initial', '2025-11-29 16:28:40.697128');
INSERT INTO `django_migrations` VALUES (16, 'accounts', '0002_alter_bloguser_options_remove_bloguser_created_time_and_more', '2025-11-29 16:28:41.015369');
INSERT INTO `django_migrations` VALUES (17, 'admin', '0001_initial', '2025-11-29 16:28:41.238252');
INSERT INTO `django_migrations` VALUES (18, 'admin', '0002_logentry_remove_auto_add', '2025-11-29 16:28:41.270770');
INSERT INTO `django_migrations` VALUES (19, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-29 16:28:41.304965');
INSERT INTO `django_migrations` VALUES (20, 'blog', '0001_initial', '2025-11-29 16:28:42.210396');
INSERT INTO `django_migrations` VALUES (21, 'blog', '0002_blogsettings_global_footer_and_more', '2025-11-29 16:28:42.393516');
INSERT INTO `django_migrations` VALUES (22, 'blog', '0003_blogsettings_comment_need_review', '2025-11-29 16:28:42.489283');
INSERT INTO `django_migrations` VALUES (23, 'blog', '0004_rename_analyticscode_blogsettings_analytics_code_and_more', '2025-11-29 16:28:42.624700');
INSERT INTO `django_migrations` VALUES (24, 'blog', '0005_alter_article_options_alter_category_options_and_more', '2025-11-29 16:28:43.915268');
INSERT INTO `django_migrations` VALUES (25, 'blog', '0006_alter_blogsettings_options', '2025-11-29 16:28:43.943142');
INSERT INTO `django_migrations` VALUES (26, 'comments', '0001_initial', '2025-11-29 16:28:44.258956');
INSERT INTO `django_migrations` VALUES (27, 'comments', '0002_alter_comment_is_enable', '2025-11-29 16:28:44.287040');
INSERT INTO `django_migrations` VALUES (28, 'comments', '0003_alter_comment_options_remove_comment_created_time_and_more', '2025-11-29 16:28:44.660257');
INSERT INTO `django_migrations` VALUES (29, 'oauth', '0001_initial', '2025-11-29 16:28:44.835136');
INSERT INTO `django_migrations` VALUES (30, 'oauth', '0002_alter_oauthconfig_options_alter_oauthuser_options_and_more', '2025-11-29 16:28:45.388057');
INSERT INTO `django_migrations` VALUES (31, 'oauth', '0003_alter_oauthuser_nickname', '2025-11-29 16:28:45.416052');
INSERT INTO `django_migrations` VALUES (32, 'owntracks', '0001_initial', '2025-11-29 16:28:45.477737');
INSERT INTO `django_migrations` VALUES (33, 'owntracks', '0002_alter_owntracklog_options_and_more', '2025-11-29 16:28:45.531857');
INSERT INTO `django_migrations` VALUES (34, 'servermanager', '0001_initial', '2025-11-29 16:28:45.624558');
INSERT INTO `django_migrations` VALUES (35, 'servermanager', '0002_alter_emailsendlog_options_and_more', '2025-11-29 16:28:45.741139');
INSERT INTO `django_migrations` VALUES (36, 'sessions', '0001_initial', '2025-11-29 16:28:45.852424');
INSERT INTO `django_migrations` VALUES (37, 'sites', '0001_initial', '2025-11-29 16:28:45.907495');
INSERT INTO `django_migrations` VALUES (38, 'sites', '0002_alter_domain_unique', '2025-11-29 16:28:45.962206');
INSERT INTO `django_migrations` VALUES (39, 'notifications', '0001_initial', '2025-11-29 18:55:29.384618');
INSERT INTO `django_migrations` VALUES (40, 'blog', '0007_article_approval_comment_article_approval_status_and_more', '2025-11-30 09:23:41.405731');
INSERT INTO `django_migrations` VALUES (41, 'servermanager', '0003_reviewhistory', '2025-11-30 09:23:41.692182');
INSERT INTO `django_migrations` VALUES (42, 'moderation', '0001_initial', '2025-11-30 10:08:09.406860');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('ggg4f89vzqolzf4xz1eqwhf3xweplcw3', '.eJxVjMsKwjAQAP8lZ5Ek3W7SHgWP4slzyWNrg20iTQuK-O-2oqDXGWYerDHz1DVzprEJntVMsM0vs8ZdKK7COJfmOOXtm_fpHOLXbveDCf1xPC0mmoEOyVO_-5R_u87kbnlpQ7qwlpcWSGFhKyVIt8A5-EoA1-hkIcB5q0wlOKKz6EoEiwASFLbrNFPOIcWGbtcw3lktUWKJ_PkCb25FhA:1vPITd:ZBHLOxRBSsKU8waWYgSFvgdOvAvfZ_IKHUkfauytgV0', '2025-12-30 04:22:53.928994');

-- ----------------------------
-- Table structure for django_site
-- ----------------------------
DROP TABLE IF EXISTS `django_site`;
CREATE TABLE `django_site`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_site_domain_a2e37b91_uniq`(`domain` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_site
-- ----------------------------
INSERT INTO `django_site` VALUES (1, 'example.com', 'example.com');

-- ----------------------------
-- Table structure for moderation_moderationqueue
-- ----------------------------
DROP TABLE IF EXISTS `moderation_moderationqueue`;
CREATE TABLE `moderation_moderationqueue`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content_type_id` int NOT NULL COMMENT '内容类型ID',
  `object_id` bigint NOT NULL COMMENT '对象ID',
  `priority` int NOT NULL DEFAULT 0 COMMENT '优先级，数字越大优先级越高',
  `assigned_to_id` bigint NULL DEFAULT NULL COMMENT '分配给的用户ID',
  `creation_time` datetime(6) NOT NULL COMMENT '加入队列时间',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending' COMMENT '队列状态：pending/processing/completed',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `moderation_moderationqueue_content_type_id`(`content_type_id` ASC) USING BTREE,
  INDEX `moderation_moderationqueue_object_id`(`object_id` ASC) USING BTREE,
  INDEX `moderation_moderationqueue_assigned_to_id`(`assigned_to_id` ASC) USING BTREE,
  INDEX `moderation_moderationqueue_status`(`status` ASC) USING BTREE,
  INDEX `moderation_moderationqueue_priority`(`priority` ASC) USING BTREE,
  CONSTRAINT `moderation_moderationqueue_assigned_to_id_fk` FOREIGN KEY (`assigned_to_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of moderation_moderationqueue
-- ----------------------------

-- ----------------------------
-- Table structure for moderation_moderationrecord
-- ----------------------------
DROP TABLE IF EXISTS `moderation_moderationrecord`;
CREATE TABLE `moderation_moderationrecord`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content_type_id` int NOT NULL COMMENT '内容类型ID（ContentType）',
  `object_id` bigint NOT NULL COMMENT '被审核对象的ID',
  `moderator_id` bigint NOT NULL COMMENT '审核人ID',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '审核状态：pending/approved/rejected/needs_revision',
  `moderation_time` datetime(6) NOT NULL COMMENT '审核时间',
  `comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '审核意见/备注',
  `moderation_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '审核类型：comment/article',
  `previous_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '审核前的状态',
  `creation_time` datetime(6) NOT NULL COMMENT '记录创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `moderation_moderationrecord_content_type_id`(`content_type_id` ASC) USING BTREE,
  INDEX `moderation_moderationrecord_object_id`(`object_id` ASC) USING BTREE,
  INDEX `moderation_moderationrecord_moderator_id`(`moderator_id` ASC) USING BTREE,
  INDEX `moderation_moderationrecord_status`(`status` ASC) USING BTREE,
  INDEX `moderation_moderationrecord_moderation_time`(`moderation_time` ASC) USING BTREE,
  INDEX `moderation_moderationrecord_content_object`(`content_type_id` ASC, `object_id` ASC) USING BTREE,
  CONSTRAINT `moderation_moderationrecord_moderator_id_fk` FOREIGN KEY (`moderator_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of moderation_moderationrecord
-- ----------------------------

-- ----------------------------
-- Table structure for moderation_moderationstatistics
-- ----------------------------
DROP TABLE IF EXISTS `moderation_moderationstatistics`;
CREATE TABLE `moderation_moderationstatistics`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `total_pending` int NOT NULL,
  `total_approved` int NOT NULL,
  `total_rejected` int NOT NULL,
  `total_needs_modification` int NOT NULL,
  `comment_pending` int NOT NULL,
  `comment_approved` int NOT NULL,
  `comment_rejected` int NOT NULL,
  `comment_needs_modification` int NOT NULL,
  `article_pending` int NOT NULL,
  `article_approved` int NOT NULL,
  `article_rejected` int NOT NULL,
  `article_needs_modification` int NOT NULL,
  `approval_rate` decimal(5, 2) NOT NULL,
  `creation_time` datetime(6) NOT NULL,
  `last_update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `date`(`date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of moderation_moderationstatistics
-- ----------------------------

-- ----------------------------
-- Table structure for notifications_notification
-- ----------------------------
DROP TABLE IF EXISTS `notifications_notification`;
CREATE TABLE `notifications_notification`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `recipient_id` bigint NOT NULL COMMENT '接收者ID',
  `sender_id` bigint NULL DEFAULT NULL COMMENT '发送者ID（系统通知为空）',
  `notification_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '通知类型：comment_reply/system/audit等',
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '通知标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '通知内容',
  `related_object_id` bigint NULL DEFAULT NULL COMMENT '关联对象ID',
  `related_content_type_id` int NULL DEFAULT NULL COMMENT '关联对象类型ID（ContentType）',
  `is_read` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否已读',
  `read_time` datetime(6) NULL DEFAULT NULL COMMENT '阅读时间',
  `creation_time` datetime(6) NOT NULL COMMENT '创建时间',
  `extra_data` json NULL COMMENT '额外数据（可选）',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `notifications_notification_recipient_id`(`recipient_id` ASC) USING BTREE,
  INDEX `notifications_notification_sender_id`(`sender_id` ASC) USING BTREE,
  INDEX `notifications_notification_is_read`(`is_read` ASC) USING BTREE,
  INDEX `notifications_notification_creation_time`(`creation_time` ASC) USING BTREE,
  INDEX `notifications_notification_recipient_read`(`recipient_id` ASC, `is_read` ASC) USING BTREE,
  CONSTRAINT `notifications_notification_recipient_id_fk` FOREIGN KEY (`recipient_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `notifications_notification_sender_id_fk` FOREIGN KEY (`sender_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of notifications_notification
-- ----------------------------

-- ----------------------------
-- Table structure for oauth_oauthconfig
-- ----------------------------
DROP TABLE IF EXISTS `oauth_oauthconfig`;
CREATE TABLE `oauth_oauthconfig`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `appkey` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `appsecret` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `callback_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_enable` tinyint(1) NOT NULL,
  `creation_time` datetime(6) NOT NULL,
  `last_modify_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oauth_oauthconfig
-- ----------------------------

-- ----------------------------
-- Table structure for oauth_oauthuser
-- ----------------------------
DROP TABLE IF EXISTS `oauth_oauthuser`;
CREATE TABLE `oauth_oauthuser`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `openid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `picture` varchar(350) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `author_id` bigint NULL DEFAULT NULL,
  `creation_time` datetime(6) NOT NULL,
  `last_modify_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `oauth_oauthuser_author_id_a975bef0_fk_accounts_bloguser_id`(`author_id` ASC) USING BTREE,
  CONSTRAINT `oauth_oauthuser_author_id_a975bef0_fk_accounts_bloguser_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oauth_oauthuser
-- ----------------------------

-- ----------------------------
-- Table structure for owntracks_owntracklog
-- ----------------------------
DROP TABLE IF EXISTS `owntracks_owntracklog`;
CREATE TABLE `owntracks_owntracklog`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `lat` double NOT NULL,
  `lon` double NOT NULL,
  `creation_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of owntracks_owntracklog
-- ----------------------------

-- ----------------------------
-- Table structure for servermanager_commands
-- ----------------------------
DROP TABLE IF EXISTS `servermanager_commands`;
CREATE TABLE `servermanager_commands`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `command` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `describe` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `creation_time` datetime(6) NOT NULL,
  `last_modify_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of servermanager_commands
-- ----------------------------

-- ----------------------------
-- Table structure for servermanager_emailsendlog
-- ----------------------------
DROP TABLE IF EXISTS `servermanager_emailsendlog`;
CREATE TABLE `servermanager_emailsendlog`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `emailto` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `send_result` tinyint(1) NOT NULL,
  `creation_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of servermanager_emailsendlog
-- ----------------------------

-- ----------------------------
-- Table structure for servermanager_reviewhistory
-- ----------------------------
DROP TABLE IF EXISTS `servermanager_reviewhistory`;
CREATE TABLE `servermanager_reviewhistory`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `review_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `review_time` datetime(6) NOT NULL,
  `result` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `object_id` int UNSIGNED NOT NULL,
  `content_type_id` int NOT NULL,
  `reviewer_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `servermanager_review_content_type_id_80095297_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `servermanager_review_reviewer_id_c6703190_fk_accounts_`(`reviewer_id` ASC) USING BTREE,
  CONSTRAINT `servermanager_review_content_type_id_80095297_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `servermanager_review_reviewer_id_c6703190_fk_accounts_` FOREIGN KEY (`reviewer_id`) REFERENCES `accounts_bloguser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `servermanager_reviewhistory_chk_1` CHECK (`object_id` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of servermanager_reviewhistory
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
