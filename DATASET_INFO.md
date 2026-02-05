# Análisis de COVID-19 y Movilidad en EE.UU. - Información del Dataset

## 📊 Sobre el Dataset

### Fuente de Datos
Dataset integrado que combina múltiples fuentes de información pública sobre COVID-19 en Estados Unidos durante la pandemia de 2021.

### Contenido del Dataset (`IntegratedData.csv`)

#### 📈 Datos Epidemiológicos
- **Casos confirmados acumulados** por condado y estado
- **Muertes acumuladas** por condado y estado
- **Casos diarios** (nuevos casos reportados cada día)
- **Muertes diarias** (nuevas muertes reportadas cada día)

#### 🗺️ Datos Geográficos
- **Códigos FIPS:** Identificadores únicos de condados
- **Nombres de condados:** ~3,100 condados de EE.UU.
- **Nombres de estados:** 50 estados + territorios

#### 📅 Datos Temporales
- **Fechas completas:** Serie temporal diaria del 2021
- **Día de la semana:** Lunes a Domingo
- **Indicadores:** Fines de semana, días feriados
- **Estacionalidad:** Patrones por mes, trimestre

#### 🚶 Datos de Movilidad
Cambios porcentuales respecto a una línea base pre-pandemia en visitas a:
- **Comercios y recreación:** Tiendas, restaurantes, centros comerciales, cines
- **Supermercados y farmacias:** Tiendas de alimentos, farmacias
- **Parques:** Parques nacionales, playas, plazas públicas
- **Estaciones de transporte:** Metro, autobuses, trenes
- **Lugares de trabajo:** Oficinas, fábricas
- **Zonas residenciales:** Tiempo pasado en casa

### Especificaciones Técnicas

- **Período:** 2021 (año completo)
- **Alcance Geográfico:** Nacional (Estados Unidos)
- **Granularidad:** Nivel de condado (más detallado que estado)
- **Tamaño del archivo:** ~77 MB
- **Número de registros:** Más de 935,000 filas
- **Frecuencia temporal:** Datos diarios
- **Cobertura:** ~3,100 condados en 50 estados

---

## 🎯 ¿Para Qué Sirve Este Dataset?

Este dataset es una herramienta valiosa para múltiples propósitos:

### 1. 🏥 Análisis Epidemiológico

**Aplicaciones:**
- Identificar patrones temporales de la pandemia (olas, picos estacionales)
- Comparar severidad de la pandemia entre diferentes regiones
- Analizar tasas de mortalidad por área geográfica
- Estudiar la velocidad de propagación del virus
- Evaluar el impacto de variantes del virus

**¿Quién lo usa?**
- Epidemiólogos
- Investigadores de salud pública
- Hospitales y sistemas de salud
- Organizaciones sanitarias internacionales (CDC, OMS)

### 2. 🏛️ Políticas de Salud Pública

**Aplicaciones:**
- Evaluar efectividad de medidas de confinamiento
- Identificar áreas que requieren más recursos sanitarios
- Planificar estrategias de respuesta a futuras pandemias
- Diseñar campañas de vacunación dirigidas
- Optimizar asignación de recursos (ventiladores, personal médico)

**¿Quién lo usa?**
- Gobiernos estatales y locales
- Departamentos de salud pública
- Planificadores de políticas públicas
- Gestores de emergencias

### 3. 🚶 Estudios de Comportamiento Social

**Aplicaciones:**
- Entender cómo cambiaron los patrones de movilidad durante la pandemia
- Analizar correlación entre movilidad y contagios
- Estudiar diferencias de comportamiento entre días laborales y fines de semana
- Medir el cumplimiento de restricciones de movilidad
- Identificar factores sociodemográficos que influyen en el comportamiento

**¿Quién lo usa?**
- Sociólogos
- Psicólogos sociales
- Investigadores de comportamiento humano
- Urbanistas y planificadores urbanos

