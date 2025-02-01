import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import schedule
import time
import config

# Email configuration
SENDER_EMAIL = config.SENDER_EMAIL
SENDER_PASSWORD = config.SENDER_PASSWORD
RECEIVER_EMAIL = config.RECEIVER_EMAIL
SMTP_SERVER = config.SMTP_SERVER
SMTP_SSL_PORT = config.SMTP_SSL_PORT

def generate_report():
    """Generates the daily report content."""

    today = datetime.date.today().strftime("%Y-%m-%d")
    report_content = f"""
    Daily Report - {today}

    This is the body of your daily report.  You can include 
    whatever information you need here.  For example:

    * Number of new users: 123
    * Sales: $456.78
    * Active users: 789

    You can also format the report using HTML if you prefer.
    """
    return report_content

def send_email(report_content):
    """Sends the email report."""

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = f"Daily Report - {datetime.date.today().strftime('%Y-%m-%d')}"

    # Attach the report content (you can use HTML here if needed)
    message.attach(MIMEText(report_content, "plain")) # or "html" if using HTML content

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SSL_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        print("Email report sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def send_daily_report():
    report = generate_report()
    send_email(report)

# Schedule the email to be sent daily at a specific time (e.g., 8:00 AM)
schedule.every().day.at("08:00").do(send_daily_report)  # Adjust the time as needed

print("Starting scheduler.  Reports will be sent daily at 08:00.")

while True:
    schedule.run_pending()
    time.sleep(1) # Check every second if a task needs to be run.  Can be adjusted.