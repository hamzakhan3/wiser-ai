from flask import Flask, request, jsonify
import json
from sqlalchemy import create_engine
import logging

# Disable SQLAlchemy verbose logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
from llama_index.core.indices.struct_store.sql import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from openai import OpenAI as OpenAIClient
import openai
from sqlalchemy import Table, MetaData, insert
from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from sqlalchemy import select, func, text, and_, update
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import insert
import uuid
from datetime import datetime
import base64
from dateutil import parser  
from datetime import date
from flask import Flask, Response, request, jsonify, stream_with_context
import time

import imagehash
from redis import Redis
from PIL import Image

# Matplotlib imports for chart generation
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import io
from threading import Thread


import hashlib
import os

redis = Redis()

def format_response_as_markdown(text):
    """Format AI response text as proper markdown"""
    if not text:
        return text
    
    import re
    
    # Start with the original text
    formatted_text = text
    
    # Add a main heading if the text starts with "Here is" or similar
    if re.match(r'^(Here is|Here are|The following|Below is)', formatted_text, re.IGNORECASE):
        formatted_text = "# " + formatted_text.split(':')[0] + "\n\n" + formatted_text
    
    # Convert numbered lists to proper markdown format
    # Pattern to match numbered lists like "1. Item 2. Item 3. Item"
    numbered_pattern = r'(\d+)\.\s+([^0-9]+?)(?=\s+\d+\.|$)'
    
    def replace_numbered_list(match):
        number = match.group(1)
        content = match.group(2).strip()
        # Extract machine name and description
        if ':' in content:
            parts = content.split(':', 1)
            machine_name = parts[0].strip()
            description = parts[1].strip()
            return f"{number}. **{machine_name}**: {description}"
        else:
            return f"{number}. **{content}**"
    
    # Apply the numbered list pattern
    formatted_text = re.sub(numbered_pattern, replace_numbered_list, formatted_text, flags=re.MULTILINE | re.DOTALL)
    
    # Add line breaks before numbered lists
    formatted_text = re.sub(r'(\d+\.\s)', r'\n\1', formatted_text)
    
    # Convert bullet points to proper markdown
    formatted_text = re.sub(r'^-\s+', r'- ', formatted_text, flags=re.MULTILINE)
    
    # Add line breaks before bullet points
    formatted_text = re.sub(r'(\n|^)(-\s)', r'\1\n\2', formatted_text)
    
    # Clean up multiple newlines
    formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text)
    
    # Add proper spacing around sections
    formatted_text = re.sub(r'(\n)([A-Z][^:]*:)(\n)', r'\1## \2\3', formatted_text)
    
    # Clean up any remaining formatting issues
    formatted_text = formatted_text.strip()
    
    return formatted_text
import time

def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ {func.__name__} took {end - start:.3f} seconds")
        return result
    return wrapper

llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # Enable CORS for all routes

@app.before_request
def log_request_info():
    print(f"📡 Incoming request: {request.method} {request.url}")


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response


# Set the OpenAI API key
openai.api_key = "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"
# Initialize Flask app


# Create the PostgreSQL engine with SQL logging
engine = create_engine(
    "postgresql+psycopg2://postgres:password@localhost:5432/postgres",
    echo=True,  # This will print all SQL queries to console
    echo_pool=True  # This will print connection pool info
)

# Define machine_vision_analysis table
metadata = MetaData()
metadata.reflect(bind=engine)
machine_vision_analysis = Table('machine_vision_analysis', metadata, autoload_with=engine)
machine_anomaly_screenshots = Table('machine_anomaly_screenshots', metadata, autoload_with=engine)

# Create the SQL database object
sql_database = SQLDatabase(engine)
sql_database = SQLDatabase(
    engine, 
    include_tables=[
        "lab", "users", "node", "machine", "lab_user", 
        "current_sensor", "critical_health_machine", "shift_machine_production",
        # Add these for root cause analysis:
        "temperature_sensor", "humidity_sensor", "machine_current_log",
        "anomalies", "anomaly_detections", "inference_data", 
        "work_orders", "maintenance_task", "machine_parts",
        "vibration_inference_data",
        # Add energy consumption table:
        "machine_energy_consumption",
        # Add troubleshooting and resolution tables:
        "machine_troubleshooting", "maintenance_procedures", 
        "machine_parts_inventory", "machine_issue_history",
        "machine_performance_benchmarks",
        # Add vision analysis table:
        "machine_vision_analysis"
    ]
)

# Now create the query engine with the PostgreSQL database
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, 
    tables=[
        "lab", "users", "node", "machine", "lab_user", 
        "current_sensor", "shift_machine_production", 
        "critical_health_machine",
        # Add these for root cause analysis:
        "temperature_sensor", "humidity_sensor", "machine_current_log",
        "anomalies", "anomaly_detections", "inference_data",
        "work_orders", "maintenance_task", "machine_parts", 
        "vibration_inference_data",
        # Add energy consumption table:
        "machine_energy_consumption",
        # Add troubleshooting and resolution tables:
        "machine_troubleshooting", "maintenance_procedures", 
        "machine_parts_inventory", "machine_issue_history",
        "machine_performance_benchmarks"
    ], 
    llm=None,
    verbose=False  # Disable verbose for better performance
)


from collections import deque

# Global FIFO queues
text_responses = deque(maxlen=3)
vision_responses = deque(maxlen=3)
first_prompt = 1
final_prompt = ""

@log_time
@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        query_str = data.get('query', '')
        source = data.get('source', 'unknown')
        response_format = data.get('responseFormat', 'text')
        stream = data.get('stream', False)  # New parameter
        
        print(f"📊 Query received: '{query_str}' from {source}")
        print(f"📊 Stream mode: {stream}")
        
        if not query_str:
            print("❌ ERROR: No query string provided")
            return jsonify({"error": "Query string is required"}), 400
        
        if source == "anomaly":
            machine_id = data.get("machine_id")
            sensor_type = data.get("sensor_type", "Vibration")  # Default to Vibration
            
            print(f"🔍 Anomaly query - Machine ID: {machine_id}, Sensor Type: {sensor_type}")
            
            if stream:
                # Return streaming response for anomaly queries
                return Response(
                    stream_with_context(stream_anomaly_response(query_str, machine_id, sensor_type)),
                    mimetype='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                    }
                )
            else:
                return handle_anomaly_source(query_str, machine_id, sensor_type)
        
        if stream:
            # Return streaming response
            return Response(
                stream_with_context(stream_query_response(query_str, response_format)),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                }
            )
        else:
            # Return regular JSON response (current behavior)
            return handle_text_query(query_str, response_format)
            
    except Exception as e:
        print(f"❌ Error in query endpoint: {e}")
        return jsonify({"error": str(e)}), 500


def get_machine_image_url(machine_id):
    """Get the most recent anomaly image for a machine"""
    try:
        # First try to get from database
        metadata = MetaData()
        metadata.reflect(bind=engine)
        machine = Table('machine', metadata, autoload_with=engine)

        stmt = select(machine).where(machine.c.machine_id == uuid.UUID(machine_id))

        with engine.connect() as conn:
            machine_row = conn.execute(stmt).mappings().first()
        
        if machine_row and "image_url" in machine_row and machine_row["image_url"]:
            return machine_row["image_url"]
        
        # If no image in database, look for the most recent image in file system
        base_dir = "/Users/khanhamza/Desktop/machine_images"
        machine_dir = f"{base_dir}/machine_{machine_id}"
        
        if os.path.exists(machine_dir):
            # Find the most recent image
            most_recent_image = None
            most_recent_time = 0
            
            for year_dir in os.listdir(machine_dir):
                if os.path.isdir(f"{machine_dir}/{year_dir}"):
                    for month_dir in os.listdir(f"{machine_dir}/{year_dir}"):
                        if os.path.isdir(f"{machine_dir}/{year_dir}/{month_dir}"):
                            for filename in os.listdir(f"{machine_dir}/{year_dir}/{month_dir}"):
                                if filename.endswith(('.png', '.jpg', '.jpeg')):
                                    filepath = f"{machine_dir}/{year_dir}/{month_dir}/{filename}"
                                    file_time = os.path.getmtime(filepath)
                                    if file_time > most_recent_time:
                                        most_recent_time = file_time
                                        most_recent_image = filepath
            
            if most_recent_image:
                return most_recent_image
        
        return None
        
    except Exception as e:
        return None
    


def cache_key(image_path, query_str):
    img_fp = get_image_fingerprint(image_path)
    query_hash = hashlib.sha256(query_str.encode()).hexdigest()
    return f"vision:{img_fp}:{query_hash}"

def get_cached_response(key):
    return redis.get(key)

def cache_response(key, response):
    redis.setex(key, 3600, response)  # 1-hour expiry

def get_analysis_from_chart(machine_id, sensor_type):
    """Get analysis from matplotlib chart stored in machine_anomaly_screenshots table"""
    try:
        print(f"🔍 get_analysis_from_chart: Looking for machine_id={machine_id}, sensor_type={sensor_type}")
        with engine.connect() as conn:
            # First try to get analysis from matplotlib chart
            chart_result = conn.execute(
                select(machine_anomaly_screenshots).where(
                    and_(
                        machine_anomaly_screenshots.c.machine_id == machine_id,
                        machine_anomaly_screenshots.c.sensor_type == sensor_type
                    )
                )
            )
            chart_row = chart_result.fetchone()
            
            if chart_row and chart_row.analysis_id:
                print(f"✅ Found matplotlib chart with analysis_id={chart_row.analysis_id}")
                
                # Get the analysis from machine_vision_analysis table
                analysis_result = conn.execute(
                    select(machine_vision_analysis).where(
                        machine_vision_analysis.c.id == chart_row.analysis_id
                    )
                )
                analysis_row = analysis_result.fetchone()
                
                if analysis_row:
                    print(f"✅ Found analysis for matplotlib chart")
                    return {
                        'analysis_text': analysis_row.analysis_text,
                        'sensor_type': analysis_row.sensor_type,
                        'created_at': analysis_row.created_at.isoformat(),
                        'chart_title': chart_row.chart_title
                    }
            
            # Fallback: get the most recent analysis for this machine from any source
            result = conn.execute(
                select(machine_vision_analysis).where(
                    machine_vision_analysis.c.machine_id == machine_id
                ).order_by(machine_vision_analysis.c.created_at.desc())
            )
            row = result.fetchone()
            print(f"🔍 get_analysis_from_chart: Found fallback analysis = {row is not None}")
            if row:
                return {
                    'analysis_text': row.analysis_text,
                    'sensor_type': row.sensor_type,
                    'created_at': row.created_at.isoformat(),
                    'chart_title': None
                }
    except Exception as e:
        print(f"Error getting analysis from chart: {e}")
    return None

