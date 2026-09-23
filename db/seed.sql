TRUNCATE categories, users, suppliers, customers, products, purchases, purchase_items, orders, order_items RESTART IDENTITY CASCADE;

-- 1. Insert Categories
INSERT INTO categories (name, description) VALUES
('Keyboards & Mice', 'Wired and wireless keyboards, optical mice, and gaming peripherals'),
('Storage Devices', 'Pendrives, external hard drives, NVMe SSDs, and memory cards'),
('Cables & Adapters', 'HDMI cables, USB-C hubs, DisplayPort adapters, and ethernet cables'),
('Audio Accessories', 'Wired headsets, Bluetooth earphones, and desktop speakers'),
('Monitors & Displays', 'Full HD, 4K, and gaming monitors'),
('Power & Surge Protection', 'UPS units, spike guards, power banks, and laptop chargers'),
('Networking & Wireless', 'Wi-Fi adapters, routers, and ethernet switches'),
('Laptop Accessories', 'Cooling pads, laptop stands, sleeves, and cleaning kits');

-- 2. Insert Users (Default password for all seeded users: admin123)
INSERT INTO users (username, email, password_hash, role) VALUES
('rajesh_admin', 'rajesh.sharma@techstore.in', '$2b$12$nP6yhKfakOVri.MJJNH9.u6axtKGSIIzP4axheWm06zqNeJXOOyc6', 'admin'),
('priya_mgr', 'priya.patel@techstore.in', '$2b$12$nP6yhKfakOVri.MJJNH9.u6axtKGSIIzP4axheWm06zqNeJXOOyc6', 'manager'),
('amit_cashier', 'amit.verma@techstore.in', '$2b$12$nP6yhKfakOVri.MJJNH9.u6axtKGSIIzP4axheWm06zqNeJXOOyc6', 'cashier'),
('sneha_cashier', 'sneha.kulkarni@techstore.in', '$2b$12$nP6yhKfakOVri.MJJNH9.u6axtKGSIIzP4axheWm06zqNeJXOOyc6', 'cashier');

-- 3. Insert Suppliers
INSERT INTO suppliers (company_name, contact_name, email, phone, address) VALUES
('Redington India Ltd', 'Vikram Mehta', 'v.mehta@redington.co.in', '+91 98400 12345', 'Guindy Industrial Estate, Chennai, Tamil Nadu'),
('Ingram Micro India Pvt Ltd', 'Suresh Nair', 'suresh.nair@ingrammicro.in', '+91 98200 54321', 'Andheri East, Mumbai, Maharashtra'),
('Savex Technologies Pvt Ltd', 'Ananya Rao', 'ananya.rao@savex.in', '+91 98800 67890', 'Koramangala, Bengaluru, Karnataka'),
('Rashi Peripherals Ltd', 'Manish Shah', 'manish.s@rptechindia.com', '+91 98190 11223', 'Nariman Point, Mumbai, Maharashtra'),
('Supertron Electronics Pvt Ltd', 'Debabrata Das', 'd.das@supertronindia.com', '+91 98300 44556', 'Salt Lake, Kolkata, West Bengal');

-- 4. Insert Customers
INSERT INTO customers (first_name, last_name, email, phone) VALUES
('Rohan', 'Gupta', 'rohan.gupta@gmail.com', '+91 98111 22334'),
('Deepika', 'Sundaram', 'deepika.s@outlook.com', '+91 98444 55667'),
('Aarav', 'Reddy', 'aarav.reddy@yahoo.in', '+91 97333 44556'),
('Meera', 'Joshi', 'meera.j@gmail.com', '+91 99000 11223'),
('Siddharth', 'Agarwal', 'siddharth.a@gmail.com', '+91 98765 43210'),
('Kavya', 'Nair', 'kavya.nair@gmail.com', '+91 98450 99887'),
('Aditya', 'Chopra', 'aditya.c@outlook.com', '+91 98100 88776'),
('Ananya', 'Iyer', 'ananya.iyer@gmail.com', '+91 98401 22334'),
('Vikram', 'Singh', 'vikram.singh@yahoo.com', '+91 98290 66778'),
('Pooja', 'Deshmukh', 'pooja.d@gmail.com', '+91 98220 33445'),
('Karan', 'Malhotra', 'karan.m@gmail.com', '+91 98180 55443'),
('Rhea', 'Banerjee', 'rhea.b@outlook.com', '+91 98310 77665');

-- 5. Insert Products
INSERT INTO products (category_id, supplier_id, name, sku, description, cost_price, selling_price, stock_quantity, low_stock_threshold) VALUES
-- Keyboards & Mice
(1, 1, 'Logitech B100 Optical Wired Mouse', 'LOG-B100-BLK', 'USB plug-and-play optical mouse, 800 DPI', 280.00, 399.00, 45, 10),
(1, 1, 'Zebronics Transformer Gaming Keyboard', 'ZEB-TR-KBD', 'Multicolor LED backlit wired USB gaming keyboard', 850.00, 1299.00, 20, 10),
(1, 1, 'HP X1000 Wired Optical Mouse', 'HP-X1000-MSE', 'Sleek 3-button USB mouse with 1600 DPI', 310.00, 449.00, 30, 10),
(1, 4, 'Dell KB216 Wired Multimedia Keyboard', 'DELL-KB216-BLK', 'Chiclet key design USB keyboard', 620.00, 899.00, 25, 10),

