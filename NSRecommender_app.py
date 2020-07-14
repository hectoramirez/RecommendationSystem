import streamlit as st
import pandas as pd
import textwrap


#Load and Cache the data
#@st.cache(persist=True)
def getdata():
    games_df = pd.read_csv('datasets/Games_dataset.csv', index_col=0)
    similarity_df = pd.read_csv('datasets/sim_matrix.csv', index_col=0)
    return(games_df, similarity_df)


games_df, similarity_df = getdata()[0], getdata()[1]


# Sidebar
st.sidebar.markdown('__Nintendo Switch game recommendations__  \nAn app by ' \
            '[Héctor Ramírez](https://hectoramirez.github.io/Portfolio/datascience.html)')
st.sidebar.image('images/banner.png', use_column_width=True)
st.sidebar.markdown('# Choose your game!')
st.sidebar.markdown('')
ph = st.sidebar.empty()
selected_game = ph.selectbox('Select one among the 787 games ' \
                                    'from the menu: (you can type it as well)', 
                                    [''] + games_df['Title'].to_list(), key='default',
                             format_func=lambda x: 'Select an option' if x == '' else x)

st.sidebar.markdown("# Want to know what's behind this app?") 
st.sidebar.markdown("Click on the button :point_down::")
btn = st.sidebar.button("How this app works?")
 
    
# Explanation with button 
if btn:
    selected_game = ph.selectbox('Select one among the 787 games ' \
                                    'from the menu: (you can type it as well)', 
                                    [''] + games_df['Title'].to_list(),
                                    format_func=lambda x: 'Select an option' if x == '' else x,
                                        index=0, key='button')
    
    st.markdown('# How does this app work?')
    st.markdown('---')
    st.markdown('The recommendation system used in this app employs a series of algorithms based '\
                'on unsupervised learning techniques. Namely, it process the texts and transforms '\
                'them in vectors in order to compute their similarity distance, _i.e.,_ how closely '\
                ' related two texts are.')
    st.text('')
    st.markdown('But beforehand, the dataset was obtained by scraping these two Wikipedia pages:')
    st.markdown('* https://en.wikipedia.org/wiki/List_of_Nintendo_Switch_games_(A–L)')
    st.markdown('* https://en.wikipedia.org/wiki/List_of_Nintendo_Switch_games_(M–Z)#Games_list_(M–Z)')
    st.markdown('I scraped the table entries which contain links to their video game pages. Then, '\
               'for each video game, I scraped either the Gameplay section, the Plot section, or both. '\
               'With this, I created the following dataframe:')
    
    games_df
    
        
# Recommendations    
if selected_game:
    
    # DF query
    matches = similarity_df[selected_game].sort_values()[1:6]
    matches = matches.index.tolist()
    matches = games_df.set_index('Title').loc[matches]
    matches.reset_index(inplace=True)

    # Results
    cols = ['Genre', 'Developer', 'Publisher', 'Released in: Japan', 'North America', 'Rest of countries']

    st.markdown('# The recommended games for you are:')
    for idx, row in matches.iterrows():
        st.markdown('### {} - {}'.format(str(idx + 1), row['Title']))
        st.markdown('{} [[...]](https://en.wikipedia.org{})'.format( textwrap.wrap(row['Plots'][0:], 600)[0] , row['Link']))
        st.table(pd.DataFrame(row[cols]).T.set_index('Genre'))
        st.markdown('Link to wiki page: [{}](https://en.wikipedia.org{})'.format(row['Title'], row['Link'])) 
    
else:
    if btn:
        pass
    else:
        st.warning(':point_left: Select a game from the dropdown menu!')