# Archive Folder

This folder stores historical XML weather forecast files downloaded from IMS.

## Purpose

- Keep last 14 days of XML files for backup/fallback
- Automatically cleaned up (files older than 14 days are deleted)

## File Naming Convention

- Format: `isr_cities_YYYY-MM-DD.xml`
- Example: `isr_cities_2025-10-15.xml`

## Automated Management

- New file added daily when `download_forecast.py` runs
- Old files (>14 days) deleted automatically
- Used as fallback if fresh download fails
