
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df1= pd.read_csv('fcc-forum-pageviews.csv',index_col='date') 
df1.index.name='date'


# Convert 'date' column to datetime
df1.index = pd.to_datetime(df1.index)

# Clean data
lower_bound = df1['value'].quantile(0.025)
upper_bound = df1['value'].quantile(0.975)
# Filter the DataFrame to exclude the top 2.5% and bottom 2.5%
df = df1[(df1['value'] > lower_bound) & (df1['value'] < upper_bound)]


def draw_line_plot():

    # Draw line plot
    df_line = df.copy()
    
    fig= df_line.plot(kind='line',y='value', color='red',figsize=(18, 6)).get_figure()
    
    # Adding labels and title
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    # plt.show()
    # Save image and return fig 
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy the dataframe
    df_bar = df.copy()
    
    # Reset the index to ensure the 'date' column is not the index
    df_bar.reset_index(inplace=True)
    
    # Extract year and month from the 'date' column
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.month_name()
  
    # Make the 'month' column categorical with a defined order for sorting
    df_bar['month'] = pd.Categorical(df_bar['month'],
                                     categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                                                                        ordered=True)
    
    #df for average views per month
    # used unstack to have months as columns
    df_average_views = df_bar.groupby(['year', 'month'])['value'].mean().unstack(fill_value=0)
    
    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))  
    
    # Plot the bar chart
    df_average_views.plot(kind='bar', ax=ax)
    
    # Add labels 
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views') 
    
    plt.legend(title='Months')
    # plt.tight_layout()
    # plt.show()
    
    # Save image and return fig 
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    #strftime('%b') to get month abbreviation ('Jan', 'Feb', ...)
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['month'] = pd.Categorical(df_box['month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
    # Sorting DataFrame by month
    df_box.sort_values('month', inplace=True)

    
    fig= plt.figure(figsize=(12, 6))
    
    # First subplot: Box plot by year
    plt.subplot(1, 2, 1)  # 1 row, 2 columns, first subplot
    sns.boxplot(x='year', y='value', data=df_box, hue='year',legend=False)
    plt.title('Year-wise Box Plot (Trend)')
    plt.xlabel('Year')
    plt.ylabel('Page Views')
    
    # Second subplot: Box plot by month
    plt.subplot(1, 2, 2)  # 1 row, 2 columns, second subplot
    sns.boxplot(x='month', y='value', data=df_box, hue='month', legend=False)
    plt.title('Month-wise Box Plot (Seasonality)')
    plt.xlabel('Month')
    plt.ylabel('Page Views')
    
    # Show the plot
    # plt.tight_layout()
    # plt.show()

    # Save image and return fig 
    fig.savefig('box_plot.png')
    return fig