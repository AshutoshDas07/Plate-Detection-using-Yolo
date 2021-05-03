from selenium import webdriver
import os
import pandas as pd

os.environ["LANG"] = "en_US.UTF-8"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='/home/kmba/Documents/Python/Yash/chromedriver',options=chrome_options)
#webpage = "http://zipnet.in/index.php?page=stolen_vehicles_search&criteria=zoom" # edit me
page_source = []

webpage = "http://zipnet.in/index.php?page=stolen_vehicles_search&criteria=zoom&Page_No=1&state=008&state_name=DELHI&Start_Date=01/12/2020&End_Date=09/12/2020"

driver.get(webpage)
dfs = pd.read_html(webpage)
page = dfs[-6][0].to_string()
nos = page.split()
n = nos[-1]
license = []
for i in range(1,int(int(n)/3)):
    webpage = "http://zipnet.in/index.php?page=stolen_vehicles_search&criteria=zoom&Page_No="+ str(i) + "&state=008&state_name=DELHI&Start_Date=01/12/2020&End_Date=09/12/2020"

    driver.get(webpage)
    dfs = pd.read_html(webpage)
    for j in range (0,3):
        lic = dfs[-4+j][3].iloc[3]
        license.append(lic)
    #print(dfs[-4][3].iloc[3])
    #print(dfs[-3][3].iloc[3])
    #print(dfs[-2][3].iloc[3])
    
df = pd.DataFrame(license) 
df.to_csv('lic.csv',index = False)
