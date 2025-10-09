-- CNC Machine A Troubleshooting and Resolution Data
-- Machine ID: 09ce4fec-8de8-4c1e-a987-9a0080313456

-- 1. Machine Troubleshooting/Diagnostics for CNC Machine A
INSERT INTO machine_troubleshooting (machine_id, machine_name, issue_type, severity_level, symptoms, possible_causes, recommended_actions, estimated_downtime_hours, required_parts, required_skills, priority_level) VALUES 

-- Vibration Issues
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'vibration', 'critical', 'Excessive vibration during operation, poor surface finish, unusual noise, tool chatter', 
 ARRAY['Worn spindle bearings', 'Misaligned tool holder', 'Loose mounting bolts', 'Unbalanced cutting tool', 'Worn ball screws', 'Damaged spindle taper'],
 ARRAY['Stop machine immediately', 'Check spindle bearing condition', 'Inspect tool holder alignment', 'Tighten all mounting bolts', 'Replace cutting tool', 'Schedule maintenance', 'Check spindle taper'],
 4, ARRAY['Spindle bearings', 'Tool holder', 'Mounting bolts', 'Cutting tool'], ARRAY['Mechanical repair', 'Precision alignment'], 1),

-- Temperature Issues
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'temperature', 'high', 'Spindle overheating, thermal shutdowns, poor cutting quality, excessive heat generation',
 ARRAY['Insufficient coolant flow', 'Clogged coolant lines', 'Faulty temperature sensor', 'Worn spindle bearings', 'Overloaded spindle', 'Dirty coolant'],
 ARRAY['Check coolant system', 'Clean coolant lines', 'Replace temperature sensor', 'Inspect spindle bearings', 'Reduce cutting parameters', 'Change coolant'],
 2, ARRAY['Temperature sensor', 'Coolant filters', 'Spindle bearings'], ARRAY['System maintenance', 'Coolant system repair'], 2),

-- Current/Power Issues
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'current', 'critical', 'High current draw, motor overheating, frequent circuit breaker trips, power fluctuations',
 ARRAY['Faulty motor windings', 'Loose electrical connections', 'Worn motor brushes', 'Overloaded spindle', 'Power supply issues', 'Short circuit'],
 ARRAY['Shutdown machine immediately', 'Check motor windings', 'Inspect electrical connections', 'Replace motor brushes', 'Check power supply', 'Call electrician'],
 6, ARRAY['Motor brushes', 'Electrical connectors', 'Power supply unit'], ARRAY['Electrical repair', 'Motor maintenance'], 1),

-- Accuracy Issues
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'accuracy', 'medium', 'Poor dimensional accuracy, inconsistent cuts, positioning errors, backlash issues',
 ARRAY['Worn ball screws', 'Loose gibs', 'Worn linear guides', 'Backlash in drive system', 'Encoder problems', 'Mechanical wear'],
 ARRAY['Check ball screw condition', 'Adjust gibs', 'Inspect linear guides', 'Compensate for backlash', 'Check encoder', 'Schedule calibration'],
 3, ARRAY['Ball screws', 'Linear guides', 'Gibs'], ARRAY['Precision alignment', 'Calibration'], 3),

-- Surface Finish Issues
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'surface_finish', 'medium', 'Poor surface finish, tool marks, chatter marks, inconsistent finish quality',
 ARRAY['Dull cutting tools', 'Incorrect cutting parameters', 'Tool holder issues', 'Spindle vibration', 'Workpiece clamping problems', 'Coolant issues'],
 ARRAY['Replace cutting tools', 'Optimize cutting parameters', 'Check tool holder', 'Address vibration issues', 'Improve workpiece clamping', 'Check coolant'],
 1, ARRAY['Cutting tools', 'Tool holder'], ARRAY['Tooling expertise', 'Process optimization'], 4);

-- 2. Maintenance Procedures for CNC Machine A
INSERT INTO maintenance_procedures (machine_id, machine_name, procedure_name, procedure_type, description, steps, estimated_duration_minutes, required_tools, required_parts, safety_requirements, skill_level_required, frequency_days) VALUES 

