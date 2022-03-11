import jsonlines as jl
import re
# from googletrans import Translator
import six
import translators as ts


def translate(text):
    result = ts.google(text, to_language='en')
    return result

file = 'Crawlers\collector\collector\iplants.jl'
file_out = 'Crawlers\collector\collector\iplants_out.jl'

re_names = re.compile('([^\(\)]*)\s\(([^\(\)]*)\)')
re_rus = re.compile('[а-яА-ЯёЁ\,\s]+')
re_trailing = re.compile('[\s:\,\.]+$')

# translator = Translator(service_urls=['translate.googleapis.com'])
# translator = Translator()

with jl.open(file) as input:
    with jl.open(file_out, mode='w') as output:
        for item in input:
            
            new = dict()
            for el in item:
                el_new = re_trailing.sub('', el)
                
                if re_rus.match(el_new):
                    # result = translator.translate(el_new, src='ru', dest='en')
                    result = translate(el_new)
                    new[result.lower()] = item[el]
                else:
                    new[el.lower()] = item[el]
                
            output.write(new)
            
            
print("ended")