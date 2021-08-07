import streamlit as st
import preprocessor
import pandas as pd
import joblib

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

user_menu = st.sidebar.radio('Select an Option',
                            ('Country-wise Analysis',
                             'Athlete wise Analysis'))


sort_val = {'ascending':True, 'descending':False}
l1 = ['descending','ascending']
sort_by_col1 = ['Total','Gold','Silver','Bronze']
p = {'All':['Gold','Silver','Bronze'],'Total':['Total'],'Gold':['Gold'],'Silver':['Silver'],'Bronze':['Bronze']}
select_x = list(p.keys())
years = joblib.load('years.joblib')

if user_menu == 'Country-wise Analysis':
    countries = joblib.load('countries.joblib')
    st.sidebar.title('Country-wise Analysis')
    st.title('Country-wise Analysis')
    s1 = st.sidebar.selectbox("Select Country",countries)
    s2 = st.sidebar.selectbox("Select year",years)
    
    if (s2 == 'Overall') and (s1 == 'Overall'):
        s3 = st.selectbox("Select sorting column",sort_by_col1)
        s4 = st.selectbox("Select sorting type",l1)
        no = st.number_input('No of rows to show', min_value=10)
        
        df,h = preprocessor.f1(sort_val[s4],s3,no)
        st.header("Tabular data of medal tally")
        st.table(df)
        
        st.header("Bar plot of medal tally")
        x_axis = st.selectbox("Select plot type",select_x)
        if len(p[x_axis]) == 1:
                df = df[df[p[x_axis][0]] != 0]
        y_axis = 'Country'
        label =  {'value':'No of {} medals'.format(x_axis)}
        title = 'Country vs Medal Counts'
        fig = preprocessor.plotly_bar_plot(df.iloc[::-1],p[x_axis],y_axis,label,title,h)

        st.plotly_chart(fig)
            
    elif (s2 != 'Overall') and (s1 == 'Overall'):
        s3 = st.selectbox("Select sorting column",sort_by_col1)
        s4 = st.selectbox("Select sorting type",l1)
        no = st.number_input('No of rows to show', min_value=10)
        
        df,h = preprocessor.f2(sort_val[s4],s3,no,s2)
        st.header("Tabular data of medal tally")
        st.table(df)
        
        st.header("Bar plot of medal tally")
        x_axis = st.selectbox("Select plot type",select_x)
        if len(p[x_axis]) == 1:
                df = df[df[p[x_axis][0]] != 0]
        y_axis = 'Country'
        label = {'value':'No of {} medals'.format(x_axis)}
        title = 'Country vs Medal Counts in {}'.format(s2)
        fig = preprocessor.plotly_bar_plot(df.iloc[::-1],p[x_axis],y_axis,label,title,h)

        st.plotly_chart(fig)
        
        
    elif (s2 == 'Overall') and (s1 != 'Overall'):
        sort_by_col1.insert(0,'year')
        s3 = st.selectbox("Select sorting column",sort_by_col1)
        s4 = st.selectbox("Select sorting type",l1)
        df,data,h = preprocessor.f3(sort_val[s4],s3,s1)
        st.header("Tabular data of medal tally")
        st.table(df)
        
        if df.shape[0] > 5:
            df = df.iloc[::-1]
            
            st.header("Bar plot of medal tally")
            x_axis = st.selectbox("Select plot type",select_x)
            if len(p[x_axis]) == 1:
                df = df[df[p[x_axis][0]] != 0]
                
            year = df.year.values.tolist()
            year = [str(i) for i in year]
            label = {'y':'year','value':'No of {} medals'.format(x_axis)}
            title = 'Performance of {} yearwise'.format(s1)
            fig = preprocessor.plotly_bar_plot(df,p[x_axis],year,label,title,h)

            st.plotly_chart(fig)
            
            st.header("Line plot of medal tally")
            data = data.loc[:, (data != 0).any(axis=0)]
            s = data.columns.tolist()
            t = sort_by_col1[1:]
            s = [i for i in t if i in s]
            
            s = st.selectbox("Select plot type",s)
            label = {'value':'No of {} medals'.format(s)}
            title = 'Performance of {} yearwise'.format(s1)
            color_code = {'Total':'green','Gold':'gold','Silver':'silver','Bronze':'burlywood'}
            year = data.year.values.tolist()
            year = [str(i) for i in year]
            
            fig = preprocessor.plotly_line_plot(data,year,s,label,title,color_code)
            st.plotly_chart(fig)
            
        else:        
            df = df.iloc[::-1]
            year = df.year.values.tolist()
            year = [str(i) for i in year]
            
            df = df.loc[:, (df != 0).any(axis=0)]
            s = df.columns.tolist()
            s = [i for i in select_x if i in s]
            p['All'] = s[1:]
            if len(p['All']) > 1:
                s.insert(0,'All')
            else:
                s = p['All']
            
            st.header("Bar plot of medal tally")
            x_axis = st.selectbox("Select plot type",s)
            label = {'x':'year','value':'No of {} medals'.format(x_axis)}
            title = 'Performance of {} yearwise'.format(s1)
            fig = preprocessor.plotly_bar_plot(df,year,p[x_axis],label,title,400,'group','v')

            st.plotly_chart(fig)

    
    else:
        df = preprocessor.f4(s2,s1)
        if not df.empty:
            st.header("Tabular data of medal tally")
            st.table(df)
            
            df = df.iloc[::-1]
            year = df.year.values.tolist()
            year = [str(i) for i in year]
            
            df = df.loc[:, (df != 0).any(axis=0)]
            s = df.columns.tolist()
            s = [i for i in select_x if i in s]
            p['All'] = s[1:]
            if len(p['All']) > 1:
                s.insert(0,'All')
            else:
                s = p['All']
            
            st.header("Bar plot of medal tally")
            x_axis = st.selectbox("Select plot type",s)
            label = {'x':'year','value':'No of {} medals'.format(x_axis)}
            title = 'Performance of {} in {}'.format(s1,s2)
            fig = preprocessor.plotly_bar_plot(df,year,p[x_axis],label,title,400,'group','v')

            st.plotly_chart(fig)

        else:
            st.header("{} has won no medlas in the year {}".format(s1,s2))
               
            
