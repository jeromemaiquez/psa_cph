import pandas as pd
import numpy as np


def get_brgy_psgc(df: pd.DataFrame, reg: str = "REG", prv: str = "PRV", mun: str = "MUN", bgy: str = "BGY", zfill_widths: list[int] = [2, 2, 2, 3]) -> pd.Series:
    df_psgc = pd.DataFrame(index=df.index, dtype=str)
    
    levels = [reg, prv, mun, bgy]

    for level, width in zip(levels, zfill_widths):
        df_psgc[level] = df[level].astype(str).str.zfill(width)
    
    return "PH" + df_psgc[reg] + df_psgc[prv] + df_psgc[mun] + df_psgc[bgy]