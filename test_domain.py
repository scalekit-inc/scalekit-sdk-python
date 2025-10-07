#!/usr/bin/env python3
"""
Test script to find the correct domain for local Scalekit server
"""

import os
import requests
from scalekit_local import LocalScalekitClient

def test_different_domains():
    """Test different domain configurations"""
    
    base_url = "http://127.0.0.1:8888"
    client_id = os.getenv('SCALEKIT_CLIENT_ID', 'test_client_id')
    client_secret = os.getenv('SCALEKIT_CLIENT_SECRET', 'test_client_secret')
    
    # Common domain patterns for local development
    test_domains = [
        "localhost",
        "127.0.0.1",
        "local.scalekit.com",
        "dev.scalekit.com",
        "scalekit.local",
        "api.localhost",
        "api.scalekit.com"
    ]
    
    print("🔍 Testing different domain configurations...")
    
    for domain in test_domains:
        print(f"\n📋 Testing domain: {domain}")
        
        # Test HTTP request with Host header
        try:
            headers = {"Host": domain}
            response = requests.get(base_url, headers=headers, timeout=5)
            print(f"  HTTP Response: {response.status_code}")
            if response.status_code != 404:
                print(f"  Content: {response.text[:100]}")
        except Exception as e:
            print(f"  HTTP Error: {e}")
        
        # Test with gRPC client
        try:
            env_url = f"http://{domain}:8888"
            client = LocalScalekitClient(env_url, client_id, client_secret, disable_ssl_verification=True)
            print(f"  ✅ gRPC client connected successfully!")
            
            # Try to generate auth URL
            auth_url = client.get_authorization_url(
                "http://localhost:8000/callback",
                state="test",
                connection_id="test"
            )
            print(f"  ✅ Auth URL generated: {auth_url[:50]}...")
            return env_url, client_id, client_secret
            
        except Exception as e:
            print(f"  ❌ gRPC Error: {e}")
    
    return None, None, None

def test_with_env_file():
    """Test using environment variables from .env file"""
    print("\n🔍 Testing with environment variables from .env file...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv('tests/.env')
    
    env_url = os.getenv('SCALEKIT_ENV_URL')
    client_id = os.getenv('SCALEKIT_CLIENT_ID')
    client_secret = os.getenv('SCALEKIT_CLIENT_SECRET')
    
    if env_url and client_id and client_secret:
        print(f"Found environment variables:")
        print(f"  URL: {env_url}")
        print(f"  Client ID: {client_id}")
        print(f"  Client Secret: {'*' * len(client_secret)}")
        
        try:
            client = LocalScalekitClient(env_url, client_id, client_secret, disable_ssl_verification=True)
            print("✅ Client initialized successfully!")
            
            auth_url = client.get_authorization_url(
                "http://localhost:8000/callback",
                state="test",
                connection_id="test"
            )
            print(f"✅ Auth URL: {auth_url}")
            return env_url, client_id, client_secret
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return None, None, None

if __name__ == "__main__":
    print("🚀 Scalekit Local Domain Testing")
    print("=" * 50)
    
    # First try with environment file
    env_url, client_id, client_secret = test_with_env_file()
    
    if not env_url:
        # If that fails, try different domains
        env_url, client_id, client_secret = test_different_domains()
    
    if env_url:
        print(f"\n🎉 Success! Use these settings:")
        print(f"SCALEKIT_ENV_URL={env_url}")
        print(f"SCALEKIT_CLIENT_ID={client_id}")
        print(f"SCALEKIT_CLIENT_SECRET={client_secret}")
    else:
        print("\n❌ No working configuration found.")
        print("You may need to:")
        print("1. Check your local Scalekit server configuration")
        print("2. Verify the expected domain/host header")
        print("3. Check if the server is running on the correct port")
