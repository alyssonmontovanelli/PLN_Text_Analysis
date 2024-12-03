# Web Sracping do site https://consumidor.gov.br/pages/indicador/relatos/abrir
import os
import json
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
tempo_maximo = 120 * 60  # 2 horas
inicio = time.time()  # Marca o tempo de início

try:
    while True:
        # Verifica se o tempo máximo foi alcançado
        if time.time() - inicio > tempo_maximo:
            print("Tempo máximo de coleta alcançado.")
            break  # Sai do loop quando tempo finalizar
        try:
            load_more_button = WebDriverWait(driver, 3).until(
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


# Pegando comenta´rios e notas e colocando-os em listas 
comentarios_validos = []
nota_resposta = []

for contador in range(len(comentarios)):
 if contador >= 3 and (contador - 3) % 4 == 0:
  comentarios_validos.append(comentarios[contador].text)
 
 elif contador >= 5 and (contador - 5) % 4 == 0:
  nota_resposta.append(comentarios[contador].text)
print(len(comentarios_validos))

# Extraindo até onde foi o scraping
contador_num = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "contador")))
# print("abaixo estão nota resposta")
# print(nota_resposta)

# Extraido nomes das empresas
titulo_teste = driver.find_elements(By.TAG_NAME , "h3")
titulo_valido = [titulo.text for titulo in titulo_teste]

# Criação de Dicionário para DF
dict_consumidor = {
 'Empresa': titulo_valido,
 'Relato': comentarios_validos,
 'Avaliacao': nota_resposta
}

# Apenas para garantir que ao final do scrapping, os dados serão salvos, mesmo se der
# inconsistência no DF produzido pelo dict_consumidor
dict_empresa = {
   'Empresa': titulo_valido
}
dict_relato = {
   'Relato': comentarios_validos
}
dict_avaliacao = {
   'Avaliacao': nota_resposta
}

with open('dict_empresa.json', 'w', encoding='utf-8') as json_file:
    json.dump(dict_empresa, json_file, ensure_ascii=False)

with open('dict_relato.json', 'w', encoding='utf-8') as json_file:
    json.dump(dict_relato, json_file, ensure_ascii=False)

with open('dict_avaliacao.json', 'w', encoding='utf-8') as json_file:
    json.dump(dict_avaliacao, json_file, ensure_ascii=False)

print(f"Data Final - {contador_num}")



try:
   df = pd.DataFrame(dict_consumidor)
except Exception as e:
   print("Não foi possível criar o DF, por causa do: ", e)
   

print(contador_num)
print(df.shape)

# Como existem duplicadas nesse dataset, 
df.to_csv('/Projetos Pessoais/DataScience/PLN_Text_Analysis/data/data_scraping_bruto_2hr.csv',
                       sep =',', index = False, encoding = 'utf-8')
