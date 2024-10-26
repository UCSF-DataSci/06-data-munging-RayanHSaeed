# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: 125718
- **Columns**: 5
- **Duplicated Rows:** 2950

### Column Details
| Column Name     | Data Type | Non-Null Count | Unique Values | Mean          |
|-----------------|-----------|----------------|---------------|---------------|
| income_groups   | object    | 119412         | 124718        | N/A           |
| age             | float64   | 119495         | 119495        | 50.007        |
| gender          | float64   | 119811         | 119718        | 1.579         |
| year            | float64   | 119516         | 119516        | 2025.068      |
| population      | float64   | 119378         | 119378        | 111298303.154 |

### Maximum and minimum values for each column
Maximum values for each column:
- age:           1.000000e+02
- gender:        3.000000e+00
- year:          2.119000e+03
- population:    3.293043e+10

Minimum values for each column:
- age:              0.0
- gender:           1.0
- year:          1950.0
- population:      21.0

### Missing Values for each column
- **income_groups:**    6306
- **age:**              6223
- **gender:**           5907
- **year:**             6202
- **population:**       6340

### Identified Issues

1. **Missing Values**
   - Description: All columns contain missing values (as documented in "Missing Values for each column" section above). 
   - Affected Column(s): income_groups, age, gender, year, and population. 
   - Example: 
       income_groups  age  gender    year    population
      high_income  NaN     3.0  1960.0  8.172589e+06
      high_income  NaN     1.0  1995.0  6.780019e+09
      high_income  NaN     1.0  2007.0  6.734036e+06
      high_income  NaN     NaN  2034.0  5.837574e+06
      high_income  NaN     1.0  2079.0           NaN
   - Potential Impact: Missing values can skew statistical analyses, especially if the data is missing non-randomly.

2. **Duplicated Rows**
   - Description: There are duplicate records, which can bias statistical analyses. **Total Number of Duplicated Rows:** 2950
   - Affected Column(s): All columns
   - Example: Duplicate rows in the dataset:
    income_groups  age  gender    year  population
    138   high_income  0.0     1.0  2088.0   5657492.0
    210   high_income  0.0     2.0  2009.0   6478604.0
    241           NaN  0.0     2.0  2040.0   5701227.0
    298   high_income  0.0     2.0  2097.0   5361755.0
    376   high_income  1.0     1.0  2024.0   5885574.0
    - Potential Impact: Duplicate records can unnecessarily increase counts and distort summary statistics.

3. **Unexpected Values in Selected Columns**
    - Description: 'gender' column contains values besides 1 and 2. Age column contains unrealistic values. Year column contains values past 2024. 
    - Affected Column(s): gender, age, year
    - Example: 
        - Unique values in gender:
            gender
            1.0    56777
            2.0    56748
            3.0     6286
            NaN     5907
            Name: count, dtype: int64 

        - age mininum value: 0 

        - year maximum value: 2119
        - year mean: 2025.0680494661804
    
    - Potential Impact: Incorrect category values make it challenging to accurately analyze data by categories, in this case by gender (male vs. female). Minimum value of age is unrealistic; perhaps incorrectly entered. Maximum value of 'year' is 2119 and mean value of 'year' is 2025.068 meaning that 'year' column contains year values past 2024. 


## 2. Data Cleaning Process

### Issue 1: Missing Values
- **Cleaning Method**: Dropped rows with complete missing data and filled specific columns with appropriate values.
- **Implementation**:
  ```python
    df.dropna(inplace=True)                          #drop rows with any missing values
    numeric_columns = ['age', 'population']          #fill missing values in numeric columns with the column mean
    for column in numeric_columns:
    df[column].fillna(df[column].mean(), inplace=True)


    rows_dropped_na = initial_row_count - len(df)     #calculate number of rows affected by dropping
    initial_row_count = len(df)                       #update the row count after dropping
    numeric_columns = ['age', 'population']           #fill missing values in specific numeric columns with the column mean
    for column in numeric_columns:
    df[column].fillna(df[column].mean(), inplace=True)
  ```
- **Justification**: This approach ensures that only essential data is retained for analysis, meaning that all rows with missing data are dropped. Missing numeric values for 'age' and 'population' were filled in with column mean values. Forward-fill and backfill were not used for non-numeric columns ('income_groups') in this case since that would skew the values in the 'population' column. 
- **Impact**: 
  - Rows affected: 28079
  -Rows Filled due to Missing Values: 
    income_groups    6306
    age              6223
    gender           5907
    year             6202
    population       6340

  - Data distribution change: the count for 'age' column when from 119495 to 97639. The rest of the statistics (mean, std, min, IQR, and max) did not change significantly. Similarly, the count for population went from 119378 to 97639 while the statistics did not change significantly. 

### Issue 2: Removing Completely Duplicated Rows
- **Cleaning Method**: Drop rows that are completely duplicated across all columns.
- **Implementation**:
  ```python
    row_count_before_duplicates = len(df)               #record initial row count before removing duplicates
    df.drop_duplicates(inplace=True)                    #calculate number of rows affected by removing duplicates
    rows_dropped_duplicates = row_count_before_duplicates - len(df)                       
    distribution_after_duplicates = data_distribution_summary(df, numeric_columns)
  ```
