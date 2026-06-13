import os
import requests
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")


sources = [
    "bbc-news",
    "cnn",
    "the-times-of-india"
]

headlines = []

for source in sources:

    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"sources={source}&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data["status"] == "ok" and len(data["articles"]) > 0:

        article = data["articles"][0]

        headlines.append({
            "source": source,
            "title": article["title"],
            "url": article["url"],
            "published": article["publishedAt"]
        })


html = """
<html>
<body>
<h2> Daily News Digest</h2>
"""

for item in headlines:

    html += f"""
    <h3>{item['source']}</h3>

    <p>
    <a href="{item['url']}">{item['title']}</a>
    <br>
    Published: {item['published']}
    </p>
    <hr>
    """

html += """
</body>
</html>
"""


msg = MIMEMultipart("alternative")

msg["Subject"] = "Daily News Digest"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO

msg.attach(MIMEText(html, "html"))


with smtplib.SMTP("smtp.gmail.com", 587) as server:

    server.starttls()

    server.login(
        EMAIL_USER,
        EMAIL_PASS
    )

    server.sendmail(
        EMAIL_USER,
        EMAIL_TO,
        msg.as_string()
    )

print("News email sent successfully!")