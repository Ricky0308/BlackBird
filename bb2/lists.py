

c = 'Afghanistan:Albania:Algeria:Andorra:Angola:Antigua & Deps:Argentina:Armenia:Australia:Austria:Azerbaijan:Bahamas:Bahrain:Bangladesh:Barbados:Belarus:Belgium:Belize:Benin:Bhutan:Bolivia:Bosnia Herzegovina:Botswana:Brazil:Brunei:Bulgaria:Burkina:Burundi:Cambodia:Cameroon:Canada:Cape Verde:Central African Rep:Chad:Chile:China:Colombia:Comoros:Congo:Congo {Democratic Rep}:Costa Rica:Croatia:Cuba:Cyprus:Czech Republic:Denmark:Djibouti:Dominica:Dominican Republic:East Timor:Ecuador:Egypt:El Salvador:Equatorial Guinea:Eritrea:Estonia:Ethiopia:Fiji:Finland:France:Gabon:Gambia:Georgia:Germany:Ghana:Greece:Grenada:Guatemala:Guinea:Guinea-Bissau:Guyana:Haiti:Honduras:Hungary:Iceland:India:Indonesia:Iran:Iraq:Ireland {Republic}:Israel:Italy:Ivory Coast:Jamaica:Japan:Jordan:Kazakhstan:Kenya:Kiribati:Korea North:Korea South:Kosovo:Kuwait:Kyrgyzstan:Laos:Latvia:Lebanon:Lesotho:Liberia:Libya:Liechtenstein:Lithuania:Luxembourg:Macedonia:Madagascar:Malawi:Malaysia:Maldives:Mali:Malta:Marshall Islands:Mauritania:Mauritius:Mexico:Micronesia:Moldova:Monaco:Mongolia:Montenegro:Morocco:Mozambique:Myanmar, {Burma}:Namibia:Nauru:Nepal:Netherlands:New Zealand:Nicaragua:Niger:Nigeria:Norway:Oman:Pakistan:Palau:Palestine:Panama:Papua New Guinea:Paraguay:Peru:Philippines:Poland:Portugal:Qatar:Romania:Russian Federation:Rwanda:St Kitts & Nevis:St Lucia:Saint Vincent & the Grenadines:Samoa:San Marino:Sao Tome & Principe:Saudi Arabia:Senegal:Serbia:Seychelles:Sierra Leone:Singapore:Slovakia:Slovenia:Solomon Islands:Somalia:South Africa:South Sudan:Spain:Sri Lanka:Sudan:Suriname:Swaziland:Sweden:Switzerland:Syria:Taiwan:Tajikistan:Tanzania:Thailand:Togo:Tonga:Trinidad & Tobago:Tunisia:Turkey:Turkmenistan:Tuvalu:Uganda:Ukraine:United Arab Emirates:United Kingdom:United States:Uruguay:Uzbekistan:Vanuatu:Vatican City:Venezuela:Vietnam:Yemen:Zambia:Zimbabwe'
COUNTRY_LIST = c.split(':')
COUNTRY_CHOICES = tuple(((x, x) for x in COUNTRY_LIST))



AGE_LIST = ['20s', '30s', '40s', '50s', '60s', '70s or more']
AGE_CHOICES = tuple(((x, x) for x in AGE_LIST))

ENGLISH_LEVEL_GENERAL_LISTS = ['Begginer', 'Lower Intermediate', 'Intermediate', 'Upper Intermediate', 'Advanced', 'Almost Native']
ENGLISH_LEVEL_GENERAL_CHOICES = tuple(((x, x) for x in ENGLISH_LEVEL_GENERAL_LISTS))

SEX_LIST = ['Female', 'Male']
SEX_CHOICES = tuple(((x, x) for x in SEX_LIST))

PUNCTUALITY_LIST = ['below 5 mins late', 'below 10 mins late', 'below 15 mins late', 'below 30 mins late']
PUNCTUALITY_CHOICES = (
		('no', "don't care" ), 
		('0','almost 0 min late'),
		('5', 'around 5 mins late'),
		('10', 'around 10 mins late'),
		('15', 'around 15 mins or later'),
	)

POLITENESS_CHIOCES=(
		('3', 'polite'),
		('2', 'normal'),
		('1', 'a bit impolite'),
		('0', 'impolite'), 
	)

IELTS_SCORE_LISTS = ['3.5', '4', '4.5' ,'5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9']
IELTS_SCORE_CHOICES = tuple(((x, x) for x in IELTS_SCORE_LISTS))
TOEFL_SCORE_LISTS = ['60', '65', '70', '75', '80', '85', '90', '95', '100', '105', '110', '115', '120']
TOEFL_SCORE_CHOICES = tuple(((x, x) for x in TOEFL_SCORE_LISTS))


# tags, footprints
TAG_LIST = ['General', 'Sports', 'Tech', 'Religion', 'Lifestyle', 
'Study', 'Dream', 'Personality', 
'Culture',]
TAG_CHOICES = tuple(((x, x) for x in TAG_LIST))
FOOTPRINT_LISTS = ['login' ,'search', 'profile_page', 'room_page', 'join',]
FOOTPRINT_CHOICES = tuple(((x, x) for x in FOOTPRINT_LISTS))

PURPOSE_LIST = ['IELTS', 'CAE', 'CPE', 'TOEIC', 
'Linguaskill (Bulats)', 'PTE', 'TOEFL', 
'DET (Duolingo English Test)', 'job interview practice', 
'conversation practice', ]
PURPOSE_CHOICES = tuple(((x, x) for x in PURPOSE_LIST))