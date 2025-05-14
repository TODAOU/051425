import streamlit as st
import ee
from google.oauth2 import service_account
import geemap.foliumap as geemap

# 從 Streamlit Secrets 讀取 GEE 服務帳戶金鑰 JSON
service_account_info = st.secrets["GEE_SERVICE_ACCOUNT"]

# 使用 google-auth 進行 GEE 授權
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)

# 初始化 GEE
ee.Initialize(credentials)


###############################################
st.set_page_config(layout="wide")
st.title("🌍 使用服務帳戶連接 GEE 的 Streamlit App")


# 地理區域
point = ee.Geometry.Point([120.5583462887228, 24.081653403304525])

# 擷取 Landsat NDVI
image = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
    .filterBounds(point) \
    .filterDate("2021-01-01", "2021-12-31") \
    .median()
    .first()
    .select('B.*')

vis_params = image.normalizedDifference(["B8", "B4", "B3"]).rename("vis_params")

training001 = my_image.sample(
    **{
        'region': my_image.geometry(),  # 若不指定，則預設為影像my_image的幾何範圍。
        'scale': 10,
        'numPixels': 10000,
        'seed': 0,
        'geometries': True,  # 設為False表示取樣輸出的點將忽略其幾何屬性(即所屬網格的中心點)，無法作為圖層顯示，可節省記憶體。
    }
)

clusterer_KMeans = ee.Clusterer.wekaKMeans(nClusters=n_clusters).train(training001)
# ee.Clusterer.wekaKMeans().train() 使用K Means 演算法建立分群器進行訓練

legend_dict = {
    'zero': '#ab0000',
    'one': '#1c5f2c',
    'two': '#d99282',
    'three': '#466b9f',
    'four': '#ab6c28',
}
# 為分好的每一群賦予標籤

palette = list(legend_dict.values())
vis_params_001 = {'min': 0, 'max': 4, 'palette': palette}



# 顯示地圖
Map = geemap.Map(center=[120.5583462887228, 24.081653403304525], zoom=10)
Map.addLayer(result001, vis_params_001, {"min": 100, "max": 3500, "palette": ["white", "green"]}, "Labelled clusters")
Map.to_streamlit(height=600)
