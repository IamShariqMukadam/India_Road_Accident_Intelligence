# ============================================================
# NOTEBOOK 04 — STATISTICAL CORRELATION + REGRESSION
# Find statistically significant relationships in accident data
# ============================================================

# %% CELL 1 — Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats as sp_stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import warnings
warnings.filterwarnings('ignore')

CLEAN = '../data/cleaned'
OUTPUT = '../outputs'

import os
os.makedirs(OUTPUT, exist_ok=True)
print("Imports OK")

# %% CELL 2 — Load data
state_master = pd.read_csv(f'{CLEAN}/state_master.csv')
latest = state_master[state_master['year'] == 2024].dropna(
    subset=['accidents','fatalities','fatality_rate_per_accident']
).copy()

# Remove tiny UTs (< 500 accidents) — they distort correlations with extreme rates
latest_filtered = latest[latest['accidents'] >= 500].copy()
print(f"States after filtering tiny UTs: {len(latest_filtered)}")
print(latest_filtered[['state','accidents','fatalities',
                        'fatality_rate_per_accident']].head(8))

# %% CELL 3 — Engineer features for correlation analysis
# From state_master we have: accidents, fatalities, fatality_rate_per_accident
# Derive log transforms (handles skewness in accident counts)
latest_filtered['log_accidents']  = np.log(latest_filtered['accidents'])
latest_filtered['log_fatalities'] = np.log(latest_filtered['fatalities'])

# Accident share = this state's % of national accidents
total_accidents_2024 = latest_filtered['accidents'].sum()
latest_filtered['accident_share_pct'] = (
    latest_filtered['accidents'] / total_accidents_2024 * 100
).round(3)

# YoY changes already in state_master
latest_filtered['yoy_accident_change']  = latest_filtered['yoy_accident_change'].fillna(0)
latest_filtered['yoy_fatality_change']  = latest_filtered['yoy_fatality_change'].fillna(0)

# Percent YoY change
latest_filtered['yoy_acc_pct'] = (
    latest_filtered['yoy_accident_change'] / latest_filtered['accidents'] * 100
).round(3)
latest_filtered['yoy_fat_pct'] = (
    latest_filtered['yoy_fatality_change'] / latest_filtered['fatalities'] * 100
).round(3)

print("\nEngineered features added:")
print(latest_filtered[['state','log_accidents','accident_share_pct',
                        'yoy_acc_pct','yoy_fat_pct']].head())

# %% CELL 4 — Pearson Correlation Matrix (primary output)
corr_cols = [
    'accidents',
    'fatalities',
    'fatality_rate_per_accident',
    'log_accidents',
    'log_fatalities',
    'yoy_acc_pct',
    'yoy_fat_pct',
    'accident_share_pct',
]
corr_matrix = latest_filtered[corr_cols].corr(method='pearson')

print("\nCorrelation Matrix (Pearson):")
print(corr_matrix.round(3).to_string())

# %% CELL 5 — Plot correlation heatmap
fig, ax = plt.subplots(figsize=(11, 9))
fig.patch.set_facecolor('#0f0f1a')
ax.set_facecolor('#1a1a2e')

# Clean labels for display
clean_labels = [
    'Accidents', 'Fatalities', 'Fatality Rate',
    'Log Accidents', 'Log Fatalities',
    'YoY Accident %', 'YoY Fatality %',
    'Accident Share %'
]

mask = np.triu(np.ones_like(corr_matrix, dtype=bool))  # upper triangle mask

sns.heatmap(
    corr_matrix,
    mask=mask,
    annot=True,
    fmt='.2f',
    cmap='RdYlGn',
    vmin=-1, vmax=1,
    center=0,
    square=True,
    linewidths=0.5,
    linecolor='#333',
    cbar_kws={'shrink': 0.8, 'label': 'Pearson r'},
    xticklabels=clean_labels,
    yticklabels=clean_labels,
    ax=ax
)

ax.set_title(
    'Feature Correlation Matrix — India Road Accidents 2024\n'
    'State-Level Analysis (States with 500+ accidents)',
    color='white', fontsize=13, fontweight='bold', pad=15
)
ax.tick_params(colors='white', labelsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha='right', color='white')
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, color='white')
plt.colorbar(ax.collections[0], ax=ax, label='Pearson r')

plt.tight_layout()
plt.savefig(f'{OUTPUT}/correlation_heatmap.png', dpi=150,
            bbox_inches='tight', facecolor='#0f0f1a')
plt.show()
print("Correlation heatmap saved: outputs/correlation_heatmap.png")

