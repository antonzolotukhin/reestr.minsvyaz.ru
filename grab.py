import pandas as pd
from datetime import datetime
from ReestrMinsvyaz import MinsvyazReestr
start=datetime.now()			
reestr = MinsvyazReestr ('https://reestr.minsvyaz.ru/reestr/?PAGEN_1={page_num}&show_count={perpage}')
reestr.getAllPagesData()
reestr.df.columns=['рег. №', 'Название','Класс ПО','Дата внесения','Сайт']
print (reestr.df)
with pd.ExcelWriter('reestr.xlsx', engine='xlsxwriter') as writer:
    reestr.df.to_excel(writer,sheet_name='Реестр ПО',index=False)
    worksheet=writer.sheets['Реестр ПО']
    worksheet.set_column('A:A', 3)
    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 14)
    worksheet.set_column('A:A', 12)
    worksheet.autofilter('C1:C{}'.format(len(reestr.df.index) + 1))
    writer.save()
    writer.close()
print ('{} elapsed'.format(datetime.now()-start))
