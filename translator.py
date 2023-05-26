import ctranslate2
import sentencepiece as spm
import time 
import chinese_converter 
class Translator:
    CTRANSLATE_MODEL: str
    SP_MODEL: str

    def __init__(self, device='cpu'):
        self.translator = ctranslate2.Translator(self.CTRANSLATE_MODEL, device=device)
        self.sp = spm.SentencePieceProcessor(model_file=self.SP_MODEL)
    
    def translate(self, text):
        sentences = text.split("\n")
        print(sentences)
        encoded_text = self.sp.encode(sentences, out_type=str)                        
        translation = self.translator.translate_batch(encoded_text)
        print(translation)
        result = ""
        for i in range(len(translation)):            
            result += self.sp.decode(translation[i].hypotheses[0], out_type=str) + " "
        return result

class TibTranslator(Translator):
    CTRANSLATE_MODEL = 'tib'
    SP_MODEL = 'tib/spm/chn_eng.model'

class KoTranslator(Translator):
    CTRANSLATE_MODEL = 'ko'
    SP_MODEL = 'ko/spm/chn_eng.model'

class SktTagger(Translator):
    CTRANSLATE_MODEL = 'skt-tag'
    SP_MODEL = 'skt-tag/spm/skt-tag8k.model'



