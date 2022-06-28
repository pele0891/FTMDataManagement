import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.chart import BarChart, Reference

import win32com.client as win32
from pathlib import Path

def createGraph(dataFile: str, sheetName: str):
    win32c = win32.constants

    # path to your file
    f_path = Path.cwd()
    # your excel file name
    f_name = dataFile
    filename = f_path / f_name
    # create excel object
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    # excel can be visible or not
    excel.Visible = True  # False
    wb = excel.Workbooks.Open(filename)

    chart = wb.Sheets(sheetName).Shapes.AddChart2(-1, 76, True)
    chart.Chart.SetSourceData(Source= wb.Sheets(sheetName).UsedRange)
    #add a stack area graph chart with usedRange of data provided

    chart.Chart.HasTitle = True
    chart.Chart.ChartTitle.Text = "Sum of FTE per project"
    chart.Chart.HasLegend = True
    #add title and legend.
