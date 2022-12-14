import pandas as pd
import geopandas
import folium

def SortCount(nations): # Sort va dem cac thanh phan
	sort = []
	tem = [sort.append(i) for i in nations if i not in sort and pd.isna(i) == False]
	#print(sort)

	count = [0]*len(sort)
	for i in range(len(count)):
		for t in nations:
			if t == sort[i]:
				count[i] += 1
	#print(sort)
	#print(count)
	return sort, count

data = pd.read_csv("ba_table.csv",sep="#")
#print(data)

data[["low tem", "opt tem", "hig tem"]] = data["Temperature"].str.split("/",expand=True)
#print(data)

nations = list(data.iloc[:, 0])
isola = list(data.iloc[:, 1])

sort, count = SortCount(nations) # sort lai cac quoc gia

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres')) # Cac quoc gia the gioi
pd.set_option("display.max_columns",10)
pd.set_option("display.width",1000)
pd.set_option("display.max_rows",200)

#print(world)

"""
## Sua ten quoc gia
quogia =['Morocco', 'Greece', 'Spain', 'United Kingdom', 'United States of America', 'South Korea', 'China', 'Thailand', 'Nepal', 'Ghana', 'Argentina', 'Italy', 'Japan', 'Taiwan']
dem = [8, 1, 4, 3, 5, 41, 25, 23, 2, 10, 1, 4, 13, 2]

table = pd.DataFrame(zip(quogia,dem),columns = ["Nations","count"])
print(table)

world_table = world.merge(table, how = "left", left_on = ["name"], right_on = ['Nations'])
world_table = world_table.dropna(subset = ["count"])
#print(world_table)

## Ve do thi the gioi
my_map = folium.Map(location=[48, -102], zoom_start=3)
folium.Choropleth(
	geo_data=world_table,
    name="choropleth",
    data=world_table,
    columns=["Nations", "count"],
    key_on="feature.properties.name",
    fill_color="OrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Research on B.amyloliquefaciens",
	).add_to(my_map)
my_map.save("ba.html")
"""
sorti, counti = SortCount(isola) # sort lai cac quoc gia
#print(sorti)
#print(counti)

counti,sorti  = zip(*sorted(zip(counti,sorti))) # sort lại nguon phan lap
#print(sorti)
#print(sum(counti))

## Xem xet nhiet do
low_tem = list(data["low tem"])
#print(low_tem)

opt_tem = list(data["opt tem"])
#print(opt_tem)

hig_tem = list(data["hig tem"])
#print(hig_tem)