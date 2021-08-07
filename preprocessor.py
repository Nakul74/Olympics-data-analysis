import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def f1(s1,s2,no):
    df = pd.read_csv('country_data.csv')
    df = df[df.year == '1896 - 2016']
    df.sort_values(by = s2 , ascending = s1, inplace=True)
    temp = df.head(no).reset_index(drop=True)
    temp.index += 1 
    
    if (no < 16):
        h = 400
    elif ((no > 15) and (no < 21)):
        h = 500
    elif ((no > 20) and (no < 31)):
        h = 600
    else:
        h = 800

    return temp,h


def f2(s1,s2,no,year):
    df = pd.read_csv('country_data.csv')
    df = df[df.year != '1896 - 2016']
    temp = df[df.year == str(year)]
    temp.sort_values(by = s2 , ascending = s1, inplace=True)
    temp = temp.head(no).reset_index(drop=True)
    temp.index += 1 
    
    if (no < 16):
        h = 400
    elif ((no > 15) and (no < 21)):
        h = 500
    elif ((no > 20) and (no < 31)):
        h = 600
    else:
        h = 800
        
    return temp,h

   
def f3(s1,s2,country):
    df = pd.read_csv('country_data.csv')
    df = df[df.year != '1896 - 2016']
    temp = df[df['Country'] == country]
    
    if temp.shape[0] > 1:
        temp['year'] = temp['year'].astype('int32') 
        data = temp.copy()
        data = data.sort_values(by = 'year' , ascending = True)
        data['year'] = data['year'].astype('object')
        temp.sort_values(by = s2 , ascending = s1, inplace=True)
        no = temp.shape[0]
        
        temp = temp.reset_index(drop=True)
        temp.index += 1 
    
        if (no < 11):
            h = 400
        elif ((no > 10) and (no < 21)):
            h = 500
        else:
            h = 600
    
        return temp,data,h
    else:
        temp = temp.reset_index(drop=True)
        temp.index += 1 
        return temp,[],400


def f4(year,country):
    df = pd.read_csv('country_data.csv')
    df = df[df.year != '1896 - 2016']
    temp = df[(df['Country'] == country) & (df['year'] == str(year))]
    temp = temp.reset_index(drop=True)
    temp.index += 1 

    return temp



def f5(df,s1,s2,no,country):
    if country != 'Overall':
        df = df[df.Country == country]
    df = df.drop_duplicates(subset=['Athlete'])
    df.sort_values(by = s2 , ascending = s1, inplace=True)
    temp = df.head(no).reset_index(drop=True)
    temp.index += 1 
    
    if (no < 16):
        h = 400
    elif ((no > 15) and (no < 21)):
        h = 500
    elif ((no > 20) and (no < 31)):
        h = 600
    else:
        h = 800

    return temp,h


def f6(df,s1,s2,no,country,year):
    df = df.drop_duplicates(subset=['Athlete'])
    if country != 'Overall':
        df = df[df.Country == country]
    df.sort_values(by = s2 , ascending = s1, inplace=True)
    temp = df.head(no).reset_index(drop=True)
    temp.index += 1 
    
    if (no < 16):
        h = 400
    elif ((no > 15) and (no < 21)):
        h = 500
    elif ((no > 20) and (no < 31)):
        h = 600
    else:
        h = 800

    return temp,h

def f7(s1,s2,no,athlete):
    df = pd.read_csv('athletes_data.csv')
    df = df[df.year != '1896 - 2016']
    temp = df[df.Athlete == athlete]
    temp = temp.drop_duplicates(subset=['year'])
    
    temp['year'] = temp['year'].astype('int32') 
    data = temp.copy()
    data = data.sort_values(by = 'year' , ascending = True)
    data['year'] = data['year'].astype('object')
    temp.sort_values(by = s2 , ascending = s1, inplace=True)
    temp = temp.reset_index(drop=True)
    temp.index += 1 
    

    return temp,data
        
        
def f8(athlete,year):
  df = pd.read_csv('athletes_data.csv')
  df = df[df.year != '1896 - 2016']
  temp = df[(df['Athlete'] == athlete) & (df['year'] == str(year))]
  temp = temp.drop_duplicates(subset=['year'])
  temp = temp.reset_index(drop=True)
  temp.index += 1 

  return temp  
    

def plotly_bar_plot(data,x_axis,y_axis,label,title,h = 400,mode='stack',orient = 'h'):
    
    fig = px.bar(data, y = y_axis, x = x_axis, title = title,
                 orientation = orient, labels = label,
                 template = 'plotly_dark', barmode = mode,
                 color_discrete_map={'Gold': 'gold','Silver':'lightgrey',
                                     'Bronze': 'burlywood'})
    fig.update_layout(height = h)
    
    return fig

def plotly_line_plot(data,x_axis,y_axis,label,title,color_code):
    
    fig = px.line(data, x=x_axis, y=[y_axis],labels=label,template = 'plotly_dark',
                  color_discrete_map={y_axis:color_code[y_axis]},title=title)
    
    return fig


    
    
    
    