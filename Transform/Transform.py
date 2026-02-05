"""🔄 MÓDULO DE TRANSFORMACIÓN DE DATOS

Este módulo es el TERCER PASO del pipeline ETL. Se encarga de TRANSFORMAR
datos limpios en información útil calculando métricas derivadas.

🎯 PROPÓSITO:
   Convertir datos crudos en métricas significativas que revelan patrones,
   tendencias y relaciones en la pandemia de COVID-19.

🔧 QUÉ HACE:
   1. Promedios móviles (suaviza fluctuaciones diarias)
   2. Tasas de crecimiento y mortalidad
   3. Agregaciones por fecha/estado/condado
   4. Rankings (top N más afectados)
   5. Matrices de correlación (qué variables se relacionan)
   6. Features temporales (año, mes, semana)
   7. Normalización de datos
   8. Detección y remoción de outliers

💡 EJEMPLO SIMPLE:
   ```python
   from Transform.Transform import DataTransformer
   import pandas as pd
   
   # Cargar datos limpios
   df = pd.read_csv("Output/IntegratedData_cleaned.csv")
   
   # Crear transformador
   transformer = DataTransformer(df)
   
   # Calcular promedio móvil de 7 días (elimina ruido)
   df_transformed = transformer.calculate_moving_average('daily_cases', window=7)
   
   # Calcular tasa de mortalidad (deaths/cases * 100)
   df_transformed = transformer.calculate_mortality_rate()
   
   # Obtener top 10 estados más afectados
   top_states = transformer.get_top_states('cases', n=10)
   ```

📊 FUNCIONES PRINCIPALES:
   - calculate_moving_average(): Suaviza series temporales
   - calculate_mortality_rate(): Calcula letalidad del virus
   - aggregate_by_date(): Suma nacional diaria
   - get_top_states(): Ranking de estados
   - calculate_correlation_matrix(): Relaciones entre variables
"""

from __future__ import annotations

from typing import Optional, List
import pandas as pd
import numpy as np

# ============================================================================
# IMPORTAR CONFIGURACIONES
# ============================================================================

try:
    # Importar constantes desde Config.py
    from Config.Config import (
        MOVING_AVERAGE_WINDOW,  # Ventana para promedio móvil (7 días)
        TOP_N_COUNTIES,         # Cuántos condados mostrar (10)
        TOP_N_STATES,           # Cuántos estados mostrar (10)
        MOBILITY_COLUMNS,       # Columnas de movilidad
        NUMERIC_COLUMNS         # Columnas numéricas
    )
except ImportError:
    # Si Config.py no existe, usar valores por defecto
    MOVING_AVERAGE_WINDOW = 7
    TOP_N_COUNTIES = 10
    TOP_N_STATES = 10
    MOBILITY_COLUMNS = ['retail_recreation', 'grocery_pharmacy', 'parks', 
                       'transit', 'workplaces', 'residential']
    NUMERIC_COLUMNS = ['cases', 'deaths', 'daily_cases', 'daily_deaths']


# ============================================================================
# CLASE PRINCIPAL: DataTransformer
# ============================================================================

