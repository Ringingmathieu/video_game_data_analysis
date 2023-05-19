# import the libraries 
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import streamlit as st

# import the dataset 
video_game = pd.read_csv('Video_Games.csv')

## clean the dataset for analysis

# in this analysis we will only be looking for video games sales
# drop columns from index 10 to 16 becaus we won't use them for this analysis
video_game.drop(video_game.iloc[:,10:16], inplace=True, axis=1)
# we will drop these two rows as is will not have a big impact on the analysis
video_game.dropna(subset=['Name'], inplace=True)
# drop the rows as it won't have a big impact on the dataframe
video_game.dropna(subset=['Publisher'], inplace=True)
# replace missing years with the median value
video_game['Year_of_Release'].fillna((video_game['Year_of_Release'].median()), inplace=True)

# create a markdown to center the title
st.markdown("<h2 style='text-align: center; color: black;'>Video Game Sales Analysis </h2>", 
            unsafe_allow_html=True)

# import an image 
st.image('img/controller.jpg')

# create a separator
st.markdown('------')

# create a header
st.header('Introduction')

# create a writing section
st.write('''For a long time seen as a subculture, the video game market has become one of the most powerful industries. 
From arcade rooms, the explosion of the market has been pushed by the release of the first gaming consoles back in the 70's, 
and hasn't ceased to grow ever since. 
''')

# create a header
st.header('The objective')

# create a writing section
st.write('''The goal of this analysis is to have a better understanding of the video game console market, 
in terms of volume sold. We will highlight the top players, identify the evolution of sales throughout the years, 
and see if one genre stands out from the others. The analysis is going to be supported by graphs, to justify the information provided.
''')

# create a header
st.header('The Data')

# create a writing section
st.write('''The dataset contains a list of video games that sold more than 100,000 copies. Each row represent a game, 
and more than 16,000 games are listed. 

The dataset is available on Kaggle [here](https://www.kaggle.com/datasets/ibriiee/video-games-sales-dataset-2022-updated-extra-feat) and 
contains the following features:

- **Name** - The name of the video game.
- **Platform** - The platform on which the game was released, such as PlayStation, Xbox, Nintendo, etc.
- **Year of Release** - The year in which the game was released.
- **Genre** - The genre of the video game, such as action, adventure, sports, etc.
- **Publisher** - The company responsible for publishing the game.
- **NA Sales**	- The sales of the game in North America.
- **EU Sales**	- The sales of the game in Europe.
- **JP Sales**	- The sales of the game in Japan.
- **Other Sales**	- The sales of the game in other regions.
- **Global Sales**	- The total sales of the game across the world.
- **Critic Score**	- The average score given to the game by professional critics.
- **Critic Count**	- The number of critics who reviewed the game.
- **User Score**	- The average score given to the game by users.
- **User Count**	- The number of users who reviewed the game.
- **Developer** - The company responsible for developing the game.
- **Rating**	- The rating assigned to the game by organizations such as the ESRB or PEGI.

As a lot of data are missing in the Critic Score, Critic Count, User Score, User Count, Developer and Rating columns. As we don't 
need them for this analysis, we will delete these columns beforehand.

We need to keep in mind that the data only focuses on gaming consoles and handheld consoles. Despite the limited data, 
we can have a good overview of the gaming console market from 1980 to 2020. The study is based on available information only, 
and therefore may not be a perfect reflection of the current market.
''')

# create a header
st.header('Which Region is the biggest market?')

# calculate the sum of sales for each region and global sales
# multiply by 1000000 as the column is in millions
NA_Sales = video_game['NA_Sales'].sum()*1000000
EU_Sales = video_game['EU_Sales'].sum()*1000000
JP_Sales = video_game['JP_Sales'].sum()*1000000
Other_Sales = video_game['Other_Sales'].sum()*1000000
Global_Sales = video_game['Global_Sales'].sum()*1000000

# create a writing section
st.write('''To have a good overview of the market on a global scale, we will look at the overall sales and see if 
a region stands out from another. We can summarize the market with the five key figures below:
''')

