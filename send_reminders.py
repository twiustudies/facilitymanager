import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from models import maintenance_plans

# Konfiguration für den E-Mail-Versand
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@example.com"
SMTP_PASSWORD = "your-password"

# Funktion zum Versenden der Erinnerungen
def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, [to_email], msg.as_string())

# Funktion zur Überprüfung und Versendung der Erinnerungen
def check_and_send_reminders():
    today = datetime.today().date()
    for plan in maintenance_plans:
        if not hasattr(plan, 'reminder_enabled') or not plan.reminder_enabled:
            continue  # Überspringen, wenn Erinnerungen deaktiviert sind
        
        maintenance_date = datetime.strptime(plan.date, "%Y-%m-%d").date()
        if maintenance_date in [today + timedelta(days=7), today + timedelta(days=1)]:
            subject = "Maintenance Reminder"
            body = f"Reminder: Maintenance scheduled on {plan.date}. Click here to view: /maintenance/{plan.id}"
            send_email("facility_manager@example.com", subject, body)

if __name__ == "__main__":
    check_and_send_reminders()