
# Epiworld

**AI-Powered Epidemic Intelligence and Forecasting Platform**

Epiworld is an AI-powered epidemic intelligence and forecasting platform designed to analyze infectious disease trends, predict future cases and deaths, and support data-driven public health decisions.

The platform applies **seven machine learning models** across seven infectious diseases and 237+ countries. It integrates an AI assistant, **EpiGem**, powered by Groq LLaMA 3.1, to provide natural-language answers about platform data, forecasts, and methodology.

**Technology Stack:** Flask, Python, scikit-learn, TensorFlow/Keras, XGBoost, Chart.js, and Groq API.

> **Research and educational use only.**

---

## Objectives

- Forecast future case and death trends for different infectious diseases using multiple machine learning models.
- Automatically select the best-performing model for each disease through walk-forward validation.
- Present predictions through an intuitive dashboard with plain-language trend directions and qualitative confidence ratings.
- Allow users to upload their own epidemiological datasets in CSV, Excel, and JSON formats.
- Generate downloadable PDF reports based on uploaded data and model predictions.
- Provide an integrated AI assistant restricted to the platform's own data and methodology.

---

## Machine Learning Models

Epiworld integrates seven machine learning and deep learning approaches.

| Model | Category | Purpose |
|---|---|---|
| Random Forest | Ensemble Learning | Captures nonlinear relationships and complex disease trends |
| Ridge Regression | Linear Regression | Handles multicollinearity through L2 regularization |
| Lasso Regression | Linear Regression | Performs feature selection through L1 regularization |
| Support Vector Machine (SVM) | Machine Learning | Models nonlinear patterns using kernel-based learning |
| XGBoost | Gradient Boosting | Captures complex patterns through sequential boosting |
| LSTM | Deep Learning | Learns long-term temporal dependencies in epidemiological sequences |
| GRU | Deep Learning | Models sequential patterns with a computationally efficient recurrent architecture |

The platform evaluates the available models and automatically selects the best-performing model for each disease series using out-of-sample R².

---

## Supported Infectious Diseases

The bundled reference dataset covers seven infectious diseases:

1. COVID-19
2. AIDS/HIV
3. Malaria
4. Dengue
5. Measles
6. Hepatitis B
7. Polio

The dataset includes epidemiological information across **237+ countries**, covering the period from 1980 to 2024.

---

## Project Structure

```text
epiworld/
│
├── server.py
│   └── Flask application routes and HTTP request handling
│
├── config.py
│   └── Central environment-driven configuration
│
├── data_loader.py
│   └── Loads disease_data.json
│
├── ml_features.py
│   └── Feature engineering, walk-forward validation, and metrics
│
├── ml_models.py
│   └── Model training functions: run_sklearn() and run_rnn()
│
├── forecast_service.py
│   └── Series selection, model dispatch, and best-model selection
│
├── explainability.py
│   └── SHAP-based feature attribution for tree-based models
│
├── chatbot.py
│   └── EpiGem AI assistant, scope filtering, and local RAG fallback
│
├── disease_data.json
│   └── Bundled epidemiological reference dataset
│
├── requirements.txt
│   └── Project dependencies
│
├── .env.example
│   └── Example environment configuration
│
├── static/
│   ├── css/
│   │   └── main.css
│   │
│   ├── js/
│   │   └── dashboard.js
│   │
│   └── vendor/
│       └── Locally bundled frontend libraries
│
└── templates/
    ├── base.html
    ├── home.html
    ├── dashboard.html
    ├── upload.html
    └── about.html
```

Each module has a dedicated responsibility. Adding a new model primarily requires changes to `ml_models.py` and registration in `forecast_service.ALL_MODEL_NAMES`, without modifying the Flask routing layer.

---

## Installation

### Requirements

