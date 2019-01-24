from bs4 import BeautifulSoup
import requests

START_STR = '''
<table class="table table-dark">
    <thead>
      <tr>
        <th>Channel</th>
        <th>Members</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
'''

END_STR = '''
    </tbody>
</table>
'''

IDS = ['Englishdaybyday', 'Englishoftheday', 'TinyFacts', 'KeepInspiring', 
'OpenLibrary', 'EnglishStoriesTM', 'Vocabulix', 'GlobalTube', 'IdiomsLand', 
'PhrasalCards', 'MusicRegion', 'GrammarCards', 'EnglishGate', 'SlangWords', 
'Wallpaperarea', 'FactsLegend', 'Humourger', 'English_Songs_and_Lyrics', 
'ProverbsinEnglish', 'MydownloadTube', 'Quotery', 'Quotelicious']

BASE_URL = 'https://t.me/'

def format_row(id_, membersK_, status_=False):
    if status_:
        status = '<div class="spinner-grow text-success">'
    else:
        status = ''

    return '''
      <tr>
        <td><a href="{0}{1}">@{1}</a></div></td>
        <td>{2}K</td>
        <td>{3}</td>
      </tr>'''.format(BASE_URL, id_, membersK_, status)

def get_members(id_):
    url = BASE_URL + id_
    r  = requests.get(url)
    data = r.text
    # print(data.encode("utf-8"))
    soup = BeautifulSoup(data, "html.parser")
    members_class = soup.find(attrs={'class':'tgme_page_extra'})
    members = ' '.join(members_class.text.split()[:2])
    members_int = int(members.replace(' ', ''))
    return {'int':members_int, 'str':members, 'K':members_int//1000}

for id in IDS:
    status = 0
    inK = get_members(id)['K']
    if get_members(id)['int'] > 50000:
        status = 1
    else:
        status = 0
    print(format_row(id, inK, status_=status))