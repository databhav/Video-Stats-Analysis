import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.sidebar.title("Video Stats Analysis Tool")
file = st.sidebar.file_uploader('Upload excel file:')
comparison_box = st.sidebar.checkbox('Compare Multiple Videos')
df = pd.read_excel(file)
#df
col1, col2 = st.columns((4,2))
if comparison_box == False:
  video_title = st.sidebar.selectbox('Select the Video to see stats for:',df['Title'].unique())
  df_new=df[df['Title']==video_title]
  # Convert 'Video Start' column to string format
  df_new['Video Start'] = df_new['Video Start'].apply(lambda x: x.strftime('%H:%M:%S'))
  #df_new

  with col1:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_new['Video Start'], y=df_new['Retention Start (%)'], fill='tozeroy', name='Retention Start (%)'))
    # Add shapes for instant declines
    for i in range(1, len(df_new)):
      decline = df_new.iloc[i - 1]['Retention Start (%)'] - df_new.iloc[i]['Retention Start (%)']
      if decline >= 1:
          fig2.add_shape(type="rect", x0=df_new.iloc[i - 1]['Video Start'], y0=0, x1=df_new.iloc[i]['Video Start'], y1=100, fillcolor="rgb(255, 99, 71)", opacity=0.5, layer="below", line=dict(width=0))
      if decline <= 0.4:
          fig2.add_shape(type="rect", x0=df_new.iloc[i - 1]['Video Start'], y0=0, x1=df_new.iloc[i]['Video Start'], y1=100, fillcolor="rgb(144, 238, 144)", opacity=0.5, layer="below", line=dict(width=0))

    fig2.update_xaxes(title_text='Time Stamp')
    fig2.update_yaxes(title_text='Retention (%)')
    st.plotly_chart(fig2,use_container_width=True)
elif comparison_box==True:
  video_title_1 = st.sidebar.selectbox('Select the Video 1 to see stats for:',df['Title'].unique())
  video_title_2 = st.sidebar.selectbox('Select the Video 2 to see stats for:',df['Title'].unique())
  df1=df[df['Title']==video_title_1]
  # Convert 'Video Start' column to string format
  df1['Video Start'] = df1['Video Start'].apply(lambda x: x.strftime('%H:%M:%S'))
  #df_new

  with col1:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df1['Video Start'], y=df1['Retention Start (%)'], fill='tozeroy', name='Retention Start (%)'))
    # Add shapes for instant declines
    for i in range(1, len(df1)):
      decline = df1.iloc[i - 1]['Retention Start (%)'] - df1.iloc[i]['Retention Start (%)']
      if decline >= 1:
          fig2.add_shape(type="rect", x0=df1.iloc[i - 1]['Video Start'], y0=0, x1=df1.iloc[i]['Video Start'], y1=100, fillcolor="rgb(255, 99, 71)", opacity=0.5, layer="below", line=dict(width=0))
      if decline <= 0.4:
          fig2.add_shape(type="rect", x0=df1.iloc[i - 1]['Video Start'], y0=0, x1=df1.iloc[i]['Video Start'], y1=100, fillcolor="rgb(144, 238, 144)", opacity=0.5, layer="below", line=dict(width=0))

    fig2.update_layout(title=f'"{video_title_1}" Retention (%) chart', xaxis_title='Time Stamp', yaxis_title='Retention (%)')
    st.plotly_chart(fig2,use_container_width=True)

    df2=df[df['Title']==video_title_2]
    # Convert 'Video Start' column to string format
    df2['Video Start'] = df2['Video Start'].apply(lambda x: x.strftime('%H:%M:%S'))
    #df_new

    with col1:
      fig3 = go.Figure()
      fig3.add_trace(go.Scatter(x=df2['Video Start'], y=df2['Retention Start (%)'], fill='tozeroy', name='Retention Start (%)'))
      # Add shapes for instant declines
      for i in range(1, len(df2)):
        decline = df2.iloc[i - 1]['Retention Start (%)'] - df2.iloc[i]['Retention Start (%)']
        if decline >= 1:
            fig3.add_shape(type="rect", x0=df2.iloc[i - 1]['Video Start'], y0=0, x1=df2.iloc[i]['Video Start'], y1=100, fillcolor="rgb(255, 99, 71)", opacity=0.5, layer="below", line=dict(width=0))
        if decline <= 0.4:
            fig3.add_shape(type="rect", x0=df2.iloc[i - 1]['Video Start'], y0=0, x1=df2.iloc[i]['Video Start'], y1=100, fillcolor="rgb(144, 238, 144)", opacity=0.5, layer="below", line=dict(width=0))
      fig3.update_layout(title=f'"{video_title_2}" Retention (%) chart', xaxis_title='Time Stamp', yaxis_title='Retention (%)')
      st.plotly_chart(fig3,use_container_width=True)



with col2:
  df_bar = df[df['Retention End (%)'].isna()]
  df_bar['Retention Lost (%)'] = 100-df_bar['Retention Start (%)']

  fig_double_bar = go.Figure()
  fig_double_bar.add_trace(go.Bar(x=df_bar['Title'], y=df_bar['Retention Start (%)'], name='Retention (%)',marker_color='rgb(144, 238, 144)',opacity=0.7))
  fig_double_bar.add_trace(go.Bar(x=df_bar['Title'], y=df_bar['Retention Lost (%)'], name='Churn(%)', marker_color='rgb(255, 99, 71)',opacity=0.7))

  fig_double_bar.update_layout(xaxis_title='Video Title', yaxis_title='Percentage', barmode='group')

  st.plotly_chart(fig_double_bar,use_container_width=True)
