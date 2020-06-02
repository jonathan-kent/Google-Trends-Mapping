import os
import time
import copy
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
import pandas as pd
from svgpathtools import svg2paths, wsvg
from svgpathtools import disvg
import colorsys
import webcolors


nfl_team_names = ["Arizona Cardinals", "Atlanta Falcons", "Carolina Panthers", \
                  "Chicago Bears", "Dallas Cowboys", "Detroit Lions", \
                  "Green Bay Packers", "Los Angeles Rams", "Minnesota Vikings", \
                  "New Orleans Saints", "New York Giants", "Philadelphia Eagles", \
                  "San Francisco 49ers", "Seattle Seahawks", "Tampa Bay Buccaneers", \
                  "Washington Redskins", "Baltimore Ravens", "Buffalo Bills", \
                  "Cincinnati Bengals", "Cleveland Browns", "Denver Broncos", \
                  "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", \
                  "Kansas City Chiefs", "Los Angeles Chargers", "Miami Dolphins", \
                  "New England Patriots", "New York Jets", "Las Vegas Raiders", \
                  "Pittsburgh Steelers", "Tennessee Titans"]
nfl_team_color_codes = ["#B00539", "#CA233D", "#0297D9", \
                        "#1C1D41", "#082D72", "#006BAF", \
                        "#244729", "#BB9648", "#1A065B",\
                        "#D3BC8D", "#0B2488", "#004A53", \
                        "#B3995E", "#2C587D", "#CA233D", \
                        "#7C1415", "#2D3075", "#C60C3D", \
                        "#FB4F14", "#643615", "#F36A24", \
                        "#CA233D", "#143D75", "#01839B", \
                        "#CA243C", "#F5C113", "#006C6E", \
                        "#002244", "#CD2C31", "#BEBEBE", \
                        "#FFC30D", "#31A2DA"]


nba_team_names = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", \
                  "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers", \
                  "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", \
                  "Golden State Warriors", "Houston Rockets", "Indiana Pacers", \
                  "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", \
                  "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", \
                  "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", \
                  "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", \
                  "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", \
                  "Toronto Raptors", "Washington Wizards", "Utah Jazz"]
nba_team_color_codes = ["#C6242F", "#098348", "#222020", \
                        "#02788C", "#BC032B", "#73233C", \
                        "#007CC4", "#F8B627", "#054F96", \
                        "#FFD429", "#CA0D1E", "#002D62", \
                        "#363294", "#552582", "#57B3A5", \
                        "#860028", "#1F4F26", "#002A5C", \
                        "#002B5C", "#DD8035", "#318FCA", \
                        "#0E77BD", "#036BB5", "#E56020", \
                        "#B03236", "#5C6770", "#040404", \
                        "#000000", "#052144", "#D48E3D"]


mlb_team_names = ["Chicago White Sox", "Cleveland Indians", "Detroit Tigers", \
                  "Kansas City Royals", "Minnesota Twins", "Baltimore Orioles", \
                  "Boston Red Sox", "New York Yankees", "Tampa Bay Rays", \
                  "Toronto Blue Jays", "Houston Astros", "Los Angeles Angels", \
                  "Oakland Athletics", "Seattle Mariners", "Texas Rangers", \
                  "Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", \
                  "Pittsburgh Pirates", "St. Louis Cardinals", "Atlanta Braves", \
                  "Miami Marlins", "New York Mets", "Philadelphia Phillies", \
                  "Washington Nationals", "Arizona Diamondbacks", "Colorado Rockies", \
                  "Los Angeles Dodgers", "San Diego Padres", "San Francisco Giants"]
mlb_team_color_codes = ["#1F1A19", "#0A2341", "#FF4819", \
                        "#B09347", "#BB042F", "#FC4A01", \
                        "#CD0224", "#01338F", "#011C45", \
                        "#184DA2", "#E67000", "#BE0126", \
                        "#004338", "#00AA99", "#6DADDE", \
                        "#002C6D", "#EF0A4B", "#C58D5D", \
                        "#FFC80C", "#FFF9EC", "#33305B", \
                        "#0077CC", "#FC4A01", "#E61B3F", \
                        "#BE0126", "#A91028", "#1F0C5A", \
                        "#005A9C", "#11264A", "#FC4A01"]


