#!/usr/bin/python
from types import IntType,StringType
import sys
import re
def getCountryCode(value):
    """
    Return dictionary of information about country from input.

    The lists of country codes can be obtained from Wikipedia:
    http://en.wikipedia.org/wiki/ISO_3166-1

    Note: Three PAGER specific US earthquake regions have been added:
    'U.S. Earthquake Region California','XF','XFA','902'
    'U.S. Earthquake Region Western United States','XG','XGA','901'
    'U.S. Earthquake Region Central/Eastern United States','XH','XHA','903'

    @param value: Any of the following:
      - Two letter ISO country code (i.e., 'US' for United States)
      - Three letter ISO country code (i.e., 'USA' for United States)
      - Numeric ISO country code (i.e. 840 for United States)
      - String (preferably short) containing the name of the country.  Regular expressions will be used to attempt a match.
        NB:  The first potential match will be returned!
    @return: Dictionary containing the following values:
      - 'name' Full country name.
      - 'alpha2' Two letter ISO country code.
      - 'alpha3' Three letter ISO country code.
      - 'number' Numeric ISO country code.
    """
    doRegMatch = False
    if type(value) is StringType:
        if len(value) != 2 and len(value) != 3:
            doRegMatch = True
    elif type(value) is IntType:
        method = 'num'
        value = str(value)
    else:
        msg = 'Unsupported country search key %s with type %s' % (str(value),type(value))
        raise TypeError, msg
    clist = getCountryList()
    cdict = {'name':'','alpha2':'','alpha3':'','number':0,'shortname':''}
    for country in clist:
        if doRegMatch:
            s1 = re.search(value.lower(),country[0].lower())
            s2 = re.search(country[0].lower(),value.lower())
            if s1 is not None or s2 is not None:
                cdict['name'] = country[0]
                cdict['alpha2'] = country[1]
                cdict['alpha3'] = country[2]
                cdict['number'] = int(country[3])
                if len(country) == 5:
                    cdict['shortname'] = country[4]
                else:
                    cdict['shortname'] = country[0]
                break
        if value in country or value.upper() in country:
            cdict['name'] = country[0]
            cdict['alpha2'] = country[1]
            cdict['alpha3'] = country[2]
            cdict['number'] = int(country[3])
            if len(country) == 5:
                cdict['shortname'] = country[4]
            else:
                cdict['shortname'] = country[0]
            break
    return cdict
        
