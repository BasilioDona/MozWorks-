import requests
from bs4 import BeautifulSoup
import json

def capturar_vagas_limpas():
    print("--- FILTRANDO VAGAS REAIS ---")
    url = "https://www.emprego.co.mz/vagas/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    vagas = []

    try:
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # No Emprego.co.mz, as vagas costumam estar em h2 ou h3 com uma classe específica
        # Este seletor procura especificamente pelos títulos das listas
        itens = soup.find_all(['h2', 'h3'])

        for item in itens:
            link_tag = item.find('a')
            if link_tag:
                titulo = link_tag.get_text(strip=True)
                link = link_tag['href']
                
                # FILTRO: Só aceita se o título for grande e o link parecer uma vaga
                if len(titulo) > 15 and '/vaga/' in link:
                    vagas.append({
                        "titulo": titulo,
                        "empresa": "Emprego.co.mz",
                        "provincia": "Moçambique",
                        "link": link if link.startswith('http') else f"https://www.emprego.co.mz{link}"
                    })

        # Remove duplicados para o arquivo ficar limpo
        vagas_unicas = [dict(t) for t in {tuple(d.items()) for d in vagas}]

        if vagas_unicas:
            with open('vagas.json', 'w', encoding='utf-8') as f:
                json.dump(vagas_unicas[:15], f, ensure_ascii=False, indent=4) # Pega as 15 mais recentes
            print(f"Sucesso: {len(vagas_unicas)} vagas limpas guardadas!")
        else:
            print("Não encontrou vagas com o filtro. Verificando estrutura...")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    capturar_vagas_limpas()
