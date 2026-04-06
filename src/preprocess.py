import pandas as pd
import numpy as np
from typing import Union, List


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a DataFrame by removing duplicates, handling missing values, and trimming whitespace.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    # Convert any dict/list columns to strings first
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                # Check if column contains dicts or lists
                if any(isinstance(x, (dict, list)) for x in df[col] if x is not None):
                    df[col] = df[col].apply(lambda x: str(x) if x is not None else '')
            except:
                pass
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    
    # Remove rows where all values are NaN
    df = df.dropna(how='all')
    
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    
    return df.reset_index(drop=True)


def normalize_text(text: str) -> str:
    """
    Normalize text by removing extra whitespace and converting to lowercase.
    
    Args:
        text: Input text string
        
    Returns:
        Normalized text
    """
    if not isinstance(text, str):
        return text
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def preprocess_news_articles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess news articles DataFrame.
    
    Args:
        df: DataFrame with news articles
        
    Returns:
        Preprocessed DataFrame with combined content
    """
    df = clean_dataframe(df)
    
    # Normalize title and description
    if 'title' in df.columns:
        df['title'] = df['title'].apply(normalize_text)
    
    if 'description' in df.columns:
        df['description'] = df['description'].apply(normalize_text)
    
    if 'content' in df.columns:
        df['content'] = df['content'].apply(normalize_text)
    
    # Combine title, description, and content into a single text field
    df['combined_text'] = ''
    
    if 'title' in df.columns:
        df['combined_text'] += df['title'].fillna('') + ' '
    
    if 'description' in df.columns:
        df['combined_text'] += df['description'].fillna('') + ' '
    
    if 'content' in df.columns:
        df['combined_text'] += df['content'].fillna('')
    
    df['combined_text'] = df['combined_text'].apply(normalize_text)
    
    return df


def preprocess_company_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess company quote data.
    
    Args:
        df: DataFrame with company quote data
        
    Returns:
        Preprocessed DataFrame
    """
    df = clean_dataframe(df)
    
    # Convert numeric columns to proper types
    numeric_cols = ['price', 'marketCap', 'priceAvg50', 'priceAvg200', 'eps', 'pe']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def filter_by_date_range(df: pd.DataFrame, date_col: str, start_date, end_date) -> pd.DataFrame:
    """
    Filter DataFrame to only include rows within a date range.
    
    Args:
        df: Input DataFrame
        date_col: Name of the date column
        start_date: Start date
        end_date: End date
        
    Returns:
        Filtered DataFrame
    """
    if date_col not in df.columns:
        return df
    
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    mask = (df[date_col] >= start_date) & (df[date_col] <= end_date)
    
    return df[mask].reset_index(drop=True)


def combine_datasets(*dataframes: pd.DataFrame) -> pd.DataFrame:
    """
    Combine multiple DataFrames into one.
    
    Args:
        *dataframes: Variable number of DataFrames to combine
        
    Returns:
        Combined DataFrame
    """
    if not dataframes:
        return pd.DataFrame()
    
    combined = pd.concat(dataframes, ignore_index=True)
    
    return clean_dataframe(combined)
