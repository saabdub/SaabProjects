import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import io


def email(html : str):
    s = smtplib.SMTP(host='smtp.office365.com', port=587)
    s.starttls()
    s.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = os.getenv('EMAIL_USER')
    msg['Subject'] = "chart"
    msg.attach(MIMEText(html, 'html'))
    s.send_message(msg)
    del msg
    s.quit()




def scatterPlot(df:pd.DataFrame(),x : str, y : str):

    # Create a DataFrame with x and y values
    #

    # Create the scatter chart
    df.plot(kind='scatter', x=x, y=y)

    # Save the chart as a PNG file
    img_bytes = io.BytesIO()
    # Save the chart to the BytesIO object
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Encode the image data as a base64 string
    img_str = base64.b64encode(img_bytes.getvalue()).decode()
    # Create the HTML for the email
    html = f'<p><img src="data:image/png;base64,{img_str}"></p>'
    email(html)


df = pd.DataFrame({'x':[1,2,3,4,35], 'y':[5,4,3,2,1]})
scatterPlot(df,"x","y")