nhl_team_names = ["Carolina Hurricanes", "Columbus Blue Jackets", "New Jersey Devils", \
                  "New York Islanders", "New York Rangers", "Philadelphia Flyers", \
                  "Pittsburgh Penguins", "Washington Capitals", "Boston Bruins", \
                  "Buffalo Sabres", "Detroit Red Wings", "Florida Panthers", \
                  "Montreal Canadiens", "Ottawa Senators", "Tampa Bay Lightning", \
                  "Toronto Maple Leafs", "Chicago Blackhawks", "Colorado Avalanche", \
                  "Dallas Stars", "Minnesota Wild", "Nashville Predators", \
                  "St. Louis Blues", "Winnipeg Jets", "Anaheim Ducks", \
                  "Arizona Coyotes", "Calgary Flames", "Edmonton Oilers", \
                  "Los Angeles Kings", "San Jose Sharks", "Vancouver Canucks", \
                  "Vegas Golden Knights"]
nhl_team_color_codes = ["#E51837", "#002E62", "#E51837", \
                        "#F57D2F", "#045DAB", "#F37636", \
                        "#010206", "#002E62", "#FEBA2F", \
                        "#002E62", "#E51837", "#C8102E", \
                        "#C51230", "#EE1837", "#013D7D", \
                        "#051D5C", "#080808", "#850136", \
                        "#04613E", "#014F2F", "#FEBA2F", \
                        "#0065BD", "#002E62", "#8D7149", \
                        "#99022E", "#E51837", "#F26824", \
                        "#221F20", "#017889", "#002C55", \
                        "#BF9559"]


mls_team_names = ["Atlanta United FC", "Chicago Fire FC", "FC Cincinnati", \
                  "Columbus Crew SC", "D.C. United", "Inter Miami CF", \
                  "Montreal Impact", "New England Revolution", "New York City FC", \
                  "New York Red Bulls", "Orlando City SC", "Philadelphia Union", \
                  "Toronto FC", "Colorado Rapids", "FC Dallas", \
                  "Houston Dynamo", "LA Galaxy", "Los Angeles FC", \
                  "Minnesota United FC", "Nashville SC", "Portland Timbers", \
                  "Real Salt Lake", "San Jose Earthquakes", "Seattle Sounders FC", \
                  "Sporting Kansas City", "Vancouver Whitecaps FC"]
mls_team_color_codes = ["#A51C38", "#C2002F", "#F05323", \
                        "#F3CE1B", "#231F20", "#F4B4CF", \
                        "#175CAA", "#D0202E", "#78A5DB", \
                        "#D40C26", "#633492", "#A89E57", \
                        "#D40C26", "#960A2C", "#DF1835", \
                        "#EE9714", "#00245D", "#C6A566", \
                        "#8AD3F4", "#ECE83A", "#004811", \
                        "#B40A31", "#0067B1", "#5D9B3A", \
                        "#8FABD3", "#00235D"]


def main():
    #select teams and colors
    pytrend = TrendReq()
    team_names = mls_team_names
    team_color_codes = mls_team_color_codes
    data_file = 'mls_team_data/'
    team_and_color = {team_names[i]: team_color_codes[i] for i in range(len(team_names))} 
    team_and_color[''] = '#CFCFCF'
    team_names2 = copy.deepcopy(team_names)
    suggestions = get_suggestions(team_names, pytrend)
    names_and_sugs = list(zip(team_names, suggestions))
    names_and_sugs2 = copy.deepcopy(names_and_sugs)
    fetch_data(names_and_sugs, names_and_sugs2, data_file, pytrend)
    #set dataframe options
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    df = create_df(team_names, team_names2, data_file)
    geo_code_dict = create_map_template(df)
    color_map(geo_code_dict, df, team_and_color)


def get_suggestions(team_names, pytrend):
    suggestions = []
    for team in team_names:
        sugs = pytrend.suggestions(team)
        for sug in sugs:
            if sug['title'] == team:
                suggestions.append(sug['mid'])
                #print("%s -> %s -> %s" % (team, sug['title'], sug['type']))
                break
    return suggestions


def fetch_data(names_and_sugs, names_and_sugs2, data_file, pytrend):
    #API call for each term compared with every other term
    for team1 in names_and_sugs:
        for team2 in names_and_sugs2:
            if team1[0] != team2[0]:
                file = (data_file + "%s_and_%s.pkl" % (team1[0], team2[0]))
                if not os.path.isfile(file):
                    while True:
                        try:
                            kw_list = [team1[1], team2[1]]
                            pytrend.build_payload(kw_list, timeframe='2019-05-25 2020-05-25', geo='US')
                            interest_by_region_df = pytrend.interest_by_region(resolution='DMA', inc_low_vol=True, inc_geo_code=True)
                            interest_by_region_df.to_pickle(file)
                        except ResponseError:
                            print("too many requests while trying %s and %s" % (team1[0], team2[0]))
                            time.sleep(120)
                            continue
                        break
        names_and_sugs2.remove(team1)


