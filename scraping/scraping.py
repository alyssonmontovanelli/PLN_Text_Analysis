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
    while True:
        # Verifica se o tempo máximo foi alcançado
        if time.time() - inicio > tempo_maximo:
            print("Tempo máximo de coleta alcançado.")
            break  # Sai do loop quando tempo finalizar
        try:
            load_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.ID, "btn-mais-resultados"))
            )
            load_more_button.click()
            time.sleep(3)  # Espera um pouco para carregar mais comentários
        except Exception as e:
            print("Erro ao clicar no botão ou não há mais comentários:", e)
            break  # Sai do loop se não houver mais comentários

except Exception as e:
    print("Erro ao coletar dados:", e)


# Extraindo comentarios
comentarios = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
        )

comentarios_validos = []
for contador in range(len(comentarios)):
 if contador >= 3 and (contador - 3) % 4 == 0:
  comentarios_validos.append(comentarios[contador].text)
print(len(comentarios_validos))

# Extraido nomes das empresas
titulo_teste = driver.find_elements(By.TAG_NAME , "h3")
titulo_valido = [titulo.text for titulo in titulo_teste]

# Criação de Dicionário para DF
dict_consumidor = {
 'Empresa': titulo_valido,
 'Relato': comentarios_validos
}

df = pd.DataFrame(dict_consumidor)

print(df.shape)

# Como existem duplicadas nesse dataset, 
df.to_csv('/Projetos Pessoais/DataScience/PLN_Text_Analysis/data/dados_brutos_2.csv',
                       sep =',', index = False, encoding = 'utf-8')
