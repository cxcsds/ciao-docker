
function onChangeCoordRadioCel()
{
    document.getElementById('src_ra').required=true;
    document.getElementById('src_dec').required=true;
    document.getElementById('src_theta').required=false;
    document.getElementById('src_phi').required=false;
}


function onChangeSrcRA()
{
    document.getElementById('coords_cel').checked=true;
    onChangeCoordRadioCel();
}


function onChangeSrcDec()
{
    document.getElementById('coords_cel').checked=true;
    onChangeCoordRadioCel();
}


function onChangeCoordRadioMSC()
{
    document.getElementById('src_ra').required=false;
    document.getElementById('src_dec').required=false;
    document.getElementById('src_theta').required=true;
    document.getElementById('src_phi').required=true;
}


function onChangeCoordTheta( me )
{
    document.getElementById('coords_msc').checked=true;
    onChangeCoordRadioMSC();
    if ((me.value<0)||(me.value>30)) { 
        alert('Theta must be between 0 and 30 arcmin.');
        me.value='';
        me.focus();
    }

}


function onChangeCoordPhi( me )
{
    document.getElementById('coords_msc').checked=true;
    onChangeCoordRadioMSC();
    if ((me.value<-360)||(me.value>360)) { 
        alert('Phi must be between -360 and 360 degrees.');
        me.value='';
        me.focus();

    }

}


function onChangeRadioSpectrumFile()
{
    document.getElementById('spectrum').required=true;
    document.getElementById('mono').required=false;
    document.getElementById('flux').required=false;
}


function onChangeSpectrumFile()
{
    document.getElementById('spectrum_file').checked=true; 
    onChangeRadioSpectrumFile();
}



function onChangeRadioMono()
{
    document.getElementById('spectrum').required=false;
    document.getElementById('mono').required=true;
    document.getElementById('flux').required=true;
}



function onChangeMonoEnergy(me)
{

    document.getElementById('spectrum_mono').checked=true;
    onChangeRadioMono();
    if ((me.value<0.2)||(me.value>10.0)) { 
        alert('Monochromatic energy must be between 0.2 and 10.0 keV.');
        me.value='';
        me.focus();
    }

}

function onChangeMonoFlux(me)
{
    document.getElementById('spectrum_mono').checked=true;
    onChangeRadioMono();
    if ((me.value<1.0e-9)||(me.value>1.0e-2)) { 
        alert('Flux must be between 1.0e-9 and 1.0e-2 photon/cm^2/sec.');
        me.value='';
        me.focus();
    }
}


function onChangeRadioAspectObi()
{
    document.getElementById('asol_obsid').required=true;
    document.getElementById('asol_file').required=false;
    document.getElementById('ra_pnt').required=false;
    document.getElementById('dec_pnt').required=false;
    document.getElementById('roll_pnt').required=false;
    document.getElementById('exposure').required=false;
}


function onChangeObsID(me)
{
    var list_of_multiobi = ['82','108','279','380','400','433','800','861','897','906','943','1411','1431','1456','1561','1578','2010','2042','2077','2365','2783','3057','3182','3764','4175','60879','60880','62249','62264','62796'];
    
    document.getElementById('asol_obi').checked=true;
    onChangeRadioAspectObi();

    if (list_of_multiobi.indexOf(me.value)>-1) {
        document.getElementById('asol_obinum').disabled=false;
        document.getElementById('asol_obinum').required=true;
    } else {
        document.getElementById('asol_obinum').disabled=true;
        document.getElementById('asol_obinum').required=false;
    }
    
    if ((me.value<1)||(me.value>65535)) { 
        alert('OBS_ID must be between 1 and 65535.');
        me.value='';
        me.focus();
    }

}


function onChangeObiNum(me)
{
    document.getElementById('asol_obi').checked=true;
    onChangeRadioAspectObi();
    if ((me.value<0)||(me.value>9)) { 
        alert('OBI_NUM must be between 0 and 9.');
        me.value='';
        me.focus();
    }

}


function onChangeRadioUploadAsol()
{
    document.getElementById('asol_obsid').required=false;
    document.getElementById('asol_file').required=true;
    document.getElementById('ra_pnt').required=false;
    document.getElementById('dec_pnt').required=false;
    document.getElementById('roll_pnt').required=false;
    document.getElementById('exposure').required=false;
}


function onChangeUploadAsol()
{
    document.getElementById('asol_upload').checked=true;
    onChangeRadioUploadAsol();    
}

function onChangeRadioOtherAsol()
{
    document.getElementById('asol_obsid').required=false;
    document.getElementById('asol_file').required=false;
    document.getElementById('ra_pnt').required=true;
    document.getElementById('dec_pnt').required=true;
    document.getElementById('roll_pnt').required=true;
    document.getElementById('exposure').required=true;
}

function onChangeRaPnt()
{
    document.getElementById('asol_other').checked=true;
    onChangeRadioOtherAsol();
}


function onChangeDecPnt()
{
    document.getElementById('asol_other').checked=true;
    onChangeRadioOtherAsol();
}


function onChangeRollPnt(me)
{
    document.getElementById('asol_other').checked=true;
    onChangeRadioOtherAsol();
    if ((me.value<0)||(me.value>360)) { 
        alert('ROLL must be between 0 and 360 degrees.');
        me.value='';
        me.focus();
    }
    
}


function onChangeExposure(me)
{
    document.getElementById('asol_other').checked=true;
    onChangeRadioOtherAsol();
    if ((me.value<1)||(me.value>200)) { 
        alert('Exposure time must be between 1 and 200 ksec.');
        me.value='';
        me.focus();
    }
}


function onChangeNumIter(me)
{
    document.getElementById('niter_check').checked=true;
    document.getElementById('nrays_check').required=false;
    if ((me.value<1)||(me.value>50)) { 
        alert('Number of iterations must be between 1 and 50.');
        me.value='1';
        me.focus();
    }
}


function onChangeNumRays(me)
{
    document.getElementById('nrays_check').checked=true;
    document.getElementById('niter_check').required=false;
    if ((me.value<1)||(me.value>1000000)) { 
        alert('Number of rays must be between 1 and 1000000.');
        me.value='10000';
        me.focus();
    }
}

