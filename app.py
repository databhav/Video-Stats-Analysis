import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime

st.set_page_config(layout='wide')
st.title("Video Stats Analysis")

st.sidebar.title('Filters')
file = st.sidebar.file_uploader('Upload Excel File:')

if file:
  df = pd.read_excel(file)

  # Convert 'Video Start' to total seconds
  #df['Video Start Seconds'] = df['Video Start'].apply(time_to_seconds)
  # Convert 'Video Start' to seconds if it contains datetime.time objects
  if isinstance(df['Video Start'].iloc[0], pd.Timestamp):
      df['Video Start'] = df['Video Start'].dt.total_seconds()
  elif isinstance(df['Video Start'].iloc[0], datetime.time):
      df['Video Start'] = df['Video Start'].apply(lambda x: x.hour * 3600 + x.minute * 60 + x.second)

    # Create 'Flat line areas' column if it does not exist
  if 'Flat line areas' not in df.columns:
      df['Flat line areas'] = (df['Retention Start (%)'] - df['Retention End (%)']).abs().le(1).astype(int)

  # Identify decline areas where it is not a flat line
  df['Decline Areas'] = 1 - df['Flat line areas']

  # Add columns for Retention 10 and Retention 30 based on existing retention data
  df['Retention 10'] = df['Retention Start (%)']
  df['Retention 30'] = df['Retention End (%)']

  # Assuming `dfs` is a dictionary with dataframes
  # Extract and plot retention percentages
  retention_data = []

  # Create 'Video position (%)' if it does not exist
  if 'Video position (%)' not in df.columns:
      df['Video position (%)'] = df['Video Start'] / df.groupby('Title')['Video Start'].transform('max') * 100

  titles = df['Title'].unique()
  vs = st.sidebar.multiselect('Select Videos:',options=titles,default=titles)
  dnf = st.sidebar.checkbox("Show Decline and Flats")
  dfs = {}  # Dictionary to store the DataFrames

  for title in vs:
      dfs[title] = df[df['Title'] == title]

  colors = ['#d32f2f', '#2196f3', '#e91e63', '#42a5f5', '#f06292', '#64b5f6', '#f48fb1', '#90caf9', '#ef9a9a', '#1f77b4']
  opacity_value = 0.8
  graph_height = 600
  bar_graph_height = 500
  #df
  ## USER RETENTION CHART - fig
  fig = go.Figure()

  for i, (title, df) in enumerate(dfs.items()):
      # Plot each DataFrame as a line
      fig.add_trace(go.Scatter(
        x=df['Video position (%)'],
        y=df['Retention Start (%)'],
        mode='lines',
        name=title,
        line=dict(color=colors[i])
        ))
      if dnf == True:
        decline_x = df[df['Decline Areas'] == 1]['Video position (%)']
        decline_y = df[df['Decline Areas'] == 1]['Retention Start (%)']
        fig.add_trace(go.Scatter(
            x=decline_x,
            y=decline_y,
            mode='markers',
            marker=dict(color='red', size=6),
            showlegend=False
        ))
        flats_x = df[df['Flat line areas'] == 1]['Video position (%)']
        flats_y = df[df['Flat line areas'] == 1]['Retention Start (%)']
        fig.add_trace(go.Scatter(
            x=flats_x,
            y=flats_y,
            mode='markers',
            marker=dict(color='green', size=6),
            showlegend=False
        ))
  # Set the layout of the figure
  fig.update_layout(
    title='Multi-Line Chart',
    xaxis_title='Video position (%)',
    yaxis_title='Retention Start (%)',
    legend=dict(orientation="h", y=-0.55),
    xaxis_rangeslider_visible=True,
    height=graph_height)

  ## USER RETENTION CHART by duration - fig11
  fig11 = go.Figure()

  for i, (title, df) in enumerate(dfs.items()):
      # Plot each DataFrame as a line
      fig11.add_trace(go.Scatter(
        x=df['Video Start'],
        y=df['Retention Start (%)'],
        mode='lines',
        name=title,
        line=dict(color=colors[i])
        ))

  # Set the layout of the figure
  fig11.update_layout(
    title='Multi-Line Chart',
    xaxis_title='Video position (%)',
    yaxis_title='Retention Start (%)',
    legend=dict(orientation="h", y=-0.55),
    xaxis_rangeslider_visible=True,
    height=graph_height)

  ## STACKED GRAPH - fig2
  fig2 = go.Figure()

  for i, (title, df) in enumerate(dfs.items()):
      # Plot each DataFrame as a stacked bar
      fig2.add_trace(go.Bar(
          x=df['Video position (%)'],
          y=df['Audience Decline (%)'],
          name=title,
          marker=dict(color=colors[i])
      ))

  # Set the layout of the figure
  fig2.update_layout(
      title='Stacked Bar Graph',
      xaxis_title='Audience Decline (%)',
      yaxis_title='Video position (%)',
      barmode='stack',
      legend=dict(orientation="h", y=-0.55),
      height=graph_height,
      xaxis_rangeslider_visible=True
  )

  ## STACKED GRAPH by duration- fig22
  fig22 = go.Figure()

  for i, (title, df) in enumerate(dfs.items()):
      # Plot each DataFrame as a stacked bar
      fig22.add_trace(go.Bar(
          x=df['Video Start'],
          y=df['Audience Decline (%)'],
          name=title,
          marker=dict(color=colors[i])
      ))

  # Set the layout of the figure
  fig22.update_layout(
      title='Stacked Bar Graph',
      xaxis_title='Audience Decline (%)',
      yaxis_title='Video Start',
      barmode='stack',
      legend=dict(orientation="h", y=-0.55),
      height=graph_height,
      xaxis_rangeslider_visible=True
  )

  # first rows dataframe creation
  # Group the DataFrame by 'Retention 10', 'Retention 30', and 'Rank Retention 30', and then get unique values for each group
  first_rows_df = pd.DataFrame()

  # Iterate over each DataFrame in the dictionary
  for title, df in dfs.items():
      # Extract the first row of the DataFrame
      first_row = df.head(1)
      # Append the first row to the DataFrame storing all first rows
      first_rows_df = pd.concat([first_rows_df, first_row])

  # Reset the index of the DataFrame storing all first rows
  first_rows_df.reset_index(drop=True, inplace=True)
  #first_rows_df

  ## FLAT LINE COUNT GRAPH - fig3
  flat_line_sums = {}

  # Iterate over each DataFrame
  for title, df in dfs.items():
      # Calculate the sum of flat line areas for each title
      flat_line_sum = df['Flat line areas'].sum()
      # Store the sum in the dictionary
      flat_line_sums[title] = flat_line_sum

  # Create a DataFrame from the dictionary
  flat_line_df = pd.DataFrame(list(flat_line_sums.items()), columns=['Title', 'Sum'])

  fig3 = go.Figure()
  # Add a bar trace
  fig3.add_trace(go.Bar(
      x=flat_line_df['Title'],  # X values
      y=flat_line_df['Sum'],  # Y values
      name='Flat Line Count',  # Legend label
      marker=dict(color=colors,opacity=opacity_value)
  ))
  fig3.update_layout(
    title='Flat Line Count Graph',
    xaxis_title='Title',
    yaxis_title='Flat Line Count',
    height=bar_graph_height
    )
    
  
  ## RETENTION 30 BAR GRAPH - fig4
  fig4 = go.Figure()
  fig4.add_trace(go.Bar(
    x=first_rows_df['Title'],
    y=first_rows_df['Retention 30'],
    marker=dict(color=colors,opacity=opacity_value)
  ))
  fig4.update_layout(
    title='Retention 30 Bar Graph',
    xaxis_title='Title',
    yaxis_title='Retention 30 (%)',
    height=bar_graph_height
  )

  ## RETENTION 10 BAR GRAPH - fig5
  fig5 = go.Figure()
  fig5.add_trace(go.Bar(
    x=first_rows_df['Title'],
    y=first_rows_df['Retention 10'],
    marker=dict(color=colors,opacity=opacity_value)
  ))
  fig5.update_layout(
    title='Retention 10 Bar Graph',
    xaxis_title='Title',
    yaxis_title='Retention 10 (%)',
    height=bar_graph_height
  )

  

  col1, col2 = st.columns((4,2))
  with col1:
    col11,col12=st.columns((3,1))
    with col11:
      gs1 = st.selectbox('Select Chart',options=['User Retention Chart','Audience Decline Per Position Graph'])
    with col12:
      gs12 = st.selectbox('Select By:',options=['By Video Position','By Duration'])
    if gs1 == 'Audience Decline Per Position Graph' and gs12 == 'By Video Position':
      st.plotly_chart(fig2,use_container_width=True)
    elif gs1 == 'User Retention Chart' and gs12 == 'By Duration':
      st.plotly_chart(fig11,use_container_width=True)
    elif gs1 == 'Audience Decline Per Position Graph' and gs12 == 'By Duration':
      st.plotly_chart(fig22,use_container_width=True)
    else:
      st.plotly_chart(fig,use_container_width=True)
  with col2:
    gs2 = st.selectbox("Choose the graph to visualise:",options=['Retention 10','Retention 30','Flat Line Count'])
    if gs2 == 'Flat Line Count':# Create an empty dictionary to store the sums for each title
      st.plotly_chart(fig3, use_container_width=True)
    elif gs2 == 'Retention 30':
      st.plotly_chart(fig4,use_container_width=True)
    else:
      st.plotly_chart(fig5,use_container_width=True)
else:
  st.info("Upload the excel sheet first to continue and make sure the format of the columns, column names and file is as shown below")
  st.image("img/ss2.png")
