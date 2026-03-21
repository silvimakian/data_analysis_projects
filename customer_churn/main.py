import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

df=pd.read_csv("cleaned_ecommerce.csv")
df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'])
df=df.dropna(subset=['CustomerID'])

#creating rfm ( recency frequency monetary ) table
rfm=df.groupby("CustomerID").agg({
    "InvoiceDate":"max",
    "InvoiceNo": "nunique",
    "Revenue":"sum"
}).reset_index()

#changing the names of columns 
rfm.rename(columns={
    "InvoiceNo": "Frequency",
    "Revenue": "Monetary"
}, inplace=True)

#calculate recency
snapshot_date=df['InvoiceDate'].max()+pd.Timedelta(days=1)
rfm['Recency']=(snapshot_date-rfm['InvoiceDate']).dt.days
rfm=rfm.drop(columns=['InvoiceDate'])

rfm['Frequency'].value_counts().sort_index()

#print(rfm.describe())

#creaating rfm column

#Due to heavy skewness in purchase frequency, manual scoring was applied instead of quantile binning.
def f_score(x):
    if x==1:
        return 1
    elif x<=3:
        return 2
    elif x<=10:
        return 3
    else:
        return 4
    
rfm["F Score"]=rfm['Frequency'].apply(f_score)
rfm['R Score']=pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop")



rfm['M Score']=pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5], duplicates="drop")

rfm['RFM Scores']=(
    rfm["R Score"].astype(str)+
    rfm["F Score"].astype(str)+
    rfm['M Score'].astype(str)
)

#creating customer segments based on our rfm scores
def segment_customer(row):
    if row['R Score'] >= 4 and row['F Score'] >= 4 and row['M Score'] >= 4:
        return "Champions"
    
    elif row['R Score'] >= 3 and row['F Score'] >= 3 and row['M Score'] >= 3:
        return "Loyal High-Value Customers"
    
    elif row['R Score'] >= 4 and row['F Score'] <= 2:
        return "Recent One-Time Buyers"
    
    elif row['R Score'] <= 2 and row['F Score'] >= 3:
        return "At Risk Customers"
    
    elif row['R Score'] <= 2 and row['F Score'] <= 2:
        return "Lost Customers"
    
    else:
        return "Regular Customers"

rfm['Segment'] = rfm.apply(segment_customer, axis=1)
rfm['Segment'].value_counts(ascending=True)
#our business segmentation now looks like this 
# Loyal Customers        30
#At Risk               191
#Champions             307
#New Customers        1465
#Regular Customers    2345


#handling the skewness of our data by applying log transform
rfm_ml=rfm[['Recency', 'Frequency', 'Monetary']].copy()
rfm_ml['Monetary']=np.log1p(rfm_ml['Monetary'])
rfm_ml['Frequency']=np.log1p(rfm_ml['Frequency'])

#standardalizing our metrics
scaler=StandardScaler()
rfm_scaled=scaler.fit_transform(rfm_ml)

#finding the optimal k using the elbow method
inertia=[]
for k in range(2, 11):
    kmeans=KMeans(n_clusters=k, random_state=42)
    kmeans.fit(rfm_scaled)
    inertia.append(kmeans.inertia_)

plt.plot(range(2,11), inertia)
#plt.show()
#our optimal cluster number is 4

kmeans=KMeans(n_clusters=4, random_state=5)
rfm['Clusters']=kmeans.fit_predict(rfm_scaled)


cluster_profile=rfm.groupby('Clusters')[['Recency', 'Frequency', 'Monetary']].median()
print(cluster_profile)

#group 0-champions
#group 1-at risk customers
#group 2-loyal spenders
#group 3-one time customer

cluster_names={
    0:"Champions",
    1: "Lost Customers",
    2: "Loyal mid-value customers",
    3: "Recent One time buyers"
}

rfm['Cluster_Names']=rfm['Clusters'].map(cluster_names)
print(pd.crosstab(rfm['Segment'], rfm['Cluster_Names']))