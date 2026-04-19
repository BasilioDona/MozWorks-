import requests
import json

def capturar_vagas_api():
    print("--- ACEDENDO À BASE DE DADOS DA CONTACT ---")
    # Este é o link direto onde a Contact guarda as informações das vagas
    url = "https://www.contact.co.mz/pt/recrutamento/ofertas-de-emprego?format=raw"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        response = requests.get(url, headers=headers, timeout=25)
        print(f"Resposta do Servidor: {response.status_code}")
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        vagas_lista = []
        
        # Procura pelos blocos reais de vagas (conforme a imagem que enviaste)
        blocos = soup.select('.item-page') or soup.find_all('div', class_='row-fluid')

        for bloco in soup.find_all('a', href=True):
            href = bloco['href']
            # Filtramos apenas o que é detalhe de oferta real
            if 'detalhes-da-oferta' in href:
                titulo = bloco.get_text(strip=True)
                if titulo and len(titulo) > 5 and 'detalhes' not in titulo.lower():
                    link_final = href if href.startswith('http') else f"https://www.contact.co.mz{href}"
                    
                    vagas_lista.append({
                        "titulo": titulo,
                        "empresa": "Contact Moçambique",
                        "provincia": "Moçambique",
                        "link": link_final
                    })

        if vagas_lista:
            # Remove duplicados mantendo a ordem
            vagas_finais = []
            vistos = set()
            for v in vagas_lista:
                if v['titulo'] not in vistos:
                    vagas_finais.append(v)
                    vistos.add(v['titulo'])

            with open('vagas.json', 'w', encoding='utf-8') as f:
                json.dump(vagas_finais[:10], f, ensure_ascii=False, indent=4)
            print(f"SUCESSO ABSOLUTO: {len(vagas_finais)} vagas reais gravadas!")
        else:
            print("AVISO: O servidor respondeu, mas não encontrámos os títulos.")

    except Exception as e:
        print(f"ERRO NO ROBÔ: {e}")

if __name__ == "__main__":
    capturar_vagas_api()

