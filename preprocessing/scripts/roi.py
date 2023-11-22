ROIs = {
    'LL10': {
        'hc'     :['RH1', 'RH2', 'RHP1', 'LH1', 'LH2'],
        'ofc'    :['ROF1'],
        'amyg'   :['RA1', 'RA2'],
        'cing'   :['RAC1', 'RAC2', 'RAC3', 'LOF1', 'LAC1', 'LAC2'],
        'sgACC'  :['LOF1'],
        'dACC'   :['RAC1', 'RAC2', 'RAC3', 'LAC1', 'LAC2'],
        'insula' :[],
        'dlpfc'  :['ROF10', 'RAC6', 'RAC7', 'LOF8', 'LOF9', 'LOF10', 'LAC5', 'LAC6', 'LAC7', 'LAC8'],
        'mfg'    :['ROF10', 'RAC6', 'RAC7', 'LOF8', 'LOF9', 'LOF10', 'LAC5', 'LAC6', 'LAC7', 'LAC8'],
        'sfg'    :[],
        'ec'     :[]
        
    },
    'LL12': {
        'hc'     :['LH1', 'LH2', 'LHP1', 'LHP2', 'RH1'],
        'ofc'    :['ROF1'],
        'amyg'   :['LA1', 'LA2', 'LA3'],
        'cing'   :['LAC1'],
        'sgACC'  :[],
        'dACC'   :['LAC1'],
        'insula' :['LAI2', 'LAI3'],
        'dlpfc'  :['LAC6', 'LAC7', 'LAC8', 'LMC7', 'LMC8', 'ROF10', 'LOF8', 'LOF9', 'LOF10', 'LOF11', 'LOF12', 'LMC6'],
        'sfg'    :['LOF8', 'LOF9', 'LOF10', 'LOF11', 'LOF12', 'LMC6'], 
        'mfg'    :['LAC6', 'LAC7', 'LAC8', 'LMC7', 'LMC8', 'ROF10'], 
        'ec'     :[]
    },

    'LL13': {
        'hc'     :['LH1', 'RH1'],
        'ofc'    :['LOF1', 'ROF1'],
        'amyg'   :['LA1', 'LA2', 'RA1', 'RA2'],
        'cing'   :['LAC1', 'LAC2', 'RAC1'],
        'sgACC'  :[],
        'dACC'   :['LAC1', 'LAC2', 'RAC1'],    
        'insula' :[],
        'dlpfc'  :['LOF8', 'LOF9', 'LOF10', 'ROF9', 'ROF10', 'ROF11', 'ROF12', 'RAC7', 'RAC8', 'RAC9', 'RAC10', 'LAC5', 'LAC6', 'LAC7'],
        'sfg'    :['LAC5', 'LAC6', 'LAC7'], 
        'mfg'    :['LOF8', 'LOF9', 'LOF10', 'ROF9', 'ROF10', 'ROF11', 'ROF12', 'RAC7', 'RAC8', 'RAC9', 'RAC10'], 
        'ec'     :[]        

    },
    'BJH016': {
        'hc'     :['OR3', 'OR4', 'OR5', 'OR6', 'OR7', 'IL1', 'IL2', 'IL3', 'IL4', 'HL1', 'HL2', 'HL3', 'HL4', 'HL5', 'HL6'],
        'ofc'    :['AL1', 'AL2', 'AL3', 'AL4', 'AL5', 'AL6', 'AL7', 'AL9', 'AL10', 'AL11', 'AL12', 'AL13', 'AL14', 'AL15'],
        'amyg'   :['GL2', 'GL3', 'GL4', 'GL5', 'GL6'],
        'cing'   :['CL1', 'CL2', 'CL3', 'CL4', 'AL3', 'AL4', 'AL5'],
        'sgACC'  :['AL3', 'AL4', 'AL5'],
        'dACC'   :['CL1', 'CL2', 'CL3', 'CL4'],
        'insula' :['BL1', 'BL2', 'BL3', 'BL4', 'BL5',  'BL6', 'BL7', 'BL8', 'BL9', 'LL1', 'LL2', 'LL3', 'LL4'],
        'dlpfc'  :['BL12', 'BL13', 'BL14', 'BL15', 'CL7', 'CL8', 'CL9', 'CL10', 'CL11', 'CL12', 'CL13', 'CL14'],
        'ec'     :['GL1', 'GL2', 'OR1', 'OR2']        
        
    },    
    'BJH021': {
        'hc'     :['B1', 'B2',  'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
        'ofc'    :['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10'],
        'amyg'   :['A1', 'A2', 'A3', 'A4', 'A5', 'O1', 'O2', 'O3', 'O4', 'O5'],
        'cing'   :['L1', 'L2', 'L3', 'L4'],
        'insula' :['A8', 'A9', 'A10', 'I2', 'I3', 'I4', 'N4', 'N5', 'N6', 'N7', 'N8', 'OR8'],
        'dlpfc'  :['L11', 'L12', 'L13', 'L14', 'N12', 'N13', 'N14', 'N15', 'N16'], # all mfg
        'ec'     :[]        
        
    },
    'BJH025': {
        'hc'     :['HL1', 'HL2', 'HR1', 'HR2', 'I1', 'I2', 'I3', 'I4'],
        'ofc'    :['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'B2', 'B3'],
        'amyg'   :['C1', 'C2', 'GL1', 'GL2', 'GL3', 'GL4', 'GL5', 'GR1', 'GR2', 'GR3', 'GR4', 'GR5'],
        'cing'   :['B10'],
        'insula' :['C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'GR7'],
        'dlpfc'  :['C13', 'C14', 'C15', 'C16', 'B13', 'B14', 'B15', 'B16'],
        'sfg'    :['B13', 'B14', 'B15', 'B16'],
        'mfg'    :['C13', 'C14', 'C15', 'C16'],
        'ec'     :['J1', 'J2', 'J3']        
        
    },  
    'SLCH002': {
        'hc'     :['K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'K7'],
        'ofc'    :['A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'B5', 'B6', 'B7', 'B8', 'B9'],
        'amyg'   :['i1', 'i2', 'i3', 'i4', 'i5'],
        'insula' :['C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'E2', 'E3', 'E4', 'F1', 'F2', 'F3'],
        'cing'   :['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4'], # all sgACC
        'sgACC'  :['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4'],
        'dACC'   :[],
        'ec'     :['H1', 'H2', 'H3', 'H4', 'L1', 'L2', 'L3', 'L4'], 
        'dlpfc'  :['C11', 'C12', 'C13', 'C14', 'C15', 'C16'], # all mfg    
        'mfg'    :['C11', 'C12', 'C13', 'C14', 'C15', 'C16'] ,
        'sfg'    :[]

        
    }    
}