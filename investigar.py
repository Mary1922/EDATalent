import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = 'https://www.tecnoempleo.com/globalsysinfo/re-206065'

try:
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Buscar estructura
    print("=" * 70)
    print("INVESTIGANDO ESTRUCTURA DE OFERTA")
    print("=" * 70)
    print()
    
    # Extraer texto limpio
    texto = soup.get_text(separator='\n')
    lineas = [l.strip() for l in texto.split('\n') if l.strip()]
    
    print("PRIMERAS 100 LÍNEAS:")
    for i, linea in enumerate(lineas[:100]):
        print(f"{i+1:3}. {linea}")
        
except Exception as e:
    print(f"Error: {e}")
