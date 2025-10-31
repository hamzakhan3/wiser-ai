# Inference Data Tables - What Was Shown on UI

## Overview

When using the **local database**, the Inspection/Anomaly page fetched real-time sensor data from two tables that were **excluded** from the cloud migration. Here's what was displayed:

---

## Table 1: `inference_data` (Single-Value Sensor Data)

### Purpose
Stores **single-value sensor readings** over time, primarily for vibration sensors.

### Table Structure
```sql
- id: integer (Primary Key)
- timestamp: timestamp (Reading time)
- value: double precision (Sensor reading)
- run_id: uuid (Analysis run identifier)
- machine_id: uuid (Foreign key to machine table)
- sensor_type: varchar(50) (Type of sensor)
```

### Local Database Records
**Total Records:** 205,916 vibration sensor readings

### Sample Data (CNC Machine A)
```
Timestamp           | Value  | Sensor Type | Machine
--------------------|--------|-------------|------------------
2024-03-01 08:00:00 | 82.2   | vibration   | CNC Machine A
2024-03-01 08:00:05 | 82.2   | vibration   | CNC Machine A
2024-03-01 08:00:10 | 82.2   | vibration   | CNC Machine A
```

- **Reading Frequency:** Every 5 seconds
- **Data Range:** March 2024 onwards
- **Measurement:** Vibration in mm/s (millimeters per second)

### What Was Displayed on UI

**Page:** Inspection/Anomaly Page for CNC Machine A

**Graph Type:** Line Chart (Single Line)

**Display:**
- **X-Axis:** Time (timestamp)
- **Y-Axis:** Vibration (mm/s)
- **Data Points:** ~205,000+ readings (downsampled to every 4th point = ~51,000 points)
- **Anomaly Zones:** Red highlighted areas showing when vibration exceeded normal thresholds
- **Title:** "CNC Machine A - Vibration Sensor Data"

**User Experience:**
- Smooth continuous line showing vibration levels over time
- Clear visualization of when machine vibration spiked
- Anomaly detection zones overlaid on the graph
- Ability to zoom and pan through historical data

---

## Table 2: `inference_data_multi` (Multi-Value Sensor Data)

### Purpose
Stores **multi-value sensor readings** over time, primarily for 3-phase current sensors.

### Table Structure
```sql
- id: integer (Primary Key)
- timestamp: timestamp (Reading time)
- value1: double precision (Phase 1 current)
- value2: double precision (Phase 2 current)
- value3: double precision (Phase 3 current)
- run_id: uuid (Analysis run identifier)
- machine_id: uuid (Foreign key to machine table)
- sensor_type: varchar(50) (Type of sensor)
```

### Local Database Records
**Total Records:** 1,560,269 current sensor readings (520,089 per phase)

### Sample Data (Metal Lathe - Precision Pro)
```
Timestamp           | Phase 1 | Phase 2 | Phase 3 | Sensor | Machine
--------------------|---------|---------|---------|--------|-------------------------
2024-06-05 00:00:00 | 32.42 A | 13.70 A | 25.88 A | current| Metal Lathe - Precision Pro
2024-06-05 00:00:05 | 32.29 A | 15.26 A | 20.09 A | current| Metal Lathe - Precision Pro
2024-06-05 00:00:10 | 36.06 A | 14.42 A | 22.73 A | current| Metal Lathe - Precision Pro
```

- **Reading Frequency:** Every 5 seconds
- **Data Range:** June 2024 onwards  
- **Measurement:** Current in Amperes (A) for 3 electrical phases

### What Was Displayed on UI

**Page:** Inspection/Anomaly Page for Metal Lathe - Precision Pro

**Graph Type:** Line Chart (Three Lines)

**Display:**
- **X-Axis:** Time (timestamp)
- **Y-Axis:** Current (A)
- **Three Lines:**
  - Line 1 (Blue): Phase 1 current
  - Line 2 (Green): Phase 2 current  
  - Line 3 (Red): Phase 3 current
- **Data Points:** ~1.5M readings (downsampled to every 100th point = ~15,600 points)
- **Anomaly Zones:** Red highlighted areas showing when current exceeded normal ranges
- **Title:** "Metal Lathe - Precision Pro - Current Sensor Data"

**User Experience:**
- Three overlaid lines showing electrical current for each phase
- Easy identification of phase imbalances
- Clear visualization of power consumption patterns
- Anomaly detection when current spiked abnormally
- Ability to zoom and pan through historical data

---

## Backend Data Processing

### For CNC Machine A (Vibration)
**Endpoint:** `GET /inspection?machine_id=09ce4fec-8de8-4c1e-a987-9a0080313456&sensor_type=Vibration`

**Query:**
```python
SELECT timestamp, value 
FROM inference_data
WHERE machine_id = '09ce4fec-8de8-4c1e-a987-9a0080313456'
ORDER BY timestamp
```

**Downsampling:** Every 4th record (`[::4]`)
- Raw: 205,916 records
- Sent to UI: ~51,479 records

**Response Format:**
```json
{
  "title": "CNC Machine A - Vibration Sensor Data",
  "x_label": "Time",
  "y_label": "Vibration (mm/s)",
  "data_type": "single",
  "vibration_data": [
    {"timestamp": "2024-03-01T08:00:00Z", "value": 82.2},
    {"timestamp": "2024-03-01T08:00:20Z", "value": 82.2},
    ...
  ],
  "anomalies": [...]
}
```

