from cdapython import *
import requests
import pandas as pd

'''
file_df_list = summarize_files(return_data_as='dataframe_list')
# 0 - matching files count
# 1 - subject count related to files
# 2 - Data source (GDC, PDC, etc)
# 3 - Data Type
# 4 - Open/closed
# 5 - file format
# 6 - File type
# 7 - Tumor v nomral
# 8 - Anatomic site
# 9 - Various stats
for entry in file_df_list:
    print(entry)
'''


#summary_file_list = summarize_files(return_data_as='dataframe_list')
#datatype_df = summary_file_list[3]
#print(f"Starting Dataframe:\t{datatype_df.head()}")
#datatype_list = datatype_df['category'].unique()
#print(f"Data Type list: {datatype_list}")
#print(datatype_df.head())


#categorytype = 'WXS'

#datatypeinfo_df = get_file_data(match_all='category = WXS')
#datatypeinfo_df = get_file_data(match_all=f"category = {categorytype}")
#print(datatypeinfo_df.head())
#loc_df = datatypeinfo_df['data_source'].value_counts()
#print(loc_df.head())

"""
datasource_df = summary_file_list[2]
startlist = datasource_df['data_source'].unique()
finallist = []
for item in startlist:
    finallist.append(item.split(' ')[0])
print(finallist)

"""
#print(cda_functions())
#print(columns(table='file'))
#dc = ['GDC', 'IDC']
#dc = ['GDC']
#print(summarize_files(data_source = dc))
print(summarize_subjects())
#dcFileSummaryDFList = summarize_files(data_source= 'IDC', return_data_as='dataframe_list')
#print(dcFileSummaryDFList)
#temp_df = dcFileSummaryDFList[8]
#print(temp_df)
#temp2_df = temp_df['category'].value_counts()
#print(temp2_df)
#final_df = pd.DataFrame({'name':temp2_df.index, 'count':temp2_df.values})
#print(final_df.head())