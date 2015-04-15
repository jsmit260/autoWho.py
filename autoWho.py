#!/usr/bin/python
import pycurl
import sys
import json
import re
import os
import subprocess
#import cgi
#import cgitb
 
# Create instance of FieldStorage
#form = cgi.FieldStorage()
# Get data from fields
#ip_ = form.getvalue('ip')
 
if re.match(r'^((([2][5][0-5]|([2][0-4]|[1][0-9]|[0-9])?[0-9])\.){3})([2][5][0-5]|([2][0-4]|[1][0-9]|[0-9])?[0-9])$',sys.argv[1]) is None:
    	sys.exit("Invalid IPv4 format")
 
if re.match(r'^(((25[0-5]|2[0-4][0-9]|19[0-1]|19[3-9]|18[0-9]|17[0-1]|17[3-9]|1[0-6][0-9]|1[1-9]|[2-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]))|(192\.(25[0-5]|2[0-4][0-9]|16[0-7]|169|1[0-5][0-9]|1[7-9][0-9]|[1-9][0-9]|[0-9]))|(172\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|1[0-5]|3[2-9]|[4-9][0-9]|[0-9])))\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$',sys.argv[1]) is None:
    	print '\n\nYou can NOT use RFC1918 address "'+sys.argv[1]+'", as no WHOIS record exists.\t:)\n '
        sys.exit("\nPlease enter a public IP address. :)\n\n ")
 
#COUNTRIES
 
