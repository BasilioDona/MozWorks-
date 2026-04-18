import requests
from bs4 import BeautifulSoup
import json

def capturar_sdo():
    print("Buscando vagas na SDO Moçambique...")
    url = "https://sdo-mocambique.com/vagas-de-emprego/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    vagas_capturadas = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Na SDO, as vagas costumam estar em tags <h3> ou blocos de listagem
        links_vagas = soup.find_all('h3', limit=10)
        
        for item in links_vagas:
            a_tag = item.find('a')
            if a_tag:
                titulo = a_tag.get_text().strip()
                link = a_tag['href']
                
                vagas_capturadas.append({
                    "titulo": titulo,
                    "empresa": "SDO Moçambique",
                    "provincia": "Moçambique",
                    "link": link
                })
    except Exception as e:
        print(f"Erro ao acessar SDO: {e}")
    
    return vagas_capturadas

if __name__ == "__main__":
    lista_final = capturar_sdo()
    
    if lista_final:
        with open('vagas.json', 'w', encoding='utf-8') as f:
            json.dump(lista_final, f, indent=4, ensure_ascii=False)
        print(f"Sucesso! {len(lista_final)} vagas reais salvas.")
    else:
        print("Nenhuma vaga encontrada hoje.")
