
########################### For Authenticafication ######################################
import configparser
from sqlalchemy import create_engine

config = configparser.ConfigParser()
config.read('config.txt')

engine = create_engine(config.get('database', 'con'))


########################### Bar and Scatter config settings #######################################
BAR_PLOT_CONFIG = {
    "displaylogo": False,
    "displayModeBar": "hover",
    "modeBarButtonsToRemove": [
    	"zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "toggleSpikelines"
    ],
    # "toImageButtonOptions":{"width": None, "height": None,"format":["png, jpeg"]},
}

PIE_PLOT_CONFIG = {
    "displaylogo": False,
} 
########################### Rename some df indexes #######################################
card_mapping ={'P':'Primary Card', 'S':'Supplementary Card'}
Account_status_mapping={0:'Active',1:'Inactive',2:'Closed',3:'Dormant'}

GENDER_MAPPING = {'M': 'Male', 'F':'Female', 'O':'Other'}

SBU_MAPPING = {'R': 'Retail', 'S':'MSME', 'C':'Corporate'}

CHANNELS_MAPPING = {
    "atm": "Automated Teller Machine",
    "ib": "Internet Banking",
    "pbi": "Branch Processed",
    "mb": "Mobile Banking",
    "ocb": "Omni Corporate Banking",
    "orb": "Omni Retail Banking",
    "pos": "Point of Sales",
    "pnp": "MTN/Tigo Push & Pull"
}

ACCOUNT_TYPE_MAPPING = {
    'ODA': 'Overdraft',
    'CAA': 'Current',
    'SBA': 'Saving',
    'TDA': 'Term Deposit',
    'LAA': 'Loan'
}


SEGMENTS_MAPPING = {
    "PERS": "PERSONAL",
    "LLC": "LIMITED LIABILITY COMPANY",
    # "PRSP": "",
    "STAF": "STAFF",
    "PREM": "PREMIUM",
    # "TRST": "",
    "GOVT": "GOVERNMENTAL",
    "NGO": "NON GOVERNMENTAL ORGANISATION",

}

branch_name_mapping={
    "RW01002010":"Kigali Branch",         
    "RW01002012":"Umubano",
    "RW01002016":"Remera ",
    "RW01002023":"Nyabugogo",
    "RW01002019":"Nyamirambo ",
    "RW01002011":"Kigali City Market",
    "RW01002017":"Huye ",
    "RW01002027":"Rubavu ",
    "RW01002031":"Musanze",
    "RW01002025":"Karongi",
    "RW01002022":"Rusizi",
    "RW01002038":"Rwamagana",
    "RW01002012":"Kigali Heights",
    "RW01002021":"CHIC",
    "RW01002034":"Gicumbi",
    "RW01002099":"Head office",
}


push_MAPPING = {
    "B2W": "Bank to wallet",
    "W2B": "Wallet to bank",
}

tran_type_descr={
    "EFA":"Adhoc Local Payments-EFT",
    "EFP":"Local Payments-EFT",
    "IBP":"Initiate Bill Payment",
    "LAP":"Loan Account Payment",
    "MMA":"Adhoc Mobile Money Payments",
    "MMP":"Mobile Money Payment",
    "OWN":"Own Accounts",
    "PMT":"Top Up/Recharges",
    "RMA":"Adhoc Payment to International Accounts(SWIFT)",
    "RMP":"Transfer to International Accounts(SWIFT)",
    "RRA":"RRA Payment",
    "TIA":"Adhoc Local Payments-RTGS",
    "TIP":"Local Payments - RTGS",
    "TPA":"Within Bank- Adhoc",
    "XFR":"Within Bank",
}


Scheme_code_desc={
 "CAL01":"Yng Prof Bundle Caa - Lcy",
"ODL02":"Current Account Retail",
"ODL01":"Current Account Company",
"CAL04":"Staff Caa - Lcy",
"CAL05":"Credit Cards",
"SBL01":"Easy Smart Savers  - Lcy",
"CAL02":"Student Bundle Caa - Lcy",
"SBL08":"Student Bundle Sba - Lcy",
"SBL06":"Monthly Smart Savers - Lcy",
"SBL02":"Young Savers - Lcy",
"SBL07":"Yng Prof Bundle Sba - Lcy",
"SBL13":"SBL13",
"TDL02":"Term Deposit - Lcy",
"CAL03":"Malaika Bundle Caa - Lcy",
"SBL09":"Malaika Bundle Sba - Lcy",
"CAL08":"Written Off -Caa Accounts",
"CAF08":"Writtenoff Caa - Fcy",
"CAL09":"Investors Bundle - CAA - LCY",
"CAF04":"Staff Caa - Fcy",
"CAL07":"Non Staff Caa - Lcy",
"CAF07":"Non Staff Caa - Fcy",
"SBF01":"Easy Smart Savers - Fcy",
"TDL01":"Flexi Deposit - Lcy",
"TDF02":"Term Deposit - Fcy",
"CAF06":"Malaika Bundle Caa - Fcy",
"CAF09":"Investor  Bundle CAA - FCY",
"SBF06":"Monthly Smart Savers - Fcy",
}
