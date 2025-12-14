
---

### 5.2 Section B – Data Ingestion (Member 1)

**Objectives:**
- Load raw files (collisions, weather, population) into pandas.
- Basic sanity checks.
- Insert into PostgreSQL `raw_*` tables.

**Key Tasks:**
- `pd.read_csv` / `pd.read_excel` for all three datasets.
- Display `.head()`, `.info()`, `.describe()` for each.
- Use `df.to_sql('raw_collisions', engine, if_exists='replace', index=False)` etc.
- Confirm row counts using SQL queries from the notebook.

**Outputs / Files:**
- None (just DB side effects).

---

### 5.3 Section C – Initial Data Profiling (Member 1)

**Objectives:**
- Understand missingness and basic distributions.
- Produce early EDA plots.

**Key Tasks:**
- Query `raw_collisions`, `raw_weather`, `raw_population` back into pandas.
- Null counts per column.
- Plot:
  - Bar chart for missing counts in collisions: `01_missing_values_collisions.png`.
  - Bar chart for `collision_severity` distribution: `02_collision_severity_distribution.png`.

---

### 5.4 Section D – Deep Cleaning & Transformation (Member 2)

**Objectives:**
- Clean collision data
- Build daily weather
- Prepare population subset and spatial enrichment

**Key Tasks:**

#### Collisions Cleaning
- Type conversions:
  - `date` → `datetime`
  - `time` → `datetime` or minutes since midnight
- Drop rows with:
  - Missing `collision_severity`
  - Invalid `longitude`/`latitude` (e.g., 0 or extreme out-of-UK values)
- Write cleaned version to `clean_collisions`.

#### Weather Daily Interpolation
- Read `raw_weather`.
- Convert `year`, `month` to a datetime (monthly index).
- For each `station`:
  - Construct a continuous date range across months.
  - Interpolate to daily values:
    - `tmax`, `tmin`: `interpolate(method='cubic')` or `linear`
    - `rain`, `sun`, `af`: linear or forward/backward fill + smoothing
- Build `weather_daily` with `station`, `date`, daily metrics.
- Insert into `weather_daily` table.

#### Population / City Filter & Enrichment
- Read `raw_population`.
- Filter to relevant area (e.g., `country == "United Kingdom"` or another logic).
- Keep fields: `city`, `lat`, `lng`, `population`.
- Use `KDTree` on city coordinates.
- For each collision (lat/lng):
  - Find nearest city and distance.
  - Add `nearest_city`, `nearest_city_population`, `distance_to_city_km`.

- Save enriched collisions back to DB (append columns in `clean_collisions` or new stage).

---

### 5.5 Section E – EDA & Visualization (Member 2)

**Objectives:**
- Explore trends and relationships.
- Generate high-quality, labeled plots.

**Required Analyses / Plots:**

1. **Number of vehicles vs severity**
   - Boxplot or violin plot.
   - Save: `03_vehicles_vs_severity.png`.

2. **Number of casualties vs severity**
   - Save: `04_casualties_vs_severity.png`.

3. **Severity vs time of day**
   - E.g., average severity or severity distribution over `hour_of_day` (temporary feature).
   - Save: `05_severity_by_hour.png`.

4. **Severity vs day of week**
   - Barplot or heatmap.
   - Save: `06_severity_by_dayofweek.png`.

5. **Weather impact**
   - Severity rate vs `rain`, `temp_mean`, `frost_days`.
   - Save: `07_weather_impact.png`.

6. **Urban vs rural severity**
   - Compare `urban_or_rural_area`.
   - Save: `08_urban_rural_severity.png`.

7. **Correlation heatmap**
   - For numeric variables of interest.
   - Save: `09_correlation_heatmap.png`.

Plots must include:
- Clear titles
- Axis labels
- Legends where needed

---

### 5.6 Section F – Feature Engineering (Member 2 & 3)

**Objectives:**
- Create rich features combining time, weather, geography, and road context.
- Produce final dataset for modeling.

