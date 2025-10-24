#!/usr/bin/env python
"""
Static Files Verification Script
This script verifies that static files are properly configured and accessible
"""

import os
import sys
import django
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

def verify_static_files():
    print("🔍 Verifying Django Static Files Configuration")
    print("=" * 60)
    
    # Check settings
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print()
    
    # Check if static directories exist
    print("📁 Checking static directories...")
    for static_dir in settings.STATICFILES_DIRS:
        if os.path.exists(static_dir):
            print(f"✅ Directory exists: {static_dir}")
            # Count files in directory
            file_count = sum(len(files) for _, _, files in os.walk(static_dir))
            print(f"📊 Files in directory: {file_count}")
        else:
            print(f"❌ Directory missing: {static_dir}")
    
    if os.path.exists(settings.STATIC_ROOT):
        print(f"✅ Static root exists: {settings.STATIC_ROOT}")
        file_count = sum(len(files) for _, _, files in os.walk(settings.STATIC_ROOT))
        print(f"📊 Files in static root: {file_count}")
    else:
        print(f"❌ Static root missing: {settings.STATIC_ROOT}")
    
    print()
    
    # Test static file finding
    print("🔍 Testing static file resolution...")
    test_files = [
        "img/pngegg.png",  # From etudiant.html
        "img/capture2.PNG",  # From logiciel.html
        "img/capture.PNG",  # From logiciel.html
        # Add more test files as needed
    ]
    
    for test_file in test_files:
        try:
            resolved_path = finders.find(test_file)
            if resolved_path:
                print(f"✅ Found: {test_file} -> {resolved_path}")
            else:
                print(f"❌ Not found: {test_file}")
        except Exception as e:
            print(f"❌ Error finding {test_file}: {str(e)}")
    
    print()
    
    # Check if collectstatic would work
    print("📋 Static files apps to collect:")
    from django.apps import apps
    for app_config in apps.get_app_configs():
        app_path = os.path.join(app_config.path, 'static')
        if os.path.exists(app_path):
            file_count = sum(len(files) for _, _, files in os.walk(app_path))
            print(f"  - {app_config.name}: {file_count} files")
    
    print()
    print("💡 Remember: In production, serve static files through a web server")
    print("   (nginx/Apache) and not through Django for better performance.")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolv2.settings')
    django.setup()
    
    verify_static_files()