# print the result 
st.write("- The North American market represent {:,.0f} copies sold".format(NA_Sales))
st.write("- The European market represent {:,.0f} copies sold".format(EU_Sales))
st.write("- The Japanese market represent {:,.0f} copies sold".format(JP_Sales))
st.write("- The Other market represent {:,.0f} copies sold".format(Other_Sales))
st.write("- The Global market represent {:,.0f} copies sold".format(Global_Sales))


# create a bar chart to show total sales by region
fig_2 = px.bar(x=['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales', 'Global Sales'], 
            y=[NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales], 
            labels={'x':'Region', 'y':'Sales'},
            title='Sales by Region',
            color=[NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global_Sales])
# show the plot
st.plotly_chart(fig_2)

# create a writing section
st.write('''At first glance we can already see that the market is leaded by the North American market, 
that represent almost 50% of the global sales, with more than 4 billion copies sold. The second market, 
the European one, holds 30% of the shares, and Japan itself represent 15% of the global sales. These 3 regions 
are accountable for more than 90% of the global sales. We can now clearly understand why the top players in the industry 
are investing a lot in these regions. Furthermore, it makes sense to see the involvement of the regulators from these markets 
when it's comes to ensuring fair competition, like we are seeing now with the merger of two big players like Microsoft and 
Activison-Blizzard-King.
''')

# create a pie chart to show the share of every region in %
fig_3 = px.pie(values=[NA_Sales, EU_Sales, JP_Sales, Other_Sales], 
            names=['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales'], 
            title='Share of Sales by Region')
# add a title to the legend
fig_3.update_layout(legend_title='Market')
# show the plot
st.plotly_chart(fig_3)

# create a header
st.header('Evolution of sales throughout the years')

# create a writing section
st.write('''Now that we know the volume sold, we can legitimately ask ourselves: how have these sales been made over time?
As we can see with the line plot below, the first big gap was reached in 1996, with 200 millions copies sold, which was 
a gigantic step considering the numbers did not reach 100 millions just one year before. The trend has been positive every year 
Until it reached it's top in 2007, with almost 700 million copies sold, this a 350% increase in just 10 years! Since this date, 
the sales has been dropping every year.
''')

# count the sum of sales grouped by years
sales_year = video_game.groupby('Year_of_Release').sum().reset_index()

# create lineplot of sales by year and region
fig_4 = px.line(sales_year, x='Year_of_Release', y=sales_year.columns,
            title='Sales by Year')
# update the axis titles and legend
fig_4.update_layout(xaxis_title='Year of Release',
                yaxis_title='Copies in millions',
                legend_title='Market')
# show the plot
st.plotly_chart(fig_4)

# create a writing section
st.write('''It is interesting to see the evolution of sales per region too. The North American market was almost the only one 
present in the early 80's and has been since then the biggest market in terms of volume sold. The European and Japan markets, however, 
took more time to lift off, in the mid/late 90's. We can assume this big step in terms of sales coincides with the arrival 
of the Nintendo 64, the famous PlayStation 1, and the iconic Game Boy Color. We have to wait until the year 2000 for the position 
of the regions as we know it today to become established.
''')

# create a header
st.header('Which platform performed the best?')

# create a writing section
st.write('''Now that we have the figures in front of us, it can be no mistakes, the PlayStation 2 is the console that outperformed 
the other consoles in terms of volume of game unit sold, with no less than 1,252 million copies sold on this platform only. Followed 
next by the Xbox 360 with 970 million copies sold on this platform, and the PlayStation 3 and the Nintendo Wii with respectively 
938 million and 907 million copies sold on these platforms. We can see there is a huge gap between the first and the second platform, 
but also between the sixth and the seventh (729 million copies to 314 million copies). Some data should be treated with caution, 
the sales on platforms like, for the PlayStation 4 and Xbox One, are odd when we know the PlayStation 4 has sold over 120 million 
units.
''')

# count the sum of sales per platform and sort by global sales
sales_platform = video_game.groupby('Platform').sum().sort_values('Global_Sales', ascending=False).reset_index()

# create bar plot for global sales per platform
fig_5 = px.bar(sales_platform, x='Platform', y='Global_Sales', 
            title='Total Sales by Platform',
            color='Global_Sales')
