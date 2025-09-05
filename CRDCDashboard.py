from shiny import Inputs, Outputs, Session, ui, render,reactive, App
from cdapython import *
from shinywidgets import render_widget, output_widget
import plotly.express as px
from CRDCDashboardModules import dropdown_ui
import pandas as pd



####################################
#                                  #
#         Subroutines              #
#                                  #
####################################

def dcSpecificFileSummary(dc = None):
    if dc == None:
        dcFileSummaryDFList = summarize_files(return_data_as='dataframe_list')
    else:
        dcFileSummaryDFList = summarize_files(data_source= dc, return_data_as='dataframe_list')
    return dcFileSummaryDFList

def dcSpecificSubjectSummary(dc = None):
    if dc == None:
        dcSubjectSummaryDFList = summarize_subjects(return_data_as='dataframe_list')
    else:
        dcSubjectSummaryDFList = summarize_subjects(data_source= dc, return_data_as='dataframe_list')
    return dcSubjectSummaryDFList

####################################
#                                  #
#         Layouts                  #
#                                  #
####################################

app = ui.page_fluid(
    ui.panel_title(ui.h2("CRDC Dashboard")),
    ui.layout_columns(
        ui.card(
            ui.card_header("File Summary"),
            dropdown_ui("fileCommonsSelect", "Data Commons Selections", []),
            output_widget("fileDataTypeGraphic"),
            output_widget("fileFormatGraphic"),
            output_widget('fileTypeGraphic'),
            output_widget('fileTumorNormalGraphic'),
            output_widget('fileAnatomicSiteGraphic')
        ),
        ui.card(
            ui.card_header('Subject Summary'),
            dropdown_ui("subjectCommonsSelect", "Data Commons Selections",[]),
            output_widget("subjectDataSources"),
            output_widget("subjectRace"),
            output_widget("subjectCauseOfDeath"),
            output_widget("subjectEthnicity"),
            output_widget("subjectSpecies")
        )
    )
)

####################################
#                                  #
#         Run Program              #
#                                  #
####################################

def server(input, output, session):
    #
    #         Startup File stuff
    #
    
    # summarize_files DFs
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
    
    # summarize_subjects DFs
    # 0 - Total subjects
    # 1 - Number of files
    # 2 - data_source (counts in "subjects")
    # 3 - race count_result
    # 4 - cause_of_death
    # 5 - ethnicity
    # 6 - species
    # 7 - year of death stats
    # 8 - year of birth stats

    
    #
    #   Initial Data call and dropdown setup
    #
    summary_file_list = dcSpecificFileSummary()
    temp_df = summary_file_list[2]
    templist = temp_df['data_source'].unique()
    dclist = []
    for item in templist:
        dclist.append(item.split(' ')[0])
    ui.update_select(
        "fileCommonsSelect",
        choices=dclist
    )
    ui.update_select(
        "subjectCommonsSelect",
        choices=dclist
    )
  
    
    
    
    
    ####################################
    #                                  #
    #        Data Update               #
    #                                  #
    ####################################

    @reactive.calc
    @reactive.event(input.fileCommonsSelect)
    def dcFileInfoList():
        dc_specific_file_list = dcSpecificFileSummary(input.fileCommonsSelect())
        return dc_specific_file_list
        
    @reactive.calc
    @reactive.event(input.subjectCommonsSelect)
    def dcSubjectInfoList():
        dc_specific_subject_list = dcSpecificSubjectSummary(input.subjectCommonsSelect())
        return dc_specific_subject_list
    
    
    
    ####################################
    #                                  #
    #       Update Drop downs          #
    #                                  #
    ####################################
    
    ####################################
    #                                  #
    #       Update graphics            #
    #                                  #
    ####################################
    @render_widget
    @reactive.event(input.fileCommonsSelect)
    def fileDataTypeGraphic():
        if dcFileInfoList() is not None:
            graphic_df = dcFileInfoList()[3]
            #start_df = dcFileInfoList()[3]['category'].value_counts()
            #graphic_df = pd.DataFrame({'name':start_df.index, 'count':start_df.values})
            fig = px.pie(
                graphic_df,
                values='count_result',
                names='category',
                title='File Data Type',
                hole=0.3
            )
            return fig
        
    @render_widget
    @reactive.event(input.fileCommonsSelect)
    def fileFormatGraphic():
        if dcFileInfoList() is not None:
            format_df = dcFileInfoList()[5]
            fig = px.pie(
                format_df,
                values= 'count_result',
                names= 'format',
                title='File Formats',
                hole=0.3
            )
            return fig
        
    @render_widget
    @reactive.event(input.fileCommonsSelect)
    def fileTypeGraphic():
        if dcFileInfoList() is not None:
            format_df = dcFileInfoList()[6]
            fig = px.pie(
                format_df,
                values= 'count_result',
                names= 'file_type',
                title='File Type',
                hole=0.3
            )
            return fig
        
        
    @render_widget
    @reactive.event(input.fileCommonsSelect)
    def fileTumorNormalGraphic():
        if dcFileInfoList() is not None:
            format_df = dcFileInfoList()[7]
            fig = px.pie(
                format_df,
                values= 'count_result',
                names= 'tumor_vs_normal',
                title='Tumor/Normal',
                hole=0.3
            )
            return fig
        
    @render_widget
    @reactive.event(input.fileCommonsSelect)
    def fileAnatomicSiteGraphic():
        if dcFileInfoList() is not None:
            format_df = dcFileInfoList()[8]
            fig = px.pie(
                format_df,
                values= 'count_result',
                names= 'anatomic_site',
                title='Anatomic Site',
                hole=0.3
            )
            return fig
        
