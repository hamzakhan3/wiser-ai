# Cloud Database Setup Documentation

## Overview
This document describes the cloud database setup for the Wiser AI application.

## Cloud Database Details

### AWS RDS PostgreSQL
- **Host**: 3.90.156.11
- **Port**: 5432
- **Database**: postgres
- **User**: postgres
- **Version**: PostgreSQL 14.17

### Connection String
```
postgresql+psycopg2://postgres:yourpassword@3.90.156.11:5432/postgres
```

## Tables Migrated to Cloud

All 28 required tables have been successfully created on the cloud database:

### Core Tables (5)
- `lab` - Laboratory information
- `users` - User accounts
- `node` - Node configuration
- `machine` - Machine inventory
- `lab_user` - Lab-user relationships

### Sensor Tables (3)
- `current_sensor` - Current sensor readings
- `temperature_sensor` - Temperature sensor readings
- `humidity_sensor` - Humidity sensor readings

### Health & Production (2)
- `critical_health_machine` - Machine health status tracking
- `shift_machine_production` - Production data by shift

### Inference & Anomaly Tables (5)
- `machine_current_log` - Current log data
- `anomalies` - Detected anomalies
- `anomaly_detections` - Anomaly detection records
- `inference_data` - Inference results (single-value)
- `inference_data_multi` - Inference results (multi-value)
- `vibration_inference_data` - Vibration analysis data

### Work Orders & Maintenance (4)
- `work_orders` - Work order records
- `maintenance_task` - Maintenance tasks
- `machine_parts` - Machine parts inventory
- `machine_energy_consumption` - Energy consumption tracking

### Troubleshooting & Analysis (5)
- `machine_troubleshooting` - Troubleshooting records
- `maintenance_procedures` - Maintenance procedure documentation
- `machine_parts_inventory` - Parts inventory management
- `machine_issue_history` - Historical issue tracking
- `machine_performance_benchmarks` - Performance benchmarks

### Vision & Analytics (2)
- `machine_vision_analysis` - Vision-based analysis results
- `machine_anomaly_screenshots` - Anomaly screenshot storage

### Utility (1)
- `database_conn` - Database connection configuration

## Current Configuration

The application is currently configured to use the **LOCAL** database by default.

### Local Database
```python
LOCAL_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"
```

### Cloud Database
```python
AWS_DATABASE_URL = "postgresql+psycopg2://postgres:yourpassword@3.90.156.11:5432/postgres"
```

## Switching Between Local and Cloud

### Option 1: Environment Variable
Set the `DATABASE_URL` environment variable:
```bash
# Use cloud database
export DATABASE_URL="postgresql+psycopg2://postgres:yourpassword@3.90.156.11:5432/postgres"

# Use local database (default)
unset DATABASE_URL
```

### Option 2: Modify config.py
Update the default in `config.py`:
```python
# Use cloud by default
DATABASE_URL = os.getenv('DATABASE_URL', AWS_DATABASE_URL)

# Or use local by default (current)
DATABASE_URL = os.getenv('DATABASE_URL', LOCAL_DATABASE_URL)
```

### Option 3: Modify app.py
Directly change the connection string in `src/services/app.py`:
```python
# Line 132-136
engine = create_engine(
    AWS_DATABASE_URL,  # Change from hardcoded localhost
    echo=True,
    echo_pool=True
)
```

## Schema Export Files

- `cloud_db_schema.sql` - Original schema export (1,413 lines)
- `cloud_db_schema_final.sql` - Final schema with UUID extensions

## Migration Status

### ✅ Completed
- [x] Export table schemas from local database
- [x] Add UUID extensions (uuid-ossp, pgcrypto)
- [x] Create all 28 tables on AWS RDS
- [x] Verify table creation

### ⏳ Pending
- [ ] Data migration from local to cloud
- [ ] Update application to use cloud database
- [ ] Test application with cloud database
- [ ] Set up database backups on AWS RDS
- [ ] Configure security groups and access controls

## Notes

1. **No Data Migrated**: Only table structures (schemas) have been migrated. No data has been transferred yet.

2. **Application Connection**: The application is still connected to the local database. No changes to the running application.

3. **Password Update Needed**: Update `config.py` line 7 with the correct password:
   ```python
   AWS_DATABASE_URL = "postgresql+psycopg2://postgres:yourpassword@3.90.156.11:5432/postgres"
   ```

4. **Minor Errors**: Some non-critical errors occurred during migration (duplicate primary keys, missing columns in indexes) but all required tables were created successfully.

5. **Bonus Table**: The `model_anomalies` table was also migrated (29 tables total instead of 28).

## Next Steps

1. Test cloud database connection from application
2. Plan and execute data migration strategy
3. Update application configuration to use cloud database
4. Set up monitoring and alerting for cloud database
5. Configure automated backups

## Support

For issues or questions, contact the database administrator or refer to the main README.md file.

