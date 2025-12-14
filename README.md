# Road Collision Severity Prediction Project

## 🚗 Project Overview
Machine learning project to predict road collision severity using UK collision data, weather information, and population demographics.

## 📋 Prerequisites

### Required Software
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Required Python Packages
Install all dependencies using:
```bash
pip install -r requirements.txt
```

Key packages:
- `pandas`, `numpy` - Data manipulation
- `matplotlib`, `seaborn` - Visualization
- `sqlalchemy`, `psycopg2-binary` - Database connectivity
- `python-dotenv` - Environment variable management
- `scikit-learn`, `xgboost`, `lightgbm` - Machine learning
- `shap` - Model explainability

## 🔧 Setup Instructions

### 1. PostgreSQL Database Setup

Create the database in PostgreSQL:
```sql
CREATE DATABASE Uk_collision;
```

### 2. Environment Configuration

Create a `.env` file in the project root directory with your PostgreSQL credentials:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=Uk_collision
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
```

⚠️ **Important:** The `.env` file contains sensitive credentials and is already included in `.gitignore`. Never commit this file to version control.

### 3. Verify Database Connection

Test your PostgreSQL connection:
```bash
python upload_to_postgres.py
```

This script will:
- Test the database connection
- Display PostgreSQL version
- List all tables and row counts (if any exist)

### 4. Alternative Verification Scripts

Check database status:
```bash
python check_db.py
```

Check overall project status:
```bash
python check_status.py
```

## 📊 Data Files

Place the following CSV files in the `data/raw/` directory:
- `dft-road-casualty-statistics-collision-provisional-2025.csv` - Collision data
- `MET Office Weather Data.csv` - Weather data
- `gb.csv` - Population data

## 📓 Notebook Workflow

Run the notebooks in order:

### 1. `01_data_ingestion_profiling.ipynb`
- Connects to PostgreSQL database
- Loads raw CSV files
- Inserts data into `raw_collisions`, `raw_weather`, `raw_population` tables
- Performs initial data profiling and missing value analysis
- Generates visualizations

### 2. `02_deep_cleaning_transformation.ipynb`
- Cleans collision data (date/time conversion, null handling)
- Aggregates daily weather data
- Enriches with population data using spatial joins
- Creates `clean_collisions` and `weather_daily` tables

### 3. `03_eda_visualization.ipynb`
- Exploratory data analysis
- Generates comprehensive visualizations
- Analyzes patterns by time, location, and conditions

### 4. `04_feature_engineering.ipynb`
- Creates temporal features (hour, day, month, season)
- Categorical encoding
- Feature scaling and normalization
- Creates `feature_engineered_collisions` table

### 5. `05_ml_pipeline_training.ipynb`
- Train/test split with stratification
- Handles class imbalance using SMOTE
- Trains multiple models (Logistic Regression, Random Forest, XGBoost, LightGBM)
- Model evaluation and comparison
- Saves best model

### 6. `06_explainability_insights.ipynb`
- SHAP analysis for model interpretability
- Permutation importance
- Feature impact analysis
- Business insights and recommendations

## 🗄️ Database Schema

### Raw Tables
- `raw_collisions` - Original collision records
- `raw_weather` - Raw weather observations
- `raw_population` - UK city population data

### Processed Tables
- `clean_collisions` - Cleaned collision data with enrichments
- `weather_daily` - Aggregated daily weather metrics
- `feature_engineered_collisions` - ML-ready feature set

## 🔒 Security Notes

- Never commit `.env` file to version control
- Use strong PostgreSQL passwords
- Restrict database user permissions as needed
- Keep credentials secure and never share in plain text

## 📈 Expected Outputs

### Visualizations (PNG files in `images/` directory)
- `images/01_missing_values_collisions.png`
- `images/02_collision_severity_distribution.png`
- Additional EDA visualizations (images/03-17.png)

### Model Files
- Trained model pickle files
- Performance metrics and evaluation reports

## 🐛 Troubleshooting

### Database Connection Errors
```
Error: could not connect to server
```
**Solution:** Ensure PostgreSQL service is running:
- Windows: Check Services (services.msc)
- Linux/Mac: `sudo systemctl status postgresql`

### Authentication Failed
```
Error: password authentication failed
```
**Solution:** Verify credentials in `.env` file match your PostgreSQL user

### Module Not Found
```
ModuleNotFoundError: No module named 'psycopg2'
```
**Solution:** Install missing packages:
```bash
pip install -r requirements.txt
```

### Table Does Not Exist
```
Error: relation "raw_collisions" does not exist
```
**Solution:** Run notebook `01_data_ingestion_profiling.ipynb` first to create tables

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)

## 👥 Project Structure

```
testproject/
├── data/
│   └── raw/                          # Raw CSV data files
├── images/                           # Generated visualization outputs
├── .env                              # PostgreSQL credentials (not in git)
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
├── project_description.md            # Detailed project requirements
├── setup_database.py                 # Database creation script
├── upload_to_postgres.py             # Connection test script
├── check_db.py                       # Database verification
├── check_status.py                   # Project status checker
├── 01_data_ingestion_profiling.ipynb
├── 02_deep_cleaning_transformation.ipynb
├── 03_eda_visualization.ipynb
├── 04_feature_engineering.ipynb
├── 05_ml_pipeline_training.ipynb
└── 06_explainability_insights.ipynb
```

## ✅ Success Criteria

After completing all notebooks, you should have:
- ✓ All raw and processed tables in PostgreSQL
- ✓ 15+ visualization files
- ✓ Trained ML models with >80% accuracy
- ✓ SHAP analysis and feature importance insights
- ✓ Comprehensive evaluation metrics

---

**Note:** This project uses PostgreSQL for robust data management and scalability. All notebooks automatically connect using credentials from the `.env` file.
