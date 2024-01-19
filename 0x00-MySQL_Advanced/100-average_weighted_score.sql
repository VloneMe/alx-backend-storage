-- This create the stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN in_user_id INT
)
BEGIN
    DECLARE avg_weighted_score DECIMAL(10, 2);

    -- Compute the average weighted score for the specified user
    SELECT AVG(score * weight) INTO avg_weighted_score
    FROM weighted_scores
    WHERE user_id = in_user_id;

    -- Update or insert the average weighted score for the user
    INSERT INTO average_weighted_scores (user_id, avg_weighted_score)
    VALUES (in_user_id, avg_weighted_score)
    ON DUPLICATE KEY UPDATE avg_weighted_score = avg_weighted_score;
END;
//
DELIMITER ;
