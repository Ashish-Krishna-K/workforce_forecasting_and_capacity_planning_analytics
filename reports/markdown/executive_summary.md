
# Executive Summary

## Project Overview

This project demonstrates an end-to-end workforce forecasting and capacity planning workflow using synthetically generated operational workforce management data. The analysis covers the complete lifecycle from data generation and exploratory analysis through forecasting, capacity planning, and workforce scenario modeling.

The objective was to evaluate future workload demand, estimate workforce requirements, assess staffing risks, and provide data-driven recommendations for workforce planning decisions.

---

# Phase 1 – Synthetic Data Generation

## Objective

Generate realistic operational workforce management data representing a customer support environment.

## Datasets Generated

### Workload Data

* Daily transaction volumes
* Queue-level demand
* Average Handle Time (AHT)
* Trend effects
* Monthly seasonality
* Day-of-week seasonality

### Workforce Data

* Scheduled FTE
* Available FTE
* Staffing plans

### Shrinkage Data

* Shrinkage percentage

## Business Value

The generated datasets provide a realistic environment for performing workforce forecasting and capacity planning analyses without relying on proprietary operational data.

---

# Phase 2 – Exploratory Data Analysis

## Key Findings

### Workload Demand

* Total workload volume increased by **3.12%** from 2024 to 2025.
* Q4 consistently generated the highest workload volumes.
* December represented the peak demand period.
* Workload patterns demonstrated clear seasonality.

### Queue Analysis

* Customer Service contributed **36.34%** of total workload volume.
* Escalations contributed **4.55%** of total workload volume.
* Customer Service and Billing represented the majority of operational demand.

### Seasonality

* Monday generated the highest average daily volume.
* Sunday generated the lowest average daily volume.
* Strong weekly seasonality was observed.

### Average Handle Time

* Escalations recorded the highest average handling time (**696.89 seconds**).
* AHT remained relatively stable throughout the week.
* No significant day-level AHT seasonality was observed.

### Shrinkage

* Shrinkage remained stable across most months.
* December exhibited elevated shrinkage levels.
* Seasonal shrinkage increases coincided with peak workload periods.

### Workforce Implications

* Demand seasonality should be incorporated into forecasting models.
* Queue-level AHT differences significantly impact staffing requirements.
* December represents a critical planning period requiring additional staffing preparedness.

---

# Phase 3 – Forecasting

## Objective

Forecast future workload demand for 2026 using historical workload data.

## Models Evaluated

### Moving Average

* 7-Day Rolling Average

### Holt-Winters Exponential Smoothing

* Multiplicative Trend
* Multiplicative Seasonality
* Seasonal Period = 7

### Linear Regression

Features:

* Day Index
* Day-of-Week Indicators
* Month Indicators

## Key Findings

* Linear Regression achieved the strongest forecasting performance.
* Forecast accuracy reached a **MAPE of 4.97%**.
* Holt-Winters achieved **7.20% MAPE**.
* Moving Average achieved **25.53% MAPE**.

## Business Implications

* Demand patterns are strongly influenced by calendar-based seasonality.
* Historical demand trends can be effectively modeled using simple and interpretable forecasting techniques.
* Forecast outputs provide a reliable foundation for workforce planning decisions.

## Outcome

The Linear Regression model was selected and used to generate daily workload forecasts for the full year of 2026.

---

# Phase 4 – Capacity Planning

## Objective

Translate forecasted workload demand into workforce requirements.

## Key Findings

### Demand Forecast

* Average daily volume: **3,554.51**
* Peak daily volume: **5,265.64**
* Lowest daily volume: **1,492.35**

### Workload Hours

* Average daily workload: **472.87 hours**
* Peak daily workload: **698.57 hours**

### Workforce Requirements

#### Raw Requirement

* Average: **59.11 FTE**
* Peak: **87.32 FTE**

#### Shrinkage Adjusted Requirement

* Average: **85.16 FTE**
* Peak: **129.98 FTE**