def get_cached_analysis(machine_id, image_path=None):
    """Get cached analysis from database - if image_path is provided, try exact match first, then fallback to any analysis for machine"""
    try:
        print(f"🔍 get_cached_analysis: Looking for machine_id={machine_id}, image_path={image_path}")
        with engine.connect() as conn:
            # First try exact match if image_path is provided
            if image_path:
                result = conn.execute(
                    select(machine_vision_analysis).where(
                        and_(
                            machine_vision_analysis.c.machine_id == machine_id,
                            machine_vision_analysis.c.image_path == image_path
                        )
                    )
                )
                row = result.fetchone()
                if row:
                    print(f"🔍 get_cached_analysis: Found exact match")
                    return {
                        'analysis_text': row.analysis_text,
                        'sensor_type': row.sensor_type,
                        'created_at': row.created_at.isoformat()
                    }
            
            # If no exact match, get the most recent analysis for this machine
            result = conn.execute(
                select(machine_vision_analysis).where(
                    machine_vision_analysis.c.machine_id == machine_id
                ).order_by(machine_vision_analysis.c.created_at.desc())
            )
            row = result.fetchone()
            print(f"🔍 get_cached_analysis: Found most recent analysis = {row is not None}")
            if row:
                return {
                    'analysis_text': row.analysis_text,
                    'sensor_type': row.sensor_type,
                    'created_at': row.created_at.isoformat()
                }
    except Exception as e:
        print(f"Error getting cached analysis: {e}")
    return None

def save_analysis_to_db(machine_id, image_path, sensor_type, analysis_text):
    """Save analysis to database"""
    try:
        with engine.connect() as conn:
            # Check if analysis already exists
            existing = conn.execute(
                select(machine_vision_analysis).where(
                    and_(
                        machine_vision_analysis.c.machine_id == machine_id,
                        machine_vision_analysis.c.image_path == image_path
                    )
                )
            ).fetchone()
            
            if existing:
                # Update existing analysis
                conn.execute(
                    machine_vision_analysis.update().where(
                        and_(
                            machine_vision_analysis.c.machine_id == machine_id,
                            machine_vision_analysis.c.image_path == image_path
                        )
                    ).values(
                        analysis_text=analysis_text,
                        updated_at=datetime.now()
                    )
                )
                print(f"Updated existing analysis for machine {machine_id}")
            else:
                # Insert new analysis
                conn.execute(
                    insert(machine_vision_analysis).values(
                        machine_id=machine_id,
                        image_path=image_path,
                        sensor_type=sensor_type,
                        analysis_text=analysis_text,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                )
                print(f"Saved new analysis for machine {machine_id}")
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Error saving analysis to database: {e}")
        return False



def handle_anomaly_source(query_str, machine_id=None, sensor_type="Vibration"):
    global first_prompt, final_prompt
    queue = vision_responses
    
    # Check for work order intent first
    intent = get_intent_for_workorder(query_str)
    
    if intent == "yes":
        # For work orders, we still need an image_url for the legacy process_work_order function
        # This will be updated in a future iteration
        image_url = f"chart_{machine_id}_{sensor_type}.png"  # Placeholder
        return process_work_order(query_str, image_url, machine_id, sensor_type)
    
    # For all other queries, get saved analysis from matplotlib chart and combine with user prompt
    print("🔍 Getting saved analysis from chart and combining with user prompt")
    
    # Get the saved analysis from matplotlib chart
    print(f"🔍 Debug: Looking for chart analysis with machine_id={machine_id}, sensor_type={sensor_type}")
    saved_analysis = get_analysis_from_chart(machine_id, sensor_type)
    print(f"🔍 Debug: saved_analysis = {saved_analysis}")
    
    if saved_analysis:
        print("✅ Found saved analysis from chart, combining with user prompt")
        
        # Get chart title for better context
        chart_title = saved_analysis.get('chart_title', f'{sensor_type} Sensor Data')
        
        # Combine saved analysis with user prompt
        combined_prompt = f"""
You are analyzing a machine anomaly. Below is the AI vision analysis that was previously performed on a matplotlib chart showing machine anomalies and sensor data patterns:

**Chart Information:**
- Chart Title: {chart_title}
- Machine ID: {machine_id}
- Sensor Type: {sensor_type}

**Previous Chart Analysis Results:**
{saved_analysis['analysis_text']}

**User's Question:** {query_str}

Please provide a detailed response based on the previous chart analysis and the user's specific question. Focus on how the chart analysis findings relate to what the user is asking about.
"""
        
        # Call OpenAI with the combined prompt (no image needed since we have the analysis)
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": combined_prompt
                    }
                ],
                max_tokens=1000
            )
            
            analysis_text = response.choices[0].message.content
            print(f"✅ OpenAI response received for combined prompt")
            
            return jsonify({
                "response": analysis_text,
                "format": "vision"
            })
            
        except Exception as e:
            print(f"❌ Error calling OpenAI: {e}")
            return jsonify({
                "response": f"Error processing your request: {str(e)}",
                "format": "text"
            })
    
    else:
        print("❌ No saved analysis found, performing new vision analysis")
        # Fallback to original vision analysis if no saved analysis exists
        # This will trigger chart generation if needed
        image_url = f"chart_{machine_id}_{sensor_type}.png"  # Placeholder
        return process_vision_first_prompt(query_str, image_url, machine_id, sensor_type)

@log_time
def get_intent_for_workorder(query_str):
    intent_prompt = (
        "Does the following user query ask to create a work order? "
        "Reply with only 'yes', 'no', or 'maybe'.\n\n"
        f"User query: {query_str}"
    )
    intent_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an intent classifier."},
            {"role": "user", "content": intent_prompt}
        ],
        max_tokens=1
    )
    intent = intent_response.choices[0].message.content.strip().lower()
    print("Work order intent:", intent)
    return intent

@log_time
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

