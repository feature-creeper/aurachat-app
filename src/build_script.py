import os
import sys

def update_env_config():
    """Update env_config.py with environment variables during build."""
    env_config_path = os.path.join('aurachat_helper_app', 'env_config.py')
    
    # Get environment variables
    mongodb_uri = os.getenv('MONGODB_URI')
    onlyfansapi_key = os.getenv('ONLYFANSAPI_KEY')
    environment = os.getenv('ENVIRONMENT', 'production')
    
    if not mongodb_uri:
        print("Error: MONGODB_URI environment variable not set")
        sys.exit(1)
        
    if not onlyfansapi_key:
        print("Error: ONLYFANSAPI_KEY environment variable not set")
        sys.exit(1)
    
    # Create the config content
    config_content = f'''# This file is auto-generated during build
MONGODB_URI = "{mongodb_uri}"
ONLYFANSAPI_KEY = "{onlyfansapi_key}"
ENVIRONMENT = "{environment}"
'''
    
    # Write the config file
    with open(env_config_path, 'w') as f:
        f.write(config_content)
        
    print(f"Updated {env_config_path} with environment variables")

if __name__ == '__main__':
    update_env_config() 