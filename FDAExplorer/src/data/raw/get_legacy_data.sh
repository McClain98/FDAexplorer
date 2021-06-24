wget http://www.accessdata.fda.gov/premarket/ftparea/pmn7680.zip
unzip pmn7680
mv pmn7680.txt data_1978_1980.txt
rm pmn7680.zip
mv data_1978_1980.txt legacy

wget http://www.accessdata.fda.gov/premarket/ftparea/pmn8185.zip
unzip pmn8185
mv pmn8185.txt data_1981_1985.txt
rm pmn8185.zip
mv data_1981_1985.txt legacy

wget http://www.accessdata.fda.gov/premarket/ftparea/pmn8690.zip
unzip pmn8690
mv pmn8690.txt data_1986_1990.txt
rm pmn8690.zip
mv data_1986_1990.txt legacy

wget http://www.accessdata.fda.gov/premarket/ftparea/pmn9195.zip
unzip pmn9195
mv pmn9195.txt data_1991_1995.txt
rm pmn9195.zip
mv data_1991_1995.txt legacy

wget http://www.accessdata.fda.gov/premarket/ftparea/pmn96cur.zip
unzip pmn96cur
mv pmn96curr.txt data_1996_curr.txt
rm pmn96cur.zip
mv data_1996_curr.txt legacy