- Python 3.11 or Python 3.12
- pip package manager
- Internet connection for dependency installation

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd epiworld
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the environment:

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
cp .env.example .env
```

On Windows:

```powershell
copy .env.example .env
```

Open `.env` and add your Groq API key.

Obtain a key from:

https://console.groq.com

> The platform's core forecasting and dashboard functionality works without a Groq API key. The key is required for the Groq-powered EpiGem chatbot functionality.

### Installation Note

If TensorFlow or XGBoost fails to install on Windows, use the virtual environment described above rather than installing packages globally. This helps avoid Python dependency and version conflicts.

---

## Running the Application

Start the Flask application:

```bash
python server.py
```

The application runs locally at:

```text
http://127.0.0.1:5000
```

The console displays the server port and whether the EpiGem chatbot is enabled.

### Changing Host and Port

To change the host or port, update the following environment variables in `.env`:

```env
EPIWORLD_HOST=127.0.0.1
EPIWORLD_PORT=5000
```

Refer to the Configuration section for additional settings.

---

## Application Workflow

Epiworld is organized into four primary sections.

### 1. Home

The landing page provides:

- Interactive global disease map.
- Platform statistics.
- Overview of supported infectious diseases.
- General epidemic intelligence information.

### 2. Dashboard

The dashboard opens directly on the Live Summary screen.

The best-performing model is automatically selected and forecasting starts for the currently selected disease.

The dashboard includes the following sections:

| Dashboard Section | Functionality |
|---|---|
| Live Summary | Overall disease statistics and automatic forecasting |
| Trends & Overview | Historical epidemiological trends |
| Risk Map | Geographical visualization of disease distribution |
| Early Warning | Identification of potential future disease increases |
| Explainability | Model-derived feature importance and SHAP explanations |
| Simulation | Forecast scenario analysis |
| Forecast Settings | Manual selection of model and prediction horizon |

### 3. Upload Data

Users can upload their own epidemiological datasets in:

- CSV
- Excel
- JSON

The uploaded dataset undergoes preprocessing and forecasting using the same analytical pipeline.

The platform also generates a downloadable PDF report.

### 4. About

Provides information about:

- Platform methodology.
- Machine learning approaches.
- Data sources.
- Model evaluation.
- Contact information.

---

## Methodology

### 1. Data Preprocessing and Feature Engineering

Epidemiological time-series data undergoes preprocessing before model training.

- Large case and death counts are log-transformed to stabilize variance.
- Time-series features are generated for forecasting models.
- Lag, moving-average, momentum, and trend features are used where applicable.
- Leading zeros are trimmed before forecasting to avoid unnecessary zero-only periods.
- Uploaded datasets are validated and cleaned before model execution.

### 2. Machine Learning and Deep Learning

The platform implements two primary modelling approaches.

**Traditional Machine Learning**

- Random Forest
- Ridge Regression
- Lasso Regression
- Support Vector Machine
- XGBoost

These models use detrended and feature-engineered epidemiological time-series data.

Ridge Regression directly uses trend, lag, moving-average, and momentum features.

**Deep Learning**

- Long Short-Term Memory (LSTM)
- Gated Recurrent Unit (GRU)

Both recurrent neural network models use:

- Two recurrent layers.
- 64 units in the first layer.
- 32 units in the second layer.
- Dropout of 0.2.

These models are trained on raw sequential data for comparison.

### 3. Model Validation

The platform uses **Walk-Forward Cross-Validation** with six expanding-window folds.

This approach is preferred over ordinary random train/test splitting because epidemiological time-series data can be short and non-stationary.

Walk-forward validation ensures that future information is not introduced into the training process.

### 4. Automatic Model Selection

For each disease series:

1. All seven models are evaluated.
2. Out-of-sample R² is calculated.
3. Models are compared using their predictive performance.
4. The model with the highest test R² is selected as the default model.
5. When a series is too short for a genuine test fold, a discounted training R² is used as a fallback.

### 5. Forecast Interpretation

The dashboard presents predictions through understandable indicators instead of displaying raw statistical metrics to non-technical users.

**Trend Direction**

- Rising
- Falling
- Stable

**Forecast Confidence**

- High
- Moderate
- Limited

Raw evaluation metrics remain available through the JSON API for technical evaluation and reporting.

---

## Data Sources and Preprocessing

### Data Sources

The bundled epidemiological dataset integrates information from:

- World Health Organization (WHO)
- UNAIDS
- Our World in Data (OWID)

### Dataset Coverage

| Parameter | Coverage |
|---|---|
| Infectious Diseases | 7 |
| Countries | 237+ |
| Historical Period | 1980–2024 |
| Data Type | Epidemiological case and death statistics |
| Dataset File | `disease_data.json` |

### Data Preprocessing

**1. Leading-Zero Trimming**

Some diseases have years of zero-valued data before reporting begins for a particular country or region.

The platform removes these leading zeros before model training.

Zeros appearing after the series has started are retained as actual observations.

**2. Missing Values**

For uploaded datasets:

- Rows missing a year or case value are dropped.
- Non-numeric case and death values are converted to zero.
- The year column is validated before analysis.
- Uploads containing no parseable year values are rejected with a clear error message.

**3. Log Transformation**

A log transformation is automatically applied whenever the maximum absolute value of a series exceeds 1,000.

The transformation is reversed using `expm1` before returning results to the client.

Therefore, the API returns predictions in their original scale rather than log-scale values.

**4. Minimum Series Length**

At least three data points are required after trimming.

Series with fewer than eight data points trigger a small-sample warning in the dashboard.

COVID-19 in the bundled dataset has only five usable points after trimming. This limits the ability of traditional machine learning models to fit the series.

### Dataset Update Policy

`disease_data.json` is a static dataset snapshot captured at build time.

It is not a live epidemiological feed and does not have an automatic scheduled refresh mechanism.

Updating the reference data requires regenerating and replacing the JSON file.

---

## API Documentation

All endpoints return JSON responses.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/predict` | POST | Run one forecasting model for one disease |
| `/api/all_models` | POST | Run all seven models and return the best model with a full comparison |
| `/api/upload` | POST | Analyze uploaded CSV, Excel, or JSON data |
| `/api/chat-groq` | POST | EpiGem AI chat with local fallback |
| `/api/chat-status` | GET | Check whether the Groq chatbot is configured and reachable |
| `/api/explain/<model_name>` | POST | SHAP feature attribution for Random Forest and XGBoost |

