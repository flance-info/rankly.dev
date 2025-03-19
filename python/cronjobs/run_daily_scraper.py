import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from scraper_wordpress import process_plugins

# Load environment variables
load_dotenv()

def setup_logging():
    """Setup logging directory"""
    base_dir = os.path.dirname(__file__)
    log_dir = os.path.join(base_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def main():
    start_time = datetime.now()
    log_dir = setup_logging()
    
    print(f"\n{'='*50}")
    print(f"🚀 Starting WordPress Plugin Scraper")
    print(f"⏰ Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    try:
        process_plugins()
        
    except Exception as e:
        print(f"❌ Error running scraper: {str(e)}")
        return False
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n{'='*50}")
    print(f"✅ Scraper Completed")
    print(f"⏰ End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⌛ Duration: {duration}")
    print(f"{'='*50}\n")
    
    return True

if __name__ == "__main__":
    main() 