### Shrinkage Impact

* Average additional staffing requirement: **26.05 FTE**
* Shrinkage increased workforce requirements by approximately **44%** on average.

### Seasonal Workforce Demand

Highest Staffing Requirement:

1. December
2. November
3. June

Lowest Staffing Requirement:

1. August
2. July
3. February

### Operational Insights

* Staffing requirements vary significantly throughout the year.
* Seasonal workload increases create substantial workforce demand spikes.
* Shrinkage materially impacts workforce planning outcomes and cannot be ignored during staffing calculations.

---

# Phase 5 – Workforce Scenario Modeling

## Objective

Evaluate workforce coverage and staffing risk under alternative workforce availability scenarios.

## Scenarios Evaluated

### Attrition Scenario

* Workforce Availability: -15%

### Baseline Scenario

* Historical Workforce Availability

### Hiring Scenario

* Workforce Availability: +15%

## Scenario Summary

| Scenario  | Avg Available FTE | Avg Required FTE | Avg Gap | Avg Coverage |
| --------- | ----------------- | ---------------- | ------- | ------------ |
| Attrition | 60.68             | 84.77            | -24.08  | 77.31%       |
| Baseline  | 71.39             | 84.77            | -13.37  | 90.96%       |
| Hiring    | 82.10             | 84.77            | -2.66   | 104.60%      |

## Key Findings

### Attrition Risk

* Critical Risk Days: **241**
* Average staffing deficit: **24.08 FTE**
* Coverage reduced to **77.31%**

### Baseline Performance

* Historical staffing levels fail to fully support forecasted demand.
* Average staffing deficit remains **13.37 FTE**.

### Hiring Benefits

* Average coverage improves to **104.60%**.
* Critical Risk Days reduced from **135 to 32**.
* Staffing deficit reduced to **2.66 FTE**.

### Seasonal Risk

* Worst coverage date: **29 June 2026**
* Best coverage date: **04 January 2026**
* September produced the lowest average monthly coverage.
* January produced the highest average monthly coverage.

---

# Major Business Risks

## Workforce Attrition

The Attrition scenario demonstrated that modest workforce reductions can create substantial operational risk.

Potential impacts:

* Service level degradation
* Increased workload per employee
* Higher burnout risk
* Reduced customer satisfaction

## Seasonal Demand Peaks

Demand surges during Q4 and December significantly increase staffing requirements.

Potential impacts:

* Understaffing
* Increased backlog
* Reduced service performance

## Shrinkage Risk

Shrinkage increased workforce requirements by approximately 26 FTE on average.

Potential impacts:

* Underestimation of staffing needs
* Scheduling inefficiencies
* Capacity shortages

---

# Recommendations

## 1. Increase Workforce Capacity

The Hiring scenario consistently produced the strongest operational outcomes.

Recommendation:

* Increase staffing capacity by approximately 15% ahead of forecasted demand growth.

## 2. Improve Shrinkage Management

Recommendation:

* Review meetings, training schedules, and non-productive activities to improve workforce availability.

## 3. Prepare for Seasonal Peaks

Recommendation:

* Implement seasonal workforce planning ahead of Q4 demand increases.

## 4. Monitor Workforce Risk Indicators

Recommendation:

Track:

* Coverage Percentage
* Staffing Gap
* Shrinkage
* Workforce Availability

through ongoing workforce planning dashboards.

---

# Final Conclusion

This project demonstrates how forecasting, capacity planning, and scenario modeling can be integrated into a workforce planning framework capable of supporting staffing decisions and operational risk assessments.

The analysis showed that workforce demand exhibits clear seasonal behavior, staffing requirements are heavily influenced by shrinkage assumptions, and workforce availability remains a key driver of operational performance.

Among the evaluated workforce strategies, increasing staffing availability produced the most favorable outcomes, while workforce attrition created significant operational risk. These findings highlight the importance of proactive workforce planning and demonstrate how data analytics can support workforce management decision-making.
