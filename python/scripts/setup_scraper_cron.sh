#!/bin/bash

# Directory for logs
mkdir -p /home/ubuntu/rankly/rankly/python/logs

# Add both cron jobs to run at different times
(crontab -l 2>/dev/null; echo "0 2 * * * cd /home/ubuntu/rankly/rankly && docker-compose exec -T python python /app/python/run_daily_scraper.py >> /home/ubuntu/rankly/rankly/python/logs/scraper.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "40 2 * * * cd /home/ubuntu/rankly/rankly && docker-compose exec -T python python /app/python/plugin_tags_populate_simple.py >> /home/ubuntu/rankly/rankly/python/logs/tags_populate.log 2>&1") | crontab -

echo "Cron jobs installed successfully!"
echo "1. Scraper will run daily at 2 AM"
echo "2. Tags population will run daily at 2:30 AM"
echo "Logs will be written to:"
echo "- /home/ubuntu/rankly/rankly/python/logs/scraper.log"
echo "- /home/ubuntu/rankly/rankly/python/logs/tags_populate.log" 