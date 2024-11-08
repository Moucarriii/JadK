import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '325-Project.xlsx'  # Update with the correct path if necessary
data = pd.read_excel(file_path)

# Convert Last GPA values over 4 to a 4.0 scale, and set any non-student entries to 0
data['Last GPA - (Enter 0 if non-students)'] = data['Last GPA - (Enter 0 if non-students)'].apply(
    lambda x: x / 25 if x > 4 else (x if x > 0 else 0)
)

# Convert Current Test Scores values over 4 to a 4.0 scale, and set any non-student entries to 0
data['Current test scores(average) - (Enter 0 if non-students)'] = data['Current test scores(average) - (Enter 0 if non-students)'].apply(
    lambda x: x / 25 if x > 4 else (x if x > 0 else 0)
)

# Sidebar filter for Region
st.sidebar.header("Filter Criteria")
region_options = data['Region'].unique()
selected_region = st.sidebar.multiselect("Select Region(s)", region_options, default=region_options)

# Selection between Last GPA and Current Test Scores
gpa_type = st.sidebar.radio("Select GPA Type", ["Last GPA", "Current Test Scores"])

# Apply filters based on the selection
filtered_data = data[data['Region'].isin(selected_region)]

# Display the filtered data based on GPA type
if gpa_type == "Last GPA":
    gpa_column = 'Last GPA - (Enter 0 if non-students)'
else:
    gpa_column = 'Current test scores(average) - (Enter 0 if non-students)'

# Filtered data view
st.write("Filtered Data", filtered_data[['Region', gpa_column]])

# Create a bar chart and line chart to show average GPA by Region based on the selection
if not filtered_data.empty:
    avg_gpa_by_region = filtered_data.groupby('Region')[gpa_column].mean()

    # Plotting both charts side-by-side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Bar Chart
    avg_gpa_by_region.plot(kind='bar', color='skyblue', ax=ax1)
    ax1.set_xlabel("Region")
    ax1.set_ylabel(f"Average {gpa_type}")
    ax1.set_title(f"Average {gpa_type} by Region (Bar Chart)")

    # Line Chart
    avg_gpa_by_region.plot(kind='line', marker='o', color='purple', ax=ax2)
    ax2.set_xlabel("Region")
    ax2.set_ylabel(f"Average {gpa_type}")
    ax2.set_title(f"Average {gpa_type} by Region (Line Chart)")

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    st.write("No data available for the selected filters.")
