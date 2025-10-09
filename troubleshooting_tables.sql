-- Create troubleshooting and resolution tables for machine issue resolution

-- 1. Machine Troubleshooting/Diagnostics Table
CREATE TABLE IF NOT EXISTS machine_troubleshooting (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id UUID NOT NULL,
    machine_name VARCHAR(255) NOT NULL,
    issue_type VARCHAR(100) NOT NULL,
    severity_level VARCHAR(20) NOT NULL,
    symptoms TEXT NOT NULL,
    possible_causes TEXT[] NOT NULL,
    recommended_actions TEXT[] NOT NULL,
    estimated_downtime_hours INTEGER,
    required_parts TEXT[],
    required_skills TEXT[],
    priority_level INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Machine Maintenance Procedures Table
CREATE TABLE IF NOT EXISTS maintenance_procedures (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id UUID NOT NULL,
    machine_name VARCHAR(255) NOT NULL,
    procedure_name VARCHAR(255) NOT NULL,
    procedure_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    steps JSONB NOT NULL,
    estimated_duration_minutes INTEGER,
    required_tools TEXT[],
    required_parts TEXT[],
    safety_requirements TEXT[],
    skill_level_required VARCHAR(20),
    frequency_days INTEGER,
    last_performed TIMESTAMP,
    next_due TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Machine Parts Inventory Table
CREATE TABLE IF NOT EXISTS machine_parts_inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id UUID NOT NULL,
    machine_name VARCHAR(255) NOT NULL,
    part_name VARCHAR(255) NOT NULL,
    part_number VARCHAR(100),
    current_stock INTEGER DEFAULT 0,
    minimum_stock INTEGER DEFAULT 1,
    maximum_stock INTEGER DEFAULT 10,
    unit_cost DECIMAL(10,2),
    supplier VARCHAR(255),
    lead_time_days INTEGER,
    is_critical BOOLEAN DEFAULT FALSE,
    last_ordered TIMESTAMP,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Machine Issue History Table
CREATE TABLE IF NOT EXISTS machine_issue_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id UUID NOT NULL,
    machine_name VARCHAR(255) NOT NULL,
    issue_description TEXT NOT NULL,
    issue_type VARCHAR(100) NOT NULL,
    severity_level VARCHAR(20) NOT NULL,
    reported_by VARCHAR(255),
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    resolution_description TEXT,
    resolution_steps TEXT[],
    parts_used TEXT[],
    downtime_hours DECIMAL(5,2),
    cost_of_repair DECIMAL(10,2),
    technician_name VARCHAR(255),
    status VARCHAR(20) DEFAULT 'open'
);

-- 5. Machine Performance Benchmarks Table
CREATE TABLE IF NOT EXISTS machine_performance_benchmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id UUID NOT NULL,
    machine_name VARCHAR(255) NOT NULL,
    parameter_name VARCHAR(100) NOT NULL,
    normal_min_value DECIMAL(10,3),
    normal_max_value DECIMAL(10,3),
    warning_min_value DECIMAL(10,3),
    warning_max_value DECIMAL(10,3),
    critical_min_value DECIMAL(10,3),
    critical_max_value DECIMAL(10,3),
    unit VARCHAR(20),
    measurement_frequency_minutes INTEGER DEFAULT 5,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample troubleshooting data
INSERT INTO machine_troubleshooting (machine_id, machine_name, issue_type, severity_level, symptoms, possible_causes, recommended_actions, estimated_downtime_hours, required_parts, required_skills, priority_level) VALUES 
-- CNC Machine A - Vibration Issues
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'vibration', 'critical', 'Excessive vibration during operation, poor surface finish, unusual noise', 
 ARRAY['Worn spindle bearings', 'Misaligned tool holder', 'Loose mounting bolts', 'Unbalanced cutting tool', 'Worn ball screws'],
 ARRAY['Stop machine immediately', 'Check spindle bearing condition', 'Inspect tool holder alignment', 'Tighten all mounting bolts', 'Replace cutting tool', 'Schedule maintenance'],
 4, ARRAY['Spindle bearings', 'Tool holder', 'Mounting bolts'], ARRAY['Mechanical repair', 'Precision alignment'], 1),

-- Wire EDM - Temperature Issues  
('178d85b5-856a-424f-b066-7ae31a9705c7', 'Wire EDM - AccuteX', 'temperature', 'high', 'Overheating during operation, thermal shutdowns, poor cutting quality',
 ARRAY['Clogged coolant system', 'Faulty temperature sensor', 'Insufficient coolant flow', 'Worn wire guide', 'Dirty dielectric fluid'],
 ARRAY['Check coolant system', 'Clean filters', 'Replace temperature sensor', 'Inspect wire guide', 'Change dielectric fluid'],
 2, ARRAY['Temperature sensor', 'Coolant filters', 'Wire guide'], ARRAY['Electrical repair', 'System maintenance'], 2),