-- Spindle Bearing Replacement
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Spindle Bearing Replacement', 'corrective', 'Replace worn spindle bearings to eliminate vibration and ensure smooth operation',
 '{"steps": [
   {"step": 1, "action": "Power down machine and lock out", "duration": 5},
   {"step": 2, "action": "Remove spindle housing cover", "duration": 15},
   {"step": 3, "action": "Extract old bearings using bearing puller", "duration": 30},
   {"step": 4, "action": "Clean bearing seats thoroughly", "duration": 20},
   {"step": 5, "action": "Install new bearings with proper preload", "duration": 45},
   {"step": 6, "action": "Reassemble spindle housing", "duration": 25},
   {"step": 7, "action": "Test run and verify smooth operation", "duration": 15}
 ]}'::jsonb,
 155, ARRAY['Bearing puller', 'Torque wrench', 'Dial indicator', 'Clean rags'], ARRAY['Spindle bearings', 'Grease', 'Seals'], ARRAY['Lockout/tagout', 'Safety glasses', 'Gloves'], 'expert', NULL),

-- Ball Screw Maintenance
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Ball Screw Maintenance', 'preventive', 'Clean, lubricate, and inspect ball screws for wear and proper operation',
 '{"steps": [
   {"step": 1, "action": "Power down and lock out machine", "duration": 5},
   {"step": 2, "action": "Remove way covers", "duration": 20},
   {"step": 3, "action": "Clean ball screws with solvent", "duration": 30},
   {"step": 4, "action": "Inspect for wear and damage", "duration": 25},
   {"step": 5, "action": "Apply proper lubrication", "duration": 15},
   {"step": 6, "action": "Check backlash", "duration": 20},
   {"step": 7, "action": "Reassemble and test", "duration": 15}
 ]}'::jsonb,
 130, ARRAY['Solvent', 'Lubrication gun', 'Dial indicator', 'Wrenches'], ARRAY['Ball screw grease', 'Way covers'], ARRAY['Lockout/tagout', 'Safety glasses'], 'intermediate', 90),

-- Coolant System Maintenance
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Coolant System Maintenance', 'preventive', 'Clean and maintain coolant system for optimal performance and tool life',
 '{"steps": [
   {"step": 1, "action": "Drain existing coolant", "duration": 10},
   {"step": 2, "action": "Remove and clean filters", "duration": 20},
   {"step": 3, "action": "Flush system with cleaning solution", "duration": 30},
   {"step": 4, "action": "Inspect pump and hoses", "duration": 15},
   {"step": 5, "action": "Refill with fresh coolant", "duration": 10},
   {"step": 6, "action": "Test system operation", "duration": 10}
 ]}'::jsonb,
 95, ARRAY['Filter wrench', 'Cleaning solution', 'Pump'], ARRAY['Coolant filters', 'Fresh coolant'], ARRAY['Gloves', 'Eye protection'], 'beginner', 30),

-- Tool Holder Maintenance
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Tool Holder Maintenance', 'preventive', 'Clean and inspect tool holders for proper clamping and alignment',
 '{"steps": [
   {"step": 1, "action": "Remove all tools from holders", "duration": 5},
   {"step": 2, "action": "Clean holder tapers", "duration": 15},
   {"step": 3, "action": "Inspect for damage or wear", "duration": 20},
   {"step": 4, "action": "Check clamping force", "duration": 10},
   {"step": 5, "action": "Lubricate moving parts", "duration": 10},
   {"step": 6, "action": "Test clamping operation", "duration": 5}
 ]}'::jsonb,
 65, ARRAY['Cleaning solvent', 'Lubricant', 'Force gauge'], ARRAY['Tool holder grease'], ARRAY['Gloves'], 'beginner', 14),

-- Emergency Shutdown Procedure
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Emergency Shutdown Procedure', 'emergency', 'Immediate shutdown procedure for critical failures',
 '{"steps": [
   {"step": 1, "action": "Press emergency stop button", "duration": 1},
   {"step": 2, "action": "Turn off main power switch", "duration": 2},
   {"step": 3, "action": "Lock out power source", "duration": 3},
   {"step": 4, "action": "Assess situation and call supervisor", "duration": 5},
   {"step": 5, "action": "Document incident", "duration": 10}
 ]}'::jsonb,
 21, ARRAY['Lockout device', 'Emergency stop button'], ARRAY[], ARRAY['Emergency procedures', 'Communication'], 'beginner', NULL);

