import re
from fuzzywuzzy import fuzz
import deepl
from pattern_dictionaries import get_dict


def find_classroom(pattern):
    pattern_upper = pattern.upper()
    building = pattern_upper[0:2]
    floor = pattern_upper[2]

    if building in ['NB', 'SB', 'RB', 'IB']:
        answer = f'Učebna {pattern_upper} se nachází v budově {building} (Areál Žižkov) na {floor}. patře. Plánek ' \
                 f'areálu najdeš na https://www.vse.cz/wp-content/uploads/page/2419/planek_cz.pdf'
    elif building in ['JM']:
        answer = f'Učebna {pattern_upper} se nachází v budově {building} (Areál Jižní Město) na {floor}. patře.'
    else:
        answer = f'Učebnu {pattern_upper} neznám. Napsal jsi ji správně?'

    return answer


dict_thresholds = {
    'master': 45,
    'food': 50,
    'general_info': 20,
    'bc_ai': 40,
    'bc_da': 40,
    'bc_ims': 40,
    'bc_mme': 40,
    'bc_mep': 40,
    'mgr_im': 40,
    'mgr_bi': 40,
    'mgr_dab': 40,
    'mgr_eov': 40,
    'mgr_ed': 40,
    'mgr_st': 40,
}


def fuzzy_lookup(my_string, level):
    max_score = 0
    identified_intent = None

    dict = get_dict(level)
    dict_answers = get_dict('answers')

    my_string = my_string.lower()

    # print(dict)

    if level in dict_thresholds.keys():
        threshold = dict_thresholds[level]
    else:
        threshold = 40

    for word in dict.keys():
        score = fuzz.ratio(my_string, word)
        if score >= threshold and score > max_score:
            max_score = score
            identified_intent = word

    if identified_intent:
        print(f'The string "{my_string}" contains the word "{identified_intent}" (score: {max_score})')
        print(f'The corresponding value in the dictionary is {dict[identified_intent]}')
        if level == 'master':
            return dict[identified_intent]
        else:
            return dict_answers[dict[identified_intent]]
    else:
        print('Nothing found')
        if level == 'master':
            return 'general_info'
        else:
            return dict['fallback']


def request_handler(request, deepl_api_key, translate=False):
    if translate:
        translator = deepl.Translator(deepl_api_key)
        translated = translator.translate_text(request, target_lang='EN-US')
        request = translated.text
        source_lang = translated.detected_source_lang
        print(source_lang)
        if source_lang == 'EN':
            source_lang = 'EN-US'
        if source_lang == 'PT':
            source_lang = 'PT-BR'

    pattern_find_classroom = re.compile(r'\b[A-Za-z]{2}\s*\d{3}\b')
    matches_classroom = pattern_find_classroom.findall(request)

    if matches_classroom:
        answer = find_classroom(matches_classroom[0].replace(' ', ''))
        master_intent = 'find_classroom'
    else:
        master_intent = fuzzy_lookup(request, 'master')
        answer = master_intent

    if master_intent != 'find_classroom':
        intent = fuzzy_lookup(request, master_intent)
        answer = intent

    if translate:
        translator = deepl.Translator(deepl_api_key)
        answer = translator.translate_text(answer, target_lang=source_lang).text

    return answer