### Example API Functions

**Single Model Forecasting**

```text
POST /api/predict
```

Runs one selected model for a specified infectious disease.

**Multiple Model Comparison**

```text
POST /api/all_models
```

Runs the available forecasting models and returns:

- Best-performing model.
- Forecast results.
- Model comparison.
- Training and testing metrics.

**Dataset Upload**

```text
POST /api/upload
```

Processes user-uploaded epidemiological data.

**AI Assistant**

```text
POST /api/chat-groq
```

Processes natural-language questions through EpiGem AI.

If Groq is unavailable or not configured, the assistant uses its local answer mechanism.

**Model Explainability**

```text
POST /api/explain/<model_name>
```

Provides SHAP-based feature attribution for Random Forest and XGBoost.

If SHAP is unavailable or the selected model is not tree-based, the API returns a structured response indicating that the explanation is unavailable.

### Model Evaluation Metrics

All ML endpoints return the following metrics in their JSON responses:

- R² Score
- Root Mean Squared Error (RMSE)
- Mean Absolute Error (MAE)
- Mean Absolute Percentage Error (MAPE)
- Akaike Information Criterion (AIC)

These metrics are available for technical evaluation and reporting even though they are not directly displayed in the dashboard.

---

## EpiGem AI Assistant

**EpiGem** is the integrated AI-powered assistant designed to answer questions related to the Epiworld platform.

It uses Groq LLaMA 3.1 for natural-language responses.

### Key Capabilities

- Answers questions about supported infectious diseases.
- Explains epidemiological forecasting results.
- Provides information about model selection and methodology.
- Helps users understand disease trends.
- Explains platform functionality.
- Restricts responses to platform-related information.

### Architecture

The assistant includes:

1. Scope filtering to restrict unrelated questions.
2. Groq LLaMA 3.1 integration for AI-generated responses.
3. Local RAG-based fallback for situations where Groq is unavailable.
4. Platform-specific context to ground responses in available data.

