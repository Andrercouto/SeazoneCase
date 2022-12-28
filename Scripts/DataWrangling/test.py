# Libraries needed.
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import sys
import matplotlib.pyplot as plt
import datetime
import unidecode
import string
import zipfile_deflate64
import scipy.stats as stats
import unidecode
import string

tag_hist_path = r'data\Price_AV_Itapema.zip'
parentZip = zipfile.ZipFile(tag_hist_path, mode="r", compression=zipfile.ZIP_DEFLATED64)
df = pd.read_csv(parentZip.open('Price_AV_Itapema.csv'))
