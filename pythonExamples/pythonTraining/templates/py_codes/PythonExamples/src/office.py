import win32com.client

answer = raw_input("Do you want to create a new (W)ord, (E)xcel or (P)owerPoint document? (W/E/P)")

if answer == "W":
    word = win32com.client.Dispatch("Word.Application")
    word.visible = True
    doc = word.Documents.Add()
    doc.Content.Text = "Hello Python and have a nice day!"
elif answer == "E":
    excel = win32com.client.Dispatch("Excel.Application")
    #excel.visible = True
    excel.Workbooks.Add()
    excel.Range("A1").Value = "Hello Python and Excel!"
elif answer == "P":
    pp = win32com.client.Dispatch("PowerPoint.Application")
    pp.visible = True
    presentation = doc = pp.Presentations.Add()
    slide = presentation.Slides.Add(1,12) # 12 is the code for empty silde
    label = slide.Shapes.AddLabel(1, 100, 100, 150, 150)
    label.TextFrame.TextRange.Text="Hello Python and PowerPoint!"
else:
    print "No such option!"

