#!/usr/bin/env python
import os
import sys
import django
import requests
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

def test_notification_api():
    base_url = "http://localhost:8000/api"
    
    # Test 1: Get notifications (requires authentication)
    print("Testing notification API endpoints...")
    
    try:
        # Test notifications endpoint
        response = requests.get(f"{base_url}/notifications/")
        print(f"GET /notifications/ - Status: {response.status_code}")
        if response.status_code == 200:
            notifications = response.json()
            print(f"Found {len(notifications)} notifications")
        else:
            print(f"Response: {response.text}")
            
        # Test unread count endpoint
        response = requests.get(f"{base_url}/notifications/unread-count/")
        print(f"GET /notifications/unread-count/ - Status: {response.status_code}")
        if response.status_code == 200:
            count_data = response.json()
            print(f"Unread count: {count_data.get('count', 0)}")
        else:
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the server first.")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_notification_api() 