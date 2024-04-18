import pyautogui
import time 

pyautogui.PAUSE = 2.5

# Abrir o Excel e o Brave
pyautogui.press("win") # abre o iniciar
pyautogui.typewrite("Bloco") # busca pelo bloco de notas
pyautogui.press("enter") # abre o bloco de notas 
pyautogui.doubleClick(x=1146, y=269) # maximiza o bloco de notas 
pyautogui.press("win") # abre o iniciar
pyautogui.typewrite("Brave") # pesquisa o navegador
pyautogui.press("enter") # abre o navegador

# Acessar a abrape.com.br/associados
pyautogui.typewrite("https://abrape.com.br/associados") # digita o site
pyautogui.press("enter") # acessa o site
# Clicar na página 2
pyautogui.click(x=906, y=826)


# Coordenadas dos associados
coordenadas = [
    (862, 331), (957, 332), (1051, 320), (1143, 327),
    (862, 387), (957, 387), (1051, 387), (1143, 387),
    (862, 449), (957, 449), (1051, 449), (1143, 449),
    (862, 525), (957, 525), (1051, 525), (1143, 525),
    (862, 581), (957, 581), (1051, 581), (1143, 581),
    (862, 645), (957, 645), (1151, 645), (1143, 645),
    (862, 712), (957, 712), (1151, 712), (1143, 712),
    (862, 775), (957, 775), (1151, 775), (1143, 775)
]

# Loop para extrair dados de cada associado
for i, (x, y) in enumerate(coordenadas, start=1):
    pyautogui.doubleClick(x= 1254, y=364) # maximixa a aba do site
    pyautogui.click(x=x, y=y) # clica no associado
    time.sleep(2)  # Espera um pouco para carregar os dados
    pyautogui.tripleClick(x=975, y=537)  # Clica na razão social do associado no popup
    time.sleep(1)  # Espera um pouco para o texto ser selecionado
    pyautogui.hotkey('ctrl', 'c')  # Copia o texto
    pyautogui.click(x=1332, y=1061)  # Acessa o bloco de notas
    pyautogui.hotkey('ctrl', 'v')  # Cola o texto
    pyautogui.press("backspace")  # Apaga as quebras de linha
    pyautogui.press("backspace")  # Apaga as quebras de linha
    pyautogui.typewrite(",")  # Adiciona a vírgula para separar as colunas 

    pyautogui.click(x=1261, y=1050) # volta para o navegador 
    pyautogui.tripleClick(x=973, y=548)  # Clica no nome do associado no popup
    pyautogui.hotkey('ctrl','c') # copia texto
    pyautogui.click(x=1332, y=1061)  # Acessa o bloco de notas
    pyautogui.hotkey('ctrl', 'v')  # Cola o texto
    pyautogui.press("backspace")  # Apaga as quebras de linha
    pyautogui.press("backspace")  # Apaga as quebras de linha
    pyautogui.typewrite(",")  # Adiciona a vírgula para separar as colunas 

    pyautogui.click(x=1261, y=1050) # volta para o navegador 
    pyautogui.tripleClick(x=973, y=558) # Clica no 1 telefone do associado 
    pyautogui.hotkey('ctrl','c') # copia texto
    pyautogui.click(x=1332, y=1061)  # Acessa o bloco de notas
    pyautogui.hotkey('ctrl', 'v')  # Cola o texto
    pyautogui.press("backspace")  # Apaga as quebras de linha
    pyautogui.press("backspace")  # Apaga as quebras de linha
    pyautogui.typewrite(",")  # Adiciona a vírgula para separar as colunas 

    pyautogui.click(x=1261, y=1050) # volta para o navegador 
    pyautogui.tripleClick(x=975, y=567) # Clica no 2 telefone do associado 
    pyautogui.hotkey('ctrl','c') # copia texto
    pyautogui.click(x=1332, y=1061)  # Acessa o bloco de notas
    pyautogui.hotkey('ctrl', 'v')  # Cola o texto
    pyautogui.press("backspace")  # Apaga as quebras de linha
    pyautogui.press("backspace")  # Apaga as quebras de linha
    pyautogui.typewrite(",")  # Adiciona a vírgula para separar as colunas 

    pyautogui.click(x=1261, y=1050) # volta para o navegador 
    pyautogui.rightClick(x=959, y=577) # clica com o direito no icone do email
    pyautogui.click(x=1068, y=290) #copia o email 
    pyautogui.click(x=1332, y=1061)  # Acessa o bloco de notas
    pyautogui.hotkey('ctrl', 'v')  # Cola o texto
    pyautogui.typewrite(",")  # Adiciona a vírgula para separar as colunas 
    pyautogui.press("enter")  # fechar o popup
    pyautogui.click(x=1261, y=1050) # volta para o navegador 

    pyautogui.press("esc")  # fechar o popup

# Salvando o arquivo
pyautogui.hotkey('ctrl', 's')  # Atalho para salvar
