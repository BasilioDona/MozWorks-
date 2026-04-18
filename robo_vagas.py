import requests
from bs4 import BeautifulSoup
import json

def capturar_vagas_sdo():
    print("Iniciando captura de vagas reais...")
    url = "https://sdo-mocambique.com/vagas/" # Link oficial da SDO
    vagas_reais = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # O robô procura os blocos de vaga no site da SDO
        vagas_html = soup.find_all('div', class_='job-list-content') 

        for item in vagas_html:
            titulo = item.find('h3').get_text(strip=True)
            link = item.find('a')['href']
            
            vagas_reais.append({
                "titulo": titulo,
                "empresa": "SDO Moçambique",
                "provincia": "Moçambique",
                "link": link
            })
        
        if not vagas_reais:
            print("Aviso: Nenhuma vaga encontrada. Verificando estrutura...")
            
    except Exception as e:
        print(f"Erro ao capturar: {e}")
    
    # Se falhar, mantém as de teste para o site não quebrar
    if len(vagas_reais) > 0:
        with open('vagas.json', 'w', encoding='utf-8') as f:
            json.dump(vagas_reais, f, ensure_ascii=False, indent=4)
        print(f"Sucesso! {len(vagas_reais)} vagas capturadas.")
    else:
        print("Usando dados de reserva.")

if __name__ == "__main__":
    capturar_vagas_sdo()
