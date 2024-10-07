import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, StringVar, filedialog, OptionMenu, messagebox
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Global variable to store the loaded data
data = None
file_path = ""

# Step 1: Create a function to select the input table
def select_file():
    global file_path
    file_path = filedialog.askopenfilename(title="Select the input table", 
                                           filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if file_path:
        file_path_var.set(file_path)  # Update displayed file path

# Step 2: Process the data and generate plots
def process_data():
    global data, file_path
    if not file_path:
        messagebox.showerror("Error", "Please select a file first.")
        return
    
    try:
        # Load data
        data = pd.read_csv(file_path, sep="\t")  # Adjust sep if needed (e.g., comma for CSV)

        # Clean data: drop rows with NaN values
        data = data.dropna()

        # Extract treatments and biological replicates
        melted_data = data.melt(id_vars="Accession", var_name="Treatment_Sample", value_name="Value")
        
        # Extract treatment and sample information
        melted_data[['Treatment1', 'Treatment2', 'Sample']] = melted_data['Treatment_Sample'].str.split('_', expand=True, n=2)
        melted_data = melted_data.drop(columns=['Treatment_Sample'])  # Drop the original column
        
        # Choose plot type
        plot_type = plot_type_var.get()
        
        # Select treatment to compare (Treatment1 or Treatment2)
        treatment_to_compare = treatment_var.get()

        # Generate selected plot type
        plt.figure(figsize=(12, 6))

        if plot_type == "Violin Plot":
            sns.violinplot(x=treatment_to_compare, y='Value', data=melted_data, inner=None)
            overlay_data_points_and_error_bars(melted_data, treatment_to_compare)
        
        elif plot_type == "Box Plot":
            sns.boxplot(x=treatment_to_compare, y='Value', data=melted_data)
            overlay_data_points_and_error_bars(melted_data, treatment_to_compare)
        
        elif plot_type == "Bar Plot":
            summary_stats = melted_data.groupby(treatment_to_compare)['Value'].agg(['mean', 'std', 'count']).reset_index()
            summary_stats['error'] = summary_stats['std'] / summary_stats['count'] ** 0.5  # Standard error
            
            sns.barplot(x=treatment_to_compare, y='Value', data=melted_data, estimator='mean', ci=None)
            plt.errorbar(summary_stats[treatment_to_compare], summary_stats['mean'], yerr=summary_stats['error'],
                         fmt='o', color='k', capsize=5, label='Mean ± SE')

        elif plot_type == "Scatter Plot":
            sns.scatterplot(data=melted_data, x=treatment_to_compare, y='Value')
            overlay_data_points_and_error_bars(melted_data, treatment_to_compare)
        
        elif plot_type == "Line Plot":
            summary_stats = melted_data.groupby(treatment_to_compare)['Value'].agg(['mean', 'std']).reset_index()
            sns.lineplot(data=melted_data, x=treatment_to_compare, y='Value', estimator='mean', ci=None)
            plt.errorbar(summary_stats[treatment_to_compare], summary_stats['mean'], yerr=summary_stats['std'],
                         fmt='o', color='k', capsize=5, label='Mean ± SD')
        
        elif plot_type == "Strip Plot":
            sns.stripplot(x=treatment_to_compare, y='Value', data=melted_data, color='red', alpha=0.6, jitter=True)
            overlay_data_points_and_error_bars(melted_data, treatment_to_compare)

        elif plot_type == "Histogram":
            sns.histplot(melted_data['Value'], bins=20)
        
        plt.title(f'{plot_type} for {treatment_to_compare}')
        plt.xlabel(f'{treatment_to_compare}')
        plt.ylabel('Values')
        plt.xticks(rotation=45)
        plt.tight_layout()  # Ensure the layout is adjusted
        plt.legend()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to overlay data points and error bars on plots
def overlay_data_points_and_error_bars(melted_data, treatment_to_compare):
    summary_stats = melted_data.groupby(treatment_to_compare)['Value'].agg(['mean', 'std', 'count']).reset_index()
    summary_stats['error'] = summary_stats['std'] / summary_stats['count'] ** 0.5  # Standard error

    # Overlay individual data points
    sns.stripplot(x=treatment_to_compare, y='Value', data=melted_data, color='red', alpha=0.6, jitter=True, label='Data Points')

    # Overlay error bars
    plt.errorbar(summary_stats[treatment_to_compare], summary_stats['mean'], yerr=summary_stats['error'],
                 fmt='o', color='k', capsize=5, label='Mean ± SE')

# Step 3: Plot Clustermap Function
def plot_clustermap(data, method, cmap, width, height, font_size, line_thickness, dendro_line_thickness):
    plt.clf()  # Clear the current figure
    sns.set(font_scale=font_size)  # Set the font size

    # Clean data: drop rows with NaN values
    data = data.dropna()

    # Generate clustermap
    g = sns.clustermap(data.set_index('Accession'), method=method, metric='euclidean', cmap=cmap, cbar=True, 
                       figsize=(width, height), linewidths=line_thickness)
    
    # Adjust the line thickness of the dendrogram
    for d in g.ax_row_dendrogram.collections:
        d.set_linewidth(dendro_line_thickness)
    for d in g.ax_col_dendrogram.collections:
        d.set_linewidth(dendro_line_thickness)

    plt.title(f'Heatmap with Dendrogram (Method: {method}, Color Map: {cmap})', fontsize=font_size * 10)  # Adjust title font size
    plt.xlabel('Samples', fontsize=font_size * 8)  # Adjust x-label font size
    plt.ylabel('Features', fontsize=font_size * 8)  # Adjust y-label font size
    plt.tight_layout()  # Ensure the layout is adjusted
    plt.show()

# Step 4: Perform PCA and plot
def perform_pca():
    global data
    if data is None:
        messagebox.showerror("Error", "Please select a file and load data first.")
        return

    try:
        # Drop non-numeric columns and handle NaNs
        numeric_data = data.select_dtypes(include=['number']).dropna()
        
        # Standardize the data
        standardized_data = StandardScaler().fit_transform(numeric_data)

        # Perform PCA
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(standardized_data)

        # Create a DataFrame for PCA results
        pca_df = pd.DataFrame(data=pca_result, columns=['Principal Component 1', 'Principal Component 2'])
        pca_df['Accession'] = data['Accession']  # Add Accession back for labeling

        # Plot PCA results
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Principal Component 1', y='Principal Component 2', data=pca_df)
        plt.title('PCA of Data')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during PCA: {str(e)}")

# Step 5: Set up the GUI
root = Tk()
root.title("Data Analysis Tool")
file_path_var = StringVar()
plot_type_var = StringVar(value="Violin Plot")  # Default plot type
treatment_var = StringVar(value="Treatment2")  # Default treatment to compare
cluster_method_var = StringVar(value="average")  # Default clustering method
color_map_var = StringVar(value="viridis")  # Default color map

# Create UI elements
label = Label(root, text="Selected file:")
label.pack()

file_path_entry = Label(root, textvariable=file_path_var, wraplength=400)
file_path_entry.pack()

select_file_button = Button(root, text="Select File", command=select_file)
select_file_button.pack()

# Dropdown menu for plot types
plot_type_label = Label(root, text="Select Plot Type:")
plot_type_label.pack()
plot_type_menu = OptionMenu(root, plot_type_var, 
                             "Violin Plot", 
                             "Box Plot", 
                             "Bar Plot", 
                             "Scatter Plot", 
                             "Line Plot", 
                             "Strip Plot", 
                             "Histogram", 
                             "Clustermap")  # Added Clustermap option
plot_type_menu.pack()

# Dropdown menu for selecting treatment to compare
treatment_label = Label(root, text="Select Treatment to Compare:")
treatment_label.pack()
treatment_menu = OptionMenu(root, treatment_var, "Treatment1", "Treatment2")
treatment_menu.pack()

# Button to process data and generate plots
process_button = Button(root, text="Process Data and Generate Plots", command=process_data)
process_button.pack()

# Button to plot Clustermap
clustermap_button = Button(root, text="Plot Clustermap", 
                            command=lambda: plot_clustermap(data, 
                                                             cluster_method_var.get(), 
                                                             color_map_var.get(), 
                                                             10, 8, 1, 0.1, 0.5))  # Example parameters
clustermap_button.pack()

# Button to perform PCA
pca_button = Button(root, text="Perform PCA", command=perform_pca)
pca_button.pack()

# Start the GUI
root.mainloop()
