# SendGrid Setup Guide for IMS Weather Forecast

**Phase 4 Implementation - Email Delivery**

This guide walks you through setting up SendGrid for automated email delivery of daily forecast images to your social media team.

---

## Table of Contents

1. [Why SendGrid?](#why-sendgrid)
2. [Prerequisites](#prerequisites)
3. [Step 1: Create SendGrid Account](#step-1-create-sendgrid-account)
4. [Step 2: Verify Your Sender Identity](#step-2-verify-your-sender-identity)
5. [Step 3: Create API Key](#step-3-create-api-key)
6. [Step 4: Configure Your Project](#step-4-configure-your-project)
7. [Step 5: Test Email Sending](#step-5-test-email-sending)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

---

## Why SendGrid?

We chose SendGrid over traditional SMTP (smtplib) for several important reasons:

✅ **Reliability**: SendGrid has 99.99% uptime and handles email delivery professionally
✅ **No ISP Blocks**: Unlike Gmail SMTP, SendGrid won't block your automated emails
✅ **Analytics**: Track delivery status, open rates, and engagement
✅ **API-Based**: Simple REST API instead of complex SMTP configuration
✅ **Free Tier**: 100 emails/day free (perfect for daily forecasts)
✅ **Professional**: Used by major companies for transactional emails

---

## Prerequisites

Before you begin, make sure you have:

- [ ] A valid email address (preferably @ims.gov.il)
- [ ] Access to that email inbox (for verification)
- [ ] Python environment with project dependencies installed
- [ ] The forecast image generation working (Phase 3 complete)

---

## Step 1: Create SendGrid Account

### 1.1 Sign Up

1. Go to **https://signup.sendgrid.com/**
2. Click **"Create Account"**
3. Fill in your details:
   - **Email**: Use your IMS email (noamweisss@icloud.com or IMS work email)
   - **Password**: Create a strong password
   - **Company**: Israel Meteorological Service
   - **Website**: https://ims.gov.il
4. Choose the **Free** plan (100 emails/day)
5. Click **"Create Account"**

### 1.2 Verify Your Email

1. Check your inbox for verification email from SendGrid
2. Click the verification link
3. You'll be redirected to SendGrid dashboard

### 1.3 Complete Onboarding

SendGrid will ask a few questions:
- **Why are you sending emails?**: Select "Marketing" or "Transactional"
- **How many emails per month?**: Select "< 1,000"
- Skip any optional setup steps for now

---

## Step 2: Verify Your Sender Identity

**IMPORTANT**: SendGrid requires sender verification before you can send emails.

### 2.1 Access Sender Authentication

1. In SendGrid dashboard, click **Settings** (left sidebar)
2. Click **Sender Authentication**
3. Click **"Get Started"** under "Single Sender Verification"
   - (This is easier than domain authentication and works great for your use case)

### 2.2 Fill in Sender Details

Complete the form:

| Field | Value |
|-------|-------|
| **From Name** | `IMS Weather Forecast` (or your preferred name) |
| **From Email** | Your verified email address |
| **Reply To** | Same as From Email (or different if you want) |
| **Company Address** | IMS official address |
| **City** | Bet Dagan (or IMS location) |
| **State** | Israel |
| **Zip Code** | Your postal code |
| **Country** | Israel |
| **Nickname** | `IMS-Daily-Forecast` |

### 2.3 Verify Email Address

1. Click **"Create"**
2. Check your inbox for verification email
3. Click **"Verify Single Sender"** in the email
4. You'll see a success message

✅ **Status**: Your sender email is now verified and ready to use!

---

## Step 3: Create API Key

### 3.1 Navigate to API Keys

1. In SendGrid dashboard, go to **Settings** → **API Keys**
2. Click **"Create API Key"** (top right)

### 3.2 Configure API Key

1. **API Key Name**: `IMS-Weather-Forecast-Automation`
2. **API Key Permissions**: Choose one of:
   - **Full Access** (easiest - recommended for testing)
   - **Restricted Access** → check only **"Mail Send"** (more secure for production)
3. Click **"Create & View"**

### 3.3 Copy Your API Key

⚠️ **CRITICAL STEP - READ CAREFULLY**:

1. You'll see your API key displayed **ONCE** (it starts with `SG.`)
2. **COPY IT IMMEDIATELY** - You won't be able to see it again!
3. Save it temporarily in a secure location (password manager or secure note)
4. Do NOT share this key or commit it to git

**Example format**: `SG.aBc123xYz...` (it's quite long)

If you lose it, you'll need to create a new one.

---

## Step 4: Configure Your Project

### 4.1 Install Dependencies

```bash
# Navigate to project directory
cd /path/to/Automated-Daily-Forecast

# Install new dependencies
pip install -r requirements.txt
```

This installs:
- `sendgrid` - SendGrid Python library
- `python-dotenv` - Environment variable management

### 4.2 Create .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in your text editor

3. Fill in your actual values:

```bash
# ============================================================================
# SendGrid Configuration
# ============================================================================

# Paste your SendGrid API key here (from Step 3.3)
SENDGRID_API_KEY=SG.aBc123xYz...paste_your_actual_key_here...

# Your verified sender email (from Step 2.2)
SENDER_EMAIL=noamweisss@icloud.com
SENDER_NAME=IMS Weather Forecast

# ============================================================================
# Email Recipients
# ============================================================================

# Add recipient email(s) - comma-separated for multiple
RECIPIENT_EMAILS=social-media-team@ims.gov.il

# Optional: CC recipients
# CC_EMAILS=backup@ims.gov.il,manager@ims.gov.il

# ============================================================================
# Email Settings
# ============================================================================

EMAIL_SUBJECT=Daily Weather Forecast - {date}

# Environment: development or production
ENVIRONMENT=development
```

### 4.3 Verify .env is Ignored by Git

```bash
# This should output ".env" - confirming it's in .gitignore
grep "^.env$" .gitignore
```

✅ **Your API key is now secure and will NOT be committed to git!**

---

## Step 5: Test Email Sending

### 5.1 Test with Dry Run (Recommended First)

```bash
# Dry run - validates everything without sending
python send_email.py --dry-run
```

**Expected output**:
```
============================================================
IMS WEATHER FORECAST - EMAIL DELIVERY
============================================================
Validating configuration...
Validating image: output/daily_forecast.jpg
✓ Image validated: 197.6 KB
Preparing email...
From: IMS Weather Forecast <noamweisss@icloud.com>
To: social-media-team@ims.gov.il
Subject: Daily Weather Forecast - 05/11/2025
============================================================
DRY RUN MODE - Email not actually sent
============================================================
Email would be sent with:
  - Attachment: daily_forecast.jpg (197.6 KB)
  - Recipients: 1
  - Environment: development
```

### 5.2 Send Test Email (For Real)

First, **update recipient email to YOUR OWN EMAIL** in `.env`:

```bash
# In .env file, temporarily change to your email
RECIPIENT_EMAILS=your-email@example.com
```

Then send:

```bash
# Send actual test email
python send_email.py
```

**Expected output**:
```
============================================================
IMS WEATHER FORECAST - EMAIL DELIVERY
============================================================
...
Sending email via SendGrid...
============================================================
✓ Email sent successfully!
Status code: 202
============================================================
```

### 5.3 Check Your Inbox

1. Open your email inbox
2. Look for email from **IMS Weather Forecast**
3. Open the email - it should have:
   - ✅ Hebrew subject and content
   - ✅ Professional HTML formatting
   - ✅ Attached forecast image (daily_forecast.jpg)
   - ✅ "DEVELOPMENT ENVIRONMENT" warning badge

**If you received the email successfully**: 🎉 **Setup complete!**

### 5.4 Update Recipients

Once testing works, update `.env` with real recipients:

```bash
# Change back to actual social media team email(s)
RECIPIENT_EMAILS=social-media-team@ims.gov.il,another-person@ims.gov.il
```

For production, also change:

```bash
ENVIRONMENT=production
```

---

## Troubleshooting

### Problem: "Missing required environment variables"

**Solution**: Check that `.env` file exists and has all required fields filled in.

```bash
# Verify .env exists
ls -la .env

# Check contents (will show variable names but not values for security)
cat .env
```

### Problem: "HTTP 403" Error

**Cause**: API key lacks permissions or is invalid.

**Solutions**:
1. Verify API key is copied correctly (no extra spaces)
2. Create new API key with "Full Access" or "Mail Send" permission
3. Update `SENDGRID_API_KEY` in `.env` with new key

### Problem: "HTTP 401" Error

**Cause**: API key is invalid or expired.

**Solution**: Create a new API key in SendGrid dashboard and update `.env`.

### Problem: "Sender verification issue"

**Cause**: Sender email not verified in SendGrid.

**Solution**:
1. Go to SendGrid → Settings → Sender Authentication
2. Check if your sender email is verified (green checkmark)
3. If not, verify it via email

### Problem: "Image file not found"

**Cause**: Forecast image doesn't exist yet.

**Solution**: Generate the image first:

```bash
# Generate forecast image
python generate_forecast_image.py

# Then send email
python send_email.py
```

### Problem: Email sends but doesn't arrive

**Solutions**:
1. **Check spam folder** - sometimes new senders go to spam
2. **Check SendGrid Activity Feed**:
   - SendGrid Dashboard → Activity Feed
   - Shows delivery status, bounces, etc.
3. Wait 1-2 minutes - sometimes there's a delay
4. Verify recipient email is correct in `.env`

### Problem: Hebrew text shows as gibberish

**Solution**: This shouldn't happen with our HTML email template, but if it does:
1. Verify `.env` file is saved with UTF-8 encoding
2. Check that `send_email.py` has `<meta charset="UTF-8">` in HTML

---

## Next Steps

### Integration with Workflow

Once SendGrid is working, integrate it into your automation workflow:

**Option 1: Manual Testing**
```bash
# Run complete workflow manually
python forecast_workflow.py     # Downloads, extracts, generates image
python send_email.py            # Sends email
```

**Option 2: Automated Workflow** (Phase 4 - To be implemented)
```bash
# Update forecast_workflow.py to include email sending
# Add email step after image generation
```

### Email Customization

You can customize the email by editing `send_email.py`:

**Subject line**: Update `EMAIL_SUBJECT` in `.env`
```bash
EMAIL_SUBJECT=תחזית יומית - {date}
```

**Email body**: Edit the `create_email_body()` function in `send_email.py` (lines 100-150)

**Add more recipients**: Add comma-separated emails in `.env`
```bash
RECIPIENT_EMAILS=person1@ims.gov.il,person2@ims.gov.il,person3@ims.gov.il
```

### Monitoring & Analytics

**SendGrid Dashboard Features**:

1. **Activity Feed**: Real-time email delivery tracking
   - Dashboard → Activity Feed
   - See: Delivered, Opened, Clicked, Bounced

2. **Statistics**: Email performance over time
   - Dashboard → Stats
   - Track delivery rates, engagement

3. **Alerts**: Set up email alerts for issues
   - Settings → Alerts
   - Get notified of bounces or spam reports

### Production Checklist

Before going to production:

- [ ] SendGrid sender email verified
- [ ] API key created with appropriate permissions
- [ ] `.env` file configured with real recipient emails
- [ ] Test email sent and received successfully
- [ ] `.env` file in `.gitignore` (security check)
- [ ] `ENVIRONMENT=production` in `.env`
- [ ] Email sending integrated into workflow
- [ ] Schedule automation (Windows Task Scheduler - Phase 4)

---

## Security Best Practices

1. **NEVER commit `.env` to git** - it contains your API key
2. **Use Restricted Access API key** for production (only "Mail Send" permission)
3. **Regenerate API key** if compromised
4. **Keep SendGrid password secure** - use password manager
5. **Monitor Activity Feed** for suspicious activity

---

## Getting Help

### SendGrid Resources

- **SendGrid Docs**: https://docs.sendgrid.com/
- **Python Library**: https://github.com/sendgrid/sendgrid-python
- **Support**: https://support.sendgrid.com/

### Project Support

- **Issues**: Contact Noam W (noamweisss@icloud.com)
- **Documentation**: See `CLAUDE.md` and `README.md`

---

**Last Updated**: November 5, 2025
**Phase**: Phase 4 - Email Delivery Setup
**Status**: Ready for Implementation 🚀
