# from flask import Flask, request, jsonify
# from sqlalchemy import create_engine
# from llama_index.core.indices.struct_store.sql import SQLDatabase
# from llama_index.core.query_engine import NLSQLTableQueryEngine
# from openai import OpenAI as OpenAIClient
# import openai

# from sqlalchemy import Table, MetaData, insert
# from llama_index.core import SQLDatabase
# from llama_index.llms.openai import OpenAI
# from sqlalchemy import select
# import uuid
# from sqlalchemy.dialects.postgresql import UUID as PG_UUID
# from sqlalchemy import insert
# import uuid
# from datetime import datetime
# import base64
# from dateutil import parser  
# from datetime import date
# from flask import Flask, Response, request, jsonify, stream_with_context




# llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")

# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}) # Enable CORS for all routes

# @app.before_request
# def log_request_info():
#     print(f"📡 Incoming request: {request.method} {request.url}")


# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#     response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
#     return response


# # Set the OpenAI API key
# openai.api_key = "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"
# # Initialize Flask app


# # Create the PostgreSQL engine
# engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/postgres")

# # Create the SQL database object
# sql_database = SQLDatabase(engine)

# # Now create the query engine with the PostgreSQL database
# query_engine = NLSQLTableQueryEngine(
#     sql_database=sql_database, 
#     tables=["machine_current_log", "lab", "users", "node", "machine", "lab_user", "current_sensor", "daily_machine_health"], 
#     llm=None,
#     verbose=True
# )


# from collections import deque

# # Global FIFO queues
# text_responses = deque(maxlen=3)
# vision_responses = deque(maxlen=3)
# first_prompt = 1
# final_prompt = ""

# @app.route('/query', methods=['POST'])
# def query():
#     global first_prompt, final_prompt
#     print("🚀 /query endpoint hit")
    
#     data = request.json
#     print("📥 Request JSON:", data)
    
#     query_str = data.get("query")
#     source = data.get("source")
#     response_format = data.get("responseFormat", "markdown")
    
#     #print(f"Machine ID: {machine_id}, Source: {source}, Query: {query_str}")
    
#     if not query_str:
#         return jsonify({"error": "Query string is required"}), 400
    
       
#     if source == "anomaly":
#         print("🔍 Handling anomaly source")
#         machine_id = data.get("machine_id")
#         image_url = get_machine_image_url(machine_id)
#         return handle_anomaly_source(query_str, image_url)
    
#     return handle_text_query(query_str, response_format)


# def get_machine_image_url(machine_id):
#     metadata = MetaData()
#     metadata.reflect(bind=engine)
#     machine = Table('machine', metadata, autoload_with=engine)

#     stmt = select(machine).where(machine.c.machine_id == uuid.UUID(machine_id))

#     with engine.connect() as conn:
#         machine_row = conn.execute(stmt).mappings().first()
    
#     if machine_row and "image_url" in machine_row:
#         print("Image URL for this machine:", machine_row["image_url"])
#         return machine_row["image_url"]
#     else:
#         print("No image_url found for this machine.")
#         return None


# def handle_anomaly_source(query_str, image_url):
#     global first_prompt, final_prompt
#     queue = vision_responses
#     intent = get_intent_for_workorder(query_str)
    
#     if intent == "yes":
#         return process_work_order(query_str, image_url)
    
#     if first_prompt == 1:
#         first_prompt = 0
#         print("Processing first vision prompt ---------------- ")
#         return process_vision_first_prompt(query_str, image_url)
#     else:
#         return process_vision_followup(query_str)


# def get_intent_for_workorder(query_str):
#     intent_prompt = (
#         "Does the following user query ask to create a work order? "
#         "Reply with only 'yes', 'no', or 'maybe'.\n\n"
#         f"User query: {query_str}"
#     )
#     intent_response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are an intent classifier."},
#             {"role": "user", "content": intent_prompt}
#         ],
#         max_tokens=1
#     )
#     intent = intent_response.choices[0].message.content.strip().lower()
#     print("Work order intent:", intent)
#     return intent


# def encode_image_to_base64(image_path):
#     with open(image_path, "rb") as f:
#         return base64.b64encode(f.read()).decode("utf-8")


