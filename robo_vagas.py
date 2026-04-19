
import requests
from bs4 import BeautifulSoup
import json

def capturar_sdo():
    print("--- INICIANDO CAPTURA REAL ---")
    url = "https://sdo.co.mz/vagas/"
    vagas_lista = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Status: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procura por links que contenham a palavra 'vaga' no endereço
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            texto = link.get_text(strip=True)
            
            if 'vaga' in href.lower() and len(texto) > 10:
                vagas_lista.append({
                    "titulo": texto,
                    "empresa": "SDO Moçambique",
                    "provincia": "Moçambique",
                    "link": href if href.startswith('http') else f"https://sdo.co.mz{href}"
                })

        # Remove duplicados
        vagas_lista = [dict(t) for t in {tuple(d.items()) for d in vagas_lista}]

        if vagas_lista:
            with open('vagas.json', 'w', encoding='utf-8') as f:
                json.dump(vagas_lista, f, ensure_ascii=False, indent=4)
            print(f"SUCESSO: {len(vagas_lista)} vagas encontradas!")
        else:
            print("ERRO: Nenhuma vaga encontrada. O site pode ter bloqueado o robô.")

    except Exception as e:
        print(f"FALHA: {e}")

if __name__ == "__main__":
    capturar_sdo()
