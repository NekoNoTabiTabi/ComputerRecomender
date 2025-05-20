--Get-Content ".\schema.sql" | sqlite3 "components.db"

CREATE TABLE cpus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    series VARCHAR(50),
    name VARCHAR(255),
    socket_type VARCHAR(50),
    required_watt INT,
    price INT
);


CREATE TABLE cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_size VARCHAR(50),
    form_factor_compatability VARCHAR(50),
    name VARCHAR(255),
    price INT
);


CREATE TABLE motherboards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    socket_type VARCHAR(50),
    form_factor VARCHAR(50), -- e.g., ITX, mATX, ATX
    gpu_socket VARCHAR(50),
    required_watt INT,
    price INT
);


CREATE TABLE psus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    certification VARCHAR(50), 
    form_factor VARCHAR(50),
    watt_output INT,   
    price INT
);


CREATE TABLE gpus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(255),
    compatible_sockets VARCHAR(50),
    form_factor VARCHAR(50),
    required_watt INT,
    price INT
);


CREATE TABLE cooling_systems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    cooling_type VARCHAR(50), -- e.g., Air, Liquid, Stock
    compatible_sockets VARCHAR(255),
    required_watt INT,
    price INT
);


CREATE TABLE ram (
    id INT AUTO_INCREMENT PRIMARY KEY,
    size VARCHAR(50), 
    ram_type VARCHAR(20) DEFAULT 'DDR4',
    required_watt INT,
    price INT
);


CREATE TABLE storage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    storage_type VARCHAR(50), -- HDD or SSD
    capacity INT, -- in GB
    required_watt INT,
    price INT
);

--for future use if there is time
CREATE TABLE components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    component_type TEXT CHECK(component_type IN ('CPU', 'Motherboard', 'Power Supply', 'GPU', 'Cooling System', 'RAM', 'Storage', 'Cases')),
    reference_id INTEGER
);


INSERT INTO cases (case_size, form_factor_compatability, name, price) VALUES
('Mid Tower', 'ATX, Micro-ATX', 'NZXT H510', 4418),
('Full Tower', 'E-ATX, ATX, Micro-ATX', 'Corsair 7000D Airflow', 8314),
('Mini Tower', 'Mini-ITX, Micro-ATX', 'Cooler Master MasterBox Q300L', 3292),
('Mid Tower', 'ATX, Micro-ATX', 'Fractal Design Meshify C', 5524),
('Full Tower', 'E-ATX, ATX, Micro-ATX', 'Lian Li PC-O11 Dynamic', 11142),
('Mini Tower', 'Mini-ITX', 'Thermaltake Core V1', 3840),
('Mid Tower', 'ATX, Micro-ATX', 'Phanteks Eclipse P400A', 4977),
('Full Tower', 'E-ATX, ATX, Micro-ATX', 'be quiet! Dark Base Pro 900', 9997),
('Mini Tower', 'Mini-ITX', 'SilverStone SG13', 2734),
('Mid Tower', 'ATX, Micro-ATX', 'Cooler Master HAF 500', 6082);


INSERT INTO cpus (brand, series, name, socket_type, required_watt, price) VALUES
('Intel', 'Core i9', 'Intel Core i9-13900K', 'LGA1700', 125, 32862),
('Intel', 'Core i7', 'Intel Core i7-13700K', 'LGA1700', 105, 22822),
('Intel', 'Core i5', 'Intel Core i5-13600K', 'LGA1700', 125, 17800),
('AMD', 'Ryzen 9', 'AMD Ryzen 9 7950X', 'AM5', 170, 38912),
('AMD', 'Ryzen 7', 'AMD Ryzen 7 7700X', 'AM5', 105, 22262),
('AMD', 'Ryzen 5', 'AMD Ryzen 5 7600X', 'AM5', 105, 16684),
('Intel', 'Core i9', 'Intel Core i9-12900K', 'LGA1700', 125, 32862),
('Intel', 'Core i7', 'Intel Core i7-12700K', 'LGA1700', 125, 22822),
('Intel', 'Core i5', 'Intel Core i5-12600K', 'LGA1700', 125, 17800),
('Intel', 'Core i3', 'Intel Core i3-12100F', 'LGA1700', 58, 7200),
('AMD', 'Ryzen 9', 'AMD Ryzen 9 5950X', 'AM4', 105, 44574),
('AMD', 'Ryzen 7', 'AMD Ryzen 7 5800X', 'AM4', 105, 25050),
('AMD', 'Ryzen 5', 'AMD Ryzen 5 5600X', 'AM4', 65, 16684),
('AMD', 'Ryzen 3', 'AMD Ryzen 3 5300G', 'AM4', 65, 8311);