### For Metal Lathe (Current)
**Endpoint:** `GET /inspection?machine_id=a8795833-ca35-4fef-b9c9-a02e2cc00e0f&sensor_type=Current`

**Query:**
```python
SELECT timestamp, value1, value2, value3
FROM inference_data_multi
WHERE machine_id = 'a8795833-ca35-4fef-b9c9-a02e2cc00e0f'
ORDER BY timestamp
```

**Downsampling:** Every 100th record (`[::100]`)
- Raw: 1,560,269 records
- Sent to UI: ~15,603 records

**Response Format:**
```json
{
  "title": "Metal Lathe - Precision Pro - Current Sensor Data",
  "x_label": "Time",
  "y_label": "Current (A)",
  "data_type": "multi",
  "multi_value_data": [
    {"timestamp": "2024-06-05T00:00:00Z", "value1": 32.42, "value2": 13.7, "value3": 25.88},
    {"timestamp": "2024-06-05T00:08:20Z", "value1": 32.29, "value2": 15.26, "value3": 20.09},
    ...
  ],
  "anomalies": [...]
}
```

---

## Frontend Display (InspectionPage.tsx)

### Recharts Line Chart Component

**For Single-Value Data (Vibration):**
```jsx
<Line
  type="monotone"
  dataKey="value"
  stroke="#8884d8"
  dot={false}
  isAnimationActive={false}
/>
```

**For Multi-Value Data (Current - 3 phases):**
```jsx
<Line type="monotone" dataKey="value1" stroke="#8884d8" dot={false} />
<Line type="monotone" dataKey="value2" stroke="#82ca9d" dot={false} />
<Line type="monotone" dataKey="value3" stroke="#ffc658" dot={false} />
```

**Anomaly Highlighting:**
```jsx
{anomalies.map((anomaly, idx) => (
  <ReferenceArea
    key={idx}
    x1={new Date(anomaly.start).getTime()}
    x2={new Date(anomaly.end).getTime()}
    fill="red"
    fillOpacity={0.3}
  />
))}
```

---

## Current State (Cloud Database)

### What's Missing
❌ `inference_data` table is **empty** on cloud
❌ `inference_data_multi` table is **empty** on cloud

### Impact on UI
When visiting the Inspection/Anomaly page now:

**CNC Machine A:**
- Graph loads but shows **no data** (empty line chart)
- Title displays correctly: "CNC Machine A - Vibration Sensor Data"
- Axes are visible but no line is drawn
- Anomaly zones still show (hardcoded test data)

**Metal Lathe - Precision Pro:**
- Graph loads but shows **no data** (empty line chart)
- Title displays correctly: "Metal Lathe - Precision Pro - Current Sensor Data"
- Axes are visible but no lines are drawn
- Anomaly zones still show (hardcoded test data)

---

## Data Size Comparison

| Table | Local Records | Data Volume | Cloud Records |
|-------|---------------|-------------|---------------|
| `inference_data` | 205,916 | ~50 MB | 0 (excluded) |
| `inference_data_multi` | 1,560,269 | ~400 MB | 0 (excluded) |
| **Total** | **1,766,185** | **~450 MB** | **0** |

---

## Why These Tables Were Excluded

1. **Large Data Volume:** ~450 MB of sensor data (1.7M+ records)
2. **Rapid Growth:** These tables grow continuously with real-time sensor readings
3. **Not Essential for Demo:** Core app functionality (machine health, charts, work orders) works without them
4. **Can Be Populated Later:** Easy to migrate when needed
5. **Cost Optimization:** AWS RDS storage costs scale with data size

---

## How to Populate These Tables on Cloud (If Needed)

### Option 1: Full Data Migration
```bash
# Export from local
pg_dump -U postgres -d postgres --data-only \
  -t inference_data -t inference_data_multi \
  > inference_sensor_data.sql

# Import to cloud (will take ~2-3 minutes for 450MB)
PGPASSWORD=yourpassword psql -h 3.90.156.11 -U postgres -d postgres \
  -f inference_sensor_data.sql
```

### Option 2: Recent Data Only (Last 30 Days)
```bash
# Export only recent data to reduce size
pg_dump -U postgres -d postgres --data-only \
  -t inference_data -t inference_data_multi \
  --where="timestamp >= NOW() - INTERVAL '30 days'" \
  > inference_recent_data.sql

# Import to cloud
PGPASSWORD=yourpassword psql -h 3.90.156.11 -U postgres -d postgres \
  -f inference_recent_data.sql
```

### Option 3: Generate Sample Data
Create a smaller dataset for demo purposes instead of migrating all 1.7M records.

---

## Summary

**What Users Saw (Local DB):**
- Real-time sensor graphs with 1.7M+ data points
- Smooth visualization of vibration and current readings
- Historical data from March-June 2024
- Anomaly detection zones overlaid

**What Users See Now (Cloud DB):**
- Empty graphs on Inspection pages
- All other features working perfectly
- Machine health dashboard fully functional
- Charts and analytics working with other data

**Recommendation:**
- For production: Migrate recent data (last 30-90 days)
- For demo: Current state is sufficient
- For full historical analysis: Migrate all data

The application is **fully functional** without this data. The inspection graphs are the only feature impacted, and this can be remedied anytime with a simple data migration.

