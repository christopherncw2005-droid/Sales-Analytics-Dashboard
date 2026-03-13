#!/usr/bin/env python3
"""
Walmart Sales Data Processing Script

This script processes Walmart weekly sales data and prepares it for analysis
and dashboard creation in BI tools like Looker Studio, Tableau, or PowerBI.

Dataset Structure:
- Store: Store number (1-45)
- Date: Week ending date (MM-DD-YYYY format)
- Weekly_Sales: Sales amount for the week
- Holiday_Flag: Whether it's a holiday week (0 or 1)
- Temperature: Temperature in Fahrenheit
- Fuel_Price: Fuel price
- CPI: Consumer Price Index
- Unemployment: Unemployment rate

Usage:
    python data_processing.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SalesDataProcessor:
    def __init__(self, data_dir='data', output_dir='data/processed'):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def load_data(self, filename):
        """Load raw sales data from CSV file."""
        file_path = self.data_dir / filename
        logger.info(f"Loading data from {file_path}")

        # Load Walmart data with specific date format (DD-MM-YYYY)
        df = pd.read_csv(file_path, parse_dates=['Date'], date_format='%d-%m-%Y')

        # Standardize column names to lowercase with underscores
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('/', '_')

        # Handle Walmart-specific column mappings
        column_mappings = {
            'store': 'store_id',
            'date': 'order_date',
            'weekly_sales': 'total_amount',
            'holiday_flag': 'is_holiday',
            'temperature': 'temperature',
            'fuel_price': 'fuel_price',
            'cpi': 'cpi',
            'unemployment': 'unemployment_rate'
        }

        df = df.rename(columns=column_mappings)

        logger.info(f"Loaded {len(df)} weekly store records")
        return df

        logger.info(f"Loaded {len(df)} rows of data")
        return df

    def clean_data(self, df):
        """Clean and preprocess the Walmart sales data."""
        logger.info("Cleaning Walmart data...")

        # Remove duplicates
        df = df.drop_duplicates()

        # Handle missing values - keep records with essential fields
        df = df.dropna(subset=['store_id', 'order_date', 'total_amount'])

        # Create unique order/transaction IDs for each store-week combination
        df['order_id'] = 'ORD_' + df['store_id'].astype(str) + '_' + df['order_date'].dt.strftime('%Y%m%d')

        # For aggregated weekly data, we don't have individual customer transactions
        # Create synthetic customer segments based on store performance
        df['customer_segment'] = pd.cut(df['total_amount'],
                                      bins=[0, 500000, 1000000, 2000000, float('inf')],
                                      labels=['Low_Value', 'Medium_Value', 'High_Value', 'Premium_Value'])

        # Since this is aggregated data, we'll treat each store-week as a "transaction"
        # with quantity representing estimated number of items sold
        if 'quantity' not in df.columns:
            # Estimate quantity based on sales amount (rough approximation for retail)
            df['quantity'] = (df['total_amount'] / 75).round().astype(int)  # Assume avg item price ~$75

        # Calculate average price per item
        df['price'] = df['total_amount'] / df['quantity']

        # Add location data (Walmart stores are primarily in USA)
        df['country'] = 'USA'

        # Extract date features
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.month
        df['order_week'] = df['order_date'].dt.isocalendar().week
        df['order_quarter'] = df['order_date'].dt.quarter
        df['is_holiday_week'] = df['is_holiday'].astype(bool)

        logger.info(f"Data cleaned. Shape: {df.shape}")
        return df

        logger.info(f"Data cleaned. Shape: {df.shape}")
        return df

    def calculate_kpis(self, df):
        """Calculate key performance indicators for Walmart data."""
        logger.info("Calculating Walmart KPIs...")

        # Overall metrics
        total_revenue = df['total_amount'].sum()
        total_stores = df['store_id'].nunique()
        total_weeks = df['order_date'].nunique()
        avg_weekly_sales = total_revenue / len(df)

        # Store performance metrics
        store_performance = df.groupby('store_id').agg({
            'total_amount': ['sum', 'mean', 'std', 'count'],
            'is_holiday': 'sum'
        }).reset_index()
        store_performance.columns = ['store_id', 'total_sales', 'avg_weekly_sales',
                                   'sales_volatility', 'weeks_recorded', 'holiday_weeks']

        # Seasonal analysis (monthly)
        monthly_sales = df.groupby(['order_year', 'order_month'])['total_amount'].agg(['sum', 'mean', 'count']).reset_index()
        monthly_sales['period'] = monthly_sales['order_year'].astype(str) + '-' + monthly_sales['order_month'].astype(str).str.zfill(2)
        monthly_sales.columns = ['order_year', 'order_month', 'monthly_total_sales', 'avg_weekly_sales', 'weeks_in_month', 'period']

        # Holiday impact analysis
        holiday_sales = df.groupby('is_holiday')['total_amount'].agg(['sum', 'mean', 'count']).reset_index()
        holiday_sales.columns = ['is_holiday', 'total_sales', 'avg_weekly_sales', 'weeks_count']

        # Quarterly analysis
        quarterly_sales = df.groupby(['order_year', 'order_quarter'])['total_amount'].agg(['sum', 'mean']).reset_index()
        quarterly_sales['period'] = quarterly_sales['order_year'].astype(str) + '-Q' + quarterly_sales['order_quarter'].astype(str)
        quarterly_sales.columns = ['order_year', 'order_quarter', 'quarterly_sales', 'avg_weekly_sales', 'period']

        # Economic factors correlation (if available)
        economic_factors = df.groupby(['order_year', 'order_month']).agg({
            'total_amount': 'mean',
            'temperature': 'mean',
            'fuel_price': 'mean',
            'cpi': 'mean',
            'unemployment_rate': 'mean'
        }).reset_index()

        # Customer segment analysis (synthetic segments based on sales volume)
        segment_analysis = df.groupby('customer_segment')['total_amount'].agg(['sum', 'mean', 'count']).reset_index()
        segment_analysis.columns = ['segment', 'total_sales', 'avg_sales', 'weeks_count']

        kpis = {
            'total_revenue': total_revenue,
            'total_stores': total_stores,
            'total_weeks': total_weeks,
            'avg_weekly_sales': avg_weekly_sales,
            'store_performance': store_performance,
            'monthly_sales': monthly_sales,
            'quarterly_sales': quarterly_sales,
            'holiday_sales': holiday_sales,
            'economic_factors': economic_factors,
            'segment_analysis': segment_analysis
        }

        return kpis

    def save_processed_data(self, df, kpis):
        """Save processed Walmart data and KPIs for BI tool consumption."""
        logger.info("Saving processed Walmart data...")

        # Save main processed dataset
        df.to_csv(self.output_dir / 'processed_walmart_data.csv', index=False)

        # Save KPI summaries
        kpis['store_performance'].to_csv(self.output_dir / 'store_performance.csv', index=False)
        kpis['monthly_sales'].to_csv(self.output_dir / 'monthly_sales_summary.csv', index=False)
        kpis['quarterly_sales'].to_csv(self.output_dir / 'quarterly_sales_summary.csv', index=False)
        kpis['holiday_sales'].to_csv(self.output_dir / 'holiday_impact_analysis.csv', index=False)
        kpis['economic_factors'].to_csv(self.output_dir / 'economic_factors_analysis.csv', index=False)
        kpis['segment_analysis'].to_csv(self.output_dir / 'customer_segment_analysis.csv', index=False)

        # Save KPI overview
        kpi_overview = pd.DataFrame({
            'kpi_name': ['Total Revenue', 'Total Stores', 'Total Weeks', 'Average Weekly Sales'],
            'value': [
                kpis['total_revenue'],
                kpis['total_stores'],
                kpis['total_weeks'],
                kpis['avg_weekly_sales']
            ]
        })
        kpi_overview.to_csv(self.output_dir / 'kpi_overview.csv', index=False)

        logger.info("Processed Walmart data saved successfully")

    def process(self, filename):
        """Main processing pipeline."""
        try:
            # Load data
            df = self.load_data(filename)

            # Clean data
            df_clean = self.clean_data(df)

            # Calculate KPIs
            kpis = self.calculate_kpis(df_clean)

            # Save results
            self.save_processed_data(df_clean, kpis)

            logger.info("Data processing completed successfully!")
            return True

        except Exception as e:
            logger.error(f"Error during processing: {str(e)}")
            return False

if __name__ == "__main__":
    # Initialize processor
    processor = SalesDataProcessor()

    # Process the data (update filename as needed)
    # Note: Using Walmart.csv dataset
    success = processor.process('Walmart.csv')

    if success:
        print("Data processing completed. Check the data/processed/ directory for output files.")
    else:
        print("Data processing failed. Check the logs for details.")