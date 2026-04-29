import pandas as pd
from cdapython import *

#subject_dict = summarize_subjects(return_data_as='dict')['data_source']

#print(len(subject_dict.keys()))
#print(len(subject_dict.values()))

#newdict = {"DataCommons": subject_dict.keys(), "SubjectCount":{subject_dict.values()}}

#df = pd.DataFrame.from_dict({"DataCommons": subject_dict.keys(), "SubjectCount":subject_dict.values()})

#print(df)

filedata = summarize_files(return_data_as='dict')
print(filedata.keys())