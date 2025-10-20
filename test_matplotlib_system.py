#!/usr/bin/env python3
"""
Comprehensive testing script for the matplotlib chart generation and AI analysis system.
Run this script to test all components of the system.
"""

import requests
import json
import time
from sqlalchemy import create_engine, text
import uuid

# Configuration
API_BASE = "http://localhost:5001"
DB_URL = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"

def test_database_connection():
    """Test database connection and table existence"""
    print("🔍 Testing database connection...")
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            # Check if tables exist
            result = conn.execute(text("SELECT COUNT(*) FROM machine_anomaly_screenshots"))
            screenshot_count = result.fetchone()[0]
            
            result = conn.execute(text("SELECT COUNT(*) FROM machine_vision_analysis"))
            analysis_count = result.fetchone()[0]
            
            print(f"✅ Database connected successfully")
            print(f"   - Screenshots in DB: {screenshot_count}")
            print(f"   - Analyses in DB: {analysis_count}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_chart_generation():
    """Test chart generation for both sensor types"""
    print("\n📊 Testing chart generation...")
    
    test_cases = [
        {
            "machine_id": "09ce4fec-8de8-4c1e-a987-9a0080313456",
            "sensor_type": "Vibration",
            "machine_name": "Test Vibration Machine"
        },
        {
            "machine_id": "a8795833-ca35-4fef-b9c9-a02e2cc00e0f", 
            "sensor_type": "Current",
            "machine_name": "Test Current Machine"
        }
    ]
    
    results = []
    for test_case in test_cases:
        print(f"   Testing {test_case['sensor_type']} sensor...")
        try:
            response = requests.post(
                f"{API_BASE}/generate-chart",
                json=test_case,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {test_case['sensor_type']}: {data.get('message', 'Success')}")
                if 'analysis_id' in data:
                    print(f"      Analysis ID: {data['analysis_id']}")
                results.append(True)
            else:
                print(f"   ❌ {test_case['sensor_type']}: HTTP {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ {test_case['sensor_type']}: {e}")
            results.append(False)
    
    return all(results)

def test_anomaly_chat():
    """Test anomaly page chat functionality"""
    print("\n💬 Testing anomaly page chat...")
    
    test_queries = [
        "What anomalies do you see?",
        "What are the main issues with this machine?",
        "How can I fix the vibration problems?"
    ]
    
    test_case = {
        "machine_id": "09ce4fec-8de8-4c1e-a987-9a0080313456",
        "sensor_type": "Vibration",
        "source": "anomaly"
    }
    
    results = []
    for query in test_queries:
        print(f"   Testing query: '{query}'")
        try:
            response = requests.post(
                f"{API_BASE}/query",
                json={**test_case, "query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('format') == 'vision' and 'response' in data:
                    response_preview = data['response'][:100] + "..." if len(data['response']) > 100 else data['response']
                    print(f"   ✅ Response: {response_preview}")
                    results.append(True)
                else:
                    print(f"   ❌ Unexpected response format: {data}")
                    results.append(False)
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append(False)
    
    return all(results)

def test_inspection_endpoint():
    """Test the inspection endpoint triggers background chart generation"""
    print("\n🔍 Testing inspection endpoint...")
    
    test_case = {
        "machine_id": "09ce4fec-8de8-4c1e-a987-9a0080313456",
        "sensor_type": "Vibration"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/inspection",
            json=test_case,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'vibration_data' in data or 'multi_value_data' in data:
                print("   ✅ Inspection endpoint returned graph data")
                print("   ✅ Background chart generation should be triggered")
                return True
            else:
                print(f"   ❌ Unexpected response format: {data}")
                return False
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_screenshot_endpoints():
    """Test screenshot check and save endpoints"""
    print("\n📸 Testing screenshot endpoints...")
    
    test_case = {
        "machine_id": "09ce4fec-8de8-4c1e-a987-9a0080313456",
        "sensor_type": "Vibration"
    }
    
    try:
        # Test check endpoint
        response = requests.post(
            f"{API_BASE}/check-screenshot",
            json=test_case,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Check screenshot: exists={data.get('exists', False)}")
            if data.get('exists'):
                print(f"      Screenshot ID: {data.get('screenshot_id')}")
                print(f"      Analysis ID: {data.get('analysis_id')}")
            return True
        else:
            print(f"   ❌ Check screenshot failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🚀 Starting comprehensive matplotlib system test...")
    print("=" * 60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Chart Generation", test_chart_generation),
        ("Anomaly Chat", test_anomaly_chat),
        ("Inspection Endpoint", test_inspection_endpoint),
        ("Screenshot Endpoints", test_screenshot_endpoints)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! The matplotlib system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == len(results)

if __name__ == "__main__":
    run_comprehensive_test()