# %% CELL 6 — Pairwise Significance Testing
# For each meaningful pair, print r, p-value, and interpretation
print("\n" + "="*60)
print("PAIRWISE CORRELATION SIGNIFICANCE TESTS")
print("="*60)

pairs = [
    ('accidents',   'fatalities',                'Do more accidents = more deaths?'),
    ('log_accidents','fatality_rate_per_accident','Does accident volume predict fatality rate?'),
    ('yoy_acc_pct', 'yoy_fat_pct',               'Do accident increases drive fatality increases?'),
    ('accident_share_pct','fatality_rate_per_accident','Do high-share states have worse rates?'),
]

results = []
for x_col, y_col, question in pairs:
    x = latest_filtered[x_col].dropna()
    y = latest_filtered[y_col].dropna()
    idx = x.index.intersection(y.index)
    x, y = x.loc[idx], y.loc[idx]

    r, p = sp_stats.pearsonr(x, y)
    sig = "✅ SIGNIFICANT" if p < 0.05 else "❌ NOT significant"
    strength = (
        "Very Strong" if abs(r) > 0.7 else
        "Strong"      if abs(r) > 0.5 else
        "Moderate"    if abs(r) > 0.3 else
        "Weak"
    )
    direction = "Positive" if r > 0 else "Negative"

    print(f"\nQ: {question}")
    print(f"   r = {r:.4f} | p = {p:.4f} | {sig}")
    print(f"   Interpretation: {direction} {strength} correlation")

    results.append({'x': x_col, 'y': y_col, 'r': round(r,4),
                    'p_value': round(p,4), 'significant': p < 0.05,
                    'strength': strength, 'question': question})

results_df = pd.DataFrame(results)
results_df.to_csv(f'{OUTPUT}/correlation_significance.csv', index=False)

# %% CELL 7 — OLS Regression: Fatalities ~ Accidents (state level)
print("\n" + "="*60)
print("OLS REGRESSION 1: Fatalities ~ Accidents (State Level 2024)")
print("="*60)

X1 = sm.add_constant(latest_filtered['accidents'])
y1 = latest_filtered['fatalities']
model1 = sm.OLS(y1, X1).fit()
print(model1.summary())

# Extract key numbers
coef  = model1.params['accidents']
r2    = model1.rsquared
p_acc = model1.pvalues['accidents']
print(f"\nKEY: For every 1 additional accident in a state,")
print(f"     fatalities increase by {coef:.4f} on average")
print(f"     R² = {r2:.4f} | p = {p_acc:.6f}")

# %% CELL 8 — OLS Regression: National fatalities ~ Year (trend line)
print("\n" + "="*60)
print("OLS REGRESSION 2: National Fatalities ~ Year (Trend 2019-2024)")
print("="*60)

national = state_master.groupby('year').agg(
    fatalities=('fatalities','sum'),
    accidents=('accidents','sum')
).reset_index()

X2 = sm.add_constant(national['year'])
y2 = national['fatalities']
model2 = sm.OLS(y2, X2).fit()
print(model2.summary())

annual_increase = model2.params['year']
r2_nat = model2.rsquared
print(f"\nKEY: India adds ~{int(annual_increase):,} fatalities per year on average")
print(f"     R² = {r2_nat:.4f} — trend explains {r2_nat*100:.1f}% of variance")

# %% CELL 9 — Scatter plots with regression lines
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.patch.set_facecolor('#0f0f1a')

def scatter_reg(ax, x_data, y_data, labels, x_label, y_label, title, color):
    ax.set_facecolor('#1a1a2e')

    slope, intercept, r, p, _ = sp_stats.linregress(x_data, y_data)
    ax.scatter(x_data, y_data, color=color, s=80, alpha=0.8, zorder=5)

    # Regression line
    x_line = np.linspace(x_data.min(), x_data.max(), 100)
    ax.plot(x_line, slope * x_line + intercept,
            color='white', linewidth=2, alpha=0.8, zorder=4)

    # Annotate top 5 states
    combined = pd.DataFrame({'x': x_data.values, 'y': y_data.values,
                              'label': labels.values})
    for _, row in combined.nlargest(5, 'y').iterrows():
        ax.annotate(row['label'], (row['x'], row['y']),
                    textcoords='offset points', xytext=(5, 3),
                    fontsize=8, color='white', alpha=0.9)

    sig_str = f"p={p:.4f} {'✓' if p<0.05 else '✗'}"
    ax.set_title(f"{title}\nr={r:.3f} | R²={r**2:.3f} | {sig_str}",
                 color='white', fontsize=11, fontweight='bold')
    ax.set_xlabel(x_label, color='#aaa')
    ax.set_ylabel(y_label, color='#aaa')
    ax.tick_params(colors='#aaa')
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['bottom','left']].set_color('#444')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'{int(v):,}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'{int(v):,}'))