# def process_work_order(query_str, anomaly_image_path):
#     import json

#     image_path_workorder = "/Users/khanhamza/Desktop/image4.png"
#     print("Image paths:", image_path_workorder, anomaly_image_path)

#     query_str = "."

#     vision_response = process_vision_first_prompt(query_str, anomaly_image_path)

#     if hasattr(vision_response, "get_json"):
#         vision_json = vision_response.get_json()
#         vision_result_str = vision_json.get("response", "No response key found")
#         print("Vision model JSON result in process_work_order:", vision_result_str)
#     else:
#         print("Vision model result in process_work_order:", vision_response)

#     workorder_prompt = (
#         "This is the analysis of the anomaly: \n"
#         f"{vision_result_str}\n\n"
#         "1️⃣ Give me a Work Order template. Format your response according to this Work Order.\n"
#         "In the generated Work Order give proper detailed description of work (atleast 7 points or more) based on ISO standards and take into account the machine name/type mentioned and detailed sepcial instructions (atleast 3 points) and give multiple parts_and_components_required also. Company name will be Honda. And the week_of date will be after "
#         f"{date.today()}""and depending upon the criticality of the machine health \n\n"
#         "description_of_work and special_instructions can be a multi-line string. If there are multiple tasks or steps, include them as separate lines within the string. Choose emplyee name, work perfromed by from the names: Kamran Ali, Ryan Ahmed or Greg Smith "
#         "IMPORTANT: Return your answer as a JSON object with specified fields.\n\n"
#         "The response MUST strictly match the following JSON structure:\n\n"
#         "{\n"
#         "  \"page_no\": \" \",\n"
#         "  \"company_name\": \" \",\n"
#         "  \"priority\": \" \",\n"
#         "  \"date\": \" \",\n"
#         "  \"work_order_no\": \" \",\n"
#         "  \"week_no\": \" \",\n"
#         "  \"week_of\": \" \",\n"
#         "  \"equipment_id\": \" \",\n"
#         "  \"category\": \" \",\n"
#         "  \"equipment_description\": \" \",\n"
#         "  \"location\": {\n"
#         "    \"building\": \" \",\n"
#         "    \"floor\": \" \",\n"
#         "    \"room\": \" \",\n"
#         "    \"description\": \" \"\n"
#         "  },\n"
#         "  \"special_instructions\": \" \",\n"
#         "  \"shop_vendor\": {\n"
#         "    \"shop_vendor\": \"  \",\n"
#         "    \"name\": \" \"\n"
#         "  },\n"
#         "  \"employee\": \" \",\n"
#         "  \"tasks\": [\n"
#         "    {\n"
#         "      \"task_no\": \"64\",\n"
#         "      \"description_of_work\": \" \",\n"
#         "      \"frequency\": \"N/A\"\n"
#         "    }\n"
#         "  ],\n"
#         "  \"parts_and_components_required\": [\n"
#         "    {\n"
#         "      \"part_no\": \" \",\n"
#         "      \"quantity\": \" \",\n"
#         "      \"part_description\": \" \",\n"
#         "      \"location\": \" \",\n"
#         "      \"qty_in_stock\": \" \"\n"
#         "    }\n"
#         "  ],\n"
#         "  \"work_performed_by\": {\n"
#         "    \"employee\": \" \",\n"
#         "    \"time_spent\": {\n"
#         "      \"hours\": \" \"\n"
#         "    }\n"
#         "  },\n"
#         "  \"materials_and_parts_used\": [\n"
#         "    {\n"
#         "      \"quantity\": \" \",\n"
#         "      \"part_no\": \" \"\n"
#         "    }\n"
#         "  ]\n"
#         "}\n\n"
#         "Fill in the relevant details based on the images provided. Do not add, remove, or rename any fields. Only replace the values as necessary."
#     )


#     final_response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": workorder_prompt},
#                         ],
#             }
#         ],
#         max_tokens=700
#     )

#     workorder_response = final_response.choices[0].message.content
#     print("Work order response:", workorder_response)