INSERT INTO motherboards (name, socket_type, form_factor, gpu_socket, required_watt, price) VALUES
('ASUS ROG Maximus Z790 Hero', 'LGA1700', 'ATX', 'PCIe 5.0 x16', 250, 27900),
('MSI MAG B760 Tomahawk WiFi', 'LGA1700', 'ATX', 'PCIe 4.0 x16', 180, 13400),
('Gigabyte Z690 AORUS Elite AX', 'LGA1700', 'ATX', 'PCIe 4.0 x16', 200, 15600),
('ASRock B550 Phantom Gaming 4', 'AM4', 'ATX', 'PCIe 3.0 x16', 150, 7800),
('MSI MEG X570 Unify', 'AM4', 'ATX', 'PCIe 4.0 x16', 220, 21300),
('ASUS TUF Gaming B550-Plus', 'AM4', 'ATX', 'PCIe 4.0 x16', 160, 9500),
('Gigabyte B650 AORUS Elite AX', 'AM5', 'ATX', 'PCIe 5.0 x16', 190, 16800),
('ASRock X670E Taichi', 'AM5', 'ATX', 'PCIe 5.0 x16', 250, 30100),
('MSI PRO B760M-P DDR4', 'LGA1700', 'mATX', 'PCIe 4.0 x16', 140, 5200),
('ASUS Prime B650M-A WiFi', 'AM5', 'mATX', 'PCIe 4.0 x16', 170, 11200),
('Gigabyte B550M DS3H', 'AM4', 'mATX', 'PCIe 3.0 x16', 130, 6900),
('ASRock X570 ITX/TB3', 'AM4', 'ITX', 'PCIe 4.0 x16', 180, 24500),
('ASUS ROG Strix Z790-I Gaming WiFi', 'LGA1700', 'ITX', 'PCIe 5.0 x16', 200, 19200),
('MSI MPG B650I Edge WiFi', 'AM5', 'ITX', 'PCIe 5.0 x16', 190, 16100);


-- make it so psu appears after calculating user's compont required watts PS: we be outputting badly
INSERT INTO psus (name, certification, form_factor, watt_output, price) VALUES
('Corsair RM750x', '80+ Gold', 'ATX', 750, 7520),
('EVGA SuperNOVA 850 G5', '80+ Gold', 'ATX', 850, 9460),
('Seasonic Focus GX-650', '80+ Gold', 'ATX', 650, 6700),
('Cooler Master MWE Gold 750', '80+ Gold', 'ATX', 750, 7250),
('ASUS ROG Thor 1200W', '80+ Platinum', 'ATX', 1200, 16740),
('MSI MPG A1000G', '80+ Gold', 'ATX', 1000, 11160),
('Gigabyte P650B', '80+ Bronze', 'ATX', 650, 5020),
('Thermaltake Toughpower GF1 850W', '80+ Gold', 'ATX', 850, 9460),
('SilverStone SX700-G', '80+ Gold', 'SFX', 700, 8370),
('Corsair SF600', '80+ Platinum', 'SFX', 600, 7250);