def create_df(team_names, team_names2, data_file):
    #new dataframe with each location's most popular term and its percentage
    #compared to the next most popular team
    df_input = pd.read_pickle(data_file + team_names[0]+"_and_"+team_names[1]+".pkl")
    cols = [1, 2]
    df = df_input.drop(df_input.columns[cols], axis=1)
    favorite_team = [''] * (len(df_input[df_input.columns[2]].tolist()))
    percentage = [0] * (len(df_input[df_input.columns[2]].tolist()))

    for team1 in team_names:
        for team2 in team_names2:
            if team1 != team2:
                df_input = pd.read_pickle(data_file + team1+"_and_"+team2+".pkl")
                l1 = df_input[df_input.columns[1]].tolist()
                l2 = df_input[df_input.columns[2]].tolist()
                if favorite_team[0] == '':
                    for i in range(0, len(l1)):
                        if l1[i] > l2[i]:
                            favorite_team[i] = team1
                            percentage[i] = l1[i]
                        else:
                            favorite_team[i] = team2
                            percentage[i] = l2[i]
                else:
                    for i in range(0, len(l1)):
                        if favorite_team[i] == team1:
                            if l1[i] < l2[i]:
                                favorite_team[i] = team2
                                percentage[i] = l2[i]
                            else:
                                percentage[i] = min(percentage[i], l1[i])
        team_names2.remove(team1)
    for i in range(0, len(percentage)):
            if percentage[i] == 0:
                    favorite_team[i] = ''
    df['Favorite Team'] = favorite_team
    df['Percentage'] = percentage

    #change geoCodes for Anchorage (743), Fairbanks (745), Juneau(747),
    #and Honolulu (744) to 900 and up
    geo_code_list = df['geoCode'].tolist()
    edited_geo_code_list = []
    for code in geo_code_list:
        if code == '743':
            edited_geo_code_list.append('901')
        elif code == '744':
            edited_geo_code_list.append('900')
        elif code == '745':
            edited_geo_code_list.append('902')
        elif code == '747':
            edited_geo_code_list.append('903')
        else:
            edited_geo_code_list.append(code)
    df['geoCode'] = edited_geo_code_list
    df.sort_values(by=['geoCode'], inplace=True)
    print(df)
    return df


def create_map_template(df):
    #get a list of paths and attributes from the Map SVG
    paths, attributes = svg2paths('US_metro_template.svg')
    geo_code_dict = {}
    #combine attributes of seperate paths into one for each location
    j = 0
    for i in range(0, len(attributes)):
        if i == 0:
            geo_code_dict[df['geoCode'][0]] = attributes[0]
        elif attributes[i]['fill'] != attributes[i-1]['fill']:
            j = j + 1
            geo_code_dict[df['geoCode'][j]] = attributes[i]
        else:
            geo_code_dict[df['geoCode'][j]]['d'] = geo_code_dict[df['geoCode'][j]]['d'] + attributes[i]['d']
    return geo_code_dict


def color_map(geo_code_dict, df, team_and_color):
    #recolor and create output svg
    output = open("output.svg", "w")
    output.write("<!DOCTYPE html><html><body><svg width=\"543\" height=\"228\">")

    #fill in primary color
    i=0
    for code in geo_code_dict:
        geo_code_dict[code]['stroke'] = "#000000"
        geo_code_dict[code]['stroke-width'] = "0.5"

        color = team_and_color[df['Favorite Team'][i]]
        #change color saturation according to percentage
        
        #rgb_color = webcolors.hex_to_rgb(team_and_color[df['Favorite Team'][i]])
        #hsv_color = colorsys.rgb_to_hsv(rgb_color[0],rgb_color[1],rgb_color[2])
        #lst = list(hsv_color)
        #lst[1] = lst[1] * ((df['Percentage'][i])/100)
        #hsv_color = tuple(lst)
        #rgb_color = hsv_to_rgb(hsv_color[0],hsv_color[1],hsv_color[2])
        #lst = list(rgb_color)
        #lst[0] = int(rgb_color[0])
        #lst[1] = int(rgb_color[1])
        #lst[2] = int(rgb_color[2])
        #rgb_color = tuple(lst)
        #color = webcolors.rgb_to_hex(rgb_color)
        
        geo_code_dict[code]['fill'] = color
        output.write("<path d=\"%s\" stroke=\"%s\" stroke-width=\"%s\" fill=\"%s\"></path>" % \
                     (geo_code_dict[code]['d'], geo_code_dict[code]['stroke'], geo_code_dict[code]['stroke-width'], geo_code_dict[code]['fill']))
        i = i + 1

    output.write("</svg></body></html>")
    output.close()
    #output final svg map
    paths, attributes = svg2paths('output.svg')
    disvg(paths, filename='output.svg', attributes=attributes)


def hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)


if __name__ == "__main__":
    main()