#     try:
#         workorder_dict = json.loads(workorder_response)
#     except Exception as e:
#         print("Failed to parse workorder as JSON:", e)
#         workorder_dict = {"raw": workorder_response}

#     # --- UNWRAP 'work_order' KEY IF PRESENT ---
#     if isinstance(workorder_dict, dict) and "work_order" in workorder_dict:
#         workorder_dict = workorder_dict["work_order"]

#     print("Final work order dict:", workorder_dict)
#     return jsonify({
#         "workorder": workorder_dict,
#         "format": "vision"
#     })


# def process_vision_first_prompt(query_str, image_path):
#     queue = vision_responses
#     encoded_image = encode_image_to_base64(image_path)
    
#     final_response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": "This is an image of an anomaly in a machine. Please analyze it and provide insights.\n" + query_str},
#                     {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}},
#                 ],
#             }
#         ],
#         max_tokens=300
#     )

#     return finalize_vision_response(final_response)


# def process_vision_followup(query_str):
#     queue = vision_responses
#     global final_prompt

#     final_response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are a helpful AI assistant analyzing anomaly images. " + query_str},
#             {"role": "user", "content": final_prompt}
#         ]
#     )

#     return finalize_vision_response(final_response)


# def finalize_vision_response(openai_response):
#     global final_prompt
#     queue = vision_responses

#     vision_result = openai_response.choices[0].message.content
#     print("🖼️ Vision model result:", vision_result)
    
#     queue.append(vision_result)
#     print("📋 Vision FIFO Queue:", list(queue))

#     combined_vision = ""
#     for idx, resp in enumerate(queue, start=1):
#         combined_vision += f"Previous result {idx}: {resp}\n"

#     final_prompt = combined_vision.strip()
#     print("Final prompt for OpenAI:", final_prompt)

#     print("✅ Final vision response ---------___:", vision_result)

#     return jsonify({
#         "response": vision_result,
#         "format": "vision"
#     })


# def handle_text_query(query_str, response_format):
#     queue = text_responses
#     print("Previous responses:", list(queue))

#     combined_responses = ""
#     if queue:
#         for idx, resp in enumerate(queue, start=1):
#             combined_responses += f"Previous response {idx}: {resp}\n"
#         combined_responses += f"Current query: {query_str}"
#     else:
#         combined_responses = query_str

#     response = query_engine.query(combined_responses)
#     print("SQL Response:", response)

#     missing_data_indicators = [
#         "not in the database", "no specific information available",
#         "I'm sorry", "unable to locate", "not found", "error"
#     ]

#     response_str = str(response)
#     use_second_prompt = any(phrase in response_str.lower() for phrase in missing_data_indicators)

#     system_prompt = "You are a helpful AI assistant." if use_second_prompt else (
#         "Respond using clean Markdown formatting such as **bold headings**, new lines, and bullet points. "
#         "Avoid phrases like 'Sure', 'Here's a refined version', or 'Certainly'. Just give the structured answer."
#     )

#     queue.append(response_str)

#     final_openai_response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": response_str if not use_second_prompt else combined_responses}
#         ]
#     )

#     refined_response = final_openai_response.choices[0].message.content
#     print("✅ Final GPT-4o response:", refined_response)

#     return jsonify({
#         "response": refined_response,
#         "format": response_format
#     })


    
# @app.route('/', methods=['GET'])
# def home():
#     return "Flask server is running!"

# @app.route('/clear_history', methods=['POST'])
# def clear_history():
#     global previous_responses
#     previous_responses.clear()
#     print("🧹 Cleared previous_responses FIFO queue")
#     return jsonify({"message": "Previous responses cleared."}), 200


# @app.route('/status', methods=['GET'])
# def status():
#     return jsonify({"status": "ok"}), 200

# @app.route('/addConnection', methods=['POST'])
# def add_connection():
#     data = request.json
#     databasetype = data.get("databaseType")
#     url = data.get("url")

#     if not databasetype or not url:
#         return jsonify({"error": "Missing databaseType or url"}), 400

#     try:
#         metadata = MetaData()
#         metadata.reflect(bind=engine)
#         database_conn = Table('database_conn', metadata, autoload_with=engine)

