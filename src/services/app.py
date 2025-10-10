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
from sqlalchemy import select, func
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
        "machine_performance_benchmarks"
    ]
)

# Now create the query engine with the PostgreSQL database
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, 
    tables=[
        "lab", "users", "node", "machine", "lab_user", 
        "current_sensor", "shift_machine_production", "maintenance_schedule", 
        "maintenance_parts", "critical_health_machine",
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
            print("🔍 Handling anomaly source")
            machine_id = data.get("machine_id")
            print(f"🔍 Machine ID: {machine_id}")
            image_url = get_machine_image_url(machine_id)
            print(f"🔍 Image URL: {image_url}")
            
            # Fallback to default image if no image found
            if image_url is None:
                image_url = "/Users/khanhamza/Desktop/image3.png"
                print(f"🔍 Using fallback image: {image_url}")
            
            return handle_anomaly_source(query_str, image_url, machine_id)
        
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
            print(f"🔍 Executing SQL: {stmt}")
            machine_row = conn.execute(stmt).mappings().first()
        
        if machine_row and "image_url" in machine_row and machine_row["image_url"]:
            print("Image URL for this machine:", machine_row["image_url"])
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
                print("Most recent image found:", most_recent_image)
                return most_recent_image
        
        print("No image found for this machine.")
        return None
        
    except Exception as e:
        print(f"Error getting machine image: {e}")
        return None
    


def cache_key(image_path, query_str):
    img_fp = get_image_fingerprint(image_path)
    query_hash = hashlib.sha256(query_str.encode()).hexdigest()
    return f"vision:{img_fp}:{query_hash}"

def get_cached_response(key):
    return redis.get(key)

def cache_response(key, response):
    redis.setex(key, 3600, response)  # 1-hour expiry



def handle_anomaly_source(query_str, image_url, machine_id=None):
    global first_prompt, final_prompt
    queue = vision_responses
    intent = get_intent_for_workorder(query_str)
    
    if intent == "yes":
        return process_work_order(query_str, image_url, machine_id)
    
    if first_prompt == 1:
        first_prompt = 0
        return process_vision_first_prompt(query_str, image_url, machine_id)
    else:
        return process_vision_followup(query_str)

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
def process_work_order(query_str, anomaly_image_path, machine_id=None):
    import json

    image_path_workorder = "/Users/khanhamza/Desktop/image4.png"
    print("Image paths:", image_path_workorder, anomaly_image_path)
    print("Machine ID for work order:", machine_id)

    query_str = "."

    vision_response = process_vision_first_prompt(query_str, anomaly_image_path, machine_id)

    if hasattr(vision_response, "get_json"):
        vision_json = vision_response.get_json()
        vision_result_str = vision_json.get("response", "No response key found")
        print("Vision model JSON result in process_work_order:", vision_result_str)
    else:
        print("Vision model result in process_work_order:", vision_response)

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
    print("Work order response:", workorder_response)

    try:
        workorder_dict = json.loads(workorder_response)
    except Exception as e:
        print("Failed to parse workorder as JSON:", e)
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
def process_vision_first_prompt(query_str, image_path, machine_id=None):
    queue = vision_responses

    # 🚀 DATABASE-FIRST APPROACH - CHECK DB BEFORE OPENAI CALL
    print("🖼️" + "="*60)
    print("🖼️ CHECKING DATABASE FOR CACHED VISION ANALYSIS")
    print("🖼️" + "="*60)
    print(f"🖼️ Image path: {image_path}")
    print(f"🖼️ Machine ID: {machine_id}")
    print("🖼️" + "="*60)
    
    try:
        # Try to get analysis from database first
        with engine.connect() as conn:
            # Use provided machine_id or fallback to default
            if machine_id is None:
                machine_id = "09ce4fec-8de8-4c1e-a987-9a0080313456"  # Default fallback
                print(f"🖼️ No machine_id provided, using default: {machine_id}")
            
            # Try exact match first
            result = conn.execute(
                text("SELECT analysis_text FROM machine_vision_analysis WHERE machine_id = :machine_id AND image_path = :image_path"),
                {"machine_id": machine_id, "image_path": image_path}
            )
            row = result.fetchone()
            
            # If no exact match, try with fallback image path
            if not row and image_path != "/Users/khanhamza/Desktop/image3.png":
                result = conn.execute(
                    text("SELECT analysis_text FROM machine_vision_analysis WHERE machine_id = :machine_id AND image_path = :fallback_path"),
                    {"machine_id": machine_id, "fallback_path": "/Users/khanhamza/Desktop/image3.png"}
                )
                row = result.fetchone()
            
            if row:
                cached_analysis = row[0]
                print("✅ FOUND CACHED ANALYSIS IN DATABASE")
                print("🤖" + "="*60)
                print("🤖 USING CACHED VISION RESPONSE FROM DATABASE")
                print("🤖" + "="*60)
                print(f"🤖 Response length: {len(cached_analysis)} characters")
                print(f"🤖 Full response:")
                print("🤖" + "-"*40)
                print(cached_analysis)
                print("🤖" + "-"*40)
                print("🤖" + "="*60)
                
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
                
                final_response = MockResponse(cached_analysis)
                return finalize_vision_response(final_response)
            else:
                print("❌ NO CACHED ANALYSIS FOUND - FALLING BACK TO HARDCODED")
                
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e} - FALLING BACK TO HARDCODED")
    
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
    
    print("🤖" + "="*60)
    print("🤖 USING HARDCODED VISION RESPONSE (FALLBACK)")
    print("🤖" + "="*60)
    print(f"🤖 Response length: {len(hardcoded_response)} characters")
    print(f"🤖 Full response:")
    print("🤖" + "-"*40)
    print(hardcoded_response)
    print("🤖" + "-"*40)
    print("🤖" + "="*60)
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
        "maintenance_schedule", "maintenance_parts",
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
        
        # Check for table names
        table_names = ["machine_current_log", "lab", "users", "node", "machine", "lab_user", "current_sensor", "daily_machine_health", "shift_machine_production"]
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


    
@app.route('/stream', methods=['POST'])
def stream_response():
    """Get AI model response without streaming"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        print(f"🎯 REQUEST: {query}")
        
        # Use the existing AI model to get a real response
        print("🤖 Getting AI response...")
                
        # Check if query is asking for machine health, production, or parts distribution
        health_keywords = ['health status', 'machine health', 'health overview', 'status of machines', 'health distribution']
        production_keywords = ['production', 'units produced', 'output', 'manufacturing']
        parts_keywords = ['parts distribution', 'machines by parts', 'parts produced', 'number of parts']
        query_lower = query.lower()
        is_health_chart_request = any(keyword in query_lower for keyword in health_keywords)
        is_production_chart_request = any(keyword in query_lower for keyword in production_keywords)
        is_parts_distribution_request = any(keyword in query_lower for keyword in parts_keywords)
        
        response_data = {
            'content': '',
            'chartData': None
        }
        
        if is_health_chart_request:
            print(f"📊 MACHINE HEALTH CHART REQUEST DETECTED: '{query}'")
            
            # Get LlamaIndex to query the database
            print("🔍 Querying database via LlamaIndex...")
            ai_response = query_engine.query(query)
            response_text = str(ai_response)
            
            print(f"📋 LlamaIndex response: {response_text[:200]}...")
            
            # Now query the database directly to get structured data for the chart
            from sqlalchemy import select, func
            
            metadata = MetaData()
            health_table = Table('daily_machine_health', metadata, autoload_with=engine)
            
            # Get count of machines by health status
            stmt = select(
                health_table.c.health_status,
                func.count(health_table.c.machine_id.distinct()).label('machine_count')
            ).group_by(health_table.c.health_status)
            
            with engine.connect() as connection:
                result = connection.execute(stmt).fetchall()
            
            # Color mapping for health statuses
            color_map = {
                'Good': '#437874',
                'Healthy': '#437874',
                'Normal': '#437874',
                'Warning': '#D4A574',
                'maintenance': '#5A8F8B',
                'Critical': '#C67B7B',
                'Error': '#C67B7B'
            }
            
            labels = []
            values = []
            chart_colors = []
            
            for row in result:
                status = row.health_status
                count = int(row.machine_count)
                labels.append(status)
                values.append(count)
                chart_colors.append(color_map.get(status, '#A9BBB7'))
            
            total_machines = sum(values)
            
            print(f"📊 Found {len(labels)} health statuses, {total_machines} total machines")
            
            # Generate insights
            insights = f"""Machine Health Overview:

📊 Fleet Status:
- Total Machines: {total_machines}

⚙️ Status Distribution:
{chr(10).join([f"- {labels[i]}: {values[i]} machines ({values[i]/total_machines*100:.1f}%)" for i in range(len(labels))])}"""
            
            chart_data = {
                'type': 'pie',
                'title': 'Machine Health Status Distribution',
                'insights': insights,
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'label': 'Machines',
                        'data': values,
                        'backgroundColor': chart_colors
                    }]
                }
            }
            
            print(f"✅ Chart data prepared from real database query")
            
            response_data['content'] = insights
            response_data['chartData'] = chart_data
            
        elif is_production_chart_request:
            print(f"📊 PRODUCTION CHART REQUEST DETECTED: '{query}'")
            
            # Get LlamaIndex to query the database
            print("🔍 Querying database via LlamaIndex...")
            ai_response = query_engine.query(query)
            response_text = str(ai_response)
            
            print(f"📋 LlamaIndex response: {response_text[:200]}...")
            
            # Query production data
            from sqlalchemy import select, func
            
            metadata = MetaData()
            production_table = Table('shift_machine_production', metadata, autoload_with=engine)
            
            # Get total production by machine
            stmt = select(
                production_table.c.machine_name,
                func.sum(production_table.c.units_produced).label('total_production')
            ).group_by(production_table.c.machine_name).order_by(func.sum(production_table.c.units_produced).desc())
            
            with engine.connect() as connection:
                result = connection.execute(stmt).fetchall()
            
            labels = []
            values = []
            
            for row in result:
                machine_name = row.machine_name
                total_units = int(row.total_production) if row.total_production else 0
                labels.append(machine_name)
                values.append(total_units)
            
            total_production = sum(values)
            
            print(f"📊 Found {len(labels)} machines with total production: {total_production} units")
            
            # Generate color gradient using sage green variations
            sage_colors = ['#437874', '#5A8F8B', '#4F8480', '#679E9A', '#7AADA9', '#3A6663', '#325B58']
            bar_colors = [sage_colors[i % len(sage_colors)] for i in range(len(labels))]
            
            # Generate insights combining AI response and production data
            insights = f"""{response_text}

