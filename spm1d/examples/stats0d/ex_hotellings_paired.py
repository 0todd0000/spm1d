

import spm1d




#(0) Load dataset:
dataset = spm1d.data.mv0d.hotellings_paired.NCSSBeforeAfter()
# dataset = spm1d.data.mv0d.hotellings_paired.RSXLHotellingsPaired()
yA,yB   = dataset.get_data()
print( dataset )


#(1) Conduct T2 test using spm1d:
T2      = spm1d.stats.hotellings_paired(yA, yB)
T2i     = T2.inference(alpha=0.05)
print( T2i )





