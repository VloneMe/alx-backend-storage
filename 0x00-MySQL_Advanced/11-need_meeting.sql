-- This creates the view need_meeting
CREATE VIEW need_meeting AS
SELECT
    id,
    name
FROM
    students
WHERE
    score < 80
    AND (last_meeting IS NULL OR last_meeting < NOW() - INTERVAL 1 MONTH);
