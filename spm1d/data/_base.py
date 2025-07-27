'''
Base classes for all built-in datasets.
'''

# Copyright (C) 2025  Todd Pataky


import os
import numpy as np


def get_datafilepath():
    return os.path.join( os.path.dirname(__file__), 'datafiles' )


class _Dataset(object):
    STAT              = 'Z'    #test statistic
    design            = ''     #design string (e.g. "One-way ANOVA")
    dim               = 0      #data dimensionality
    testname          = None   #spm1d.stats test name

    def __init__(self):
        self._rtol    = 0.001  #relative tolerance (for unit tests)
        self.Y        = None   #dataset
        self.z        = None   #expected test stat
        self.df       = None   #expected degrees of freedom
        self.p        = None   #expected p value
        self.cite     = None   #literature citation (if relevant)
        self.datafile = None   #data file (if available on the web)
        self.www      = None   #web source
        self.note     = None   #note
        self._set_values()
    def __repr__(self):
        s      = 'Dataset\n'
        s     += '   Name      : "%s"\n' %self.name
        s     += '   Design    :  %s\n' %self.design
        s     += '   Data dim  :  %d\n' %self.dim
        s     += '   testname  :  %s\n' %self.testname
        if self.cite:
            s += '   Reference :  %s\n' %self.cite
        if self.www:
            s += '   Web       :  %s\n' %self.www
        if self.datafile:
            s += '   Data file :  %s\n' %self.datafile
        if self.note:
            s += '   %s :  %s\n' %tuple(self.note)
        ss     = self.get_expected_results_as_string()
        s     += ss
        return s
    def _printR(self, x, name='x'):
        print( '%s = c(%s)' %(name, str(x.tolist())[1:-1]) )
    def _printRs(self, xx, names=('x')):
        for x,name in zip(xx,names):
            print
            self._printR(x, name)
    def _set_values(self):    #abstract method;  instantiated by all subclasses
        pass
    @property
    def name(self):
        return self.__class__.__name__
    def get_dependent_variable(self):
        return self.Y
    def get_expected_df(self):
        return self.df
    def get_data(self):
        return self.Y
    def get_expected_test_stat(self):
        return self.z
    def get_expected_p_value(self):
        return self.p
    def get_expected_results_as_string(self):
        s      = '  (Expected results)\n'
        s     += '  %s         :  %s\n' %("{:<2}".format(self.STAT), str(self.z))
        if self.df is not None:
            s += '  df         :  %s\n' %str(self.df)
        s     += '  p          :  %s\n' %str(self.p)
        return s



class _Dataset0D(_Dataset):
    dim   = 0
class Dataset1D(_Dataset):
    dim   = 1


class _DatasetANOVA(_Dataset):
    STAT  = 'F'
class _DatasetT(_Dataset):
    STAT  = 't'
class _DatasetT2(_Dataset):
    STAT  = 'T2'
class _DatasetX2(_Dataset):
    STAT  = 'X2'
class _DatasetK2(_Dataset):
    STAT = 'K2'
class _DatasetSW(_Dataset):
    STAT = 'W'





class DatasetNormality(_DatasetK2):
    design = "Normality test (D'Agostino-Pearson K2)"
class DatasetNormalitySW(_DatasetSW):
    design = 'Normality test (Shapiro-Wilk)'
class DatasetNormality1D(DatasetNormality, Dataset1D):
    design = "Normality test (D'Agostino-Pearson K2)"
class DatasetNormalitySW1D(DatasetNormalitySW, Dataset1D):
    design = 'Normality test (Shapiro-Wilk)'




class DatasetANOVA1(_DatasetANOVA):
    def __init__(self):
        self.rm       = False  #repeated measures
        super(DatasetANOVA1, self).__init__()
        self.design   = 'One-way ANOVA'
        self.testname = 'anova1'
    def get_data(self):
        return self.Y, self.A
    # def get_expected_df(self, type='sphericity_assumed'):
    #     if type=='sphericity_assumed':
    #         return self.df
    #     if type=='GG':
    #         return self.dfGG
    #     elif type=='GGX':
    #         return self.dfGGX
    #     elif type=='HF':
    #         return self.dfHF
    # def get_expected_p_value(self, type='sphericity_assumed'):
    #     if type=='sphericity_assumed':
    #         return self.p
    #     if type=='GG':
    #         return self.pGG
    #     elif type=='GGX':
    #         return self.pGGX
    #     elif type=='HF':
    #         return self.pHF

class DatasetANOVA1rm(_DatasetANOVA):
    def __init__(self):
        self.rm       = True  #repeated measures
        super(DatasetANOVA1rm, self).__init__()
        self.design   = 'One-way repeated measures ANOVA'
        self.testname = 'anova1rm'
    def get_data(self):
        return self.Y, self.A, self.SUBJ

class DatasetANOVA2(_DatasetANOVA):
    def __init__(self):
        self.rm       = False  #repeated measures
        super(DatasetANOVA2, self).__init__()
        self.design   = 'Two-way ANOVA'
        self.testname = 'anova2'
    def get_data(self):
        return self.Y, self.A, self.B
    def print_variables_R_format(self):
        self._printRs(self.get_data(), ['Y','A','B'])
class DatasetANOVA2nested(DatasetANOVA2):
    def __init__(self):
        super(DatasetANOVA2nested, self).__init__()
        self.design   = 'Two-way ANOVA (nested)'
        self.testname = 'anova1nested'
