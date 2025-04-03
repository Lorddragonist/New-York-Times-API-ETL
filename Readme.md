# NYT Articles ETL Pipeline

This project implements an ETL (Extract, Transform, Load) pipeline to fetch, process, and store articles from The New York Times API.

## Components

### 1. Extract (`extract.py`)
- Makes requests to the New York Times API
- Allows searching articles by keyword
- Implements API rate limiting (12 seconds between requests)
- Returns a list of JSONs containing article information

### 2. Transform (`transform.py`)
- Processes JSONs obtained from the API
- Extracts the following information from each article:
  - ID
  - Web URL
  - Abstract
  - Print section
  - Print page
  - Main headline
  - Multimedia count
  - Average height of multimedia elements
  - Median width of multimedia elements
  - Keywords count
  - Document type
  - Publication date
  - Word count
- Converts data into a pandas DataFrame

### 3. Load (`load.py`)
- Establishes connection with MySQL database
- Loads transformed data into a table named 'tb_nytimes_articles'
- Allows replacing existing data in the table

## Usage

### 1. Install Dependencies
```bash
pip install requests pandas numpy python-dotenv sqlalchemy pymysql
```
or
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Configure environment variables in the `.env` file

### 3. Running the ETL Process

#### Option 1: Using Python Scripts
```python
from ETL.extract import extract_data
from ETL.transform import transform_data
from ETL.load import load_data

# Extract data
jsons = extract_data("keyword", desired_article_count)

# Transform data
df = transform_data(jsons)

# Load data
load_data(df)
```

#### Option 2: Using Pipeline Notebook
The project includes a Jupyter notebook (`Pipeline.ipynb`) that demonstrates the complete ETL process:

1. The notebook sets up the necessary imports and path configurations
2. Defines parameters for article extraction (keyword and count)
3. Executes the ETL process step by step:
   - Extracts articles using the specified keyword
   - Transforms the raw data into a structured DataFrame
   - Loads the processed data into MySQL
4. Provides visual feedback on the progress of each step

Example notebook usage:
```python
# Set parameters
target_articles_count = 10
key_word = 'economy'

# Execute ETL
raw_data = extract_data(key_word, target_articles_count)
transformed_data = transform_data(raw_data)
load_data(transformed_data)
```

## Notes
- The NYT API has rate limits, so a 12-second delay is implemented between page requests
- Null values are handled appropriately in the transformation
- The MySQL table is completely replaced with each load
