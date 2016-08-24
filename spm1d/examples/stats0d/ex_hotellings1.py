
import spm1d




#(0) Load dataset:
dataset = spm1d.data.mv0d.hotellings1.RSXLHotellings1()
# dataset = spm1d.data.mv0d.hotellings1.Sweat()
y,mu    = dataset.Y, dataset.mu
print( dataset )


#(1) Conduct T2 test:
T2      = spm1d.stats.hotellings(y, mu=mu)
T2i     = T2.inference(alpha=0.05)
print( T2i )



