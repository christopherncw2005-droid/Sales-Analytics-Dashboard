# Sales Analytics Dashboard

## Business Context

This project develops a comprehensive sales analytics dashboard for Walmart to gain actionable insights from their weekly sales data across 45 stores. The dashboard will help stakeholders understand store performance, seasonal trends, holiday impacts, economic factors, and identify opportunities for revenue growth and operational improvements.

## Project Overview

## Project Overview

- **Tech Stack**: Python (pandas) for data processing + BI tools (PowerBI)
- **Dataset**: Walmart Sales Dataset (Kaggle) - Weekly sales data for 45 stores from 2010-2012
- **Data Structure**: 6,435 weekly records with sales, holiday flags, temperature, fuel prices, CPI, and unemployment data
- **Key Deliverables**:
  - SQL queries for data preparation and aggregation
  - Interactive dashboard with 5-7 key performance indicators (KPIs)
  - Prescriptive insights and recommended actions
  - Comprehensive documentation

## Project Structure

```
├── data/              # Raw and processed datasets
├── scripts/           # Python data processing scripts
├── queries/           # SQL queries for data preparation
├── dashboards/        # BI tool files and exports
├── reports/           # Analysis reports and insights
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## KPIs to Track

### Store Performance
1. **Total Revenue**: $6.7B across all stores and time periods
2. **Average Weekly Sales**: $1.05M per store per week
3. **Store Performance Ranking**: Top vs bottom performing stores
4. **Sales Volatility**: Week-to-week sales variation by store

### Seasonal & Temporal Analysis
5. **Monthly Sales Trends**: Seasonal patterns and growth rates
6. **Quarterly Performance**: Q4 vs other quarters analysis
7. **Holiday Impact**: Sales uplift during holiday weeks

### Economic Factors
- Temperature correlation with sales
- Fuel price impact analysis
- CPI and unemployment effects
- Customer segment analysis (synthetic segments based on sales volume)

## Prescriptive Insights Framework

The analysis will provide actionable recommendations in areas such as:
- Product pricing optimization
- Inventory management
- Marketing campaign targeting
- Customer retention strategies
- Seasonal trend analysis