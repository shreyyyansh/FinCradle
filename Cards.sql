-- DELETE FROM credit_cards;

-- INSERT INTO credit_cards (card_id, bank, card_name) VALUES
-- (1, 'HDFC', 'Millennia'),
-- (2, 'ICICI', 'Amazon Pay'),
-- (3, 'SBI', 'SimplyClick'),
-- (4, 'Axis', 'Flipkart');


-- -- ================= CARD REWARDS =================
-- DELETE FROM card_rewards;

-- INSERT INTO card_rewards (reward_id, card_id, category_id, cashback_percent) VALUES
-- -- Shopping (category_id = 1)
-- (1, 1, 1, 5),
-- (2, 2, 1, 5),
-- (3, 3, 1, 10),
-- (4, 4, 1, 5),

-- -- Food (category_id = 2)
-- (5, 1, 2, 2),
-- (6, 2, 2, 1),
-- (7, 4, 2, 4),

-- -- Travel (category_id = 3)
-- (8, 3, 3, 5),

-- -- Subscriptions (category_id = 4)
-- (9, 1, 4, 5),
-- (10, 2, 4, 2);



INSERT INTO banks (name) VALUES
('ICICI Bank'),
('HDFC Bank'),
('SBI'),
('American Express');


-- INSERT INTO credit_cards (bank_id, card_name, annual_fee)
-- VALUES
-- (1, 'ICICI Amazon Pay', 0),
-- (2, 'HDFC Millennia', 1000),
-- (3, 'SBI Cashback', 999);

INSERT INTO credit_cards (bank, card_name)
VALUES
('ICICI Bank', 'ICICI Amazon Pay'),
('HDFC Bank', 'HDFC Millennia'),
('SBI', 'SBI Cashback');


-- INSERT INTO credit_card_benefits
-- (card_id, category_name, cashback_percent, max_cashback)
-- VALUES
-- (1, 'Lifestyle', 5.00, 1500),
-- (1, 'Shopping', 5.00, 1500),
-- (2, 'Dining', 5.00, 1000),
-- (3, 'All', 5.00, 5000);

INSERT INTO credit_card_benefits 
(card_id, category_name, cashback_percent, max_cashback, frequency)
VALUES
-- ICICI Amazon Pay
(1, 'Shopping', 5, NULL, 'per_transaction'),
(1, 'Utilities', 2, NULL, 'monthly'),

-- HDFC Millennia
(2, 'Shopping', 5, 1000, 'monthly'),
(2, 'Dining', 5, 1000, 'monthly'),

-- SBI Cashback
(3, 'Online', 5, 5000, 'monthly');

INSERT INTO card_rewards (card_id, category_id, cashback_percent)
VALUES
(1, 5, 5.0),   -- ICICI Amazon Pay on Shopping
(2, 5, 5.0),   -- HDFC Millennia
(3, 5, 5.0),   -- SBI Cashback
(4, 3, 3.0);   -- AMEX on Dining
	