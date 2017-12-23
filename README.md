Processing Flight Data using Python
===================================

I started this project to share some examples of using Python to process flight data. 

The [source data](http://stat-computing.org/dataexpo/2009/the-data.html "Flight Data") 
for this project is published in CSV format by the *American Statistical Association* 
based on data they received from the Bureau of Transportation Statistics (a division 
of the U.S. Department of Transportation). You may notice that the data does have 
missing fields. For example, for some flight records, there is no tailNum field. This 
obviously limits what you can do with the data in those cases.

There are 2 implementations of each report method, one using 
[pandas](https://pandas.pydata.org/) and one using
[RxPY](https://github.com/ReactiveX/RxPY).

If you visit the [source data link](http://stat-computing.org/dataexpo/2009/the-data.html "Flight Data"), 
you will notice there are data files for each year from 1987 to 2008. 
The install phase will only download the 2008 flight data file. If you want to 
execute the above classes using flight data from earlier years, you can 
download and extract any of the other available files. Then you can add them to 
the configuration file (*config.yaml*) like this:

![YAML File](https://i.imgur.com/YJjsU6w.gif) 

All of the code in this project is licensed under the MIT License. See the 
LICENSE file for details.

Pull requests are welcome.
