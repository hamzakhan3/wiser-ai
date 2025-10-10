-- Create table to store machine vision analysis results
CREATE TABLE IF NOT EXISTS machine_vision_analysis (
    id SERIAL PRIMARY KEY,
    machine_id UUID NOT NULL,
    image_path TEXT NOT NULL,
    analysis_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(machine_id, image_path)
);

-- Insert the hardcoded analysis for CNC Machine A
INSERT INTO machine_vision_analysis (machine_id, image_path, analysis_text) 
VALUES (
    '09ce4fec-8de8-4c1e-a987-9a0080313456',
    '/Users/khanhamza/Desktop/image3.png',
    'Based on the vibration sensor data from the CNC machine and the detected anomalies, here are the top five likely causes for the anomalies:

- **Imbalance**: Uneven weight distribution in rotating components can cause increased vibration levels, indicating a potential imbalance in the machine.

- **Misalignment**: Components such as couplings, shafts, or pulleys might be misaligned, leading to periodic increases in vibration.

- **Bearing Wear**: Worn or damaged bearings can lead to irregular vibration patterns, which may correlate with the observed anomalies.

- **Resonance**: The machine could be amplifying vibrations at certain frequencies, possibly corresponding with the operational times highlighted in the anomalies.

- **Component Looseness**: Looseness in machine parts, such as bolts or mounts, can cause intermittent spikes in vibration, potentially matching the detected anomalies.'
) ON CONFLICT (machine_id, image_path) DO UPDATE SET
    analysis_text = EXCLUDED.analysis_text,
    updated_at = CURRENT_TIMESTAMP;

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_machine_vision_analysis_machine_id ON machine_vision_analysis(machine_id);
CREATE INDEX IF NOT EXISTS idx_machine_vision_analysis_image_path ON machine_vision_analysis(image_path);