**Feature List:**

#### Temporal Features
- `hour_of_day` (0–23) from `time`
- `day_of_week` (1–7)
- `is_weekend` (0/1)
- `month` (1–12)
- `season` (categorical: Winter, Spring, Summer, Autumn)
- `is_rush_hour` (0/1) – define morning + evening rush windows

#### Weather Features
- `temp_mean` = (tmax + tmin)/2
- `temp_range` = tmax - tmin
- `rain_mm` = daily rainfall
- `is_frost_day` (1 if `af > 0`)
- `rain_category` (e.g., `none`, `light`, `medium`, `heavy`)

#### Geographic Features
- `nearest_city_population`
- `log_population` = log(1 + population)
- `distance_to_city_km`
- `urban_or_rural_area` recoded to simpler categories if needed

#### Road / Collision Features
- `speed_limit`
- `speed_limit_band` (e.g., <=30, 40–50, 60–70, >70)
- `number_of_vehicles`
- `number_of_casualties`
- `has_pedestrian_crossing` (from pedestrian crossing fields)
- Encoded versions of:
  - `road_type`
  - `junction_detail`
  - `light_conditions`
  - `weather_conditions`
  - `first_road_class` etc.

#### Interaction Features (at least 3)
- `speed_limit * number_of_vehicles`
- `is_rush_hour * rain_mm`
- `urban_or_rural_area * speed_limit_band` (encoded numeric product)

**Deliverable:**
- Final pandas DataFrame `df_features`:
  - `collision_id`
  - `collision_severity`
  - All engineered features
  - No missing values
- Persist as `feature_engineered_collisions` in PostgreSQL.

---

## 6. ML Pipeline

### 6.1 Section G – Data Preparation for ML (Member 3)

**Objectives:**
- Train-test split
- Encoding & scaling
- Imbalance handling

**Tasks:**
- Load `feature_engineered_collisions` into pandas.
- Define input features `X` and target `y = collision_severity`.
- Perform `train_test_split(test_size=0.2, stratify=y, random_state=42)`.
- Encode categorical variables:
  - Use `OneHotEncoder` or `OrdinalEncoder` within a `ColumnTransformer`.
- Scale numeric features with `StandardScaler` (fit on train, transform both train & test).
- Apply `SMOTE` to the training set only.
- Plot class distribution before and after SMOTE:
  - Save `10_class_distribution_before_after_smote.png`.

---

### 6.2 Section H – Model Training (Member 3)

**Objectives:**
- Train multiple models
- Compare performance
- Build an ensemble

**Models:**

1. **Baselines**
   - `DummyClassifier(strategy="most_frequent")`
   - `LogisticRegression` (regularized)

2. **Random Forest**
   - Example hyperparameters:
     - `n_estimators=300`
     - `max_depth` tuned
     - `class_weight="balanced"`
   - Stratified 5-fold cross-validation.

3. **XGBoost Classifier**
   - Tuned (`max_depth`, `learning_rate`, `n_estimators`, `subsample`, `colsample_bytree`).
   - Early stopping on validation set if feasible.

4. **LightGBM Classifier**
   - Similar tuning as XGB for depth, leaves, learning rate.

5. **Voting Ensemble**
   - `VotingClassifier` with RF + XGBoost + LightGBM (soft voting).

**Metrics (per model):**
- Accuracy
- Precision (macro, weighted)
- Recall (macro, weighted)
- F1-score (macro, weighted)
- ROC-AUC (macro, weighted, if probabilities available)

**Visual Outputs:**
- Bar chart comparing models by selected metric(s):
  - `11_model_metric_comparison.png`.
- Confusion matrices for 2–3 key models (RF, XGB, ensemble):
  - `12_confusion_matrices.png`.
- ROC curves for multiple models:
  - `13_roc_curves.png`.

**Persistence:**
- For each model and metric, write rows into `model_metrics`.
- For best model (chosen by primary metric, e.g., `f1_macro`), write predictions into `model_predictions`.

