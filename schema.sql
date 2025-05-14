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
    CONSTRAINT case_size_id FOREIGN KEY (id) REFERENCES case_sizes(id)
);

-- 4. Create the power_supplies table
CREATE TABLE power_supplies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    wattage INT,
    certification VARCHAR(50), -- e.g., 80+ Bronze, Gold
    price INT,
    case_size_id INT,
    CONSTRAINT case_size_id FOREIGN KEY (id) REFERENCES case_sizes(id)
);

-- 5. Create the GPUs table
CREATE TABLE gpus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(255),
    price INT,
    case_size_id INT,
    CONSTRAINT case_size_id FOREIGN KEY (id) REFERENCES case_sizes(id)
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

-- 9. Case size options
INSERT INTO case_sizes (case_size) VALUES
('Mini Tower'),
('Mid Tower'),
('Full Tower'),
('No Preference');

-- 10. Example CPU entries
INSERT INTO cpus (brand, series, name, socket_type, price, min_price, max_price, integrated_graphics, stock_cooler) VALUES
('Intel', 'i3', 'Intel Core i3-12100', 'LGA1700', 8000, 8000, 9500, 1, 1),
('Intel', 'i5', 'Intel Core i5-13600K', 'LGA1700', 28000, 28000, 35000, 1, 0),
('Intel', 'i9', 'Intel Core i9-13900K', 'LGA1700', 43000, 43000, 48000, 1, 0),
('AMD', 'Ryzen 5', 'AMD Ryzen 5 7600X', 'AM5', 17000, 17000, 20000, 1, 0),
('AMD', 'Ryzen 9', 'AMD Ryzen 9 7950X', 'AM5', 55000, 55000, 60000, 0, 0);


-- 11. Insert AMD CPUs (example)
INSERT INTO cpus (brand, series, name, price, min_price, max_price, integrated_graphics, stock_cooler) VALUES
('AMD', 'Ryzen 3', 'AMD Ryzen 3 7300X', 9500, 9500, 12000, 0, 0),
('AMD', 'Ryzen 5', 'AMD Ryzen 5 7600X', 17000, 17000, 20000, 1, 0),
('AMD', 'Ryzen 7', 'AMD Ryzen 7 7800X3D', 30000, 30000, 35000, 0, 0),
('AMD', 'Ryzen 9', 'AMD Ryzen 9 7950X', 55000, 55000, 60000, 0, 0);

-- 12. Insert motherboards (example)
INSERT INTO motherboards (id, case_size_id, name, price) VALUES
(1, 1, 'Intel Z690 ITX Motherboard', 10000),
(2, 2, 'Intel Z690 mATX Motherboard', 12000),
(3, 3, 'Intel Z690 ATX Motherboard', 15000),
(4, 3, 'Intel Z790 ATX Motherboard', 17000),
(5, 4, 'Intel Z790 E-ATX Motherboard', 20000);

-- 13. Insert power supplies (example)
INSERT INTO power_supplies (id, case_size_id, name, price, wattage) VALUES
(1, 1, 'Corsair 450W ITX PSU', 4000, 450),
(2, 2, 'Corsair 550W mATX PSU', 5000, 550),
(3, 3, 'Corsair 650W ATX PSU', 6500, 650),
(4, 3, 'Corsair 750W ATX PSU', 8000, 750),
(5, 4, 'Corsair 850W E-ATX PSU', 10000, 850);

-- 14. Insert GPUs (example for CPUs without integrated graphics)
INSERT INTO gpus (id, model, price) VALUES
(1, 'NVIDIA GTX 1650', 15000),
(2, 'NVIDIA GTX 1660', 20000),
(3, 'NVIDIA RTX 3060', 30000),
(4, 'NVIDIA RTX 3070', 40000);

-- 15. Insert cooling systems (example)
INSERT INTO cooling_systems (id, name, price) VALUES
(1, 'Cooler Master Hyper 212', 2500),
(2, 'Noctua NH-U12S', 4000),
(3, 'Corsair iCUE H100i', 8000),
(4, 'NZXT Kraken X73', 12000),
(5, 'Corsair iCUE H150i', 15000);

-- 16. Insert RAM options
INSERT INTO ram (size, price) VALUES
('8GB', 4000),
('16GB', 7000),
('32GB', 12000),
('64GB', 20000);

-- 17. Insert storage options
INSERT INTO storage (type, capacity, price) VALUES
('HDD', 1000, 4000),
('SSD', 500, 7000),
('SSD', 1000, 12000);
