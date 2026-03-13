# Adding Your Kaggle Dataset

## Step-by-Step Guide

### 1. Download from Kaggle
```bash
# Install Kaggle CLI (if not already installed)
pip install kaggle

# Download a specific dataset (replace with your dataset)
kaggle datasets download -d <username/dataset-name> -p data/

# Unzip if needed
unzip data/<dataset-name>.zip -d data/
```

### 2. Alternative: Manual Download
1. Go to the Kaggle dataset page
2. Click "Download"
3. Save the CSV file to your computer
4. Upload/copy it to the `data/` folder in this project

### 3. Update the Processing Script
Edit `scripts/data_processing.py` and change this line:
```python
success = processor.process('sample_sales_data.csv')
```
To:
```python
success = processor.process('your_dataset_filename.csv')
```

### 4. Handle Different Dataset Formats
The script automatically handles common column name variations:
- `Date` → `order_date`
- `Store` → `store_id`
- `Weekly_Sales` → `total_amount`
- etc.

### 5. Run the Processing
```bash
python3 scripts/data_processing.py
```

### 6. Validate Results
```bash
python3 scripts/validate_data.py
```

## Common Kaggle Sales Datasets

- **Walmart Sales**: `yasserh/walmart-dataset`
- **Retail Sales**: `mohammadtalib786/retails-dataset`
- **E-commerce Sales**: `carrie1/ecommerce-data`
- **Superstore Sales**: `bravehart101/sample-supermarket-dataset`

## Troubleshooting

- **Empty file**: Make sure the download completed successfully
- **Column errors**: Check the dataset structure and update column mappings in the script
- **Large files**: The script handles datasets with 1M+ rows efficiently

Once your dataset is in place, the processing pipeline will automatically adapt to its structure!