📊 Production Summary:
- Total Machines: {len(labels)}
- Total Units Produced: {total_production:,}

⚙️ Production by Machine:
{chr(10).join([f"- {labels[i]}: {values[i]:,} units ({values[i]/total_production*100:.1f}%)" for i in range(len(labels))])}"""
            
            chart_data = {
                'type': 'bar',
                'title': 'Production by Machine',
                'insights': insights,
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'label': 'Units Produced',
                        'data': values,
                        'backgroundColor': bar_colors  # Sage green gradient
                    }]
                }
            }
            
            print(f"✅ Production chart data prepared")
            
            response_data['content'] = insights
            response_data['chartData'] = chart_data
            
        elif is_parts_distribution_request:
            print(f"📊 PARTS DISTRIBUTION CHART REQUEST DETECTED: '{query}'")
            
            # Get LlamaIndex to query the database
            print("🔍 Querying database via LlamaIndex...")
            ai_response = query_engine.query(query)
            response_text = str(ai_response)
            
            # Query database for parts distribution
            from sqlalchemy import select, func, case
            
            metadata = MetaData()
            production_table = Table('shift_machine_production', metadata, autoload_with=engine)
            
            # Get machines grouped by production ranges (bins)
            stmt = select(
                production_table.c.machine_name,
                func.sum(production_table.c.units_produced).label('total_parts')
            ).group_by(production_table.c.machine_name)
            
            with engine.connect() as connection:
                result = connection.execute(stmt).fetchall()
            
            # Create bins for parts produced (e.g., 0-100, 101-200, 201-300, etc.)
            bins = {}
            for row in result:
                parts = int(row.total_parts) if row.total_parts else 0
                # Determine which bin this falls into (100 parts per bin)
                bin_size = 500
                bin_start = (parts // bin_size) * bin_size
                bin_label = f"{bin_start}-{bin_start + bin_size - 1}"
                
                if bin_label not in bins:
                    bins[bin_label] = 0
                bins[bin_label] += 1
            
            # Sort bins by parts range
            sorted_bins = sorted(bins.items(), key=lambda x: int(x[0].split('-')[0]))
            
            labels = [item[0] for item in sorted_bins]
            values = [item[1] for item in sorted_bins]
            
            # Use sage green color theme
            sage_colors = ['#437874'] * len(labels)
            
            total_machines = sum(values)
            
            print(f"📊 Found {len(labels)} bins with {total_machines} total machines")
            
            # Generate insights
            insights = f"""{response_text}