class DataTransformer:
    """
    🔄 TRANSFORMADOR DE DATOS - Calcula métricas derivadas
    
    Esta clase toma datos limpios y calcula métricas útiles:
    - Promedios móviles (suaviza fluctuaciones)
    - Tasas de cambio (crecimiento, mortalidad)
    - Agregaciones (sumas por fecha/estado/condado)
    - Rankings (top N más afectados)
    - Correlaciones (qué variables se relacionan)
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        🏗️ CONSTRUCTOR - Inicializa el transformador
        
        Args:
            df: DataFrame con datos limpios (después de Clean.py)
        
        Qué hace:
            - Copia el DataFrame (no modifica el original)
            - Convierte columna 'date' a formato datetime si existe
        
        Ejemplo:
            >>> import pandas as pd
            >>> df = pd.read_csv("Output/IntegratedData_cleaned.csv")
            >>> transformer = DataTransformer(df)
        """
        # Hacer una COPIA del DataFrame (no modificar el original)
        self.df = df.copy()
        
        # Asegurar que la columna 'date' esté en formato correcto
        self._ensure_date_column()
    
    def _ensure_date_column(self):
        """
        🗓️ ASEGURAR FORMATO DE FECHA - Convierte 'date' a datetime
        
        Qué hace:
            - Busca si existe columna 'date'
            - La convierte a formato datetime de pandas
            - Si ya está en datetime, no hace nada
            - Si tiene errores, pone NaT (Not a Time)
        
        ¿Por qué es importante?
            - Facilita operaciones con fechas (filtrar, agrupar, ordenar)
            - Permite calcular diferencias entre fechas
            - Necesario para agregaciones temporales
        """
        if 'date' in self.df.columns:
            # Convertir a datetime
            # errors='coerce': Si falla, pone NaT en lugar de error
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
    
    def calculate_moving_average(self, 
                                 column: str, 
                                 window: int = None,
                                 center: bool = True) -> pd.DataFrame:
        """
        📈 PROMEDIO MÓVIL - Suaviza fluctuaciones diarias
        
        🎯 ¿QUÉ ES UN PROMEDIO MÓVIL?
           Es el promedio de los últimos N días. Elimina picos/valles
           artificiales (ej: menos reportes los fines de semana) y muestra
           la TENDENCIA REAL.
        
        📊 EJEMPLO VISUAL:
           Datos diarios:     100, 80, 90, 50, 60, 110, 95
           Promedio móvil 3:   -,  90, 90, 73, 66, 85,  88
                              (promedio de últimos 3 valores)
        
        ⚠️ USO TÍPICO:
           - window=7 (1 semana): Elimina efecto fin de semana
           - window=14 (2 semanas): Suavizado más agresivo
           - window=3 (3 días): Más sensible a cambios
        
        Args:
            column: Columna a suavizar (ej: 'daily_cases')
            window: Ventana en días (default: 7)
            center: Si True, centra la ventana (más preciso)
        Calcula promedio móvil para una columna.
        
        Args:
            column: Nombre de la columna
            window: Ventana del promedio (días)
            center: Si True, centra la ventana
            
        Returns:
            DataFrame con columna adicional de promedio móvil
        """
        window = window or MOVING_AVERAGE_WINDOW
        
        # Ordenar por fecha
        self.df = self.df.sort_values('date')
        
        # Calcular por grupo si hay county/state
        if 'county' in self.df.columns and 'state' in self.df.columns:
            self.df[f'{column}_ma{window}'] = (
                self.df.groupby(['county', 'state'])[column]
                .transform(lambda x: x.rolling(window=window, center=center).mean())
            )
        else:
            self.df[f'{column}_ma{window}'] = (
                self.df[column].rolling(window=window, center=center).mean()
            )
        
        print(f"✅ Promedio móvil calculado: {column}_ma{window}")
        return self.df
    
    def calculate_growth_rate(self, column: str = 'daily_cases') -> pd.DataFrame:
        """
        Calcula tasa de crecimiento diaria.
        
        Args:
            column: Columna para calcular crecimiento
            
        Returns:
            DataFrame con columna de tasa de crecimiento
        """
        self.df = self.df.sort_values('date')
        
        if 'county' in self.df.columns and 'state' in self.df.columns:
            self.df[f'{column}_growth_rate'] = (
                self.df.groupby(['county', 'state'])[column]
                .pct_change() * 100
            )
        else:
            self.df[f'{column}_growth_rate'] = self.df[column].pct_change() * 100
        
        print(f"✅ Tasa de crecimiento calculada: {column}_growth_rate")
        return self.df
    
    def calculate_mortality_rate(self) -> pd.DataFrame:
        """
        Calcula tasa de mortalidad (deaths / cases * 100).
        
        Returns:
            DataFrame con columna mortality_rate
        """
        self.df['mortality_rate'] = (
            (self.df['deaths'] / self.df['cases']) * 100
        ).replace([np.inf, -np.inf], np.nan)
        
        print("✅ Tasa de mortalidad calculada: mortality_rate")
        return self.df
    
    def aggregate_by_date(self, agg_dict: Optional[dict] = None) -> pd.DataFrame:
        """
        Agrega datos por fecha (nacional).
        
        Args:
            agg_dict: Diccionario de agregación personalizado
            
        Returns:
            DataFrame agregado por fecha
        """
        if agg_dict is None:
            agg_dict = {
                'cases': 'sum',
                'deaths': 'sum',
                'daily_cases': 'sum',
                'daily_deaths': 'sum'
            }
        
        df_agg = self.df.groupby('date').agg(agg_dict).reset_index()
        print(f"✅ Datos agregados por fecha: {len(df_agg)} fechas únicas")
        return df_agg
    
    def aggregate_by_state(self, agg_dict: Optional[dict] = None) -> pd.DataFrame:
        """
        Agrega datos por estado.
        
        Args:
            agg_dict: Diccionario de agregación personalizado
            
        Returns:
            DataFrame agregado por estado
        """
        if 'state' not in self.df.columns:
            raise ValueError("DataFrame no contiene columna 'state'")
        
        if agg_dict is None:
            agg_dict = {
                'cases': 'max',
                'deaths': 'max',
                'daily_cases': 'mean',
                'daily_deaths': 'mean'
            }
        
        df_agg = self.df.groupby('state').agg(agg_dict).reset_index()
        print(f"✅ Datos agregados por estado: {len(df_agg)} estados")
        return df_agg
    
    def aggregate_by_county(self, agg_dict: Optional[dict] = None) -> pd.DataFrame:
        """
        Agrega datos por condado.
        
        Args:
            agg_dict: Diccionario de agregación personalizado
            
        Returns:
            DataFrame agregado por condado y estado
        """
        if 'county' not in self.df.columns or 'state' not in self.df.columns:
            raise ValueError("DataFrame no contiene columnas 'county' y 'state'")
        
        if agg_dict is None:
            agg_dict = {
                'cases': 'max',
                'deaths': 'max',
                'daily_cases': 'mean',
                'daily_deaths': 'mean'
            }
        
        df_agg = self.df.groupby(['county', 'state']).agg(agg_dict).reset_index()
        print(f"✅ Datos agregados por condado: {len(df_agg)} condados")
        return df_agg
    
    def get_top_counties(self, metric: str = 'cases', n: int = None) -> pd.DataFrame:
        """
        Obtiene los top N condados por una métrica.
        
        Args:
            metric: Métrica para ordenar
            n: Número de condados a retornar
            
        Returns:
            DataFrame con top condados
        """
        n = n or TOP_N_COUNTIES
        
        df_agg = self.aggregate_by_county()
        df_top = df_agg.nlargest(n, metric)
        
        print(f"✅ Top {n} condados por {metric}")
        return df_top
    
    def get_top_states(self, metric: str = 'cases', n: int = None) -> pd.DataFrame:
        """
        Obtiene los top N estados por una métrica.
        
        Args:
            metric: Métrica para ordenar
            n: Número de estados a retornar
            
        Returns:
            DataFrame con top estados
        """
        n = n or TOP_N_STATES
        
        df_agg = self.aggregate_by_state()
        df_top = df_agg.nlargest(n, metric)
        
        print(f"✅ Top {n} estados por {metric}")
        return df_top
    
    def calculate_correlation_matrix(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Calcula matriz de correlación entre columnas numéricas.
        
        Args:
            columns: Lista de columnas a incluir (None = todas numéricas)
            
        Returns:
            DataFrame con matriz de correlación
        """
        if columns is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        else:
            numeric_cols = columns
        
        corr_matrix = self.df[numeric_cols].corr()
        print(f"✅ Matriz de correlación calculada: {len(numeric_cols)} variables")
        return corr_matrix
    
    def add_time_features(self) -> pd.DataFrame:
        """
        Agrega características temporales derivadas de la fecha.
        
        Returns:
            DataFrame con características temporales adicionales
        """
        if 'date' not in self.df.columns:
            raise ValueError("DataFrame no contiene columna 'date'")
        
        self._ensure_date_column()
        
        # Características temporales
        self.df['year'] = self.df['date'].dt.year
        self.df['month'] = self.df['date'].dt.month
        self.df['week'] = self.df['date'].dt.isocalendar().week
        self.df['day'] = self.df['date'].dt.day
        self.df['day_of_year'] = self.df['date'].dt.dayofyear
        self.df['quarter'] = self.df['date'].dt.quarter
        
        # Ya existe day_of_week en los datos originales, pero podemos verificar
        if 'day_of_week' not in self.df.columns:
            self.df['day_of_week'] = self.df['date'].dt.dayofweek
        
        print("✅ Características temporales agregadas")
        return self.df
    
    def normalize_column(self, column: str, method: str = 'minmax') -> pd.DataFrame:
        """
        Normaliza una columna numérica.
        
        Args:
            column: Nombre de la columna
            method: Método de normalización ('minmax' o 'zscore')
            
        Returns:
            DataFrame con columna normalizada
        """
        if column not in self.df.columns:
            raise ValueError(f"Columna '{column}' no encontrada")
        
        if method == 'minmax':
            min_val = self.df[column].min()
            max_val = self.df[column].max()
            self.df[f'{column}_normalized'] = (
                (self.df[column] - min_val) / (max_val - min_val)
            )
        elif method == 'zscore':
            mean_val = self.df[column].mean()
            std_val = self.df[column].std()
            self.df[f'{column}_normalized'] = (
                (self.df[column] - mean_val) / std_val
            )
        else:
            raise ValueError("Método debe ser 'minmax' o 'zscore'")
        
        print(f"✅ Columna normalizada: {column}_normalized (método: {method})")
        return self.df
    
    def filter_outliers(self, column: str, method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Filtra outliers de una columna.
        
        Args:
            column: Columna a filtrar
            method: Método ('iqr' o 'zscore')
            threshold: Umbral para detección
            
        Returns:
            DataFrame sin outliers
        """
        initial_len = len(self.df)
        
        if method == 'iqr':
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            self.df = self.df[
                (self.df[column] >= lower_bound) & 
                (self.df[column] <= upper_bound)
            ]
        elif method == 'zscore':
            z_scores = np.abs((self.df[column] - self.df[column].mean()) / self.df[column].std())
            self.df = self.df[z_scores < threshold]
        else:
            raise ValueError("Método debe ser 'iqr' o 'zscore'")
        
        removed = initial_len - len(self.df)
        print(f"✅ Outliers removidos: {removed:,} filas ({removed/initial_len*100:.2f}%)")
        return self.df
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Obtiene estadísticas resumidas del dataset.
        
        Returns:
            DataFrame con estadísticas descriptivas
        """
        stats = self.df.describe()
        print("✅ Estadísticas resumidas generadas")
        return stats


def transform_data(df: pd.DataFrame, operations: List[str] = None) -> pd.DataFrame:
    """
    Función de conveniencia para aplicar múltiples transformaciones.
    
    Args:
        df: DataFrame a transformar
        operations: Lista de operaciones a aplicar
        
    Returns:
        DataFrame transformado
    """
    transformer = DataTransformer(df)
    
    if operations is None:
        operations = ['moving_average', 'mortality_rate', 'time_features']
    
    if 'moving_average' in operations:
        transformer.calculate_moving_average('daily_cases')
        transformer.calculate_moving_average('daily_deaths')
    
    if 'mortality_rate' in operations:
        transformer.calculate_mortality_rate()
    
    if 'growth_rate' in operations:
        transformer.calculate_growth_rate('daily_cases')
    
    if 'time_features' in operations:
        transformer.add_time_features()
    
    return transformer.df


if __name__ == "__main__":
    print("="*60)
    print("MÓDULO DE TRANSFORMACIÓN DE DATOS")
    print("="*60)
    
    # Ejemplo con datos sintéticos
    print("\n📊 Creando datos de ejemplo...")
    dates = pd.date_range('2021-01-01', periods=30)
    df_example = pd.DataFrame({
        'date': dates,
        'county': ['Example'] * 30,
        'state': ['State'] * 30,
        'cases': np.cumsum(np.random.randint(10, 100, 30)),
        'deaths': np.cumsum(np.random.randint(0, 10, 30)),
        'daily_cases': np.random.randint(10, 100, 30),
        'daily_deaths': np.random.randint(0, 10, 30)
    })
    
    # Aplicar transformaciones
    print("\n🔄 Aplicando transformaciones...")
    transformer = DataTransformer(df_example)
    
    # Promedio móvil
    df_transformed = transformer.calculate_moving_average('daily_cases', window=7)
    
    # Tasa de mortalidad
    df_transformed = transformer.calculate_mortality_rate()
    
    # Características temporales
    df_transformed = transformer.add_time_features()
    
    print("\n📈 Datos transformados (primeras 5 filas):")
    print(df_transformed.head())
    
    print("\n" + "="*60)
