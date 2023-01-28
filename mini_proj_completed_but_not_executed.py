from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager#sometimes chrome keeps updating so once i ran into error as chrome version was 110 but my chrome driver version was 96 so selenium couldnt work,so to manage all upgrades we use this module
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from PyPDF2 import PdfMerger
import time
import os
import pyautogui as pg
s_pdf_name=[[],[],[],[],[]]
n_pdf_name=[[],[],[],[],[]]
prn=input('enter prn')
pw=input('enter password')
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.pesuacademy.com/Academy/s/studentProfilePESU")

username_entry = driver.find_element(By.NAME, "j_username")
username_entry.clear()
username_entry.send_keys(prn)
password_entry = driver.find_element(By.NAME, "j_password")
password_entry.clear()
password_entry.send_keys(pw)
password_entry.send_keys(Keys.RETURN)
time.sleep(4)

my_courses_b=driver.find_element(By.LINK_TEXT,"My Courses")
my_courses_b.click()
time.sleep(5)

my_courses_name_obj=driver.find_elements(By.XPATH,"//tr/td")
my_courses_name=[i.text for i in my_courses_name_obj]
my_courses_name_tuple_lis=[my_courses_name[i:i+5] for i in range(0,len(my_courses_name),5)]

my_courses_table=driver.find_elements(By.TAG_NAME,"tr")

t=len(my_courses_table)

for i1 in range(1,len(my_courses_table)):
    my_courses_table[i1].click()
    course_name=my_courses_name_tuple_lis[i1-1][1]
    time.sleep(10)#try to put a condition where only if all elements loaded it searches for it,http loaded
    unit_and_non_unit_li_obj=driver.find_elements(By.XPATH,"//ul/li")
    if unit_and_non_unit_li_obj=='' or unit_and_non_unit_li_obj==None:
        continue
    units=unit_and_non_unit_li_obj[-15:-10:]
    for j in range(len(units)):
        unit_name=units[j].text
        units[j].click()#put implicit wait conditions above code worked ,that is unit_and_non_unit_li will give output if u put appropriate wait condition
        time.sleep(5)
        classes=driver.find_elements(By.TAG_NAME,"tr")
        time.sleep(5)
        t1=driver.find_elements(By.CSS_SELECTOR,"span.short-title")
        names=[i.text for i in t1]
        for k in range(1,len(classes)):
            class_name=names[k-1]#k-1
            classes[k].click()#
            time.sleep(5)
            slides_tab=driver.find_element(By.LINK_TEXT,"Slides")
            notes_tab=driver.find_element(By.LINK_TEXT,"Notes")
            slides_tab.click()
            time.sleep(3)
            slides_obj=driver.find_elements(By.TAG_NAME,"iframe")
            slides_link=[i.get_attribute("src") for i in slides_obj]
            ex=1
            for i in slides_link:
                if i=='' or i==None:
                    continue
                link=i[:i.index('#'):]
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                name=class_name+'s'+str(ex)+'.pdf'
                time.sleep(10)
                driver.implicitly_wait(10)
                x, y = pg.locateCenterOnScreen('download_b1.png',confidence=0.9)
                pg.click(x, y)
                time.sleep(5)
                pg.write(name)
                time.sleep(5)
                pg.press('enter')
                time.sleep(5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                ex+=1
                s=r'C:\Users\rohit\Downloads'
                s+='\\'+name
                s_pdf_name[j].append(s)#k-1
            notes_tab.click()
            time.sleep(9)
            notes_obj=driver.find_elements(By.TAG_NAME,"iframe")
            notes_link=[i.get_attribute("src") for i in notes_obj]
            xe=1
            for j in notes_link:
                if j=='' or j==None:
                    continue
                link=j[:j.index('#'):]
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                name=class_name+'n'+str(xe)+'.pdf'
                time.sleep(10)
                driver.implicitly_wait(10)
                x, y = pg.locateCenterOnScreen('download_b1.png',confidence=0.9)
                pg.click(x, y)
                time.sleep(5)
                pg.write(name)
                time.sleep(5)
                pg.press('enter')
                time.sleep(5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                xe+=1
                s=r'C:\Users\rohit\Downloads'
                s+='\\'+name
                n_pdf_name[j].append(s)#k-1
            time.sleep(5)
            back=driver.find_element(By.PARTIAL_LINK_TEXT,my_courses_name[1]) #k
            back.click()

        time.sleep(10)
        unit_and_non_unit_li_obj=driver.find_elements(By.XPATH,"//ul/li")
        units=unit_and_non_unit_li_obj[-15:-10:]
        units[j].click()

    time.sleep(5)
    my_courses_b.click()

time.sleep(5)

time.sleep(5)
driver.close()

def merge_units(name1,l):
    ss,x="Unit",1
    for slides in name1:
        combination = PdfMerger()
        for slide in slides:
            combination.append(slide)
            os.remove(slide)
        combination.write(ss+str(x)+l+".pdf")
        combination.close()
        x+=1
def merge_all(name2,l):
    l=[i for i in name2 for j in i]
    combination = PdfMerger()
    for slide in l:
        combination.append(slide)
        os.remove(slide)
    combination.write("unit12345"+l+".pdf")
    combination.close()
merge_units(s_pdf_name,"s")
merge_units(n_pdf_name,"n")
merge_all(s_pdf_name,"s")
merge_all(n_pdf_name,"n")