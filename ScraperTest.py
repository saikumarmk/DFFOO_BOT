from gsheets import Sheets
url = 'https://docs.google.com/spreadsheets/d/1oqyT_NxHMkAPenO0lwiRvgT9ZcdBLbjeGcmE5AAYVwE/edit#gid=1899432153'
s = sheets.get(url)
s.sheets[1].to_csv('Spam.csv', encoding='utf-8', dialect='excel')