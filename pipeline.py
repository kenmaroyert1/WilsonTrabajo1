"""Pipeline ETL completo para análisis de datos COVID-19.

Este script integra todos los módulos del proyecto para ejecutar el pipeline completo:
Extract → Clean → Transform → Load → Visualize
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional
import pandas as pd

# Agregar directorio raíz al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importar módulos
try:
    from Config.Config import (
        DATA_DIR, OUTPUT_DIR, FIGURES_DIR,
        ensure_directories, get_config_summary
    )
    from Extract.Extract import DataExtractor
    from Extract.Clean.Clean import clean_csv
    from Transform.Transform import DataTransformer
    from Load.Load import DataLoader
    print("✅ Módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)


class COVIDPipeline:
    """Pipeline completo para procesamiento de datos COVID-19."""
    
    def __init__(self, input_file: str = "IntegratedData.csv"):
        """
        Inicializa el pipeline.
        
        Args:
            input_file: Nombre del archivo de entrada
        """
        self.input_file = DATA_DIR / input_file
        self.cleaned_file = OUTPUT_DIR / "IntegratedData_cleaned.csv"
        self.transformed_file = OUTPUT_DIR / "IntegratedData_transformed.csv"
        
        # Verificar que existe el archivo
        if not self.input_file.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {self.input_file}")
        
        # Crear directorios
        ensure_directories()
        
        print("="*70)
        print(" 🚀 PIPELINE ETL COVID-19 - INICIADO")
        print("="*70)
        print(f"📁 Archivo de entrada: {self.input_file.name}")
        print(f"📊 Tamaño: {self.input_file.stat().st_size / (1024**2):.2f} MB")
        print("="*70)
    
    def step1_extract(self, method: str = 'chunks') -> pd.DataFrame:
        """
        Paso 1: Extracción de datos.
        
        Args:
            method: Método de extracción ('full', 'chunks', 'sample')
            
        Returns:
            DataFrame extraído
        """
        print("\n" + "="*70)
        print("📥 PASO 1: EXTRACCIÓN DE DATOS")
        print("="*70)
        
        extractor = DataExtractor(self.input_file)
        
        if method == 'full':
            df = extractor.extract_full()
        elif method == 'chunks':
            print("⚠️ Modo chunks requiere procesamiento iterativo")
            print("   Ejecutando limpieza directamente...")
            return None  # Se procesa en step2
        elif method == 'sample':
            df = extractor.extract_sample(frac=0.1)
        else:
            raise ValueError(f"Método no válido: {method}")
        
        if df is not None:
            print(f"✅ Datos extraídos: {len(df):,} filas, {len(df.columns)} columnas")
        
        return df
    
    def step2_clean(self) -> pd.DataFrame:
        """
        Paso 2: Limpieza de datos.
        
        Returns:
            DataFrame limpio
        """
        print("\n" + "="*70)
        print("🧹 PASO 2: LIMPIEZA DE DATOS")
        print("="*70)
        
        # Usar función de limpieza que procesa en chunks
        clean_csv(str(self.input_file), str(self.cleaned_file))
        
        # Cargar datos limpios
        print("\n📂 Cargando datos limpios...")
        df_clean = pd.read_csv(self.cleaned_file)
        
        print(f"✅ Datos limpios: {len(df_clean):,} filas, {len(df_clean.columns)} columnas")
        return df_clean
    
    def step3_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Paso 3: Transformación de datos.
        
        Args:
            df: DataFrame limpio
            
        Returns:
            DataFrame transformado
        """
        print("\n" + "="*70)
        print("🔄 PASO 3: TRANSFORMACIÓN DE DATOS")
        print("="*70)
        
        transformer = DataTransformer(df)
        
        # Aplicar transformaciones
        print("\n📊 Aplicando transformaciones...")
        
        # 1. Promedios móviles
        print("\n1️⃣ Calculando promedios móviles...")
        transformer.calculate_moving_average('daily_cases', window=7)
        transformer.calculate_moving_average('daily_deaths', window=7)
        
        # 2. Tasa de mortalidad
        print("\n2️⃣ Calculando tasa de mortalidad...")
        transformer.calculate_mortality_rate()
        
        # 3. Tasa de crecimiento
        print("\n3️⃣ Calculando tasa de crecimiento...")
        transformer.calculate_growth_rate('daily_cases')
        
        # 4. Características temporales
        print("\n4️⃣ Agregando características temporales...")
        transformer.add_time_features()
        
        df_transformed = transformer.df
        print(f"\n✅ Transformaciones completadas")
        print(f"   Columnas originales: {len(df.columns)}")
        print(f"   Columnas finales: {len(df_transformed.columns)}")
        print(f"   Nuevas columnas: {len(df_transformed.columns) - len(df.columns)}")
        
        return df_transformed
    
    def step4_load(self, df: pd.DataFrame) -> None:
        """
        Paso 4: Carga de datos transformados.
        
        Args:
            df: DataFrame transformado
        """
        print("\n" + "="*70)
        print("💾 PASO 4: CARGA DE DATOS")
        print("="*70)
        
        loader = DataLoader()
        
        # Guardar datos transformados
        print("\n1️⃣ Guardando CSV transformado...")
        loader.save_to_csv(df, 'IntegratedData_transformed.csv')
        
        # Guardar metadatos
        print("\n2️⃣ Guardando metadatos...")
        metadata = {
            'description': 'Datos COVID-19 transformados con métricas derivadas',
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'date_range': {
                'start': str(df['date'].min()),
                'end': str(df['date'].max())
            },
            'transformations_applied': [
                'moving_average_7d',
                'mortality_rate',
                'growth_rate',
                'time_features'
            ]
        }
        loader.save_metadata('IntegratedData_transformed.csv', metadata)
        
        # Crear backup del archivo original limpio
        print("\n3️⃣ Creando backup...")
        try:
            loader.create_backup('IntegratedData_cleaned.csv')
        except FileNotFoundError:
            print("   ⚠️ No se pudo crear backup (archivo no encontrado)")
        
        print("\n✅ Datos cargados exitosamente")
    
    def step5_analyze(self, df: pd.DataFrame) -> dict:
        """
        Paso 5: Análisis y agregaciones.
        
        Args:
            df: DataFrame transformado
            
        Returns:
            Diccionario con resultados de análisis
        """
        print("\n" + "="*70)
        print("📊 PASO 5: ANÁLISIS Y AGREGACIONES")
        print("="*70)
        
        transformer = DataTransformer(df)
        
        results = {}
        
        # 1. Agregación nacional
        print("\n1️⃣ Agregación nacional por fecha...")
        df_nacional = transformer.aggregate_by_date()
        results['nacional'] = df_nacional
        print(f"   {len(df_nacional):,} fechas únicas")
        
        # 2. Top estados
        print("\n2️⃣ Top 10 estados por casos...")
        df_top_states = transformer.get_top_states('cases', n=10)
        results['top_states'] = df_top_states
        print(f"   Top estado: {df_top_states.iloc[0]['state']} ({df_top_states.iloc[0]['cases']:,} casos)")
        
        # 3. Top condados
        print("\n3️⃣ Top 10 condados por casos...")
        df_top_counties = transformer.get_top_counties('cases', n=10)
        results['top_counties'] = df_top_counties
        print(f"   Top condado: {df_top_counties.iloc[0]['county']}, {df_top_counties.iloc[0]['state']}")
        
        # 4. Estadísticas resumidas
        print("\n4️⃣ Estadísticas descriptivas...")
        stats = transformer.get_summary_statistics()
        results['statistics'] = stats
        
        # 5. Matriz de correlación
        print("\n5️⃣ Matriz de correlación...")
        corr_matrix = transformer.calculate_correlation_matrix()
        results['correlation'] = corr_matrix
        
        print("\n✅ Análisis completado")
        return results
    
    def run_full_pipeline(self, save_intermediate: bool = True) -> pd.DataFrame:
        """
        Ejecuta el pipeline completo.
        
        Args:
            save_intermediate: Si guardar resultados intermedios
            
        Returns:
            DataFrame final transformado
        """
        print("\n🚀 Ejecutando pipeline completo...")
        
        try:
            # Paso 2: Limpieza (incluye extracción en chunks)
            df_clean = self.step2_clean()
            
            # Paso 3: Transformación
            df_transformed = self.step3_transform(df_clean)
            
            # Paso 4: Carga
            self.step4_load(df_transformed)
            
            # Paso 5: Análisis
            analysis_results = self.step5_analyze(df_transformed)
            
            # Guardar agregaciones si se solicita
            if save_intermediate:
                loader = DataLoader()
                print("\n💾 Guardando agregaciones...")
                loader.save_to_csv(analysis_results['nacional'], 'agregado_nacional.csv')
                loader.save_to_csv(analysis_results['top_states'], 'top_estados.csv')
                loader.save_to_csv(analysis_results['top_counties'], 'top_condados.csv')
            
            print("\n" + "="*70)
            print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
            print("="*70)
            print(f"📊 Filas procesadas: {len(df_transformed):,}")
            print(f"📁 Archivos generados en: {OUTPUT_DIR}")
            print(f"📈 Visualizaciones en: {FIGURES_DIR}")
            print("="*70)
            
            return df_transformed
            
        except Exception as e:
            print("\n" + "="*70)
            print(f"❌ ERROR EN PIPELINE: {e}")
            print("="*70)
            raise


def main():
    """Función principal para ejecutar el pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Pipeline ETL completo para datos COVID-19'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='IntegratedData.csv',
        help='Archivo de entrada'
    )
    parser.add_argument(
        '--skip-intermediate',
        action='store_true',
        help='No guardar archivos intermedios'
    )
    parser.add_argument(
        '--show-config',
        action='store_true',
        help='Mostrar configuración y salir'
    )
    
    args = parser.parse_args()
    
    # Mostrar configuración si se solicita
    if args.show_config:
        print(get_config_summary())
        return
    
    # Ejecutar pipeline
    pipeline = COVIDPipeline(input_file=args.input)
    df_final = pipeline.run_full_pipeline(save_intermediate=not args.skip_intermediate)
    
    print("\n🎉 Pipeline ejecutado correctamente!")
    print(f"📊 DataFrame final: {len(df_final):,} filas x {len(df_final.columns)} columnas")


if __name__ == "__main__":
    main()
