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
        'mfg'    :['BL12', 'BL13', 'BL14', 'BL15', 'CL7', 'CL8', 'CL9', 'CL10', 'CL11', 'CL12', 'CL13', 'CL14'] ,
        'sfg'    :[],
        'ec'     :['GL1', 'GL2', 'OR1', 'OR2']        
        
    },    
    'BJH021': {
        'hc'     :['B1', 'B2',  'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
        'ofc'    :['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10'],
        'amyg'   :['A1', 'A2', 'A3', 'A4', 'A5', 'O1', 'O2', 'O3', 'O4', 'O5'],
        'cing'   :['L1', 'L2', 'L3', 'L4'],
        'sgACC'  :[],
        'dACC'   :['L1', 'L2', 'L3', 'L4'], # all dacc
        'insula' :['A8', 'A9', 'A10', 'I2', 'I3', 'I4', 'N4', 'N5', 'N6', 'N7', 'N8', 'OR8'],
        'dlpfc'  :['L11', 'L12', 'L13', 'L14', 'N12', 'N13', 'N14', 'N15', 'N16'], # all mfg
        'mfg'    :['L11', 'L12', 'L13', 'L14', 'N12', 'N13', 'N14', 'N15', 'N16'], # all mfg
        'sfg'    :[], # all mfg
        'ec'     :[]        
        
    },
    'BJH025': {
        'hc'     :['HL1', 'HL2', 'HR1', 'HR2', 'I1', 'I2', 'I3', 'I4'],
        'ofc'    :['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'B2', 'B3'],
        'amyg'   :['C1', 'C2', 'GL1', 'GL2', 'GL3', 'GL4', 'GL5', 'GR1', 'GR2', 'GR3', 'GR4', 'GR5'],
        'cing'   :['B10'],
        'sgACC'  :['B10'],
        'dACC'   :[],
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

        
    },
    'BJH026': {
        'hc'     :['HL1', 'HL2', 'IL1', 'IL2', 'IL3'],
        'ofc'    :['AL6'],
        'amyg'   :['GL1', 'GL2', 'GL3', 'GR1', 'GR2', 'GR3', 'GR4'],
        'insula' :['LL1', 'LL2', 'CL2', 'CL3', 'BL4', 'BL5', 'BL6', 'BL7'],
        'cing'   :['AL1', 'AL2', 'AL3'],
        'sgACC'  :['AL1', 'AL2', 'AL3'],
        'dACC'   :[],
        'ec'     :['JL1', 'JL2'],
        'dlpfc'  :['BL12', 'BL13', 'BL14', 'BL15'],
        'mfg'    :['BL12', 'BL13', 'BL14', 'BL15'],
        'sfg'    :[]

        
    },
    'BJH027': {
        'hc'     :['HL1', 'HL2', 'HL3', 'HL4', 'HL5', 'HR1', 'HR2', 'HR3', 'HR4', 'HR5', 'HR6', 'JL1', 'JL2', 'JR1', 'JR2', 'JR3', ],
        'ofc'    :['AL1', 'AL2', 'AL3', 'AL4', 'AL5', 'AL6', 'AL7', 'AL8', 'AL9', 'AL10', 'AL11', 'AL12', 'AL13', 'AL14'],
        'amyg'   :['BL1', 'BL2', 'BL3', 'GL1', 'GL2', 'GL3', 'GL4', 'GR1', 'GR2', 'GR3', 'GR4', 'GR5'],
        'insula' :['BL4', 'BL5', 'BL6', 'BL7', 'BL8', 'BL9', 'CL9', 'GL7', 'GR8', 'LL8', 'LL9'],
        'cing'   :[],
        'sgACC'  :[],
        'dACC'   :[],
        'ec'     :['LL1', 'LL2'],
        'dlpfc'  :['BL13', 'BL14', 'BL15', 'BL16'],
        'mfg'    :['BL13', 'BL14', 'BL15', 'BL16'],
        'sfg'    :[]

        
    },    
    'BJH029': {
        'hc'     :['B\'1', 'B\'2', 'B\'3', 'B\'4', 'B\'5', 'B\'6', 'B1', 'B2', 'B3', 'B4', 'B5', 'C\'1', 'C\'2'],
        'ofc'    :['D\'1', 'D\'2', 'D\'3', 'D\'4', 'D\'5', 'D\'7'],
        'amyg'   :['A\'1', 'A\'2', 'A\'3', 'A\'4', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'],
        'insula' :['A8', 'A9', 'A10', 'G\'8', 'M\'8', 'M\'9', 'M\'10', 'M\'11'],
        'cing'   :[],
        'sgACC'  :[],
        'dACC'   :[],
        'ec'     :['F\'1', 'F\'2', 'F\'3', 'H\'1', 'H\'2', 'H\'3'],
        'dlpfc'  :[],
        'mfg'    :[],
        'sfg'    :[]

        
    },    
    'BJH039': {
        'hc'     :['GR3', 'GR4', 'GR5', 'GR6', 'ML1', 'ML2', 'ML3', 'HR2', 'HR3', 'HR4', 'LL1', 'LL2', 'LL3', 'LL4', 'IR2', 'IR3', 'IR4', 'IR5'],
        'ofc'    :['AR3', 'AR5', 'AR6', 'AR7', 'AR8', 'AR9', 'BR1', 'BR2', 'BR3', 'BR4', 'BR5', 'BR6', 'BR7', 'BR8', 'BR9', 'BR10'],
        'amyg'   :['KL1', 'KL2', 'KL3', 'KL4', 'KR1', 'GR1', 'GR2'],
        'insula' :[],
        'cing'   :['AR1', 'AR2', 'ER1', 'ER2', 'ER3', 'ER4', 'ER5', 'ER6', 'ER7', 'ER8'],
        'sgACC'  :['AR1', 'AR2'],
        'dACC'   :['ER1', 'ER2', 'ER3', 'ER4', 'ER5', 'ER6', 'ER7', 'ER8'],
        'ec'     :['IR1'],
        'dlpfc'  :['CR4', 'CR5', 'CR6', 'CR7', 'CR8', 'CR9', 'DR6', 'DR7', 'DR8', 'DR9', 'DR10', 'DR11', 'ER9', 'ER10', 'ER12', 'ER13'],
        'mfg'    :['CR4', 'CR5', 'CR6', 'CR7', 'CR8', 'CR9', 'DR6', 'DR7', 'DR8', 'DR9', 'DR10', 'DR11', 'ER9', 'ER10', 'ER12', 'ER13'],
        'sfg'    :[]

        
    },    
    'BJH041': {
        'hc'     :['BL2', 'BL3', 'BL4', 'BL5', 'CL1', 'CL2', 'DL4'],
        'ofc'    :['GL1', 'GL2', 'GL3', 'GL4', 'GL5'],
        'amyg'   :['AL2', 'AL3', 'AL4', 'AL5', 'AL6'],
        'insula' :['HL2', 'HL3', 'NL9', 'NL10'],
        'cing'   :[],
        'sgACC'  :[],
        'dACC'   :[],
        'ec'     :['AL1', 'BL1', 'EL1', 'EL2', 'EL3'],
        'dlpfc'  :[],
        'mfg'    :[],
        'sfg'    :[]

        
    },    
    'LL14': {
        'hc'     :['LA1', 'LH1', 'LHP1', 'RH1'],
        'ofc'    :['LOF1', 'ROF1'],
        'amyg'   :['LA2', 'RA1', 'RA2'],
        'insula' :[],
        'cing'   :[],
        'sgACC'  :[],
        'dACC'   :[],
        'ec'     :[],
        'dlpfc'  :['LOF8', 'LOF9', 'LOF10', 'LOF11', 'LOF12', 'LAC7', 'LAC8', 'LAC9', 'RMC6', 'RMC7', 'RMC8', 'ROF7', 'ROF8', 'ROF9', 'ROF10'],
        'mfg'    :['LOF8', 'LOF9', 'LOF10', 'LOF11', 'LOF12', 'LAC7', 'LAC8', 'LAC9', 'ROF7', 'RMC6', 'RMC7', 'RMC8'],
        'sfg'    :['ROF7', 'ROF8', 'ROF9', 'ROF10']

        
    },    
    'LL16': {
        'hc'     :['LA1', 'LA2', 'LA3', 'LH1', 'LH2', 'LHP1'],
        'ofc'    :['LOF1', 'ROF1', 'ROF3'],
        'amyg'   :[],
        'insula' :[],
        'cing'   :['LOF2', 'LOF3', 'LAC1', 'LAC2'],
        'sgACC'  :['LOF2', 'LOF3'],
        'dACC'   :['LAC1', 'LAC2'],
        'ec'     :['RTL1'],
        'dlpfc'  :['LOF10', 'LOF11', 'LOF12', 'LAC8', 'LAC9', 'LMC9', 'ROF9', 'ROF10', 'ROF11', 'RAC9', 'LAC6', 'LAC7', 'LMC6', 'LMC7'],
        'mfg'    :['LOF10', 'LOF11', 'LOF12', 'LAC8', 'LAC9', 'LMC9', 'ROF9', 'ROF10', 'ROF11', 'RAC9'],
        'sfg'    :['LAC6', 'LAC7', 'LMC6', 'LMC7']

        
    },    
    'LL17': {
        'hc'     :['LH1', 'LH2', 'RA1', 'RA2'],
        'ofc'    :['ROF1'],
        'amyg'   :['LA1', 'LA2'],
        'insula' :[],
        'cing'   :['LOF1'],
        'sgACC'  :['LOF1'],
        'dACC'   :[],
        'ec'     :[],
        'dlpfc'  :['LOF10', 'LOF11', 'ROF8', 'ROF9'],
        'mfg'    :['LOF10', 'LOF11', 'ROF8', 'ROF9'],
        'sfg'    :[]

        
    },    
    'LL19': {
        'hc'     :['RH2', 'RH3'],
        'ofc'    :['ROF1', 'ROF2', 'ROF3', 'LOF1'],
        'amyg'   :['RA1', 'RA2', 'RA3'],
        'insula' :[],
        'cing'   :['LOF2'],
        'sgACC'  :['LOF2'],
        'dACC'   :[],
        'ec'     :['RH1'],
        'dlpfc'  :['RAC5', 'RAC6', 'RAC7', 'RAC8', 'ROF9', 'ROF10', 'ROF11', 'LOF9', 'LOF10'],
        'mfg'    :['RAC5', 'RAC6', 'RAC7', 'RAC8', 'ROF9', 'ROF10', 'ROF11', 'LOF9', 'LOF10'],
        'sfg'    :[]

        
    },
    'BJH046': {
        'hc'     :['BL1', 'BL2'],
        'ofc'    :['DL1', 'DL2', 'DL3', 'DL4', 'DL5', 'DL6', 'DL7', 'DL8', 'DL9', 'DL10', 'DL11', 'DL12', 'EL1', 'EL2', 'EL3', 'EL4'],
        'amyg'   :['AL1', 'AL2', 'AL3', 'AL4'],
        'insula' :['EL6', 'EL7', 'FL10', 'FL11'],
        'cing'   :['GL3', 'GL4', 'GL5', 'GL6', 'GL7', 'GL8', 'GL9', 'HL1', 'HL2', 'HL3', 'IL1', 'IL2', 'IL3', 'IR1', 'IR2', 'IR3'],
        'sgACC'  :[],
        'dACC'   :['GL3', 'GL4', 'GL5', 'GL6', 'GL7', 'GL8', 'GL9', 'HL1', 'HL2', 'HL3', 'IL1', 'IL2', 'IL3', 'IR1', 'IR2', 'IR3'],
        'ec'     :[],
        'dlpfc'  :['GL12', 'HL5', 'HL8', 'HL9', 'HL10', 'HL11', 'LL1', 'LL2', 'LL3', 'LL4', 'LL5', 'LL6', 'LL7', 'LL8', 'ML1', 'ML2', 'ML3', 'ML4', 'ML5', 'ML6', 'ML7', 'ML8', 'ML9', 'ML10', 'NL1', 'NL2', 'NL3', 'NL4', 'NL5', 'NL7', 'NL8', 'NL9', 'NL10'],
        'mfg'    :['GL12', 'HL8', 'HL9', 'HL10', 'HL11', 'LL6', 'LL7', 'LL8', 'ML8', 'ML9', 'ML10', 'NL9', 'NL10'],
        'sfg'    :['HL5', 'LL1', 'LL2', 'LL3', 'LL4', 'LL5', 'ML1', 'ML2', 'ML3', 'ML4', 'ML5', 'ML6', 'ML7', 'NL1', 'NL2', 'NL3', 'NL4', 'NL5', 'NL7', 'NL8']

        
    },    
    'BJH050': {
        'hc'     :['BL1', 'BL2', 'BL3', 'BL4', 'BL5', 'BR1', 'BR2', 'BR3', 'CR1', 'CR2', 'CR3', 'GR1', 'GR2'],
        'ofc'    :['LR1', 'LR2', 'LR3', 'LR4', 'LR6', 'LR8', 'LR9', 'LR10', 'LR11', 'LR12'],
        'amyg'   :['AR4', 'AR5', 'AR6'],
        'insula' :['GR2', 'GR3', 'KR3', 'KR4', 'KR5', 'KR6'],
        'cing'   :['MR1', 'MR2', 'MR3', 'MR4'],
        'sgACC'  :[],
        'dACC'   :['MR1', 'MR2', 'MR3', 'MR4'],
        'ec'     :[],
        'dlpfc'  :['MR9', 'MR10', 'MR11', 'M12', 'MR13'],
        'mfg'    :['MR9', 'MR10', 'MR11', 'M12', 'MR13'],
        'sfg'    :[]

        
    },  
    'BJH051': {
        'hc'     :['BL1', 'BL2', 'BL3', 'BL4', 'BR1', 'BR2', 'CL1', 'CL2', 'CL3', 'CL4', 'CL5'],
        'ofc'    :['LL1', 'LL2', 'LL3', 'LL4', 'LL5', 'LL6', 'LL7', 'LL8', 'LL9', 'LL10', 'LL11', 'LL12'],
        'amyg'   :['AL1', 'AL2', 'AL3', 'AL4', 'AL5', 'AL6', 'AR1', 'AR2', 'AR3'],
        'insula' :['IL4', 'IL5', 'JL4', 'JL5', 'KL2', 'KL3', 'KL4', 'KL5', 'KL6'],
        'cing'   :['ML1'],
        'sgACC'  :[],
        'dACC'   :['ML1'],
        'ec'     :[],
        'dlpfc'  :['ML5', 'ML6', 'ML7', 'ML8', 'ML9', 'ML10'],
        'mfg'    :['ML5', 'ML6', 'ML7', 'ML8', 'ML9', 'ML10'],
        'sfg'    :[]

        
    },    
    'SLCH018': {
        'hc'     :['`B1', '`B2', '`B3', '`C1', '`C2', '`C3', '`C4', '`C5'],
        'ofc'    :['`G1', '`G2', '`G3', '`G4', '`G5', '`G6', '`G7', '`G8', '`G9'],
        'amyg'   :['`A1', '`A2', '`A3', 'A4', '`A5', 'J`1', 'J`2', 'J`3', 'J`4', 'J`5', 'K`1', 'K`2', 'K`3', 'K`4', 'K`5'],
        'insula' :[],
        'cing'   :[],
        'sgACC'  :[],
        'dACC'   :[],
        'ec'     :[],
        'dlpfc'  :[],
        'mfg'    :[],
        'sfg'    :[]

        
    },   
    'BJH024': {
        'hc'     :['HL1', 'HL2', 'HL3', 'HL4', 'HL5', 'HR1', 'IL1', 'IL2', 'IL3', 'IL4', 'IR1', 'IR2', 'IR3', 'IR4', 'IR5'],
        'ofc'    :['AL1', 'AL2', 'AL3', 'AL4', 'AL5', 'AL6', 'AL7', 'AL8', 'AL9', 'AL10', 'AR1', 'AR2', 'AR3', 'AR4', 'AR5', 'AR6', 'AR7', 'AR8', 'AR9', 'BL1', 'BL2', 'BL3', 'BR1', 'BR2', 'BR3', 'BR4'],
        'amyg'   :['GL1', 'GL2', 'GL3', 'GL4', 'GR1'],
        'insula' :['CL4', 'CL5', 'CL6', 'CL7', 'CR5', 'CR6', 'CR7', 'CR8', 'GL7', 'GL8', 'GR3', 'GR4'],
        'cing'   :['BL4', 'BL5', 'BL6', 'BL7', 'BL8', 'BL9', 'BL10', 'BL11', 'BL12', 'BR5', 'BR6', 'BR7', 'BR8', 'BR9', 'BR10'],
        'sgACC'  :['BL4', 'BL5', 'BL6', 'BL7'],
        'dACC'   :['BL8', 'BL9', 'BL10', 'BL11', 'BL12'],
        'ec'     :[],
        'dlpfc'  :['BL14', 'BL15', 'BL16', 'BR11', 'BR12', 'BR13', 'BR14', 'BR15', 'CL13', 'CL14', 'CL15', 'CL16', 'CR12', 'CR13', 'CR14', 'CR15', 'CR16'],
        'mfg'    :['CL13', 'CL14', 'CL15', 'CL16', 'CR12', 'CR13', 'CR14', 'CR15', 'CR16'],
        'sfg'    :['BR11', 'BR12', 'BR13', 'BR14','BL14', 'BL15', 'BL16']

        
    },    
    'BJH017': {
        'hc'     :['BR1', 'BR2', 'BR3', 'BR4', 'BR5', 'BR6', 'BR7', 'CR1', 'CR2', 'CR3', 'CR4', 'CR5', 'CR6', 'CR7', 'OL1', 'OL2', 'OL3', 'OL4', 'OL5', 'OL6'],
        'ofc'    :['MR4', 'MR6', 'MR7', 'MR8', 'MR9', 'MR10', 'MR12','MR14', 'MR15', 'MR16'],
        'amyg'   :['AR1', 'AR2', 'AR3', 'AR4', 'AR5'],
        'insula' :['NR3', 'NR4', 'NR5', 'NR6', 'NR7', 'NR8'],
        'cing'   :['MR1', 'MR2', 'MR3'],
        'sgACC'  :['MR1', 'MR2', 'MR3'],
        'dACC'   :[],
        'ec'     :[],
        'dlpfc'  :[],
        'mfg'    :[],
        'sfg'    :[]

        
    }                                      
}