def spell_out_pos_tags(pos):
    if pos == "V":
        return "verb"
    elif pos == "NC":
        return "common noun"
    elif pos == "NP":
        return "proper noun"
    elif pos == "ADJ":
        return "adjective"
    elif pos == "ADV":
        return "adverb"
    elif pos == "PRON":
        return "pronoun"
    elif pos == "PP":
        return "postposition"
    elif pos == "PREV":
        return "preverb"
    elif pos == "CC":
        return "conjunction"
    elif pos == "CX":
        return "conjunctive particle"
    elif pos == "PRL":
        return "relative pronoun"
    elif pos == "JJ":
        return "adjective"
    return pos 

def replace_tags(tag_string):
    replacement_dict = {    
        'PPP': 'past passive participle (ppp) ',
        'NC': 'common noun ',
        'CADP': 'preverb ',
        'CAD': 'adverb ',
        'CCD': 'coordinating conjunction ',
        'CCM': 'particle for comparison ',
        'CEM': 'emphatic particle ',
        'CGDA': 'absolutive ',
        'CGDI': 'infinitive ',
        'CNG': 'negation ',
        'CQT': 'quotation particle ',
        'CSB': 'subordinating conjunction ',
        'CX': 'adverb/indeclinable ',
        'JJ': 'adjective ',
        'JQ': 'quantifying adjective ',
        'KDG': 'gerundive ',
        'KDP': 'participle ',
        'NUM': 'number ',
        'PPR': 'personal pronoun ',
        'PPX': 'other word inflected like a pronoun ',
        'PRC': 'reciprocal pronoun ',
        'PRD': 'demonstrative pronoun ',
        'PRI': 'indefinite pronoun ',
        'PRL': 'relative pronoun ',
        'PRQ': 'interrogative pronoun ',
        'Gen,': 'genitive, ',
        'Nom': 'nominative ',
        'Abl': 'ablative ',
        'Dat': 'dative ',
        'Ins': 'instrumental ',
        'Loc': 'locative ',
        'Voc': 'vocative ',
        'Acc': 'accusative ',
        'Sing': 'singular',
        'Masc': 'masculine',
        'Fem': 'feminine',
        'Neut': 'neuter',
        'Pres': 'present',
        'Fut': 'future',
        'Imp': 'imperative',
        'Aor': 'aorist',
        'Perf': 'perfect',
        'Opt': 'optative',
        'Impf': 'imperfect',
        'Pass': 'passive',
        'Mid': 'middle',
        'Act': 'active',
        'Ind': 'indicative',
        'V ': 'finite verb ',
        'Cpd': 'compound ',
        '1': 'singular',
        '2': 'dual',
        '3': 'plural',
        }   
    for key in replacement_dict:
        tag_string = tag_string.replace(key, replacement_dict[key])
        tag_string = tag_string.replace("|", " ")
    return tag_string


def create_dictionary(path):    
    # read dictionary from path csv
    df = pd.read_csv(path, sep='\t', encoding='utf-8', low_memory=False, names=['word', 'meanings'])
    # creater dictionary with column 'word' as key and column 'meanings' as value    
    dictionary = {}
    for index, row in df.iterrows():
        if type(row['word']) == str:
            current_head_word = row['word'].strip()
            if current_head_word not in dictionary:
                dictionary[current_head_word] =  str(row['meanings'])
            else:
                dictionary[current_head_word] += "; " + str(row['meanings'])    
    return dictionary
    
