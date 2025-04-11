# Rankly Python Scripts

This directory contains Python scripts for the Rankly application, primarily focused on WordPress plugin data collection, processing, and analysis.

## Key Scripts

### Data Collection
- `scraper.py` - Web scraper for collecting WordPress plugin data
- `check_proxies.py` - Utility to verify and validate proxy servers
- `extract_search_key.py` - Extracts search keywords from collected data
- `extract_tags.py` - Extracts tags from WordPress plugin metadata

### Data Processing
- `process_stored_plugins.py` - Processes collected plugin data
- `process_stored_plugins_new.py` - Updated version with improved processing
- `populate_plugins.py` - Populates database with processed plugin data
- `clean-table-keyword.py` - Cleans keyword data in database tables

### Database Management
- `migrate.py` - Database migration script
- `vacuum_full.py` - PostgreSQL database optimization script
- `init.py` - Database initialization
- `duplicates.py` - Identifies and manages duplicate entries

### API and Web Server
- `app.py` - Flask application for serving API endpoints

### Utilities
- `count.py` - Counts records in database tables
- `your_script.py` - Template/utility script

## Folders
- `/cronjobs` - Scheduled tasks 
- `/database` - Database connection and model definitions
- `/populate` - Data population scripts
- `/scripts` - Utility scripts

## Requirements
See `requirements.txt` for dependencies.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure database connection in appropriate files
3. Run initialization scripts

## Usage
Most scripts can be run directly with Python:
```python
python scraper.py
```

For scheduled tasks, see the `/cronjobs` directory.