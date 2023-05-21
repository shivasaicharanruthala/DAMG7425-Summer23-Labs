## Data Profiling

Use the `ydata-profiling` python package for Exploratory Data Analysis (EDA)
Github [link](https://github.com/ydataai/ydata-profiling)
PyPi [link](https://pypi.org/project/ydata-profiling/)

### Datasource

NASA Meteorites example
Source of data: https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh

Original file is located at
https://colab.research.google.com/github/ydataai/pandas-profiling/blob/master/examples/meteorites/meteorites_cloud.ipynb

### Steps to generate a profiling report

1. Install the python package in the venv
   ```bash
   python -m venv .env
   source .env/bin/activate
   pip install ydata-profiling
   ```
2. Run the script
   ```bash
   python data_profile.py
   ```
3. It generates a html [report](./profile_export.html)

4. Explore the html report to find insights about the dataset
