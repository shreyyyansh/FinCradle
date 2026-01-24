SELECT 
    e.user_id,
    ccb.card_id,
    cc.card_name,
    SUM(e.amount * (ccb.cashback_percent / 100)) AS possible_savings
FROM expenses e
JOIN categories cat ON e.category_id = cat.category_id
JOIN credit_card_benefits ccb 
    ON LOWER(cat.name) = LOWER(ccb.category_name)
JOIN credit_cards cc ON cc.card_id = ccb.card_id
WHERE 
    e.user_id = ?
    AND MONTH(e.date) = MONTH(CURDATE())
GROUP BY cc.card_name;
