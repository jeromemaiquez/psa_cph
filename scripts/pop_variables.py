import pandas as pd
import numpy as np


def count_per_barangay(df: pd.DataFrame, col_to_count: str | None = None, for_each: str = "BGY_PSGC", condition: pd.Series | None = None) -> pd.Series:
    if condition is not None:
        df = df[condition]
    
    if col_to_count is None:
        return df.groupby(for_each).size()
    
    return df.groupby(for_each)[col_to_count].count()


def population(df: pd.DataFrame, for_each: str = "BGY_PSGC", col_to_count: str = "P2") -> pd.Series:
    return count_per_barangay(df, for_each=for_each, col_to_count=col_to_count)


def sex_ratio(df: pd.DataFrame, for_each: str = "BGY_PSGC", sex: str = "P3", places: int = 3) -> pd.Series:
    is_male = df[sex] == 1
    is_female = df[sex] == 2
    count_males: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=sex, condition=is_male)
    count_females: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=sex, condition=is_female)

    return round(count_males / count_females * 100, places)


def working_age_population(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5") -> pd.Series:
    is_working_age: pd.Series = df[age].between(15, 64, "both")
    return count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_working_age)


def youth_dependency_ratio(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5", places: int = 3) -> pd.Series:
    is_youth: pd.Series = df[age] < 15
    count_youth: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_youth)
    count_working_age: pd.Series = working_age_population(df, for_each=for_each, age=age)

    return round(count_youth / count_working_age * 100, places)


def old_age_dependency_ratio(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5", places: int = 3) -> pd.Series:
    is_old_age: pd.Series = df[age] < 15
    count_old_age: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_old_age)
    count_working_age: pd.Series = working_age_population(df, for_each=for_each, age=age)
    
    return round(count_old_age / count_working_age * 100, places)


# def school_population(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5") -> pd.Series:
#     is_school_age: pd.Series = df[age].between(5, 24, "both")

#     return count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_school_age)


# def after_school_population(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5") -> pd.Series:
#     is_after_school_age: pd.Series = df[age] > 24

#     return count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_after_school_age)


def school_attendance_rate(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5", attendance: str = "P10", places: int = 3) -> pd.Series:
    is_attending_school: pd.Series = df[attendance] == 1
    is_school_age: pd.Series = df[age].between(5, 24, "both")
    count_attending_school: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_attending_school & is_school_age)
    count_school_age: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_school_age)
    
    return round(count_attending_school / count_school_age * 100, places)


def adult_literacy_rate(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5", literacy: str = "P11", places: int = 3) -> pd.Series:
    is_literate: pd.Series = df[literacy] == 1
    is_reading_age: pd.Series = df[age] > 4
    count_literate: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_literate & is_reading_age)
    count_reading_age: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_reading_age)

    return round(count_literate / count_reading_age * 100, places)


def mean_years_schooling(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5", attainment: str = "P12", places: int = 3) -> pd.Series:
    is_graduate_age: pd.Series = df[age] > 24
    ...


def ofw_per_1k_people(df: pd.DataFrame, for_each: str = "BGY_PSGC", ofw: str = "P15", col_to_count: str = "P2", places: int = 3) -> pd.Series:
    is_ofw: pd.Series = df[ofw] == 1
    count_ofw: pd.Series = df[is_ofw].groupby(for_each)[ofw].count()
    count_pop: pd.Series = population(df, for_each=for_each, col_to_count=col_to_count)

    return round(count_ofw / count_pop * 1_000, places)