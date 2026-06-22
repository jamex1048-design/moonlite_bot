import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

sheet = client.open("Moonlite_DB").sheet1


def save_order(project_id, user, message):

    sheet.append_row([
        project_id,
        user,
        message,
        "PENDING",
        str(datetime.datetime.now())
    ])