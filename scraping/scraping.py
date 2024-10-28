# Web Sracping do site https://consumidor.gov.br/pages/indicador/relatos/abrir
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

# Iniciando o driver
driver = webdriver.Chrome()  # Ou o navegador que você estiver usando
driver.get("https://consumidor.gov.br/pages/indicador/relatos/abrir")


# Controle de tempo para o execução da raspagem
tempo_maximo = 15 * 60  # 20 minutos
inicio = time.time()  # Marca o tempo de início

try:
    comentarios_validos = []  # Lista para armazenar comentários válidos
    titulos = []  # Lista para armazenar títulos
    while True:
        # Verifica se o tempo máximo foi alcançado
        if time.time() - inicio > tempo_maximo:
            print("Tempo máximo de coleta alcançado.")
            break  # Sai do loop se 10 minutos se passaram

        # Coleta os textos dos comentários
        comentarios = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
        )

        # Coleta os títulos das empresas usando a tag <h3> sem intervalos
        novos_titulos = driver.find_elements(By.TAG_NAME, "h3")
        titulos.extend([titulo.text.strip() for titulo in novos_titulos])  # Adiciona todos os títulos

        # Adiciona comentários válidos à lista
        for i in range(len(comentarios)):
            if i >= 3 and (i - 3) % 4 == 0:  # Mantém os índices relevantes (3, 7, 11, ...)
                comentario = comentarios[i].text.strip()
                comentarios_validos.append(comentario)

        # Espera até que o botão de carregar mais comentários esteja presente
        try:
            load_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.ID, "btn-mais-resultados"))
            )
            load_more_button.click()
            time.sleep(1)  # Espera um pouco para carregar mais comentários
        except Exception as e:
            print("Erro ao clicar no botão ou não há mais comentários:", e)
            break  # Sai do loop se não houver mais comentários

except Exception as e:
    print("Erro ao coletar dados:", e)

# Cria DF
df_comentarios = pd.DataFrame({
    'Empresa': titulos,
    'Texto': comentarios_validos
})

# Como existem duplicadas nesse dataset, 
df_comentarios.to_csv('/Projetos Pessoais/DataScience/PLN_Text_Analysis/data/dados_brutos.csv',
                       sep =',', index = False, encoding = 'utf-8')
