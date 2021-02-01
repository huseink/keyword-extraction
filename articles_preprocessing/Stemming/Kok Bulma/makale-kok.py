
import os
import pandas
import re
import nltk
nltk.download("punkt")
import xml.etree.ElementTree as ET
from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM, java
ZEMBEREK_PATH = './zemberek-full.jar'
startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))


TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
morphology = TurkishMorphology.createWithDefaults()

path = '/home/mert/Desktop/AnahtarSozcukCıkarımı/Kok Bulma/TemizHalleri/Dilbilim.xml'
tree = ET.parse(path)
root = tree.getroot()
varOlanKelimeler = set([])
ozetce = root[0].find('Özetçe').text
ozetce = str(ozetce)
kelimeler = nltk.word_tokenize(ozetce)
yeni_kelimeler= [kelimeler for kelimeler in kelimeler if kelimeler.isalnum()]

pos: List[str] = []
for kelime in yeni_kelimeler:
    analysis: java.util.ArrayList = (
        morphology.analyzeAndDisambiguate(kelime).bestAnalysis()
        )
    for i, analysis in enumerate(analysis, start=1):
        if "UNK" in str(analysis.getDictionaryItem()):
            pos.append(kelime)

        else:
            pos.append(
                str(analysis.getDictionaryItem())
                )

with open('./Makale kok deneme/hukuk-makale-kok.txt', "w", encoding="utf-8") as f:
    for i in pos:
        i=re.sub(r'\[(.*)\]', '', i)
        f.write(i + ' ')
f.close()

