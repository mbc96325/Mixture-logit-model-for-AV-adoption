import pandas as pd
import numpy as np

# The following package can be installed using
# pip install factor_analyzer
# See https://github.com/EducationalTestingService/factor_analyzer
from factor_analyzer import FactorAnalyzer



mode_att = ['WSAFE','PTSAFE','CARSAFE','DRSAFE',
            'WCOMF','PTCOMF','CARCOMF','DRCOMF',
            'WRELY','PTRELY','CARRELY','DRRELY',
            'WEASY','PTEASY','CAREASY','DREASY']
over_all_perception = ['WPERC','PTPERC','CARPERC','DRPERC']
#activities = ['CMACTAV','CMEFF','CMNOIMP','CMNOTVEH','CMNOTNOS']
risk = ['UNACCRISK','LIKENEW','CAUTIOUS']
# We first extract the columns containing the indicators
columns = mode_att + over_all_perception  #+ risk

indicators = pd.read_csv("../data/individual_new.csv")
indicators = indicators.loc[:,columns]
# Negative values are missing values.
indicators[indicators <= 0] = np.nan
indicators = indicators.dropna(axis = 0, how = 'any')
num_factor = 3
col = ['Factor_'+str(i+1) for i in range(num_factor)]
fa = FactorAnalyzer(rotation='varimax',n_factors=num_factor)
fa.fit(indicators)


labeledResults = pd.DataFrame(fa.loadings_)
filter = (labeledResults <= 0.25) & (labeledResults >= -0.25)
labeledResults[filter] = ''
labeledResults.index = columns
labeledResults.columns = col
labeledResults.to_csv('../data/factor_analysis.csv',index=True)