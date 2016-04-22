# sostc3
SOSTC3 - StackOverflow's Statistics To C3 Library

## How to run
Firstly, we need raw data from the _Spark data mining script_. Given the next folder structure, the data should be inside `data_mining` folder. The other 3 folders should be empty:

```bash
.
├── data_mining       # Raw data from Spark
├── data_coefficient  # Calculated coefficients
├── data_prediction   # Calculated coefficients + prediction
└── data_chart        # Data for charts (grouped coefficients)
```

### 1. Generate coefficients

Then we need to run `data_to_coefficient.py` script, to get the total coefficient values for each year-month timeseries from each language and technology, putting the result in the `data_coefficient` folder:

```bash
$ data_to_coefficient.py data_mining data_coefficient
```

Here we can generate the final chart files if we only want real data and we don't want to include some month predictions.

If we only want real data, jump to _4. Generate chart data without predictions_.

### 2. Generate predictions

To predict the next months data we only need to call the `coefficient_prediction.py` script, with the input and output dirs and, optionally, the number of months to predict (default: 3).

```bash
$ coefficient_prediction.py data_coefficient data_prediction 3
```

Here we got the same coefficients we generated in the _1. Generate coefficients_ step plus the given number of months of coefficient prediction. At this point we can generate the final data for the chart.

### 3. Generate chart data with predictions

Giving data_prediction folder as input dir we ensure we take the prediction coefficients along with real data to generate the final charts:

```bash
$ coefficient_to_chart_.py data_prediction data_chart
```

**WARNING**: Don't go further, we'd already finished!!! The _4. Generate chart data without predictions_ step is **only to generate chart dat WITHOUT predictions**.

### 4. Generate chart data without predictions

This step is only necessary if we didn't want to predict data (we should have jumped the _2. Generate predictions_ and _3. Generate chart data with predictions_ steps)

```bash
$ coefficient_to_chart_.py data_coefficient data_chart
```

