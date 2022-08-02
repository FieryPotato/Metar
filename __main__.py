import argparse
import re
import requests


URL = 'https://www.aviationweather.gov/metar/data?'\
      'ids={}&format=raw&hours=0&taf={}&layout=on'


CODE_RE = re.compile('\<code\>.*?\<\/code\>')
BR_RE = re.compile('\<br\/\>\&nbsp;\&nbsp;')
TAGS_RE = re.compile('\<.*?\>')


def metar_for(aerodrome: str, taf: str) -> str:
    full_page = requests.get(URL.format(aerodrome, taf)).text
    code = re.findall(CODE_RE, full_page)
    nl_tabtab = [re.sub(BR_RE, '\n\t', c) for c in code]
    metar = [re.sub(TAGS_RE, '', line) for line in nl_tabtab]
    
    return '\n'.join(metar)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--taf', action='store_true', help='Include TAF.')
    parser.add_argument('locations', nargs='*', 
    help='List of aerodrome identifiers.', default=['cyul'])
    
    
    locations = parser.parse_args().locations
    taf = 'on' if parser.parse_args().taf else 'off'
    buffer = []
    
    for aerodrome in locations:
        metar = metar_for(aerodrome, taf=taf)
        buffer.append(aerodrome.upper())
        buffer.append(metar+'\n')
        
        
    print('\n'.join(buffer))
    
        

if __name__ == '__main__':
    main()
