import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import csv

class Preprocessor(object):
    def process_population(self, df):
        return df['Population'].apply(lambda x: x * 1000)

    def process_revenue(self, df):
        return df[['Money spent on C and J (Billion)', 'Revenue']].apply(lambda x: x * 10000000)

    def drop_columns(self, df, columns):
        new_state = df.drop(columns, axis=1)
        df = new_state.dropna()
        return df


class Predictor(object):
    def predict_population(self, df, year):
        X = np.array(df['Year']).reshape(-1, 1)
        y = np.array(df['Population']).reshape(-1, 1)
        reg = LinearRegression().fit(X, y)
        pred = reg.predict(np.array([year]).reshape(-1, 1))
        return pred[0][0]

    def predict_expenditure(self, df, year):
        X = np.array(df['Year']).reshape(-1, 1)
        y = np.array(df['Money spent on C and J (Billion)']).reshape(-1, 1)
        reg = LinearRegression().fit(X, y)
        pred = reg.predict(np.array([year]).reshape(-1, 1))
        return pred[0][0]

    def predict_revenue(self, df, year):
        X = np.array(df['Year']).reshape(-1, 1)
        y = np.array(df['Revenue']).reshape(-1, 1)
        reg = LinearRegression().fit(X, y)
        pred = reg.predict(np.array([year]).reshape(-1, 1))
        return pred[0][0]

    def tax_payers_expenditure(self, df, year, state):
        X = df[['Year', 'Money spent on C and J (Billion)', 'Population', 'Revenue']]
        y = df['Money spent by tax payers']
        reg = LinearRegression().fit(X, y)
        population = self.predict_population(df, year)
        expenditure = self.predict_expenditure(df, year)
        revenue = self.predict_revenue(df, year)
        pred = reg.predict(
            np.array([[year, expenditure, population, revenue]]))
        row = [year, state, expenditure, population, revenue, pred[0]]
        return row


states = pd.read_excel(r"Prison.xls", engine='openpyxl')
states.isnull().sum()

preprocessor = Preprocessor()
prison_data = preprocessor.drop_columns(states, ['Percentage on C and J of total', 'Individual Revenue'])
prison_data[['Money spent on C and J (Billion)', 'Revenue']] = preprocessor.process_revenue(prison_data)
prison_data['Population'] = preprocessor.process_population(prison_data)
prison_data.to_csv(r'data.csv')
years = [2020, 2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036,2037,2038,2039,2040]

US_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
             "Delaware", "District of Columbia", "Florida", "Hawaii", "Idaho", "Illinois",
             "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
             "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
             "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
             "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
             "South Dakota", "Tennessee",
             "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin",
             "Wyoming"]
fields = ["Year", "State", "Money spent on C and J (Billion)", "Population", "Revenue", "Money spent by tax payers"]
rows = []

start_index = 2
end_index = start_index + 32
predictor = Predictor()

for state in US_states:
    for year in years:
        predict_tax_payers_expenditure = predictor.tax_payers_expenditure(prison_data[start_index:end_index], year,
                                                                          state)
        # print(state, "\t", year, "\t", predict_tax_payers_expenditure, "\t \n")
        rows.append(predict_tax_payers_expenditure)
    start_index = end_index + 1
    end_index = start_index + 32

filename = "prison_records.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