@log_time
def process_work_order(query_str, anomaly_image_path, machine_id=None, sensor_type="Vibration"):
    import json

    image_path_workorder = "/Users/khanhamza/Desktop/image4.png"

    query_str = "."

    vision_response = process_vision_first_prompt(query_str, anomaly_image_path, machine_id, sensor_type)

    if hasattr(vision_response, "get_json"):
        vision_json = vision_response.get_json()
        vision_result_str = vision_json.get("response", "No response key found")
    else:
        vision_result_str = str(vision_response)

    workorder_prompt = (
        "This is the analysis of the anomaly: \n"
        f"{vision_result_str}\n\n"
        "1️⃣ Give me a Work Order template. Format your response according to this Work Order.\n"
        "In the generated Work Order give proper detailed description of work (atleast 7 points or more) based on ISO standards and take into account the machine name/type mentioned and detailed sepcial instructions (atleast 3 points) and give multiple parts_and_components_required also. Company name will be Honda. And the week_of date will be after "
        f"{date.today()}""and depending upon the criticality of the machine health \n\n"
        "description_of_work and special_instructions can be a multi-line string. If there are multiple tasks or steps, include them as separate lines within the string. Choose emplyee name, work perfromed by from the names: Kamran Ali, Ryan Ahmed or Greg Smith "
        "IMPORTANT: Return your answer as a JSON object with specified fields.\n\n"
        "The response MUST strictly match the following JSON structure:\n\n"
        "{\n"
        "  \"page_no\": \" \",\n"
        "  \"company_name\": \" \",\n"
        "  \"priority\": \" \",\n"
        "  \"date\": \" \",\n"
        "  \"work_order_no\": \" \",\n"
        "  \"week_no\": \" \",\n"
        "  \"week_of\": \" \",\n"
        "  \"equipment_id\": \" \",\n"
        "  \"category\": \" \",\n"
        "  \"equipment_description\": \" \",\n"
        "  \"location\": {\n"
        "    \"building\": \" \",\n"
        "    \"floor\": \" \",\n"
        "    \"room\": \" \",\n"
        "    \"description\": \" \"\n"
        "  },\n"
        "  \"special_instructions\": \" \",\n"
        "  \"shop_vendor\": {\n"
        "    \"shop_vendor\": \"  \",\n"
        "    \"name\": \" \"\n"
        "  },\n"
        "  \"employee\": \" \",\n"
        "  \"tasks\": [\n"
        "    {\n"
        "      \"task_no\": \"64\",\n"
        "      \"description_of_work\": \" \",\n"
        "      \"frequency\": \"N/A\"\n"
        "    }\n"
        "  ],\n"
        "  \"parts_and_components_required\": [\n"
        "    {\n"
        "      \"part_no\": \" \",\n"
        "      \"quantity\": \" \",\n"
        "      \"part_description\": \" \",\n"
        "      \"location\": \" \",\n"
        "      \"qty_in_stock\": \" \"\n"
        "    }\n"
        "  ],\n"
        "  \"work_performed_by\": {\n"
        "    \"employee\": \" \",\n"
        "    \"time_spent\": {\n"
        "      \"hours\": \" \"\n"
        "    }\n"
        "  },\n"
        "  \"materials_and_parts_used\": [\n"
        "    {\n"
        "      \"quantity\": \" \",\n"
        "      \"part_no\": \" \"\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Fill in the relevant details based on the images provided. Do not add, remove, or rename any fields. Only replace the values as necessary."
    )


    workorder_prompt_1 = (
    "Fill in the following Work Order strictly matching the JSON structure provided below using the details given.\n\n"
    "Here are the values to use:\n"
    "```json\n"
    "{\n"
    "  \"page_no\": \"1\",\n"
    "  \"company_name\": \"Honda\",\n"
    "  \"priority\": \"High\",\n"
    "  \"date\": \"2025-06-24\",\n"
    "  \"work_order_no\": \"WO-2025-1001\",\n"
    "  \"week_no\": \"26\",\n"
    "  \"week_of\": \"2025-06-23\",\n"
    "  \"equipment_id\": \"CNC-2023-MK2\",\n"
    "  \"category\": \"Maintenance\",\n"
    "  \"equipment_description\": \"CNC Milling Machine\",\n"
    "  \"location\": {\n"
    "    \"building\": \"Main Manufacturing\",\n"
    "    \"floor\": \"1\",\n"
    "    \"room\": \"101A\",\n"
    "    \"description\": \"CNC Workshop Area\"\n"
    "  },\n"
    "  \"special_instructions\": \"Ensure machine is powered down before inspection.\\n"
    "Document any unusual wear or damages.\\n"
    "Report findings immediately to the maintenance supervisor.\",\n"
    "  \"shop_vendor\": {\n"
    "    \"shop_vendor\": \"CNC Solutions Inc.\",\n"
    "    \"name\": \"John Doe\"\n"
    "  },\n"
    "  \"employee\": \"Kamran Ali\",\n"
    "  \"tasks\": [\n"
    "    {\n"
    "      \"task_no\": \"64\",\n"
    "      \"description_of_work\": \"Conduct a comprehensive inspection to identify the cause of vibration anomaly.\\n"
    "Check for loose components within the spindle assembly.\\n"
    "Inspect and verify alignment of the machine bed.\\n"
    "Examine bearings for signs of wear and replace if necessary.\\n"
    "Verify correct tension of belts and drives.\\n"
    "Assess the lubrication levels and refresh as needed.\\n"
    "Log vibration levels in post-inspection test runs.\",\n"
    "      \"frequency\": \"N/A\"\n"
    "    }\n"
    "  ],\n"
    "  \"parts_and_components_required\": [\n"
    "    {\n"
    "      \"part_no\": \"BRG-4567\",\n"
    "      \"quantity\": \"2\",\n"
    "      \"part_description\": \"Spindle Bearings\",\n"
    "      \"location\": \"Storage Room B\",\n"
    "      \"qty_in_stock\": \"15\"\n"
    "    },\n"
    "    {\n"
    "      \"part_no\": \"BLT-8910\",\n"
    "      \"quantity\": \"1\",\n"
    "      \"part_description\": \"Drive Belt\",\n"
    "      \"location\": \"Storage Room C\",\n"
    "      \"qty_in_stock\": \"10\"\n"
    "    },\n"
    "    {\n"
    "      \"part_no\": \"LUB-7852\",\n"
    "      \"quantity\": \"5\",\n"
    "      \"part_description\": \"Lubrication Oil\",\n"
    "      \"location\": \"Storage Room A\",\n"
    "      \"qty_in_stock\": \"50\"\n"
    "    }\n"
    "  ],\n"
    "  \"work_performed_by\": {\n"
    "    \"employee\": \"Ryan Ahmed\",\n"
    "    \"time_spent\": {\n"
    "      \"hours\": \"3\"\n"
    "    }\n"
    "  },\n"
    "  \"materials_and_parts_used\": [\n"
    "    {\n"
    "      \"quantity\": \"2\",\n"
    "      \"part_no\": \"BRG-4567\"\n"
    "    },\n"
    "    {\n"
    "      \"quantity\": \"1\",\n"
    "      \"part_no\": \"BLT-8910\"\n"
    "    },\n"
    "    {\n"
    "      \"quantity\": \"2\",\n"
    "      \"part_no\": \"LUB-7852\"\n"
    "    }\n"
    "  ]\n"
    "}\n"
    "```\n\n"
    "⚠️ IMPORTANT: \n"
    "- Strictly match the JSON structure above.\n"
    "- Do not add or remove any fields.\n"
    "- Only **fill in** the JSON with the provided values exactly.\n"
)


    final_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": workorder_prompt},
                        ],
            }
        ],
        max_tokens=700
    )

    workorder_response = final_response.choices[0].message.content

    try:
        workorder_dict = json.loads(workorder_response)
    except Exception as e:
        workorder_dict = {"raw": workorder_response}

    # --- UNWRAP 'work_order' KEY IF PRESENT ---
    if isinstance(workorder_dict, dict) and "work_order" in workorder_dict:
        workorder_dict = workorder_dict["work_order"]

    print("Final work order dict:", workorder_dict)
    return jsonify({
        "workorder": workorder_dict,
        "format": "vision"
    })



def get_image_fingerprint(image_path):
    img = Image.open(image_path)
    return str(imagehash.phash(img))  # Perceptual hash