### 4. 🎓 Investigación Académica

**Aplicaciones:**
- Desarrollar modelos predictivos de propagación viral
- Estudios de correlación entre variables socioeconómicas y salud
- Análisis de series temporales y forecasting
- Machine learning para predicción de brotes
- Análisis geoespacial de propagación de enfermedades

**¿Quién lo usa?**
- Profesores y estudiantes universitarios
- Investigadores en ciencia de datos
- Estudiantes de maestría y doctorado
- Centros de investigación

### 5. 💼 Toma de Decisiones Empresariales

**Aplicaciones:**
- **Empresas:** Planificación de operaciones durante crisis sanitarias
- **Retail:** Ajustar horarios y personal según patrones de movilidad
- **Transporte:** Planificar servicios según demanda real
- **Seguros:** Evaluar riesgos y ajustar primas
- **Inmobiliaria:** Entender cambios en preferencias de ubicación
- **Tecnología:** Desarrollar soluciones de monitoreo y predicción

**¿Quién lo usa?**
- Directores ejecutivos (CEOs)
- Gerentes de operaciones
- Analistas de negocios
- Consultores estratégicos

### 6. 🗣️ Comunicación y Periodismo

**Aplicaciones:**
- Crear visualizaciones comprensibles para el público
- Reportar tendencias basadas en datos reales
- Combatir desinformación con evidencia
- Explicar conceptos epidemiológicos complejos

**¿Quién lo usa?**
- Periodistas de datos
- Comunicadores científicos
- Diseñadores de información
- Equipos de comunicación pública

---

## 📊 Visualizaciones Generadas (11 Gráficas Profesionales)

Este proyecto genera automáticamente 11 visualizaciones profesionales en español que ayudan a interpretar los datos. Todas las gráficas se guardan en alta resolución (300 DPI) en `Output/figures/`.

### 1️⃣ Evolución Temporal de Casos y Muertes (Nacional)
**Archivo:** `1_evolucion_casos_muertes.png`

![Evolución Temporal de Casos y Muertes](Output/figures/1_evolucion_casos_muertes.png)

**Qué muestra:** Gráfica de líneas doble (eje Y dual) que muestra la suma nacional diaria de casos y muertes a lo largo del tiempo.

**Interpretación:** 
- Permite identificar olas/picos de la pandemia
- Observar la relación temporal entre casos y muertes
- Las muertes suelen seguir a los casos con un retraso de ~2-3 semanas

**¿Qué nos dice esta gráfica?**
Esta visualización es fundamental para entender la cronología de la pandemia. Los picos azules (casos) anticipan picos rojos (muertes), lo que ayuda a:
- Predecir carga hospitalaria futura
- Evaluar si las medidas de salud pública están funcionando
- Identificar cuándo comienza y termina cada ola de contagios

**Utilidad práctica:** Hospitales pueden prepararse para picos de muertes 2-3 semanas después de picos de casos.

---

### 2️⃣ Top 10 Condados con Más Casos Acumulados
**Archivo:** `2_top_condados_casos.png`

![Top 10 Condados con Más Casos](Output/figures/2_top_condados_casos.png)

**Qué muestra:** Gráfica de barras horizontales mostrando los 10 condados con mayor número de casos totales, incluyendo nombre del estado.

**Interpretación:**
- Identifica las áreas más afectadas por la pandemia
- Condados urbanos grandes típicamente tienen más casos debido a mayor densidad poblacional
- Útil para priorizar recursos de salud pública

**¿Qué nos dice esta gráfica?**
Muestra las "zonas calientes" de la pandemia. Los condados con más casos suelen ser:
- Áreas metropolitanas grandes (Los Angeles, Nueva York, Chicago)
- Centros de transporte y comercio
- Zonas con mayor densidad poblacional

**Utilidad práctica:** 
- Gobiernos pueden dirigir vacunas y recursos médicos a estas áreas prioritarias
- Empresas pueden ajustar operaciones según riesgo por zona
- Investigadores pueden estudiar factores comunes en áreas más afectadas