def getCountryList():
    """
    Return list of country information.
    
    Each entry in the list looks like this:
    ['Afghanistan','AF','AFG','4']

    @return: List of country lists, where each country list contains the following information:
      - Country name (i.e., 'Afghanistan')
      - Two letter ISO code (i.e., 'AF')
      - Three letter ISO code (i.e., 'AFG')
      - Numeric ISO code (i.e., '4')
    """
    country = []
    country.append(['Afghanistan','AF','AFG','4'])
    country.append(['the Aland Islands','AX','ALA','248'])
    country.append(['Albania','AL','ALB','8'])
    country.append(['Algeria','DZ','DZA','12'])
    country.append(['American Samoa','AS','ASM','16'])
    country.append(['Andorra','AD','AND','20'])
    country.append(['Angola','AO','AGO','24'])
    country.append(['Anguilla','AI','AIA','660'])
    country.append(['Antarctica','AQ','ATA','10'])
    country.append(['Antigua and Barbuda','AG','ATG','28'])
    country.append(['Argentina','AR','ARG','32'])
    country.append(['Armenia','AM','ARM','51'])
    country.append(['Aruba','AW','ABW','533'])
    country.append(['Australia','AU','AUS','36'])
    country.append(['Austria','AT','AUT','40'])
    country.append(['Azerbaijan','AZ','AZE','31'])
    country.append(['Bahamas','BS','BHS','44'])
    country.append(['Bahrain','BH','BHR','48'])
    country.append(['Bangladesh','BD','BGD','50'])
    country.append(['Barbados','BB','BRB','52'])
    country.append(['Belarus','BY','BLR','112'])
    country.append(['Belgium','BE','BEL','56'])
    country.append(['Belize','BZ','BLZ','84'])
    country.append(['Benin','BJ','BEN','204'])
    country.append(['Bermuda','BM','BMU','60'])
    country.append(['Bhutan','BT','BTN','64'])
    country.append(['Bolivia','BO','BOL','68'])
    country.append(['Bosnia and Herzegovina','BA','BIH','70'])
    country.append(['Botswana','BW','BWA','72'])
    country.append(['Bouvet Island','BV','BVT','74'])
    country.append(['Brazil','BR','BRA','76'])
    country.append(['the British Indian Ocean Territory','IO','IOT','86','Indian Ocean Territory'])
    country.append(['Brunei Darussalam','BN','BRN','96'])
    country.append(['Bulgaria','BG','BGR','100'])
    country.append(['Burkina Faso','BF','BFA','854'])
    country.append(['Burundi','BI','BDI','108'])
    country.append(['Cambodia','KH','KHM','116'])
    country.append(['Cameroon','CM','CMR','120'])
    country.append(['Canada','CA','CAN','124'])
    country.append(['Cape Verde','CV','CPV','132'])
    country.append(['the Cayman Islands','KY','CYM','136'])
    country.append(['the Central African Republic','CF','CAF','140'])
    country.append(['Chad','TD','TCD','148'])
    country.append(['Chile','CL','CHL','152'])
    country.append(['China','CN','CHN','156'])
    country.append(['Christmas Island','CX','CXR','162'])
    country.append(['the Cocos (Keeling) Islands','CC','CCK','166'])
    country.append(['Colombia','CO','COL','170'])
    country.append(['Comoros','KM','COM','174'])
    country.append(['Congo','CG','COG','178'])
    country.append(['the Democratic Republic of the Congo','CD','COD','180','Congo'])
    country.append(['the Cook Islands','CK','COK','184'])
    country.append(['Costa Rica','CR','CRI','188'])
    country.append(['Cote d''Ivoire','CI','CIV','384'])
    country.append(['Croatia','HR','HRV','191'])
    country.append(['Cuba','CU','CUB','192'])
    country.append(['Cyprus','CY','CYP','196'])
    country.append(['the Czech Republic','CZ','CZE','203'])
    country.append(['Denmark','DK','DNK','208'])
    country.append(['Djibouti','DJ','DJI','262'])
    country.append(['Dominica','DM','DMA','212'])
    country.append(['the Dominican Republic','DO','DOM','214'])
    country.append(['Ecuador','EC','ECU','218'])
    country.append(['Egypt','EG','EGY','818'])
    country.append(['El Salvador','SV','SLV','222'])
    country.append(['Equatorial Guinea','GQ','GNQ','226'])
    country.append(['Eritrea','ER','ERI','232'])
    country.append(['Estonia','EE','EST','233'])
    country.append(['Ethiopia','ET','ETH','231'])
    country.append(['the Falkland Islands (Malvinas)','FK','FLK','238','the Falklands'])
    country.append(['the Faroe Islands','FO','FRO','234'])
    country.append(['Fiji','FJ','FJI','242'])
    country.append(['Finland','FI','FIN','246'])
    country.append(['France','FR','FRA','250'])
    country.append(['French Guiana','GF','GUF','254'])
    country.append(['French Polynesia','PF','PYF','258'])
    country.append(['the French Southern Territories','TF','ATF','260'])
    country.append(['Gabon','GA','GAB','266'])
    country.append(['Gambia','GM','GMB','270'])
    country.append(['Georgia','GE','GEO','268'])
    country.append(['Germany','DE','DEU','276'])
    country.append(['Ghana','GH','GHA','288'])
    country.append(['Gibraltar','GI','GIB','292'])
    country.append(['Greece','GR','GRC','300'])
    country.append(['Greenland','GL','GRL','304'])
    country.append(['Grenada','GD','GRD','308'])
    country.append(['Guadeloupe','GP','GLP','312'])
    country.append(['Guam','GU','GUM','316'])
    country.append(['Guatemala','GT','GTM','320'])
    country.append(['Guernsey','GG','GGY','831'])
    country.append(['Guinea','GN','GIN','324'])
    country.append(['Guinea-Bissau','GW','GNB','624'])
    country.append(['Guyana','GY','GUY','328'])
    country.append(['Haiti','HT','HTI','332'])
    country.append(['the Heard Island and McDonald Islands','HM','HMD','334','Heard Islands'])
    country.append(['the Holy See (Vatican City State)','VA','VAT','336','Vatican City'])
    country.append(['Honduras','HN','HND','340'])
    country.append(['Hong Kong','HK','HKG','344'])
    country.append(['Hungary','HU','HUN','348'])
    country.append(['Iceland','IS','ISL','352'])
    country.append(['India','IN','IND','356'])
    country.append(['Indonesia','ID','IDN','360'])
    country.append(['the Islamic Republic of Iran','IR','IRN','364'])
    country.append(['Iraq','IQ','IRQ','368'])
    country.append(['Ireland','IE','IRL','372'])
    country.append(['Isle of Man','IM','IMN','833'])
    country.append(['Israel','IL','ISR','376'])
    country.append(['Italy','IT','ITA','380'])
    country.append(['Jamaica','JM','JAM','388'])
    country.append(['Japan','JP','JPN','392'])
    country.append(['Jersey','JE','JEY','832'])
    country.append(['Jordan','JO','JOR','400'])
    country.append(['Kazakhstan','KZ','KAZ','398'])
    country.append(['Kenya','KE','KEN','404'])
    country.append(['Kiribati','KI','KIR','296'])
    country.append(['the Democratic People''s Republic of Korea','KP','PRK','408','North Korea'])
    country.append(['the Republic of Korea','KR','KOR','410'])
    country.append(['Kuwait','KW','KWT','414'])
    country.append(['Kyrgyzstan','KG','KGZ','417'])
    country.append(['the Lao People''s Democratic Republic','LA','LAO','418','Laos'])
    country.append(['Latvia','LV','LVA','428'])
    country.append(['Lebanon','LB','LBN','422'])
    country.append(['Lesotho','LS','LSO','426'])
    country.append(['Liberia','LR','LBR','430'])
    country.append(['the Libyan Arab Jamahiriya','LY','LBY','434'])
    country.append(['Liechtenstein','LI','LIE','438'])
    country.append(['Lithuania','LT','LTU','440'])
    country.append(['Luxembourg','LU','LUX','442'])
    country.append(['Macao','MO','MAC','446'])
    country.append(['Macedonia','MK','MKD','807'])
    country.append(['Madagascar','MG','MDG','450'])
    country.append(['Malawi','MW','MWI','454'])
    country.append(['Malaysia','MY','MYS','458'])
    country.append(['Maldives','MV','MDV','462'])
    country.append(['Mali','ML','MLI','466'])
    country.append(['Malta','MT','MLT','470'])
    country.append(['the Marshall Islands','MH','MHL','584'])
    country.append(['Martinique','MQ','MTQ','474'])
    country.append(['Mauritania','MR','MRT','478'])
    country.append(['Mauritius','MU','MUS','480'])
    country.append(['Mayotte','YT','MYT','175'])
    country.append(['Mexico','MX','MEX','484'])
    country.append(['the Federated States of Micronesia','FM','FSM','583','Micronesia'])
    country.append(['the Republic of Moldova','MD','MDA','498'])
    country.append(['Monaco','MC','MCO','492'])
    country.append(['Mongolia','MN','MNG','496'])
    country.append(['Montenegro','ME','MNE','499'])
    country.append(['Montserrat','MS','MSR','500'])
    country.append(['Morocco','MA','MAR','504'])
    country.append(['Mozambique','MZ','MOZ','508'])
    country.append(['Myanmar','MM','MMR','104'])
    country.append(['Namibia','NA','NAM','516'])
    country.append(['Nauru','NR','NRU','520'])
    country.append(['Nepal','NP','NPL','524'])
    country.append(['the Netherlands','NL','NLD','528'])
    country.append(['the Netherlands Antilles','AN','ANT','530'])
    country.append(['New Caledonia','NC','NCL','540'])
    country.append(['New Zealand','NZ','NZL','554'])
    country.append(['Nicaragua','NI','NIC','558'])
    country.append(['Niger','NE','NER','562'])
    country.append(['Nigeria','NG','NGA','566'])
    country.append(['Niue','NU','NIU','570'])
    country.append(['Norfolk Island','NF','NFK','574'])
    country.append(['the Northern Mariana Islands','MP','MNP','580'])
    country.append(['Norway','NO','NOR','578'])
    country.append(['Oman','OM','OMN','512'])
    country.append(['Pakistan','PK','PAK','586'])
    country.append(['Palau','PW','PLW','585'])
    country.append(['the Occupied Palestinian Territory','PS','PSE','275','Palestine'])
    country.append(['Panama','PA','PAN','591'])
    country.append(['Papua New Guinea','PG','PNG','598'])
    country.append(['Paraguay','PY','PRY','600'])
    country.append(['Peru','PE','PER','604'])
    country.append(['the Philippines','PH','PHL','608'])
    country.append(['Pitcairn','PN','PCN','612'])
    country.append(['Poland','PL','POL','616'])
    country.append(['Portugal','PT','PRT','620'])
    country.append(['Puerto Rico','PR','PRI','630'])
    country.append(['Qatar','QA','QAT','634'])
    country.append(['Reunion','RE','REU','638'])
    country.append(['Romania','RO','ROU','642'])
    country.append(['the Russian Federation','RU','RUS','643'])
    country.append(['Rwanda','RW','RWA','646'])
    country.append(['Saint Helena','SH','SHN','654'])
    country.append(['Saint Kitts and Nevis','KN','KNA','659'])
    country.append(['Saint Lucia','LC','LCA','662'])
    country.append(['Saint Pierre and Miquelon','PM','SPM','666'])
    country.append(['Saint Vincent and the Grenadines','VC','VCT','670','Saint Vincent'])
    country.append(['Samoa','WS','WSM','882'])
    country.append(['San Marino','SM','SMR','674'])
    country.append(['Sao Tome and Principe','ST','STP','678'])
    country.append(['Saudi Arabia','SA','SAU','682'])
    country.append(['Senegal','SN','SEN','686'])
    country.append(['Serbia','RS','SRB','688'])
    country.append(['Seychelles','SC','SYC','690'])
    country.append(['Sierra Leone','SL','SLE','694'])
    country.append(['Singapore','SG','SGP','702'])
    country.append(['Slovakia','SK','SVK','703'])
    country.append(['Slovenia','SI','SVN','705'])
    country.append(['the Solomon Islands','SB','SLB','90'])
    country.append(['Somalia','SO','SOM','706'])
    country.append(['South Africa','ZA','ZAF','710'])
    country.append(['South Georgia and the South Sandwich Islands','GS','SGS','239','South Georgia'])
    country.append(['Spain','ES','ESP','724'])
    country.append(['Sri Lanka','LK','LKA','144'])
    country.append(['Sudan','SD','SDN','736'])
    country.append(['Suriname','SR','SUR','740'])
    country.append(['Svalbard and Jan Mayen','SJ','SJM','744'])
    country.append(['Swaziland','SZ','SWZ','748'])
    country.append(['Sweden','SE','SWE','752'])
    country.append(['Switzerland','CH','CHE','756'])
    country.append(['the Syrian Arab Republic','SY','SYR','760'])
    country.append(['Taiwan, Province of China','TW','TWN','158'])
    country.append(['Tajikistan','TJ','TJK','762'])
    country.append(['the United Republic of Tanzania','TZ','TZA','834'])
    country.append(['Thailand','TH','THA','764'])
    country.append(['Timor-Leste','TL','TLS','626'])
    country.append(['Togo','TG','TGO','768'])
    country.append(['Tokelau','TK','TKL','772'])
    country.append(['Tonga','TO','TON','776'])
    country.append(['Trinidad and Tobago','TT','TTO','780'])
    country.append(['Tunisia','TN','TUN','788'])
    country.append(['Turkey','TR','TUR','792'])
    country.append(['Turkmenistan','TM','TKM','795'])
    country.append(['the Turks and Caicos Islands','TC','TCA','796'])
    country.append(['Tuvalu','TV','TUV','798'])
    country.append(['Uganda','UG','UGA','800'])
    country.append(['Ukraine','UA','UKR','804'])
    country.append(['the United Arab Emirates','AE','ARE','784'])
    country.append(['the United Kingdom','GB','GBR','826'])
    country.append(['the United States','US','USA','840'])
    country.append(['the United States Minor Outlying Islands','UM','UMI','581','U.S. Islands'])
    country.append(['Uruguay','UY','URY','858'])
    country.append(['Uzbekistan','UZ','UZB','860'])
    country.append(['Vanuatu','VU','VUT','548'])
    country.append(['Venezuela','VE','VEN','862'])
    country.append(['Viet Nam','VN','VNM','704'])
    country.append(['the British Virgin Islands','VG','VGB','92'])
    country.append(['the U.S. Virgin Islands','VI','VIR','850'])
    country.append(['Wallis and Futuna','WF','WLF','876'])
    country.append(['Western Sahara','EH','ESH','732'])
    country.append(['Yemen','YE','YEM','887'])
    country.append(['Zambia','ZM','ZMB','894'])
    country.append(['Zimbabwe','ZW','ZWE','716'])
    country.append(['Saint Barthelemy','BL','BLM','652'])
    country.append(['Saint Martin (France)','MF','MAF','663'])
    #what follows are not actual ISO country codes, they are PAGER earthquake regions
    #in the US that have been added to the list
    country.append(['U.S. Earthquake Region California','XF','XFA','902','California'])
    country.append(['U.S. Earthquake Region Central/Eastern United States','EU','EUS','903','Eastern U.S.'])
    country.append(['U.S. Earthquake Region Western United States','WU','WUS','904','Western U.S.'])
    return country

def getLongestCountryName(useshort=False):
    clist = getCountryList()
    maxlen = 0
    for country in clist:
        if len(country) == 5 and useshort:
            name = country[4]
        else:
            name = country[0]
        if name > maxlen:
            maxlen = len(name)
    return maxlen

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage:\n %s [key]\n, where key is either a 2 character or 3 character ISO code, or numeric ISO code' % sys.argv[0]
        sys.exit(1)
    key = sys.argv[1]
    try:
        cdict = getCountryCode(key)
        print 'Name: %s\nAlpha2: %s\nAlpha3: %s\nNumeric: %i' % (cdict['name'],cdict['alpha2'],cdict['alpha3'],cdict['number'])
    except TypeError,msg:
        print 'Command failed: %s' % (msg)
        sys.exit(1)
    sys.exit(0)
    
