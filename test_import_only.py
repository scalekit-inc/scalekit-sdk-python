#!/usr/bin/env python3
"""
Simple import compatibility test for scalekit-sdk-python
Tests only the critical imports that were failing in Python 3.10
"""

import sys

def test_critical_imports():
    """Test only the critical imports that were causing issues"""
    print(f"Testing Python {sys.version}")
    print(f"Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print("=" * 60)
    
    success = True
    
    # Test 1: Main client import (this was failing in Python 3.10)
    try:
        from scalekit import ScalekitClient
        print("✅ ScalekitClient import successful")
    except Exception as e:
        print(f"❌ ScalekitClient import failed: {e}")
        success = False
    
    # Test 2: PasswordlessClient import (this was the main issue)
    try:
        from scalekit.passwordless import PasswordlessClient
        print("✅ PasswordlessClient import successful")
    except Exception as e:
        print(f"❌ PasswordlessClient import failed: {e}")
        success = False
    
    # Test 3: DomainClient import (this had the same issue)
    try:
        from scalekit.domain import DomainClient
        print("✅ DomainClient import successful")
    except Exception as e:
        print(f"❌ DomainClient import failed: {e}")
        success = False
    
    # Test 4: Test the specific protobuf enum imports that were causing issues
    try:
        from scalekit.v1.auth.passwordless_pb2 import TemplateType
        print("✅ TemplateType enum import successful")
    except Exception as e:
        print(f"❌ TemplateType enum import failed: {e}")
        success = False
    
    try:
        from scalekit.v1.domains.domains_pb2 import DomainType
        print("✅ DomainType enum import successful")
    except Exception as e:
        print(f"❌ DomainType enum import failed: {e}")
        success = False
    
    print("=" * 60)
    if success:
        print("🎉 ALL CRITICAL IMPORTS SUCCESSFUL!")
        print("The Python 3.10 compatibility issue has been resolved.")
    else:
        print("💥 SOME IMPORTS FAILED!")
        print("The Python 3.10 compatibility issue still exists.")
    
    return success

if __name__ == "__main__":
    success = test_critical_imports()
    sys.exit(0 if success else 1)
