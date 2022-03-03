from yargy import Parser, rule, and_, or_
from yargy.predicates import gram
from yargy.pipelines import morph_pipeline
from yargy.interpretation import fact
from IPython.display import display
from yargy.predicates import gram, eq, lte, gte, in_, is_capitalized, dictionary, normalized, caseless,type as typ

from yargy.tokenizer import INT, MorphTokenizer


# tokenizer = MorphTokenizer()

NUM = typ('INT')
DOT = eq('.')

Temperature = fact(
    'Temperature',
    ['min', 'max', 'singular']
)

TEMPSIGN = morph_pipeline([
    '°C',
    '°С'
])
SIGN = or_(
    rule('+'),
    rule('-')
)

Num = fact(
    'Num',
    ['n']
)

SIGNEDINT = rule(
    SIGN,
    NUM
)

_SIGNEDINT = rule(
    SIGNEDINT.interpretation(Num.n)
).interpretation(Num)

TRIPLEPERIOD = rule(
        rule('.'),
        rule('.'),
        rule('.')
)

TEMPERATURE = or_(
    rule(
        SIGNEDINT.interpretation(Temperature.min), 
        or_(TRIPLEPERIOD, rule('-'), rule('…')), 
        SIGNEDINT.interpretation(Temperature.max), 
        TEMPSIGN
    ),
    rule(
        SIGNEDINT.interpretation(Temperature.singular),
        TEMPSIGN
    )
).interpretation(
    Temperature
)


parser = Parser(TEMPERATURE)

def process_care(txt):
    res = [];
    for match in parser.findall(txt):
        element = dict()
        element['min'] = match.fact.min
        element['max'] = match.fact.max
        element['singular'] = match.fact.singular
        
        res.append(element)
        
    return res

if __name__ == '__main__':
    text = '''
    Арбуз — свето- и теплолюбивая культура, плохо переносящая любое затенение. Для нормального развития растений необходима температура +25…+30 °С, для завязи — не ниже +18…+25 °С. Арбуз засухоустойчив, однако довольно отзывчив на полив. Арбуз нетребователен к плодородию, но предпочитает легкие песчаные и супесчаные почвы с нейтральной реакцией, отзывчив на подкормки фосфорным, азотным и калийным удобрениями.Прополку и рыхление проводят по мере появления сорняков и уплотнения почвы.
    Для размещение подходят слегка притененные окна с зимней температурой +12...+15 °C. Летом полив обильный, зимой — умеренный, рекомендуется регулярное опрыскивание. Подкормка производится с апреля по сентябрь раз в 2 недели. Пересаживают весной раз в 2–3 года, используя для посадки почвенную смесь из листовой земли и торфа (1:1).
    '''
    

    res = process_care(text)
    
    for r in res:
        print(r)
        
    # for match in parser.findall(text):
    #     display(match)

    # tokenizer = MorphTokenizer()
    # for line in text.splitlines():
    #     print([_.value for _ in tokenizer(line)])