###############  Subjects ##################
    @render_widget
    @reactive.event(input.subjectCommonsSelect)
    def subjectDataSources():
        if dcSubjectInfoList() is not None:
            format_df = dcSubjectInfoList()[2]
            fig = px.pie(
                format_df,
                values= 'subjects',
                names= 'data_source',
                title='Number of Subjects',
                hole=0.3
            )
            return fig

    @render_widget
    @reactive.event(input.subjectCommonsSelect)
    def subjectRace():
        if dcSubjectInfoList() is not None:
            format_df = dcSubjectInfoList()[3]
            fig = px.pie(
                format_df,
                values= 'count_result',
                names= 'race',
                title='Race',
                hole=0.3
            )
            return fig  

    @render_widget
    @reactive.event(input.subjectCommonsSelect)
    def subjectCauseOfDeath():
        if dcSubjectInfoList() is not None:
            format_df = dcSubjectInfoList()[4]
            fig = px.pie(
                format_df,
                values= 'count_result',
                names= 'cause_of_death',
                title='Cause of Death',
                hole=0.3
            )
            return fig
        
    @render_widget
    @reactive.event(input.subjectCommonsSelect)
    def subjectEthnicity():
        if dcSubjectInfoList() is not None:
            format_df = dcSubjectInfoList()[5]
            fig = px.pie(
                format_df,
                values= 'count_result',
                names= 'ethnicity',
                title='Ethnicity',
                hole=0.3
            )
            return fig

    @render_widget
    @reactive.event(input.subjectCommonsSelect)
    def subjectSpecies():
        if dcSubjectInfoList() is not None:
            format_df = dcSubjectInfoList()[6]
            fig = px.pie(
                format_df,
                values= 'count_result',
                names= 'race',
                title='Race',
                hole=0.3
            )
            return fig


    @render_widget
    @reactive.event(input.subjectCommonsSelect)
    def subjectRace():
        if dcSubjectInfoList() is not None:
            format_df = dcSubjectInfoList()[6]
            fig = px.pie(
                format_df,
                values= 'count_result',
                names= 'species',
                title='Species',
                hole=0.3
            )
            return fig
####################################
#                                  #
#         app command              #
#                                  #
####################################

# https://shiny.posit.co/py/get-started/create-run.html
app = App(app, server)