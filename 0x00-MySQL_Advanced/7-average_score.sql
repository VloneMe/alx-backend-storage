-- This create the stored procedure ComputeAverageScoreForUser
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN in_user_id INT
)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);

    -- Compute the average score for the specified user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = in_user_id;

    -- Update the average score for the user in the users table
    UPDATE users
    SET average_score = avg_score
    WHERE id = in_user_id;
END;
//
DELIMITER ;
