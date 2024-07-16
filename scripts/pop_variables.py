import pandas as pd
import numpy as np


def population(df: pd.DataFrame, for_each: str = "BGY_PSGC", col_to_count: str = "P2") -> pd.Series:
    return df.groupby(for_each)[col_to_count].count()


def sex_ratio(df: pd.DataFrame, for_each: str = "BGY_PSGC", sex: str = "P3", places: int = 3) -> pd.Series:
    is_male = df[sex] == 1
    is_female = df[sex] == 2
    count_males: pd.Series = df[is_male].groupby(for_each)[sex].count()
    count_females: pd.Series = df[is_female].groupby(for_each)[sex].count()

    return round(count_males / count_females * 100, places)


def working_age_population(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5") -> pd.Series:
    is_working_age: pd.Series = df[age].between(15, 64, "both")
    return df[is_working_age].groupby(for_each)[age].count()


def youth_dependency_ratio(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5", places: int = 3) -> pd.Series:
    is_youth: pd.Series = df[age] < 15
    count_youth: pd.Series =  df[is_youth].groupby(for_each)[age].count()
    count_working_age: pd.Series = working_age_population(df, for_each=for_each, age=age)

    return round(count_youth / count_working_age * 100, places)


def old_age_dependency_ratio(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5", places: int = 3) -> pd.Series:
    is_old_age: pd.Series = df[age] < 15
    count_old_age: pd.Series =  df[is_old_age].groupby(for_each)[age].count()
    count_working_age: pd.Series = working_age_population(df, for_each=for_each, age=age)
    
    return round(count_old_age / count_working_age * 100, places)


def school_attendance_rate():
    ...


def literacy_rate():
    ...


def mean_years_schooling():
    ...


def ofw_per_1k_people(df: pd.DataFrame, for_each: str = "BGY_PSGC", ofw: str = "P15", col_to_count: str = "P2", places: int = 3) -> pd.Series:
    is_ofw: pd.Series = df[ofw] == 1
    count_ofw: pd.Series = df[is_ofw].groupby(for_each)[ofw].count()
    count_pop: pd.Series = population(df, for_each=for_each, col_to_count=col_to_count)

    return round(count_ofw / count_pop * 1_000, places)