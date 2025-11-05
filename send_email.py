#!/usr/bin/env python3
"""
IMS Weather Forecast Automation - Email Delivery Module
Sends daily forecast images to social media team using SendGrid.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Email,
    To,
    Content,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition
)
import base64

from utils import setup_logging

# Load environment variables from .env file
load_dotenv()

# Setup logging
logger = setup_logging()

# ============================================================================
# Configuration
# ============================================================================

# SendGrid API Key
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# Sender information
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_NAME = os.getenv('SENDER_NAME', 'IMS Weather Forecast')

# Recipients
RECIPIENT_EMAILS_STR = os.getenv('RECIPIENT_EMAILS', '')
RECIPIENT_EMAILS = [email.strip() for email in RECIPIENT_EMAILS_STR.split(',') if email.strip()]

CC_EMAILS_STR = os.getenv('CC_EMAILS', '')
CC_EMAILS = [email.strip() for email in CC_EMAILS_STR.split(',') if email.strip()]

# Email subject template
EMAIL_SUBJECT_TEMPLATE = os.getenv('EMAIL_SUBJECT', 'Daily Weather Forecast - {date}')

# Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
DEFAULT_IMAGE_PATH = OUTPUT_DIR / "daily_forecast.jpg"

# ============================================================================
# Validation Functions
# ============================================================================

def validate_configuration() -> bool:
    """
    Validate that all required environment variables are set.

    Returns:
        bool: True if configuration is valid, False otherwise
    """
    missing = []

    if not SENDGRID_API_KEY or SENDGRID_API_KEY == 'your_sendgrid_api_key_here':
        missing.append('SENDGRID_API_KEY')

    if not SENDER_EMAIL or SENDER_EMAIL == 'your-verified-email@example.com':
        missing.append('SENDER_EMAIL')

    if not RECIPIENT_EMAILS:
        missing.append('RECIPIENT_EMAILS')

    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        logger.error("Please copy .env.example to .env and fill in your values")
        return False

    return True

def validate_image_path(image_path: Path) -> bool:
    """
    Validate that the image file exists and is readable.

    Args:
        image_path: Path to image file

    Returns:
        bool: True if valid, False otherwise
    """
    if not image_path.exists():
        logger.error(f"Image file not found: {image_path}")
        return False

    if not image_path.is_file():
        logger.error(f"Path is not a file: {image_path}")
        return False

    if image_path.stat().st_size == 0:
        logger.error(f"Image file is empty: {image_path}")
        return False

    return True

# ============================================================================
# Email Functions
# ============================================================================

def create_email_body(date_str: str, environment: str) -> str:
    """
    Create the HTML body for the forecast email.

    Args:
        date_str: Forecast date in DD/MM/YYYY format
        environment: Environment (development/production)

    Returns:
        str: HTML email body
    """
    # Add environment badge for non-production
    env_badge = ""
    if environment.lower() != 'production':
        env_badge = f'<p style="color: #e67e22; font-weight: bold;">⚠️ {environment.upper()} ENVIRONMENT</p>'

    html_body = f"""
    <html dir="rtl" lang="he">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    direction: rtl;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #3498db;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 20px;
                    border: 1px solid #ddd;
                }}
                .footer {{
                    background-color: #34495e;
                    color: white;
                    padding: 15px;
                    text-align: center;
                    font-size: 12px;
                    border-radius: 0 0 5px 5px;
                }}
                .attachment-note {{
                    background-color: #e8f4f8;
                    border-right: 4px solid #3498db;
                    padding: 10px;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>תחזית מזג אוויר יומית</h1>
                    <p>שירות המטאורולוגיה הישראלי</p>
                </div>

                <div class="content">
                    {env_badge}

                    <h2>שלום,</h2>

                    <p>מצורפת תחזית מזג האוויר היומית ל-{date_str} עבור 15 ערים מרכזיות בישראל.</p>

                    <div class="attachment-note">
                        <strong>📎 קובץ מצורף:</strong> daily_forecast.jpg<br>
                        <small>תמונה בפורמט אינסטגרם סטורי (1080x1920px) מוכנה לפרסום</small>
                    </div>

                    <p><strong>הערות:</strong></p>
                    <ul>
                        <li>התמונה כוללת תחזית עבור 15 ערים (מצפון לדרום)</li>
                        <li>מוצגים: סמל מזג אוויר, טמפרטורת מקסימום ומינימום, ושם העיר</li>
                        <li>מוכנה לפרסום ישיר ברשתות החברתיות</li>
                    </ul>

                    <p>תחזית נעימה,<br>
                    מערכת התחזית האוטומטית של שירות המטאורולוגיה</p>
                </div>

                <div class="footer">
                    <p>שירות המטאורולוגיה הישראלי (IMS)<br>
                    מייל זה נוצר אוטומטית - אנא אל תשיבו ישירות</p>
                    <p><small>נוצר ב-{datetime.now().strftime('%d/%m/%Y בשעה %H:%M')}</small></p>
                </div>
            </div>
        </body>
    </html>
    """

    return html_body

def send_forecast_email(
    image_path: Optional[Path] = None,
    forecast_date: Optional[str] = None,
    dry_run: bool = False
) -> bool:
    """
    Send daily forecast email with image attachment using SendGrid.

    Args:
        image_path: Path to forecast image (defaults to output/daily_forecast.jpg)
        forecast_date: Forecast date in DD/MM/YYYY format (defaults to today)
        dry_run: If True, validate but don't actually send email

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    logger.info("=" * 60)
    logger.info("IMS WEATHER FORECAST - EMAIL DELIVERY")
    logger.info("=" * 60)

    # Use defaults if not provided
    if image_path is None:
        image_path = DEFAULT_IMAGE_PATH

    if forecast_date is None:
        forecast_date = datetime.now().strftime('%d/%m/%Y')

    # Validate configuration
    logger.info("Validating configuration...")
    if not validate_configuration():
        return False

    # Validate image
    logger.info(f"Validating image: {image_path}")
    if not validate_image_path(image_path):
        return False

    logger.info(f"✓ Image validated: {image_path.stat().st_size / 1024:.1f} KB")

    # Prepare email
    logger.info("Preparing email...")
    subject = EMAIL_SUBJECT_TEMPLATE.format(date=forecast_date)
    html_content = create_email_body(forecast_date, ENVIRONMENT)

    # Read and encode image
    logger.info("Reading image file...")
    with open(image_path, 'rb') as f:
        image_data = f.read()

    encoded_image = base64.b64encode(image_data).decode()

    # Create email
    from_email = Email(SENDER_EMAIL, SENDER_NAME)
    to_emails = [To(email) for email in RECIPIENT_EMAILS]

    logger.info(f"From: {SENDER_NAME} <{SENDER_EMAIL}>")
    logger.info(f"To: {', '.join(RECIPIENT_EMAILS)}")
    if CC_EMAILS:
        logger.info(f"CC: {', '.join(CC_EMAILS)}")
    logger.info(f"Subject: {subject}")

    # Dry run check
    if dry_run:
        logger.info("=" * 60)
        logger.info("DRY RUN MODE - Email not actually sent")
        logger.info("=" * 60)
        logger.info("Email would be sent with:")
        logger.info(f"  - Attachment: {image_path.name} ({image_path.stat().st_size / 1024:.1f} KB)")
        logger.info(f"  - Recipients: {len(RECIPIENT_EMAILS)}")
        logger.info(f"  - Environment: {ENVIRONMENT}")
        return True

    # Create message
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content
    )

    # Add CC recipients if any
    if CC_EMAILS:
        message.cc = [To(email) for email in CC_EMAILS]

    # Add attachment
    attachment = Attachment(
        FileContent(encoded_image),
        FileName('daily_forecast.jpg'),
        FileType('image/jpeg'),
        Disposition('attachment')
    )
    message.attachment = attachment

    # Send email
    try:
        logger.info("Sending email via SendGrid...")
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        logger.info("=" * 60)
        logger.info(f"✓ Email sent successfully!")
        logger.info(f"Status code: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"✗ Failed to send email: {str(e)}")
        logger.error("=" * 60)

        # Provide helpful error messages
        if "403" in str(e):
            logger.error("HTTP 403: Check that your SendGrid API key is valid and has mail send permissions")
        elif "401" in str(e):
            logger.error("HTTP 401: Your API key is invalid or expired")
        elif "sender" in str(e).lower():
            logger.error("Sender verification issue: Ensure sender email is verified in SendGrid")

        return False

# ============================================================================
# Main Function
# ============================================================================

def main():
    """Main entry point for email sending script."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Send daily weather forecast email with SendGrid'
    )
    parser.add_argument(
        '--image',
        type=str,
        help='Path to forecast image (default: output/daily_forecast.jpg)'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Forecast date in DD/MM/YYYY format (default: today)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate configuration but do not send email'
    )

    args = parser.parse_args()

    # Convert image path to Path object if provided
    image_path = Path(args.image) if args.image else None

    # Send email
    success = send_forecast_email(
        image_path=image_path,
        forecast_date=args.date,
        dry_run=args.dry_run
    )

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
