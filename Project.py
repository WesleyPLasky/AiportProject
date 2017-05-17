#Data Science 
#Project 

from bs4 import BeautifulSoup
import urllib
import stats 
import csv
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from operator import itemgetter

def SFOAirport():#my code

    SFO={}
    
    for i in range(-9,3):
        
        page = urllib.request.urlopen("http://www.airportsfo.org/flights/departures?t="+str(i))
        soup = BeautifulSoup(page, 'html5lib')
        
        
        
        td=soup.find_all("td",{"data-label":"FROM"})
        for tag in td:
            entries = tag.find("a",{"class":"in_text"})
            if entries.string!=None:
                if entries.contents[0] in SFO:
                    SFO[entries.contents[0]]=SFO[entries.contents[0]]+1
                else:
                    SFO.setdefault(entries.contents[0],1)

    return SFO

def LAXAirport():#my code
    
    LAX={}
    Ltime=[0]*24
    
    for i in range(-9,3):
        
        page = urllib.request.urlopen("https://www.airport-la.com/lax/departures?t="+str(i))
        soup = BeautifulSoup(page, 'html5lib')
        
        td=soup.find_all("td",{"width":120})
        for tag in td:
            entries = tag.find("a",{"class":"in_text"})
            if entries!=None:
                if entries.contents[0] in LAX:
                    LAX[entries.contents[0]]=LAX[entries.contents[0]]+1
                else:
                    LAX.setdefault(entries.contents[0],1)
        
        td=soup.find_all("td",{"width":60})
        for tag in td:
            entries = tag.contents[0]
            c = entries.find(":")
            hour = int(entries[:c])
            Ltime[hour]+=1

    return LAX, Ltime


def JFKAirport():#Rebecca's code
    JFK={}
    Jtime=[0]*24
    
    for i in range(0,24,6):
    
        page = urllib.request.urlopen("http://www.airport-jfk.com/departures.php?tp="+str(i))
        soup = BeautifulSoup(page, 'html5lib')
        
        div=soup.find_all("div",{"id":"fdest"})
        for tag in div:
            horse=tag.find("b")
            if horse!=None:
                    if horse.contents[0] in JFK:
                        JFK[horse.contents[0]]=JFK[horse.contents[0]]+1
                    else:
                        JFK.setdefault(horse.contents[0],1)
    
        td=soup.find_all("div",{"id":"fhour"})
        
        for tag in td:
            if tag.contents[0]!="Departure": 
                entries=tag.find("b")
                temp=entries.find("a")
                temp2 = temp.contents[0]
                c = temp2.find(":")
                hour = int(temp2[:c])
                if i <12:
                    if hour==12:
                        Jtime[0]+=1
                    else:
                        Jtime[hour]+=1
                else:
                    if hour==12:
                        Jtime[hour]+=1
                    else:
                        Jtime[hour+12]+=1
    
        
    return JFK, Jtime

