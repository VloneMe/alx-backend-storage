-- This create the stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE avg_weighted_score DECIMAL(10, 2);

    -- This ursor to iterate over all distinct user IDs
    DECLARE user_cursor CURSOR FOR
        SELECT DISTINCT user_id FROM weighted_scores;

    -- This declare handlers for exceptions
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN user_cursor;

    -- Start fetching user IDs
    FETCH user_cursor INTO user_id;

    -- Loop through all distinct user IDs
    WHILE NOT done DO
        -- This compute the average weighted score for each user
        SELECT AVG(score * weight) INTO avg_weighted_score
        FROM weighted_scores
        WHERE user_id = user_id;

        -- Update or insert the average weighted score for the user
        INSERT INTO average_weighted_scores (user_id, avg_weighted_score)
        VALUES (user_id, avg_weighted_score)
        ON DUPLICATE KEY UPDATE avg_weighted_score = avg_weighted_score;

        -- Fetch the next user ID
        FETCH user_cursor INTO user_id;
    END WHILE;

    -- Close the cursor
    CLOSE user_cursor;
END;
//
DELIMITER ;