-- 3. Parts Inventory for CNC Machine A
INSERT INTO machine_parts_inventory (machine_id, machine_name, part_name, part_number, current_stock, minimum_stock, maximum_stock, unit_cost, supplier, lead_time_days, is_critical) VALUES 

-- Critical Spindle Parts
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Spindle Bearings', 'SB-7205', 2, 1, 5, 450.00, 'Precision Bearings Inc', 7, TRUE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Spindle Motor', 'SM-5HP', 1, 1, 2, 2500.00, 'Motor Solutions', 14, TRUE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Spindle Taper', 'ST-BT40', 1, 1, 3, 1200.00, 'Spindle Tech', 10, TRUE),

-- Tooling System
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Tool Holder', 'TH-ER32', 5, 2, 10, 125.00, 'Tooling Solutions', 3, FALSE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Collet Set', 'CS-ER32', 3, 2, 6, 85.00, 'Tooling Solutions', 2, FALSE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'End Mill Set', 'EM-HSS', 8, 5, 15, 45.00, 'Cutting Tools Co', 3, FALSE),

-- Motion System
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Ball Screw Assembly', 'BS-1605', 1, 1, 3, 850.00, 'Linear Motion Co', 14, TRUE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Linear Guides', 'LG-HG25', 2, 1, 4, 320.00, 'Linear Motion Co', 10, TRUE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Servo Motor', 'SM-2KW', 1, 1, 2, 1800.00, 'Motor Solutions', 12, TRUE),

-- Electrical Components
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Temperature Sensor', 'TS-PT100', 3, 2, 6, 65.00, 'Sensor Tech', 5, FALSE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Encoder', 'ENC-2500', 2, 1, 3, 280.00, 'Encoder Systems', 8, TRUE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Power Supply', 'PS-24V-10A', 1, 1, 2, 180.00, 'Power Systems', 7, TRUE),

-- Coolant System
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Coolant Pump', 'CP-1HP', 1, 1, 2, 450.00, 'Pump Solutions', 10, FALSE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Coolant Filters', 'CF-10', 8, 5, 15, 25.00, 'Filtration Systems', 2, FALSE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Coolant Hoses', 'CH-1/2', 4, 2, 8, 15.00, 'Hose Systems', 3, FALSE),

-- Safety and Control
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Emergency Stop Button', 'ESB-RED', 2, 1, 3, 35.00, 'Safety Systems', 4, TRUE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Limit Switches', 'LS-M18', 6, 3, 10, 45.00, 'Sensor Tech', 5, FALSE),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Control Panel', 'CP-MAIN', 1, 1, 1, 1200.00, 'Control Systems', 21, TRUE);

-- 4. Issue History for CNC Machine A
INSERT INTO machine_issue_history (machine_id, machine_name, issue_description, issue_type, severity_level, reported_by, reported_at, resolved_at, resolution_description, resolution_steps, parts_used, downtime_hours, cost_of_repair, technician_name, status) VALUES 

-- Previous vibration issue
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Excessive vibration during precision cutting operations affecting surface finish', 'vibration', 'high', 'John Smith', '2025-01-05 08:30:00', '2025-01-05 14:45:00', 'Replaced worn spindle bearings and realigned tool holder', 
 ARRAY['Diagnosed vibration source', 'Replaced spindle bearings', 'Realigned tool holder', 'Performed test cuts', 'Verified smooth operation'], 
 ARRAY['Spindle Bearings SB-7205'], 6.25, 450.00, 'Mike Johnson', 'resolved'),

-- Previous temperature issue
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Spindle overheating causing thermal shutdowns during long operations', 'temperature', 'critical', 'Sarah Wilson', '2025-01-07 10:15:00', '2025-01-07 12:30:00', 'Cleaned coolant system and replaced temperature sensor',
 ARRAY['Diagnosed overheating cause', 'Cleaned coolant filters', 'Replaced temperature sensor', 'Tested system operation', 'Verified temperature stability'],
 ARRAY['Temperature Sensor TS-PT100', 'Coolant Filters CF-10'], 2.25, 90.00, 'David Brown', 'resolved'),

