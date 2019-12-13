import pandas as pd
from ReestrMinsvyaz import MinsvyazReestr
			
reestr = MinsvyazReestr ('https://reestr.minsvyaz.ru/reestr/?PAGEN_1=59')
reestr.getAllPagesData()
reestr.df.columns=['№', 'Название','Класс ПО','Дата внесения']
with pd.ExcelWriter('reestr.xlsx') as writer:
    reestr.df.to_excel(writer,index=False)

