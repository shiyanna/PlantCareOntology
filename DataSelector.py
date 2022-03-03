import jsonlines as jl
import re

from Parser.Yargy.process_care import process_care

file = 'Crawlers\collector\collector\plantopedia.jl'
file_out = 'Crawlers\collector\collector\plantopedia_out.jl'

re_family = re.compile('(Семейство: )?(\w+)')
re_remove_start_trash = re.compile('[\w\d].*')
re_invisible_chars = re.compile('[\r\n\xa0]')
re_duplicate_spaces = re.compile('\s\s+')
re_word_combination = re.compile('[\w\(][\w\s\-\(\)]*[\w\)]')

re_care = re.compile('Уход .*')

with jl.open(file) as input:
    with jl.open(file_out, mode='w') as output:
        for item in input:
            # print(item['header'])
            new = dict()
            new['header'] = item['header']
            
            _results = re_family.findall(item['family'])
            new['family'] = [_r[1] for _r in _results]
            
            for el in item['short_data']:
                _txt = item['short_data'][el]
                _txt = re_invisible_chars.sub('', _txt)
                _txt = re_remove_start_trash.search(_txt).group(0)
                
                _results = re_word_combination.findall(_txt)
                new[el] = [_r for _r in _results]
                
            for el in item['data']:
                _txt = item['data'][el]
                
                # remove duplicate spaces and invisible characters
                _txt = re_duplicate_spaces.sub(' ', _txt)
                _txt = re_invisible_chars.sub('', _txt)
                
                # get description
                if el=='':
                    new['description'] = _txt
                    continue
                
                new[el] = _txt
                
                if re_care.match(el):
                    label = 'Temperature_'
                    parsed_data = process_care(_txt)
                    
                    if len(parsed_data)>0:
                        for index in parsed_data[0]:
                            new[label+index] = parsed_data[0][index]
                
            output.write(new)
            
            