#         stmt = insert(database_conn).values(databasetype=databasetype, url=url)
#         with engine.begin() as conn:
#             conn.execute(stmt)

#         return jsonify({"message": "Connection info saved"}), 201
#     except Exception as e:
#         print("❌ Exception:", e)
#         return jsonify({"error": str(e)}), 500
    

# @app.route('/inspection', methods=['GET'])
# def inspection():
#     try:
#         machine_name = request.args.get("machine_name")
#         sensor_type = request.args.get("sensor_type")
#         machine_id = request.args.get("machine_id")
#         print("machine_name:", machine_name)
#         print("sensor_type:", sensor_type)
#         print("machine_id:", machine_id)

#         metadata = MetaData()
#         metadata.reflect(bind=engine)

#         anomalies = [
#             {
#                 "start": "2024-03-02T21:41:00.000Z",
#                 "end": "2024-03-02T22:55:00.000Z"
#             },
#             {
#                 "start": "2024-03-03T01:55:00.000Z",
#                 "end": "2024-03-03T02:41:00.000Z"
#             },
#             {
#                 "start": "2024-03-03T15:41:00.000Z",
#                 "end": "2024-03-03T17:41:00.000Z"
#             }
#         ]

#         anomalies_current = [
#             {
#                 "start": "2024-03-01T17:41:00.000Z",
#                 "end": "2024-03-01T19:41:00.000Z"
#             }
#         ]

#         if sensor_type == "Current":
#             inference_data_multi = Table('inference_data_multi', metadata, autoload_with=engine)
#             stmt = select(inference_data_multi)
#             print("SQL Statement:", stmt)

#             # ADD THIS BLOCK TO PRINT ALL machine_id VALUES
#             if machine_id:
#                 try:
#                     machine_id_uuid = uuid.UUID(machine_id)
#                     stmt = stmt.where(inference_data_multi.c.machine_id == machine_id_uuid)
#                     print("SQL Statement after filtering:", stmt)
#                 except Exception as e:
#                     print("Invalid UUID format for machine_id:", e)
#                     return jsonify({"error": "Invalid machine_id format"}), 400

#             with engine.connect() as conn:
#                 result = conn.execute(stmt)
#                 multi_value_data = [
#                     {
#                         "timestamp": row["timestamp"].isoformat() + "Z" if row["timestamp"] else None,
#                         "value1": row["value1"],
#                         "value2": row["value2"],
#                         "value3": row["value3"]
#                     }
#                     for row in result.mappings()
#                 ][::100]
#             return jsonify({
#                 "title": f"{machine_name or 'Machine'} - Current Sensor Data",
#                 "x_label": "Time",
#                 "y_label": "Current (A)",
#                 "x_tick_labels": [],
#                 "data_type": "multi",
#                 "multi_value_data": multi_value_data,
#                 "anomalies": anomalies_current
#             }), 200

#         else:
#             # Single-value data from inference_data
#             inference_data = Table('inference_data', metadata, autoload_with=engine)
#             stmt = select(inference_data)
#             with engine.connect() as conn:
#                 result = conn.execute(stmt)
#                 vibration_data = [
#                     {
#                         "timestamp": row["timestamp"].isoformat() + "Z" if row["timestamp"] else None,
#                         "value": row["value"]
#                     }
#                     for row in result.mappings()
#                 ][::4]  # Downsample if needed

#             return jsonify({
#                 "title": f"{machine_name or 'Machine'} - Vibration Sensor Data",
#                 "x_label": "Time",
#                 "y_label": "Vibration (mm/s)",
#                 "x_tick_labels": [],
#                 "data_type": "single",
#                 "vibration_data": vibration_data,
#                 "anomalies": anomalies
#             }), 200

#     except Exception as e:
#         print("❌ Exception:", e)
#         return jsonify({"error": str(e)}), 500
    




# @app.route('/machine-health', methods=['GET'])
# def get_machine_health():
#     try:
#         metadata = MetaData()
#         metadata.reflect(bind=engine)
#         machine_health = Table('critical_health_machine', metadata, autoload_with=engine)

