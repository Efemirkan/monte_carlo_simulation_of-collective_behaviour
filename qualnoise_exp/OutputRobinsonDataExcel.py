from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

def OutputRobinsonDataExcel(outf,Ants,current_time,accepts,discovers,visits):
    # get Number of nests
    NumNests = visits.shape[0]

    wb = Workbook()
    ws = wb.active

    # generate the headings
    tst = []
    for i in range(NumNests):
        tst.append('time site ' + str(i) + ' discovered')
    for i in range(NumNests):
        tst.append('visits to site ' + str(i))
    tst.append('Path')
    tst = ['Ant','Threshold','final site','Selected','end time'] + tst

    # add column headings. NB. these must be strings
    ws.append(tst)

    # write the ant data
    for i, ant in enumerate(Ants):
         path = ant['path']
         # dat = [i,ant['thresh'],accepts[i],ant['selected'], current_time[i],discovers[:,i].T,visits[:,i].T,path]
         dat = [i,ant['thresh'],accepts[i],ant['selected'], current_time[i]]
         dat.extend(discovers[:,i].T)
         dat.extend(visits[:,i].T)
         dat.extend(path)
         ws.append(dat)

    wb.save(outf)
