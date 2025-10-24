#!/usr/bin/env python
\"\"\"
Production Static Files Collection Script
This script properly collects static files for production deployment
\"\"\"

import os
import sys
from django.core.management import execute_from_command_line
from django.conf import settings

def collect_static_files():
    \"\"\"Collect static files for production\"\"\"
    print(\"Starting static files collection for production...\")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolv2.settings')
    
    try:
        # Run collectstatic command
        print(\"Running collectstatic command...\")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
        print(\"✅ Static files collected successfully!\")
        
        # Verify static files directory
        static_root = os.path.join(settings.BASE_DIR, 'staticfiles')
        if os.path.exists(static_root):
            print(f\"📁 Static files directory exists: {static_root}\")
            files_count = sum([len(files) for r, d, files in os.walk(static_root)])
            print(f\"📊 Total static files: {files_count}\")
        else:
            print(\"❌ Static files directory does not exist!\")
            
    except Exception as e:
        print(f\"❌ Error collecting static files: {str(e)}\")
        return False
    
    return True

def verify_static_settings():
    \"\"\"Verify static files settings\"\"\"
    print(\"\\n🔍 Verifying static files settings...\")
    
    print(f\"STATIC_URL: {settings.STATIC_URL}\")
    print(f\"STATIC_ROOT: {settings.STATIC_ROOT}\")
    print(f\"STATICFILES_DIRS: {settings.STATICFILES_DIRS}\")
    
    # Check if static directories exist
    for static_dir in settings.STATICFILES_DIRS:
        if os.path.exists(static_dir):
            print(f\"✅ Static directory exists: {static_dir}\")
        else:
            print(f\"❌ Static directory missing: {static_dir}\")
    
    if os.path.exists(settings.STATIC_ROOT):
        print(f\"✅ Static root exists: {settings.STATIC_ROOT}\")
    else:
        print(f\"❌ Static root missing: {settings.STATIC_ROOT}\")

if __name__ == \"__main__\":
    # Import Django settings
    import django
    django.setup()
    
    print(\"🚀 Production Static Files Setup\")
    print(\"=\" * 50)
    
    # Verify settings first
    verify_static_settings()
    
    print(\"\\n\" + \"=\" * 50)
    
    # Collect static files
    success = collect_static_files()
    
    if success:
        print(\"\\n🎉 Static files collection completed successfully!\")
        print(\"💡 Remember to serve static files through your web server (nginx/Apache)\")
        print(\"   in production, not through Django.\")
    else:
        print(\"\\n❌ Static files collection failed!\")
        sys.exit(1)