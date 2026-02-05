"""Módulo de transformación de datos.

Este módulo contiene funciones para transformar, agregar y calcular
métricas derivadas a partir de los datos limpios de COVID-19.
"""

from __future__ import annotations

from typing import Optional, List
import pandas as pd
import numpy as np

# Importar configuración si está disponible
try:
    from Config.Config import (
        MOVING_AVERAGE_WINDOW, TOP_N_COUNTIES, TOP_N_STATES,
        MOBILITY_COLUMNS, NUMERIC_COLUMNS
    )
except ImportError:
    MOVING_AVERAGE_WINDOW = 7
    TOP_N_COUNTIES = 10
    TOP_N_STATES = 10
    MOBILITY_COLUMNS = ['retail_recreation', 'grocery_pharmacy', 'parks', 
                       'transit', 'workplaces', 'residential']
    NUMERIC_COLUMNS = ['cases', 'deaths', 'daily_cases', 'daily_deaths']


class DataTransformer:
    """Clase para transformar y enriquecer datos de COVID-19."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el transformador con un DataFrame.
        
        Args:
            df: DataFrame con datos limpios
        """
        self.df = df.copy()
        self._ensure_date_column()
    
    def _ensure_date_column(self):
        """Asegura que la columna date esté en formato datetime."""
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
    
    def calculate_moving_average(self, 
                                 column: str, 
                                 window: int = None,
                                 center: bool = True) -> pd.DataFrame:
        """
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