---

### 3️⃣ Relación entre Casos Diarios y Muertes Diarias
**Archivo:** `3_casos_vs_muertes.png`

![Casos vs Muertes Diarias](Output/figures/3_casos_vs_muertes.png)

**Qué muestra:** Diagrama de dispersión con línea de tendencia mostrando la correlación entre casos diarios y muertes diarias.

**Interpretación:**
- Muestra la tasa de letalidad implícita (pendiente de la línea)
- Puntos dispersos indican variabilidad por factores como edad, acceso a salud, etc.
- Tendencia positiva esperada: más casos → más muertes

**¿Qué nos dice esta gráfica?**
La pendiente de la línea roja muestra la "letalidad promedio" del virus. Si la línea es muy empinada, significa alta mortalidad relativa. La dispersión de puntos indica que hay muchos factores adicionales:
- Calidad del sistema de salud local
- Demografía (áreas con población mayor tienen más muertes)
- Acceso a tratamientos y vacunas
- Variantes del virus circulantes

**Utilidad práctica:**
- Comparar letalidad entre diferentes períodos
- Evaluar efectividad de tratamientos (si la pendiente disminuye con el tiempo)
- Identificar outliers que requieren investigación especial

---

### 4️⃣ Impacto de Cambios en Movilidad sobre Casos Nuevos
**Archivo:** `4_movilidad_correlacion.png`

![Correlación Movilidad y Casos](Output/figures/4_movilidad_correlacion.png)

**Qué muestra:** Gráfica de barras mostrando correlaciones entre diferentes tipos de movilidad (comercios, supermercados, parques, transporte, trabajo, residencial) y casos diarios.

**Interpretación:**
- **Barras verdes (negativas):** Menos actividad = menos casos (ej: más tiempo en casa)
- **Barras naranjas (positivas):** Más actividad = más casos (ej: más visitas a tiendas)
- Ayuda a entender qué comportamientos reducen/aumentan contagios

**¿Qué nos dice esta gráfica?**
Esta es una de las gráficas más importantes para políticas públicas. Muestra qué cambios en comportamiento están correlacionados con casos:

- **Correlación negativa (buena):** Aumento en tiempo residencial (quedarse en casa) reduce casos
- **Correlación positiva (esperada):** Más visitas a comercios y lugares públicos aumentan casos
- **Transporte público:** Alta correlación positiva porque implica cercanía física prolongada

**Utilidad práctica:**
- Diseñar medidas de confinamiento efectivas (enfocarse en reducir actividades con mayor correlación)
- Evaluar impacto de políticas (¿funcionó el cierre de comercios?)
- Educación pública: comunicar qué actividades son más riesgosas
- Empresas: decidir políticas de trabajo remoto basadas en datos

---

### 5️⃣ Comparación: Días Laborales vs Fines de Semana
**Archivo:** `5_comparacion_dias.png`

![Comparación Días Laborales vs Fines de Semana](Output/figures/5_comparacion_dias.png)

**Qué muestra:** Dos gráficas de barras comparando promedios de casos y muertes en días laborales versus fines de semana.

**Interpretación:**
- Identifica patrones de reporte (algunos lugares reportan menos en fines de semana)
- Puede reflejar diferencias reales en comportamiento social
- Útil para ajustar modelos predictivos

**¿Qué nos dice esta gráfica?**
Muestra un sesgo importante en los datos: los fines de semana típicamente tienen menos casos reportados, pero NO necesariamente menos contagios reales. Esto se debe a:

- **Efecto administrativo:** Menos personal trabajando en laboratorios y oficinas de salud
- **Retraso en reportes:** Los casos del fin de semana se reportan el lunes/martes
- **Comportamiento real:** Menos gente va al médico en fin de semana