- **Justification**: This helps eliminate redundant rows without affecting the dataset’s overall characteristics.
- **Impact**: 
  - Rows affected: 2214
  - Data distribution change: distribution after removing duplicates resembled distribution after handling missing values. 

### Issue 3: Cleaning 'gender' and 'year' column
- **Cleaning Method**: Keep only values of 1 and 2 in the gender column. Removing year values past 2024.
- **Implementation**:
  ```python
    invalid_gender_count = len(df[~df['gender'].isin([1, 2])])     #count rows with invalid gender values before cleaning
    df = df[df['gender'].isin([1, 2])]                             #remove rows where 'gender' is not 1 or 2
    rows_greater_than_2024 = len(df[df['year'] > 2024])            #count rows greater than 'year' 2024 before cleaning
    df = df[df['year'] <= 2024]                                    #remove rows where 'year' is greater than 2024
    distribution_after_gender = df['gender'].value_counts()        #distribution change in 'gender' column
    distribution_after_year = df['year'].value_counts()            #distribution change in 'year' column
  ```
- **Justification**: Assuming that gender of value '3' was entered erroneously, it is removed from the dataset. Any year past 2024 is also assumed to be entered erroneously.
- **Impact**: 
  - Gender Rows affected: 5120
  - Year Rows affected: 45534
  - Data distribution change: distribution after removing genders resembled distribution after handling missing values and removing duplicated rows. After removing year values greater than '2024' count distributions changed to include years 1958 through 2019.  
        Distribution After Cleaning Year Column:
          year
          1988.0    636
          1981.0    623
          2018.0    617
          1999.0    616
          2019.0    616
                  ... 
          2004.0    576
          2008.0    574
          1980.0    574
          1983.0    573
          1958.0    561
          Name: count, Length: 75, dtype: int64

### Issue 4: Cleaning 'age' column
- **Cleaning Method**: Replace values of 'age' that are zero with the column mean
- **Implementation**:
  ```python
    age_zero_count = len(df[df['age'] == 0])                 #count rows where age is zero
    df.loc[df['age'] == 0, 'age'] = df['age'].mean()         #replace age=0 with the mean of the age column
    distribution_after_age = df['age'].describe()            #distribution change in 'age' column
  ```
- **Justification**: Assuming that ago of value '0' was entered erroneously, it is replaced with the mean of the age column. 
- **Impact**: 
  - Rows affected: 449
  - Data distribution change: distribution after removing age with value of 0 resembled distribution after handling missing values and removing duplicated rows. 

## 3. Final State Analysis

### Dataset Overview
- **Name**: cleanedpopulationdata.csv
- **Rows**: 44771
- **Columns**: 5

### Column Details
| Column Name   | Data Type | Non-Null Count | #Unique Values | Mean         |
|---------------|-----------|----------------|----------------|--------------|
| age           | object    | 44771          | 101            | 5.051551e+01 |
| gender        | float64   | 44771          | 2              | 1.500814e+00 |
| income_groups | float64   | 44771          | 8              | NaN          |
| population    | float64   | 44771          | 44201          | 1.145180e+08 |
| year          | float64   | 44771          | 75             | 2.025066e+03 |


### Summary of Changes
- Removed missing values in all columns to ensure each row had complete data.
- Removed entirely duplicated rows across all columns, retaining only unique rows.
- Cleaned up the gender column by removing rows with invalid values, ensuring only values 1 and 2.
- Removed rows with age = 0 for logical consistency in the dataset.
- Removed rows with year > 2024 for logical consistency in the dataset.
- Impact on Data Distribution: the removal of rows with missing or invalid data reduced the dataset size. The distribution of age is now more consistent, as unrealistic values (like 0) have been removed. The mean value of gender now accurately reflects only binary entries, making it suitable for gender-based analyses. Any unrealistic values recorded with year > 2024 have been removed to maintain data integrity as well. 
- Challenges: deciding whether to drop or fill missing values required evaluating the impact on data integrity. Ultimately, I chose to remove rows with missing values rather than filling them in order to avoid skewing the dataset and avoiding the risk of introducing unrealistic data. Going off of the assumption that entering a value of "3" for gender had to be an error, I decided to remove any entries with "3". Having a code book would have made it easier to make that decision. For age, removing zero values improved data quality. Since this was a population dataset based on income groups by age, gender, and year, an age of "0" did not make logical sense to include in the analysis. Further inspection of the data source would be required in order to determine what the cut-off age would need to be. For all intents and purposes, I decided to have the cut off age at 1-years old rather than 0-years old. Similarly, including any sort of data with a year past 2024 did not make sense, so all rows with a year value of 2024 were removed in order to maintain data integrity.
- Future improvements: Standardizing categorical values in order to ensure uniform values for categorical fields like income_groups would make data aggregation and analysis easier; perhaps only allowing certain values to be entered into the data (multiple-choice style). Another improvement could be to add validation rules, such as range checks for age, in order to prevent future entries of unrealistic values (such as age = 0 or gender = 3).