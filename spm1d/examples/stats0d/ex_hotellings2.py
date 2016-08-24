
import spm1d




#(0) Load dataset:
dataset = spm1d.data.mv0d.hotellings2.RSXLHotellings2()
# dataset = spm1d.data.mv0d.hotellings2.HELPHomeless()
yA,yB   = dataset.get_data()
print( dataset )



#(1) Conduct T2 test using spm1d:
T2      = spm1d.stats.hotellings2(yA, yB)
T2i     = T2.inference(alpha=0.05)
print( T2i )



