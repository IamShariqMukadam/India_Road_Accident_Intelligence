# ============================================================
# NOTEBOOK 03 — TIME SERIES FORECASTING WITH PROPHET
# Forecast India road accident + fatality trends 2025-2027
# ============================================================

# %% CELL 1 — Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

CLEAN = '../data/cleaned'
OUTPUT = '../outputs'

import os
os.makedirs(OUTPUT, exist_ok=True)
print("Imports OK")

# %% CELL 2 — Prepare national yearly data
state_master = pd.read_csv(f'{CLEAN}/state_master.csv')

national = state_master.groupby('year').agg(
    accidents=('accidents', 'sum'),
    fatalities=('fatalities', 'sum')
).reset_index()

print("National yearly data:")
print(national.to_string(index=False))

# %% CELL 3 — IMPORTANT: Understand what Prophet needs
# Prophet requires columns named EXACTLY 'ds' (date) and 'y' (value)
# ds must be a datetime — we use Jan 1 of each year
# With 6 data points (2019-2024), confidence intervals will be wide
# That is NORMAL and HONEST — we document this clearly

national['ds'] = pd.to_datetime(national['year'].astype(str) + '-01-01')

accidents_df = national[['ds', 'accidents']].rename(columns={'accidents': 'y'})
fatalities_df = national[['ds', 'fatalities']].rename(columns={'fatalities': 'y'})

print("\nProphet input format (accidents):")
print(accidents_df)

# %% CELL 4 — Forecast ACCIDENTS
model_acc = Prophet(
    yearly_seasonality=False,   # no within-year seasonality (annual data)
    weekly_seasonality=False,
    daily_seasonality=False,
    changepoint_prior_scale=0.05,   # conservative — prevents overfitting on 6 points
    uncertainty_samples=500,
    interval_width=0.80            # 80% confidence interval (more honest than 95% on 6pts)
)
model_acc.fit(accidents_df)

# Forecast 3 years ahead: 2025, 2026, 2027
future_acc = model_acc.make_future_dataframe(periods=3, freq='YE')
forecast_acc = model_acc.predict(future_acc)

