USE finance_db;

INSERT INTO categories (user_id, name, include_weekly, include_monthly, include_yearly)
VALUES
(1, 'Salary', 0, 1, 1),
(1, 'Freelance', 0, 1, 1),
(1, 'Food', 1, 1, 1),
(1, 'Subscriptions', 0, 1, 0),
(1, 'Entertainment', 0, 1, 0),
(1, 'Essentials', 1, 1, 1);
