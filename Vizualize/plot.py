"""Script de visualización para el dataset limpio.

Genera 11 figuras claras y en español en `Output/figures/`:
 1. Evolución temporal de casos y muertes (promedio nacional)
 2. Top 10 condados con más casos acumulados
 3. Relación entre casos diarios y muertes diarias
 4. Impacto de movilidad en casos (correlación)
 5. Comparación de actividad en días laborales vs fines de semana
 6. Comparación de top 10 estados más afectados
 7. Tasa de mortalidad por estado (top 15)
 8. Evolución de movilidad en el tiempo
 9. Distribución de casos por día de la semana
 10. Promedio móvil de casos (7 días)
 11. Mapa de calor - Correlación completa de variables

Uso:
    python -m Vizualize.plot --input <ruta_csv> --outdir Output/figures
"""

from __future__ import annotations

import argparse
import os
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Configurar estilo de gráficas
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 10


def ensure_outdir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def plot_1_temporal_nacional(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 1: Evolución temporal de casos y muertes (promedio nacional diario)"""
    df_temp = df.copy()
    df_temp['date'] = pd.to_datetime(df_temp['date'], errors='coerce')
    
    # Agrupar por fecha y calcular suma nacional diaria
    daily = df_temp.groupby('date').agg({
        'daily_cases': 'sum',
        'daily_deaths': 'sum'
    }).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    color_casos = 'tab:blue'
    ax1.set_xlabel('Fecha', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Casos Diarios (Nacional)', color=color_casos, fontsize=12, fontweight='bold')
    ax1.plot(daily['date'], daily['daily_cases'], color=color_casos, linewidth=1.5, label='Casos Diarios')
    ax1.tick_params(axis='y', labelcolor=color_casos)
    ax1.grid(True, alpha=0.3)
    
    ax2 = ax1.twinx()
    color_muertes = 'tab:red'
    ax2.set_ylabel('Muertes Diarias (Nacional)', color=color_muertes, fontsize=12, fontweight='bold')
    ax2.plot(daily['date'], daily['daily_deaths'], color=color_muertes, linewidth=1.5, label='Muertes Diarias')
    ax2.tick_params(axis='y', labelcolor=color_muertes)
    
    plt.title('Evolución Temporal de Casos y Muertes por COVID-19 (EE.UU.)', fontsize=14, fontweight='bold', pad=20)
    fig.tight_layout()
    
    fname = os.path.join(outdir, "1_evolucion_casos_muertes.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_2_top_condados(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 2: Top 10 condados con más casos acumulados"""
    # Obtener el máximo de casos por condado (casos acumulados finales)
    top_counties = df.groupby(['county', 'state'])['cases'].max().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Crear etiquetas con condado y estado
    labels = [f"{county.title()}\n({state.title()})" for (county, state) in top_counties.index]
    values = top_counties.values
    
    colors = plt.cm.Reds([(i+3)/13 for i in range(len(values))])
    bars = ax.barh(labels, values, color=colors, edgecolor='black', linewidth=0.7)
    
    # Añadir valores en las barras
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(val + max(values)*0.01, i, f'{int(val):,}', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Casos Acumulados Totales', fontsize=12, fontweight='bold')
    ax.set_ylabel('Condado (Estado)', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 Condados con Más Casos de COVID-19', fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    fname = os.path.join(outdir, "2_top_condados_casos.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_3_casos_vs_muertes(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 3: Relación entre casos diarios y muertes diarias"""
    # Tomar muestra aleatoria para hacer el scatter más legible (si hay muchos datos)
    sample_size = min(50000, len(df))
    df_sample = df[['daily_cases', 'daily_deaths']].dropna().sample(n=sample_size, random_state=42)
    
    # Filtrar outliers extremos para mejor visualización
    df_sample = df_sample[(df_sample['daily_cases'] >= 0) & (df_sample['daily_cases'] <= df_sample['daily_cases'].quantile(0.99))]
    df_sample = df_sample[(df_sample['daily_deaths'] >= 0) & (df_sample['daily_deaths'] <= df_sample['daily_deaths'].quantile(0.99))]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    scatter = ax.scatter(df_sample['daily_cases'], df_sample['daily_deaths'], 
                         alpha=0.4, s=20, c=df_sample['daily_cases'], cmap='YlOrRd', edgecolors='none')
    
    # Línea de tendencia
    z = np.polyfit(df_sample['daily_cases'], df_sample['daily_deaths'], 1)
    p = np.poly1d(z)
    ax.plot(df_sample['daily_cases'].sort_values(), p(df_sample['daily_cases'].sort_values()), 
            "r--", linewidth=2, label=f'Tendencia: y={z[0]:.3f}x+{z[1]:.2f}')
    
    ax.set_xlabel('Casos Diarios', fontsize=12, fontweight='bold')
    ax.set_ylabel('Muertes Diarias', fontsize=12, fontweight='bold')
    ax.set_title('Relación entre Casos Diarios y Muertes Diarias', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.colorbar(scatter, ax=ax, label='Casos Diarios')
    plt.tight_layout()
    
    fname = os.path.join(outdir, "3_casos_vs_muertes.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_4_movilidad_impacto(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 4: Correlación entre movilidad y casos nuevos"""
    mobility_cols = ['retail_recreation', 'grocery_pharmacy', 'parks', 'transit', 'workplaces', 'residential']
    available_cols = [c for c in mobility_cols if c in df.columns]
    
    if not available_cols:
        raise ValueError("No hay columnas de movilidad disponibles")
    
    # Calcular correlación con daily_cases
    correlations = []
    labels_es = {
        'retail_recreation': 'Comercios y\nRecreación',
        'grocery_pharmacy': 'Supermercados y\nFarmacias',
        'parks': 'Parques',
        'transit': 'Transporte\nPúblico',
        'workplaces': 'Lugares de\nTrabajo',
        'residential': 'Residencial'
    }
    
    for col in available_cols:
        corr = df[[col, 'daily_cases']].dropna().corr().iloc[0, 1]
        correlations.append((labels_es.get(col, col), corr))
    
    labels, values = zip(*correlations)
    
    fig, ax = plt.subplots(figsize=(11, 7))
    colors = ['green' if v < 0 else 'orange' for v in values]
    bars = ax.bar(range(len(labels)), values, color=colors, edgecolor='black', linewidth=1.2, alpha=0.8)
    
    # Añadir valores en las barras
    for i, (bar, val) in enumerate(zip(bars, values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + (0.02 if height > 0 else -0.05),
                f'{val:.3f}', ha='center', va='bottom' if height > 0 else 'top', fontsize=11, fontweight='bold')
    
    ax.axhline(y=0, color='black', linewidth=1)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('Correlación con Casos Diarios', fontsize=12, fontweight='bold')
    ax.set_title('Impacto de Cambios en Movilidad sobre Casos Nuevos', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim([min(values)-0.1, max(values)+0.1])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    fname = os.path.join(outdir, "4_movilidad_correlacion.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_5_dia_semana(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 5: Comparación de casos en días laborales vs fines de semana"""
    df_temp = df.copy()
    
    # Crear categoría
    df_temp['tipo_dia'] = df_temp['is_weekend'].apply(lambda x: 'Fin de Semana' if x == 1.0 else 'Día Laboral')
    
    # Calcular promedios
    avg_by_type = df_temp.groupby('tipo_dia').agg({
        'daily_cases': 'mean',
        'daily_deaths': 'mean'
    }).reset_index()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gráfica de casos
    colors_casos = ['#3498db', '#e74c3c']
    bars1 = ax1.bar(avg_by_type['tipo_dia'], avg_by_type['daily_cases'], 
                     color=colors_casos, edgecolor='black', linewidth=1.2, alpha=0.85)
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                f'{height:.1f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax1.set_ylabel('Promedio de Casos Diarios', fontsize=12, fontweight='bold')
    ax1.set_title('Casos Promedio por Tipo de Día', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Gráfica de muertes
    colors_muertes = ['#9b59b6', '#e67e22']
    bars2 = ax2.bar(avg_by_type['tipo_dia'], avg_by_type['daily_deaths'], 
                     color=colors_muertes, edgecolor='black', linewidth=1.2, alpha=0.85)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                f'{height:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax2.set_ylabel('Promedio de Muertes Diarias', fontsize=12, fontweight='bold')
    ax2.set_title('Muertes Promedio por Tipo de Día', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    fig.suptitle('Comparación: Días Laborales vs Fines de Semana', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    fname = os.path.join(outdir, "5_comparacion_dias.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_6_top_estados(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 6: Comparación de top 10 estados más afectados"""
    # Obtener el máximo de casos por estado (casos acumulados finales)
    top_states = df.groupby('state')['cases'].max().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Crear etiquetas
    labels = [state.title() for state in top_states.index]
    values = top_states.values
    
    colors = plt.cm.Blues([(i+3)/13 for i in range(len(values))])
    bars = ax.barh(labels, values, color=colors, edgecolor='black', linewidth=0.7)
    
    # Añadir valores en las barras
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(val + max(values)*0.01, i, f'{int(val):,}', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Casos Acumulados Totales', fontsize=12, fontweight='bold')
    ax.set_ylabel('Estado', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 Estados con Más Casos de COVID-19', fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    fname = os.path.join(outdir, "6_top_estados_casos.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_7_tasa_mortalidad(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 7: Tasa de mortalidad por estado (top 15)"""
    # Calcular tasa de mortalidad por estado
    state_stats = df.groupby('state').agg({
        'cases': 'max',
        'deaths': 'max'
    }).reset_index()
    
    state_stats['tasa_mortalidad'] = (state_stats['deaths'] / state_stats['cases'] * 100)
    state_stats = state_stats[state_stats['cases'] > 10000]  # Filtrar estados con pocos casos
    state_stats = state_stats.sort_values('tasa_mortalidad', ascending=False).head(15)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    labels = [state.title() for state in state_stats['state']]
    values = state_stats['tasa_mortalidad'].values
    
    # Colores basados en severidad
    colors = plt.cm.Reds([(v - values.min()) / (values.max() - values.min()) for v in values])
    bars = ax.barh(labels, values, color=colors, edgecolor='black', linewidth=0.7)
    
    # Añadir valores en las barras
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(val + max(values)*0.01, i, f'{val:.2f}%', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Tasa de Mortalidad (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Estado', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 Estados con Mayor Tasa de Mortalidad por COVID-19', fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    fname = os.path.join(outdir, "7_tasa_mortalidad_estados.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_8_evolucion_movilidad(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 8: Evolución de movilidad en el tiempo"""
    df_temp = df.copy()
    df_temp['date'] = pd.to_datetime(df_temp['date'], errors='coerce')
    
    mobility_cols = ['retail_recreation', 'grocery_pharmacy', 'parks', 'transit', 'workplaces', 'residential']
    available_cols = [c for c in mobility_cols if c in df.columns]
    
    # Agrupar por fecha y calcular promedio
    daily_mobility = df_temp.groupby('date')[available_cols].mean().reset_index()
    
    # Suavizar con rolling mean
    for col in available_cols:
        daily_mobility[col] = daily_mobility[col].rolling(window=7, center=True).mean()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    labels_es = {
        'retail_recreation': 'Comercios y Recreación',
        'grocery_pharmacy': 'Supermercados y Farmacias',
        'parks': 'Parques',
        'transit': 'Transporte Público',
        'workplaces': 'Lugares de Trabajo',
        'residential': 'Residencial'
    }
    
    for col in available_cols:
        ax.plot(daily_mobility['date'], daily_mobility[col], label=labels_es.get(col, col), linewidth=2)
    
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_xlabel('Fecha', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cambio en Movilidad (% respecto a baseline)', fontsize=12, fontweight='bold')
    ax.set_title('Evolución de Patrones de Movilidad (Promedio 7 días)', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fname = os.path.join(outdir, "8_evolucion_movilidad.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_9_casos_dia_semana(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 9: Distribución de casos por día de la semana"""
    df_temp = df.copy()
    
    # Mapear día de la semana a nombres en español
    dias_semana = {
        0.0: 'Domingo',
        1.0: 'Lunes',
        2.0: 'Martes',
        3.0: 'Miércoles',
        4.0: 'Jueves',
        5.0: 'Viernes',
        6.0: 'Sábado'
    }
    
    df_temp['dia_nombre'] = df_temp['day_of_week'].map(dias_semana)
    
    # Calcular promedios por día
    avg_by_day = df_temp.groupby('dia_nombre').agg({
        'daily_cases': 'mean',
        'daily_deaths': 'mean'
    }).reindex(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Gráfica de casos
    colors_casos = ['#3498db' if dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'] else '#e74c3c' 
                    for dia in avg_by_day.index]
    bars1 = ax1.bar(avg_by_day.index, avg_by_day['daily_cases'], 
                     color=colors_casos, edgecolor='black', linewidth=1.2, alpha=0.85)
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                f'{height:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Promedio de Casos Diarios', fontsize=12, fontweight='bold')
    ax1.set_title('Casos Promedio por Día de la Semana', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_xticklabels(avg_by_day.index, rotation=45, ha='right')
    
    # Gráfica de muertes
    colors_muertes = ['#9b59b6' if dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'] else '#e67e22' 
                      for dia in avg_by_day.index]
    bars2 = ax2.bar(avg_by_day.index, avg_by_day['daily_deaths'], 
                     color=colors_muertes, edgecolor='black', linewidth=1.2, alpha=0.85)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                f'{height:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax2.set_ylabel('Promedio de Muertes Diarias', fontsize=12, fontweight='bold')
    ax2.set_title('Muertes Promedio por Día de la Semana', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_xticklabels(avg_by_day.index, rotation=45, ha='right')
    
    fig.suptitle('Distribución de Casos y Muertes por Día de la Semana', fontsize=15, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    fname = os.path.join(outdir, "9_casos_dia_semana.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_10_promedio_movil(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 10: Promedio móvil de casos (7 días)"""
    df_temp = df.copy()
    df_temp['date'] = pd.to_datetime(df_temp['date'], errors='coerce')
    
    # Agrupar por fecha y calcular suma nacional diaria
    daily = df_temp.groupby('date').agg({
        'daily_cases': 'sum',
        'daily_deaths': 'sum'
    }).reset_index()
    
    # Calcular promedio móvil de 7 días
    daily['casos_ma7'] = daily['daily_cases'].rolling(window=7, center=True).mean()
    daily['muertes_ma7'] = daily['daily_deaths'].rolling(window=7, center=True).mean()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Gráfica de casos
    ax1.plot(daily['date'], daily['daily_cases'], alpha=0.3, color='lightblue', linewidth=0.8, label='Casos Diarios')
    ax1.plot(daily['date'], daily['casos_ma7'], color='darkblue', linewidth=2.5, label='Promedio Móvil 7 días')
    ax1.set_ylabel('Casos Diarios', fontsize=12, fontweight='bold')
    ax1.set_title('Casos de COVID-19 con Promedio Móvil de 7 Días', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Gráfica de muertes
    ax2.plot(daily['date'], daily['daily_deaths'], alpha=0.3, color='lightcoral', linewidth=0.8, label='Muertes Diarias')
    ax2.plot(daily['date'], daily['muertes_ma7'], color='darkred', linewidth=2.5, label='Promedio Móvil 7 días')
    ax2.set_xlabel('Fecha', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Muertes Diarias', fontsize=12, fontweight='bold')
    ax2.set_title('Muertes por COVID-19 con Promedio Móvil de 7 Días', fontsize=13, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle('Tendencias Suavizadas de la Pandemia', fontsize=15, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    fname = os.path.join(outdir, "10_promedio_movil.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def plot_11_mapa_calor_correlacion(df: pd.DataFrame, outdir: str) -> str:
    """Gráfica 11: Mapa de calor - Correlación completa de variables"""
    # Seleccionar columnas numéricas relevantes
    numeric_cols = ['cases', 'deaths', 'daily_cases', 'daily_deaths', 
                    'retail_recreation', 'grocery_pharmacy', 'parks', 
                    'transit', 'workplaces', 'residential', 
                    'is_weekend', 'is_holiday']
    
    available_cols = [c for c in numeric_cols if c in df.columns]
    
    # Calcular matriz de correlación
    corr_matrix = df[available_cols].corr()
    
    # Mapear nombres a español
    labels_es = {
        'cases': 'Casos\nAcumulados',
        'deaths': 'Muertes\nAcumuladas',
        'daily_cases': 'Casos\nDiarios',
        'daily_deaths': 'Muertes\nDiarias',
        'retail_recreation': 'Comercios y\nRecreación',
        'grocery_pharmacy': 'Supermercados\ny Farmacias',
        'parks': 'Parques',
        'transit': 'Transporte\nPúblico',
        'workplaces': 'Lugares de\nTrabajo',
        'residential': 'Residencial',
        'is_weekend': 'Fin de\nSemana',
        'is_holiday': 'Día\nFeriado'
    }
    
    # Renombrar índices y columnas
    corr_matrix.index = [labels_es.get(col, col) for col in corr_matrix.index]
    corr_matrix.columns = [labels_es.get(col, col) for col in corr_matrix.columns]
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Crear mapa de calor
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, vmin=-1, vmax=1, square=True, linewidths=0.5,
                cbar_kws={"shrink": 0.8, "label": "Correlación"},
                ax=ax, annot_kws={'fontsize': 9})
    
    ax.set_title('Mapa de Calor: Correlación entre Variables de COVID-19 y Movilidad', 
                 fontsize=15, fontweight='bold', pad=20)
    
    plt.tight_layout()
    fname = os.path.join(outdir, "11_mapa_calor_correlacion.png")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
    return fname


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Generador de 11 visualizaciones claras para el dataset limpio")
    parser.add_argument("--input", required=False, default="Output/IntegratedData_cleaned.csv", help="CSV limpio de entrada")
    parser.add_argument("--outdir", required=False, default="Output/figures", help="Directorio de salida para figuras")

    args = parser.parse_args(argv)
    ensure_outdir(args.outdir)

    print("Cargando dataset limpio...")
    df = pd.read_csv(args.input, low_memory=False)

    # Asegurar formatos mínimos
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    results = []
    
    print("\n🔄 Generando gráfica 1: Evolución temporal nacional...")
    try:
        results.append(plot_1_temporal_nacional(df, args.outdir))
        print("✅ Gráfica 1 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 1: {e}")

    print("\n🔄 Generando gráfica 2: Top 10 condados...")
    try:
        results.append(plot_2_top_condados(df, args.outdir))
        print("✅ Gráfica 2 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 2: {e}")

    print("\n🔄 Generando gráfica 3: Casos vs muertes...")
    try:
        results.append(plot_3_casos_vs_muertes(df, args.outdir))
        print("✅ Gráfica 3 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 3: {e}")

    print("\n🔄 Generando gráfica 4: Impacto de movilidad...")
    try:
        results.append(plot_4_movilidad_impacto(df, args.outdir))
        print("✅ Gráfica 4 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 4: {e}")

    print("\n🔄 Generando gráfica 5: Comparación días...")
    try:
        results.append(plot_5_dia_semana(df, args.outdir))
        print("✅ Gráfica 5 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 5: {e}")

    print("\n🔄 Generando gráfica 6: Top 10 estados...")
    try:
        results.append(plot_6_top_estados(df, args.outdir))
        print("✅ Gráfica 6 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 6: {e}")

    print("\n🔄 Generando gráfica 7: Tasa de mortalidad...")
    try:
        results.append(plot_7_tasa_mortalidad(df, args.outdir))
        print("✅ Gráfica 7 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 7: {e}")

    print("\n🔄 Generando gráfica 8: Evolución de movilidad...")
    try:
        results.append(plot_8_evolucion_movilidad(df, args.outdir))
        print("✅ Gráfica 8 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 8: {e}")

    print("\n🔄 Generando gráfica 9: Casos por día de la semana...")
    try:
        results.append(plot_9_casos_dia_semana(df, args.outdir))
        print("✅ Gráfica 9 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 9: {e}")

    print("\n🔄 Generando gráfica 10: Promedio móvil...")
    try:
        results.append(plot_10_promedio_movil(df, args.outdir))
        print("✅ Gráfica 10 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 10: {e}")

    print("\n🔄 Generando gráfica 11: Mapa de calor de correlación...")
    try:
        results.append(plot_11_mapa_calor_correlacion(df, args.outdir))
        print("✅ Gráfica 11 completada")
    except Exception as e:
        print(f"⚠️  Error en gráfica 11: {e}")

    print("\n" + "="*60)
    print("✨ FIGURAS GENERADAS EXITOSAMENTE:")
    print("="*60)
    for r in results:
        print(f"  📊 {r}")
    print("="*60)


if __name__ == "__main__":
    main()
