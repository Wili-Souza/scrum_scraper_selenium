from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time


#  ---- Minhas funções e classes
from conversaoData import converterData
from search import searchScrum
from exportar import exportar_df
from numberOfPage import pageNumber

data = { # -> diciionário para data frame 
    'tipo': [],
    'titulo': [],
    'link': [],
    'data': [],
    'descricao': []
}

#intervalo de págs que deseja raspar
firstPage = 1
lastPage = 45

#buscar/filtrar:
nome = ''
tag = 'All Tags'
tipo = 'All Types'

        # --- usando Selenium 

#Indicando o driver -> no caso do chrome, baixar e deixar no mesmo diretório
option = Options()
option.headless = True #Para n mostrar o precoesso -> causa lentidão
chrome = webdriver.Chrome('chromedriver.exe', options=option)

#pegando a pág a partir do selenium
chrome.get('https://www.scrum.org/resources')

#As funções de espera evitam bugs pela lentidão do carregamento
def esperar_posts(chrome):
    return chrome.find_elements_by_class_name('list-view-item')

def esperar_tipo(chrome):
    return post.find_element_by_class_name('list-view-item-type')

        # --- preenchendo formulário de pesquisa e filtro
search_link = ''

search_field = chrome.find_element_by_name('search') #Campo de pesquisa
search_field.send_keys(nome) #Pesquisando 

select_tag_field = Select(chrome.find_element_by_name('field_resource_tags_target_id'))
select_tag_field.select_by_visible_text(tag)

select_type_field = Select(chrome.find_element_by_name('type'))
select_type_field.select_by_visible_text(tipo)

wait = WebDriverWait(chrome, 5) #espera até 5 segundos -> auxiliar para wait.until

button_apply = wait.until(EC.element_to_be_clickable((By.ID, 'edit-submit-resources')))
chrome.execute_script("arguments[0].click();", button_apply)

#Espera 5 segundos para garantir que todas as informações tenham carregado
time.sleep(5)

        # --- Indo para a primeira página selecionada

#Encontrando o numero máximo de páginas (encontradas)
pager_item_last = chrome.find_element_by_xpath("//a[@title='Go to last page']")
link_last_page = pager_item_last.get_attribute('href')
maxPages = pageNumber(link_last_page)

firstPage -= 1 #O indice da pág é diferente do número
if firstPage > maxPages: #N ultrapassa o numero de páginas encontradas
    firstPage = maxPages

found = False

while not found:
    try:
        xpath_name = "//a[@title='Go to page {}']" .format(firstPage + 1)
        firstPage_icon = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_name)))
        found = True

        #Alternativa para .click() caso -> is not clickable at point...
        chrome.execute_script("arguments[0].click();", firstPage_icon)
        time.sleep(5) #tempo para carregamento da página

    except:
        xpath_name = "//a[@title='Go to next page']"
        next_icon = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_name)))
        chrome.execute_script("arguments[0].click();", next_icon)


        # --- Carregando os posts de todas as páginas selecionadas

for i in range(firstPage, lastPage):
    print(f'aeo {i} --------------- ')
    posts = WebDriverWait(chrome, 5).until(esperar_posts)

    for post in posts:
            #Recebendo tipo
        try:
            tipo_post = post.find_element_by_class_name('list-view-item-type').text.strip()
            print(tipo_post)
        except:
            tipo_post = '' #Tratamento

            #recebendo tag titulo
        try:
            titulo_post_tag = post.find_element_by_class_name('list-view-item-title')
            titulo_post = titulo_post_tag.text.strip()
        except:
            titulo_post = ''

            #recebendo link pelo tag titulo
        href = titulo_post_tag.get_attribute('href')
        if href == None:
            link_post = ''
        else:
            link_post = href

            #recebendo data
        try:
            data_post = post.find_element_by_class_name('list-view-item-date')
            data_post = converterData(data_post.text)
        except:
            data_post = ''

            #recebendo descrição / teaser
        try:
            descricao_post = post.find_element_by_class_name('list-view-item-teaser').text.strip()
        except:
            descricao_post = ''
        
        #Salvando no dicionario do dataframe
        data['tipo'].append(tipo_post)
        data['titulo'].append(titulo_post)
        data['link'].append(link_post)
        data['data'].append(data_post)
        data['descricao'].append(descricao_post)

            #Mudando página 

    #conferindo se a próxima página existe ou se essa foi a última
    if i + 1 > maxPages or i + 1 >= lastPage:
        break

    #Passando para a próxima
    xpath_name = "//a[@title='Go to next page']"
    next_icon = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_name)))
    chrome.execute_script("arguments[0].click();", next_icon)
    time.sleep(3) #Tempo para carregamento


if len(data['titulo']) > 0: #se algum resultado for capturado

        # ---- Salvando resultado
    df = pd.DataFrame(data, columns = ['tipo', 'titulo', 'link', 'data', 'descricao']) #-> criando dataframe

        # ---- Exportando para excel(xlsx) e/ou csv
    exportar_df(df, 'xlsx', 'csv')


print('FIM DA EXECUÇÃO')