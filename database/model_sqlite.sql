-- Enable foreign key support in SQLite
PRAGMA foreign_keys = ON;

-- Drop tables if they already exist to prevent conflicts
DROP TABLE IF EXISTS series;
DROP TABLE IF EXISTS colors;
DROP TABLE IF EXISTS finishes;
DROP TABLE IF EXISTS series_finishes;
DROP TABLE IF EXISTS thicknesses;
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS thickness_applications;
DROP TABLE IF EXISTS systems;
DROP TABLE IF EXISTS system_features;
DROP TABLE IF EXISTS technical_characteristics;
DROP TABLE IF EXISTS downloads;

-- 1. Series Table
CREATE TABLE series
(
    series_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name TEXT NOT NULL,
    description TEXT
);

-- 2. Colors Table
CREATE TABLE colors
(
    color_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id  INTEGER NOT NULL,
    color_name TEXT    NOT NULL,
    FOREIGN KEY (series_id) REFERENCES series (series_id) ON DELETE CASCADE
);

-- 3. Finishes Table
CREATE TABLE finishes
(
    finish_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    finish_name TEXT NOT NULL UNIQUE
);

-- 4. Series_Finishes Table (Many-to-Many relationship between series and finishes)
CREATE TABLE series_finishes
(
    series_id INTEGER NOT NULL,
    finish_id INTEGER NOT NULL,
    PRIMARY KEY (series_id, finish_id),
    FOREIGN KEY (series_id) REFERENCES series (series_id) ON DELETE CASCADE,
    FOREIGN KEY (finish_id) REFERENCES finishes (finish_id) ON DELETE CASCADE
);

-- 5. Thicknesses Table
CREATE TABLE thicknesses
(
    thickness_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    thickness_name  TEXT NOT NULL,
    thickness_value REAL NOT NULL -- Thickness in mm
);

-- 6. Applications Table
CREATE TABLE applications
(
    application_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    application_name TEXT NOT NULL UNIQUE
);

-- 7. Thickness_Applications Table (Many-to-Many relationship between thicknesses and applications)
CREATE TABLE thickness_applications
(
    thickness_id   INTEGER NOT NULL,
    application_id INTEGER NOT NULL,
    PRIMARY KEY (thickness_id, application_id),
    FOREIGN KEY (thickness_id) REFERENCES thicknesses (thickness_id) ON DELETE CASCADE,
    FOREIGN KEY (application_id) REFERENCES applications (application_id) ON DELETE CASCADE
);

-- 8. Systems Table
CREATE TABLE systems
(
    system_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    system_name TEXT NOT NULL,
    description TEXT
);

-- 9. System_Features Table
CREATE TABLE system_features
(
    feature_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id           INTEGER NOT NULL,
    feature_description TEXT    NOT NULL,
    FOREIGN KEY (system_id) REFERENCES systems (system_id) ON DELETE CASCADE
);

-- 10. Technical_Characteristics Table
CREATE TABLE technical_characteristics
(
    characteristic_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    characteristic_name  TEXT NOT NULL UNIQUE,
    characteristic_value TEXT NOT NULL
);


-- Indexes (optional but recommended for performance)
CREATE INDEX idx_colors_series_id ON colors (series_id);
CREATE INDEX idx_series_finishes_series_id ON series_finishes (series_id);
CREATE INDEX idx_series_finishes_finish_id ON series_finishes (finish_id);
CREATE INDEX idx_thickness_applications_thickness_id ON thickness_applications (thickness_id);
CREATE INDEX idx_thickness_applications_application_id ON thickness_applications (application_id);
CREATE INDEX idx_system_features_system_id ON system_features (system_id);
