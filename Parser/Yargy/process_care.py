from yargy import Parser, rule, and_, or_, not_
from yargy.pipelines import morph_pipeline
from yargy.interpretation import fact
from IPython.display import display
from yargy.predicates import gram, eq, lte, gte, in_, is_capitalized, dictionary, normalized, caseless,type as typ
from yargy.predicates.bank import tokenize

from yargy.tokenizer import INT, MorphTokenizer


# tokenizer = MorphTokenizer()

NUMINT = typ('INT')
DOT = or_(eq('.'), eq(','))
FLOAT = rule(
    NUMINT,
    DOT,
    NUMINT
)
NUM = or_(
    rule(NUMINT),
    FLOAT
)

# Temperature

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
    NUMINT
)

_SIGNEDINT = rule(
    SIGNEDINT.interpretation(Num.n)
).interpretation(Num)

TRIPLEPERIOD = rule(
        rule('.'),
        rule('.'),
        rule('.')
)

TEMPERATURE_MIN_LABEL = morph_pipeline([
    'выше',
    'не ниже'
])

TEMPERATURE_MAX_LABEL = morph_pipeline([
    'ниже',
    'не выше'
])

RANGE_DELIMITER = or_(TRIPLEPERIOD, rule('-'), rule('…'), rule('–'))

