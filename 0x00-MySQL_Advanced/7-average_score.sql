--  SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (
    user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE projects_count INT;

    -- Calculate total score and number of projects
    SELECT SUM(score), COUNT(*) INTO total_score, projects_count
        FROM corrections
        WHERE corrections.user_id = user_id;

    -- Update the average_score for the user in the users table
    UPDATE users
        SET average_score = IF(projects_count = 0, 0, total_score / projects_count)
        WHERE users.id = user_id;
END //
DELIMITER ;