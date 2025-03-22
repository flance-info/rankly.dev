#!/bin/bash

# Directory for logs
mkdir -p /home/rankly/python/cronjobs/logs

# Add both cron jobs to run at different times
(crontab -l 2>/dev/null; echo "0 2 * * * cd /home/rankly/python/cronjobs && docker exec -T beautiful_diffie python /app/python/run_daily_scraper.py >> /home/rankly/python/cronjobs/logs/scraper.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "40 2 * * * cd /home/rankly/python/cronjobs && docker exec -T beautiful_diffie python /app/python/plugin_tags_populate_simple.py >> /home/rankly/python/cronjobs/logs/tags_populate.log 2>&1") | crontab -

echo "Cron jobs installed successfully!"
echo "1. Scraper will run daily at 2 AM"
echo "2. Tags population will run daily at 2:30 AM"
echo "Logs will be written to:"
echo "- /home/rankly/python/cronjobs/logs/scraper.log"
echo "- /home/rankly/python/cronjobs/logs/tags_populate.log" 