def LGAAirport():#Rebecca's code
    lgaDest={}
    #open LGA csv file 
    with open("LGAFlights.csv", 'r') as f:
        reader = csv.reader(f)
        dest = []
        for line in reader:
            for i in line:
                dest.append(i.split('\t'))
        fixedlist = []
        for i in range(len(dest)//2 - 1):
            temp = []
            temp = dest[i]+dest[i+1]
            fixedlist.append(temp)
            i = i+2
        destinations = []
        for i in range(len(fixedlist)):
            if ( i % 2 == 1):
                destinations.append(fixedlist[i][2])
        #put entries into dictionary
        for i in range(len(destinations)):
            key = destinations[i]
            if (key in lgaDest):
                lgaDest[key] = int(lgaDest[key] + 1)
            else:
                lgaDest.setdefault(key,1)
        #print(lgaDest)
        f.close()
        return lgaDest
    
#from this point on is a combination of our code because we needed to accomadate for differences in each others code so that that code can work together  
def condenseDictionaries(JFK,LGA,LAX,SFO):
    newDict = {}
    for key in JFK:
        if (key not in newDict):
            newDict[key] = JFK[key] + LGA[key] + LAX[key] + SFO[key]
    #print("NEW DICTIONARY:", newDict)
    sortedCondensedDict = sorted(newDict.items(), key=itemgetter(1))
    #print(sortedCondensedDict)
    topten = toptenDests(sortedCondensedDict)
    return topten

def combine2Airports(JFK, LGA, LAX, SFO):
    NY = {}
    CA = {}
    for key in JFK:
        if (key not in NY):
            NY[key] = JFK[key] + LGA[key]
    #print("NY:", NY)
    for k in LAX:
        if (k not in CA):
            CA[k] = LAX[k] + SFO[k]
    #print("CA:", CA)
    return NY,CA

def toptenDests(dictionary):
    topten = []
    #print("DICTIONARY:", dictionary)
    for i in range((len(dictionary)-1),(len(dictionary)-11),-1):
        topten.append(dictionary[i])
    #print("TOP TEN:", topten)
    return topten

        
def main():
    SFO=SFOAirport()
    LAX,Ltime=LAXAirport()
    JFK,Jtime=JFKAirport()
    LGA= LGAAirport()
    
    ft=["Hour","LAXT#flights","JFKT#flights","Totals"]
    
    
    with open("projecttimes.csv","w") as csvfile:
        wr=csv.DictWriter(csvfile,delimiter=',', fieldnames=ft)
        wr.writeheader()
        for i in range(len(Ltime)):
            total=Ltime[i]+Jtime[i]
            wr.writerow({ft[0]:i,ft[1]:Ltime[i],ft[2]:Jtime[i],ft[3]:total})
    csvfile.close()
    
    
#    for key in SFO:
#        if key not in LAX:
#            LAX.setdefault(key,0)
#            
#    Sval=[]
#    Lval=[]
#            
#    for key in LAX:
#        print(key)
#        if key not in SFO:
#            SFO.setdefault(key,0)
#        Sval.append(SFO[key])
#        Lval.append(LAX[key])

    JFKval = []
    LGAval = []
    SFOval = []
    LAXval = []
    
    for key in JFK:
        #print(key)
        if key not in LGA:
            LGA.setdefault(key,0)
        if key not in LAX:
            LAX.setdefault(key,0)
        if key not in SFO:
            SFO.setdefault(key,0)
    for key in LGA:
        #print(key)
        if key not in JFK:
            JFK.setdefault(key,0)
        if key not in LAX:
            LAX.setdefault(key,0)
        if key not in SFO:
            SFO.setdefault(key,0)
    for key in LAX:
        if key not in JFK:
            JFK.setdefault(key,0)
        if key not in LGA:
            LGA.setdefault(key,0)
        if key not in SFO:
            SFO.setdefault(key,0)
    for key in SFO:
        if key not in JFK:
            JFK.setdefault(key,0)
        if key not in LGA:
            LGA.setdefault(key,0)
        if key not in LAX:
            LAX.setdefault(key,0)
        JFKval.append(JFK[key])  
        LGAval.append(LGA[key])
        SFOval.append(SFO[key])
        LAXval.append(LAX[key])
        
    NYairports, CAairports = combine2Airports(JFK,LGA,LAX,SFO)
    topten = condenseDictionaries(JFK,LGA,LAX,SFO)
    
    #compute correlation between NY and CA flights
    NYvalues = []
    CAvalues = []
    for key in NYairports:
        NYvalues.append(NYairports[key])
        CAvalues.append(CAairports[key])
    print("NY", NYvalues)
    print("CA", CAvalues)
    print("Correlation(NY, CA) by destination:", stats.correlation(NYvalues, CAvalues))      
    
    toptenCities = []
    toptenFlights = []
    for i in range(len(topten)):
        toptenCities.append(topten[i][0])
        toptenFlights.append(topten[i][1])
    #plot image 1
    #total number of flights for each airport
    totals = []
    totalJFKflights = sum(JFK.values())
    totalLGAflights = sum(LGA.values())
    totalSFOflights = sum(SFO.values()) 
    totalLAXflights = sum(LAX.values()) 
    totals.append(totalJFKflights)
    totals.append(totalLAXflights)
    totals.append(totalSFOflights)
    totals.append(totalLGAflights)
    fig,ax = plt.subplots()
    N = range(4)
    #print("Totals:", totals)
    width = .35
    airports = ['JFK', 'LAX', 'SFO', 'LGA']
    plt.bar(N,totals,width = width, color = 'b')
    plt.title("Total Number of Flights")
    plt.xlabel('Airports')
    plt.xticks(N,airports)
    plt.ylabel('Number of Flights')
    plt.show()

    #plot image 3
    #top ten popular flights
    n = range(10)
    plt.bar(n,toptenFlights,width=width, color = 'r')
    plt.title("Top Ten Popular Flights")
    plt.xlabel('Destinations')
    plt.xticks(n,toptenCities)
    plt.ylabel('Number of Flights')
    plt.show()
    
    
    print("Correlation for LAX and JFK by number of flight departures per hour " + str(stats.correlation(Ltime,Jtime)))
    
    #plot 4 line regression
    times=pd.read_csv("projecttimes.csv")
    sns.regplot(x="LAXT#flights", y="JFKT#flights", data=times);
    sns.pairplot(times, x_vars=["Hour"], y_vars=["LAXT#flights","JFKT#flights"],size=5, aspect=.8, kind="reg")
    sns.plt.show()
            

    print("Correlation between SFO and LAX by number of flights per destination " + str(stats.correlation(SFOval,LAXval)))
    print("Correlation between LGA and JFK by number of flights per destination " + str(stats.correlation(LGAval,JFKval)))
    
    
main()
    