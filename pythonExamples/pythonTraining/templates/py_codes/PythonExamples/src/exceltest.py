# coding: iso-8859-1
import win32com.client 
from win32com.client import constants
#import pythoncom

def luoWorkbook(data, filename=None):
    #excel = win32com.client.Dispatch("Excel.Application")
    # ilman makepy ajamista constants ei toimi, varmistetaan
    # asia käynnistämällä Excel hieman toisin..
    excel = win32com.client.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = True
    if filename != None:
        wb=excel.Workbooks.Open(filename)
    else:
        wb = excel.Workbooks.Add()
    sheet = wb.Sheets(1)
    sheet.Name="Data"
    for i, val in enumerate(data):
        solu=sheet.Cells(i+2,1)
        solu.Value=i
        solu=sheet.Cells(i+2,2)
        solu.Value=val
        solu=sheet.Cells(i+2,3)
        solu.Value= val*i
    return wb

def luoKaavio(wb, arvoja):
    chart = wb.Charts.Add()
    chart.ChartType = constants.xlXYScatterSmooth
    chart.Name = "Testi"     
    series1 = chart.SeriesCollection().NewSeries()
    series2 = chart.SeriesCollection().NewSeries()
    xalue = "A2:A" + str(arvoja+1)
    arvoalue1 = "B2:B" + str(arvoja+1)
    arvoalue2 = "C2:C" + str(arvoja+1)
    sheet = wb.Sheets("Data")
    series1.XValues = sheet.Range(xalue)
    series2.XValues = sheet.Range(xalue)
    series1.Values = sheet.Range(arvoalue1)
    series2.Values = sheet.Range(arvoalue2)
    series1.Name = "Data"
    series2.Name = "Kertaa"
    xAxis = chart.Axes()[0]
    yAxis = chart.Axes()[1]
    xAxis.HasMajorGridlines = True
    yAxis.HasMajorGridlines = True
    chart.HasTitle = True
    chart.ChartTitle.Characters.Text ="Otsikko"



data = list()
print "Anna arvoja, ei arvoa lopettaa"
while True:
    syote = raw_input("Luku: ")
    if syote == '':
        break
    data.append(int(syote))

wb = luoWorkbook(data)
luoKaavio(wb, len(data))

