#!/usr/bin/env python3
"""
Data Validation Script

This script validates the processed sales data and generates
basic statistics and visualizations.

Usage:
    python validate_data.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

def load_processed_data(data_dir='data/processed'):
    """Load all processed Walmart data files."""
    files = {
        'main': 'processed_walmart_data.csv',
        'store_performance': 'store_performance.csv',
        'monthly': 'monthly_sales_summary.csv',
        'quarterly': 'quarterly_sales_summary.csv',
        'holiday': 'holiday_impact_analysis.csv',
        'economic': 'economic_factors_analysis.csv',
        'segments': 'customer_segment_analysis.csv',
        'kpis': 'kpi_overview.csv'
    }

    data = {}
    for key, filename in files.items():
        filepath = Path(data_dir) / filename
        if filepath.exists():
            data[key] = pd.read_csv(filepath)
            print(f"Loaded {key}: {len(data[key])} records")
        else:
            print(f"Warning: {filename} not found")

    return data

def validate_data_integrity(data):
    """Perform basic data integrity checks."""
    print("\n=== Data Integrity Validation ===")

    main_df = data.get('main')
    if main_df is not None:
        # Check for missing values
        missing = main_df.isnull().sum()
        if missing.sum() > 0:
            print("Missing values found:")
            print(missing[missing > 0])
        else:
            print("✓ No missing values in main dataset")

        # Check data types
        print(f"Data types:\n{main_df.dtypes}")

        # Basic statistics
        print(f"\nBasic Statistics:")
        print(f"Total Records: {len(main_df)}")
        print(f"Date Range: {main_df['order_date'].min()} to {main_df['order_date'].max()}")
        print(f"Total Revenue: ${main_df['total_amount'].sum():,.2f}")

def generate_basic_plots(data, output_dir='reports'):
    """Generate basic exploratory plots for Walmart data."""
    print("\n=== Generating Basic Plots ===")

    os.makedirs(output_dir, exist_ok=True)

    main_df = data.get('main')
    monthly_df = data.get('monthly')
    store_df = data.get('store_performance')
    holiday_df = data.get('holiday')

    if main_df is not None:
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")

        # Monthly sales trend
        plt.figure(figsize=(14, 7))
        if monthly_df is not None:
            plt.plot(monthly_df['period'], monthly_df['monthly_total_sales'], marker='o', linewidth=2)
            plt.title('Monthly Sales Trend - Walmart', fontsize=16, fontweight='bold')
            plt.xlabel('Period', fontsize=12)
            plt.ylabel('Monthly Sales ($)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/monthly_sales_trend.png', dpi=150, bbox_inches='tight')
            plt.close()
            print("✓ Monthly sales trend plot saved")

        # Store performance comparison
        if store_df is not None:
            plt.figure(figsize=(12, 8))
            top_stores = store_df.nlargest(10, 'total_sales')
            plt.barh(top_stores['store_id'].astype(str), top_stores['total_sales'])
            plt.title('Top 10 Stores by Total Sales', fontsize=16, fontweight='bold')
            plt.xlabel('Total Sales ($)', fontsize=12)
            plt.ylabel('Store ID', fontsize=12)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/top_stores_performance.png', dpi=150, bbox_inches='tight')
            plt.close()
            print("✓ Top stores performance plot saved")

        # Holiday vs Non-Holiday Sales
        if holiday_df is not None:
            plt.figure(figsize=(10, 6))
            holiday_labels = ['Non-Holiday Weeks', 'Holiday Weeks']
            plt.bar(holiday_labels, holiday_df['total_sales'])
            plt.title('Holiday vs Non-Holiday Sales Impact', fontsize=16, fontweight='bold')
            plt.ylabel('Total Sales ($)', fontsize=12)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/holiday_impact.png', dpi=150, bbox_inches='tight')
            plt.close()
            print("✓ Holiday impact plot saved")

        # Quarterly sales comparison
        quarterly_df = data.get('quarterly')
        if quarterly_df is not None:
            plt.figure(figsize=(12, 6))
            plt.bar(quarterly_df['period'], quarterly_df['quarterly_sales'])
            plt.title('Quarterly Sales Comparison', fontsize=16, fontweight='bold')
            plt.xlabel('Quarter', fontsize=12)
            plt.ylabel('Quarterly Sales ($)', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/quarterly_sales.png', dpi=150, bbox_inches='tight')
            plt.close()
            print("✓ Quarterly sales plot saved")

def main():
    """Main validation function."""
    print("Starting data validation...")

    # Load data
    data = load_processed_data()

    # Validate integrity
    validate_data_integrity(data)

    # Generate plots
    generate_basic_plots(data)

    print("\n✓ Data validation completed!")
    print("Check the reports/ directory for generated plots.")

if __name__ == "__main__":
    main()