-- Storage Devices
(2, 4, 'SanDisk Cruzer Blade 64GB USB 2.0 Flash Drive', 'SND-64GB-USB', 'Compact design flash drive for data storage', 380.00, 549.00, 6, 10), -- Low Stock
(2, 4, 'Kingston DataTraveler Exodia 128GB USB 3.2', 'KNG-128GB-USB3', 'High-speed USB 3.2 Gen 1 pen drive', 550.00, 799.00, 40, 10),
(2, 2, 'WD Elements 1TB External Hard Drive', 'WDB-1TB-HDD', 'USB 3.0 portable external hard disk drive', 3200.00, 4299.00, 15, 5),
(2, 2, 'Crucial BX500 500GB 2.5-inch SATA SSD', 'CRU-500GB-SSD', 'Up to 540 MB/s sequential read internal SSD', 2100.00, 2899.00, 18, 5),

-- Cables & Adapters
(3, 1, 'Quantum QHM6633 4-Port USB Hub', 'QNM-HUB-4P', 'High-speed 4-port USB 2.0 extension hub', 150.00, 299.00, 4, 10), -- Low Stock
(3, 3, 'Portronics Mux 10-in-1 USB-C Hub', 'PRT-MUX-TYPEC', '4K HDMI, 100W PD charging, SD reader, USB 3.0', 1800.00, 2499.00, 12, 5),
(3, 3, 'Belkin HDMI to VGA Adapter Cable', 'BLK-HDMI-VGA', 'Male to female adapter with audio support', 650.00, 999.00, 22, 5),
(3, 5, 'AmazonBasics High-Speed HDMI Cable 2.0 (2m)', 'AMZ-HDMI-2M', '18Gbps gold-plated HDMI cable', 250.00, 449.00, 50, 15),

-- Audio Accessories
(4, 3, 'boAt Bassheads 100 Wired Earphones', 'BOAT-BH100-BLK', 'In-ear wired earphones with inline mic', 290.00, 499.00, 35, 15),
(4, 3, 'JBL Wave Flex True Wireless Earbuds', 'JBL-WAVE-FLEX', 'Bluetooth TWS earbuds with 32h playback', 1800.00, 2799.00, 14, 5),
(4, 5, 'Sennheiser HD 206 Over-Ear Headphones', 'SENN-HD206-BLK', 'Powerful sound reproduction with noise attenuation', 1350.00, 1890.00, 10, 5),
(4, 5, 'Creative Pebble 2.0 USB Desktop Speakers', 'CRT-PEBBLE-20', 'Far-field drivers with 45-degree elevation', 1100.00, 1599.00, 16, 5),

-- Monitors & Displays
(5, 2, 'Dell 24-inch SE2422H Full HD Monitor', 'DELL-24-SE2422H', '1080p FHD VA panel monitor with HDMI & VGA', 7200.00, 9499.00, 12, 5),
(5, 2, 'LG 27-inch Ultragear Gaming Monitor (144Hz)', 'LG-27-ULTRAGR', '1ms IPS panel with AMD FreeSync Premium', 12500.00, 15999.00, 8, 3),
(5, 5, 'Samsung 24-inch Curved FHD Monitor', 'SAMSUNG-24-CRV', '1800R curvature with slim design', 8100.00, 10499.00, 10, 3),

-- Power & Surge Protection
(6, 1, 'APC Back-UPS BX600C-IN 600VA 230V UPS', 'APC-600VA-UPS', 'Uninterruptible power supply for home desktop PC', 2400.00, 3299.00, 15, 5),
(6, 3, 'Belkin 3-Socket Surge Protector Board', 'BLK-3S-SURGE', '650 Joules surge suppressor with 1.5m cord', 950.00, 1499.00, 15, 5),
(6, 3, 'Ambrane 20000mAh Power Bank 20W', 'AMB-20K-PWRBNK', 'Type-C fast charging metallic power bank', 1150.00, 1699.00, 25, 8),

-- Networking & Wireless
(7, 2, 'TP-Link TL-WN725N 150Mbps USB Wi-Fi Adapter', 'TPL-N150-NANO', 'Mini Wi-Fi dongle for PC desktop', 350.00, 529.00, 18, 10),
(7, 2, 'Netgear R6080 Wi-Fi Router AC1000', 'NTG-AC1000-RTR', 'Dual-band Wi-Fi router for home streaming', 1450.00, 2199.00, 11, 5),
(7, 4, 'D-Link 8-Port Gigabit Unmanaged Switch', 'DLK-8P-SWITCH', 'Plug-and-play metal casing desktop switch', 1100.00, 1549.00, 14, 5),

