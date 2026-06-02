# DataTalent Solutions S.L. | EDA del Mercado Laboral de Datos en España
#  ***El arte de transformar los datos en estratégia***

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Análisis%20de%20datos-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web%20Scraping-4B8BBE?style=for-the-badge)
![Status](https://img.shields.io/badge/Estado-Proyecto%20EDA%20completo-success?style=for-the-badge)

## 📌 Descripción del proyecto

Este proyecto desarrolla un **Análisis Exploratorio de Datos (EDA)** para **DataTalent Solutions S.L.**, una consultora orientada a diseñar programas de reskilling y upskilling en perfiles de datos.

El objetivo es analizar el mercado laboral de profesionales de datos en España, combinando dos enfoques:

- Un dataset histórico global de salarios de perfiles de datos, filtrado para España.
- Un scraping propio de ofertas reales en Tecnoempleo, utilizado como fotografía actual del mercado español.

El análisis permite responder preguntas clave de negocio sobre salarios, perfiles más demandados, modalidades de trabajo, sesgos del dataset y oportunidades reales para diseñar un programa formativo ajustado al mercado.

---

## 🎯 Objetivos de negocio

El proyecto busca responder a las siguientes preguntas:

| Pregunta | Propósito |
|---|---|
| ¿Qué roles de datos concentran mayor demanda en España? | Definir itinerarios formativos prioritarios. |
| ¿Qué salarios son realistas para perfiles junior, mid y senior? | Ajustar expectativas de alumnos y empresas. |
| ¿Cómo afecta el trabajo remoto al salario? | Identificar oportunidades internacionales desde España. |
| ¿Qué sesgos contiene el dataset? | Evitar conclusiones erróneas o modelos predictivos poco fiables. |
| ¿Qué diferencias hay entre Kaggle y ofertas reales actuales? | Contrastar histórico internacional frente a mercado local activo. |

---

## 🧠 Principales conclusiones

### Resumen ejecutivo

- El dataset global contiene **105.434 registros** y **11 columnas**.
- España representa solo **233 registros**, aproximadamente el **0,22%** del total.
- El periodo analizado para España cubre **2020-2025**.
- El salario mediano en España es de **48.585 USD**, mientras que la media asciende a **66.548 USD**.
- La diferencia entre media y mediana confirma una distribución salarial con **sesgo positivo**, provocada por perfiles remotos e internacionales con salarios muy altos.
- El rol con mayor frecuencia en España es **Data Scientist**, seguido de perfiles como **Data Engineer**.
- **Data Engineer** destaca como perfil especialmente interesante para reskilling: combina volumen suficiente, demanda clara y salario competitivo.
- El trabajo remoto tiene una correlación positiva con el salario: **0,32** entre `remote_ratio` y `salary_in_usd`.
- El scraping de Tecnoempleo muestra una realidad local más prudente: de **93 ofertas**, solo **18 publican salario** y **75 lo ocultan**.

---

## 📊 Métricas clave del análisis de España

| Métrica | Valor |
|---|---:|
| Registros globales | 105.434 |
| Registros España | 233 |
| Peso de España sobre el dataset global | 0,22% |
| Periodo analizado | 2020-2025 |
| Salario medio España | 66.547,64 USD |
| Salario mediano España | 48.585 USD |
| Salario mínimo España | 20.606 USD |
| Salario máximo España | 253.750 USD |
| Registros duplicados conservados | 69 |
| Outliers salariales por IQR | 13 |
| Correlación remoto-salario | 0,32 |

> La mediana se utiliza como indicador principal porque es más robusta ante salarios extremos de perfiles internacionales o altamente especializados.

---

## 🗂️ Estructura del proyecto

```text
Proyecto I/
├── EDATalent.ipynb                  # Notebook base del proyecto
├── EDATalent_Global.ipynb           # Análisis del dataset global
├── EDATalent_Espana.ipynb           # EDA principal filtrado para España
├── EDATecnoempleo.ipynb             # Análisis de ofertas extraídas de Tecnoempleo
├── scraper.py                       # Scraper inicial de ofertas
├── improved_scraper.py              # Scraper enriquecido
├── investigate.py                   # Script auxiliar de inspección
├── verify_csv.py                    # Validación del CSV generado
├── final_summary.py                 # Resumen automatizado del scraping
├── tecnoempleo_jobs_enriched.csv    # Dataset enriquecido de ofertas reales
├── requirements.txt                 # Dependencias del proyecto
├── Proyecto_I.pdf                   # Documento o briefing del proyecto
└── README.md                        # Documentación del repositorio
```

---

## 🧾 Datasets utilizados

### 1. Dataset histórico de salarios

**Fuente:** Data Science Job Salaries, Kaggle  
**Tamaño global:** 105.434 registros  
**Países representados:** 98  
**Filtro principal:** `employee_residence = "ES"`

Se utiliza `employee_residence` en lugar de `company_location` porque el objetivo es analizar a profesionales residentes en España, incluyendo personas que trabajan en remoto para empresas extranjeras.

Columnas principales:

| Variable | Descripción |
|---|---|
| `work_year` | Año del registro |
| `experience_level` | Nivel de experiencia |
| `employment_type` | Tipo de contrato |
| `job_title` | Puesto de trabajo |
| `salary` | Salario en moneda original |
| `salary_currency` | Moneda del salario |
| `salary_in_usd` | Salario convertido a USD |
| `employee_residence` | País de residencia del empleado |
| `remote_ratio` | Porcentaje de trabajo remoto |
| `company_location` | País de la empresa |
| `company_size` | Tamaño de empresa |

### 2. Scraping de Tecnoempleo

**Fuente:** Tecnoempleo  
**Registros extraídos:** 93 ofertas  
**Fecha de publicación observada en muestras:** 29/05/2026  
**Ofertas con salario publicado:** 18  
**Ofertas sin salario publicado:** 75

Columnas principales del CSV enriquecido:

| Variable | Descripción |
|---|---|
| `Category` | Categoría de búsqueda |
| `Title` | Título de la oferta |
| `Company` | Empresa anunciante |
| `Location` | Ubicación o modalidad remota |
| `Publication Date` | Fecha de publicación |
| `Technology Stack` | Tecnologías requeridas |
| `Salary` | Salario publicado o no especificado |
| `Experience` | Experiencia requerida |
| `Contract Type` | Tipo de contrato |
| `URL` | Enlace a la oferta |
| `Description` | Descripción enriquecida |

---

## 🧪 Metodología

El proyecto sigue un flujo de trabajo completo de análisis:

```mermaid
flowchart LR
    A["Carga del dataset global"] --> B["Exploración inicial"]
    B --> C["Filtrado por España"]
    C --> D["Limpieza y normalización"]
    D --> E["Análisis estadístico"]
    E --> F["Detección de outliers y sesgos"]
    F --> G["Visualizaciones"]
    G --> H["Scraping de Tecnoempleo"]
    H --> I["Comparación con mercado local"]
    I --> J["Recomendaciones de negocio"]
```

### Fases principales

| Fase | Descripción |
|---|---|
| Exploración global | Revisión de dimensiones, tipos de datos, nulos y variables. |
| Filtrado España | Selección de registros con residencia del empleado en España. |
| Limpieza | Normalización de texto, revisión de nulos y duplicados. |
| Estadística descriptiva | Media, mediana, cuartiles, desviación estándar y rangos. |
| Outliers | Detección mediante IQR y Z-score. |
| Correlaciones | Relación entre año, salario y trabajo remoto. |
| Segmentación | Análisis por experiencia, rol, empresa y modalidad. |
| Sesgos | Identificación de riesgos de interpretación y modelado. |
| Scraping | Extracción de ofertas reales desde Tecnoempleo. |
| Recomendaciones | Traducción de insights a decisiones para reskilling. |

---

## 📈 Resultados destacados

### Salario por nivel de experiencia

| Nivel | Registros | Media USD | Mediana USD | Mínimo USD | Máximo USD |
|---|---:|---:|---:|---:|---:|
| Executive (EX) | 3 | 97.721,67 | 106.666,00 | 79.833 | 106.666 |
| Senior (SE) | 137 | 73.158,03 | 51.824,00 | 36.773 | 253.750 |
| Mid (MI) | 68 | 64.463,63 | 57.468,50 | 20.606 | 178.000 |
| Junior (EN) | 25 | 32.250,36 | 31.310,00 | 21.593 | 44.210 |

### Top roles por salario medio en España

| Rol | Registros | Media USD | Mediana USD |
|---|---:|---:|---:|
| Research Scientist | 4 | 211.475,00 | 211.475,00 |
| Manager | 4 | 134.462,50 | 127.525,00 |
| Software Engineer | 18 | 113.488,67 | 116.637,00 |
| Power BI Expert | 4 | 104.736,25 | 99.473,00 |
| Machine Learning Engineer | 12 | 102.817,75 | 104.944,00 |
| Data Engineer | 36 | 70.477,47 | 68.293,00 |

> Aunque algunos roles tienen medias muy altas, varios cuentan con pocos registros. Por eso, para decisiones de negocio se priorizan perfiles con volumen suficiente, como Data Engineer, Data Scientist y Data Analyst.

### Evolución salarial por año

| Año | Registros | Media USD | Mediana USD |
|---|---:|---:|---:|
| 2020 | 3 | 83.136,33 | 79.833,00 |
| 2021 | 5 | 49.383,20 | 47.282,00 |
| 2022 | 43 | 52.159,14 | 47.280,00 |
| 2023 | 71 | 60.604,72 | 48.585,00 |
| 2024 | 64 | 85.965,58 | 78.332,50 |
| 2025 | 47 | 63.014,91 | 42.105,00 |

La lectura temporal sugiere un mercado español que gana volumen a partir de 2023, alcanza un pico salarial en 2024 y muestra una estabilización o ajuste en 2025, especialmente en perfiles de entrada.

---

## ⚠️ Sesgos identificados

| Sesgo | Evidencia | Riesgo |
|---|---|---|
| Subrepresentación geográfica | España solo aporta 233 registros de 105.434 | Generalizar patrones globales a España puede sobreestimar salarios. |
| Sesgo de salarios altos | Media muy superior a mediana | Perfiles remotos internacionales elevan artificialmente el promedio. |
| Sesgo por contrato | 232 de 233 registros son full-time | El mercado freelance o parcial queda prácticamente invisible. |
| Sesgo MNAR hipotético | No hay nulos, pero puede haber salarios no reportados en origen | La ausencia de nulos no implica ausencia de sesgo. |
| Autoselección | Datos procedentes de plataformas donde participa un perfil concreto | Pueden estar sobrerrepresentados perfiles senior o muy digitalizados. |
| Sesgo de transparencia salarial | En Tecnoempleo, 75 de 93 ofertas no publican salario | El salario local real puede estar infraobservado o sesgado. |

---

## 🔍 Insights del scraping de Tecnoempleo

El scraping permite contrastar el dataset histórico con ofertas reales activas del mercado español.

### Distribución por categoría

| Categoría | Ofertas |
|---|---:|
| Big Data | 30 |
| Ingeniero de Datos | 29 |
| Analista de Datos | 29 |
| Científico de Datos | 5 |

### Ubicaciones más frecuentes

| Ubicación | Ofertas |
|---|---:|
| Madrid | 36 |
| 100% remoto | 22 |
| Barcelona | 13 |
| Almería | 10 |
| Bizkaia | 2 |
| Zaragoza | 2 |

### Tecnologías más demandadas

| Tecnología | Apariciones |
|---|---:|
| Python | 25 |
| SQL | 23 |
| Java | 12 |
| ETL | 10 |
| AWS | 8 |
| Power BI | 5 |
| Excel | 5 |
| Azure | 4 |
| R | 4 |
| CI/CD | 4 |
| Spark | 3 |

**Conclusión:** Python y SQL aparecen como competencias transversales para la empleabilidad en datos, mientras que cloud, ETL y herramientas BI refuerzan la orientación práctica del programa formativo.

---

## 📊 Visualizaciones incluidas

El notebook principal genera visualizaciones para facilitar la interpretación:

- Histograma con KDE de salarios en España.
- Boxplot de salario por nivel de experiencia.
- Top 10 puestos por salario medio.
- Dispersión entre experiencia y salario.
- Heatmap de correlaciones.
- Heatmap de salario por experiencia y tamaño de empresa.
- Evolución temporal de salario medio y mediano.
- Distribución salarial por modalidad de trabajo remoto.
- Simulaciones visuales de sesgo MNAR y autoselección.

---

## 🛠️ Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| Python | Lenguaje principal |
| Pandas | Limpieza, transformación y análisis |
| NumPy | Operaciones numéricas |
| Matplotlib | Visualización |
| Seaborn | Visualizaciones estadísticas |
| SciPy | Análisis estadístico |
| Requests | Extracción web |
| BeautifulSoup | Scraping HTML |
| lxml | Parseo de contenido web |
| Jupyter Notebook | Desarrollo analítico |

---

## 🚀 Instalación y ejecución

### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repositorio>
cd "Proyecto I"
```

### 2. Crear un entorno virtual

```bash
python -m venv .venv
```

Activación en Windows:

```bash
.venv\Scripts\activate
```

Activación en macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

# Instala de forma automática todo el entorno analítico, gráfico y de ejecución (incluyendo Jupyter y las librerías estadísticas) con un solo comando:

```bash
pip install -r requirements.txt
```

# Para ejecutar todos los notebooks también se recomienda instalar:

```bash
pip install jupyter matplotlib seaborn scipy numpy
```

### 4. Abrir Jupyter Notebook

```bash
jupyter notebook
```

### 5. Ejecutar los notebooks recomendados

Orden sugerido:

1. `EDATalent_Global.ipynb`
2. `EDATalent_Espana.ipynb`
3. `EDATecnoempleo.ipynb`

> El notebook Global y el de España esperan encontrar el archivo `salaries.csv` en el directorio raíz del proyecto.

---

## 📌 Recomendaciones de negocio

### Para el programa de reskilling

- Priorizar rutas formativas hacia **Data Engineer**, **Data Analyst** y **Data Scientist**.
- Construir una base sólida en **Python**, **SQL**, **ETL**, **cloud** y **Power BI**.
- Diseñar expectativas salariales realistas para perfiles junior, tomando la mediana como referencia.
- Diferenciar itinerarios por nivel: Junior → Mid y Senior → especialización avanzada.
- Incluir preparación para trabajo remoto, comunicación asíncrona y colaboración internacional.

### Para la toma de decisiones con datos

- No usar el dataset global sin filtrar para estimar salarios españoles.
- Complementar Kaggle con fuentes locales como Tecnoempleo, LinkedIn Spain, InfoJobs o encuestas salariales nacionales.
- Revisar el mercado de forma periódica, ya que el sector evoluciona rápido.
- Tratar los salarios medios con cautela cuando existan outliers o pocos registros por rol.

---

## ✅ Conclusión final

El análisis muestra que el mercado español de datos es atractivo, pero no debe interpretarse desde referencias globales dominadas por salarios internacionales. España tiene una muestra reducida dentro del dataset global, una fuerte concentración en contratos full-time y una realidad salarial más moderada cuando se contrasta con ofertas locales.

Para DataTalent Solutions S.L., la oportunidad está en diseñar un programa de reskilling orientado a perfiles con demanda real, especialmente Data Engineering, Data Analysis y Data Science, apoyado en competencias prácticas como Python, SQL, ETL, cloud y BI. El valor diferencial del proyecto está en combinar análisis histórico, detección crítica de sesgos y validación con mercado laboral activo.

---

## 👤 Autoría

Proyecto desarrollado como parte del **Módulo II: Análisis y Visualización de Datos**.

**Entidad ficticia del caso de negocio:** DataTalent Solutions S.L.

Desarrolladores: 

Jose Melo  - Ingeniero de Datos
Laura Silva Rubio - Científica de Datos
María Roldán - Estratega de Datos


Este proyecto tiene fines educativos y de portfolio.

Licencia MIT
