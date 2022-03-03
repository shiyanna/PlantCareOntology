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
        or_(TRIPLEPERIOD, rule('-')), 
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
text = '''
бутилон содержат зимой при умеренной температуре (+10...+15 °C), не допуская сквозняков.
Температуры от -50°C до +80°C это нормально...
Температуры -50 - +80°C это нормально...
'''

for match in parser.findall(text):
    display(match.fact)

# tokenizer = MorphTokenizer()
# for line in text.splitlines():
#     print([_.value for _ in tokenizer(line)])