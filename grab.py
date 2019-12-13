from ReestrMinsvyaz import MinsvyazReestr
			
reestr = MinsvyazReestr ('https://reestr.minsvyaz.ru/reestr/?PAGEN_1={page_num}&show_count=100')
reestr.getAllPagesData(max_page=61)
with pd.ExcelWriter('reestr.xlsx') as writer:
    reestr.df.to_excel(writer)