**Utilidad práctica:**
- Modelos predictivos deben ajustar por día de la semana
- No entrar en pánico por "bajadas" artificiales los domingos
- Usar promedios de 7 días en lugar de datos diarios crudos
- Periodistas y comunicadores deben reportar tendencias, no fluctuaciones diarias

---

### 6️⃣ Top 10 Estados Más Afectados
**Archivo:** `6_top_estados_casos.png`

![Top 10 Estados Más Afectados](Output/figures/6_top_estados_casos.png)

**Qué muestra:** Gráfica de barras horizontales mostrando los 10 estados con mayor número de casos totales acumulados.

**Interpretación:**
- Compara el impacto de la pandemia a nivel estatal
- Estados más poblados y urbanos típicamente tienen más casos
- Útil para análisis de políticas públicas estatales

**¿Qué nos dice esta gráfica?**
Escalada a nivel estatal, muestra qué estados fueron más golpeados por la pandemia. Factores que explican diferencias:

- **Población:** Estados como California, Texas, Florida tienen más casos por ser más poblados
- **Densidad urbana:** Estados con grandes metrópolis tienen más transmisión
- **Conectividad:** Estados con aeropuertos principales recibieron casos más temprano
- **Políticas locales:** Estados con restricciones más estrictas pueden tener menos casos

**Utilidad práctica:**
- Comparar efectividad de políticas estatales diferentes
- Asignar recursos federales proporcionalmente
- Estudios de caso: ¿por qué algunos estados lo hicieron mejor que otros?
- Planificación para futuras pandemias a nivel estatal

---

### 7️⃣ Tasa de Mortalidad por Estado
**Archivo:** `7_tasa_mortalidad_estados.png`

![Tasa de Mortalidad por Estado](Output/figures/7_tasa_mortalidad_estados.png)

**Qué muestra:** Top 15 estados con mayor porcentaje de muertes respecto a casos (tasa de letalidad).

**Interpretación:**
- Identifica estados con mayor severidad relativa
- Puede indicar diferencias en acceso a salud, demografía, o calidad de atención
- Rojo más intenso = mayor tasa de mortalidad

**¿Qué nos dice esta gráfica?**
Esta gráfica es MÁS importante que el número absoluto de casos, porque muestra la **severidad relativa** de la pandemia. Un estado puede tener pocos casos pero alta mortalidad, indicando:

- **Sistema de salud saturado:** Hospitales sin capacidad
- **Población vulnerable:** Mayor proporción de personas mayores o con comorbilidades
- **Acceso limitado a tratamientos:** Menos acceso a antivirales, oxígeno, UCI
- **Variantes más letales:** Algunas variantes del virus son más mortales
- **Retraso en diagnóstico:** Casos detectados cuando ya están graves

**Utilidad práctica:**
- Priorizar mejoras en infraestructura de salud en estados con alta letalidad
- Investigar qué están haciendo bien los estados con baja letalidad
- Dirigir vacunas y tratamientos a poblaciones vulnerables en estados críticos
- Análisis económico: impacto en productividad y costos sanitarios

---

### 8️⃣ Evolución de Movilidad en el Tiempo
**Archivo:** `8_evolucion_movilidad.png`

![Evolución de Movilidad en el Tiempo](Output/figures/8_evolucion_movilidad.png)

**Qué muestra:** Series temporales de cambios en movilidad para diferentes categorías (suavizado con promedio de 7 días).

**Interpretación:**
- Muestra cómo cambió el comportamiento durante la pandemia
- Caídas pronunciadas = confinamientos/restricciones
- Recuperación gradual = normalización de actividades
- La línea residencial aumenta cuando otras disminuyen

**¿Qué nos dice esta gráfica?**
Esta es una "radiografía del comportamiento social" durante la pandemia. Cuenta la historia de cómo la gente cambió sus hábitos:

