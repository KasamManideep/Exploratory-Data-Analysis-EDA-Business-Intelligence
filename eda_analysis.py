import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('ecommerce_sales.csv')
df['date'] = pd.to_datetime(df['date'])

# --- Summary statistics ---
print(df.describe())
print("\nCategorical columns:")
for col in ['gender', 'region', 'product_category']:
    print(f"\n{col}:\n{df[col].value_counts()}")

# --- Histograms for numerical fields ---
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
numerical_cols = ['age', 'quantity', 'unit_price', 'discount_pct', 'marketing_spend', 'revenue']
for i, col in enumerate(numerical_cols):
    df[col].hist(ax=axes[i//3][i%3], bins=10, color='steelblue', edgecolor='white')
    axes[i//3][i%3].set_title(col)
plt.tight_layout()
plt.savefig('univariate_histograms.png')
plt.show()

# --- Bar chart: Revenue by product category ---
df.groupby('product_category')['revenue'].sum().sort_values().plot(
    kind='barh', color='coral', figsize=(8,4), title='Total Revenue by Category')
plt.tight_layout()
plt.savefig('revenue_by_category.png')
plt.show()
# --- Correlation heatmap ---
plt.figure(figsize=(8, 5))
corr = df[['age','quantity','unit_price','discount_pct','marketing_spend','revenue']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.show()

# --- Scatter: Marketing spend vs Revenue ---
plt.figure(figsize=(7, 5))
colors = {'Electronics':'blue','Clothing':'green','Beauty':'pink','Home':'orange'}
for cat, group in df.groupby('product_category'):
    plt.scatter(group['marketing_spend'], group['revenue'],
                label=cat, alpha=0.7, color=colors.get(cat,'gray'))
plt.xlabel('Marketing Spend (₹)')
plt.ylabel('Revenue (₹)')
plt.title('Marketing Spend vs Revenue by Category')
plt.legend()
plt.tight_layout()
plt.savefig('scatter_marketing_vs_revenue.png')
plt.show()

# --- Pair plot ---
sns.pairplot(df[['age','unit_price','revenue','marketing_spend','product_category']],
             hue='product_category', diag_kind='kde')
plt.suptitle('Pair Plot — Key Variables', y=1.02)
plt.savefig('pairplot.png')
plt.show()

# --- Box plot: Revenue by region ---
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='region', y='revenue', palette='Set2')
plt.title('Revenue Distribution by Region')
plt.tight_layout()
plt.savefig('boxplot_region_revenue.png')
plt.show()