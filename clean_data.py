import pandas as pd

df = pd.read_csv('messy_population_data.csv')     #loading the dataset 



rows, columns = df.shape                          #get a general overview
print(f"Rows: {rows}, Columns: {columns}")

df.info()                     #check for data types and non-null counts
df.describe()                 #numerical summary statistics

missing_values = df.isnull().sum()                #summing up missing values per column
print(f"missing values: {missing_values[missing_values > 0]}")

age_missing_example = df[df['age'].isnull()]     #example for displayings rows with missing values specifically in 'age' column
print(age_missing_example.head())
               

duplicates = df.duplicated().sum()                #count duplicated rows
print(f"Duplicated Rows: {duplicates}")

duplicate_rows = df[df.duplicated(keep=False)]    #identify and display all duplicate rows in the dataset
print("Duplicate rows in the dataset:")
print(duplicate_rows.head())

for column in df.columns:                         #unique values per column
    print(f"Unique values in {column}:")
    print(df[column].value_counts(dropna=False), "\n")

mean_age = df['age'].mean()                       #calculate and print the mean for each specified column
mean_gender = df['gender'].mean()
mean_year = df['year'].mean()
mean_population = df['population'].mean()

print(f"Mean of age: {mean_age}")
print(f"Mean of gender: {mean_gender}")
print(f"Mean of year: {mean_year}")
print(f"Mean of population: {mean_population}")

print("Maximum values for each column:")          #display the maximum and minimum values for each column
print(df.max(numeric_only=True))
print("\nMinimum values for each column:")
print(df.min(numeric_only=True))



#Data Cleaning: 


def data_distribution_summary(df, columns):      #function to summarize data distribution changes for numeric columns
    return df[columns].describe()

#initial distribution and row count:
initial_distribution = data_distribution_summary(df, ['age', 'gender', 'year', 'population'])
initial_row_count = len(df)
missing_values_before = df.isnull().sum()


df.dropna(inplace=True)                          #drop rows with any missing values
numeric_columns = ['age', 'population']          #fill missing values in numeric columns with the column mean
for column in numeric_columns:
    df[column].fillna(df[column].mean(), inplace=True)


rows_dropped_na = initial_row_count - len(df)     #calculate number of rows affected by dropping
initial_row_count = len(df)                       #update the row count after dropping
numeric_columns = ['age', 'population']           #fill missing values in specific numeric columns with the column mean
for column in numeric_columns:
    df[column].fillna(df[column].mean(), inplace=True)


missing_values_after = df.isnull().sum()                                           #count missing values after filling
rows_filled_na = missing_values_before - missing_values_after                      #rows affected by filling
distribution_after_na_handling = data_distribution_summary(df, numeric_columns)    #distribution change after handling missing values



row_count_before_duplicates = len(df)               #record initial row count before removing duplicates
df.drop_duplicates(inplace=True)                    #calculate number of rows affected by removing duplicates
rows_dropped_duplicates = row_count_before_duplicates - len(df)                       
distribution_after_duplicates = data_distribution_summary(df, numeric_columns)



invalid_gender_count = len(df[~df['gender'].isin([1, 2])])     #count rows with invalid gender values before cleaning
df = df[df['gender'].isin([1, 2])]                             #remove rows where 'gender' is not 1 or 2
rows_greater_than_2024 = len(df[df['year'] > 2024])            #count rows greater than 'year' 2024 before cleaning
df = df[df['year'] <= 2024]                                    #remove rows where 'year' is greater than 2024
distribution_after_gender = df['gender'].value_counts()        #distribution change in 'gender' column
distribution_after_year = df['year'].value_counts()            #distribution change in 'year' column



age_zero_count = len(df[df['age'] == 0])                 #count rows where age is zero
df.loc[df['age'] == 0, 'age'] = df['age'].mean()         #replace age=0 with the mean of the age column
distribution_after_age = df['age'].describe()            #distribution change in 'age' column




#summary of Impact
print(f"Initial Row Count: {initial_row_count}")
print(f"Rows Dropped due to Missing Values: {rows_dropped_na}")
print(f"Rows Filled due to Missing Values: {rows_filled_na}")
print(f"Rows Dropped due to Duplicates: {rows_dropped_duplicates}")
print(f"Invalid Gender Rows Corrected: {invalid_gender_count}")
print(f"Rows Greater than Year 2024: {rows_greater_than_2024}")
print(f"Rows with Age Zero Corrected: {age_zero_count}")

print("\nData Distribution Changes after Cleaning:")
print("\nInitial Distribution:")
print(initial_distribution)
print("\nDistribution After Handling Missing Values:")
print(distribution_after_na_handling)
print("\nDistribution After Removing Duplicates:")
print(distribution_after_duplicates)
print("\nDistribution After Cleaning Gender Column:")
print(distribution_after_gender)
print("\nDistribution After Cleaning Year Column:")
print(distribution_after_year)
print("\nDistribution After Cleaning Age Column:")
print(distribution_after_age)





#Saving cleaned dataframe to new file: 
df.to_csv('cleanedpopulationdata.csv', index=False)


cleaned_df = pd.read_csv('cleanedpopulationdata.csv')

print(cleaned_df.info())
rows, columns = cleaned_df.shape                   #get a general overview
for column in cleaned_df.columns:
    data_type = cleaned_df[column].dtype
    non_null_count = cleaned_df[column].notnull().sum()
    unique_values = cleaned_df[column].nunique()
    mean_value = cleaned_df[column].mean() if cleaned_df[column].dtype != 'object' else 'N/A'
    
    print(f"Column Name: {column}")
    print(f"Data Type: {data_type}")
    print(f"Non-Null Count: {non_null_count}")
    print(f"Unique Values: {unique_values}")
    print(f"Mean: {mean_value}")
    print("")