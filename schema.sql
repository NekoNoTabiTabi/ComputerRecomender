-- 1. Create the CPU table
CREATE TABLE cpus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    series VARCHAR(50),
    name VARCHAR(255),
    socket_type VARCHAR(50),
    price INT,
    min_price INT,
    max_price INT,
    integrated_graphics BOOLEAN,
    stock_cooler BOOLEAN
);

-- 2. Create the case_sizes table
CREATE TABLE case_sizes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_size VARCHAR(50)
);

-- 3. Create the motherboards table
CREATE TABLE motherboards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    socket_type VARCHAR(50),
    form_factor VARCHAR(50), -- e.g., ITX, mATX, ATX
    price INT,
    case_size_id INT,
    FOREIGN KEY (case_size_id) REFERENCES case_sizes(id)
);

-- 4. Create the power_supplies table
CREATE TABLE power_supplies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    wattage INT,
    certification VARCHAR(50), -- e.g., 80+ Bronze, Gold
    price INT,
    case_size_id INT,
    FOREIGN KEY (case_size_id) REFERENCES case_sizes(id)
);

-- 5. Create the GPUs table
CREATE TABLE gpus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(255),
    price INT,
    case_size_id INT,
    FOREIGN KEY (case_size_id) REFERENCES case_sizes(id)
);

-- 6. Create the cooling_systems table
CREATE TABLE cooling_systems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(50), -- e.g., Air, Liquid, Stock
    compatible_sockets VARCHAR(255),
    price INT
);

-- 7. Create the RAM table
CREATE TABLE ram (
    id INT AUTO_INCREMENT PRIMARY KEY,
    size VARCHAR(50), -- e.g., 8GB, 16GB
    type VARCHAR(20) DEFAULT 'DDR4',
    price INT
);

-- 8. Create the storage table
CREATE TABLE storage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50), -- HDD or SSD
    capacity INT, -- in GB
    price INT
);

-- 9. Create the components table (revised)
CREATE TABLE components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    component_type TEXT CHECK(component_type IN ('CPU', 'Motherboard', 'Power Supply', 'GPU', 'Cooling System', 'RAM', 'Storage', 'Case Size')),
    reference_id INTEGER
);

-- 10. Case size options
INSERT INTO case_sizes (case_size) VALUES
('Mini Tower'),
('Mid Tower'),
('Full Tower'),
('No Preference');

-- 11. Example CPU entries
INSERT INTO cpus (brand, series, name, socket_type, price, min_price, max_price, integrated_graphics, stock_cooler) VALUES
('Intel', 'i3', 'Intel Core i3-12100', 'LGA1700', 8000, 8000, 9500, 1, 1),
('Intel', 'i5', 'Intel Core i5-13600K', 'LGA1700', 28000, 28000, 35000, 1, 0),
('Intel', 'i9', 'Intel Core i9-13900K', 'LGA1700', 43000, 43000, 48000, 1, 0),
('AMD', 'Ryzen 5', 'AMD Ryzen 5 7600X', 'AM5', 17000, 17000, 20000, 1, 0),
('AMD', 'Ryzen 9', 'AMD Ryzen 9 7950X', 'AM5', 55000, 55000, 60000, 0, 0);

-- 12. Insert AMD CPUs (example)
INSERT INTO cpus (brand, series, name, socket_type, price, min_price, max_price, integrated_graphics, stock_cooler) VALUES
('AMD', 'Ryzen 3', 'AMD Ryzen 3 7300X', 'AM5', 9500, 9500, 12000, 0, 0),
('AMD', 'Ryzen 7', 'AMD Ryzen 7 7800X3D', 'AM5', 30000, 30000, 35000, 0, 0);

