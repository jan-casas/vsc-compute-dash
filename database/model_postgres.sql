-- Drop tables if they already exist to prevent conflicts
DROP TABLE IF EXISTS series CASCADE;
DROP TABLE IF EXISTS colors CASCADE;
DROP TABLE IF EXISTS finishes CASCADE;
DROP TABLE IF EXISTS series_finishes CASCADE;
DROP TABLE IF EXISTS thicknesses CASCADE;
DROP TABLE IF EXISTS applications CASCADE;
DROP TABLE IF EXISTS thickness_applications CASCADE;
DROP TABLE IF EXISTS systems CASCADE;
DROP TABLE IF EXISTS system_features CASCADE;
DROP TABLE IF EXISTS technical_characteristics CASCADE;
DROP TABLE IF EXISTS downloads CASCADE;

-- 1. Series Table
CREATE TABLE series
(
    series_id   SERIAL PRIMARY KEY,
    series_name VARCHAR(100) NOT NULL,
    description TEXT
);

-- 2. Colors Table
CREATE TABLE colors
(
    color_id   SERIAL PRIMARY KEY,
    series_id  INT REFERENCES series (series_id) ON DELETE CASCADE,
    color_name VARCHAR(50) NOT NULL
);

-- 3. Finishes Table
CREATE TABLE finishes
(
    finish_id   SERIAL PRIMARY KEY,
    finish_name VARCHAR(50) NOT NULL UNIQUE
);

-- 4. Series_Finishes Table (Many-to-Many relationship between series and finishes)
CREATE TABLE series_finishes
(
    series_id INT REFERENCES series (series_id) ON DELETE CASCADE,
    finish_id INT REFERENCES finishes (finish_id) ON DELETE CASCADE,
    PRIMARY KEY (series_id, finish_id)
);

-- 5. Thicknesses Table
CREATE TABLE thicknesses
(
    thickness_id    SERIAL PRIMARY KEY,
    thickness_name  VARCHAR(50)   NOT NULL,
    thickness_value DECIMAL(5, 2) NOT NULL -- Thickness in mm
);

-- 6. Applications Table
CREATE TABLE applications
(
    application_id   SERIAL PRIMARY KEY,
    application_name VARCHAR(100) NOT NULL UNIQUE
);

-- 7. Thickness_Applications Table (Many-to-Many relationship between thicknesses and applications)
CREATE TABLE thickness_applications
(
    thickness_id   INT REFERENCES thicknesses (thickness_id) ON DELETE CASCADE,
    application_id INT REFERENCES applications (application_id) ON DELETE CASCADE,
    PRIMARY KEY (thickness_id, application_id)
);

-- 8. Systems Table
CREATE TABLE systems
(
    system_id   SERIAL PRIMARY KEY,
    system_name VARCHAR(100) NOT NULL,
    description TEXT
);

-- 9. System_Features Table
CREATE TABLE system_features
(
    feature_id          SERIAL PRIMARY KEY,
    system_id           INT REFERENCES systems (system_id) ON DELETE CASCADE,
    feature_description TEXT NOT NULL
);

-- 10. Technical_Characteristics Table
CREATE TABLE technical_characteristics
(
    characteristic_id    SERIAL PRIMARY KEY,
    characteristic_name  VARCHAR(100) NOT NULL UNIQUE,
    characteristic_value VARCHAR(100) NOT NULL
);


-- Optionally, you can create indexes to improve query performance
CREATE INDEX idx_colors_series_id ON colors (series_id);
CREATE INDEX idx_series_finishes_series_id ON series_finishes (series_id);
CREATE INDEX idx_series_finishes_finish_id ON series_finishes (finish_id);
CREATE INDEX idx_thickness_applications_thickness_id ON thickness_applications (thickness_id);
CREATE INDEX idx_thickness_applications_application_id ON thickness_applications (application_id);
CREATE INDEX idx_system_features_system_id ON system_features (system_id);