# update axis title
fig_5.update_layout(yaxis_title='Copies in millions')
fig_5.update_xaxes(tickangle=45)
# show plot
st.plotly_chart(fig_5)

# create a writing section
st.write('''It is also very interesting to look at each region more carefully, as we see the figures are not the same. The 
North American market for example was leaded by the Xbox 360, with 600 million games sold (nearly 70% of the global sales), followed 
by the PlayStation 2 and the Nintendo Wii. The European market, however, was leader by the PlayStation 2, with 338 million games sold 
(almost 25% of the global sales), followed by the PlayStation 3 and the Xbox 360. The Japan market is in a completely different 
position, leaded by the Nintendo DS (first handheld device to be in the top) with 175 million games sold, followed by the PlayStation 
and the PlayStation 2.
''')

# count the sum of sales by region per platform
platform_NA = video_game.groupby('Platform')[['NA_Sales']].sum().sort_values('NA_Sales', ascending=False).reset_index()
platform_EU = video_game.groupby('Platform')[['EU_Sales']].sum().sort_values('EU_Sales', ascending=False).reset_index()
platform_JP = video_game.groupby('Platform')[['JP_Sales']].sum().sort_values('JP_Sales', ascending=False).reset_index()
platform_Other = video_game.groupby('Platform')[['Other_Sales']].sum().sort_values('Other_Sales', ascending=False).reset_index()

# initialize a subplot
fig_6 = sp.make_subplots(
    rows=2, cols=2,
    subplot_titles=('NA Sales', 'EU Sales', 'JP Sales', 'Other Sales'),
)
# add the four bar plots
fig_6.add_trace(px.bar(platform_NA, x='Platform', y='NA_Sales', color='NA_Sales').data[0], row=1, col=1)
fig_6.add_trace(px.bar(platform_EU, x='Platform', y='EU_Sales', color='EU_Sales').data[0], row=1, col=2)
fig_6.add_trace(px.bar(platform_JP, x='Platform', y='JP_Sales', color='JP_Sales').data[0], row=2, col=1)
fig_6.add_trace(px.bar(platform_Other, x='Platform', y='Other_Sales', color='Other_Sales').data[0], row=2, col=2)
# update the title and the dimensions
fig_6.update_layout(height=600, width=950, 
                    title_text="Video Game Sales by Platform",
                yaxis_title='Copies in millions')
# update angle of x axis
fig_6.update_xaxes(tickangle=45)
# show the plot
st.plotly_chart(fig_6)

# create a header
st.header('Who are the top players on the market?')

# create a writing section
st.write('''A video game publisher is a company that publishes video games that have been developed either internally by the 
publisher or externally by a video game developer. 

That said, we can see who are the top players on the video game market in terms of publishing games that publish games 
that sell well. Without any doubt, Nintendo is at the top of the ranking with no less than 1,788 million copies sold 
overall. Far behind, Electronic Arts is in a rather comfortable place with 1,116 million copies sold. In third position 
we have Activision with 730 million copies sold. 

The top 20 publishers are dominated by American companies, but this does not prevent other actors from slipping into the 
ranking, as we can see with Japan (Nintendo, Sony) at the top, and France (Ubisoft) at the fifth place with almost 500 million 
copies sold. This ranking makes us understand the power of the North American market as a propositional force.
''')

# count the sum of sales by publisher sorted by descending
publisher_sales = video_game.groupby('Publisher').sum().sort_values('Global_Sales', ascending=False).reset_index()[:20]

# create bar plot of top 20 publishers by global sales
fig_7 = px.bar(publisher_sales, x='Publisher', y='Global_Sales',
            title='Top 20 publishers',color='Global_Sales')
# update y axis title
fig_7.update_layout(yaxis_title='Copies in millions')
fig_7.update_xaxes(tickangle=45)
# show plot
st.plotly_chart(fig_7)