INSERT INTO gpus (brand, model, compatible_sockets, form_factor, required_watt, price) VALUES
('NVIDIA', 'GeForce RTX 4090', 'PCIe 4.0 x16', 'Triple Slot', 450, 167400),
('NVIDIA', 'GeForce RTX 4080', 'PCIe 4.0 x16', 'Triple Slot', 320, 111600),
('NVIDIA', 'GeForce RTX 4070 Ti', 'PCIe 4.0 x16', 'Dual Slot', 285, 83700),
('AMD', 'Radeon RX 7900 XTX', 'PCIe 4.0 x16', 'Triple Slot', 355, 111600),
('AMD', 'Radeon RX 7900 XT', 'PCIe 4.0 x16', 'Triple Slot', 300, 94600),
('AMD', 'Radeon RX 7800 XT', 'PCIe 4.0 x16', 'Dual Slot', 263, 72500),
('NVIDIA', 'GeForce RTX 4060 Ti', 'PCIe 4.0 x8', 'Dual Slot', 160, 50200),
('AMD', 'Radeon RX 7600', 'PCIe 4.0 x8', 'Dual Slot', 165, 38400),
('NVIDIA', 'GeForce RTX 3050', 'PCIe 4.0 x8', 'Dual Slot', 130, 32900),
('AMD', 'Radeon RX 6700 XT', 'PCIe 4.0 x16', 'Dual Slot', 230, 60800),
('NVIDIA', 'GeForce RTX 5090', 'PCIe 5.0 x16', 'Triple Slot', 575, 210000),
('NVIDIA', 'GeForce RTX 5080', 'PCIe 5.0 x16', 'Triple Slot', 360, 165000),
('NVIDIA', 'GeForce RTX 5070 Ti', 'PCIe 5.0 x16', 'Dual Slot', 300, 125000),
('AMD', 'Radeon RX 9070 XT', 'PCIe 5.0 x16', 'Triple Slot', 304, 135000),
('AMD', 'Radeon RX 9070', 'PCIe 5.0 x16', 'Dual Slot', 220, 110000),
('Intel', 'Arc Pro B60', 'PCIe 5.0 x16', 'Dual Slot', 200, 95000),
('Intel', 'Arc Pro B50', 'PCIe 5.0 x16', 'Dual Slot', 170, 85000),
('NVIDIA', 'GeForce RTX 5090 D', 'PCIe 5.0 x16', 'Triple Slot', 575, 215000),
('NVIDIA', 'GeForce RTX 5070', 'PCIe 5.0 x16', 'Dual Slot', 250, 120000),
('AMD', 'Radeon RX 9070 XT', 'PCIe 5.0 x16', 'Triple Slot', 304, 135000),
('AMD', 'Radeon RX 9070', 'PCIe 5.0 x16', 'Dual Slot', 220, 110000),
('Intel', 'Arc Pro B60', 'PCIe 5.0 x16', 'Dual Slot', 200, 95000),
('Intel', 'Arc Pro B50', 'PCIe 5.0 x16', 'Dual Slot', 170, 85000),
('NVIDIA', 'GeForce RTX 5080 Mobile', 'PCIe 5.0 x16', 'Laptop', 80, 95000),
('NVIDIA', 'GeForce RTX 5070 Ti Mobile', 'PCIe 5.0 x16', 'Laptop', 60, 85000),
('AMD', 'Radeon RX 9070 GRE', 'PCIe 5.0 x16', 'Triple Slot', 260, 125000),
('NVIDIA', 'GeForce RTX 5090 Laptop', 'PCIe 5.0 x16', 'Laptop', 150, 140000);