@log_time
def process_vision_first_prompt(query_str, image_path, machine_id=None, sensor_type="Vibration"):
    queue = vision_responses

    # Use provided machine_id or fallback to default
    if machine_id is None:
        machine_id = "09ce4fec-8de8-4c1e-a987-9a0080313456"  # Default fallback
    
    print(f"🔍 Processing vision analysis for machine_id={machine_id}, image_path={image_path}, sensor_type={sensor_type}")
    
    # Step 1: Generate image hash for caching
    try:
        image_hash = get_image_fingerprint(image_path)
        print(f"🔍 Generated image hash: {image_hash}")
    except Exception as e:
        print(f"❌ Error generating image hash: {e}")
        image_hash = None
    
    # Step 2: Check for matplotlib chart in database first
    print(f"🔍 Checking for matplotlib chart in database for machine_id={machine_id}, sensor_type={sensor_type}")
    try:
        with engine.connect() as conn:
            chart_result = conn.execute(
                select(machine_anomaly_screenshots).where(
                    and_(
                        machine_anomaly_screenshots.c.machine_id == machine_id,
                        machine_anomaly_screenshots.c.sensor_type == sensor_type
                    )
                )
            )
            chart_row = chart_result.fetchone()
            
            if chart_row and chart_row.analysis_id:
                print(f"✅ Found matplotlib chart with analysis in database")
                
                # Get the analysis from machine_vision_analysis table
                analysis_result = conn.execute(
                    select(machine_vision_analysis).where(
                        machine_vision_analysis.c.id == chart_row.analysis_id
                    )
                )
                analysis_row = analysis_result.fetchone()
                
                if analysis_row:
                    print(f"✅ Found analysis for matplotlib chart")
                    
                    # Create a mock response object that matches OpenAI's structure
                    class MockResponse:
                        def __init__(self, content):
                            self.choices = [MockChoice(content)]
                    
                    class MockChoice:
                        def __init__(self, content):
                            self.message = MockMessage(content)
                    
                    class MockMessage:
                        def __init__(self, content):
                            self.content = content
                    
                    final_response = MockResponse(analysis_row.analysis_text)
                    return finalize_vision_response(final_response)
    except Exception as e:
        print(f"❌ Error checking for matplotlib chart: {e}")
    
    # Step 3: Check for cached analysis in database (fallback)
    cached_analysis = get_cached_analysis(machine_id, image_path)
    if cached_analysis:
        print(f"✅ Found cached analysis in database")
        
        # Create a mock response object that matches OpenAI's structure
        class MockResponse:
            def __init__(self, content):
                self.choices = [MockChoice(content)]
        
        class MockChoice:
            def __init__(self, content):
                self.message = MockMessage(content)
        
        class MockMessage:
            def __init__(self, content):
                self.content = content
        
        final_response = MockResponse(cached_analysis['analysis_text'])
        return finalize_vision_response(final_response)
    
    # Step 4: No cached analysis found, call OpenAI Vision API
    print(f"🚀 No cached analysis found, calling OpenAI Vision API...")
    
    try:
        # Encode image to base64
        base64_image = encode_image_to_base64(image_path)
        
        # Call OpenAI Vision API
        response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
                        {
                "role": "user",
                "content": [
                        {
                            "type": "text",
                            "text": f"Analyze this machine image and provide a detailed diagnosis. This is a {sensor_type} sensor anomaly from machine {machine_id}. Provide 5 likely causes with explanations."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        analysis_text = response.choices[0].message.content
        print(f"✅ OpenAI Vision API response received")
        
        # Step 5: Save analysis to database
        if analysis_text:
            success = save_analysis_to_db(machine_id, image_path, sensor_type, analysis_text)
            if success:
                print(f"✅ Analysis saved to database")
            else:
                print(f"❌ Failed to save analysis to database")
        
        return finalize_vision_response(response)
        
    except Exception as e:
        print(f"❌ Error calling OpenAI Vision API: {e}")
        
        # Fallback to hardcoded response
        hardcoded_response = """Based on the vibration sensor data from the CNC machine and the detected anomalies, here are the top five likely causes for the anomalies:

   - **Imbalance**: Uneven weight distribution in rotating components can cause increased vibration levels, indicating a potential imbalance in the machine.

   - **Misalignment**: Components such as couplings, shafts, or pulleys might be misaligned, leading to periodic increases in vibration.

   - **Bearing Wear**: Worn or damaged bearings can lead to irregular vibration patterns, which may correlate with the observed anomalies.

   - **Resonance**: The machine could be amplifying vibrations at certain frequencies, possibly corresponding with the operational times highlighted in the anomalies.

   - **Component Looseness**: Looseness in machine parts, such as bolts or mounts, can cause intermittent spikes in vibration, potentially matching the detected anomalies."""
        
        # Create a mock response object that matches OpenAI's structure
        class MockResponse:
            def __init__(self, content):
                self.choices = [MockChoice(content)]
        
        class MockChoice:
            def __init__(self, content):
                self.message = MockMessage(content)
        
        class MockMessage:
            def __init__(self, content):
                self.content = content
        
        final_response = MockResponse(hardcoded_response)
    return finalize_vision_response(final_response)

@log_time
def process_vision_followup(query_str):
    queue = vision_responses
    global final_prompt

    final_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant analyzing anomaly images. " + query_str},
            {"role": "user", "content": final_prompt}
        ]
    )

    return finalize_vision_response(final_response)

@log_time
def finalize_vision_response(openai_response):
    global final_prompt
    queue = vision_responses

    vision_result = openai_response.choices[0].message.content
    print("🖼️ Vision model result:", vision_result)
    
    queue.append(vision_result)
    print("📋 Vision FIFO Queue:", list(queue))

    combined_vision = ""
    for idx, resp in enumerate(queue, start=1):
        combined_vision += f"Previous result {idx}: {resp}\n"

    final_prompt = combined_vision.strip()
    print("Final prompt for OpenAI:", final_prompt)

    print("✅ Final vision response ---------___:", vision_result)

    return jsonify({
        "response": vision_result,
        "format": "vision"
    })


def generate_chart_image(machine_id, sensor_type, machine_name):
    """Generate matplotlib chart from sensor data and return as base64 string"""
    try:
        print(f"📊 Generating matplotlib chart for machine_id={machine_id}, sensor_type={sensor_type}")
        
        # Get metadata and tables
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        # Define anomaly data (same as in /inspection endpoint)
        anomalies = [
            {
                "start": "2024-03-02T21:41:00.000Z",
                "end": "2024-03-02T22:55:00.000Z"
            },
            {
                "start": "2024-03-03T01:55:00.000Z",
                "end": "2024-03-03T02:41:00.000Z"
            },
            {
                "start": "2024-03-03T15:41:00.000Z",
                "end": "2024-03-03T17:41:00.000Z"
            }
        ]

        anomalies_current = [
            {
                "start": "2024-03-01T17:41:00.000Z",
                "end": "2024-03-01T19:41:00.000Z"
            }
        ]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if sensor_type == "Current":
            # Multi-value data from inference_data_multi
            inference_data_multi = Table('inference_data_multi', metadata, autoload_with=engine)
            stmt = select(inference_data_multi)
            
            if machine_id:
                try:
                    machine_id_uuid = uuid.UUID(machine_id)
                    stmt = stmt.where(inference_data_multi.c.machine_id == machine_id_uuid)
                except Exception as e:
                    print(f"Invalid UUID format for machine_id: {e}")
                    return None

            with engine.connect() as conn:
                result = conn.execute(stmt)
                multi_value_data = [
                    {
                        "timestamp": row["timestamp"],
                        "value1": row["value1"],
                        "value2": row["value2"],
                        "value3": row["value3"]
                    }
                    for row in result.mappings()
                ][::100]  # Downsample
            
            if not multi_value_data:
                print("❌ No multi-value data found")
                return None
                
            # Convert timestamps to datetime objects (already datetime from DB)
            timestamps = [point["timestamp"] if isinstance(point["timestamp"], datetime) else parser.parse(point["timestamp"]) for point in multi_value_data]
            values1 = [point["value1"] for point in multi_value_data]
            values2 = [point["value2"] for point in multi_value_data]
            values3 = [point["value3"] for point in multi_value_data]
            
            # Plot multi-line chart
            ax.plot(timestamps, values1, label='Current 1', linewidth=2)
            ax.plot(timestamps, values2, label='Current 2', linewidth=2)
            ax.plot(timestamps, values3, label='Current 3', linewidth=2)
            
            # Add anomaly regions
            for anomaly in anomalies_current:
                start_time = parser.parse(anomaly['start'])
                end_time = parser.parse(anomaly['end'])
                ax.axvspan(start_time, end_time, alpha=0.3, color='red', label='Anomaly' if anomaly == anomalies_current[0] else "")
            
            ax.set_ylabel('Current (A)')
            ax.set_title(f'{machine_name or "Machine"} - Current Sensor Data')
            
        else:
            # Single-value data from inference_data
            inference_data = Table('inference_data', metadata, autoload_with=engine)
            stmt = select(inference_data)
            
            if machine_id:
                try:
                    machine_id_uuid = uuid.UUID(machine_id)
                    stmt = stmt.where(inference_data.c.machine_id == machine_id_uuid)
                except Exception as e:
                    print(f"Invalid UUID format for machine_id: {e}")
                    return None

            with engine.connect() as conn:
                result = conn.execute(stmt)
                vibration_data = [
                    {
                        "timestamp": row["timestamp"],
                        "value": row["value"]
                    }
                    for row in result.mappings()
                ][::4]  # Downsample
            
            if not vibration_data:
                print("❌ No vibration data found")
                return None
                
            # Convert timestamps to datetime objects (already datetime from DB)
            timestamps = [point["timestamp"] if isinstance(point["timestamp"], datetime) else parser.parse(point["timestamp"]) for point in vibration_data]
            values = [point["value"] for point in vibration_data]
            
            # Plot single line chart
            ax.plot(timestamps, values, label='Vibration', linewidth=2, color='blue')
            
            # Add anomaly regions
            for anomaly in anomalies:
                start_time = parser.parse(anomaly['start'])
                end_time = parser.parse(anomaly['end'])
                ax.axvspan(start_time, end_time, alpha=0.3, color='red', label='Anomaly' if anomaly == anomalies[0] else "")
            
            ax.set_ylabel('Vibration (mm/s)')
            ax.set_title(f'{machine_name or "Machine"} - Vibration Sensor Data')
        
        # Common chart formatting
        ax.set_xlabel('Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save to BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        print(f"✅ Generated matplotlib chart, size: {len(img_base64)} characters")
        return img_base64
        
    except Exception as e:
        print(f"❌ Error generating chart: {e}")
        if 'fig' in locals():
            plt.close(fig)
        return None


def background_chart_generation(machine_id, sensor_type, machine_name):
    """Background function to generate chart and save to database"""
    try:
        print(f"🔄 Background chart generation started for machine_id={machine_id}, sensor_type={sensor_type}")
        
        # Check if chart already exists
        with engine.connect() as conn:
            existing_result = conn.execute(
                select(machine_anomaly_screenshots).where(
                    and_(
                        machine_anomaly_screenshots.c.machine_id == machine_id,
                        machine_anomaly_screenshots.c.sensor_type == sensor_type
                    )
                )
            )
            existing_row = existing_result.fetchone()
            
            if existing_row:
                print(f"✅ Chart already exists for machine_id={machine_id}, sensor_type={sensor_type}")
                return
        
        # Generate matplotlib chart
        chart_base64 = generate_chart_image(machine_id, sensor_type, machine_name)
        if not chart_base64:
            print(f"❌ Failed to generate chart for machine_id={machine_id}")
            return
        
        # Convert base64 to binary data
        chart_binary = base64.b64decode(chart_base64)
        
        # Save chart to database
        chart_title = f'{machine_name or "Machine"} - {sensor_type} Sensor Data'
        with engine.connect() as conn:
            insert_stmt = insert(machine_anomaly_screenshots).values(
                machine_id=machine_id,
                sensor_type=sensor_type,
                screenshot_data=chart_binary,
                screenshot_url=f"chart_{machine_id}_{sensor_type}_{int(time.time())}.png",
                chart_title=chart_title
            )
            
            result = conn.execute(insert_stmt)
            screenshot_id = result.inserted_primary_key[0]
            conn.commit()
            
            print(f"✅ Background chart saved with ID: {screenshot_id}")
            
            # Trigger OpenAI vision analysis
            print(f"🤖 Background OpenAI vision analysis starting...")
            
            try:
                # Call OpenAI Vision API with the base64 image
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": f"""Analyze this machine anomaly graph titled "{chart_title}" showing {sensor_type} sensor data for {machine_name or "Machine"} (ID: {machine_id}). 

Please provide a comprehensive analysis including:

1. **Graph Overview**: Describe what you see in the chart - data patterns, trends, and overall behavior
2. **Anomaly Detection**: Identify any anomalies, spikes, or unusual patterns in the data
3. **Root Cause Analysis**: Provide 5 likely causes for any detected anomalies with detailed explanations
4. **Severity Assessment**: Rate the severity of issues (Low/Medium/High/Critical)
5. **Recommended Actions**: Specific maintenance or troubleshooting steps to address the issues
6. **Preventive Measures**: Suggestions to prevent similar issues in the future

Focus on actionable insights that would help maintenance technicians understand and resolve the machine issues."""
                            },
                            {
                                "type": "image_url", 
                                "image_url": {"url": f"data:image/png;base64,{chart_base64}"}
                            }
                        ]
                    }],
                    max_tokens=1500
                )
                
                analysis_text = response.choices[0].message.content
                print(f"✅ Background OpenAI vision analysis completed")
                
                # Save analysis to machine_vision_analysis table
                analysis_insert = insert(machine_vision_analysis).values(
                    machine_id=machine_id,
                    image_path=f"chart_{machine_id}_{sensor_type}_{int(time.time())}.png",
                    analysis_text=analysis_text,
                    sensor_type=sensor_type
                )
                
                analysis_result = conn.execute(analysis_insert)
                analysis_id = analysis_result.inserted_primary_key[0]
                conn.commit()
                
                # Update screenshot record with analysis_id
                update_stmt = update(machine_anomaly_screenshots).where(
                    machine_anomaly_screenshots.c.id == screenshot_id
                ).values(analysis_id=analysis_id)
                
                conn.execute(update_stmt)
                conn.commit()
                
                print(f"✅ Background analysis saved with ID: {analysis_id} and linked to chart")
                
            except Exception as analysis_error:
                print(f"❌ Error during background OpenAI analysis: {analysis_error}")
                
    except Exception as e:
        print(f"❌ Error in background_chart_generation: {e}")


@log_time
def handle_text_query(query_str, response_format):
    print("📊" + "="*60)
    print("📊 handle_text_query() called")
    print("📊" + "="*60)
    
    # Check for database table names from query_engine FIRST (higher priority)
    # MUST match the tables passed to NLSQLTableQueryEngine exactly
    table_names = [
        "machine_current_log", "lab", "users", "node", "machine", "lab_user", 
        "current_sensor", "shift_machine_production",
        "temperature_sensor", "humidity_sensor", "anomalies", "anomaly_detections", 
        "inference_data", "work_orders", "maintenance_task", "machine_parts", 
        "vibration_inference_data", "critical_health_machine",
        # Add energy consumption table:
        "machine_energy_consumption",
        # Add troubleshooting and resolution tables:
        "machine_troubleshooting", "maintenance_procedures", 
        "machine_parts_inventory", "machine_issue_history",
        "machine_performance_benchmarks"
    ]
    
    
    query_lower = query_str.lower().strip()
    print(f"🔍 Checking for table names in: '{query_lower}'")
    
    contains_table_name = any(table in query_lower for table in table_names)
    print(f"🔍 Contains table name: {contains_table_name}")
    
    # Check for simple greetings first - but only if no database-related words are present
    greeting_keywords = ['hey', 'hi', 'hello', 'good morning', 'good afternoon', 'good evening']
    db_related_words = ['machine', 'machines', 'production', 'health', 'status', 'data', 'list', 'show', 'tell', 'about', 'query', 'database', 'table']
    
    # Only treat as greeting if:
    # 1. Contains a greeting keyword AND
    # 2. Does NOT contain any database-related words AND  
    # 3. Query is short (less than 20 characters) OR starts with greeting
    contains_greeting = any(greeting in query_lower for greeting in greeting_keywords)
    contains_db_words = any(word in query_lower for word in db_related_words)
    is_short_query = len(query_lower) < 20
    starts_with_greeting = any(query_lower.startswith(greeting) for greeting in greeting_keywords)
    
    is_simple_greeting = contains_greeting and not contains_db_words and (is_short_query or starts_with_greeting)
    
    if is_simple_greeting:
        # Simple greeting response - no database query needed
        print("👋 Simple greeting detected - using direct response")
        return jsonify({
            "response": "Hello! I'm Wise Guy, your AI assistant for machine monitoring and data analysis. How can I help you today?",
            "format": response_format
        })
    
    # If it contains table names, go to database
    if contains_table_name:
        print("🗄️ TABLE NAME DETECTED - Will query database for table information")
        print("🗄️ Proceeding to database query...")
    
    queue = text_responses
    print(f"📊 Previous responses in queue: {list(queue)}")
    print(f"📊 Queue length: {len(queue)}")

    combined_responses = ""
    if queue:
        print("📊 Building combined responses with history...")
        for idx, resp in enumerate(queue, start=1):
            combined_responses += f"Previous response {idx}: {resp}\n"
        combined_responses += f"Current query: {query_str}"
        print(f"📊 Combined responses length: {len(combined_responses)}")
    else:
        print("📊 No previous responses, using query directly")
        combined_responses = query_str

    print("🔍 Executing SQL query via query_engine...")
    print(f"🔍 Query input: {combined_responses}")
    
    try:
        response = query_engine.query(combined_responses)
        print("🔍 SQL Response received:")
        print(f"🔍 Response type: {type(response)}")
        print(f"🔍 Response content: {response}")
    except Exception as db_error:
        print("❌" + "="*60)
        print("❌ DATABASE ERROR OCCURRED")
        print("❌" + "="*60)
        print(f"❌ Error type: {type(db_error).__name__}")
        print(f"❌ Error message: {str(db_error)}")
        print(f"❌ Query that failed: {combined_responses}")
        print("❌" + "="*60)
        
        # Try to extract SQL from the error if possible
        if hasattr(db_error, 'sql'):
            print(f"❌ SQL Query: {db_error.sql}")
        if hasattr(db_error, 'statement'):
            print(f"❌ SQL Statement: {db_error.statement}")
        
        # Return error response
        return jsonify({
            "response": f"Database error occurred: {str(db_error)}",
            "format": response_format,
            "error": True
        }), 500

    response_str = str(response)
    print(f"🔍 Response string length: {len(response_str)}")
    
    # Check if response is already well-formatted (avoid second OpenAI call)
    missing_data_indicators = [
        "not in the database", "no specific information available",
        "I'm sorry", "unable to locate", "not found", "error"
    ]
    
    use_second_prompt = any(phrase in response_str.lower() for phrase in missing_data_indicators)
    print(f"🔍 Use second prompt: {use_second_prompt}")
    
    # Fast path: If response is good, return it directly
    if not use_second_prompt and len(response_str) > 50:
        print("⚡ FAST PATH - Returning SQL response directly (no second OpenAI call)")
        queue.append(response_str)
        print(f"📊 Added to queue. New queue length: {len(queue)}")
        
        return jsonify({
            "response": response_str,
            "format": response_format
        })

    # Slow path: Use second OpenAI call for refinement
    print("🐌 SLOW PATH - Using second OpenAI call for refinement")
    system_prompt = "You are a helpful AI assistant." if use_second_prompt else (
        "Respond using clean Markdown formatting such as **bold headings**, new lines, and bullet points. "
        "Avoid phrases like 'Sure', 'Here's a refined version', or 'Certainly'. Just give the structured answer."
    )
    print(f"🔍 System prompt: {system_prompt}")

    queue.append(response_str)
    print(f"📊 Added to queue. New queue length: {len(queue)}")

    print("🤖 Calling OpenAI GPT-4o...")
    final_openai_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": response_str if not use_second_prompt else combined_responses}
        ]
    )

    refined_response = final_openai_response.choices[0].message.content
    print("✅" + "="*60)
    print("✅ Final GPT-4o response received:")
    print("✅" + "="*60)
    print(f"✅ Response length: {len(refined_response)}")
    print(f"✅ Response preview: {refined_response[:200]}...")
    print("✅" + "="*60)

    return jsonify({
        "response": refined_response,
        "format": response_format
    })


def stream_query_response(query_str, response_format):
    """Generator function for streaming responses"""
    try:
        # Check for simple greetings first
        query_lower = query_str.lower().strip()
        greeting_keywords = ['hey', 'hi', 'hello', 'good morning', 'good afternoon', 'good evening']
        db_related_words = ['machine', 'machines', 'production', 'health', 'status', 'data', 'list', 'show', 'tell', 'about', 'query', 'database', 'table']
        
        contains_greeting = any(greeting in query_lower for greeting in greeting_keywords)
        contains_db_words = any(word in query_lower for word in db_related_words)
        is_short_query = len(query_lower) < 20
        starts_with_greeting = any(query_lower.startswith(greeting) for greeting in greeting_keywords)
        
        is_simple_greeting = contains_greeting and not contains_db_words and (is_short_query or starts_with_greeting)
        
        if is_simple_greeting:
            # Stream simple greeting response
            greeting = "Hello! I'm Wise Guy, your AI assistant for machine monitoring and data analysis. How can I help you today?"
            for char in greeting:
                yield f"data: {json.dumps({'type': 'char', 'content': char})}\n\n"
                time.sleep(0.02)  # Small delay for typing effect
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            return
        
        # Check for chart requests about machine health
        chart_keywords = ['chart', 'graph', 'pie', 'visualization', 'visualize', 'plot']
        health_keywords = ['machine health', 'health status', 'machine status', 'machines']
        
        is_chart_request = any(keyword in query_lower for keyword in chart_keywords) or 'show me' in query_lower
        is_health_request = any(keyword in query_lower for keyword in health_keywords)
        
        if is_chart_request and is_health_request:
            # Generate machine health pie chart
            yield f"data: {json.dumps({'type': 'status', 'content': 'Analyzing machine health...'})}\n\n"
            
            try:
                # Query the database for actual machine health data
                with engine.connect() as conn:
                    query = text("""
                        SELECT 
                            severity_level as health_status,
                            COUNT(DISTINCT machine_id) as count
                        FROM critical_health_machine
                        GROUP BY severity_level
                    """)
                    result = conn.execute(query)
                    rows = result.fetchall()
                    
                    # Build chart data
                    chart_data = {}
                    total_machines = 0
                    for row in rows:
                        status = row[0]
                        count = row[1]
                        chart_data[status] = count
                        total_machines += count
                    
                    # If no data, use example data
                    if total_machines == 0:
                        chart_data = {
                            'Critical': 2,
                            'Warning': 5,
                            'Normal': 4
                        }
                        total_machines = 11
                    
                    # Transform to Chart.tsx expected format
                    labels = list(chart_data.keys())
                    values = list(chart_data.values())
                    # Sage-inspired sophisticated color palette
                    colors = {
                        'Critical': '#dc2626',      # Deep red
                        'Warning': '#f59e0b',       # Warm amber
                        'Normal': '#437874',        # Sage green (from sidebar - sage-500)
                        'Unknown': '#94a3b8'        # Soft slate
                    }
                    background_colors = [colors.get(label, '#8884d8') for label in labels]
                    
                    formatted_chart_data = {
                        'type': 'pie',
                        'title': 'Machine Health Status Distribution',
                        'data': {
                            'labels': labels,
                            'datasets': [{
                                'label': 'Machines',
                                'data': values,
                                'backgroundColor': background_colors
                            }]
                        }
                    }
                    
                    # Stream response text FIRST
                    response_text = f"Here's the current machine health status:\n\n"
                    for status, count in chart_data.items():
                        response_text += f"- **{status}**: {count} machine{'s' if count != 1 else ''}\n"
                    response_text += f"\n**Total Machines**: {total_machines}"
                    
                    for char in response_text:
                        yield f"data: {json.dumps({'type': 'char', 'content': char})}\n\n"
                        time.sleep(0.01)
                    
                    # Send chart data AFTER text
                    yield f"data: {json.dumps({'type': 'chart', 'data': formatted_chart_data})}\n\n"
                    
                    yield f"data: {json.dumps({'type': 'complete'})}\n\n"
                    return
                    
            except Exception as chart_error:
                print(f"⚠️ Chart generation failed: {chart_error}")
                # Fallback to text response
                error_text = "I encountered an error generating the chart. Please try again."
                for char in error_text:
                    yield f"data: {json.dumps({'type': 'char', 'content': char})}\n\n"
                    time.sleep(0.02)
                yield f"data: {json.dumps({'type': 'complete'})}\n\n"
                return
        
        # Check for table names
        table_names = ["machine_current_log", "lab", "users", "node", "machine", "lab_user", "current_sensor", "shift_machine_production", "maintenance_task"]
        contains_table_name = any(table in query_lower for table in table_names)
        
        if contains_table_name:
            # Stream LlamaIndex response
            yield f"data: {json.dumps({'type': 'status', 'content': 'Querying database...'})}\n\n"
            
            # Get LlamaIndex response
            response_text = query_engine.query(query_str).response
            print(f"📊 LlamaIndex response: {response_text}")
            
            # Stream GPT-4o refinement
            yield f"data: {json.dumps({'type': 'status', 'content': 'Processing response...'})}\n\n"
            
            try:
                refined_response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that formats information into clear, well-structured markdown. Make the response more readable, professional, and properly formatted with headings, lists, and emphasis where appropriate. Do not mention databases, SQL queries, or technical implementation details in your response."},
                        {"role": "user", "content": f"Please format this information into clear, well-structured markdown: {response_text}"}
                    ],
                    stream=True  # Enable streaming from GPT-4o
                )
                
                # Stream GPT-4o response chunk by chunk
                for chunk in refined_response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        yield f"data: {json.dumps({'type': 'char', 'content': content})}\n\n"
                        time.sleep(0.01)  # Small delay for typing effect
                        
            except Exception as refine_error:
                print(f"⚠️ GPT-4o refinement failed: {refine_error}")
                # Fallback to original response
                for char in response_text:
                    yield f"data: {json.dumps({'type': 'char', 'content': char})}\n\n"
                    time.sleep(0.02)
            
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
        else:
            # No table names found
            no_data_response = "I don't have access to that information in my current database. Please ask about machines, production data, health status, or users."
            for char in no_data_response:
                yield f"data: {json.dumps({'type': 'char', 'content': char})}\n\n"
                time.sleep(0.02)
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            
    except Exception as e:
        print(f"❌ Error in streaming: {e}")
        error_response = f"I encountered an error: {str(e)}"
        for char in error_response:
            yield f"data: {json.dumps({'type': 'char', 'content': char})}\n\n"
            time.sleep(0.02)
        yield f"data: {json.dumps({'type': 'complete'})}\n\n"

def stream_anomaly_response(query_str, machine_id=None, sensor_type="Vibration"):
    """Stream response for anomaly queries with vision analysis"""
    try:
        print(f"🚀 Starting anomaly stream for query: {query_str}")
        print(f"🔍 Machine ID: {machine_id}, Sensor Type: {sensor_type}")
        
        # Send initial status
        yield f"data: {json.dumps({'type': 'status', 'content': 'Analyzing machine anomaly...'})}\n\n"
        
        # Check for work order intent first
        intent = get_intent_for_workorder(query_str)
        
        if intent == "yes":
            # For work orders, get the response and stream it
            image_url = f"chart_{machine_id}_{sensor_type}.png"  # Placeholder
            response = process_work_order(query_str, image_url, machine_id, sensor_type)
            if isinstance(response, tuple):
                response_data = response[0].get_json()
            else:
                response_data = response.get_json()
            
            response_text = response_data.get('workorder', {})
            if isinstance(response_text, dict):
                response_text = str(response_text)
            
            # Stream the work order response
            for char in response_text:
                yield f"data: {json.dumps({'type': 'char', 'content': char})}\n\n"
                time.sleep(0.01)
            
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            return
        
        # For other queries, get saved analysis from chart and combine with user prompt
        print("🔍 Getting saved analysis from chart and combining with user prompt")
        
        # Get the saved analysis from matplotlib chart
        print(f"🔍 Debug: Looking for chart analysis with machine_id={machine_id}, sensor_type={sensor_type}")
        saved_analysis = get_analysis_from_chart(machine_id, sensor_type)
        print(f"🔍 Debug: saved_analysis = {saved_analysis}")
        
        if saved_analysis:
            print("✅ Found saved analysis from chart, combining with user prompt")
            
            # Get chart title for better context
            chart_title = saved_analysis.get('chart_title', f'{sensor_type} Sensor Data')
            
            # Combine saved analysis with user prompt
            combined_prompt = f"""
You are analyzing a machine anomaly. Below is the AI vision analysis that was previously performed on a matplotlib chart showing machine anomalies and sensor data patterns:

**Chart Information:**
- Chart Title: {chart_title}
- Machine ID: {machine_id}
- Sensor Type: {sensor_type}

**Previous Chart Analysis Results:**
{saved_analysis['analysis_text']}

**User's Question:** {query_str}

Please provide a detailed response based on the previous chart analysis and the user's specific question. Focus on how the chart analysis findings relate to what the user is asking about.
"""
            
            # Send status update
            yield f"data: {json.dumps({'type': 'status', 'content': 'Generating contextual response...'})}\n\n"
            
            # Call OpenAI with streaming for real-time response
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": combined_prompt
                        }
                    ],
                    max_tokens=1000,
                    stream=True  # Enable streaming
                )
                
                # Stream the response in real-time
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        yield f"data: {json.dumps({'type': 'char', 'content': content})}\n\n"
                
                yield f"data: {json.dumps({'type': 'complete'})}\n\n"
                
            except Exception as e:
                print(f"❌ Error calling OpenAI: {e}")
                yield f"data: {json.dumps({'type': 'error', 'content': f'Error processing your request: {str(e)}'})}\n\n"
        
        else:
            print("❌ No saved analysis found, performing new vision analysis")
            # Fallback to original vision analysis if no saved analysis exists
            # This part needs to be adapted for streaming if process_vision_first_prompt is not streaming
            # For now, we'll simulate streaming the non-streaming response
            yield f"data: {json.dumps({'type': 'status', 'content': 'Performing new vision analysis...'})}\n\n"
            image_url = f"chart_{machine_id}_{sensor_type}.png"  # Placeholder
            response_data = process_vision_first_prompt(query_str, image_url, machine_id, sensor_type)
            response_text = response_data.get_json().get('response', '')
            for char in response_text:
                yield f"data: {json.dumps({'type': 'char', 'content': char})}\n\n"
                time.sleep(0.01)
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
        
    except Exception as e:
        print(f"❌ Error in stream_anomaly_response: {e}")
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    
@app.route('/update-maintenance-status', methods=['POST'])
def update_maintenance_status():
    """Update maintenance task status from 'scheduled' to 'Scheduled'"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("UPDATE maintenance_task SET status = 'Scheduled' WHERE status = 'scheduled'"))
            conn.commit()
            return jsonify({"message": f"Updated {result.rowcount} records", "success": True})
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/', methods=['GET'])
def home():
    return "Flask server is running!"

@app.route('/clear_history', methods=['POST'])
def clear_history():
    global previous_responses
    previous_responses.clear()
    print("🧹 Cleared previous_responses FIFO queue")
    return jsonify({"message": "Previous responses cleared."}), 200

@log_time
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok"}), 200
@log_time
@app.route('/addConnection', methods=['POST'])
def add_connection():
    data = request.json
    databasetype = data.get("databaseType")
    url = data.get("url")

    if not databasetype or not url:
        return jsonify({"error": "Missing databaseType or url"}), 400

    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        database_conn = Table('database_conn', metadata, autoload_with=engine)

        stmt = insert(database_conn).values(databasetype=databasetype, url=url)
        with engine.begin() as conn:
            conn.execute(stmt)

        return jsonify({"message": "Connection info saved"}), 201
    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500
    
@log_time
@app.route('/inspection', methods=['GET'])
def inspection():
    try:
        machine_name = request.args.get("machine_name")
        sensor_type = request.args.get("sensor_type")
        machine_id = request.args.get("machine_id")
        print("machine_name:", machine_name)
        print("sensor_type:", sensor_type)
        print("machine_id:", machine_id)

        metadata = MetaData()
        metadata.reflect(bind=engine)

        anomalies = [
            {
                "start": "2024-03-02T21:41:00.000Z",
                "end": "2024-03-02T22:55:00.000Z"
            },
            {
                "start": "2024-03-03T01:55:00.000Z",
                "end": "2024-03-03T02:41:00.000Z"
            },
            {
                "start": "2024-03-03T15:41:00.000Z",
                "end": "2024-03-03T17:41:00.000Z"
            }
        ]

        anomalies_current = [
            {
                "start": "2024-03-01T17:41:00.000Z",
                "end": "2024-03-01T19:41:00.000Z"
            }
        ] 

        if sensor_type == "Current":
            inference_data_multi = Table('inference_data_multi', metadata, autoload_with=engine)
            stmt = select(inference_data_multi)
            print("SQL Statement:", stmt)

            # ADD THIS BLOCK TO PRINT ALL machine_id VALUES
            if machine_id:
                try:
                    machine_id_uuid = uuid.UUID(machine_id)
                    stmt = stmt.where(inference_data_multi.c.machine_id == machine_id_uuid)
                    print("SQL Statement after filtering:", stmt)
                except Exception as e:
                    print("Invalid UUID format for machine_id:", e)
                    return jsonify({"error": "Invalid machine_id format"}), 400

            with engine.connect() as conn:
                result = conn.execute(stmt)
                multi_value_data = [
                    {
                        "timestamp": row["timestamp"].isoformat() + "Z" if row["timestamp"] else None,
                        "value1": row["value1"],
                        "value2": row["value2"],
                        "value3": row["value3"]
                    }
                    for row in result.mappings()
                ][::100]
            # Start background chart generation
            if machine_id:
                Thread(target=background_chart_generation, args=(machine_id, sensor_type, machine_name)).start()
                print(f"🔄 Started background chart generation for machine_id={machine_id}")
            
            return jsonify({
                "title": f"{machine_name or 'Machine'} - Current Sensor Data",
                "x_label": "Time",
                "y_label": "Current (A)",
                "x_tick_labels": [],
                "data_type": "multi",
                "multi_value_data": multi_value_data,
                "anomalies": anomalies_current
            }), 200

        else:
            # Single-value data from inference_data
            inference_data = Table('inference_data', metadata, autoload_with=engine)
            stmt = select(inference_data)
            with engine.connect() as conn:
                result = conn.execute(stmt)
                vibration_data = [
                    {
                        "timestamp": row["timestamp"].isoformat() + "Z" if row["timestamp"] else None,
                        "value": row["value"]
                    }
                    for row in result.mappings()
                ][::4]  # Downsample if needed

            # Start background chart generation
            if machine_id:
                Thread(target=background_chart_generation, args=(machine_id, sensor_type, machine_name)).start()
                print(f"🔄 Started background chart generation for machine_id={machine_id}")
            
            return jsonify({
                "title": f"{machine_name or 'Machine'} - Vibration Sensor Data",
                "x_label": "Time",
                "y_label": "Vibration (mm/s)",
                "x_tick_labels": [],
                "data_type": "single",
                "vibration_data": vibration_data,
                "anomalies": anomalies
            }), 200

    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500
    



@log_time
@app.route('/machine-health', methods=['GET'])
def get_machine_health():
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        machine_health = Table('critical_health_machine', metadata, autoload_with=engine)

        stmt = select(machine_health)
        with engine.connect() as conn:
            result = conn.execute(stmt)
            machines = [
                {
                    "id": row["machine_id"],
                    "machine": row["machine_name"],
                    "severityLevel": row["severity_level"],
                    "lastAnomaly": row["last_anomaly"].isoformat() if row["last_anomaly"] else None,
                    "sensorType": row["sensor_type"]
                }
                for row in result.mappings()
            ]

        return jsonify({"machines": machines}), 200
    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500
    
@log_time
@app.route('/work-order', methods=['POST'])
def create_work_order():
    data = request.json
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        work_orders = Table('work_orders', metadata, autoload_with=engine)

        # Map camelCase JSON keys to snake_case DB columns
        work_order_id = uuid.uuid4()
        page_no = data.get("pageNo")
        priority = data.get("priority")
        company_name = data.get("companyName")
        work_order_no = data.get("workOrderNo")
        week_no = data.get("weekNo")
        week_of = data.get("weekOf")
        equipment_id = data.get("equipmentId")
        equipment_description = data.get("equipmentDescription")
        category = data.get("category")
        building = data.get("building")
        floor = data.get("floor")
        room = data.get("room")
        location_description = data.get("description")  # from "description"
        emergency_contact = data.get("emergencyContact")
        special_instructions = data.get("specialInstructions")
        shop_vendor = data.get("shopVendor")
        department_name = data.get("departmentName")
        employee_name = data.get("employee")  # from "employee"
        task_no = data.get("taskNo")
        work_description = data.get("workDescription")
        frequency = data.get("frequency")
        work_performed_by = data.get("workPerformedBy")
        completion_date = data.get("date")  # from "date"
        standard_hours = data.get("standardHours")
        overtime_hours = data.get("overtimeHours")
        machine_id = data.get("machine_id")
        part_numbers = data.get("partNumbers")
        materials_used = data.get("materialsUsed")

        # Convert types as needed
        week_of = data.get("weekOf")
        completion_date = data.get("weekOf")
        standard_hours = data.get("standardHours")
        overtime_hours = data.get("overtimeHours")

        # Convert week_of
        week_of = parse_date(data.get("weekOf"))
        completion_date = parse_date(data.get("weekOf"))

        # Convert standard_hours and overtime_hours
        if standard_hours is not None and str(standard_hours).strip() != "":
            standard_hours = float(standard_hours)
        else:
            standard_hours = None

        if overtime_hours is not None and str(overtime_hours).strip() != "":
            overtime_hours = float(overtime_hours)
        else:
            overtime_hours = None

        stmt = insert(work_orders).values(
            id=work_order_id,
            page_no=page_no,
            priority=1,
            company_name=company_name,
            work_order_no=work_order_no,
            week_no=week_no,
            week_of=week_of,
            equipment_id=equipment_id,
            equipment_description=equipment_description,
            category=category,
            building=building,
            floor=floor,
            room=room,
            location_description=location_description,
            emergency_contact=emergency_contact,
            special_instructions=special_instructions,
            shop_vendor=shop_vendor,
            department_name=department_name,
            employee_name=employee_name,
            task_no=task_no,
            work_description=work_description,
            frequency=frequency,
            work_performed_by=work_performed_by,
            completion_date=completion_date,
            standard_hours=standard_hours,
            overtime_hours=overtime_hours,
            machine_id=machine_id,
            part_numbers=part_numbers,
            materials_used=materials_used
        )

        with engine.begin() as conn:
            conn.execute(stmt)

            print("Work order Completion Date: --- ", completion_date)
            scheduled_date = completion_date or date.today()
            print("Scheduled Date: --- ", scheduled_date)
             # 🔔 Call to insert maintenance_task entry
            create_maintenance_task(
                conn=conn,
                machine_id=machine_id,
                machine_name="CNC Machine A",  # Replace with actual machine name if available
                category=category,
                work_description=work_description,
                completion_date=scheduled_date,
                standard_hours=standard_hours,
                priority=priority,
                employee_name=employee_name
            )

        
            return jsonify({"message": "Work order created successfully", "id": str(work_order_id)}), 201

    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500

@log_time  
def create_maintenance_task(conn, machine_id, machine_name, category, work_description, completion_date, standard_hours, priority, employee_name):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    maintenance_task = Table('maintenance_task', metadata, autoload_with=engine)
    print("Inserting maintenance task for machine_id:", machine_id)
    # Priority mapping
    priority_str = 'low'
    if str(priority) == '1':
        priority_str = 'high'
    elif str(priority) == '2':
        priority_str = 'medium'
    elif str(priority) == '3':
        priority_str = 'low'
    
    first_line = ""
    if work_description:
        first_line = work_description.splitlines()[0] if work_description.splitlines() else ""


    maintenance_task_entry = {
        "id": uuid.uuid4(),
        "machine_id": machine_id,
        "machine_name": machine_name,
        "task_type": category,
        "description": first_line,
        "scheduled_date": completion_date,
        "duration": int(standard_hours) if standard_hours else 1,
        "priority": priority_str,
        "status": "Scheduled",
        "assigned_technician": employee_name
    }

    conn.execute(insert(maintenance_task), [maintenance_task_entry])

    return True
    
@log_time
def parse_date(date_str):
    if not date_str or not str(date_str).strip():
        return None
    try:
        # Try ISO format first
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        try:
            # Try MM/DD/YYYY
            return datetime.strptime(date_str, "%m/%d/%Y").date()
        except ValueError:
            try:
                # Try dateutil for any other format
                return parser.parse(date_str).date()
            except Exception:
                return None

@log_time   
@app.route('/maintenance-tasks', methods=['GET'])
def get_maintenance_tasks():
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        maintenance_tasks = Table('maintenance_task', metadata, autoload_with=engine)
        print("Maintenance tasks table:", maintenance_tasks)
        stmt = select(maintenance_tasks)
        with engine.connect() as conn:
            result = conn.execute(stmt)
            tasks = [
                {
                    "id": str(row["id"]),
                    "machineId": str(row["machine_id"]),
                    "machineName": row["machine_name"],
                    "taskType": row["task_type"],
                    "description": row["description"],
                    "scheduledDate": row["scheduled_date"].strftime("%Y-%m-%d") if row["scheduled_date"] else None,
                    "duration": row["duration"],
                    "priority": row["priority"],
                    "status": row["status"],
                    "assignedTechnician": row["assigned_technician"]
                }
                for row in result.mappings()
            ]

        return jsonify({"tasks": tasks}), 200
    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500

from fastapi.responses import StreamingResponse

@log_time
def handle_text_query_stream(query_str, response_format):
    queue = text_responses
    print("Previous responses:", list(queue))

    combined_responses = ""
    if queue:
        for idx, resp in enumerate(queue, start=1):
            combined_responses += f"Previous response {idx}: {resp}\n"
        combined_responses += f"Current query: {query_str}"
    else:
        combined_responses = query_str

    response = query_engine.query(combined_responses)
    print("SQL Response:", response)

    missing_data_indicators = [
        "not in the database", "no specific information available",
        "I'm sorry", "unable to locate", "not found", "error"
    ]

    response_str = str(response)
    use_second_prompt = any(phrase in response_str.lower() for phrase in missing_data_indicators)

    system_prompt = "You are a helpful AI assistant." if use_second_prompt else (
        "Respond using clean Markdown formatting such as **bold headings**, new lines, and bullet points. "
        "Avoid phrases like 'Sure', 'Here's a refined version', or 'Certainly'. Just give the structured answer."
    )

    queue.append(response_str)

    def generate():
        openai_response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": response_str if not use_second_prompt else combined_responses}
            ],
            stream=True
        )
        for chunk in openai_response:
            content = chunk.choices[0].delta.get("content", "")
            if content:
                yield content

    return StreamingResponse(generate(), media_type="text/plain")



