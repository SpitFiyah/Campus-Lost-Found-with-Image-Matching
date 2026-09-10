CREATE DATABASE IF NOT EXISTS campus_lost_found
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE campus_lost_found;

CREATE TABLE users (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(120) NOT NULL,
  college_email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  student_id VARCHAR(50) NOT NULL UNIQUE,
  department VARCHAR(120) NOT NULL,
  phone VARCHAR(30),
  role ENUM('STUDENT', 'ADMIN', 'MODERATOR') NOT NULL DEFAULT 'STUDENT',
  is_verified BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX ix_users_role (role),
  INDEX ix_users_verified (is_verified)
);

CREATE TABLE items (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  type ENUM('LOST', 'FOUND') NOT NULL,
  name VARCHAR(160) NOT NULL,
  category VARCHAR(80) NOT NULL,
  description TEXT NOT NULL,
  color VARCHAR(80),
  location VARCHAR(100) NOT NULL,
  date_lost_found DATE NOT NULL,
  time_lost_found TIME,
  status ENUM('ACTIVE', 'MATCHED', 'RETURNED', 'CLOSED', 'REMOVED') NOT NULL DEFAULT 'ACTIVE',
  private_verification_answer VARCHAR(255),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_items_user FOREIGN KEY (user_id) REFERENCES users (id),
  INDEX ix_items_search (type, status, category, location),
  INDEX ix_items_date (date_lost_found)
);

CREATE TABLE item_images (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  item_id BIGINT UNSIGNED NOT NULL,
  image_path VARCHAR(500) NOT NULL,
  embedding_path VARCHAR(500),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_item_images_item FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE,
  INDEX ix_item_images_item (item_id)
);

CREATE TABLE matches (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  lost_item_id BIGINT UNSIGNED NOT NULL,
  found_item_id BIGINT UNSIGNED NOT NULL,
  image_similarity DECIMAL(5,2) NOT NULL,
  location_score DECIMAL(5,2) NOT NULL,
  category_score DECIMAL(5,2) NOT NULL,
  color_score DECIMAL(5,2) NOT NULL,
  date_score DECIMAL(5,2) NOT NULL,
  final_score DECIMAL(5,2) NOT NULL,
  status ENUM('PENDING', 'ACCEPTED', 'REJECTED', 'EXPIRED') NOT NULL DEFAULT 'PENDING',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_matches_lost FOREIGN KEY (lost_item_id) REFERENCES items (id),
  CONSTRAINT fk_matches_found FOREIGN KEY (found_item_id) REFERENCES items (id),
  CONSTRAINT uq_matches_pair UNIQUE (lost_item_id, found_item_id),
  INDEX ix_matches_status_score (status, final_score)
);

CREATE TABLE messages (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  sender_id BIGINT UNSIGNED NOT NULL,
  receiver_id BIGINT UNSIGNED NOT NULL,
  item_id BIGINT UNSIGNED,
  message TEXT NOT NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_messages_sender FOREIGN KEY (sender_id) REFERENCES users (id),
  CONSTRAINT fk_messages_receiver FOREIGN KEY (receiver_id) REFERENCES users (id),
  CONSTRAINT fk_messages_item FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE SET NULL,
  INDEX ix_messages_conversation (sender_id, receiver_id, created_at),
  INDEX ix_messages_unread (receiver_id, is_read)
);

CREATE TABLE notifications (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  type VARCHAR(50) NOT NULL,
  title VARCHAR(160) NOT NULL,
  message VARCHAR(500) NOT NULL,
  related_item_id BIGINT UNSIGNED,
  related_match_id BIGINT UNSIGNED,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_notifications_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_notifications_item FOREIGN KEY (related_item_id) REFERENCES items (id) ON DELETE SET NULL,
  CONSTRAINT fk_notifications_match FOREIGN KEY (related_match_id) REFERENCES matches (id) ON DELETE SET NULL,
  INDEX ix_notifications_user_read (user_id, is_read, created_at)
);

CREATE TABLE reports (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  reporter_id BIGINT UNSIGNED NOT NULL,
  item_id BIGINT UNSIGNED NOT NULL,
  reason VARCHAR(80) NOT NULL,
  description VARCHAR(500),
  status ENUM('PENDING', 'REVIEWED', 'DISMISSED', 'ACTIONED') NOT NULL DEFAULT 'PENDING',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_reports_reporter FOREIGN KEY (reporter_id) REFERENCES users (id),
  CONSTRAINT fk_reports_item FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE,
  INDEX ix_reports_status (status, created_at)
);