#         stmt = select(machine_health)
#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             machines = [
#                 {
#                     "id": row["machine_id"],
#                     "machine": row["machine_name"],
#                     "severityLevel": row["severity_level"],
#                     "lastAnomaly": row["last_anomaly"].isoformat() if row["last_anomaly"] else None,
#                     "sensorType": row["sensor_type"]
#                 }
#                 for row in result.mappings()
#             ]

#         return jsonify({"machines": machines}), 200
#     except Exception as e:
#         print("❌ Exception:", e)
#         return jsonify({"error": str(e)}), 500
    

# @app.route('/work-order', methods=['POST'])
# def create_work_order():
#     data = request.json
#     try:
#         metadata = MetaData()
#         metadata.reflect(bind=engine)
#         work_orders = Table('work_orders', metadata, autoload_with=engine)

#         # Map camelCase JSON keys to snake_case DB columns
#         work_order_id = uuid.uuid4()
#         page_no = data.get("pageNo")
#         priority = data.get("priority")
#         company_name = data.get("companyName")
#         work_order_no = data.get("workOrderNo")
#         week_no = data.get("weekNo")
#         week_of = data.get("weekOf")
#         equipment_id = data.get("equipmentId")
#         equipment_description = data.get("equipmentDescription")
#         category = data.get("category")
#         building = data.get("building")
#         floor = data.get("floor")
#         room = data.get("room")
#         location_description = data.get("description")  # from "description"
#         emergency_contact = data.get("emergencyContact")
#         special_instructions = data.get("specialInstructions")
#         shop_vendor = data.get("shopVendor")
#         department_name = data.get("departmentName")
#         employee_name = data.get("employee")  # from "employee"
#         task_no = data.get("taskNo")
#         work_description = data.get("workDescription")
#         frequency = data.get("frequency")
#         work_performed_by = data.get("workPerformedBy")
#         completion_date = data.get("date")  # from "date"
#         standard_hours = data.get("standardHours")
#         overtime_hours = data.get("overtimeHours")
#         machine_id = data.get("machine_id")
#         part_numbers = data.get("partNumbers")
#         materials_used = data.get("materialsUsed")

#         # Convert types as needed
#         week_of = data.get("weekOf")
#         completion_date = data.get("weekOf")
#         standard_hours = data.get("standardHours")
#         overtime_hours = data.get("overtimeHours")

#         # Convert week_of
#         week_of = parse_date(data.get("weekOf"))
#         completion_date = parse_date(data.get("weekOf"))

#         # Convert standard_hours and overtime_hours
#         if standard_hours is not None and str(standard_hours).strip() != "":
#             standard_hours = float(standard_hours)
#         else:
#             standard_hours = None

#         if overtime_hours is not None and str(overtime_hours).strip() != "":
#             overtime_hours = float(overtime_hours)
#         else:
#             overtime_hours = None

#         stmt = insert(work_orders).values(
#             id=work_order_id,
#             page_no=page_no,
#             priority=1,
#             company_name=company_name,
#             work_order_no=work_order_no,
#             week_no=week_no,
#             week_of=week_of,
#             equipment_id=equipment_id,
#             equipment_description=equipment_description,
#             category=category,
#             building=building,
#             floor=floor,
#             room=room,
#             location_description=location_description,
#             emergency_contact=emergency_contact,
#             special_instructions=special_instructions,
#             shop_vendor=shop_vendor,
#             department_name=department_name,
#             employee_name=employee_name,
#             task_no=task_no,
#             work_description=work_description,
#             frequency=frequency,
#             work_performed_by=work_performed_by,
#             completion_date=completion_date,
#             standard_hours=standard_hours,
#             overtime_hours=overtime_hours,
#             machine_id=machine_id,
#             part_numbers=part_numbers,
#             materials_used=materials_used
#         )

#         with engine.begin() as conn:
#             conn.execute(stmt)

#             print("Work order Completion Date: --- ", completion_date)
#             scheduled_date = completion_date or date.today()
#             print("Scheduled Date: --- ", scheduled_date)
#              # 🔔 Call to insert maintenance_task entry
#             create_maintenance_task(
#                 conn=conn,
#                 machine_id=machine_id,
#                 machine_name="CNC Machine A",  # Replace with actual machine name if available
#                 category=category,
#                 work_description=work_description,
#                 completion_date=scheduled_date,
#                 standard_hours=standard_hours,
#                 priority=priority,
#                 employee_name=employee_name
#             )

        
#             return jsonify({"message": "Work order created successfully", "id": str(work_order_id)}), 201

