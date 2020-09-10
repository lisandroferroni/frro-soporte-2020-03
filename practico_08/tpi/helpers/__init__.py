import time
import numpy as np
from matplotlib import pyplot
from matplotlib.dates import date2num

def normal_dates(from_datetime = '2020-01-01 00:00:00', to_datetime = '2020-01-01 23:59:59', qty = 10000):
    _DATE_RANGE = (from_datetime, to_datetime)
    _DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    _EMPIRICAL_SCALE_RATIO = 0.15
    _DISTRIBUTION_SIZE = qty

    time_range = tuple(time.mktime(time.strptime(d, _DATE_FORMAT))
                       for d in _DATE_RANGE)
    distribution = np.random.normal(
        loc=(time_range[0] + time_range[1]) * 0.5,
        scale=(time_range[1] - time_range[0]) * _EMPIRICAL_SCALE_RATIO,
        size=_DISTRIBUTION_SIZE
    )
    date_range = tuple(time.strftime(_DATE_FORMAT, time.localtime(t))
                       for t in np.sort(distribution))

    prev_hour = date_range[0].split(" ")[1].split(":")[0]
    hoursArray = []
    for d in date_range:
        hour = d.split(" ")[1].split(":")[0]
        hoursArray.append(int(hour))
    ##Gráfica acumulativa de fechas con distribución normal.
    #pyplot.hist(hoursArray, 24, facecolor='blue', alpha=0.5)
    #pyplot.show()
    return date_range