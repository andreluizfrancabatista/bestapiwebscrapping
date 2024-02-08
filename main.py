## main.py
import sys

# Configuração do Web-Driver

# Utilizando o WebDriver do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Instanciando o Objeto ChromeOptions
options = webdriver.ChromeOptions()

# Passando algumas opções para esse ChromeOptions
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-crash-reporter')
options.add_argument('--log-level=3')


# Criação do WebDriver do Chrome
# wd_Chrome = webdriver.Chrome('chromedriver',options=options)
# Criação do WebDriver do Chrome
wd_Chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Importando as Bibliotecas

import pandas as pd
import time
from tqdm import tqdm
from selenium.webdriver.common.by import By

"""# Iniciando a Raspagem de Dados"""
link = 'https://pt.betsapi.com/le/33440/Esoccer-Adriatic-League--10-mins-play/p.'
#link = 'https://pt.betsapi.com/le/23114/Esoccer-GT-Leagues-%E2%80%93-12-mins-play/p.'
#link = 'https://pt.betsapi.com/le/22614/Esoccer-Battle--8-mins-play/p.'

# Liga
League = 'Adriatic_League'
#League = 'GT_Leagues'
#League = 'ESoccer_Battle'

# Quantidade de páginas
pages = 20

# Criar o dicionário vazio
jogo = {
    'Date':[],'Time':[], 'Shift':[], 'League':[],'HomeTeam':[], 'HomePlayer': [],
    'AwayTeam':[], 'AwayPlayer':[],'golsHome':[], 'golsAway':[], 'FTR':[]
}

# Lista de links
for i in tqdm(range(1, pages+1)):
    # Com o WebDrive a gente consegue a pedir a página (URL)
    wd_Chrome.get(f'{link}{i}')
    time.sleep(3)

    # Para pegar todas as linhas (tr) da tabela
    linhas = wd_Chrome.find_elements(By.CSS_SELECTOR, 'tbody > tr')
    for linha in linhas:
        try:
            Date = linha.find_element(By.CSS_SELECTOR,'td.dt_n').text.split(' ')[0]
            Time = linha.find_element(By.CSS_SELECTOR,'td.dt_n').text.split(' ')[1]
            Hora = int(Time.split(':')[0]) 
            Home = linha.find_element(By.CSS_SELECTOR,'td:nth-child(3)').text.split(' v ')[0]
            Away = linha.find_element(By.CSS_SELECTOR,'td:nth-child(3)').text.split(' v ')[1]
            HomeTeam = Home.split(' (')[0]
            AwayTeam = Away.split(' (')[0]
            HomePlayer = Home.split(' (')[1].split(')')[0]
            AwayPlayer = Away.split(' (')[1].split(')')[0]
            golsHome = linha.find_element(By.CSS_SELECTOR,'td:nth-child(4)').text.split('-')[0]
            golsAway = linha.find_element(By.CSS_SELECTOR,'td:nth-child(4)').text.split('-')[1]
            # Colocar tudo dentro do df pra salvar no csv
            jogo['Date'].append(Date)
            jogo['Time'].append(Time)
            if(Hora>=18):
                jogo['Shift'].append('Noite')
            elif(Hora>=12):
                jogo['Shift'].append('Tarde')
            elif(Hora>=6):
                jogo['Shift'].append('Manhã')
            else:
                jogo['Shift'].append('Madrugada')
            jogo['League'].append(League)
            jogo['HomeTeam'].append(HomeTeam)
            jogo['HomePlayer'].append(HomePlayer)
            jogo['AwayTeam'].append(AwayTeam)
            jogo['AwayPlayer'].append(AwayPlayer)
            jogo['golsHome'].append(golsHome)
            jogo['golsAway'].append(golsAway)
            if(golsHome > golsAway):
                jogo['FTR'].append('H')
            elif(golsHome < golsAway):
                jogo['FTR'].append('A')
            else:
                jogo['FTR'].append('D')
        except Exception as error:
            print(f'Exception: {error}\n')
            pass
        # print(f'Date: {Date} - Time: {Time} - HomeTeam: {HomeTeam} ({HomePlayer})- AwayTeam: {AwayTeam} ({AwayPlayer}) - Placar: {golsHome}x{golsAway}')

# Salvar no  csv
df = pd.DataFrame(jogo)
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(['Nº'])
df = df.rename(index=lambda x: x + 1)
filename = f'{League}_resultados.csv'
df.to_csv(filename, sep=";")