# create a writing section
st.write('''Like for the platform, every region has its own specificities when it's about publishers. Nintendo deserves its 
leadership position, with an overwhelming presence in all markets, even in the North American one with more than 800 million 
copies sold. The North American and European have a lot in common when it's about publishers, which could make sense in the 
way our cultures shares a lot of similarities, and publisher like Electronic Arts, Activision or Ubisoft are focusing on these 
specific markets. Apart from some players, we find the same companies in the top 10 publishers with little space from other 
Japanese publishers than Nintendo and Sony.

The Japanese market is, once again, against the tide, with almost only local publishers in the top 10 with very little space 
for foreign companies (Electronic Arts sold only 14 million copies). Nintendo is literally crushing the competition with 
more than 450 million copies sold, leaving the rest with only mouthfuls of bread, as Namco Bandai which sold 130 million 
copies and is the second player on the local market.
''')

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
fig_8.add_trace(px.bar(publisher_NA, x='Publisher', y='NA_Sales', color='NA_Sales').data[0], row=1, col=1)
fig_8.add_trace(px.bar(publisher_EU, x='Publisher', y='EU_Sales', color='EU_Sales').data[0], row=1, col=2)
fig_8.add_trace(px.bar(publisher_JP, x='Publisher', y='JP_Sales', color='JP_Sales').data[0], row=2, col=1)
fig_8.add_trace(px.bar(publisher_Other, x='Publisher', y='Other_Sales', color='Other_Sales').data[0], row=2, col=2)
# update the dimensions and title
fig_8.update_layout(height=1200, width=950, title_text="Top 20 publishers by Region",
                    yaxis_title='Copies in millions')
fig_8.update_xaxes(tickangle=45)
# show plot
st.plotly_chart(fig_8)

# create a header
st.header('Which is the most represented genre?')

# create a writing section
st.write('''With 12 unique genres, we can see that the genre distribution follows a rather logical curve. The 
leader is Action games, with more than 1,700 million games sold, followed by Sport games, with 1,300 copies sold and 
Shooter games are closing the top 3, with 1,000 million units sold. The gap between the top 1 and the last genre is 
quite large, with Strategy games selling 10 times less than Action games.
''')

# count the sum of sales by genre sorted by global sales
genre_sales = video_game.groupby('Genre').sum().sort_values('Global_Sales', ascending=False).reset_index()

# create bar plot 
fig_9 = px.bar(genre_sales, x='Genre', y='Global_Sales',
            title='Global Sales by Genre', color='Global_Sales')
# update y axis title
fig_9.update_yaxes(title='Copies in millions')
# show the plot
st.plotly_chart(fig_9)

# create a writing section
st.write('''Once again, the disparities between eastern and western markets are being seen here. The top 3 genres are 
exactly the same in the North American region and in the European market, which are Action, Sports and Shooter. Although 
the North American market is still the leader, Europe is not far behind with 878 millions and 519 million sales respectively for 
Action games, 683 millions and 376 million copies sold for Sports games, 592 million and 317 million unit sold for Shooter games. 
Japan is still in the same vein, with a massive majority of games that are Role-Plays with 355 million copies sold, followed by Action 
and Sport games with respectively 160 million copies and 135 million copies sold.
''')

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
fig_10.add_trace(px.bar(genre_NA, x='Genre', y='NA_Sales', color='NA_Sales').data[0], row=1, col=1)
fig_10.add_trace(px.bar(genre_EU, x='Genre', y='EU_Sales', color='EU_Sales').data[0], row=1, col=2)
fig_10.add_trace(px.bar(genre_JP, x='Genre', y='JP_Sales', color='JP_Sales').data[0], row=2, col=1)
fig_10.add_trace(px.bar(genre_Other, x='Genre', y='Other_Sales', color='Other_Sales').data[0], row=2, col=2)
# update dimensions and title
fig_10.update_layout(height=900, width=950, title_text="Sales by Genre per Region",
                    yaxis_title='Copies in millions')
fig_10.update_xaxes(tickangle=45)
# show the plot
st.plotly_chart(fig_10)

# create a writing section
st.write('''This sunburst plot allows us to have a more visual idea of the distribution of game genres according to consoles. 
We see that for the top 3 consoles the Action, Shooter and Sport genres highly represented.
''')

# create a sunburst of genres per platform
fig_11 = px.sunburst(video_game, path=['Platform', 'Genre'],
                values='Global_Sales', title='Genre distribution by platform')
# show the plot
st.plotly_chart(fig_11)

