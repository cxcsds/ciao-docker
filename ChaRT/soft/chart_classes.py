import os
import sys
import stat
import tempfile
import pickle
import xml.etree.ElementTree as ET
from datetime import datetime

from pycrates import read_file
from coords.format import *

# Load location specific info
from chart_config_v2 import *


class TmpDir ( str ):
    """
    wrap dir name so that we make sure that tmp dir is clean when
    application exists.
    """
    def __del__(self):
        for pp in os.listdir( self.__str__() ):
            os.unlink( os.path.join( self.__str__(), pp ))
        os.rmdir( self.__str__() )


class Aspect( object ):
    """
    Hold all things aspect related
    """
    def __init__(self):
        pass
        
    def get_ra_dec_roll( self ):
        return self.ra_pnt, self.dec_pnt, self.roll_pnt
    
    def get_start_stop_times(self):
        return self.tstart, self.tstop
    
    
class AspectFile( Aspect ):
    """
    Aspect stuff retrieved from a file
    """
    def __init__(self, infile ):
        tab = read_file( infile )        
        # Yes _NOM values in asol file are the _PNT values!
        self.ra_pnt = tab.get_key_value("RA_NOM")
        self.dec_pnt = tab.get_key_value("DEC_NOM")
        self.roll_pnt = tab.get_key_value("ROLL_NOM")
        self.tstart = tab.get_key_value("TSTART")
        self.tstop = tab.get_key_value("TSTOP")
        self.infile = infile
        musthave = ["time", "ra", "dec", "roll", "dy", "dz", "dtheta", "q_att"]

        if not all( [x in tab.get_colnames() for x in musthave]):
            raise IOError("Bad Stuff")


class AspectValue( Aspect ):
    """
    Aspect stuff input by values
    """
    def __init__( self, ra, dec, roll, exposure ):        
        try:
            self.ra_pnt = float(ra)
            self.dec_pnt = float(dec)
        except:
            try:
                self.ra_pnt = ra2deg(ra)
                self.dec_pnt = dec2deg(dec)
            except:
                raise RuntimeError("Unknown format for the aspect RA and DEC values")

        self.roll_pnt = float(roll)
        if self.roll_pnt < 0.0 or self.roll_pnt > 360.0:
            raise RuntimeError("ROLL should be between 0 and 360 degrees")

        self.tstart = 0
        self.tstop = float(exposure)*1000 # seconds
        
        if self.tstop <= 0:
            raise RuntimeError("Exposure time must be greater than 0")
        if self.tstop > 200000:
            raise RuntimeError("Exposure time must be less than 200ksec")
        

        self.infile = "none"


class Spectrum( object ):    
    pass
    
class SpectrumFile( Spectrum ):
    """
    Spectrum taken from a file
    """    
    def __init__( self, infile ):
        self.infile = infile
        self.mono = None
        self.flux = None
        self.check_file()
    
    def set_params( self, tool ):
        setattr( tool, "spectrumfile", self.infile )
        
    def check_file(self):
        try:
            tab = read_file(self.infile)
        except:
            raise IOError("Uploaded spectrum is an invalid format")
        
        if len( tab.get_colnames() ) != 3:
            raise IOError("""Spectrum must have 3 columns:  Energy_lo, Energy_hi, and Flux.
                The sherpa commands with the required normalization are shown in this thread:

                https://cxc.cfa.harvard.edu/ciao/threads/prep_chart/index.html#upload_spectrum
                """)
    def noop(self):
        pass
        
                
        
class SpectrumMono( Spectrum ):
    """
    Spectrum taken from individual values
    """
    def __init__( self, mono, flux ):
        self.mono = float(mono)
        self.flux = float(flux)
        self.infile = None
        if self.mono < 0.2:
            raise ValueError("Monochromatic energy must be > 0.2 keV")
        if self.mono > 10.0:
            raise ValueError("Monochromatic energy must be < 10.0 keV")
        
        if self.flux < 1e-9 or self.flux > 1e-2:
            raise ValueError("Flux value should be between 1e-2 and 1e-9")
        
    
    def set_params( self, tool ):
        setattr( tool, "monoenergy", self.mono)
        setattr( tool, "flux", self.flux )


class Realizations(object):
    pass
    

class Iterations(Realizations):
    def __init__(self, niter):
        self.niter = niter
        self.nrays = None
        if int(self.niter) < 1:
            raise ValueError("Number of iterations must be >= 1")
        if int(self.niter) > 500:
            raise ValueError("Number of iterations must be < 500")
        
    def set_params(self, tool):
        tool.numiter = self.niter
        tool.numrays = None

    
class Rays(Realizations):
    def __init__(self, numrays):
        self.nrays = numrays
        self.niter = None
        if int(self.nrays) < 1:
            raise ValueError("Number of rays must be >= 1")
        if int(self.nrays) > 1000000:
            raise ValueError("Number of rays must be < 1000000")
    
    def set_params(self, tool):
        tool.numrays = self.nrays
        tool.numiter = "INDEF"


