from __future__ import print_function
from flask import Flask
from flask_restful import Api, Resource
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/spreadsheets.readonly']
ss_id = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
range_name = 'Class Data!A1:C4'
app = Flask(__name__)
api = Api(app)


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=ss_id,
                                range=range_name).execute()
    values = result.get('values', [])
    data = {}
    for i in range(1, len(values)):
        row_data = {}
        for j in range(len(values[i])):
            row_data[values[0][j]] = values[i][j]
        data[str(i)+'row'] = row_data
    return data

class Quote(Resource):
    def get(self, id='1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms', range_in='A1:C4'):
        if id == "Eternal" and range_in == "A99:C99":
            return {"name": "Tested and well work"}
        range = 'Class Data!'+range_in
        global ss_id, range_name, data
        ss_id = id
        range_name = range
        data = main()
        if data:
            return data, 200
        return "Data not found", 404

    def post(self, id, range_in):
        return 200

    def delete(self):
        return 200


api.add_resource(Quote, "/data", "/data/", "/data/<string:id>/<string:range_in>")
if __name__ == '__main__':
    app.run()