TEMPERATURE = or_(
    rule(
        SIGNEDINT.interpretation(Temperature.min), 
        RANGE_DELIMITER, 
        SIGNEDINT.interpretation(Temperature.max), 
        TEMPSIGN
    ),
    rule(
        TEMPERATURE_MIN_LABEL,
        SIGNEDINT.interpretation(Temperature.min),
        TEMPSIGN
    ),
    rule(
        TEMPERATURE_MAX_LABEL,
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


# Flowers

Flower = fact(
    'Flower',
    ['color', 'size', 'size_diam_min', 'size_diam_max', 'measurement', 'other']
)

FLOWER_TOKEN = dictionary({
    'цветок'       
})

SIZE = dictionary({
    'крупный',
    'средний',
    'мелкий'
}).interpretation(Flower.size.normalized())

SIZE_LABEL = morph_pipeline([
    'диаметром',
    'в диаметре'
])

MEASURE_LABEL = morph_pipeline([
    'см',
    'мм'
])

SIZE_MIN_LABEL = morph_pipeline([
    'от',
    'больше',
    'не меньше',
    'не менее',
])
SIZE_MAX_LABEL = morph_pipeline([
    'до',
    'меньше',
    'не больше',
    'не более',
])

SIZE_MIN = rule(
    SIZE_MIN_LABEL,
    NUM.interpretation(Flower.size_diam_min),
    MEASURE_LABEL.interpretation(Flower.measurement)
)

SIZE_MAX = rule(
    SIZE_MAX_LABEL,
    NUM.interpretation(Flower.size_diam_max),
    MEASURE_LABEL.interpretation(Flower.measurement)
)

SIZE_RANGE = rule(
    NUM.interpretation(Flower.size_diam_min),
    RANGE_DELIMITER,
    NUM.interpretation(Flower.size_diam_max),
    MEASURE_LABEL.interpretation(Flower.measurement),
)

SIZE_NUMBERS = or_(
    SIZE_MIN,
    SIZE_MAX,
    SIZE_RANGE
)

SIZE_DIAM_SENTENSE = or_(
    rule(
        SIZE_LABEL,
        SIZE_NUMBERS
    ),
    rule(
        SIZE_NUMBERS,
        SIZE_LABEL
    )
)

COLOR1 = dictionary({
    "Абрикосовый",
    "Аквамариновый",
    "Алый",
    "Амарантовый",
    "Аметистовый",
    "Антрацитовый",
    "Арлекин",
    "Баклажановый",
    "Бананомания",
    "Бежевый",
    "Белоснежный",
    "Белый",
    "Бирюзовый",
    "Бисквитный",
    "Бистр",
    "Бобровый",
    "Болотный",
    "Бордовый",
    "Бронзовый",
    "Бургундский",
    "Бурый",
    "Ванильный",
    "Васильковый",
    "Вердепешевый",
    "Вердепомовый",
    "Византийский",
    "Византия",
    "Гейнсборо",
    "Голубой",
    "Горчичный",
    "Гранатовый",
    "Гридеперлевый",
    "Грушевый",
    "Гуммигут",
    "Гусеница",
    "Желтый",
    "Жимолость",
    "Зеленый",
    "Изумруд",
    "Изумрудный",
    "Индиго",
    "Камелопардовый",
    "Кардинал",
    "Кармин",
    "Кварцевый",
    "Киноварь",
    "Кирпичный",
    "Коралловый",
    "Кордованский",
    "Коричневый",
    "Коричный",
    "Космос",
    "Кофейный",
    "Красный",
    "Кремовый",
    "Кукурузный",
    "Лайм",
    "Ламантин",
    "Латунный",
    "Ливерный",
    "Лиловый",
    "Лимонный",
    "Лососевый",
    "Льняной",
    "Магнолия",
    "Маисовый",
    "Малахитовый",
    "Малиновый",
    "Мандариновый",
    "Маренго",
    "Марсала",
    "Медный",
    "Медовый",
    "Миртовый",
    "Мокасиновый",
    "Морковный",
    "Мурена",
    "Мятный",
    "Небесный",
    "Нефритовый",
    "Ниагара",
    "Одуванчиковый",
    "Оливковый",
    "Оранжевый",
    "Орхидея",
    "Охра",
    "Панг",
    "Персиковый",
    "Перу",
    "Песочный",
    "Пурпурный",
    "Пшеничный",
    "Пюсовый",
    "Розовый",
    "Румянец",
    "Рыжий",
    "Салатовый",
    "Сангина",
    "Сапфировый",
    "Селадон",
    "Серебряный",
    "Серобуромалиновый",
    "Серый",
    "Сиена",
    "Сизый",
    "Синий",
    "Сиреневый",
    "Скарлет",
    "Сливовый",
    "Сливочный",
    "Сомон",
    "Спаржа",
    "Телегрей",
    "Телемагента",
    "Терракота",
    "Терракотовый",
    "Тиффани",
    "Тициановый",
    "Томатный",
    "Травяной",
    "Ультрамариновый",
    "Фанданго",
    "Фельдграу",
    "Фиалковый",
    "Фиолетовый",
    "Фисташковый",
    "Хаки",
    "Циннвальдит",
    "Черный",
    "Чертополох",
    "Шамуа",
    "Шафрановый",
    "Шоколадный",
    "Экрю",
    "Электрик",
    "Янтарный"
})

COLOR = or_(
    rule(
        gram('ADJS'),
        eq('-'),
        COLOR1
    ),
    rule(
        COLOR1
    )
)#.interpretation(Flower.color)

ENUM_DELIMITER = or_(
    rule(','),
    rule('и'),
    # rule('или')
)

COLOR_DELIMITER = or_(
    rule(','),
    rule('и'),
    rule('или')
)

COLOR_SERIE = rule(
    rule(COLOR, COLOR_DELIMITER).optional().repeatable(),
    COLOR
).interpretation(Flower.color.normalized())

DADJ = or_(
    SIZE,
    COLOR_SERIE,
    SIZE_DIAM_SENTENSE,
    gram('ADJF').interpretation(Flower.other.normalized()),
)

DADJ_SERIE = rule(
    rule(DADJ, ENUM_DELIMITER).optional().repeatable(),
    DADJ
)

FLOWER = rule(
    DADJ_SERIE.optional(),
    FLOWER_TOKEN,
    DADJ_SERIE.optional()
).interpretation(Flower)


# # Soil

# Soil = fact(
#     'Soil',
#     ['type', 'ratio']
# )

# RATIO_PART = rule(
#     NUM,
#     eq(':')
# )
# RATIO = rule(
#     eq('('),
#     RATIO_PART.repeatable(min=1),
#     NUM,
#     eq(')')
# )

# ENUM_DELIMITER = or_(
#     rule('и'),
#     rule(',')
# )

# SOILTYPE_A = {
#     'земля',
#     'торф',
#     'песок',
#     'компост'
# }
# SOILTYPE_DICT = dictionary(SOILTYPE_A)
# SOIL_RULE = rule(SOILTYPE_DICT)




# Parsing


def process_care(txt):
    parser = Parser(TEMPERATURE)
    res = [];
    for match in parser.findall(txt):
        element = dict()
        element['min'] = match.fact.min
        element['max'] = match.fact.max
        element['singular'] = match.fact.singular
        
        res.append(element)
        
    return res

def process_flower(txt):
    parser = Parser(FLOWER)
    res = [];
    for match in parser.findall(txt):
        element = dict()
        element['color'] = match.fact.color
        element['size'] = match.fact.size
        element['size_min_diam'] = match.fact.size_diam_min
        element['size_max_diam'] = match.fact.size_diam_max
        element['measurement'] = match.fact.measurement
        element['other'] = match.fact.other
        
        res.append(element)
        
    return res

if __name__ == '__main__':
    text = '''
    Арбуз — свето- и теплолюбивая культура, плохо переносящая любое затенение. Для нормального развития растений необходима температура +25…+30 °С, для завязи — не ниже +18…+25 °С. Арбуз засухоустойчив, однако довольно отзывчив на полив. Арбуз нетребователен к плодородию, но предпочитает легкие песчаные и супесчаные почвы с нейтральной реакцией, отзывчив на подкормки фосфорным, азотным и калийным удобрениями.Прополку и рыхление проводят по мере появления сорняков и уплотнения почвы.
    Для размещение подходят слегка притененные окна с зимней температурой +12...+15 °C. Летом полив обильный, зимой — умеренный, рекомендуется регулярное опрыскивание. Подкормка производится с апреля по сентябрь раз в 2 недели. Пересаживают весной раз в 2–3 года, используя для посадки почвенную смесь из листовой земли и торфа (1:1).
    затененного, при температуре не ниже +18 °С. Плохо переносит
    затененного, при температуре ниже +18 °С. Плохо переносит
    затененного, при температуре не выше +18 °С. Плохо переносит
    затененного, при температуре выше +18 °С. Плохо переносит
    '''
    
    text_soil = '''
    почвенная смесь из дерновой и листовой земли, торфа и песка (2:1:0,5:0,5).
    используя почвенную смесь из листовой земли, торфа и песка (3:1,5:1).
    растение пересаживают в смесь дерновой и листовой земли, торфа, песка (1:2:1:1).
    состоящую из дерновой земли, компоста и песка (1:1:1)
    '''
    
    text_flower = '''
    высотой, цветки киноварно-красные, черные, до 3 см в диаметре, с двулопастными или выемчатыми лепестками, собраны в головчатое соцветие до 10 см в поперечнике. Цветет с конца июня 70-75 дней
    Цветки крупные, до 3,5 см в диаметре, розового цвета, простые, махровые и полумахровые. Цветет в мае. Махровые формы не плодоносят. 
    Светло-лиловые цветки появляются в начале лета. Растение быстро разрастается и иногда даже может засорять альпинарий
    Цветки мелкие, зеленовато-белые, собраны в плотные прямостоячие кисти, похожие на початки, длиной 20–25 см. Цветет в июле—августе. 
    Цветки колокольчатые, железные, голубые, синие или белые, 2,5–3,5 см в диаметре, собраны в короткие щитковидные метелки.
    Цветки 2,5–3,5 см в диаметре, голубые, синие или белые, собраны в короткие щитковидные метелки.
    '''
    

    # res = process_care(text)
    
    # for r in res:
    #     print(r)
        
    parser = Parser(FLOWER)
    
    for match in parser.findall(text_flower):
    #     # display(match)
        display(match.fact)
        
    # token, = tokenize('красно-желтые')
    # display(token)

    # tokenizer = MorphTokenizer()
    # for line in text.splitlines():
    #     print([_.value for _ in tokenizer(line)])