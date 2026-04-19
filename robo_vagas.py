import requests
from bs4 import BeautifulSoup
import json

def capturar_contact_certeiro():
    print("--- PESQUISANDO VAGAS REAIS NA CONTACT ---")
    url = "https://www.contact.co.mz/pt/recrutamento/ofertas-de-emprego"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    vagas_lista = []

    try:
        response = requests.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # No site da Contact, os títulos das vagas estão em <a> dentro de h2 ou h3, 
        # mas o segredo é filtrar pelo link que contém 'detalhes-da-oferta'
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            texto = link.get_text(strip=True)
            
            # FILTRO: Só aceita links de detalhes da vaga e ignora nomes de províncias
            if 'detalhes-da-oferta' in href.lower() and len(texto) > 5:
                # Se o texto for apenas um número ou província (como "Maputo (2)"), o robô ignora
                if '(' not in texto: 
                    vagas_lista.append({
                        "titulo": texto,
                        "empresa": "Contact Moçambique",
                        "provincia": "Moçambique",
                        "link": href if href.startswith('http') else f"https://www.contact.co.mz{href}"
                    })

        if vagas_lista:
            # Remove duplicados e salva
            vagas_unicas = [dict(t) for t in {tuple(d.items()) for d in vagas_lista}]
            with open('vagas.json', 'w', encoding='utf-8') as f:
                json.dump(vagas_unicas[:15], f, ensure_ascii=False, indent=4)
            print(f"SUCESSO: {len(vagas_unicas)} vagas reais encontradas!")
        else:
            print("AVISO: Nenhuma vaga real encontrada. A verificar estrutura...")

    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    capturar_contact_certeiro()
