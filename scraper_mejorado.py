import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

print("🔍 SCRAPING MEJORADO DE TECNOEMPLEO.COM")
print("=" * 90 + "\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Términos de búsqueda
terminos = [
    'big-data',
    'analista-de-datos', 
    'ingeniero-de-datos',
    'cientifico-de-datos'
]

empleos = []
contador = 1

# Scraping
for termino in terminos:
    print(f"🔎 Buscando: '{termino}'...")
    
    try:
        url = f"https://www.tecnoempleo.com/ofertas-trabajo/{termino}"
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        print(f"   ✅ Conexión exitosa\n")
        
        soup = BeautifulSoup(response.content, 'lxml')
        jobs = soup.find_all('a', class_=['text-primary'])
        
        print(f"   📊 Elementos encontrados: {len(jobs)}\n")
        
        for i, job in enumerate(jobs[:25]):
            try:
                texto = job.get_text(strip=True)
                href = job.get('href', '')
                
                # Extraer empresa de texto entre paréntesis
                empresa_text = "No especificada"
                if "(" in texto and ")" in texto:
                    empresa_text = texto[texto.rfind("(")+1:texto.rfind(")")]
                    titulo_text = texto[:texto.rfind("(")].strip()
                else:
                    titulo_text = texto
                
                if not titulo_text or len(titulo_text) < 3:
                    continue
                
                # Construir URL completa
                if href and not href.startswith('http'):
                    href = "https://www.tecnoempleo.com" + href
                
                # Valores por defecto
                localidad = "No especificada"
                stack = "No especificado"
                salario = "No especificado"
                experiencia = "No especificada"
                contrato = "No especificado"
                
                # Intentar obtener detalles de la oferta
                if href and href.startswith('http'):
                    try:
                        resp_detalle = requests.get(href, headers=headers, timeout=10)
                        if resp_detalle.status_code == 200:
                            soup_detalle = BeautifulSoup(resp_detalle.content, 'lxml')
                            texto_detalle = soup_detalle.get_text(separator='\n')
                            
                            # Extraer localidad - buscar palabras clave
                            for linea in texto_detalle.split('\n'):
                                linea = linea.strip()
                                if linea and (
                                    any(ciudad in linea for ciudad in ['Madrid', 'Barcelona', 'Valencia', 'Bilbao', 'Málaga', 'Sevilla', 'Zaragoza']) or
                                    'remoto' in linea.lower() or '100%' in linea
                                ):
                                    localidad = linea[:40]
                                    break
                            
                            # Extraer salario (buscar números con €)
                            match_salario = re.search(r'(\d{2,3}\.?\d*\s*€?.*\d{2,3}\.?\d*\s*€?)', texto_detalle)
                            if match_salario:
                                salario = match_salario.group(0)[:50]
                            
                            # Extraer stack tecnológico
                            techs = ['Python', 'SQL', 'Azure', 'AWS', 'Spark', 'Databricks', 'Java', 
                                    'Scala', 'R', 'TensorFlow', 'Kafka', 'Hadoop', 'Power BI',
                                    'Tableau', 'Git', 'Docker', 'Kubernetes', 'PostgreSQL', 'MongoDB',
                                    'Airflow', 'Flink', 'Scala', 'PySpark', 'Hive', 'HBase', 'Cassandra']
                            stack_encontrado = []
                            for tech in techs:
                                if tech.lower() in texto_detalle.lower():
                                    stack_encontrado.append(tech)
                            if stack_encontrado:
                                stack = ', '.join(list(dict.fromkeys(stack_encontrado))[:10])
                            
                            # Extraer experiencia requerida
                            match_exp = re.search(r'(\d+)\s*[\+]?\s*(años|year|exp)', texto_detalle, re.IGNORECASE)
                            if match_exp:
                                experiencia = f"{match_exp.group(1)}+ años"
                            
                            # Tipo de contrato
                            if 'indefinido' in texto_detalle.lower():
                                contrato = "Indefinido"
                            elif 'temporal' in texto_detalle.lower():
                                contrato = "Temporal"
                            elif 'freelance' in texto_detalle.lower():
                                contrato = "Freelance"
                    
                    except Exception as e:
                        pass
                
                # Agregar empleo
                empleos.append({
                    'Categoría': termino.replace('-', ' ').title(),
                    'Nº': contador,
                    'Título': titulo_text[:80],
                    'Empresa': empresa_text[:60],
                    'Localidad': localidad,
                    'Stack Tecnológico': stack,
                    'Salario': salario,
                    'Experiencia': experiencia,
                    'Tipo Contrato': contrato,
                    'URL': href[:120]
                })
                print(f"   ✅ [{contador}] {titulo_text[:40]}... → {localidad}")
                contador += 1
                
            except Exception as e:
                pass
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}\n")
    
    time.sleep(1)

# Crear DataFrame
df = pd.DataFrame(empleos)

# Mostrar resumen
print("\n" + "=" * 90)
print("📊 RESUMEN DEL SCRAPING MEJORADO")
print("=" * 90)

if len(df) > 0:
    print(f"\n✅ Total de empleos extraídos: {len(df)}")
    print(f"📌 Columnas: {', '.join(df.columns.tolist())}")
    
    print(f"\n📋 DISTRIBUCIÓN POR CATEGORÍA:")
    print(df['Categoría'].value_counts().to_string())
    
    print(f"\n🏢 TOP 5 EMPRESAS:")
    print(df['Empresa'].value_counts().head(5).to_string())
    
    print(f"\n📍 TOP 5 LOCALIDADES:")
    print(df['Localidad'].value_counts().head(5).to_string())
    
    print(f"\n💻 TECNOLOGÍAS MÁS COMUNES:")
    todas_techs = []
    for stack in df['Stack Tecnológico']:
        if stack and stack != "No especificado":
            todas_techs.extend([t.strip() for t in stack.split(',')])
    tech_counts = {}
    for tech in todas_techs:
        tech_counts[tech] = tech_counts.get(tech, 0) + 1
    top_techs = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for tech, count in top_techs:
        print(f"  • {tech}: {count} ofertas")
    
    # Guardar CSV
    archivo_csv = 'empleos_tecnoempleo.csv'
    df.to_csv(archivo_csv, index=False, encoding='utf-8-sig')
    
    print(f"\n{'=' * 90}")
    print(f"✅ ¡ARCHIVO GUARDADO EXITOSAMENTE!")
    print(f"📁 Nombre: {archivo_csv}")
    print(f"📊 Total de registros: {len(df)}")
    print(f"📌 Columnas en el dataset: {len(df.columns)}")
    print(f"{'=' * 90}\n")
    
    print("📋 MUESTRA DE DATOS (primeros 15 registros):\n")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 30)
    print(df.head(15).to_string(index=False))
else:
    print("\n⚠️ No se extrajeron datos.")