#     except Exception as e:
#         print("❌ Exception:", e)
#         return jsonify({"error": str(e)}), 500
    
# def handle_text_query_stream(query_str, response_format):
#     queue = text_responses
#     print("Previous responses:", list(queue))

#     combined_responses = ""
#     if queue:
#         for idx, resp in enumerate(queue, start=1):
#             combined_responses += f"Previous response {idx}: {resp}\n"
#         combined_responses += f"Current query: {query_str}"
#     else:
#         combined_responses = query_str

#     response = query_engine.query(combined_responses)
#     print("SQL Response:", response)

#     missing_data_indicators = [
#         "not in the database", "no specific information available",
#         "I'm sorry", "unable to locate", "not found", "error"
#     ]

#     response_str = str(response)
#     use_second_prompt = any(phrase in response_str.lower() for phrase in missing_data_indicators)

#     system_prompt = "You are a helpful AI assistant." if use_second_prompt else (
#         "Respond using clean Markdown formatting such as **bold headings**, new lines, and bullet points. "
#         "Avoid phrases like 'Sure', 'Here's a refined version', or 'Certainly'. Just give the structured answer."
#     )

#     queue.append(response_str)

#     def generate():
#         import openai
#         openai_response = openai.ChatCompletion.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": response_str if not use_second_prompt else combined_responses}
#             ],
#             stream=True
#         )
#         for chunk in openai_response:
#             content = chunk['choices'][0]['delta'].get('content', '')
#             if content:
#                 yield content

#     return Response(stream_with_context(generate()), mimetype='text/plain')

    
# def create_maintenance_task(conn, machine_id, machine_name, category, work_description, completion_date, standard_hours, priority, employee_name):
#     metadata = MetaData()
#     metadata.reflect(bind=engine)
#     maintenance_task = Table('maintenance_task', metadata, autoload_with=engine)
#     print("Inserting maintenance task for machine_id:", machine_id)
#     # Priority mapping
#     priority_str = 'low'
#     if str(priority) == '1':
#         priority_str = 'high'
#     elif str(priority) == '2':
#         priority_str = 'medium'
#     elif str(priority) == '3':
#         priority_str = 'low'
    
#     first_line = ""
#     if work_description:
#         first_line = work_description.splitlines()[0] if work_description.splitlines() else ""


#     maintenance_task_entry = {
#         "id": uuid.uuid4(),
#         "machine_id": machine_id,
#         "machine_name": machine_name,
#         "task_type": category,
#         "description": first_line,
#         "scheduled_date": completion_date,
#         "duration": int(standard_hours) if standard_hours else 1,
#         "priority": priority_str,
#         "status": "scheduled",
#         "assigned_technician": employee_name
#     }

#     conn.execute(insert(maintenance_task), [maintenance_task_entry])

#     return True
    
# def parse_date(date_str):
#     if not date_str or not str(date_str).strip():
#         return None
#     try:
#         # Try ISO format first
#         return datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError:
#         try:
#             # Try MM/DD/YYYY
#             return datetime.strptime(date_str, "%m/%d/%Y").date()
#         except ValueError:
#             try:
#                 # Try dateutil for any other format
#                 return parser.parse(date_str).date()
#             except Exception:
#                 return None
    
# @app.route('/maintenance-tasks', methods=['GET'])
# def get_maintenance_tasks():
#     try:
#         metadata = MetaData()
#         metadata.reflect(bind=engine)
#         maintenance_tasks = Table('maintenance_task', metadata, autoload_with=engine)
#         print("Maintenance tasks table:", maintenance_tasks)
#         stmt = select(maintenance_tasks)
#         with engine.connect() as conn:
#             result = conn.execute(stmt)
#             tasks = [
#                 {
#                     "id": str(row["id"]),
#                     "machineId": str(row["machine_id"]),
#                     "machineName": row["machine_name"],
#                     "taskType": row["task_type"],
#                     "description": row["description"],
#                     "scheduledDate": row["scheduled_date"].isoformat() if row["scheduled_date"] else None,
#                     "duration": row["duration"],
#                     "priority": row["priority"],
#                     "status": row["status"],
#                     "assignedTechnician": row["assigned_technician"]
#                 }
#                 for row in result.mappings()
#             ]

