import requests
from bs4 import BeautifulSoup
import json

def capturar_vagas_sdo():
    print("--- INICIANDO CAPTURA NO SITE NOVO (sdo.co.mz) ---")
    url = "https://sdo.co.mz/vagas/"
    vagas_lista = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Conexão: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procura pelos links de vagas que o site da SDO usa
        # Geralmente dentro de tags h2 ou h3 com links
        vagas_html = soup.find_all(['h2', 'h3']) 

        for item in vagas_html:
            link_tag = item.find('a')
            if link_tag and 'vaga' in link_tag['href'].lower():
                titulo = link_tag.get_text(strip=True)
                link_vaga = link_tag['href']
                
                # Se o link for relativo, adiciona o domínio
                if not link_vaga.startswith('http'):
                    link_vaga = "https://sdo.co.mz" + link_vaga

                vagas_lista.append({
                    "titulo": titulo,
                    "empresa": "SDO Moçambique",
                    "provincia": "Moçambique",
                    "link": link_vaga
                })
        
        if len(vagas_lista) > 0:
            # Salva apenas se encontrar vagas reais
            with open('vagas.json', 'w', encoding='utf-8') as f:
                json.dump(vagas_lista, f, ensure_ascii=False, indent=4)
            print(f"SUCESSO: {len(vagas_lista)} vagas reais encontradas e salvas!")
        else:
            print("AVISO: Nenhuma vaga encontrada com os seletores atuais.")

    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    capturar_vagas_sdo()
