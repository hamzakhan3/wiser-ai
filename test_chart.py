#!/usr/bin/env python3

import requests
import json

def test_chart_endpoint():
    """Test the chart endpoint"""
    url = "http://localhost:5001/query"
    
    # Test data
    test_data = {
        "query": "Show me a chart of machine status",
        "source": "chat-page",
        "responseFormat": "markdown"
    }
    
    try:
        print("🧪 Testing chart endpoint...")
        print(f"📤 Sending request to: {url}")
        print(f"📤 Data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!")
            print(f"📊 Response: {data.get('response', 'No response')[:200]}...")
            print(f"📊 Chart Data: {data.get('chart_data', 'No chart data')}")
            print(f"📊 ASCII Chart: {data.get('ascii_chart', 'No ASCII chart')}")
            print(f"📊 Chart Type: {data.get('chart_type', 'No chart type')}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"❌ Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to backend. Make sure the Flask app is running on port 5001")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_chart_endpoint()