**Fase 1 - Confinamiento:** Todas las líneas caen excepto residencial (la gente se queda en casa)
**Fase 2 - Reapertura gradual:** Las líneas empiezan a subir, especialmente supermercados (esenciales)
**Fase 3 - Nueva normalidad:** Patrones se estabilizan pero no vuelven al 100% pre-pandemia

**Detalles importantes:**
- **Parques:** Muy variable (depende del clima y restricciones locales)
- **Transporte público:** Recuperación lenta (la gente prefiere auto por miedo al contagio)
- **Trabajo:** Muchas empresas adoptaron trabajo remoto permanente

**Utilidad práctica:**
- Empresas de transporte pueden planificar servicios según demanda real
- Comercios pueden ajustar horarios y personal
- Gobiernos locales pueden evaluar cumplimiento de restricciones
- Economistas pueden medir impacto en sectores específicos (turismo, retail, etc.)

---

### 9️⃣ Distribución por Día de la Semana
**Archivo:** `9_casos_dia_semana.png`

![Distribución por Día de la Semana](Output/figures/9_casos_dia_semana.png)

**Qué muestra:** Dos gráficas mostrando promedio de casos y muertes para cada día de la semana (Lunes a Domingo).

**Interpretación:**
- Identifica sesgos en reportes (ej: menos reportes los fines de semana)
- Azul/Morado = días laborales, Rojo/Naranja = fines de semana
- Útil para corregir modelos por efectos de calendario

**¿Qué nos dice esta gráfica?**
Detalla día por día el patrón semanal de reportes y casos reales. Observaciones típicas:

**Lunes/Martes:** Picos artificiales porque se reportan casos acumulados del fin de semana
**Miércoles-Viernes:** Datos más estables y confiables
**Sábado/Domingo:** Caída en reportes (menos personal administrativo trabajando)

**Diferencia entre casos y muertes:**
- Casos: Mayor variabilidad semanal (más dependiente de reportes administrativos)
- Muertes: Menos variabilidad (eventos más críticos se reportan más consistentemente)

**Utilidad práctica:**
- **Para analistas:** No comparar lunes con domingo, usar semanas completas
- **Para modelos predictivos:** Incluir variables dummy de día de la semana
- **Para comunicación pública:** Reportar promedios de 7 días, no picos/valles diarios
- **Para planificación hospitalaria:** Anticipar que los lunes tendrán más diagnósticos acumulados

---

### 🔟 Promedio Móvil de Casos (7 días)
**Archivo:** `10_promedio_movil.png`

![Promedio Móvil de 7 Días](Output/figures/10_promedio_movil.png)

**Qué muestra:** Dos gráficas con datos diarios (línea tenue) y promedio móvil de 7 días (línea gruesa) para casos y muertes.

**Interpretación:**
- Suaviza fluctuaciones diarias y resalta tendencias reales
- Facilita identificar inicio/fin de olas
- El promedio móvil es más confiable para análisis de tendencias

**¿Qué nos dice esta gráfica?**
Esta es la versión "limpia" de los datos diarios. El promedio móvil de 7 días elimina:

- **Ruido del fin de semana:** Ya no vemos bajadas artificiales los domingos
- **Picos administrativos:** Los lunes ya no se ven inflados artificialmente
- **Fluctuaciones aleatorias:** Eventos únicos (ej: un brote en una prisión) no distorsionan la tendencia

**¿Por qué 7 días?**
- Captura un ciclo semanal completo
- Es el estándar usado por CDC, OMS y medios de comunicación
- Permite comparaciones internacionales

**Cómo leerla:**
- **Línea sube:** La pandemia está empeorando (ola creciente)
- **Línea baja:** La pandemia está mejorando (ola en descenso)
- **Línea plana:** Situación estable (meseta)
- **Cambio de pendiente:** Momento crucial para decisiones de política pública

