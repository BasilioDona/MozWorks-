import requests
from bs4 import BeautifulSoup
import json

def capturar_vagas_contact():
    print("--- PESQUISANDO NA CONTACT MOÇAMBIQUE ---")
    url = "https://www.contact.co.mz/pt/recrutamento/ofertas-de-emprego"
    vagas_lista = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Na Contact, as vagas estão geralmente em links dentro de uma lista de ofertas
        # Procuramos por links que levam para detalhes da vaga
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            texto = link.get_text(strip=True)
            
            # FILTRO: Só aceita se o link tiver 'ofertas-de-emprego/' e o texto for longo
            if 'ofertas-de-emprego/' in href and len(texto) > 10:
                # Garante que o link é completo
                link_final = href if href.startswith('http') else f"https://www.contact.co.mz{href}"
                
                vagas_lista.append({
                    "titulo": texto,
                    "empresa": "Contact Moçambique",
                    "provincia": "Moçambique",
                    "link": link_final
                })

        # Limpar duplicados (o site às vezes repete o link na imagem e no texto)
        vagas_unicas = [dict(t) for t in {tuple(d.items()) for d in vagas_lista}]

        if vagas_unicas:
            with open('vagas.json', 'w', encoding='utf-8') as f:
                json.dump(vagas_unicas[:15], f, ensure_ascii=False, indent=4)
            print(f"SUCESSO: {len(vagas_unicas)} vagas capturadas da Contact!")
        else:
            print("AVISO: Nenhuma vaga encontrada. O robô pode precisar de um ajuste de filtro.")

    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    capturar_vagas_contact()
