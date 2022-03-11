import jsonlines as jl
import re

file = 'Crawlers\collector\collector\plantopedia_out.jl'
file_out = 'Crawlers\collector\collector\plantopedia_out2.jl'

re_names = re.compile('([^\(\)]*)\s\(([^\(\)]*)\)')

with jl.open(file) as input:
    with jl.open(file_out, mode='w') as output:
        for item in input:
            
            new = dict()
            for el in item:
                if el == 'header':
                    txt = item[el]
                    _re_result = re_names.findall(txt) 
                    header_ru = _re_result[0][0]
                    header_en = _re_result[0][1]
                    new['header'] = header_en
                    new['header_ru'] = header_ru
                    
                    continue
                # rename to eng
                if el == 'Форма декоративности':          
                    new['decoration_property'] = item[el]
                    continue
                if el == 'Высота':
                    new['height'] = item[el]
                    continue
                if el == 'Значимость в композиции':
                    new['significance_in_composition'] = item[el]
                    continue
                if el == 'Устойчивость в срезке':
                    new['shear_stability'] = item[el]
                    continue
                
                
                new[el.lower()] = item[el]
                
            output.write(new)
            
            
print("ended")