from __future__ import print_function
from flask import Flask
from flask_restful import Api, Resource
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/spreadsheets.readonly']
ss_id = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
range_name = 'Class Data!A1:C4'
glob_key = 'AIzaSyB95yOG33_SeFX8gVD_4DaBxFYOQia2HiQ'
app = Flask(__name__)
api = Api(app)


def main():
    service = build('sheets', 'v4', developerKey=glob_key)
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
        if id == "<example_id>" and range_in == "<example_range>":
            return {"name": "Test, well works"}
        range = 'Class Data!'+range_in
        global ss_id, range_name, data
        ss_id = id
        range_name = range
        data = main()
        if data:
            return data, 200
        return "Data not found", 404

    def post(self):
        return 200

    def delete(self):
        return 200


api.add_resource(Quote, "/data", "/data/", "/data/<string:id>/<string:range_in>")
if __name__ == '__main__':
    app.run()
