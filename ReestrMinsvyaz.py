import pandas as pd
import re
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class MinsvyazReestr:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.page_num = None
        self.xpath_data_dict = self.XPathDataDict()
        self.xpath_ctrls_dict = self.XPathCtrlsDict()
        self.data_columns = ['no', 'name', 'class', 'date']#, 'site']
        self.df = pd.DataFrame(columns=self.data_columns, index=[])
                        
                                
        
    def getDriver(self, page_num):
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url.format(page_num = page_num))
    
    def getIds(self):
        ids_list = []
        ids = self.driver.find_elements_by_xpath('//div[@class="line"]')
        for ii in ids:
            if len(re.findall(r'bx_\d+_\d+',ii.get_attribute('id'))) > 0:
                try:
                    ids_list.append(ii.get_attribute('id'))
                except:
                   None
        return ids_list
    
    def XPathDataDict(self):
        xpathdict = { 'no': '//div[@id="{i_d}"]/div[1]'
                    , 'name': '//div[@id="{i_d}"]/div[2]/a'
                    , 'class': '//div[@id="{i_d}"]/div[3]/span'
                    , 'date': '//div[@id="{i_d}"]/div[4]'
                    #, 'site': '//div[@id="{i_d}"]/div[5]/a'                    
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
    

    
    
    def getXPathData(self, xpath, i_d):
        try:
            return self.driver.find_element_by_xpath(xpath.format(i_d=i_d)).text
        except:
            return None
        
    
    def getAllData(self):
        for i_d in self.getIds():
            data = []
            for xpath in self.xpath_data_dict:
                data.append(self.getXPathData(xpath=self.xpath_data_dict[xpath], i_d=i_d))
                
            if any(data): #checks to see if the list data has all 'None' values
                self.df = self.df.append(pd.Series(data, index=self.data_columns), ignore_index=True)
    
    def clickButton (self,name):
        try:
            btn = self.driver.find_element_by_xpath(self.xpath_ctrls_dict.get(name))
            btn.click()
        except exceptions.NoSuchElementException:
            return 0
        except exceptions.ElementNotInteractableException:
            return 0
        else:
            return 1
                
                
    def getAllPagesData(self, perpage=100):
        if perpage not in ('20','40','100'):
            perpage='100'
        self.getDriver(page_num = 1)
        self.clickButton('selector')
        self.clickButton(perpage)
        self.getAllData()
        while self.clickButton('next_page'):	
            self.getAllData()
            #WebDriverWait(self.driver, delay)
        self.driver.close()