**Utilidad práctica:**
- **Gobiernos:** Decidir cuándo implementar o levantar restricciones
- **Hospitales:** Planificar capacidad con 1-2 semanas de anticipación
- **Medios de comunicación:** Reportar tendencias reales sin alarmar innecesariamente
- **Individuos:** Evaluar riesgo personal y ajustar precauciones

---

### 1️⃣1️⃣ Mapa de Calor de Correlación Completo
**Archivo:** `11_mapa_calor_correlacion.png`

![Mapa de Calor de Correlación](Output/figures/11_mapa_calor_correlacion.png)

**Qué muestra:** Matriz de correlación entre todas las variables numéricas del dataset (casos, muertes, movilidad, fin de semana, feriados).

**Interpretación:**
- **Rojo intenso:** Correlación positiva fuerte (cuando una sube, la otra también)
- **Azul intenso:** Correlación negativa fuerte (cuando una sube, la otra baja)
- **Blanco:** Sin correlación
- Útil para identificar relaciones entre variables y validar hipótesis
- Por ejemplo: casos acumulados y muertes acumuladas tienen correlación cercana a 1 (esperado)

**¿Qué nos dice esta gráfica?**
Este es el "mapa de conexiones" entre todas las variables del dataset. Es una herramienta poderosa para:

**Validar hipótesis:**
- ¿La movilidad realmente afecta los casos? → Ver correlación entre columnas de movilidad y daily_cases
- ¿Los fines de semana afectan reportes? → Ver correlación entre is_weekend y daily_cases

**Descubrir patrones no obvios:**
- Correlaciones inesperadas pueden indicar factores causales ocultos
- Falta de correlación donde esperábamos una puede indicar problemas en los datos

**Cómo leerlo:**
- **Diagonal (1.0):** Cada variable perfectamente correlacionada consigo misma
- **Casos acumulados ↔ Muertes acumuladas (~0.95):** Fuerte correlación (más casos = más muertes)
- **Movilidad residencial ↔ Otros tipos de movilidad (negativa):** Cuando aumenta tiempo en casa, disminuye movilidad externa
- **Daily_cases ↔ Movilidad en comercios (positiva):** Más visitas = más contagios

**Correlaciones importantes a buscar:**
1. **Casos vs Movilidad:** ¿Qué actividades tienen mayor correlación con contagios?
2. **Casos vs Fines de semana:** ¿Hay sesgo de reporte?
3. **Casos vs Días feriados:** ¿Los feriados afectan los datos?

**Utilidad práctica:**
- **Científicos de datos:** Selección de variables para modelos predictivos
- **Epidemiólogos:** Identificar factores de riesgo principales
- **Políticos:** Decidir qué restricciones implementar (enfocar en actividades con alta correlación)
- **Investigadores:** Generar nuevas hipótesis para estudios profundos
- **Verificación de calidad:** Detectar datos anómalos (correlaciones que no tienen sentido)

---

## 🔍 Insights Principales del Análisis

Después de procesar y visualizar este dataset, podemos concluir:

1. **✅ La movilidad SÍ afecta los contagios**
   - Existe correlación clara entre aumento en actividades públicas y casos
   - El transporte público muestra la correlación más fuerte
   - Quedarse en casa (aumento en movilidad residencial) correlaciona con menos casos

2. **✅ Las muertes siguen a los casos con 2-3 semanas de retraso**
   - Patrón consistente útil para predicción
   - Permite a hospitales prepararse con anticipación
   - Crucial para planificación de recursos médicos

3. **✅ Los datos tienen sesgo de reporte**
   - Los fines de semana muestran menos casos (efecto administrativo)
   - Los lunes tienen picos artificiales (acumulación del fin de semana)
   - Es esencial usar promedios móviles de 7 días

4. **✅ La tasa de mortalidad varía significativamente por región**
   - No todos los estados experimentaron la misma severidad
   - Factores: demografía, sistema de salud, acceso a tratamientos
   - Importante para asignación equitativa de recursos

