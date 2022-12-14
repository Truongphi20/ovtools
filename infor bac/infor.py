import requests
import urllib
import pandas as pd

def PhanCatLinkGet(linkget): # phan cat link get thanh link va cac header
	stra = linkget
	bou = stra.split("?")
	link = bou[0]
	headers = bou[1].split("&")  
	lib = {}
	for ele in headers:
		tem = ele.split("=")
		lib[tem[0]] = tem[1]
	#print(lib)
	return link, lib
#print(PhanCatLinkGet("https://www.wdcm.org/gcmapi/api/strainpassport/listByStrainName?page=1&size=10&application=&author=&ccs=&collections=&dateOfIsolation=&geographicOrigin=&historyOfDeposit=&isolatedFrom=&isolatedFromInput=&keyword=Bacillus+amyloliquefaciens&latitudeEnd=&latitudeStart=&literature=&longitudeEnd=&longitudeStart=&optimumTemperature=&organismType=&otherCollectionNumbers=&strainName=&strainNumber=&temperatureEnd=99&temperatureStart=0&typeStrain=&userId=&namehtml=&sort=&search=Bacillus+amyloliquefaciens"))
#print(PhanCatLinkGet("https://www.wdcm.org/gcmapi/api/strainpassport/strainnumbers?page=1&size=10&application=&author=&ccs=&collections=&dateOfIsolation=&geographicOrigin=&historyOfDeposit=&isolatedFrom=&isolatedFromInput=&keyword=&latitudeEnd=&latitudeStart=&literature=&longitudeEnd=&longitudeStart=&optimumTemperature=&organismType=&otherCollectionNumbers=&strainName=Bacillus+amyloliquefaciens&strainNumber=&temperatureEnd=&temperatureStart=&typeStrain=&userId=&namehtml=&term=Bacillus+amyloliquefaciens&type=name"))


def SearchNumBac(name): # Tim so luong giong vi khuan   
	#print(str('%20'.join(name.split(" "))))
	total_rs = []
	rs = ["0"]
	page = 0
	while len(rs) != 0:
		page += 1 
		payload = {'page': page, 'size': '10', 'application': '', 'author': '',
					 'ccs': '', 'collections': '', 'dateOfIsolation': '', 'geographicOrigin': '',
					  'historyOfDeposit': '', 'isolatedFrom': '', 'isolatedFromInput': '',
					   'keyword': name, 'latitudeEnd': '', 'latitudeStart': '',
					    'literature': '', 'longitudeEnd': '', 'longitudeStart': '', 'optimumTemperature': '',
					     'organismType': '', 'otherCollectionNumbers': '', 'strainName': '', 'strainNumber': '',
					      'temperatureEnd': '99', 'temperatureStart': '0', 'typeStrain': '', 'userId': '',
					       'namehtml': '', 'sort': '', 'search': name}

		r = requests.get('https://www.wdcm.org/gcmapi/api/strainpassport/listByStrainName',params=payload)
		rs = r.json()["content"]
		total_rs.extend(rs)
		#print(r.url)
		#print(r.json())
		#print(r.json()["content"][0])
	return total_rs
#print(SearchNumBac("Bacillus amyloliquefaciens"))


def FindBacCode(name): # Tim ma code va nguon goc cua cac chung vi khuan theo ten
	strain_num = []
	history = []
	page = 0
	rs = [0]
	while len(rs) != 0:
		page += 1 
		payload = {'page': page, 'size': '10', 'application': '', 'author': '',
					 'ccs': '', 'collections': '', 'dateOfIsolation': '', 'geographicOrigin': '',
					  'historyOfDeposit': '', 'isolatedFrom': '', 'isolatedFromInput': '',
					   'keyword': '', 'latitudeEnd': '', 'latitudeStart': '', 'literature': '',
					    'longitudeEnd': '', 'longitudeStart': '', 'optimumTemperature': '',
					     'organismType': '', 'otherCollectionNumbers': '',
					      'strainName': name, 'strainNumber': '',
					       'temperatureEnd': '', 'temperatureStart': '', 'typeStrain': '',
					        'userId': '', 'namehtml': '', 'term': name, 'type': 'name'}
		r = requests.get('https://www.wdcm.org/gcmapi/api/strainpassport/strainnumbers',params=payload)
		#print(r.json()["content"])
		rs = r.json()["content"]
		for lib in rs:
			strain_num.append(lib["strainNumber"])
			history.append(lib["history"])
	#print(len(strain_num))
	return strain_num, history
#print(FindBacCode('Bacillus amyloliquefaciens')[1])


#str_num = 'CCMM B993'
def FindPassport(name): # Tim passport cua vi khuan

	strain_num, history = FindBacCode(name) # tim code cua cac vi khuan
	#print(strain_num)
	#print(history)

	cgo  = [] # correct_geographic_origin
	isolate = [] #isolated_from
	tem = []	# minimum_temperature_for_growth---optimum_temperature_for_growth---maximum_temperature_for_growth

	for str_num in strain_num:
		payload = {'strainNumber':str_num}
		params = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote) # space laf %20 thay vi +

		r = requests.get("https://www.wdcm.org/gcmapi/api/species/strainnumbertoinfo",params=params)
		#print(r.json()['strainPassport'])

		rs = r.json()['strainPassport']

		cgo.append(rs["correct_geographic_origin"])
		#print(cgo)
		isolate.append(rs["isolated_from"])
		#print(isolate)
		tem.append([rs["minimum_temperature_for_growth"],rs["optimum_temperature_for_growth"],rs["maximum_temperature_for_growth"]])
		#print(tem)
	return cgo, isolate, tem

khurong = lambda lista: ['N' if i == None or i == "" else i for i in lista]

cgo, isolate, tem = FindPassport('Bacillus amyloliquefaciens')
#print(cgo)
#print(isolate)
#print(tem)

temstr = ["/".join(khurong(i)) for i in tem]
#print(temstr)

# Xuat data
ba_data = pd.DataFrame(zip(cgo,isolate,temstr),columns=["Geographic origin","Isolated from","Temperature"])
ba_data.to_csv(r'ba_table.csv',index=False,sep="#")


