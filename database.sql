CREATE DATABASE IF NOT EXISTS finance_db;
USE finance_db;

-- ================= USERS =================
CREATE TABLE users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    verified BOOLEAN DEFAULT FALSE
);

-- ================= CATEGORIES =================
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    type ENUM('income','expense') NOT NULL,
    include_weekly BOOLEAN DEFAULT TRUE,
    include_monthly BOOLEAN DEFAULT TRUE,
    include_yearly BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ================= INCOME =================
CREATE TABLE income (
    income_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT
);

-- ================= EXPENSES =================
CREATE TABLE expenses (
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    date DATE NOT NULL,
    note VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT
);

-- ================= CATEGORY LEAK VIEW =================
CREATE OR REPLACE VIEW category_leak_view AS
SELECT 
    e.user_id,
    c.name AS category_name,
    SUM(CASE 
            WHEN YEAR(e.date) = YEAR(CURDATE())
             AND MONTH(e.date) = MONTH(CURDATE())
            THEN e.amount ELSE 0 
        END) AS this_month,
    SUM(CASE 
            WHEN YEAR(e.date) = YEAR(DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
             AND MONTH(e.date) = MONTH(DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
            THEN e.amount ELSE 0 
        END) AS last_month
FROM expenses e
JOIN categories c 
    ON e.category_id = c.category_id
GROUP BY e.user_id, c.name;

-- ================= CREDIT CARDS =================
CREATE TABLE credit_cards (
    card_id INT AUTO_INCREMENT PRIMARY KEY,
    bank VARCHAR(100) NOT NULL,
    card_name VARCHAR(100) NOT NULL
);

ALTER TABLE credit_cards
ADD COLUMN bank_id INT,
ADD COLUMN annual_fee INT DEFAULT 0,
ADD COLUMN joining_fee INT DEFAULT 0,
ADD COLUMN reward_type ENUM('cashback','points','miles') DEFAULT 'cashback',
ADD COLUMN active BOOLEAN DEFAULT TRUE,
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;


-- ================= CARD REWARDS =================
CREATE TABLE card_rewards (
    reward_id INT PRIMARY KEY AUTO_INCREMENT,
    card_id INT NOT NULL,
    category_id INT NOT NULL,
    cashback_percent FLOAT NOT NULL,
    FOREIGN KEY (card_id) REFERENCES credit_cards(card_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
);


CREATE TABLE banks (
    bank_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE credit_cards
ADD CONSTRAINT fk_credit_cards_bank
FOREIGN KEY (bank_id) REFERENCES banks(bank_id);

-- CREATE TABLE credit_card_benefits (
--     benefit_id INT AUTO_INCREMENT PRIMARY KEY,
--     card_id INT NOT NULL,
--     category_name VARCHAR(100) NOT NULL,
--     cashback_percent DECIMAL(5,2),
--     min_spend INT DEFAULT 0,
--     max_cashback INT,
--     frequency ENUM('per_txn','monthly','yearly') DEFAULT 'monthly',
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (card_id) REFERENCES credit_cards(card_id) ON DELETE CASCADE
-- );

CREATE TABLE credit_card_benefits (
    benefit_id INT AUTO_INCREMENT PRIMARY KEY,
    card_id INT NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    cashback_percent DECIMAL(5,2) DEFAULT 0,
    max_cashback DECIMAL(10,2) DEFAULT NULL,
    frequency ENUM('monthly','yearly','per_transaction') DEFAULT 'monthly',
    FOREIGN KEY (card_id) REFERENCES credit_cards(card_id) ON DELETE CASCADE
);


CREATE TABLE card_recommendations (
    rec_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    card_id INT NOT NULL,
    category VARCHAR(100),
    expense_amount DECIMAL(10,2),
    estimated_saving DECIMAL(10,2),
    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES credit_cards(card_id) ON DELETE CASCADE
);

CREATE TABLE credit_card_conditions (
    condition_id INT AUTO_INCREMENT PRIMARY KEY,
    card_id INT NOT NULL,
    min_amount DECIMAL(10,2) DEFAULT 0,
    max_amount DECIMAL(10,2) DEFAULT NULL,
    cap_amount DECIMAL(10,2) DEFAULT NULL,
    FOREIGN KEY (card_id) REFERENCES credit_cards(card_id) ON DELETE CASCADE
);


