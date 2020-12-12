import smtplib
import requests
import datetime
from requests_html import HTML


class Alert:

    to_mail = 'DEFAULT@EMAIL.COM'

    def __init__(self):
        r = requests.get("https://safetravel.is/")
        if r.status_code != 200:
            raise Exception("Server is not available")

    def send(self, to_mail=None):
        if to_mail != None:
            self.to_mail = to_mail

        username = "YOUR_EMAIL"
        password = "PASSWORD_TO_YOUR_MAIL"

        now = datetime.datetime.now()
        day = now.strftime("%A, %d, %b, %Y")

        r = requests.get("https://safetravel.is/")

        html_text = r.text.encode("utf-8")
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

                    smtp.sendmail(username, self.to_mail,
                                  msg.encode("utf-8"))
                print("Alert has been sent")
            else:
                print("\nNa dnesni den nejsou hlaseny zadne vystrahy.")

    @classmethod
    def ch_mail(cls, to_mail):
        cls.to_mail = to_mail

    def show(self, msg=None):
        r = requests.get("https://safetravel.is/")

        html_text = r.text.encode("utf-8")
        r_html = HTML(html=html_text)
        alert_class = "#warning-menu"
        r_alert = r_html.find(alert_class)

        if len(r_alert[0].text) > 20:
            print(r_alert[0].text)
            if msg != None:
                print(f"{msg}")
        else:
            print("\nNa dnesni den nejsou hlaseny zadne vystrahy.")
