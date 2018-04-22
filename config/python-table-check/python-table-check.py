# Overall algorithm
#
# 1. Read array with PR IDs from Google Spreasheets
#    - convert it into 2d array
# 2. Read the list of GitHub PR with their statuses
# 3. Get status of every PR in the Table, convert it to color
# 4. Colorize the Google Spreadsheet depending on the PR's status

WHITE = 0

def read_from_google_docs():
    # From here: https://developers.google.com/sheets/api/quickstart/python
    """
    Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
    """
    from apiclient.discovery import build
    from httplib2 import Http
    from oauth2client import file, client, tools

    # Setup the Sheets API
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    SPREADSHEET_ID = '1uDIcBwqF3WnLn2UFTHB0i7lyqQPXvlQ6g9tAr0_C0L0'
    RANGE_NAME = 'Tab1!U4:W'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        table = [[[0, WHITE], [0, WHITE], [0, WHITE]] for _ in values]

        for i in range(len(values)):
            for j in range(len(values[i])):
                table[i][j][0] = values[i][j]
        return table

table = read_from_google_docs()
print(table)