# Chart 1: Accidents vs Fatalities
scatter_reg(axes[0],
    latest_filtered['accidents'],
    latest_filtered['fatalities'],
    latest_filtered['state'],
    'Total Accidents (2024)',
    'Total Fatalities (2024)',
    'Accidents vs Fatalities\n(State Level)',
    '#4fc3f7')

# Chart 2: Log Accidents vs Fatality Rate
scatter_reg(axes[1],
    latest_filtered['log_accidents'],
    latest_filtered['fatality_rate_per_accident'],
    latest_filtered['state'],
    'Log(Total Accidents)',
    'Fatality Rate per Accident',
    'Accident Volume vs Fatality Rate\n(Do busier roads kill more per crash?)',
    '#ef5350')

# Chart 3: YoY accident % vs YoY fatality %
# Filter outliers for clean plot
yoy_clean = latest_filtered[
    (latest_filtered['yoy_acc_pct'].abs() < 50) &
    (latest_filtered['yoy_fat_pct'].abs() < 50)
]
scatter_reg(axes[2],
    yoy_clean['yoy_acc_pct'],
    yoy_clean['yoy_fat_pct'],
    yoy_clean['state'],
    'YoY Accident Change %',
    'YoY Fatality Change %',
    'Accident Growth vs Fatality Growth\n(2023→2024)',
    '#66bb6a')

plt.suptitle(
    'Statistical Relationships — India Road Accident Data 2024\n'
    'Pearson Correlation with OLS Regression Lines',
    color='white', fontsize=13, y=1.02
)
plt.tight_layout()
plt.savefig(f'{OUTPUT}/regression_scatter.png', dpi=150,
            bbox_inches='tight', facecolor='#0f0f1a')
plt.show()
print("Regression scatter saved: outputs/regression_scatter.png")

# %% CELL 10 — Spearman Rank Correlation (non-parametric, more robust)
print("\n" + "="*60)
print("SPEARMAN RANK CORRELATION (robust, non-parametric)")
print("="*60)

pairs_sp = [
    ('accidents', 'fatalities'),
    ('accidents', 'fatality_rate_per_accident'),
    ('yoy_acc_pct', 'yoy_fat_pct'),
]
for x_col, y_col in pairs_sp:
    x = latest_filtered[x_col].dropna()
    y = latest_filtered[y_col].dropna()
    idx = x.index.intersection(y.index)
    rho, p = sp_stats.spearmanr(x.loc[idx], y.loc[idx])
    print(f"{x_col} vs {y_col}: rho={rho:.4f}, p={p:.4f} "
          f"{'✅' if p<0.05 else '❌'}")

# %% CELL 11 — Summary print (copy these numbers to README)
print("\n" + "="*60)
print("SUMMARY — COPY THESE TO YOUR README")
print("="*60)
acc_fat_r, acc_fat_p = sp_stats.pearsonr(
    latest_filtered['accidents'], latest_filtered['fatalities'])
log_rate_r, log_rate_p = sp_stats.pearsonr(
    latest_filtered['log_accidents'],
    latest_filtered['fatality_rate_per_accident'])
yoy_r, yoy_p = sp_stats.pearsonr(
    yoy_clean['yoy_acc_pct'], yoy_clean['yoy_fat_pct'])

print(f"1. Accidents vs Fatalities: r={acc_fat_r:.3f}, p={acc_fat_p:.4f}")
print(f"   → {'Significant' if acc_fat_p<0.05 else 'Not significant'}")
print(f"2. Log(Accidents) vs Fatality Rate: r={log_rate_r:.3f}, p={log_rate_p:.4f}")
print(f"   → {'Significant' if log_rate_p<0.05 else 'Not significant'}")
print(f"3. YoY Accident % vs YoY Fatality %: r={yoy_r:.3f}, p={yoy_p:.4f}")
print(f"   → {'Significant' if yoy_p<0.05 else 'Not significant'}")
print(f"4. OLS: India adds ~{int(annual_increase):,} fatalities/year")
print(f"   National trend R²={r2_nat:.4f}")
print(f"5. OLS: Each additional state accident → {coef:.4f} more fatalities")

# %%
