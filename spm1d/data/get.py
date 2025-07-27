

def iter_all():
    datasets = []
    
    
    # ---------- Univariate 0D ----------
    
    from . uv0d.t1 import RSWeightReduction,ColumbiaSalmonella
    datasets.append( RSWeightReduction )
    datasets.append( ColumbiaSalmonella )
    
    from . uv0d.tpaired import RSWeightClinic, ColumbiaMileage
    datasets.append( RSWeightClinic )
    datasets.append( ColumbiaMileage )
    
    from . uv0d.t2 import RSFlavor,ColumbiaPlacebo
    datasets.append( RSFlavor )
    datasets.append( ColumbiaPlacebo )
    
    from . uv0d.regress import RSRegression,ColumbiaHeadCircumference
    datasets.append( RSRegression )
    datasets.append( ColumbiaHeadCircumference )
    
    from . uv0d.anova1 import Cars,ConstructionUnequalSampleSizes,RSUnequalSampleSizes,Sound,Southampton1
    datasets.append( Cars )
    datasets.append( ConstructionUnequalSampleSizes )
    datasets.append( RSUnequalSampleSizes )
    datasets.append( Sound )
    datasets.append( Southampton1 )
    
    from . uv0d.anova1rm import Abdi2010,Groceries,Imacelebrity,Southampton1rm
    datasets.append( Abdi2010 )
    datasets.append( Groceries )
    datasets.append( Imacelebrity )
    datasets.append( Southampton1rm )
    
    from . uv0d.anova2 import Detergent, Mouse, Satisfaction, SouthamptonCrossed1, SPM1D3x3, SPM1D3x4, SPM1D4x4, SPM1D4x5
    datasets.append( Detergent )
    datasets.append( Mouse )
    datasets.append( Satisfaction )
    datasets.append( SouthamptonCrossed1 )
    datasets.append( SPM1D3x3 )
    datasets.append( SPM1D3x4 )
    datasets.append( SPM1D4x4 )
    datasets.append( SPM1D4x5 )
    
    
    from . uv0d.anova2nested import QIMacros, SouthamptonNested1
    datasets.append( QIMacros )
    datasets.append( SouthamptonNested1 )

    from . uv0d.anova2onerm import RSXLDrug, Santa23, Southampton2onerm, SPM1D3x3, SPM1D3x4, SPM1D3x4A, SPM1D3x5, SPM1D4x4, SPM1D4x5, Santa23UnequalSampleSizes, Southampton2onermUnequalSampleSizes
    datasets.append( RSXLDrug )
    datasets.append( Santa23 )
    datasets.append( Southampton2onerm )
    datasets.append( SPM1D3x3 )
    datasets.append( SPM1D3x4 )
    datasets.append( SPM1D3x4A )
    datasets.append( SPM1D3x5 )
    datasets.append( SPM1D4x4 )
    datasets.append( SPM1D4x4 )
    datasets.append( Santa23UnequalSampleSizes )
    datasets.append( Southampton2onermUnequalSampleSizes )

    from . uv0d.anova2rm import Antidepressant, RSXLTraining, SocialNetworks, Southampton2rm, SPM1D3x3, SPM1D3x4, SPM1D3x5, SPM1D4x4, SPM1D4x5
    datasets.append( Antidepressant )
    datasets.append( RSXLTraining )
    datasets.append( SocialNetworks )
    datasets.append( Southampton2rm )
    datasets.append( SPM1D3x3 )
    datasets.append( SPM1D3x4 )
    datasets.append( SPM1D3x5 )
    datasets.append( SPM1D4x4 )
    datasets.append( SPM1D4x4 )

    from . uv0d.anova3 import RSItalian, SouthamptonFullyCrossedMixed
    datasets.append( RSItalian )
    datasets.append( SouthamptonFullyCrossedMixed )

    from . uv0d.anova3nested import SouthamptonNested3
    datasets.append( SouthamptonNested3 )

    from . uv0d.anova3onerm import NYUCaffeine, Southampton3onerm
    datasets.append( NYUCaffeine )
    datasets.append( Southampton3onerm )

    from . uv0d.anova3tworm import NYUHiringExperience, Southampton3tworm
    datasets.append( NYUHiringExperience )
    datasets.append( Southampton3tworm )

    from . uv0d.anova3rm import SPM1D2x2x2, SPM1D2x3x5, SPM1D3x3x3
    datasets.append( SPM1D2x2x2 )
    datasets.append( SPM1D2x3x5 )
    datasets.append( SPM1D3x3x3 )


    # ---------- Multivariate 0D ----------
    
    from . mv0d.hotellings1 import RSXLHotellings1, Sweat
    datasets.append( RSXLHotellings1 )
    datasets.append( Sweat )
    
    
    from . mv0d.hotellings_paired import NCSSBeforeAfter, RSXLHotellingsPaired
    datasets.append( NCSSBeforeAfter )
    datasets.append( RSXLHotellingsPaired )
    
    from . mv0d.hotellings2 import RSXLHotellings2, HELPHomeless
    datasets.append( RSXLHotellings2 )
    datasets.append( HELPHomeless )
    
    from . mv0d.cca import FitnessClub, StackExchange
    datasets.append( FitnessClub )
    datasets.append( StackExchange )
    
    from . mv0d.manova1 import AnimalDepression, Stevens2002
    datasets.append( AnimalDepression )
    datasets.append( Stevens2002 )
    
    
    # ---------- Univariate 1D ----------
    
    from . uv1d.t1 import Random, RandomRough, SimulatedPataky2015a, SimulatedPataky2015b
    datasets.append( Random )
    datasets.append( RandomRough )
    datasets.append( SimulatedPataky2015a )
    datasets.append( SimulatedPataky2015b )
    
    from . uv1d.tpaired import PlantarArchAngle
    datasets.append( PlantarArchAngle )
    
    from . uv1d.t2 import SmallSampleLargePosNegEffects, PlantarArchAngle, SimulatedTwoLocalMax
    datasets.append( SmallSampleLargePosNegEffects )
    datasets.append( PlantarArchAngle )
    datasets.append( SimulatedTwoLocalMax )
    
    from . uv1d.regress import SimulatedPataky2015c, SpeedGRF
    datasets.append( SimulatedPataky2015c )
    datasets.append( SpeedGRF )
    
    from . uv1d.anova1 import SpeedGRFcategorical, Weather
    datasets.append( SpeedGRFcategorical )
    datasets.append( Weather )
    
    from . uv1d.anova1rm import SpeedGRFcategoricalRM
    datasets.append( SpeedGRFcategoricalRM )

    from . uv1d.anova2 import Besier2009kneeflexion, Dorn2012, SPM1D_ANOVA2_2x2, SPM1D_ANOVA2_2x3, SPM1D_ANOVA2_3x3, SPM1D_ANOVA2_3x4, SPM1D_ANOVA2_3x5, SPM1D_ANOVA2_4x4, SPM1D_ANOVA2_4x5
    datasets.append( Besier2009kneeflexion )
    datasets.append( Dorn2012 )
    datasets.append( SPM1D_ANOVA2_2x2 )
    datasets.append( SPM1D_ANOVA2_2x3 )
    datasets.append( SPM1D_ANOVA2_3x3 )
    datasets.append( SPM1D_ANOVA2_3x4 )
    datasets.append( SPM1D_ANOVA2_3x5 )
    datasets.append( SPM1D_ANOVA2_4x4 )
    datasets.append( SPM1D_ANOVA2_4x5 )
    
    from . uv1d.anova2nested import SPM1D_ANOVA2NESTED_2x2, SPM1D_ANOVA2NESTED_2x3, SPM1D_ANOVA2NESTED_3x3, SPM1D_ANOVA2NESTED_3x4, SPM1D_ANOVA2NESTED_3x5, SPM1D_ANOVA2NESTED_4x4, SPM1D_ANOVA2NESTED_4x5
    datasets.append( SPM1D_ANOVA2NESTED_2x2 )
    datasets.append( SPM1D_ANOVA2NESTED_2x3 )
    datasets.append( SPM1D_ANOVA2NESTED_3x3 )
    datasets.append( SPM1D_ANOVA2NESTED_3x4 )
    datasets.append( SPM1D_ANOVA2NESTED_3x5 )
    datasets.append( SPM1D_ANOVA2NESTED_4x4 )
    datasets.append( SPM1D_ANOVA2NESTED_4x5 )
    
    from . uv1d.anova2rm import SPM1D_ANOVA2RM_2x2, SPM1D_ANOVA2RM_2x3, SPM1D_ANOVA2RM_3x3, SPM1D_ANOVA2RM_3x4, SPM1D_ANOVA2RM_3x5, SPM1D_ANOVA2RM_4x4, SPM1D_ANOVA2RM_4x5
    datasets.append( SPM1D_ANOVA2RM_2x2 )
    datasets.append( SPM1D_ANOVA2RM_2x3 )
    datasets.append( SPM1D_ANOVA2RM_3x3 )
    datasets.append( SPM1D_ANOVA2RM_3x4 )
    datasets.append( SPM1D_ANOVA2RM_3x5 )
    datasets.append( SPM1D_ANOVA2RM_4x4 )
    datasets.append( SPM1D_ANOVA2RM_4x5 )

    from . uv1d.anova2onerm import SPM1D_ANOVA2ONERM_2x2, SPM1D_ANOVA2ONERM_2x3, SPM1D_ANOVA2ONERM_3x3, SPM1D_ANOVA2ONERM_3x4, SPM1D_ANOVA2ONERM_3x5, SPM1D_ANOVA2ONERM_4x4, SPM1D_ANOVA2ONERM_4x5
    datasets.append( SPM1D_ANOVA2ONERM_2x2 )
    datasets.append( SPM1D_ANOVA2ONERM_2x3 )
    datasets.append( SPM1D_ANOVA2ONERM_3x3 )
    datasets.append( SPM1D_ANOVA2ONERM_3x4 )
    datasets.append( SPM1D_ANOVA2ONERM_3x5 )
    datasets.append( SPM1D_ANOVA2ONERM_4x4 )
    datasets.append( SPM1D_ANOVA2ONERM_4x5 )

    from . uv1d.anova3 import SPM1D_ANOVA3_2x2x2, SPM1D_ANOVA3_2x3x4
    datasets.append( SPM1D_ANOVA3_2x2x2 )
    datasets.append( SPM1D_ANOVA3_2x3x4 )

    from . uv1d.anova3nested import SPM1D_ANOVA3NESTED_2x2x2, SPM1D_ANOVA3NESTED_2x4x2
    datasets.append( SPM1D_ANOVA3NESTED_2x2x2 )
    datasets.append( SPM1D_ANOVA3NESTED_2x4x2 )

    from . uv1d.anova3rm import SPM1D_ANOVA3RM_2x2x2, SPM1D_ANOVA3RM_2x3x4
    datasets.append( SPM1D_ANOVA3RM_2x2x2 )
    datasets.append( SPM1D_ANOVA3RM_2x3x4 )

    from . uv1d.anova3onerm import SPM1D_ANOVA3ONERM_2x2x2, SPM1D_ANOVA3ONERM_2x3x4
    datasets.append( SPM1D_ANOVA3ONERM_2x2x2 )
    datasets.append( SPM1D_ANOVA3ONERM_2x3x4 )

    from . uv1d.anova3tworm import SPM1D_ANOVA3TWORM_2x2x2, SPM1D_ANOVA3TWORM_2x3x4
    datasets.append( SPM1D_ANOVA3TWORM_2x2x2 )
    datasets.append( SPM1D_ANOVA3TWORM_2x3x4 )

    # ---------- Multivariate 1D ----------
    
    from . mv1d.hotellings_paired import Neptune1999kneekin, Pataky2014cop
    datasets.append( Neptune1999kneekin )
    datasets.append( Pataky2014cop )
    
    from . mv1d.hotellings2 import Besier2009muscleforces
    datasets.append( Besier2009muscleforces )
    
    from . mv1d.cca import Dorn2012
    datasets.append( Dorn2012 )
    
    from . mv1d.manova1 import Dorn2012
    datasets.append( Dorn2012 )

    
    for d in datasets:
        yield eval('d()')


def iter_datasets(dim=None, testname=None):
    for d in iter_all():
        if (dim is None) and (testname is None):
            yield d
        elif (testname is None):
            if d.dim==0:
                yield d
        elif (dim is None):
            if d.testname == testname:
                yield d
        else:
            if (d.dim==dim) and (d.testname == testname):
                yield d




if __name__ == '__main__':
    # for d in iter_all():
    #     print( d.dim, d.name, d.testname )
        
    for d in iter_datasets(dim=1, testname='hotellings'):
        print( d )