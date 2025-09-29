#!/usr/bin/env python3
"""
ANGELSUCCESS Cybersecurity Platform - Deployment Test Script
Tests all major functionality after deployment to Railway
"""

import requests
import sys
import time
import json
from urllib.parse import urljoin

class DeploymentTester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.test_results = []
        
    def print_status(self, message, status=None):
        """Print status message with colored output"""
        if status == "SUCCESS":
            print(f"✅ {message}")
        elif status == "FAIL":
            print(f"❌ {message}")
        elif status == "WARNING":
            print(f"⚠️  {message}")
        else:
            print(f"🔍 {message}")
    
    def test_endpoint(self, endpoint, description, method="GET", data=None, expected_status=200):
        """Test a single endpoint"""
        try:
            url = urljoin(self.base_url, endpoint)
            
            if method == "GET":
                response = self.session.get(url, timeout=10)
            elif method == "POST":
                response = self.session.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            if response.status_code == expected_status:
                self.print_status(f"{description}: OK (Status {response.status_code})", "SUCCESS")
                return True
            else:
                self.print_status(f"{description}: Failed (Status {response.status_code})", "FAIL")
                return False
                
        except requests.exceptions.RequestException as e:
            self.print_status(f"{description}: Error - {e}", "FAIL")
            return False
    
    def test_page_load(self, endpoint, description):
        """Test that a page loads successfully"""
        return self.test_endpoint(endpoint, description, "GET", expected_status=200)
    
    def test_api_endpoint(self, endpoint, description):
        """Test API endpoint returns JSON"""
        try:
            url = urljoin(self.base_url, endpoint)
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # Try to parse as JSON
                data = response.json()
                self.print_status(f"{description}: OK - {data.get('status', 'API working')}", "SUCCESS")
                return True
            else:
                self.print_status(f"{description}: Failed (Status {response.status_code})", "FAIL")
                return False
                
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            self.print_status(f"{description}: Error - {e}", "FAIL")
            return False
    
    def test_real_time_data(self):
        """Test real-time data API"""
        try:
            url = urljoin(self.base_url, '/api/realtime-data')
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we have the expected structure
                required_keys = ['ai_confidence', 'system_health', 'threat_feed', 'charts']
                if all(key in data for key in required_keys):
                    self.print_status(f"Real-time Data: OK - AI Confidence: {data['ai_confidence']}%", "SUCCESS")
                    return True
                else:
                    self.print_status("Real-time Data: Incomplete response structure", "WARNING")
                    return True
            else:
                self.print_status(f"Real-time Data: Failed (Status {response.status_code})", "FAIL")
                return False
                
        except Exception as e:
            self.print_status(f"Real-time Data: Error - {e}", "FAIL")
            return False
    
    def test_authentication_flow(self):
        """Test login functionality"""
        try:
            # Test login API
            login_data = {
                'email': 'test@example.com',
                'password': 'password123'
            }
            
            url = urljoin(self.base_url, '/api/auth/login')
            response = self.session.post(url, json=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.print_status("Authentication: Login successful", "SUCCESS")
                    
                    # Store token for authenticated tests
                    token = data.get('token')
                    if token:
                        self.session.headers.update({'Authorization': f'Bearer {token}'})
                        return True
                else:
                    self.print_status(f"Authentication: Login failed - {data.get('message')}", "FAIL")
                    return False
            else:
                self.print_status(f"Authentication: Failed (Status {response.status_code})", "FAIL")
                return False
                
        except Exception as e:
            self.print_status(f"Authentication: Error - {e}", "FAIL")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print(f"🚀 Testing ANGELSUCCESS Deployment at: {self.base_url}")
        print("=" * 60)
        
        tests = [
            # Page load tests
            ("/", "Landing Page"),
            ("/auth", "Authentication Page"),
            ("/dashboard", "Dashboard Page"),
            ("/network-monitor", "Network Monitor Page"),
            ("/ai-analysis", "AI Analysis Page"),
            ("/threat-intelligence", "Threat Intelligence Page"),
            ("/optimization-center", "Optimization Center Page"),
            ("/system-settings", "System Settings Page"),
            ("/free-access", "Free Access Page"),
        ]
        
        # Test all pages
        page_success = 0
        for endpoint, description in tests:
            if self.test_page_load(endpoint, description):
                page_success += 1
            time.sleep(1)  # Be nice to the server
        
        print("\n" + "=" * 60)
        
        # Test API endpoints
        api_tests = [
            ("/api/system-status", "System Status API"),
            ("/api/realtime-data", "Real-time Data API"),
        ]
        
        api_success = 0
        for endpoint, description in api_tests:
            if self.test_api_endpoint(endpoint, description):
                api_success += 1
            time.sleep(1)
        
        print("\n" + "=" * 60)
        
        # Test real-time data specifically
        real_time_success = self.test_real_time_data()
        
        print("\n" + "=" * 60)
        
        # Test authentication
        auth_success = self.test_authentication_flow()
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(tests) + len(api_tests) + 2  # +2 for real-time and auth
        passed_tests = page_success + api_success + (1 if real_time_success else 0) + (1 if auth_success else 0)
        
        print(f"Pages Tested: {page_success}/{len(tests)}")
        print(f"API Endpoints: {api_success}/{len(api_tests)}")
        print(f"Real-time Data: {'✅' if real_time_success else '❌'}")
        print(f"Authentication: {'✅' if auth_success else '❌'}")
        print(f"Overall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! Deployment is successful!")
            return True
        elif passed_tests >= total_tests * 0.8:
            print("⚠️  MOST TESTS PASSED! Deployment is mostly successful.")
            return True
        else:
            print("❌ DEPLOYMENT HAS ISSUES! Check the failed tests above.")
            return False

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        # Default to local development
        base_url = "http://localhost:5000"
    
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')
    
    tester = DeploymentTester(base_url)
    success = tester.run_comprehensive_test()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()