📊 Parts Distribution Summary:
- Total Machines: {total_machines}
- Production Ranges: {len(labels)}

⚙️ Machine Distribution by Parts Produced:
{chr(10).join([f"- {labels[i]} parts: {values[i]} machines" for i in range(len(labels))])}"""
            
            chart_data = {
                'type': 'bar',
                'title': 'Machine Distribution by Parts Produced',
                'insights': insights,
                'data': {
                    'labels': labels,  # Parts ranges on Y-axis
                    'datasets': [{
                        'label': 'Number of Machines',
                        'data': values,  # Machine counts on X-axis
                        'backgroundColor': sage_colors
                    }]
                }
            }
            
            print(f"✅ Parts distribution chart data prepared")
            
            response_data['content'] = insights
            response_data['chartData'] = chart_data
            
        else:
            # Check for simple greetings first - but only if no database-related words are present
            greeting_keywords = ['hey', 'hi', 'hello', 'good morning', 'good afternoon', 'good evening']
            db_related_words = ['machine', 'machines', 'production', 'health', 'status', 'data', 'list', 'show', 'tell', 'about', 'query', 'database', 'table']
            
            query_lower = query.lower().strip()
            
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
                response_data['content'] = "Hello! I'm Wise Guy, your AI assistant for machine monitoring and data analysis. How can I help you today?"
            else:
                # Use the existing query engine for real AI responses
                print("🔍 Processing with AI model...")
                response = query_engine.query(query)
                response_text = str(response)
                
                # Refine with GPT-4o for better formatting and clarity
                print("🤖 Refining response with GPT-4o...")
                try:
                    refined_response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that formats information into clear, well-structured markdown. Make the response more readable, professional, and properly formatted with headings, lists, and emphasis where appropriate. Do not mention databases, SQL queries, or technical implementation details in your response."},
                            {"role": "user", "content": f"Please format this information into clear, well-structured markdown: {response_text}"}
                        ]
                    )
                    refined_text = refined_response.choices[0].message.content
                    print(f"✅ GPT-4o refinement completed: {len(refined_text)} characters")
                    
                    # Use GPT-4o's markdown formatting directly (no additional processing)
                    response_data['content'] = refined_text
                    
                except Exception as refine_error:
                    print(f"⚠️ GPT-4o refinement failed: {refine_error}")
                    print("📝 Using original response with basic formatting...")
                    # Use the original response with minimal formatting
                    response_data['content'] = response_text
        
        print(f"✅ AI Response received: {len(response_data['content'])} characters")
        
        return jsonify(response_data)
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

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
        "status": "scheduled",
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
                    "scheduledDate": row["scheduled_date"].isoformat() if row["scheduled_date"] else None,
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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