elif user_menu == 'Athlete wise Analysis':
    athletes = joblib.load('unique_athletes.joblib')
    st.sidebar.title("Athlete wise Analysis")
    st.title("Athlete wise Analysis")
    s1 = st.sidebar.selectbox("Select athlete",athletes)
    s2 = st.sidebar.selectbox("Select year",years)
    
    if (s1 == 'Overall') and (s2 == 'Overall'):
        df = pd.read_csv('athletes_data.csv')
        df = df[df.year == '1896 - 2016']
        countries = sorted(df.Country.unique().tolist())
        countries.insert(0,'Overall')
        #directly acces country from data
        s3 = st.selectbox("Select Country",countries)
        s4 = st.selectbox("Select sorting column",sort_by_col1)
        s5 = st.selectbox("Select sorting type",l1)
        no = st.number_input('No of rows to show', min_value=10)
        
        df,h = preprocessor.f5(df,sort_val[s5],s4,no,s3)
        st.header("Tabular data of medal tally")
        st.table(df)
             
        if df.shape[0] > 5:
            st.header('Bar plot of Athletes medal tally')
            x_axis = st.selectbox("Select plot type",select_x)
            if len(p[x_axis]) == 1:
                df = df[df[p[x_axis][0]] != 0]
            y_axis = 'Athlete'
            label = {'value':'No of {} medals'.format(x_axis)}
            if s3 == 'Overall':
                title = 'Athlete vs Medal Counts'
                df['Athlete'] = df['Athlete'] + ' ('+ df['Country'] +')'
            else:
                title = 'Athlete vs Medal Counts for {}'.format(s3)
                
            fig = preprocessor.plotly_bar_plot(df.iloc[::-1],p[x_axis],y_axis,label,title,h)
                
            st.plotly_chart(fig)
            
        else:
            df = df.iloc[::-1]
            
            df = df.loc[:, (df != 0).any(axis=0)]
            s = df.columns.tolist()
            s = [i for i in select_x if i in s]
            p['All'] = s[1:]
            if len(p['All']) > 1:
                s.insert(0,'All')
            else:
                s = p['All']
            
            st.header("Bar plot of medal tally")
            x_axis = st.selectbox("Select plot type",s)
            y_axis = 'Athlete'
            label = {'value':'No of {} medals'.format(x_axis)}
            title = 'Performance of {}\'s athlete'.format(s3)
            fig = preprocessor.plotly_bar_plot(df,y_axis,p[x_axis],label,title,400,'group','v')

            st.plotly_chart(fig)
      
 
    elif (s1 == 'Overall') and (s2 != 'Overall'):
        df = pd.read_csv('athletes_data.csv')
        df = df[df.year != '1896 - 2016']
        df = df[df.year == str(s2)]
        countries = sorted(df.Country.unique().tolist())
        countries.insert(0,'Overall')
        
        s3 = st.selectbox("Select Country",countries)
        s4 = st.selectbox("Select sorting column",sort_by_col1)
        s5 = st.selectbox("Select sorting type",l1)
        no = st.number_input('No of rows to show', min_value=10)
        
        df,h = preprocessor.f6(df,sort_val[s5],s4,no,s3,s2)
        st.header("Tabular data of medal tally")
        st.table(df)

            
        if df.shape[0] > 1:
            st.header('Bar plot of Athletes medal tally')
            x_axis = st.selectbox("Select plot type",select_x)
            if len(p[x_axis]) == 1:
                df = df[df[p[x_axis][0]] != 0]
            y_axis = 'Athlete'
            label = {'value':'No of {} medals'.format(x_axis)}
            if s3 == 'Overall':
                title = 'Athlete vs Medal Counts in {}'.format(s2)
                df['Athlete'] = df['Athlete'] + ' ('+ df['Country'] +')'
            else:
                title = 'Athlete vs Medal Counts for {} in {}'.format(s3,s2)
            
            fig = preprocessor.plotly_bar_plot(df.iloc[::-1],p[x_axis],y_axis,label,title,h)
            st.plotly_chart(fig)
            
        else:
            df = df.iloc[::-1]
            
            df = df.loc[:, (df != 0).any(axis=0)]
            s = df.columns.tolist()
            s = [i for i in select_x if i in s]
            p['All'] = s[1:]
            if len(p['All']) > 1:
                s.insert(0,'All')
            else:
                s = p['All']
                
            st.header("Bar plot of medal tally")
            x_axis = st.selectbox("Select plot type",s)
            y_axis = 'Athlete'
            label = {'value':'No of {} medals'.format(x_axis)}
            title = 'Performance of {}\'s athlete in {}'.format(s3,s2)
            fig = preprocessor.plotly_bar_plot(df,y_axis,p[x_axis],label,title,400,'group','v')

            st.plotly_chart(fig)
            
    elif (s1 != 'Overall') and (s2 == 'Overall'):
        sort_by_col1.insert(0,'year')
        s4 = st.selectbox("Select sorting column",sort_by_col1)
        s5 = st.selectbox("Select sorting type",l1)
        no = st.number_input('No of rows to show', min_value=10)
        
        df,data = preprocessor.f7(sort_val[s5],s4,no,s1)
    
        st.header("Tabular data of medal tally")
        st.table(df)
        country = df.Country.values[0]
        
        if df.shape[0] > 5:
            df = df.iloc[::-1]

            st.header('Bar plot of medal tally')
            x_axis = st.selectbox("Select plot type",select_x)
            if len(p[x_axis]) == 1:
                df = df[df[p[x_axis][0]] != 0]
                
            year = df.year.values.tolist()
            year = [str(i) for i in year]
                
            label = {'value':'No of {} medals'.format(x_axis)}
            title = 'Performance of {} for {} yearwise'.format(s1,country)
            fig = preprocessor.plotly_bar_plot(df,p[x_axis],year,label,title,300)
            
            st.plotly_chart(fig)
            
            
            st.header("Line plot of medal tally")
            data = data.loc[:, (data != 0).any(axis=0)]
            s = data.columns.tolist()
            t = sort_by_col1[1:]
            s = [i for i in t if i in s]
            
            s = st.selectbox("Select plot type",s)
            label = {'value':'No of {} medals'.format(s)}
            title = 'Performance of {} for {} yearwise'.format(s1,country)
            color_code = {'Total':'green','Gold':'gold','Silver':'silver','Bronze':'burlywood'}
            year = data.year.values.tolist()
            year = [str(i) for i in year]
            
            fig = preprocessor.plotly_line_plot(data,year,s,label,title,color_code)
            st.plotly_chart(fig)
  
        else:
            df = df.iloc[::-1]
            year = df.year.values.tolist()
            year = [str(i) for i in year]
            
            df = df.loc[:, (df != 0).any(axis=0)]
            s = df.columns.tolist()
            s = [i for i in select_x if i in s]
            p['All'] = s[1:]
            if len(p['All']) > 1:
                s.insert(0,'All')
            else:
                s = p['All']
            
            st.header("Bar plot of medal tally")
            x_axis = st.selectbox("Select plot type",s)
            label = {'x':'year','value':'No of {} medals'.format(x_axis)}
            title = 'Performance of {} for {} yearwise'.format(s1,country)
            fig = preprocessor.plotly_bar_plot(df,year,p[x_axis],label,title,400,'group','v')

            st.plotly_chart(fig)
            

    else :
        df = preprocessor.f8(s1,s2)
        if not df.empty:
            st.header("Tabular data of medal tally")
            st.table(df)
            
            df = df.iloc[::-1]
            df = df.loc[:, (df != 0).any(axis=0)]
            df['Athlete'] = df['Athlete'] + ' (' + df['Country'] + ')'
            s = df.columns.tolist()
            s = [i for i in select_x if i in s]
            p['All'] = s[1:]
            if len(p['All']) > 1:
                s.insert(0,'All')
            else:
                s = p['All']
            
            st.header("Bar plot of medal tally")
            x_axis = st.selectbox("Select plot type",s)
            y_axis = 'Athlete'
            label = {'value':'No of {} medals'.format(x_axis)}
            title = 'Performance of {} in {}'.format(s1,df.year.values[0])
            fig = preprocessor.plotly_bar_plot(df,y_axis,p[x_axis],label,title,400,'group','v')

            st.plotly_chart(fig)

        else:
            st.header("{} didnot participated in the Olympics {}".format(s1,s2))
        