-- 13. Insert motherboards (example)
INSERT INTO motherboards (name, socket_type, form_factor, price, case_size_id) VALUES
('Intel Z690 ITX Motherboard', 'LGA1700', 'ITX', 10000, 1),
('Intel Z690 mATX Motherboard', 'LGA1700', 'mATX', 12000, 2),
('Intel Z690 ATX Motherboard', 'LGA1700', 'ATX', 15000, 3),
('Intel Z790 ATX Motherboard', 'LGA1700', 'ATX', 17000, 3),
('Intel Z790 E-ATX Motherboard', 'LGA1700', 'EATX', 20000, 4);

-- 14. Insert power supplies (example)
INSERT INTO power_supplies (name, wattage, certification, price, case_size_id) VALUES
('Corsair 450W ITX PSU', 450, '80+ Bronze', 4000, 1),
('Corsair 550W mATX PSU', 550, '80+ Bronze', 5000, 2),
('Corsair 650W ATX PSU', 650, '80+ Gold', 6500, 3),
('Corsair 750W ATX PSU', 750, '80+ Gold', 8000, 3),
('Corsair 850W E-ATX PSU', 850, '80+ Platinum', 10000, 4);

-- 15. Insert GPUs (example for CPUs without integrated graphics)
INSERT INTO gpus (brand, model, price, case_size_id) VALUES
('NVIDIA', 'GTX 1650', 15000, 2),
('NVIDIA', 'GTX 1660', 20000, 2),
('NVIDIA', 'RTX 3060', 30000, 3),
('NVIDIA', 'RTX 3070', 40000, 3);

-- 16. Insert cooling systems (example)
INSERT INTO cooling_systems (name, type, compatible_sockets, price) VALUES
('Cooler Master Hyper 212', 'Air', 'LGA1700,AM5', 2500),
('Noctua NH-U12S', 'Air', 'LGA1700,AM5', 4000),
('Corsair iCUE H100i', 'Liquid', 'LGA1700,AM5', 8000),
('NZXT Kraken X73', 'Liquid', 'LGA1700,AM5', 12000),
('Corsair iCUE H150i', 'Liquid', 'LGA1700,AM5', 15000);

-- 17. Insert RAM options
INSERT INTO ram (size, type, price) VALUES
('8GB', 'DDR4', 4000),
('16GB', 'DDR4', 7000),
('32GB', 'DDR4', 12000),
('64GB', 'DDR4', 20000),
('16GB', 'DDR5', 10000),
('32GB', 'DDR5', 18000);

-- 18. Insert storage options
INSERT INTO storage (type, capacity, price) VALUES
('HDD', 1000, 4000),
('SSD', 500, 7000),
('SSD', 1000, 12000),
('NVMe', 500, 10000),
('NVMe', 1000, 18000);

-- 19. Now populate the components table with data from all other tables
-- Insert CPUs
INSERT INTO components (name, component_type, reference_id)
SELECT CONCAT(brand, ' ', series, ' ', name), 'CPU', id FROM cpus;

-- Insert Motherboards
INSERT INTO components (name, component_type, reference_id)
SELECT name, 'Motherboard', id FROM motherboards;

-- Insert Power Supplies
INSERT INTO components (name, component_type, reference_id)
SELECT name, 'Power Supply', id FROM power_supplies;

-- Insert GPUs
INSERT INTO components (name, component_type, reference_id)
SELECT CONCAT(brand, ' ', model), 'GPU', id FROM gpus;

-- Insert Cooling Systems
INSERT INTO components (name, component_type, reference_id)
SELECT name, 'Cooling System', id FROM cooling_systems;

-- Insert RAM
INSERT INTO components (name, component_type, reference_id)
SELECT CONCAT(size, ' ', type), 'RAM', id FROM ram;

-- Insert Storage
INSERT INTO components (name, component_type, reference_id)
SELECT CONCAT(type, ' ', capacity, 'GB'), 'Storage', id FROM storage;

-- Insert Case Sizes
INSERT INTO components (name, component_type, reference_id)
SELECT case_size, 'Case Size', id FROM case_sizes;