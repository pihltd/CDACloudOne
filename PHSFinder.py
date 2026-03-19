import cdapython as cda
import pandas as pd
import sys


subject_df = cda.get_subject_data(add_columns='project_id')
subject_df = subject_df.explode('project_id')
print(subject_df)
mask = subject_df['project_id'].str.contains('phs', case=False, na=False)
phs_subject_df = subject_df[mask]

print(phs_subject_df)
sys.exit(0)

t = cda.columns(table='project')
print(t)

project_df = cda.column_values('project_id')
print(project_df.head(5))

#print(project_df['project_id'].str.contains('phs', case=False, na=False))
mask = project_df['project_id'].str.contains('phs', case=False, na=False)
print(project_df[mask].sample(10))

