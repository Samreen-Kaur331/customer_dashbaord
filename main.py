import pandas as pd
df=pd.read_csv('customer_shopping_behavior.csv')
# print(df.head())
# print(df.describe(include='all'))
# print(df.info())
# Check for missing values
# print(df.isnull().sum())
# Handle missing values (if any)



# For simplicity, we will drop rows with missing value
# df.dropna(inplace=True)
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df.columns=df.columns.str.lower().str.replace(' ', '_')
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

print(df.columns)

print(df.isnull().sum())
# "pd.cut() is used when I want custom ranges such as age groups. pd.qcut() is used when I want to divide data into equal-sized groups like quartiles or percentiles."
labels=["young_adults","adults","middle-aged","seniors"]

df['age_group']=pd.qcut(df['age'],q=4,labels=labels)
print(df[['age','age_group']].head(10))

# create columns purchase_frequency_days
freqency_mapping={
    'Fortnightly':14,
    'Weekly':7, 
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(freqency_mapping)

print(df[['frequency_of_purchases', 'purchase_frequency_days']].head(10))



# print(df[['discount_applied','promo_code_used']].head(10))
# Create a new column 'discount_promo_interaction' to capture the interaction between discount and promo code usage
(df['discount_applied']==df['promo_code_used']).all() 
df=df.drop('promo_code_used',axis=1)
print(df.columns)


from sqlalchemy import create_engine

username = "root"
password = "123456789"
host = "127.0.0.1"
port = "3306"
database = "customer_behavior"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# DataFrame ko MySQL table me save karo
df.to_sql(
    name="customer",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data inserted successfully!")











# b['Size']=b['Size'].fillna('Unknown')
# print(b['Size'].isnull().sum())

# b['Units_Sold']=b['Units_Sold'].fillna(0)
# print(b['Units_Sold'].isnull().sum())

# b['MRP']=b['MRP'].fillna(
#     b.groupby('Product_Name')['MRP'].transform('median'))     
# print(b['MRP'].isnull().sum())


# df['product_category'] = df['product_category'].replace({'electronics': 'Electronics'})
# print(df['product_category'])