class DatasetANOVA2rm(DatasetANOVA2):
    def __init__(self):
        self.rm       = True  #repeated measures
        super(DatasetANOVA2rm, self).__init__()
        self.design   = 'Two-way repeated measures ANOVA'
        self.testname = 'anova2rm'
    def get_data(self):
        return self.Y, self.A, self.B, self.SUBJ
class DatasetANOVA2onerm(DatasetANOVA2rm):
    def __init__(self):
        super(DatasetANOVA2onerm, self).__init__()
        self.design   = 'Two-way ANOVA (repeated measures on one factor)'
        self.testname = 'anova1onerm'



class DatasetANOVA3(_DatasetANOVA):
    def __init__(self):
        self.rm       = False  #repeated measures
        super(DatasetANOVA3, self).__init__()
        self.design   = 'Three-way ANOVA'
        self.testname = 'anova3'
    def get_data(self):
        return self.Y, self.A, self.B, self.C
class DatasetANOVA3nested(DatasetANOVA3):
    def __init__(self):
        super(DatasetANOVA3nested, self).__init__()
        self.design   = 'Three-way ANOVA (nested)'
        self.testname = 'anova3nested'
class DatasetANOVA3rm(DatasetANOVA3):
    def __init__(self):
        self.rm       = True  #repeated measures
        super(DatasetANOVA3rm, self).__init__()
        self.design   = 'Three-way ANOVA (repeated measures on all factors)'
        self.testname = 'anova3rm'
    def get_data(self):
        return self.Y, self.A, self.B, self.C, self.SUBJ
    def print_variables_R_format(self):
        self._printRs(self.get_data(), ['Y','A','B','C','SUBJ'])
class DatasetANOVA3onerm(DatasetANOVA3rm):
    def __init__(self):
        self.rm       = True  #repeated measures
        super(DatasetANOVA3onerm, self).__init__()
        self.design   = 'Three-way ANOVA (repeated measures on one factor)'
        self.testname = 'anova3onerm'
class DatasetANOVA3tworm(DatasetANOVA3rm):
    def __init__(self):
        super(DatasetANOVA3tworm, self).__init__()
        self.design   = 'Three-way ANOVA (repeated measures on two factors)'
        self.testname = 'anova3tworm'





class DatasetCCA(_DatasetX2):
    def __init__(self):
        super(DatasetCCA, self).__init__()
        self.design   = "Canonical Correlation Analysis"
        self.testname = 'cca'
    def get_data(self):
        return self.Y, self.x



class DatasetHotellings1(_DatasetT2):
    def __init__(self):
        super(DatasetHotellings1, self).__init__()
        self.design   = "One-sample Hotelling's T2 test"
        self.testname = 'hotellings'
    def get_data(self):
        return self.Y, self.mu
class DatasetHotellings2(_DatasetT2):
    def __init__(self):
        super(DatasetHotellings2, self).__init__()
        self.design   = "Two-sample Hotelling's T2 test"
        self.testname = 'hotellings2'
    def get_data(self):
        return self.YA, self.YB
class DatasetHotellingsPaired(DatasetHotellings2):
    def __init__(self):
        super(DatasetHotellingsPaired, self).__init__()
        self.design   = "Paired Hotelling's T2 test"
        self.testname = 'hotellings_paired'



class DatasetMANOVA1(_DatasetX2):
    def __init__(self):
        super(DatasetMANOVA1, self).__init__()
        self.design   = "One-way MANOVA"
        self.testname = 'manova1'
    def get_data(self):
        return self.Y, self.A




class _CI(object):
    def get_expected_results_as_string(self):
        s      = '  (Expected results)\n'
        s     += '   ci        :  (%.5f, %.5f)\n' %self.ci
        return s

class DatasetCI1(_CI, _DatasetT):
    design   = 'One-sample CI'
    testname = 'ci_onesample'
    mu       = 0
    ci       = (0, 0)
    def get_data(self):
        return self.Y, self.mu

class DatasetCIpaired(_CI, _DatasetT):
    design   = 'Paired-sample CI'
    testname = 'ci_pairedsample'
    YA       = None
    YB       = None
    def get_data(self):
        return self.YA, self.YB

class DatasetCI2(_CI, _DatasetT):
    design   = 'Two-sample CI'
    testname = 'ci_twosample'
    YA       = None
    YB       = None
    def get_data(self):
        return self.YA, self.YB







class DatasetT1(_DatasetT):
    design   = 'One-sample t test'
    testname = 'ttest'
    mu       = None
    def get_data(self):
        return self.Y, self.mu

class DatasetT2(_DatasetT):
    design   = 'Two-sample t test'
    testname = 'ttest2'
    YA       = None
    YB       = None
    A        = None
    def get_data(self):
        return self.YA, self.YB

class DatasetTpaired(DatasetT2):
    design   = 'Paired t test'
    testname = 'ttest_paired'

class DatasetRegress(_DatasetT):
    design  = 'Simple linear regression OK?'
    x       = None
    def get_data(self):
        return self.Y, self.x
    def get_expected_results_as_string(self):
        s      = '  (Expected results)\n'
        s     += '   %s          :  %s\n' %(self.STAT, self.z)
        s     += '   df         :  %s\n' %str(self.df)
        s     += '   r          :  %s\n' %str(self.r)
        s     += '   p          :  %s\n' %str(self.p)
        return s