-- Laptop Accessories
(8, 3, 'Portronics My Buddy K Adjustable Laptop Stand', 'PRT-BUDDYK-STND', 'Ergonomic aluminum portable stand', 520.00, 849.00, 30, 8),
(8, 5, 'Cosmic Byte Asteroid 5-Fan Laptop Cooling Pad', 'CB-ASTEROID-PAD', 'Supports laptops up to 17-inch with dual USB ports', 900.00, 1349.00, 9, 5),
(8, 1, 'Lapcare Multi-Functional Laptop Cleaning Kit', 'LPC-CLEAN-KIT', '7-in-1 keyboard brush and screen spray kit', 120.00, 249.00, 50, 15);

-- 6. Insert Purchases (Stock-In Batches)
INSERT INTO purchases (supplier_id, created_by_user_id, purchase_date, total_amount, status) VALUES
(1, 2, '2026-08-10 10:30:00', 41850.00, 'Received'),
(2, 2, '2026-08-15 14:15:00', 187000.00, 'Received'),
(4, 2, '2026-08-20 11:00:00', 77300.00, 'Received'),
(3, 2, '2026-08-25 16:30:00', 82000.00, 'Received');

-- 7. Insert Purchase Items
INSERT INTO purchase_items (purchase_id, product_id, quantity, unit_cost) VALUES
-- Batch 1
(1, 1, 50, 280.00), -- Logitech Mouse
(1, 2, 25, 850.00), -- Zebronics Kbd
(1, 9, 30, 220.00), -- USB Hub (Total: 41,850)

-- Batch 2
(2, 17, 10, 7200.00), -- Dell Monitor
(2, 18, 10, 11500.00),-- LG Gaming Monitor (Total: 1,87,000)

-- Batch 3
(3, 5, 40, 380.00),  -- SanDisk Pendrive
(3, 6, 30, 550.00),  -- Kingston Pendrive
(3, 7, 15, 3040.00), -- WD Hard Drive (Total: 77,300)

-- Batch 4
(4, 13, 50, 290.00), -- boAt Earphones
(4, 14, 20, 1800.00),-- JBL Earbuds
(4, 20, 13, 2400.00);-- APC UPS (Total: 82,000)

-- 8. Insert Sales Orders (10 Orders)
INSERT INTO orders (customer_id, processed_by_user_id, order_date, total_amount, status) VALUES
(1, 3, '2026-09-01 11:20:00', 1698.00, 'Completed'),
(2, 4, '2026-09-02 14:45:00', 10998.00, 'Completed'),
(3, 3, '2026-09-03 16:05:00', 1597.00, 'Completed'),
(4, 4, '2026-09-04 10:15:00', 2147.00, 'Completed'),
(5, 3, '2026-09-05 17:30:00', 3348.00, 'Completed'),
(6, 4, '2026-09-06 12:00:00', 16448.00, 'Completed'),
(7, 3, '2026-09-07 15:10:00', 4748.00, 'Completed'),
(8, 4, '2026-09-08 18:25:00', 5396.00, 'Completed'),
(9, 3, '2026-09-09 11:40:00', 3848.00, 'Completed'),
(10, 4, '2026-09-10 13:50:00', 13847.00, 'Completed');

-- 9. Insert Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
-- Order 1
(1, 1, 1, 399.00),   -- Logitech Mouse
(1, 2, 1, 1299.00),  -- Zebronics Kbd (Total: 1,698)

-- Order 2
(2, 17, 1, 9499.00), -- Dell Monitor
(2, 21, 1, 1499.00), -- Belkin Surge Board (Total: 10,998)

-- Order 3
(3, 5, 2, 549.00),   -- 2x SanDisk Flash Drive
(3, 13, 1, 499.00),  -- boAt Earphones (Total: 1,597)

-- Order 4
(4, 6, 1, 799.00),   -- Kingston 128GB
(4, 27, 1, 1348.00), -- 1x Cooling Pad (Total: 2,147)

-- Order 5
(5, 10, 1, 2499.00), -- Portronics USB-C Hub
(5, 26, 1, 849.00),  -- Laptop Stand (Total: 3,348)

-- Order 6
(6, 18, 1, 15999.00),-- LG Gaming Monitor
(6, 3, 1, 449.00),   -- HP Mouse (Total: 16,448)

-- Order 7
(7, 7, 1, 4299.00),  -- WD 1TB HDD
(7, 12, 1, 449.00),  -- HDMI Cable (Total: 4,748)

-- Order 8
(8, 14, 1, 2799.00), -- JBL TWS Earbuds
(8, 22, 1, 1699.00), -- Ambrane Power Bank
(8, 1, 2, 399.00),   -- 2x Logitech Mouse (Total: 5,396)

-- Order 9
(9, 20, 1, 3299.00), -- APC 600VA UPS
(9, 23, 1, 529.00),  -- TP-Link Wi-Fi Adapter (Total: 3,848)

-- Order 10
(10, 19, 1, 10499.00),-- Samsung Curved Monitor
(10, 24, 1, 2199.00), -- Netgear Router
(10, 4, 1, 899.00);   -- Dell Keyboard (Total: 13,847)