#         return jsonify({"tasks": tasks}), 200
#     except Exception as e:
#         print("❌ Exception:", e)
#         return jsonify({"error": str(e)}), 500

# from fastapi.responses import StreamingResponse

# def handle_text_query_stream(query_str, response_format):
#     queue = text_responses
#     print("Previous responses:", list(queue))

#     combined_responses = ""
#     if queue:
#         for idx, resp in enumerate(queue, start=1):
#             combined_responses += f"Previous response {idx}: {resp}\n"
#         combined_responses += f"Current query: {query_str}"
#     else:
#         combined_responses = query_str

#     response = query_engine.query(combined_responses)
#     print("SQL Response:", response)

#     missing_data_indicators = [
#         "not in the database", "no specific information available",
#         "I'm sorry", "unable to locate", "not found", "error"
#     ]

#     response_str = str(response)
#     use_second_prompt = any(phrase in response_str.lower() for phrase in missing_data_indicators)

#     system_prompt = "You are a helpful AI assistant." if use_second_prompt else (
#         "Respond using clean Markdown formatting such as **bold headings**, new lines, and bullet points. "
#         "Avoid phrases like 'Sure', 'Here's a refined version', or 'Certainly'. Just give the structured answer."
#     )

#     queue.append(response_str)

#     def generate():
#         openai_response = openai.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": response_str if not use_second_prompt else combined_responses}
#             ],
#             stream=True
#         )
#         for chunk in openai_response:
#             content = chunk.choices[0].delta.get("content", "")
#             if content:
#                 yield content

#     return StreamingResponse(generate(), media_type="text/plain")



# # if __name__ == '__main__':
# #     app.run(debug=True, host='127.0.0.1', port=5001)


import random
from datetime import date, timedelta

# List of machine UUIDs
machine_ids = [
    "2d44f6ce-7f47-41ea-b673-f81c1847a90e",
    "df8d87b4-360d-498d-8854-da713b3df4d5",
    "7f7967c3-fc68-48fa-aea9-b3cf89e82c62",
    "1ae3ff01-b19d-456a-aa4b-16f59beab476",
    "4845cbf3-6cef-4c66-b2e3-874a41f0d63a",
    "f8cba151-2ca3-4575-a9f0-fec6b06edfe2",
    "178d85b5-856a-424f-b066-7ae31a9705c7",
    "39e62077-a4b0-44d6-8459-c8b364a95a85",
    "b5b1f88e-2ad0-4f02-a61d-0c95dbc647f3",
    "a8795833-ca35-4fef-b9c9-a02e2cc00e0f",
    "09ce4fec-8de8-4c1e-a987-9a0080313456"
]

shifts = ["Shift A", "Shift B", "Shift C"]

# Define date range for September 2025
start_date = date(2025, 9, 1)
end_date = date(2025, 9, 30)
delta = timedelta(days=1)

# Open a file to write SQL statements
with open("daily_production_sept2025.sql", "w") as f:
    f.write("-- DailyProduction inserts for September 2025\n")
    
    current_date = start_date
    while current_date <= end_date:
        for machine_id in machine_ids:
            for shift in shifts:
                units_produced = random.randint(100, 150)  # realistic units
                downtime_minutes = random.randint(0, 30)   # downtime in minutes
                notes = "Normal operation" if downtime_minutes < 20 else "Some downtime issues"
                
                sql = f"INSERT INTO DailyProduction (machine_id, date, shift, units_produced, downtime_minutes, notes) " \
                      f"VALUES ('{machine_id}', '{current_date}', '{shift}', {units_produced}, {downtime_minutes}, '{notes}');\n"
                
                f.write(sql)
        current_date += delta

print("SQL script generated: daily_production_sept2025.sql")
