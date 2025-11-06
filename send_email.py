"""
IMS Weather Forecast Automation - Email Delivery Module

Sends daily forecast images via email using SendGrid API.
Designed for automated execution via GitHub Actions or local scheduling.

Environment Variables Required:
    SENDGRID_API_KEY: SendGrid API key for authentication
    FROM_EMAIL: Sender email address (must be verified in SendGrid)
    TO_EMAIL: Recipient email address(es) - comma-separated for multiple

Usage:
    from send_email import send_forecast_email

    success = send_forecast_email(
        image_path="output/daily_forecast.jpg",
        forecast_date="2025-11-05",
        logger=logger,
        dry_run=False
    )
"""

import os
import sys
import base64
import traceback
from pathlib import Path
from typing import Optional
from datetime import datetime

# SendGrid imports
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, To, Cc
    import sendgrid
except ImportError:
    print("ERROR: SendGrid library not installed")
    print("Install with: pip install sendgrid")
    sys.exit(1)


# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

# Email subject and content templates
SUBJECT_TEMPLATE = "תחזית יומית IMS - {date_hebrew}"
HTML_BODY_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            direction: rtl;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: bold;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 16px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
            text-align: center;
        }}
        .content p {{
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            margin-bottom: 20px;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌤️ תחזית יומית - השירות המטאורולוגי</h1>
            <p>{date_hebrew} | {date_english}</p>
        </div>
        <div class="content">
            <p>
                <strong>שלום,</strong>
            </p>
            <p>
                מצורפת תחזית מזג האויר היומית עבור 15 הערים המרכזיות בישראל.
                <br>
                התמונה מוכנה לפרסום כסטורי באינסטגרם.
            </p>
            <p style="color: #667eea; font-weight: bold;">
                📊 15 ערים | 🌡️ טמפרטורות | ☁️ מזג אוויר
            </p>
        </div>
        <div class="footer">
            <p>
                <strong>השירות המטאורולוגי הישראלי</strong>
                <br>
                Israel Meteorological Service
            </p>
            <p>
                תחזית זו נוצרה באופן אוטומטי על ידי מערכת IMS Weather Forecast Automation
            </p>
        </div>
    </div>
</body>
</html>
"""

PLAIN_TEXT_TEMPLATE = """
תחזית יומית IMS - {date_hebrew}
{date_english}

שלום,

מצורפת תחזית מזג האויר היומית עבור 15 הערים המרכזיות בישראל.
התמונה מוכנה לפרסום כסטורי באינסטגרם.

📊 15 ערים | 🌡️ טמפרטורות | ☁️ מזג אוויר

---
השירות המטאורולוגי הישראלי
Israel Meteorological Service

תחזית זו נוצרה באופן אוטומטי על ידי מערכת IMS Weather Forecast Automation
"""


# ============================================================================
# DATE FORMATTING HELPERS
# ============================================================================

def format_date_hebrew(date_str: str) -> str:
    """
    Format date in Hebrew format: DD/MM/YYYY

    Args:
        date_str: Date in YYYY-MM-DD format

    Returns:
        Date in DD/MM/YYYY format (Hebrew style)
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except Exception:
        return date_str


def format_date_english(date_str: str) -> str:
    """
    Format date in English format: Day, Month DD, YYYY

    Args:
        date_str: Date in YYYY-MM-DD format

    Returns:
        Date in English format (e.g., "Wednesday, November 05, 2025")
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%A, %B %d, %Y")
    except Exception:
        return date_str


# ============================================================================
# EMAIL SENDING FUNCTION
# ============================================================================

def send_forecast_email(
    image_path: str,
    forecast_date: str,
    logger,
    dry_run: bool = False
) -> bool:
    """
    Send daily forecast image via email using SendGrid.

    Args:
        image_path: Path to the forecast image (JPG)
        forecast_date: Forecast date in YYYY-MM-DD format
        logger: Logger instance for output
        dry_run: If True, simulate without actually sending

    Returns:
        True if email sent successfully, False otherwise

    Environment Variables:
        SENDGRID_API_KEY: SendGrid API key
        FROM_EMAIL: From address (must be verified in SendGrid)
        TO_EMAIL: To address(es) - comma-separated for multiple
    """

    logger.info("=" * 60)
    logger.info("EMAIL DELIVERY")
    logger.info("=" * 60)

    # Log SendGrid version for debugging
    try:
        sendgrid_version = sendgrid.__version__
        logger.info(f"SendGrid library version: {sendgrid_version}")
    except AttributeError:
        logger.warning("Unable to determine SendGrid library version")

    # ========================================================================
    # VALIDATE ENVIRONMENT VARIABLES
    # ========================================================================

    api_key = os.environ.get('SENDGRID_API_KEY')
    sender_email = os.environ.get('FROM_EMAIL')
    recipient_emails = os.environ.get('TO_EMAIL')

    if not api_key:
        logger.error("Missing environment variable: SENDGRID_API_KEY")
        logger.error("Set with: export SENDGRID_API_KEY='your-api-key'")
        return False

    if not sender_email:
        logger.error("Missing environment variable: FROM_EMAIL")
        logger.error("Set with: export FROM_EMAIL='forecast@example.com'")
        return False

    if not recipient_emails:
        logger.error("Missing environment variable: TO_EMAIL")
        logger.error("Set with: export TO_EMAIL='recipient@example.com'")
        return False

    # Parse multiple recipients (comma-separated)
    recipient_list = [email.strip() for email in recipient_emails.split(',')]

    logger.info(f"Sender: {sender_email}")
    logger.info(f"Recipients: {', '.join(recipient_list)}")
    logger.info(f"Recipient count: {len(recipient_list)} (1 To, {len(recipient_list) - 1} CC)" if len(recipient_list) > 1 else f"Recipient count: 1 (To only)")

    # ========================================================================
    # VALIDATE IMAGE FILE
    # ========================================================================

    image_file = Path(image_path)

    if not image_file.exists():
        logger.error(f"Image file not found: {image_path}")
        return False

    file_size_mb = image_file.stat().st_size / (1024 * 1024)
    logger.info(f"Image file: {image_file.name} ({file_size_mb:.2f} MB)")

    if file_size_mb > 10:
        logger.warning("Image file is large (>10MB) - may cause delivery issues")

    # ========================================================================
    # DRY RUN MODE
    # ========================================================================

    if dry_run:
        logger.info("\n[DRY RUN] Email details:")
        logger.info(f"  From: {sender_email}")
        logger.info(f"  To: {', '.join(recipient_list)}")
        logger.info(f"  Subject: {SUBJECT_TEMPLATE.format(date_hebrew=format_date_hebrew(forecast_date))}")
        logger.info(f"  Attachment: {image_file.name} ({file_size_mb:.2f} MB)")
        logger.info("\n[DRY RUN] Email would be sent via SendGrid API")
        return True

    # ========================================================================
    # PREPARE EMAIL CONTENT
    # ========================================================================

    date_hebrew = format_date_hebrew(forecast_date)
    date_english = format_date_english(forecast_date)

    subject = SUBJECT_TEMPLATE.format(date_hebrew=date_hebrew)
    html_body = HTML_BODY_TEMPLATE.format(
        date_hebrew=date_hebrew,
        date_english=date_english
    )
    plain_body = PLAIN_TEXT_TEMPLATE.format(
        date_hebrew=date_hebrew,
        date_english=date_english
    )

    logger.info(f"\nSubject: {subject}")

    # ========================================================================
    # PREPARE IMAGE ATTACHMENT
    # ========================================================================

    try:
        with open(image_file, 'rb') as f:
            image_data = f.read()

        encoded_file = base64.b64encode(image_data).decode()

        attachment = Attachment(
            FileContent(encoded_file),
            FileName('ims_daily_forecast.jpg'),
            FileType('image/jpeg'),
            Disposition('attachment')
        )

        logger.info("Image attachment prepared")

    except Exception as e:
        logger.error(f"Failed to read image file: {e}")
        return False

    # ========================================================================
    # SEND EMAIL VIA SENDGRID
    # ========================================================================

    try:
        # Create message for first recipient
        # IMPORTANT: Wrap emails in To() and Cc() objects to avoid KeyError: 'email'
        logger.info("Building email message...")
        message = Mail(
            from_email=sender_email,
            to_emails=To(recipient_list[0]),  # Wrap primary recipient in To() object
            subject=subject,
            plain_text_content=plain_body,
            html_content=html_body
        )
        logger.info(f"  Primary recipient: {recipient_list[0]}")

        # Add CC recipients if multiple
        if len(recipient_list) > 1:
            logger.info(f"  Adding {len(recipient_list) - 1} CC recipient(s)...")
            for cc_email in recipient_list[1:]:
                message.add_cc(Cc(cc_email))  # Wrap CC email in Cc() object
                logger.info(f"    CC: {cc_email}")

        # Add attachment
        message.attachment = attachment
        logger.info("  Attachment added")

        # Send via SendGrid
        logger.info("\nSending email via SendGrid API...")

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        # Check response
        if response.status_code in [200, 201, 202]:
            logger.info(f"✓ Email sent successfully!")
            logger.info(f"  Status code: {response.status_code}")
            logger.info(f"  Message ID: {response.headers.get('X-Message-Id', 'N/A')}")
            return True
        else:
            logger.error(f"✗ SendGrid returned unexpected status: {response.status_code}")
            logger.error(f"  Response: {response.body}")
            return False

    except Exception as e:
        logger.error(f"✗ Failed to send email: {e}")
        logger.error(f"✗ Exception type: {type(e).__name__}")

        # Log full traceback for detailed debugging
        logger.error("\n" + "=" * 60)
        logger.error("FULL EXCEPTION TRACEBACK:")
        logger.error("=" * 60)
        tb_str = traceback.format_exc()
        for line in tb_str.split('\n'):
            if line.strip():
                logger.error(line)
        logger.error("=" * 60)

        # Log context information
        logger.error("\nCONTEXT INFORMATION:")
        logger.error(f"  Sender email: {sender_email}")
        logger.error(f"  Recipient count: {len(recipient_list)}")
        logger.error(f"  Primary recipient: {recipient_list[0] if recipient_list else 'N/A'}")
        if len(recipient_list) > 1:
            logger.error(f"  CC recipients: {len(recipient_list) - 1}")
        logger.error(f"  Subject: {subject}")
        logger.error(f"  Attachment size: {file_size_mb:.2f} MB")

        # Provide helpful error messages based on common issues
        error_str = str(e).lower()

        logger.error("\nDIAGNOSTIC SUGGESTIONS:")
        if 'keyerror' in error_str and 'email' in error_str:
            logger.error("  → KeyError: 'email' detected")
            logger.error("     This typically means SendGrid library expects Email objects")
            logger.error("     Check that To() and Cc() wrappers are used correctly")
            logger.error(f"     SendGrid version: {getattr(sendgrid, '__version__', 'unknown')}")
        elif 'unauthorized' in error_str or '401' in error_str:
            logger.error("  → Authentication Error (401):")
            logger.error("     1. Invalid SendGrid API key")
            logger.error("     2. API key not activated")
            logger.error("     3. API key doesn't have mail.send permission")
        elif 'forbidden' in error_str or '403' in error_str:
            logger.error("  → Permission Error (403):")
            logger.error("     1. Sender email not verified in SendGrid")
            logger.error("     2. SendGrid account suspended")
            logger.error("     3. Insufficient permissions")
        elif 'not found' in error_str or '404' in error_str:
            logger.error("  → Not Found Error (404):")
            logger.error("     SendGrid API endpoint not found - check library version")
        else:
            logger.error("  → Unknown error - see traceback above for details")

        return False


# ============================================================================
# COMMAND-LINE INTERFACE (FOR TESTING)
# ============================================================================

def main():
    """Test the email sending functionality from command line."""
    import argparse
    from utils import setup_logging, get_today_date

    parser = argparse.ArgumentParser(
        description='Send IMS forecast email via SendGrid',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables Required:
  SENDGRID_API_KEY    SendGrid API key
  FROM_EMAIL          From email address (verified in SendGrid)
  TO_EMAIL            To email address(es) - comma-separated

Examples:
  # Dry run (test without sending)
  python send_email.py --dry-run

  # Send today's forecast
  python send_email.py --image output/daily_forecast.jpg

  # Send specific date
  python send_email.py --image output/daily_forecast.jpg --date 2025-11-05
        """
    )

    parser.add_argument(
        '--image',
        type=str,
        default='output/daily_forecast.jpg',
        help='Path to forecast image (default: output/daily_forecast.jpg)'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Forecast date in YYYY-MM-DD format (default: today)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate without actually sending email'
    )

    args = parser.parse_args()

    # Setup
    logger = setup_logging()
    forecast_date = args.date if args.date else get_today_date()

    # Send email
    success = send_forecast_email(
        image_path=args.image,
        forecast_date=forecast_date,
        logger=logger,
        dry_run=args.dry_run
    )

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
