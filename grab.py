import pandas as pd
from datetime import datetime
from ReestrMinsvyaz import MinsvyazReestr
			
start=datetime.now()
reestr = MinsvyazReestr ('https://reestr.minsvyaz.ru/reestr/')
reestr.getAllPagesData()
reestr.df.columns=['№', 'Название','Класс ПО','Дата внесения']
print (reestr.df)
with pd.ExcelWriter('reestr.xlsx') as writer:
    reestr.df.to_excel(writer,index=False)

print ('{} elapsed'.format(datetime.now()-start))