---

## Configuration

All configuration settings are maintained in `config.py` and loaded through environment variables.

| Variable | Default | Purpose |
|---|---|---|
| `GROQ_API_KEY` | Empty | API key for EpiGem AI chat |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Groq model name |
| `EPIWORLD_HOST` | `127.0.0.1` | Flask bind host |
| `EPIWORLD_PORT` | `5000` | Flask bind port |
| `EPIWORLD_DEBUG` | `false` | Flask debug mode |
| `EPIWORLD_DEFAULT_HORIZON` | `5` | Default forecast horizon in years |
| `EPIWORLD_MAX_HORIZON` | `20` | Maximum API forecast horizon in years |

> **Security:** Never commit `.env` or expose API keys in source control. Only `.env.example` containing placeholder values should be committed.

---

## Frontend Libraries

The frontend uses locally bundled JavaScript libraries rather than relying on external CDNs.

| Library | Purpose | Version |
|---|---|---|
| Chart.js | Data visualization and charts | 4.4.1 |
| D3.js | Interactive data visualization | 7.8.5 |
| topojson-client | Geographic data processing | 3.x |
| world-atlas | Country boundary visualization | Bundled |
| jsPDF | PDF report generation | 2.5.1 |
| html2canvas | HTML-to-image conversion | 1.4.1 |

These libraries are stored locally in `static/vendor/`.

This improves reliability when internet access is restricted or external CDNs are unavailable.

---

## Auto-Load Forecast Performance

Opening the Dashboard automatically triggers forecasting for the default disease.

For diseases with very short historical series, traditional machine learning models may fail, requiring the two recurrent neural network models (LSTM and GRU) to run.

For a five-point series such as the bundled COVID-19 dataset, automatic forecasting may take approximately 16–20 seconds on a typical machine.

### Performance Optimization

The platform uses two optimizations:

1. **Fast Auto-Load Mode:** The automatic dashboard forecast uses fewer training epochs (30 instead of 100) and fewer Monte Carlo dropout passes (8 instead of 20). Explicit Run Forecast and Run All Models actions continue to use full-quality settings.

2. **Training Indicator:** The dashboard displays an animated "Training forecast models..." indicator while models are running.

This helps users distinguish active model training from a frozen page.

---

## Known Limitations

- Diseases with very few historical data points may cause traditional machine learning models to fail during training.
- In such cases, `/api/all_models` returns the models that successfully completed training rather than guaranteeing all seven results.
- For extremely short series, such as the five usable COVID-19 observations in the bundled dataset, LSTM and GRU may predict values approaching zero at later forecast horizons.
- The bundled `disease_data.json` is a static snapshot and not a live epidemiological feed.
- SHAP explanations are implemented only for Random Forest and XGBoost.
- Ridge, Lasso, SVM, LSTM, and GRU use the existing model-derived Feature Weights panel instead.
- Forecast confidence is limited by the quantity, quality, and historical coverage of the available data.

The dashboard communicates short-series limitations through its small-sample warning and Limited confidence rating rather than hiding them.

---

## Evaluation Report

The project includes a separately generated evaluation artifact:

`Epiworld_Model_Evaluation_Report.xlsx`

This workbook contains the full walk-forward-validated evaluation metrics for every model and disease combination.

### Evaluation Metrics

- R²
- RMSE
- MAE
- MAPE
- AIC

The evaluation report is generated separately from the runtime application.

It can be regenerated by calling `forecast_service.predict_all()` for each disease in `data_loader.DISEASE_DATA` and exporting the resulting dictionaries.

The report provides a consolidated technical evaluation while keeping the primary dashboard focused on understandable epidemiological trends and forecast confidence.

---

## License and Use

**Research and educational use only.**

The platform is intended for academic research, experimentation, and educational purposes.

It is a forecasting and decision-support tool and should not be interpreted as a substitute for official public health surveillance, epidemiological investigation, or professional public health decisions.

---

**Epiworld — Understand Disease Trends. Forecast the Future. Support Public Health Intelligence.**