-- CNC Router - Current Issues
('7f7967c3-fc68-48fa-aea9-b3cf89e82c62', 'CNC Router - ShopBot', 'current', 'critical', 'High current draw, motor overheating, frequent circuit breaker trips',
 ARRAY['Faulty motor windings', 'Loose electrical connections', 'Worn motor brushes', 'Overloaded spindle', 'Power supply issues'],
 ARRAY['Shutdown machine', 'Check motor windings', 'Inspect electrical connections', 'Replace motor brushes', 'Check power supply'],
 6, ARRAY['Motor brushes', 'Electrical connectors', 'Power supply unit'], ARRAY['Electrical repair', 'Motor maintenance'], 1);

-- Insert sample maintenance procedures
INSERT INTO maintenance_procedures (machine_id, machine_name, procedure_name, procedure_type, description, steps, estimated_duration_minutes, required_tools, required_parts, safety_requirements, skill_level_required, frequency_days) VALUES 
-- CNC Machine A - Spindle Bearing Replacement
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Spindle Bearing Replacement', 'corrective', 'Replace worn spindle bearings to eliminate vibration issues',
 '{"steps": [
   {"step": 1, "action": "Power down machine and lock out", "duration": 5},
   {"step": 2, "action": "Remove spindle housing cover", "duration": 15},
   {"step": 3, "action": "Extract old bearings using bearing puller", "duration": 30},
   {"step": 4, "action": "Clean bearing seats thoroughly", "duration": 20},
   {"step": 5, "action": "Install new bearings with proper preload", "duration": 45},
   {"step": 6, "action": "Reassemble spindle housing", "duration": 25},
   {"step": 7, "action": "Test run and verify smooth operation", "duration": 15}
 ]}'::jsonb,
 155, ARRAY['Bearing puller', 'Torque wrench', 'Dial indicator'], ARRAY['Spindle bearings', 'Grease'], ARRAY['Lockout/tagout', 'Safety glasses'], 'expert', NULL),

-- Wire EDM - Coolant System Maintenance
('178d85b5-856a-424f-b066-7ae31a9705c7', 'Wire EDM - AccuteX', 'Coolant System Maintenance', 'preventive', 'Clean and maintain coolant system for optimal performance',
 '{"steps": [
   {"step": 1, "action": "Drain existing coolant", "duration": 10},
   {"step": 2, "action": "Remove and clean filters", "duration": 20},
   {"step": 3, "action": "Flush system with cleaning solution", "duration": 30},
   {"step": 4, "action": "Inspect pump and hoses", "duration": 15},
   {"step": 5, "action": "Refill with fresh coolant", "duration": 10},
   {"step": 6, "action": "Test system operation", "duration": 10}
 ]}'::jsonb,
 95, ARRAY['Filter wrench', 'Cleaning solution'], ARRAY['Coolant filters', 'Fresh coolant'], ARRAY['Gloves', 'Eye protection'], 'intermediate', 30);

-- Insert sample parts inventory
INSERT INTO machine_parts_inventory (machine_id, machine_name, part_name, part_number, current_stock, minimum_stock, maximum_stock, unit_cost, supplier, lead_time_days, is_critical) VALUES 
-- CNC Machine A parts
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Spindle Bearings', 'SB-7205', 2, 1, 5, 450.00, 'Precision Bearings Inc', 7, TRUE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Tool Holder', 'TH-ER32', 5, 2, 10, 125.00, 'Tooling Solutions', 3, FALSE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Ball Screw Assembly', 'BS-1605', 1, 1, 3, 850.00, 'Linear Motion Co', 14, TRUE),

-- Wire EDM parts
('178d85b5-856a-424f-b066-7ae31a9705c7', 'Wire EDM - AccuteX', 'Temperature Sensor', 'TS-100', 3, 2, 6, 85.00, 'Sensor Tech', 5, TRUE),
('178d85b5-856a-424f-b066-7ae31a9705c7', 'Wire EDM - AccuteX', 'Coolant Filters', 'CF-10', 8, 5, 15, 25.00, 'Filtration Systems', 2, FALSE),
('178d85b5-856a-424f-b066-7ae31a9705c7', 'Wire EDM - AccuteX', 'Wire Guide', 'WG-0.25', 4, 2, 8, 45.00, 'EDM Parts Co', 4, FALSE),

-- CNC Router parts
('7f7967c3-fc68-48fa-aea9-b3cf89e82c62', 'CNC Router - ShopBot', 'Motor Brushes', 'MB-550', 6, 3, 12, 35.00, 'Motor Parts Inc', 3, FALSE),
('7f7967c3-fc68-48fa-aea9-b3cf89e82c62', 'CNC Router - ShopBot', 'Power Supply Unit', 'PSU-24V', 1, 1, 2, 320.00, 'Power Systems', 10, TRUE);

