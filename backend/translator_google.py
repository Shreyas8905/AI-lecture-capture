from googletrans import Translator

def translate_text(text, target_lang="hi"):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang, src="en")
    return translated.text
