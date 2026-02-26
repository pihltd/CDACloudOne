from cdapython import *
import pandas as pd



#summarize_subjects(data_source='GC')
subject_df = get_subject_data(data_source='GC')
print(subject_df.head())