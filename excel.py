import pandas as pd
import os
import numpy as np


data = pd.read_excel("통합 문서1.xlsx")
print("original: ", data)

data['지출일'] = pd.to_datetime(data['지출일'], format='%Y.%m.%d')
original_start_date = data['지출일'].min()
original_end_date = data['지출일'].max()
new_end_date = pd.to_datetime("2023-10-08")
date_difference = new_end_date - original_end_date

data['지출일'] = data['지출일'] + date_difference

print("changed: ", data)
data.to_excel('통합 문서.xlsx')