---

## 7. Explainability

### 7.1 Section I – Permutation Importance (Member 3)

**Objectives:**
- Model-agnostic feature importance.

**Tasks:**
- Use `sklearn.inspection.permutation_importance` on the best model.
- Compute importance on the test set.
- Plot top 15 features as horizontal bar chart:
  - Save `14_permutation_importance.png`.
- Insert importance values into `feature_importance` with `importance_type="permutation"`.

---

### 7.2 Section J – SHAP Analysis (Member 3)

**Objectives:**
- Global and local explanations via SHAP.

**Tasks:**
- Initialize `shap.TreeExplainer` with the best tree-based model.
- Compute SHAP values on a **subset** of test data (e.g., 2000 rows).
- Generate and save:

1. SHAP summary bar plot:
   - `15_shap_summary_bar.png`.

2. SHAP beeswarm plot:
   - `16_shap_summary_beeswarm.png`.

3. 2–3 SHAP dependence plots (for top features):
   - Files like `17_shap_dependence_temp_mean.png`, etc.

4. (Optional) SHAP force plot for 1–2 sample collisions:
   - Save as `18_shap_force_example.png` (if feasible as PNG).

- Insert subset of SHAP values into `shap_samples`.

---

## 8. Insights & Reporting Support

### 8.1 Section K – Insight Tables (Member 3)

**Objectives:**
- Prepare quantitative summaries for the written report.

**Tasks:**
- Compute:
  - Severity rates by `hour_of_day`.
  - Severity rates by `is_frost_day`.
  - Severity rates by `urban_or_rural_area`.
  - Severity vs `speed_limit_band`.

- Extract SHAP-based ranking of top 10 features (mean absolute SHAP value).
- Display these as pandas DataFrames in the notebook.
- These tables will be used directly in the report (copied/converted to LaTeX/IEEE format).

---

## 9. Non-Functional Requirements

- **Single Notebook:** All logic in `road_collision_severity.ipynb`.
- **Image Outputs:** All figures saved as `.png` in notebook root using `save_fig(...)`.
- **Reproducibility:**  
  - Running all cells from top to bottom should complete without manual edits (assuming DB reachable).
  - Random seeds set for reproducibility.
- **Performance:**  
  - End-to-end runtime should be reasonable on a typical laptop; if not, subsampling for SHAP is allowed.
- **Code Quality:**
  - Clear markdown headings for each section and subsection.
  - Comments for non-trivial logic.
  - Functions used where logic is complex (e.g. KDTree enrichment, interpolation).

---

## 10. Team Responsibilities (Code Only)

**Member 1 – Data Collection & Initial Cleaning**
- Sections: A, B, C, early part of D
- Owns:
  - File loading
  - Raw → PostgreSQL
  - Basic cleaning
  - Initial profiling

**Member 2 – Deep Cleaning, EDA & Feature Engineering**
- Sections: rest of D, E, F
- Owns:
  - Weather interpolation
  - Geographic enrichment
  - Deep cleaning
  - EDA plots
  - Feature engineering

**Member 3 – ML & Explainability**
- Sections: G, H, I, J, K
- Owns:
  - Preprocessing + SMOTE
  - Models + evaluation
  - Explainability (SHAP, permutation importance)
  - Insights tables

---

## 11. Next Steps

1. Create the notebook skeleton:
   - Add all markdown headings as outlined above.
   - Add empty code cells beneath each heading.
2. Implement sections in order:
   - Member 1 starts with A–C, then D base.
   - Member 2 builds on that for D–F.
   - Member 3 implements G–K once `feature_engineered_collisions` is ready.
3. After implementation:
   - Run the full notebook end-to-end.
   - Verify:
     - All DB tables exist and populated.
     - All PNGs exist in root.
     - No cell errors.

This markdown file defines the **full technical scope** of the project’s code implementation in one notebook with PostgreSQL and saved images.
