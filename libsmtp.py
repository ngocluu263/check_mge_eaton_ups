"""
 * Code owner: CCIntegration Inc. / cDrone framework
 * Modified Date: 10/13/16
 * Modified by: Luu Nguyen
 */
 """
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(subject, message):

    sender = "Alert-From-Eyes@ccintegration.com"
    receipt = "luunguyen@ccintegration.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receipt

    # Create the body of the message (a plain-text and an HTML version).
    html = ("""\
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
            <table style ="width:500px">
            <strong>UPS Capacity Information</strong>
            %s
            </table>
            </body>
            </html>
                """ % message
           )

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, receipt, msg.as_string())
    s.quit()