countries={'AF' :'Afghanistan','AX' :'Aland Islands','AL' :'Albania','DZ' :'Algeria','AS' :'American Samoa','AD' :'Andorra','AO' :'Angola','AI' :'Anguilla','AQ' :'Antarctica','AG' :'Antigua and Barbuda','AR' :'Argentina','AM' :'Armenia','AW' :'Aruba','AC' :'Ascension Island','AU' :'Australia','AT' :'Austria','AZ' :'Azerbaijan','BS' :'Bahamas','BH' :'Bahrain','BB' :'Barbados' ,'BD' :'Bangladesh' ,'BY' :'Belarus','BE' :'Belgium' ,'BZ' :'Belize','BJ' :'Benin','BM' :'Bermuda','BT' :'Bhutan','BW' :'Botswana' ,'BO' :'Bolivia' ,'BA' :'Bosnia and Herzegovina','BV' :'Bouvet Island' ,'BR' :'Brazil' ,'IO' :'British Indian Ocean Territory' ,'BN' :'Brunei Darussalam','BG' :'Bulgaria' ,'BF' :'Burkina Faso' ,'BI' :'Burundi' ,'KH' :'Cambodia','CM' :'Cameroon' ,'CA' :'Canada' ,'CV' :'Cape Verde' ,'KY' :'Cayman Islands','CF' :'Central African Republic' ,'TD' :'Chad' ,'CL' :'Chile' ,'CN' :'China' ,'CX' :'Christmas Island' ,'CC' :'Cocos (Keeling) Islands','CO' :'Colombia' ,'KM' :'Comoros' ,'CG' :'Congo' ,'CD' :'Congo, Democratic Republic' ,'CK' :'Cook Islands' ,'CR' :'Costa Rica' ,'CI' :'Cote D Ivoire (Ivory Coast)' ,'HR' :'Croatia (Hrvatska)' ,'CU' :'Cuba' ,'CY' :'Cyprus','CZ' :'Czech Republic','CS' :'Czechoslovakia (former)' ,'DK' :'Denmark' ,'DJ' :'Djibouti' ,'DM' :'Dominica','DO' :'Dominican Republic' ,'TP' :'East Timor' ,'EC' :'Ecuador' ,'EG' :'Egypt' ,'SV' :'El Salvador' ,'GQ' :'Equatorial Guinea' ,'ER' :'Eritrea' ,'EE' :'Estonia' ,'ET' :'Ethiopia' ,'EU' :'European Union' ,'FK' :'Falkland Islands (Malvinas)' ,'FO' :'Faroe Islands' ,'FJ' :'Fiji' ,'FI' :'Finland','FR' :'France' ,'FX' :'France, Metropolitan' ,'GF' :'French Guiana' ,'PF' :'French Polynesia' ,'TF' :'French Southern Territories' ,'MK' :'F.Y.R.O.M. (Macedonia)' ,'GA' :'Gabon' ,'GM' :'Gambia' ,'GE' :'Georgia' ,'DE' :'Germany' ,'GH' :'Ghana' ,'GI' :'Gibraltar' ,'GB' :'Great Britain (UK)','GR' :'Greece' ,'GL' :'Greenland','GD' :'Grenada' ,'GP' :'Guadeloupe' ,'GU' :'Guam' ,'GT' :'Guatemala' ,'GG' :'Guernsey' ,'GN' :'Guinea' ,'GW' :'Guinea Bissau' ,'GY' :'Guyana' ,'HT' :'Haiti' ,'HM' :'Heard and McDonald Islands','HN' :'Honduras' ,'HK' :'Hong Kong' ,'HU' :'Hungary' ,'IS' :'Iceland' ,'IN' :'India' ,'ID' :'Indonesia' ,'IR' :'Iran' ,'IQ' :'Iraq' ,'IE' :'Ireland','IL' :'Israel' ,'IM' :'Isle of Man' ,'IT' :'Italy' ,'JE' :'Jersey' ,'JM' :'Jamaica' ,'JP' :'Japan' ,'JO' :'Jordan' ,'KZ' :'Kazakhstan','KE' :'Kenya','KI' :'Kiribati','KP' :'Korea (North)','KR' :'Korea (South)' ,'KW' :'Kuwait' ,'KG' :'Kyrgyzstan','LA' :'Laos' ,'LV' :'Latvia' ,'LB' :'Lebanon','LI' :'Liechtenstein','LR' :'Liberia' ,'LY' :'Libya' ,'LS' :'Lesotho' ,'LT' :'Lithuania' ,'LU' :'Luxembourg' ,'MO' :'Macau' ,'MG' :'Madagascar' ,'MW' :'Malawi' ,'MY' :'Malaysia' ,'MV' :'Maldives' ,'ML' :'Mali' ,'MT' :'Malta' ,'MH' :'Marshall Islands' ,'MQ' :'Martinique' ,'MR' :'Mauritania' ,'MU' :'Mauritius' ,'YT' :'Mayotte' ,'MX' :'Mexico' ,'FM' :'Micronesia','MC' :'Monaco','MD' :'Moldova' ,'MN' :'Mongolia' ,'ME' :'Montenegro' ,'MS' :'Montserrat' ,'MA' :'Morocco' ,'MZ' :'Mozambique' ,'MM' :'Myanmar' ,'NA' :'Namibia' ,'NR' :'Nauru' ,'NP' :'Nepal' ,'NL' :'Netherlands' ,'AN' :'Netherlands Antilles' ,'NT' :'Neutral Zone' ,'NC' :'New Caledonia' ,'NZ' :'New Zealand (Aotearoa)' ,'NI' :'Nicaragua','NE' :'Niger' ,'NG' :'Nigeria' ,'NU' :'Niue' ,'NF' :'Norfolk Island' ,'MP' :'Northern Mariana Islands' ,'NO' :'Norway' ,'OM' :'Oman' ,'PK' :'Pakistan' ,'PW' :'Palau' ,'PS' :'Palestinian Territory, Occupied' ,'PA' :'Panama' ,'PG' :'Papua New Guinea' ,'PY' :'Paraguay' ,'PE' :'Peru' ,'PH' :'Philippines','PN' :'Pitcairn' ,'PL' :'Poland' ,'PT' :'Portugal' ,'PR' :'Puerto Rico' ,'QA' :'Qatar' ,'RE' :'Reunion' ,'RO' :'Romania' ,'RU' :'Russian Federation' ,'RW' :'Rwanda' ,'GS' :'S. Georgia and S. Sandwich Isls.' ,'KN' :'Saint Kitts and Nevis','LC' :'Saint Lucia' ,'VC' :'Saint Vincent & the Grenadines' ,'WS' :'Samoa' ,'SM' :'San Marino' ,'ST' :'Sao Tome and Principe','SA' :'Saudi Arabia','SN' :'Senegal','RS' :'Serbia','YU' :'Serbia and Montenegro (former)','SC' :'Seychelles','SL' :'Sierra Leone','SG' :'Singapore' ,'SI' :'Slovenia','SK' :'Slovak Republic' ,'SB' :'Solomon Islands' ,'SO' :'Somalia' ,'ZA' :'South Africa' ,'ES' :'Spain' ,'LK' :'Sri Lanka' ,'SH' :'St. Helena','PM' :'St. Pierre and Miquelon' ,'SD' :'Sudan' ,'SR' :'Suriname' ,'SJ' :'Svalbard & Jan Mayen Islands' ,'SZ' :'Swaziland' ,'SE' :'Sweden' ,'CH' :'Switzerland' ,'SY' :'Syria' ,'TW' :'Taiwan' ,'TJ' :'Tajikistan' ,'TZ' :'Tanzania' ,'TH' :'Thailand' ,'TG' :'Togo' ,'TK' :'Tokelau' ,'TO' :'Tonga' ,'TT' :'Trinidad and Tobago' ,'TN' :'Tunisia' ,'TR' :'Turkey' ,'TM' :'Turkmenistan' ,'TC' :'Turks and Caicos Islands' ,'TV' :'Tuvalu' ,'UG' :'Uganda' ,'UA' :'Ukraine' ,'AE' :'United Arab Emirates' ,'UK' :'United Kingdom' ,'US' :'United States' ,'UM' :'US Minor Outlying Islands' ,'UY' :'Uruguay' ,'SU' :'USSR (former)' ,'UZ' :'Uzbekistan' ,'VU' :'Vanuatu' ,'VA' :'Vatican City State (Holy See)' ,'VE' :'Venezuela' ,'VN' :'Viet Nam' ,'VG' :'British Virgin Islands' ,'VI' :'Virgin Islands (U.S.)' ,'WF' :'Wallis and Futuna Islands' ,'EH' :'Western Sahara' ,'YE' :'Yemen' ,'ZM' :'Zambia' ,'ZR' :'Zaire See CD Congo, Democratic Republic' ,'ZW' :'Zimbabwe'}
 
 
 