5. **✅ El comportamiento social cambió drásticamente**
   - Las gráficas de movilidad muestran un "antes y después" claro
   - El trabajo remoto se adoptó masivamente
   - El transporte público nunca recuperó niveles pre-pandemia

6. **✅ Los promedios móviles son esenciales**
   - Los datos diarios crudos tienen demasiado ruido
   - Ventanas de 7 días capturan ciclos semanales
   - Facilitan identificación de tendencias reales

---

## 📈 Casos de Uso Reales

### 🏥 Sector Salud
- **Hospitales:** Planificar capacidad de UCI y personal según tendencias
- **Departamentos de Salud Pública:** Diseñar campañas de vacunación y comunicación
- **Investigadores médicos:** Estudiar patrones de transmisión y efectividad de tratamientos

### 🏛️ Gobierno y Política Pública
- **Tomadores de decisiones:** Evaluar cuándo implementar/levantar restricciones
- **Planificadores urbanos:** Diseñar ciudades más resilientes a pandemias
- **Gestión de emergencias:** Preparación para futuras crisis sanitarias

### 📚 Educación e Investigación
- **Universidades:** Material didáctico para cursos de epidemiología, ciencia de datos, salud pública
- **Estudiantes:** Proyectos de tesis sobre análisis de datos, machine learning aplicado
- **Investigadores:** Publicaciones académicas sobre correlación movilidad-contagios

### 💼 Sector Empresarial
- **Comercios:** Entender patrones de consumo durante crisis
- **Transporte:** Planificar servicios según demanda real
- **Seguros:** Evaluar riesgos y ajustar primas
- **Empresas tech:** Desarrollar soluciones de monitoreo y predicción

### 📊 Ciencia de Datos y Analytics
- **Modelos predictivos:** Entrenar algoritmos de machine learning para predecir olas
- **Análisis de series temporales:** Estudiar patrones estacionales y cíclicos
- **Visualización de datos:** Ejemplos de buenas prácticas en gráficas explicativas

---

## 📖 Documentación Relacionada

- **[README.md](README.md)** - Documentación técnica del proyecto, arquitectura del código, módulos y pipeline ETL

---

## 📊 Cómo Generar las Visualizaciones

### Opción 1: Ejecutar el pipeline completo
```bash
python pipeline.py
```
Esto genera automáticamente todas las 11 gráficas en `Output/figures/`

### Opción 2: Generar solo las visualizaciones
```bash
python -m Vizualize.plot --input "Output/IntegratedData_cleaned.csv" --outdir "Output/figures"
```

### Opción 3: Desde código Python
```python
from Vizualize.plot import generar_todas_las_graficas

generar_todas_las_graficas(
    csv_path="Output/IntegratedData_transformed.csv",
    output_dir="Output/figures"
)
```

---

## 💡 Recomendaciones para Interpretar los Datos

### 1. Siempre usa promedios móviles
- Los datos diarios tienen mucho ruido
- Ventana de 7 días es el estándar internacional
- Facilita ver tendencias reales

### 2. Ten en cuenta el sesgo de reporte
- Los fines de semana tienen menos reportes
- Los lunes tienen picos artificiales
- Compara semanas completas, no días individuales

### 3. Contexto es clave
- Considera la población de cada región
- Tasas son más informativas que números absolutos
- Compara tasas per cápita, no valores brutos

### 4. Correlación no implica causalidad
- La movilidad correlaciona con casos, pero hay otros factores
- Usa análisis multivariable para conclusiones robustas
- Considera variables confusoras

### 5. Valida tus hipótesis
- Usa múltiples gráficas para confirmar patrones
- Compara diferentes periodos temporales
- Busca consistencia en distintos niveles geográficos

---

## 📞 Contacto y Recursos

- **Repositorio:** https://github.com/kenmaroyert1/WilsonTrabajo1
- **Documentación Técnica:** [README.md](README.md)
- **Proyecto académico** - Universidad

---

**Última actualización:** Febrero 2026
