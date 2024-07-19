### Calculating Barangay-Level Population and Housing Characteristics from PSA 2015 CPH Data

Author:
Jerome Maiquez

#### Rationale
Barangay-level variables related to population and housing characteristics can be used as data for various kinds of analysis, from economic and development planning to climate vulnerability assessments.

For example, mean years of schooling is used as a sub-indicator of the Human Development Index developed by the UNDP. Meanwhile, the percentage of households within a barangay that do not have access to electricity for lighting can be an indicator of energy access.

#### Why PSA CPH 2015?
This is the most recent edition of the PSA census that is openly available for download (from the PSADA website; requires registration). The 2020 CPH microdata requires an application for access.

#### Objectives
1. Iterate over each province/NCR city data for housing and population characteristics
2. Generate barangay-level PSGC column via concatenation
3. Calculate relevant variables (see below)
4. Join resulting DataFrames to barangay shapefile

#### Relevant Variables
See `VARIABLES.md`

#### Project Structure
- `data\`
    - `inputs\`
        - `census`
        - `shapefiles`
    - `outputs\`
        - `census`
        - `shapefiles`
- `notebooks\`
- `scripts\`
- `.gitignore\`
- `README.md`
- `VARIABLES.md`