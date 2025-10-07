#!/usr/bin/env python3
"""
Scalekit SDK Demo Application

This demo shows how to use the Scalekit Python SDK.
You need to set up your environment variables before running this.
"""

import os
from scalekit import ScalekitClient

def main():
    print("🚀 Scalekit SDK Demo")
    print("=" * 50)
    
    # Check if environment variables are set
    env_url = os.getenv('SCALEKIT_ENV_URL')
    client_id = os.getenv('SCALEKIT_CLIENT_ID')
    client_secret = os.getenv('SCALEKIT_CLIENT_SECRET')
    
    if not all([env_url, client_id, client_secret]):
        print("❌ Missing required environment variables!")
        print("\nPlease set the following environment variables:")
        print("  - SCALEKIT_ENV_URL: Your Scalekit environment URL")
        print("  - SCALEKIT_CLIENT_ID: Your Scalekit client ID")
        print("  - SCALEKIT_CLIENT_SECRET: Your Scalekit client secret")
        print("\nYou can set them in several ways:")
        print("1. Export in your shell:")
        print("   export SCALEKIT_ENV_URL='https://your-org.scalekit.com'")
        print("   export SCALEKIT_CLIENT_ID='your_client_id'")
        print("   export SCALEKIT_CLIENT_SECRET='your_client_secret'")
        print("\n2. Create a .env file in the tests/ directory with:")
        print("   SCALEKIT_ENV_URL=your_env_url_here")
        print("   SCALEKIT_CLIENT_ID=your_client_id_here")
        print("   SCALEKIT_CLIENT_SECRET=your_client_secret_here")
        print("\n3. Set them when running the script:")
        print("   SCALEKIT_ENV_URL=xxx SCALEKIT_CLIENT_ID=xxx SCALEKIT_CLIENT_SECRET=xxx python3 demo.py")
        return
    
    try:
        # Initialize the Scalekit client
        print("🔧 Initializing Scalekit client...")
        sc = ScalekitClient(env_url, client_id, client_secret)
        print("✅ Scalekit client initialized successfully!")
        
        # Example: Get authorization URL
        print("\n📋 Example: Getting authorization URL")
        redirect_uri = "http://localhost:8000/auth/callback"
        auth_url = sc.get_authorization_url(
            redirect_uri,
            state="demo_state",
            connection_id="con_123456789"  # Replace with your actual connection ID
        )
        print(f"🔗 Authorization URL: {auth_url}")
        
        print("\n🎉 Demo completed successfully!")
        print("\nNext steps:")
        print("1. Visit the authorization URL to test the OAuth flow")
        print("2. Check out the README.md for more examples")
        print("3. Explore the tests/ directory for comprehensive usage examples")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nThis might be due to:")
        print("- Invalid credentials")
        print("- Network connectivity issues")
        print("- Invalid connection ID")

if __name__ == "__main__":
    main()
