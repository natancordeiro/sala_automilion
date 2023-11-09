from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from time import sleep
import schedule
import os

def main():
    LOGIN = 'SEU_LOGIN' # <-- SEU LOGIN AQUI
    SENHA = 'SUA_SENHA' # <-- SUA SENHA AQUI
    token = 'SEU BOT TOKEN' # <-- SEU BOT TOKEN AQUI 
    chat_id = 'ID DO SEU GRUPO OU SALA' # <-- SEU ID DA SALA AQUI
    def enviar_mensagem(mensagem):
        try:
            data = {"chat_id": chat_id, "text": mensagem}
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, data)
        except Exception as e:
            print("Erro ao enviar mensagem para o Telegram: ", e)

    def enviar_imagem(photo_path):
        try:
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            files = {"photo": open(photo_path, "rb")}
            data = {"chat_id": chat_id}
            requests.post(url, files=files, data=data)
        except Exception as e:
            print("Erro ao enviar imagem para o Telegram: ", e)

    iniciando_sessao = """⚠️ Iniciando sessão.. fiquem atentos 💰"""
    enviar_mensagem(iniciando_sessao)
    salvar_cache = os.getcwd()
    filename = os.getcwd() + "\\imagem_win.png"
    url = "https://fortunastake.com/"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-block')
    chrome_options.add_argument("no-default-browser-check")
    if os.path.exists(salvar_cache) == False:
        os.makedirs(salvar_cache)
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--user-data-dir=" + salvar_cache)

    driver = webdriver.Chrome()
    action = ActionChains(driver)

    driver.get(url)

    login_button = driver.find_element(By.XPATH, '//*[@id="__next"]/nav/div[2]/div[2]/button')
    if login_button.is_displayed():
        login_button.click()
        username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Usuário"]')))
        username_input.click()
        username_input.send_keys(LOGIN)
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Senha"]')
        password_input.click()
        password_input.send_keys(SENHA)
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()

    casino_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="casino-container"]/ul/li[2]')))
    sleep(1)
    casino_element.click()

    element2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="casino-container"]/div/div/div[2]')))
    sleep(1)
    action.move_to_element(element2)
    action.click(element2)
    action.perform()

    frame = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[2]/iframe')))
    driver.switch_to.frame(frame)
    sleep(10)
    video = driver.find_element(By.XPATH, '//*[@id="61801e1cffa74a472964b112"]/video')
    video.click()
    driver.switch_to.window(driver.window_handles[-1])

    elemento_numero = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "desktop-history-slot-1")))
    numero = elemento_numero.text
    while driver.find_element(By.ID, "desktop-history-slot-1").text == numero:
        pass
    numero_atual = driver.find_element(By.ID, "desktop-history-slot-1").text
    while driver.find_element(By.ID, "desktop-history-slot-1").text == numero_atual:
        pass
    numero_novo = int(driver.find_element(By.ID, "desktop-history-slot-1").text)

    # Verifica a qual grupo o número pertence
    if 1 <= numero_novo <= 12:
        entrada = "🔥 Entrada: Coluna 2 e Coluna 3"
        coluna = 1
    elif 13 <= numero_novo <= 24:
        entrada = "🔥 Entrada: Coluna 1 e Coluna 3"
        coluna = 2
    elif 25 <= numero_novo <= 34:
        entrada = "🔥 Entrada: Coluna 1 e Coluna 2"
        coluna = 3

    texto = f"""
    ✅ ENTRADA CONFIRMADA ✅

    🚨 Las Vegas Roullete
    🎯 PAGOU NO Nº {numero_novo}
    {entrada}
    🖥 PROTEGER NO ZERO
    """
    enviar_mensagem(texto)

    while driver.find_element(By.ID, "desktop-history-slot-1").text == str(numero_novo):
        pass
    numero = int(driver.find_element(By.ID, "desktop-history-slot-1").text)
    if 1 <= numero <= 12:
        coluna_nova = 1
    elif 13 <= numero <= 24:
        coluna_nova = 2
    elif 25 <= numero <= 34:
        coluna_nova = 3

    if coluna_nova != coluna:
        sleep(2)
        driver.get_screenshot_as_file(filename)
        resultado = "Win ✅"
    else:
        resultado = "Loss ❌"

    # ENVIAR IMAGEM #
    enviar_imagem(filename)
    enviar_mensagem(resultado)

    driver.quit()
    sleep(2)
    os.remove(filename)
    finalizando_sessao = """⚠️ Finalizando sessão...💰"""
    enviar_mensagem(finalizando_sessao)

schedule.every().day.at("10:00").do(main)
schedule.every().day.at("15:00").do(main)
schedule.every().day.at("20:00").do(main)

while True:
    schedule.run_pending()
    sleep(0.5)
