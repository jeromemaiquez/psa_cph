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
    is_old_age: pd.Series = df[age] > 64
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


def literacy_rate(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5", literacy: str = "P11", places: int = 3) -> pd.Series:
    is_literate: pd.Series = df[literacy] == 1
    is_reading_age: pd.Series = df[age] > 4
    count_literate: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_literate & is_reading_age)
    count_reading_age: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_reading_age)

    return round(count_literate / count_reading_age * 100, places)


def attainment_to_years(attainment: 'pd.Series[int]', min_code: int, years_before: int) -> pd.Series:
    return (attainment - min_code) / 10 + years_before

def mean_years_schooling(df: pd.DataFrame, for_each: str = "BGY_PSGC", age: str = "P5", attainment: str = "P12", places: int = 3) -> pd.Series:
    is_graduate_age: pd.Series = df[age] > 24
    count_graduate_age: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=is_graduate_age)

    set_year_per_attainment: dict = {
        "preschool": [df[attainment] == 10, 1],
        "special_education": [df[attainment] == 190, 11],
        "post_secondary": [df[attainment].between(250, 700, "right"), 11],
        "post_tertiary": [df[attainment].between(750, 999, "neither"), 15],
    }

    total_years_schooling = pd.Series(0, index=count_graduate_age.index, dtype=np.float64)

    for level in set_year_per_attainment:
        count_level: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=age, condition=set_year_per_attainment[level][0] & is_graduate_age)
        total_years_at_level: pd.Series = count_level * set_year_per_attainment[level][1]
        total_years_schooling = total_years_schooling.add(total_years_at_level, fill_value=0)

    # primary, secondary, tertiary
    pst: dict = {
        "primary": [110, 170, 1],
        "secondary": [210, 250, 7],
        "tertiary": [710, 750, 11],
    }

    for level in pst:
        is_graduate_age_psgc: pd.Series = df.set_index(for_each)[age] > 24
        is_in_level = df.set_index(for_each)[attainment].between(pst[level][0], pst[level][1], "both")
        years_per_level: pd.Series = attainment_to_years(df.set_index(for_each).loc[is_in_level & is_graduate_age_psgc, attainment], min_code=pst[level][0], years_before=pst[level][2])
        total_years_per_level: pd.Series = years_per_level.groupby(for_each).sum()
        total_years_schooling = total_years_schooling.add(total_years_per_level, fill_value=0)
    
    return round(total_years_schooling / count_graduate_age, places)


def ofw_per_1k_people(df: pd.DataFrame, for_each: str = "BGY_PSGC", ofw: str = "P15", col_to_count: str = "P2", places: int = 3) -> pd.Series:
    is_ofw: pd.Series = df[ofw] == 1
    count_ofw: pd.Series = count_per_barangay(df, for_each=for_each, col_to_count=ofw, condition=is_ofw)
    count_pop: pd.Series = population(df, for_each=for_each, col_to_count=col_to_count)

    return round(count_ofw / count_pop * 1_000, places)