@log_time
@app.route('/upload-anomaly-image', methods=['POST'])
def upload_anomaly_image():
    """Upload and save anomaly image for a specific machine and date"""
    try:
        data = request.json
        machine_id = data.get('machine_id')
        image_base64 = data.get('image_base64')
        sensor_type = data.get('sensor_type', 'Vibration')
        anomaly_severity = data.get('anomaly_severity', 'Medium')
        anomaly_description = data.get('anomaly_description', '')
        captured_date = data.get('captured_date', date.today().isoformat())
        
        if not machine_id or not image_base64:
            return jsonify({"error": "machine_id and image_base64 are required"}), 400
        
        # Create directory structure
        base_dir = "/Users/khanhamza/Desktop/machine_images"
        machine_dir = f"{base_dir}/machine_{machine_id}"
        year = captured_date[:4]
        month = captured_date[5:7]
        day = captured_date[8:10]
        
        os.makedirs(f"{machine_dir}/{year}/{month}", exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{captured_date}_{sensor_type.lower()}_{anomaly_severity.lower()}_{timestamp}.png"
        filepath = f"{machine_dir}/{year}/{month}/{filename}"
        
        # Save image
        image_data = base64.b64decode(image_base64)
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        # Calculate file hash for duplicate detection
        file_hash = hashlib.sha256(image_data).hexdigest()
        file_size = len(image_data)
        
        # Save to database (if you create the table)
        # For now, update the machine table
        metadata = MetaData()
        metadata.reflect(bind=engine)
        machine = Table('machine', metadata, autoload_with=engine)
        
        stmt = machine.update().where(
            machine.c.machine_id == uuid.UUID(machine_id)
        ).values(
            image_url=filepath,
            last_image_captured=datetime.now()
        )
        
        with engine.begin() as conn:
            conn.execute(stmt)
        
        return jsonify({
            "message": "Image uploaded successfully",
            "filepath": filepath,
            "filename": filename,
            "file_size": file_size,
            "file_hash": file_hash
        }), 201
        
    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500

@log_time
@app.route('/machine-images/<machine_id>', methods=['GET'])
def get_machine_images(machine_id):
    """Get all images for a specific machine"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        image_type = request.args.get('type', 'anomaly')
        
        base_dir = "/Users/khanhamza/Desktop/machine_images"
        machine_dir = f"{base_dir}/machine_{machine_id}"
        
        images = []
        
        if os.path.exists(machine_dir):
            for year_dir in os.listdir(machine_dir):
                if os.path.isdir(f"{machine_dir}/{year_dir}"):
                    for month_dir in os.listdir(f"{machine_dir}/{year_dir}"):
                        if os.path.isdir(f"{machine_dir}/{year_dir}/{month_dir}"):
                            for filename in os.listdir(f"{machine_dir}/{year_dir}/{month_dir}"):
                                if filename.endswith(('.png', '.jpg', '.jpeg')):
                                    filepath = f"{machine_dir}/{year_dir}/{month_dir}/{filename}"
                                    file_stat = os.stat(filepath)
                                    
                                    # Parse filename for metadata
                                    parts = filename.replace('.png', '').split('_')
                                    if len(parts) >= 3:
                                        file_date = f"{year_dir}-{month_dir}-{parts[0].split('-')[2]}"
                                        sensor_type = parts[1]
                                        severity = parts[2]
                                        
                                        images.append({
                                            "filename": filename,
                                            "filepath": filepath,
                                            "date": file_date,
                                            "sensor_type": sensor_type,
                                            "severity": severity,
                                            "file_size": file_stat.st_size,
                                            "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                                        })
        
        # Sort by date (newest first)
        images.sort(key=lambda x: x['date'], reverse=True)
        
        return jsonify({"images": images}), 200
        
    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500

@log_time
@app.route('/daily-image-summary', methods=['GET'])
def get_daily_image_summary():
    """Get summary of images captured today for all machines"""
    try:
        today = date.today().isoformat()
        base_dir = "/Users/khanhamza/Desktop/machine_images"
        
        summary = []
        
        if os.path.exists(base_dir):
            for machine_folder in os.listdir(base_dir):
                if machine_folder.startswith('machine_'):
                    machine_id = machine_folder.replace('machine_', '')
                    year = today[:4]
                    month = today[5:7]
                    day = today[8:10]
                    
                    machine_dir = f"{base_dir}/{machine_folder}/{year}/{month}"
                    today_images = []
                    
                    if os.path.exists(machine_dir):
                        for filename in os.listdir(machine_dir):
                            if filename.startswith(today):
                                filepath = f"{machine_dir}/{filename}"
                                file_stat = os.stat(filepath)
                                
                                parts = filename.replace('.png', '').split('_')
                                if len(parts) >= 3:
                                    sensor_type = parts[1]
                                    severity = parts[2]
                                    
                                    today_images.append({
                                        "filename": filename,
                                        "sensor_type": sensor_type,
                                        "severity": severity,
                                        "file_size": file_stat.st_size,
                                        "captured_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                                    })
                    
                    summary.append({
                        "machine_id": machine_id,
                        "date": today,
                        "image_count": len(today_images),
                        "images": today_images
                    })
        
        return jsonify({"summary": summary}), 200
        
    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500


@log_time
@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    """Generate matplotlib chart and trigger OpenAI vision analysis"""
    try:
        data = request.get_json()
        machine_id = data.get('machine_id')
        sensor_type = data.get('sensor_type', 'Vibration')
        machine_name = data.get('machine_name', 'Machine')
        
        if not machine_id:
            return jsonify({"error": "machine_id is required"}), 400
        
        print(f"🎯 Generating chart for machine_id={machine_id}, sensor_type={sensor_type}")
        
        # Check if chart already exists
        with engine.connect() as conn:
            existing_result = conn.execute(
                select(machine_anomaly_screenshots).where(
                    and_(
                        machine_anomaly_screenshots.c.machine_id == machine_id,
                        machine_anomaly_screenshots.c.sensor_type == sensor_type
                    )
                )
            )
            existing_row = existing_result.fetchone()
            
            if existing_row:
                print(f"✅ Chart already exists for machine_id={machine_id}, sensor_type={sensor_type}")
                return jsonify({
                    "message": "Chart already exists",
                    "screenshot_id": str(existing_row.id),
                    "analysis_id": existing_row.analysis_id,
                    "chart_title": existing_row.chart_title
                }), 200
        
        # Generate matplotlib chart
        chart_base64 = generate_chart_image(machine_id, sensor_type, machine_name)
        if not chart_base64:
            return jsonify({"error": "Failed to generate chart"}), 500
        
        # Convert base64 to binary data
        chart_binary = base64.b64decode(chart_base64)
        
        # Save chart to database
        chart_title = f'{machine_name or "Machine"} - {sensor_type} Sensor Data'
        with engine.connect() as conn:
            insert_stmt = insert(machine_anomaly_screenshots).values(
                machine_id=machine_id,
                sensor_type=sensor_type,
                screenshot_data=chart_binary,
                screenshot_url=f"chart_{machine_id}_{sensor_type}_{int(time.time())}.png",
                chart_title=chart_title
            )
            
            result = conn.execute(insert_stmt)
            screenshot_id = result.inserted_primary_key[0]
            conn.commit()
            
            print(f"✅ Chart saved with ID: {screenshot_id}")
            
            # Trigger OpenAI vision analysis
            print(f"🤖 Triggering OpenAI vision analysis for chart...")
            
            try:
                # Call OpenAI Vision API with the base64 image
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": f"""Analyze this machine anomaly graph titled "{chart_title}" showing {sensor_type} sensor data for {machine_name or "Machine"} (ID: {machine_id}). 

Please provide a comprehensive analysis including:

1. **Graph Overview**: Describe what you see in the chart - data patterns, trends, and overall behavior
2. **Anomaly Detection**: Identify any anomalies, spikes, or unusual patterns in the data
3. **Root Cause Analysis**: Provide 5 likely causes for any detected anomalies with detailed explanations
4. **Severity Assessment**: Rate the severity of issues (Low/Medium/High/Critical)
5. **Recommended Actions**: Specific maintenance or troubleshooting steps to address the issues
6. **Preventive Measures**: Suggestions to prevent similar issues in the future

Focus on actionable insights that would help maintenance technicians understand and resolve the machine issues."""
                            },
                            {
                                "type": "image_url", 
                                "image_url": {"url": f"data:image/png;base64,{chart_base64}"}
                            }
                        ]
                    }],
                    max_tokens=1500
                )
                
                analysis_text = response.choices[0].message.content
                print(f"✅ OpenAI vision analysis completed")
                
                # Save analysis to machine_vision_analysis table
                analysis_insert = insert(machine_vision_analysis).values(
                    machine_id=machine_id,
                    image_path=f"chart_{machine_id}_{sensor_type}_{int(time.time())}.png",
                    analysis_text=analysis_text,
                    sensor_type=sensor_type
                )
                
                analysis_result = conn.execute(analysis_insert)
                analysis_id = analysis_result.inserted_primary_key[0]
                conn.commit()
                
                # Update screenshot record with analysis_id
                update_stmt = update(machine_anomaly_screenshots).where(
                    machine_anomaly_screenshots.c.id == screenshot_id
                ).values(analysis_id=analysis_id)
                
                conn.execute(update_stmt)
                conn.commit()
                
                print(f"✅ Analysis saved with ID: {analysis_id} and linked to chart")
                
                return jsonify({
                    "message": "Chart generated and analysis completed",
                    "screenshot_id": screenshot_id,
                    "analysis_id": analysis_id,
                    "chart_title": chart_title,
                    "analysis_preview": analysis_text[:200] + "..." if len(analysis_text) > 200 else analysis_text
                }), 200
                
            except Exception as analysis_error:
                print(f"❌ Error during OpenAI analysis: {analysis_error}")
                # Still return success for chart generation, but note analysis failed
                return jsonify({
                    "message": "Chart generated but analysis failed",
                    "screenshot_id": screenshot_id,
                    "error": str(analysis_error)
                }), 200
                
    except Exception as e:
        print(f"❌ Error in generate_chart: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