INSERT INTO cooling_systems (name, cooling_type, compatible_sockets, required_watt, price) VALUES
('Noctua NH-D15', 'Air', 'LGA1700, AM4, AM5', 10, 5580),
('Corsair iCUE H150i Elite Capellix', 'Liquid', 'LGA1700, AM4, AM5', 35, 8370),
('Cooler Master Hyper 212 Black Edition', 'Air', 'LGA1700, AM4', 8, 2790),
('NZXT Kraken X73', 'Liquid', 'LGA1700, AM4, AM5', 40, 11160),
('DeepCool AK620', 'Air', 'LGA1700, AM4, AM5', 12, 5020),
('Arctic Liquid Freezer II 280', 'Liquid', 'LGA1700, AM4, AM5', 38, 7250),
('be quiet! Dark Rock Pro 4', 'Air', 'LGA1700, AM4', 11, 3840),
('EVGA CLC 240mm', 'Liquid', 'LGA1700, AM4', 30, 6700),
('Thermaltake Floe DX RGB 360', 'Liquid', 'LGA1700, AM4, AM5', 42, 12500),
('Stock AMD Wraith Prism', 'Stock', 'AM4', 5, 0),
('Noctua NH-D15 G2', 'Air', 'LGA1700, AM4, AM5', 12, 6200),
('Corsair iCUE H170i Elite LCD XT', 'Liquid', 'LGA1700, AM4, AM5', 45, 13500),
('Cooler Master V8 Ace', 'Air', 'LGA1700, AM4, AM5', 15, 7500),
('NZXT Kraken Elite 420', 'Liquid', 'LGA1700, AM4, AM5', 50, 14500),
('DeepCool Assassin IV', 'Air', 'LGA1700, AM4, AM5', 14, 5800),
('Arctic Liquid Freezer III 360 A-RGB', 'Liquid', 'LGA1700, AM4, AM5', 42, 12800),
('be quiet! Silent Loop 2 360', 'Liquid', 'LGA1700, AM4, AM5', 40, 11000),
('EVGA CLCx 280mm', 'Liquid', 'LGA1700, AM4, AM5', 35, 8900),
('Thermaltake Pacific CL360 Max', 'Liquid', 'LGA1700, AM4, AM5', 48, 15500),
('Intel Direct Water Cooling Prototype', 'Liquid', 'LGA1700, AM4, AM5', 100, 20000);

INSERT INTO ram (size, ram_type, required_watt, price) VALUES
('8 GB', 'DDR4', 5, 2790),
('16 GB', 'DDR4', 8, 5020),
('32 GB', 'DDR4', 12, 8370),
('8 GB', 'DDR5', 6, 3840),
('16 GB', 'DDR5', 10, 7250),
('32 GB', 'DDR5', 15, 11160),
('64 GB', 'DDR4', 18, 16740),
('64 GB', 'DDR5', 20, 19200),
('128 GB', 'DDR4', 25, 27900),
('128 GB', 'DDR5', 30, 33480);

INSERT INTO storage (storage_type, capacity, required_watt, price) VALUES
('SSD', 256, 5, 2790),
('SSD', 512, 7, 5020),
('SSD', 1024, 10, 8370),
('HDD', 1000, 8, 3840),
('HDD', 2000, 12, 7250),
('HDD', 4000, 15, 11160),
('SSD', 2048, 12, 16740),
('SSD', 4096, 18, 19200),
('HDD', 8000, 20, 27900),
('SSD', 8192, 25, 33480);


INSERT INTO components (name, component_type, reference_id)
SELECT CONCAT(brand, ' ', series, ' ', name), 'CPU', id FROM cpus;


INSERT INTO components (name, component_type, reference_id)
SELECT name, 'Motherboard', id FROM motherboards;


INSERT INTO components (name, component_type, reference_id)
SELECT name, 'Power Supply', id FROM psus;


INSERT INTO components (name, component_type, reference_id)
SELECT CONCAT(brand, ' ', model), 'GPU', id FROM gpus;


INSERT INTO components (name, component_type, reference_id)
SELECT name, 'Cooling System', id FROM cooling_systems;


INSERT INTO components (name, component_type, reference_id)
SELECT CONCAT(size, ' ', ram_type), 'RAM', id FROM ram;


INSERT INTO components (name, component_type, reference_id)
SELECT CONCAT(storage_type, ' ', capacity, 'GB'), 'Storage', id FROM storage;


INSERT INTO components (name, component_type, reference_id)
SELECT name, 'Cases', id FROM cases;