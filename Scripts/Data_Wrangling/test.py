import pandas as pd
import zipfile_deflate64 as zipfile

tag_hist_path = r'data\Price_AV_Itapema.zip'
parentZip = zipfile.ZipFile(tag_hist_path, mode="r", compression=zipfile.ZIP_DEFLATED64)
df = pd.read_csv(parentZip.open('Price_AV_Itapema.csv'))