-- Insert sample issue history
INSERT INTO machine_issue_history (machine_id, machine_name, issue_description, issue_type, severity_level, reported_by, reported_at, resolved_at, resolution_description, resolution_steps, parts_used, downtime_hours, cost_of_repair, technician_name, status) VALUES 
-- CNC Machine A - Previous vibration issue
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Excessive vibration during precision cutting operations', 'vibration', 'high', 'John Smith', '2025-01-05 08:30:00', '2025-01-05 14:45:00', 'Replaced worn spindle bearings and realigned tool holder', 
 ARRAY['Diagnosed vibration source', 'Replaced spindle bearings', 'Realigned tool holder', 'Performed test cuts'], 
 ARRAY['Spindle Bearings SB-7205'], 6.25, 450.00, 'Mike Johnson', 'resolved'),

-- Wire EDM - Previous temperature issue
('178d85b5-856a-424f-b066-7ae31a9705c7', 'Wire EDM - AccuteX', 'Machine overheating and thermal shutdowns', 'temperature', 'critical', 'Sarah Wilson', '2025-01-07 10:15:00', '2025-01-07 12:30:00', 'Cleaned coolant system and replaced temperature sensor',
 ARRAY['Diagnosed overheating cause', 'Cleaned coolant filters', 'Replaced temperature sensor', 'Tested system operation'],
 ARRAY['Temperature Sensor TS-100', 'Coolant Filters CF-10'], 2.25, 110.00, 'David Brown', 'resolved');

-- Insert sample performance benchmarks
INSERT INTO machine_performance_benchmarks (machine_id, machine_name, parameter_name, normal_min_value, normal_max_value, warning_min_value, warning_max_value, critical_min_value, critical_max_value, unit) VALUES 
-- CNC Machine A benchmarks
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'vibration', 0.5, 2.0, 2.0, 4.0, 4.0, 10.0, 'mm/s'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'temperature', 20.0, 45.0, 45.0, 60.0, 60.0, 80.0, '°C'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'current', 8.0, 15.0, 15.0, 20.0, 20.0, 25.0, 'A'),

-- Wire EDM benchmarks
('178d85b5-856a-424f-b066-7ae31a9705c7', 'Wire EDM - AccuteX', 'temperature', 18.0, 35.0, 35.0, 50.0, 50.0, 70.0, '°C'),
('178d85b5-856a-424f-b066-7ae31a9705c7', 'Wire EDM - AccuteX', 'current', 12.0, 25.0, 25.0, 35.0, 35.0, 45.0, 'A'),
('178d85b5-856a-424f-b066-7ae31a9705c7', 'Wire EDM - AccuteX', 'pressure', 2.0, 4.0, 4.0, 6.0, 6.0, 8.0, 'bar'),

-- CNC Router benchmarks
('7f7967c3-fc68-48fa-aea9-b3cf89e82c62', 'CNC Router - ShopBot', 'current', 10.0, 18.0, 18.0, 25.0, 25.0, 30.0, 'A'),
('7f7967c3-fc68-48fa-aea9-b3cf89e82c62', 'CNC Router - ShopBot', 'temperature', 25.0, 50.0, 50.0, 65.0, 65.0, 80.0, '°C'),
('7f7967c3-fc68-48fa-aea9-b3cf89e82c62', 'CNC Router - ShopBot', 'vibration', 1.0, 3.0, 3.0, 5.0, 5.0, 8.0, 'mm/s');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_troubleshooting_machine ON machine_troubleshooting(machine_id, issue_type);
CREATE INDEX IF NOT EXISTS idx_procedures_machine ON maintenance_procedures(machine_id, procedure_type);
CREATE INDEX IF NOT EXISTS idx_parts_machine ON machine_parts_inventory(machine_id, is_critical);
CREATE INDEX IF NOT EXISTS idx_issues_machine ON machine_issue_history(machine_id, status);
CREATE INDEX IF NOT EXISTS idx_benchmarks_machine ON machine_performance_benchmarks(machine_id, parameter_name);

-- Verify the data
SELECT 'machine_troubleshooting' as table_name, COUNT(*) as record_count FROM machine_troubleshooting
UNION ALL
SELECT 'maintenance_procedures', COUNT(*) FROM maintenance_procedures
UNION ALL
SELECT 'machine_parts_inventory', COUNT(*) FROM machine_parts_inventory
UNION ALL
SELECT 'machine_issue_history', COUNT(*) FROM machine_issue_history
UNION ALL
SELECT 'machine_performance_benchmarks', COUNT(*) FROM machine_performance_benchmarks;