-- Previous accuracy issue
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'Poor dimensional accuracy and positioning errors in X-axis', 'accuracy', 'medium', 'Tom Davis', '2025-01-03 14:20:00', '2025-01-04 09:15:00', 'Adjusted ball screw backlash and recalibrated system',
 ARRAY['Diagnosed accuracy issues', 'Measured backlash', 'Adjusted ball screw', 'Recalibrated encoders', 'Performed accuracy tests'],
 ARRAY[], 18.92, 0.00, 'Mike Johnson', 'resolved'),

-- Current open issue
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'High current draw and motor overheating during heavy cutting operations', 'current', 'critical', 'Lisa Chen', '2025-01-09 11:45:00', NULL, NULL,
 ARRAY['Initial diagnosis in progress'], 
 ARRAY[], 0.00, 0.00, 'David Brown', 'open');

-- 5. Performance Benchmarks for CNC Machine A
INSERT INTO machine_performance_benchmarks (machine_id, machine_name, parameter_name, normal_min_value, normal_max_value, warning_min_value, warning_max_value, critical_min_value, critical_max_value, unit) VALUES 

-- Vibration benchmarks
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'vibration', 0.5, 2.0, 2.0, 4.0, 4.0, 10.0, 'mm/s'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'spindle_vibration', 0.3, 1.5, 1.5, 3.0, 3.0, 8.0, 'mm/s'),

-- Temperature benchmarks
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'spindle_temperature', 20.0, 45.0, 45.0, 60.0, 60.0, 80.0, '°C'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'motor_temperature', 25.0, 50.0, 50.0, 65.0, 65.0, 85.0, '°C'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'coolant_temperature', 18.0, 35.0, 35.0, 45.0, 45.0, 60.0, '°C'),

-- Current/Power benchmarks
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'spindle_current', 8.0, 15.0, 15.0, 20.0, 20.0, 25.0, 'A'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'servo_current', 5.0, 12.0, 12.0, 18.0, 18.0, 22.0, 'A'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'total_power', 2.0, 4.5, 4.5, 6.0, 6.0, 8.0, 'kW'),

-- Accuracy benchmarks
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'positioning_accuracy', 0.005, 0.01, 0.01, 0.02, 0.02, 0.05, 'mm'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'repeatability', 0.002, 0.005, 0.005, 0.01, 0.01, 0.02, 'mm'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'backlash', 0.001, 0.003, 0.003, 0.005, 0.005, 0.01, 'mm'),

-- Pressure benchmarks
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'coolant_pressure', 1.5, 3.0, 3.0, 4.0, 4.0, 5.0, 'bar'),
('09ce4fec-8de8-4c1e-a987-9a0080313456', 'CNC Machine A', 'air_pressure', 4.0, 6.0, 6.0, 7.0, 7.0, 8.0, 'bar');

-- Verify the data for CNC Machine A
SELECT 'CNC Machine A Troubleshooting Data' as summary;
SELECT 'machine_troubleshooting' as table_name, COUNT(*) as record_count FROM machine_troubleshooting WHERE machine_id = '09ce4fec-8de8-4c1e-a987-9a0080313456'
UNION ALL
SELECT 'maintenance_procedures', COUNT(*) FROM maintenance_procedures WHERE machine_id = '09ce4fec-8de8-4c1e-a987-9a0080313456'
UNION ALL
SELECT 'machine_parts_inventory', COUNT(*) FROM machine_parts_inventory WHERE machine_id = '09ce4fec-8de8-4c1e-a987-9a0080313456'
UNION ALL
SELECT 'machine_issue_history', COUNT(*) FROM machine_issue_history WHERE machine_id = '09ce4fec-8de8-4c1e-a987-9a0080313456'
UNION ALL
SELECT 'machine_performance_benchmarks', COUNT(*) FROM machine_performance_benchmarks WHERE machine_id = '09ce4fec-8de8-4c1e-a987-9a0080313456';
