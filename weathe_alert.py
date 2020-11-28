import smtplib
import requests
import datetime
from requests_html import HTML

now = datetime.datetime.now()
day = now.strftime("%A, %d, %b, %Y")

username = "YOUR_EMAIL@gmail.com"
password = "PASSWORD"
to_mail = "RECIPIENT_EMAIL"


def url_to_txt(url):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text.encode("utf-8")
        return html_text
    return ""


url = "https://safetravel.is/"

html_text = url_to_txt(url)
r_html = HTML(html=html_text)
alert_class = "#warning-menu"
r_alert = r_html.find(alert_class)

if len(r_alert) == 1:
    if len(r_alert[0].text) > 20:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(username, password)

            subject = f"Varovani z {day}"
            body = f"Zde je prehled varovani ze safetravel pro den {day}: \n{r_alert[0].text}"
            msg = f"Subject: {subject}\n\n{body}"

            smtp.sendmail(username, to_mail, msg.encode("utf-8"))
    else:
        print("\nNa dnesni den nejsou hlaseny zadne vystrahy.")
