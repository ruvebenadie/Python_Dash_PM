# import libraries
import pandas as pd

# read csv file
df = pd.read_csv('C:/Users/ruveb/Desktop/WHO_AAP.csv')
print(df.head())
# drop columns not wanted
df.drop('WHO Region', inplace=True, axis=1)
df.drop('ISO3', inplace=True, axis=1)
df.drop('NO2 (μg/m3)', inplace=True, axis=1)
df.drop('Reference', inplace=True, axis=1)
df.drop('Number and type of monitoring stations', inplace=True, axis=1)
df.drop('Version of the database', inplace=True, axis=1)
df.drop('Status', inplace=True, axis=1)
df.drop('PM25 temporal coverage (%)', inplace=True, axis=1)
df.drop('PM10 temporal coverage (%)', inplace=True, axis=1)
df.drop('NO2 temporal coverage (%)', inplace=True, axis=1)
df.drop('Unnamed: 15', inplace=True, axis=1)
df.drop('Unnamed: 16', inplace=True, axis=1)

# rename columns
df.rename(columns = {'WHO Country Name':'country'}, inplace = True)
df.rename(columns = {'City or Locality':'city'}, inplace = True)
df.rename(columns = {'Measurement Year':'year'}, inplace = True)

# select only in SA
df = df[df['country'] == 'South Africa']

# remove NaN values
df = df.fillna(0)

# drop SA and save to new csv
df.drop('country', axis=1).to_csv('pm_cleaned.csv', index = False)

# read new csv
df_pm = pd.read_csv('pm_cleaned.csv')

from geopy.geocoders import Nominatim

# geocode cities
locator = Nominatim(timeout=10, user_agent="PDS")

from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
# create location column
df['location'] = df['city'].apply(geocode)
# create longitude, latitude and altitude from location column
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
# split point column into latitude, longitude and altitude columns
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)

# drop unwanted columns, save csv
df.drop('altitude',  inplace = True,  axis=1)
df.drop('location', inplace = True, axis=1)
df.drop('point',  axis=1).to_csv('pm_geocode.csv', index = False)

# read csv
df = pd.read_csv('pm_geocode.csv')

# correct coordinates of cities
df['city'] = df['city'].replace(['Bojanala'], ['Bojanala Platinum'])
df['latitude'] = df['latitude'].replace([44.23052, 0, 0.2896368, 52.0143297, 43.3538584], [-32.9344, -23.6123, -30.4218, -23.9748, -26.3214])
df['latitude'] = df['latitude'].replace([-91.864325, 0, 32.8052602, 5.910263261, 42.4356862], [27.6435, 29.2321, 19.9497, 28.2994, 27.4556])
df.to_csv('pm.csv')







