-- This list bands with Glam rock as main style, ranked by longevity
SELECT
    band_name,
    style,
    CONCAT(
        IF(split IS NOT NULL, split, 2022) - formed,
        ' years'
    ) AS lifespan
FROM
    metal_bands
WHERE
    style = 'Glam rock'
ORDER BY
    IF(split IS NOT NULL, split, 2022) - formed DESC;