#1 Create a pycurl.Curl instance
 
with open('out.json', 'w') as f :
    	uri = ('ipinfo.io/'+sys.argv[1])
 
    	#curl page
    	c = pycurl.Curl()
    	c.setopt(c.URL, uri)
    	#2 Use setopt to set options
    	c.setopt(c.WRITEDATA, f)
    	c.perform()
    	c.close()
 
with open('out.json', 'r') as f :
    	file = f.readlines()
 
    	IP = file[1].split(':')
    	if IP[1]:
            	nextIP = IP[1].replace('"','').strip()
            	finalIP = nextIP.replace(',','').strip()
 
    	Nation = file[5].split(':')
    	if Nation:
            	nextNation = Nation[1].replace('"', '').strip()
                finalNation = nextNation.replace(",",'').strip()
 
    	Org = file[7].split(':')
    	if Org:
            	nextOrg= Org[1].replace('"','').strip()
            	finalOrg= nextOrg.replace(",",'').strip()
 
 
    	sentence = ('%s (%s/%s)') %(finalIP,finalOrg,finalNation)
 
    	os.remove('out.json')
 
#for key,value in countries.items():
 
    	if finalNation in countries:
 
            	fullCountryName = countries[finalNation]
            	sentence2 = ('%s (%s/%s)') %(finalIP,finalOrg,fullCountryName)
 
            	print ''
            	print sentence2
            	print ''
 
    	else :
            	print sentence