print("\nAccident forecast 2025-2027:")
forecast_tail = forecast_acc[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(3)
forecast_tail['ds'] = forecast_tail['ds'].dt.year
forecast_tail.columns = ['Year', 'Forecast', 'Lower Bound', 'Upper Bound']
forecast_tail = forecast_tail.round(0).astype(int)
print(forecast_tail.to_string(index=False))

# %% CELL 5 — Forecast FATALITIES
model_fat = Prophet(
    yearly_seasonality=False,
    weekly_seasonality=False,
    daily_seasonality=False,
    changepoint_prior_scale=0.05,
    uncertainty_samples=500,
    interval_width=0.80
)
model_fat.fit(fatalities_df)

future_fat = model_fat.make_future_dataframe(periods=3, freq='YE')
forecast_fat = model_fat.predict(future_fat)

print("\nFatality forecast 2025-2027:")
forecast_fat_tail = forecast_fat[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(3)
forecast_fat_tail['ds'] = forecast_fat_tail['ds'].dt.year
forecast_fat_tail.columns = ['Year', 'Forecast', 'Lower Bound', 'Upper Bound']
forecast_fat_tail = forecast_fat_tail.round(0).astype(int)
print(forecast_fat_tail.to_string(index=False))

# Extract 2026 forecast for README
fat_2026 = forecast_fat[forecast_fat['ds'].dt.year == 2026].iloc[0]
print(f"\nKEY NUMBER: Projected 2026 fatalities = {int(fat_2026['yhat']):,}")
print(f"Range: {int(fat_2026['yhat_lower']):,} to {int(fat_2026['yhat_upper']):,}")

# %% CELL 6 — Plot both forecasts in one figure (publication quality)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor('#0f0f1a')

def plot_forecast(ax, national_df, forecast_df, metric, color, title):
    actual_years = national_df['ds'].dt.year
    actual_vals  = national_df['y']

    all_years = pd.to_datetime(forecast_df['ds']).dt.year
    forecast_only = forecast_df[all_years > 2024]

    ax.set_facecolor('#1a1a2e')

    # Historical line
    ax.plot(actual_years, actual_vals,
            color=color, linewidth=2.5, marker='o',
            markersize=8, zorder=5, label='Actual (2019-2024)')

    # COVID annotation
    ax.annotate('COVID\ndip', xy=(2020, national_df[national_df['ds'].dt.year==2020]['y'].values[0]),
                xytext=(2020.3, national_df[national_df['ds'].dt.year==2020]['y'].values[0] * 1.08),
                fontsize=9, color='#aaa',
                arrowprops=dict(arrowstyle='->', color='#aaa', lw=1))

    # Forecast line
    forecast_years = pd.to_datetime(forecast_only['ds']).dt.year
    ax.plot(forecast_years, forecast_only['yhat'],
            color=color, linewidth=2, linestyle='--',
            marker='s', markersize=7, zorder=5, label='Forecast (2025-2027)')

    # Confidence band
    ax.fill_between(forecast_years,
                    forecast_only['yhat_lower'],
                    forecast_only['yhat_upper'],
                    alpha=0.25, color=color, label='80% Confidence Interval')

    # Bridge from 2024 actual to 2025 forecast
    last_actual_val = actual_vals.iloc[-1]
    first_forecast_year = forecast_years.iloc[0]
    first_forecast_val  = forecast_only['yhat'].iloc[0]
    ax.plot([2024, first_forecast_year], [last_actual_val, first_forecast_val],
            color=color, linewidth=2, linestyle='--', alpha=0.6)

    # Vertical divider
    ax.axvline(x=2024.5, color='white', linestyle=':', alpha=0.4, linewidth=1)
    ax.text(2024.6, ax.get_ylim()[1]*0.97, 'Forecast →',
            color='white', fontsize=9, alpha=0.6)

    ax.set_title(title, color='white', fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel('Year', color='#aaa', fontsize=11)
    ax.set_ylabel(metric, color='#aaa', fontsize=11)
    ax.tick_params(colors='#aaa')
    ax.spines[['bottom','left']].set_color('#444')
    ax.spines[['top','right']].set_visible(False)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=9)
    ax.grid(axis='y', color='#333', alpha=0.5)

plot_forecast(ax1, accidents_df, forecast_acc, 'Total Accidents',
              '#4fc3f7', 'Road Accident Forecast — India 2025-2027')
plot_forecast(ax2, fatalities_df, forecast_fat, 'Total Fatalities',
              '#ef5350', 'Fatality Forecast — India 2025-2027')

plt.suptitle(
    'India Road Accident Trend & Forecast\n'
    'Based on MoRTH Data 2019–2024 | Prophet Model | 80% Confidence Interval',
    color='white', fontsize=13, y=1.01
)
plt.tight_layout()
plt.savefig(f'{OUTPUT}/forecast_chart.png', dpi=150, bbox_inches='tight',
            facecolor='#0f0f1a')
plt.show()
print("Forecast chart saved: outputs/forecast_chart.png")

# %% CELL 7 — State-Level Trend Analysis (bonus — no ML needed)
# Which states show consistent multi-year upward/downward fatality trend?
# Use linear regression slope per state as a trend score

from scipy import stats as sp_stats

state_trends = []
for state, grp in state_master.groupby('state'):
    grp = grp.sort_values('year').dropna(subset=['fatalities'])
    if len(grp) < 4:
        continue
    slope, intercept, r, p, se = sp_stats.linregress(grp['year'], grp['fatalities'])
    state_trends.append({
        'state': state,
        'slope': round(slope, 1),          # fatalities added per year
        'r_squared': round(r**2, 3),       # how linear the trend is
        'p_value': round(p, 4),
        'significant': p < 0.05
    })

trends_df = pd.DataFrame(state_trends).sort_values('slope', ascending=False)
trends_df.to_csv(f'{OUTPUT}/state_fatality_trends.csv', index=False)

print("\nTop 5 WORSENING states (highest annual fatality increase):")
print(trends_df[trends_df['significant']].head(5)[
    ['state','slope','r_squared','p_value']].to_string(index=False))

print("\nTop 5 IMPROVING states (decreasing fatalities):")
print(trends_df[trends_df['significant']].tail(5)[
    ['state','slope','r_squared','p_value']].to_string(index=False))

# %% CELL 8 — Plot state trend ranking
fig, ax = plt.subplots(figsize=(12, 10))
ax.set_facecolor('#1a1a2e')
fig.patch.set_facecolor('#0f0f1a')

plot_df = trends_df[trends_df['significant']].sort_values('slope')
colors = ['#ef5350' if s > 0 else '#66bb6a' for s in plot_df['slope']]

ax.barh(plot_df['state'], plot_df['slope'], color=colors, edgecolor='none')
ax.axvline(x=0, color='white', linewidth=1, alpha=0.6)
ax.set_title('Fatality Trend by State — Annual Change (2019-2024)\nRed = Worsening | Green = Improving',
             color='white', fontsize=13, fontweight='bold')
ax.set_xlabel('Average Annual Change in Fatalities', color='#aaa')
ax.tick_params(colors='#aaa')
ax.spines[['top','right']].set_visible(False)
ax.spines[['bottom','left']].set_color('#444')
ax.grid(axis='x', color='#333', alpha=0.5)

plt.tight_layout()
plt.savefig(f'{OUTPUT}/state_fatality_trends.png', dpi=150, bbox_inches='tight',
            facecolor='#0f0f1a')
plt.show()
print("State trend chart saved: outputs/state_fatality_trends.png")

# %%
