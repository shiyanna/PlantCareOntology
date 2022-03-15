import jsonlines as jl
import re
# from googletrans import Translator
# import six
# import translators as ts

from Parser.Yargy.process_lang import process_plant_height, process_seasons


# def translate(text):
#     result = ts.google(text, to_language='en')
#     return result

file = 'Crawlers\collector\collector\plantopedia_out2.jl'
file_out = 'Crawlers\collector\collector\plantopedia_out3.jl'

re_names = re.compile('([^\(\)]*)\s\(([^\(\)]*)\)')
re_rus = re.compile('[а-яА-ЯёЁ\,\s]+')
re_trailing = re.compile('[\s:\,\.]+$')


with jl.open(file) as input:
    with jl.open(file_out, mode='w') as output:
        # iterr = 0
        for item in input:
            # iterr = iterr + 1
            # if iterr > 5 : break
            
            new = dict()
            
            # seasons
            for el in item:
                if el == 'сроки цветения':
                    arr = item[el]
                    
                    fl_s = []
                    
                    for i in arr:
                        fl_s.append(process_seasons(i)[0])
                    
                    new['flowering_season'] = fl_s
                    continue
                
                if el == 'height':
                    arr = item[el]
                    
                    fl_s = []
                    
                    for i in arr:
                        fl_s.append(process_plant_height(i)[0])
                    
                    new['height'] = fl_s
                    continue
            
                new[el] = item[el]
                
                # el_new = re_trailing.sub('', el)
                
                # if re_rus.match(el_new):
                #     result = translate(el_new)
                #     new[result.lower()] = item[el]
                # else:
                #     new[el.lower()] = item[el]
                
                
                
            output.write(new)
            
            
print("ended")