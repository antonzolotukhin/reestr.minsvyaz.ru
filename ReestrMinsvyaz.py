import pandas as pd
import re
from lxml import etree

try:
    # Python 2
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

class MinsvyazReestr:
    def __init__(self, url):
        self.url = url
        self.tree = None
        self.page_num = None
        self.xpath_data_dict = self.XPathDataDict()
        self.xpath_ctrls_dict = self.XPathCtrlsDict()
        self.data_columns = ['no', 'name', 'class', 'date', 'site']
        self.df = pd.DataFrame(columns=self.data_columns, index=[])
                                
    def getTree(self, page_num,perpage):
        url=self.url.format(page_num = page_num,perpage = perpage)
        print ('fetching\t' + url)
        response = urlopen(url)
        htmlparser = etree.HTMLParser()
        self.tree = etree.parse(response, htmlparser)
   
    def getRows(self):
        return self.tree.xpath('//div[@class="line"]')
    
    def XPathDataDict(self):
        xpathdict = { 'no': 'div[@class="num"]/text()'
                    , 'name': 'div[@class="name"]/a/text()'
                    , 'class': 'div[@class="class"]'
                    , 'date': 'div[@class="date"]/text()'
                    , 'site': 'div[@class="status"]/a'                    
                    }
        return xpathdict
		
    def XPathCtrlsDict(self):
        xpathdict = { 'next_page': '//a[contains(text(), ">")]'
                    , 'selector': '//div[@class="select_area"]'
                    , '20': '//ul[@class="select2-results__options"]/li[contains(text(), "20")]'
                    , '40': '//ul[@class="select2-results__options"]/li[contains(text(), "40")]'
                    , '100': '//ul[@class="select2-results__options"]/li[contains(text(), "100")]'
                    }
        return xpathdict    
    
    def getXPathData(self, row, xpath):
        data=[]
        for elmnt in row.xpath(xpath):
            if isinstance(elmnt, str):
                content = elmnt
                href = None
            else:
                content = ''.join(elmnt.itertext())
                href = elmnt.attrib.get('href')
            content=re.sub(r'\s+', ' ', content.strip())
            data.append(content)
        content = '\n'.join(data)
        if content.isdigit():
            content = int(content)
        if href != None:
            content = '=HYPERLINK("{href}", "{text}")'.format(href=href,text=re.sub(r'"','""',content))
        return content
            
    def getAllData(self):
        parsed_count=0
        for row in self.getRows():
            data = []
            for xpath in self.xpath_data_dict:
                data.append(self.getXPathData(row=row, xpath=self.xpath_data_dict[xpath]))
            if any(data): #checks to see if the list data has all 'None' values
                self.df = self.df.append(pd.Series(data, index=self.data_columns), ignore_index=True)
                parsed_count+=1
        print('\t\t{} rows parsed.'.format(parsed_count))

    def isElementExists (self,name):
            return (len(self.tree.xpath(self.xpath_ctrls_dict.get(name))) > 0)

    def getAllPagesData(self, perpage=100):
        print ('Process started.')
        if perpage not in ('20','40','100'):
            perpage='100'
        page_num=1
        self.getTree(page_num,perpage)
        self.getAllData()
        while self.isElementExists('next_page'):
            page_num+=1
            self.getTree(page_num,perpage)
            self.getAllData()
        print ('Done!')
        

