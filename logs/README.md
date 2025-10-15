# Logs Folder

This folder stores log files from the weather forecast automation system.

## Purpose

- Track all operations (downloads, extractions, image generation)
- Debug problems when they occur
- Review history of script execution

## Main Log File

- `forecast_automation.log` - Contains all operation logs

## Log Format

```format
YYYY-MM-DD HH:MM:SS [LEVEL] Message
```

Levels:

- `[INFO]` - Normal operation information
- `[SUCCESS]` - Successful completion of task
- `[WARNING]` - Something unusual (e.g., wrong city count)
- `[ERROR]` - Something failed

## Usage

Check this log file if:

- Script fails or has errors
- Want to verify script ran at 6 AM
- Need to debug unexpected behavior
- Want to see city count warnings