# create a header
st.header('What about the games?')

# create a writing section
st.write('''With a no-contest, Wii Sports outperforms every other game in terms of sales, with no less than 82 million 
copies sold! This is more than twice the amount of sales obtained by the second game, Super Mario Bros., with 40 million 
units sold. The top 5 games is ruled by Japanese made games, and we have to wait for the sixth place with the entrance 
of Tetris, and it's 30 millions copies sold for a western game. Out of 20 games, 14 of them comes from Japanese publishers, 
which shows the importance of this market, as a producer, in relation to the global video game scene.
''')

# top 20 games sorted by global sales
top_games = video_game.sort_values('Global_Sales', ascending=False)[:20]

# create bar plot of sales per game
fig_12 = px.bar(top_games, x='Name', y='Global_Sales', 
                title='Top 20 Games by Global Sales', color='Global_Sales')
# update y axis title
fig_12.update_layout(yaxis_title='Copies in millions',
                    xaxis_title='Game')
fig_12.update_xaxes(tickangle=45)
# show plot
st.plotly_chart(fig_12)

# create a writing section
st.write('''Once again, when we look at the distribution of the games according to their genre, we see the domination 
of Nintendo games, especially Sports games for the Wii console. Surprisingly, only two games in the top 20 are Action 
games, even if this is the leading genre in terms of global sales. Most of the games in the top 20 most sold are not part 
of the top 3 most selling genres. Which means for some genres, like Sports, only a few games made most of the sales.
''')

# create a bar plot of sales top 20 games by genre
fig_13 = px.bar(top_games, x='Name', y='Global_Sales', 
            title='Top 20 Games by Global Sales by Genre', color='Genre')
# update axis titles
fig_13.update_layout(xaxis_title='Game',
                    yaxis_title='Copies in millions')
fig_13.update_xaxes(tickangle=45)
# show plot
st.plotly_chart(fig_13)

# create a writing section
st.write('''Like for every regional analysis until now, the top-selling games make no exception. The supremacy of 
Wii Sports can be seen on the North America and European markets with respectively 41 million copies and 28 million copies 
sold, which represent 85% of the sales only on these two regions. As strange as it can be, the game doesn't even appear 
on the top 20 games of Japanese region.

With Wii Sports in the lead, the rest of the European and North American markets are quite alike, with famous game franchises 
as Call of Duty, Grand Theft Auto or even FIFA. 

The Japanese market on the other hand has almost no similarities with other markets, with the top 20 games divided with 
just a few different franchises, the most famous being Pokémon and Mario games.
''')

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
fig_14.add_trace(px.bar(game_NA, x='Name', y='NA_Sales', color='NA_Sales').data[0], row=1, col=1)
fig_14.add_trace(px.bar(game_EU, x='Name', y='EU_Sales', color='EU_Sales').data[0], row=1, col=2)
fig_14.add_trace(px.bar(game_JP, x='Name', y='JP_Sales', color='JP_Sales').data[0], row=2, col=1)
fig_14.add_trace(px.bar(game_Other, x='Name', y='Other_Sales', color='Other_Sales').data[0], row=2, col=2)
# update dimensions and titles
fig_14.update_layout(height=1200, width=1000, title_text="Top 20 Games by Region",
                    yaxis_title='Copies in millions')
fig_14.update_xaxes(tickangle=45)
# show plot
st.plotly_chart(fig_14)

# create a header
st.header('Conclusion')

# create a writing section
st.write('''Thanks to this analysis, we now have a better understanding of the video game console market, with 
some figures to keep in mind:
- The North American market represent 50% of the global market, with 4 billion copies sold
- North America and Europe follows the global trend while the Japanese market has its own specificities
- 2007 was the year with the most sales
- PlayStation 2 is the platform that sold the most games, followed by Xbox 360 and PlayStation 3.
- Sony (PlayStation) is the best player in terms of platforms
- Nintendo is the best publisher, followed by Electronic Arts and Activision
- The most represented genre is Action, followed by Sports and Shooters
- Wii Sports is the most sold game, followed by Super Mario Bros. and Mario Kart Wii
- Japan has a very important place in the video game market, even for a country with a limited local market
''')
