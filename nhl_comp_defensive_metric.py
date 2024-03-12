import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LassoCV

df = pd.read_csv('nhl_defensive_data.csv')
# Assume df has columns for Player, Team, SA/60, QoC, DZS%, Takeaways, PK Eff, xGA, and additional metrics like Corsi Against (CA/60), Fenwick Against (FA/60)

# Feature Engineering
df['TA/GA Ratio'] = df['Takeaways'] / (df['Giveaways'] + 1)  # Avoid division by zero

# Normalize the data
features = ['SA/60', 'QoC', 'DZS%', 'Takeaways', 'PK Eff', 'xGA', 'CA/60', 'FA/60', 'TA/GA Ratio']
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])
df_scaled = pd.DataFrame(df_scaled, columns=features)

# Assuming 'Defensive_Effectiveness' is your target variable
X_train, X_test, y_train, y_test = train_test_split(df_scaled, df['Defensive_Effectiveness'], test_size=0.2, random_state=42)

# Use LassoCV for automatic regularization strength selection
lasso = LassoCV(cv=5).fit(X_train, y_train)

# Extract feature importance (weights) and adjust them to sum to 1 for interpretability
weights = np.abs(lasso.coef_) / np.sum(np.abs(lasso.coef_))

df['Composite_Score'] = np.dot(df_scaled[features], weights)

# Rank players based on the composite score
df['Rank'] = df['Composite_Score'].rank(ascending=False)
df.sort_values('Rank', inplace=True)

# Display top 10 defensive players
print(df[['Player', 'Team', 'Composite_Score', 'Rank']].head(10))

