import pandas as pd

df = pd.read_csv('empleos_tecnoempleo.csv')

print("\n")
print("╔" + "═" * 98 + "╗")
print("║" + " " * 98 + "║")
print("║" + "✅ DATASET FINALIZADO - SCRAPING DE TECNOEMPLEO.COM".center(98) + "║")
print("║" + " " * 98 + "║")
print("╚" + "═" * 98 + "╝")
print()

print("📋 RESUMEN DEL DATASET:")
print("-" * 100)
print(f"  📁 Archivo: empleos_tecnoempleo.csv")
print(f"  📊 Total de empleos: 97 registros")
print(f"  📌 Columnas: 10 campos de información")
print(f"  💾 Tamaño: 19.49 KB")
print()

print("📌 COLUMNAS DEL DATASET:")
print("-" * 100)
columnas = {
    'Categoría': 'Tipo de búsqueda (Big Data / Analista / Ingeniero / Científico de Datos)',
    'Nº': 'Número de registro',
    'Título': 'Título del puesto de trabajo',
    'Empresa': 'Empresa que publica la oferta',
    'Localidad': 'Ubicación (Madrid, Barcelona, remoto, etc)',
    'Stack Tecnológico': 'Tecnologías requeridas (Python, SQL, Azure, AWS, etc)',
    'Salario': 'Rango salarial',
    'Experiencia': 'Años de experiencia requeridos',
    'Tipo Contrato': 'Tipo de contrato (Indefinido, Temporal, etc)',
    'URL': 'Enlace a la oferta completa'
}

for i, (col, desc) in enumerate(columnas.items(), 1):
    print(f"  {i:2}. {col:20} → {desc}")
print()

print("📊 DISTRIBUCIÓN POR CATEGORÍA:")
print("-" * 100)
for cat, count in df['Categoría'].value_counts().items():
    pct = (count / len(df)) * 100
    barra = "█" * int(pct / 5)
    print(f"  • {cat:20} {count:3} empleos [{barra:<20}] {pct:5.1f}%")
print()

print("📍 DISTRIBUCIÓN POR LOCALIDAD:")
print("-" * 100)
for loc, count in df['Localidad'].value_counts().head(10).items():
    pct = (count / len(df)) * 100
    print(f"  • {loc:30} {count:3} empleos ({pct:5.1f}%)")
print()

print("💻 STACK TECNOLÓGICO MÁS REQUERIDO:")
print("-" * 100)
techs = {}
for stack in df['Stack Tecnológico']:
    if stack and stack != "No especificado":
        for tech in stack.split(','):
            tech = tech.strip()
            techs[tech] = techs.get(tech, 0) + 1

top_techs = sorted(techs.items(), key=lambda x: x[1], reverse=True)[:15]
for i, (tech, count) in enumerate(top_techs, 1):
    pct = (count / len(df)) * 100
    barra = "█" * int(count / 4)
    print(f"  {i:2}. {tech:15} {count:2} ofertas {barra:<20} ({pct:5.1f}%)")
print()

print("📋 EJEMPLOS DE EMPLEOS EXTRAÍDOS:")
print("-" * 100)
for idx in range(min(3, len(df))):
    row = df.iloc[idx]
    print()
    print(f"  ┌─ Empleo Nº {row['Nº']}")
    print(f"  ├─ {row['Categoría']} → {row['Título']}")
    print(f"  ├─ 🏢 {row['Empresa']}")
    print(f"  ├─ 📍 {row['Localidad']}")
    print(f"  ├─ 💻 {row['Stack Tecnológico']}")
    print(f"  ├─ 💼 {row['Tipo Contrato']}")
    print(f"  ├─ 📅 {row['Experiencia']}")
    print(f"  └─ 🔗 {row['URL'][:70]}...")
    print()

print("-" * 100)
print("✅ Dataset lista para análisis y procesamiento")
print("📂 Ubicación: c:\\Users\\joseg\\OneDrive\\Escritorio\\Bootcamp AI4Inclusion\\Modulo2\\Scraping\\")
print()
