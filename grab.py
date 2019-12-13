import pandas as pd
from ReestrMinsvyaz import MinsvyazReestr
			
reestr = MinsvyazReestr ('https://reestr.minsvyaz.ru/reestr/')
reestr.getAllPagesData()
with pd.ExcelWriter('reestr.xlsx') as writer:
    reestr.df.to_excel(writer)

