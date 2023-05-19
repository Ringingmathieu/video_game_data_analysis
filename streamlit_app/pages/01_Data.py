# import the libraries 
import pandas as pd
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer

# import the dataset
video_game = pd.read_csv('Data/Video_Games.csv')

# Create a header for the page
st.title('Data exploration')

# initiate tabs
tab1, tab2 = st.tabs(['Dataframe', 'Exploration script'])

with tab1:
    # initiate a title for the tab
    st.subheader('Exploration of Dataframe')
    
    # use streamlit library to show dataframe
    # create a filtering tool for the data exploration
    filtered_video_game = dataframe_explorer(video_game, case=False)
    st.dataframe(filtered_video_game, use_container_width=True)


with tab2:
    # initiate a title for the tab
    st.subheader('Python script used to create the graphical analysis')
    # write the python script
    code = '''
            In this code you can see how I made the analysis of the dataset.
            The observation of the data has been done with pandas
            and the vizualisation with the plotly express library.
            The goal of the analysis is to highlight the sales, in volume, of the video 
            game market from 1980 to 2020.
            
            # show basic info of the dataset
            video_game.info()

            # show the shape of the dataset
            video_game.shape

            # in this analysis we will only be looking for video games sales
            # drop columns from index 10 to 16 becaus we won't use them for this analysis
            video_game.drop(video_game.iloc[:,10:16], inplace=True, axis=1)

            # check for null values
            video_game.isnull().sum()

            # look at the two games with missing values
            video_game.loc[video_game['Name'].isnull()]

            # we will drop these two rows as is will not have a big impact on the analysis
            video_game.dropna(subset=['Name'], inplace=True)

            # look at the missing publishers
            video_game.loc[video_game['Publisher'].isnull()]

            # drop the rows as it won't have a big impact on the dataframe
            video_game.dropna(subset=['Publisher'], inplace=True)

            # look at the missing year values
            video_game.loc[video_game['Year_of_Release'].isnull()]

            # replace missing years with the median value
            video_game['Year_of_Release'].fillna((video_game['Year_of_Release'].median()), inplace=True)

            # describe the values of the dataset
            video_game.describe()

            # show the number of games for every year in the dataframe
            # initiate the plot
            fig_1 = px.histogram(video_game, x='Year_of_Release')

            # update the layout of the plot
            fig_1.update_layout(title='Number of games per year',
                                xaxis_title='Year of Release', yaxis_title='Number of Games',
                                bargap=0.4)
            # show the plot
            fig_1.show()

            ## Analyze sales by region

            # calculate the sum of sales for each region and global sales
            # multiply by 100000 as the column is in millions
            NA_Sales = video_game['NA_Sales'].sum()*100000
            EU_Sales = video_game['EU_Sales'].sum()*100000
            JP_Sales = video_game['JP_Sales'].sum()*100000
            Other_Sales = video_game['Other_Sales'].sum()*100000
            Global_Sales = video_game['Global_Sales'].sum()*100000


            # print the result 
            print("The North American market represent {:,.2f} copies sold".format(NA_Sales))
            print("The European market represent {:,.2f} copies sold".format(EU_Sales))
            print("The Japanese market represent {:,.2f} copies sold".format(JP_Sales))
            print("The other market represent {:,.2f} copies sold".format(Other_Sales))
            print("The global market represent {:,.2f} copies sold".format(Global_Sales))

            # create a bar chart to show total sales by region
            fig_2 = px.bar(x=['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales', 'Global Sales'], 
                        y=[NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales], 
                        labels={'x':'Region', 'y':'Sales'},
                        title='Sales by Region',
                        color=[NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global_Sales])

            # show the plot
            fig_2.show()

            # create a pie chart to show the share of every region in %
            fig_3 = px.pie(values=[NA_Sales, EU_Sales, JP_Sales, Other_Sales], 
                        names=['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales'], 
                        title='Share of Sales by Region')
            # add a title to the legend
            fig_3.update_layout(legend_title='Market')

            # show the plot
            fig_3.show()

            ## Analyze sales by region throughout the years

            # count the sum of sales grouped by years
            sales_year = video_game.groupby('Year_of_Release').sum().reset_index()
            sales_year

            # create lineplot of sales by year and region
            fig_4 = px.line(sales_year, x='Year_of_Release', y=sales_year.columns,
                        title='Sales by Year')

            # update the axis titles and legend
            fig_4.update_layout(xaxis_title='Year of Release',
                            yaxis_title='Copies in millions',
                            legend_title='Market')

            # show the plot
            fig_4.show()

            ## Analyze sales per platform

            # count the sum of sales per platform and sort by global sales
            sales_platform = video_game.groupby('Platform').sum().sort_values('Global_Sales', ascending=False).reset_index()
            sales_platform

            # create bar plot for global sales per platform
            fig_5 = px.bar(sales_platform, x='Platform', y='Global_Sales', 
                        title='Total Sales by Platform')

            # update axis title
            fig_5.update_layout(yaxis_title='Copies in millions')

            # show plot
            fig_5.show()

            # count the sum of sales by region per platform
            platform_NA = video_game.groupby('Platform')[['NA_Sales']].sum().sort_values('NA_Sales', ascending=False).reset_index()
            platform_EU = video_game.groupby('Platform')[['EU_Sales']].sum().sort_values('EU_Sales', ascending=False).reset_index()
            platform_JP = video_game.groupby('Platform')[['JP_Sales']].sum().sort_values('JP_Sales', ascending=False).reset_index()
            platform_Other = video_game.groupby('Platform')[['Other_Sales']].sum().sort_values('Other_Sales', ascending=False).reset_index()

            # initialize a subplot
            fig_6 = sp.make_subplots(
                rows=2, cols=2,
                subplot_titles=('NA Sales', 'EU Sales', 'JP Sales', 'Other Sales')
            )

            # add the four bar plots
            fig_6.add_trace(px.bar(platform_NA, x='Platform', y='NA_Sales').data[0], row=1, col=1)
            fig_6.add_trace(px.bar(platform_EU, x='Platform', y='EU_Sales').data[0], row=1, col=2)
            fig_6.add_trace(px.bar(platform_JP, x='Platform', y='JP_Sales').data[0], row=2, col=1)
            fig_6.add_trace(px.bar(platform_Other, x='Platform', y='Other_Sales').data[0], row=2, col=2)

            # update the title and the dimensions
            fig_6.update_layout(height=600, width=950, 
                                title_text="Video Game Sales by Platform",
                            yaxis_title='Copies in millions')

            # update angle of x axis
            fig_6.update_xaxes(tickangle=45)

            # show the plot
            fig_6.show()

            ## Analyze top 20 publishers

            # count the sum of sales by publisher sorted by descending
            publisher_sales = video_game.groupby('Publisher').sum().sort_values('Global_Sales', ascending=False).reset_index()[:20]
            publisher_sales

            # create bar plot of top 20 publishers by global sales
            fig_7 = px.bar(publisher_sales, x='Publisher', y='Global_Sales',
                        title='Top 20 publishers')

            # update y axis title
            fig_7.update_layout(yaxis_title='Copies in millions')

            # show plot
            fig_7.show()

            # count the sum of sales by publisher per region
            publisher_NA = video_game.groupby('Publisher')[['NA_Sales']].sum().sort_values('NA_Sales', ascending=False).reset_index()[:20]
            publisher_EU = video_game.groupby('Publisher')[['EU_Sales']].sum().sort_values('EU_Sales', ascending=False).reset_index()[:20]
            publisher_JP = video_game.groupby('Publisher')[['JP_Sales']].sum().sort_values('JP_Sales', ascending=False).reset_index()[:20]
            publisher_Other = video_game.groupby('Publisher')[['Other_Sales']].sum().sort_values('Other_Sales', ascending=False).reset_index()[:20]
            
            # initialize a subplot
            fig_8 = sp.make_subplots(
                rows=2, cols=2,
                subplot_titles=('NA Sales', 'EU Sales', 'JP Sales', 'Other Sales')
            )
            # add the bar plots 
            fig_8.add_trace(px.bar(publisher_NA, x='Publisher', y='NA_Sales').data[0], row=1, col=1)
            fig_8.add_trace(px.bar(publisher_EU, x='Publisher', y='EU_Sales').data[0], row=1, col=2)
            fig_8.add_trace(px.bar(publisher_JP, x='Publisher', y='JP_Sales').data[0], row=2, col=1)
            fig_8.add_trace(px.bar(publisher_Other, x='Publisher', y='Other_Sales').data[0], row=2, col=2)

            # update the dimensions and title
            fig_8.update_layout(height=1200, width=950, title_text="Top 20 publishers by Region",
                                yaxis_title='Copies in millions')
            fig_8.update_xaxes(tickangle=45)

            # show plot
            fig_8.show()
            
            ## Analyze genres by sales  

            # count the sum of sales by genre sorted by global sales
            genre_sales = video_game.groupby('Genre').sum().sort_values('Global_Sales', ascending=False).reset_index()
            genre_sales

            # create bar plot 
            fig_9 = px.bar(genre_sales, x='Genre', y='Global_Sales',
                        title='Global Sales by Genre')

            # update y axis title
            fig_9.update_yaxes(title='Copies in millions')

            # show the plot
            fig_9.show()

            # count the sum of sales by genre per region
            genre_NA = video_game.groupby('Genre')[['NA_Sales']].sum().sort_values('NA_Sales', ascending=False).reset_index()
            genre_EU = video_game.groupby('Genre')[['EU_Sales']].sum().sort_values('EU_Sales', ascending=False).reset_index()
            genre_JP = video_game.groupby('Genre')[['JP_Sales']].sum().sort_values('JP_Sales', ascending=False).reset_index()
            genre_Other = video_game.groupby('Genre')[['Other_Sales']].sum().sort_values('Other_Sales', ascending=False).reset_index()

            # initialize the subplot
            fig_10 = sp.make_subplots(
                rows=2, cols=2,
                subplot_titles=('NA Sales', 'EU Sales', 'JP Sales', 'Other Sales')
            )

            # add the bar plots
            fig_10.add_trace(px.bar(genre_NA, x='Genre', y='NA_Sales').data[0], row=1, col=1)
            fig_10.add_trace(px.bar(genre_EU, x='Genre', y='EU_Sales').data[0], row=1, col=2)
            fig_10.add_trace(px.bar(genre_JP, x='Genre', y='JP_Sales').data[0], row=2, col=1)
            fig_10.add_trace(px.bar(genre_Other, x='Genre', y='Other_Sales').data[0], row=2, col=2)

            # update dimensions and title
            fig_10.update_layout(height=900, width=950, title_text="Sales by Genre per Region",
                                yaxis_title='Copies in millions')
            fig_10.update_xaxes(tickangle=45)

            # show the plot
            fig_10.show()

            # create a sunburst of genres per platform
            fig_11 = px.sunburst(video_game, path=['Platform', 'Genre'],
                            values='Global_Sales')

            # show the plot
            fig_11.show()
            
            ## Analyze top 20 games

            # top 20 games sorted by global sales
            top_games = video_game.sort_values('Global_Sales', ascending=False)[:20]
            top_games

            # create bar plot of sales per game
            fig_12 = px.bar(top_games, x='Name', y='Global_Sales', 
                        title='Top 20 Games by Global Sales')

            # update y axis title
            fig_12.update_layout(yaxis_title='Copies in millions',
                                xaxis_title='Game')

            # show plot
            fig_12.show()

            # create a bar plot of sales top 20 games by genre
            fig_13 = px.bar(top_games, x='Name', y='Global_Sales', 
                        title='Top 20 Games by Global Sales by Genre', color='Genre')

            # update axis titles
            fig_13.update_layout(xaxis_title='Game',
                                yaxis_title='Copies in millions')

            # show plot
            fig_13.show()

            # count the sum of sales by region
            game_NA = video_game.groupby('Name')[['NA_Sales']].sum().sort_values('NA_Sales', ascending=False).reset_index()[:20]
            game_EU = video_game.groupby('Name')[['EU_Sales']].sum().sort_values('EU_Sales', ascending=False).reset_index()[:20]
            game_JP = video_game.groupby('Name')[['JP_Sales']].sum().sort_values('JP_Sales', ascending=False).reset_index()[:20]
            game_Other = video_game.groupby('Name')[['Other_Sales']].sum().sort_values('Other_Sales', ascending=False).reset_index()[:20]

            # initialize a subplot
            fig_14 = sp.make_subplots(
                rows=2, cols=2,
                subplot_titles=('NA Sales', 'EU Sales', 'JP Sales', 'Other Sales')
            )

            # add plots
            fig_14.add_trace(px.bar(game_NA, x='Name', y='NA_Sales').data[0], row=1, col=1)
            fig_14.add_trace(px.bar(game_EU, x='Name', y='EU_Sales').data[0], row=1, col=2)
            fig_14.add_trace(px.bar(game_JP, x='Name', y='JP_Sales').data[0], row=2, col=1)
            fig_14.add_trace(px.bar(game_Other, x='Name', y='Other_Sales').data[0], row=2, col=2)

            # update dimensions and titles
            fig_14.update_layout(height=1200, width=1000, title_text="Top 20 Games by Region",
                                yaxis_title='Copies in millions')
            fig_14.update_xaxes(tickangle=45)

            # show plot
            fig_14.show()
            '''

    # show the code and specify the language used
    st.code(code, language='python')
