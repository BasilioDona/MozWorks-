import requests
from bs4 import BeautifulSoup
import json

def capturar():
    url = "https://www.emprego.co.mz/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    vagas = []

    try:
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Procura por links de vagas (ajustado para emprego.co.mz)
        for a in soup.find_all('a', href=True):
            texto = a.get_text(strip=True)
            if len(texto) > 15 and ('vaga' in a['href'] or 'emprego' in a['href']):
                vagas.append({
                    "titulo": texto,
                    "empresa": "Anúncio Recente",
                    "provincia": "Moçambique",
                    "link": a['href'] if a['href'].startswith('http') else f"https://www.emprego.co.mz{a['href']}"
                })

        if not vagas:
            vagas = [{"titulo": "Teste de Escrita", "empresa": "MozWorks", "provincia": "Maputo", "link": url}]

        with open('vagas.json', 'w', encoding='utf-8') as f:
            json.dump(vagas, f, ensure_ascii=False, indent=4)
        print("Ficheiro guardado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    capturar()
