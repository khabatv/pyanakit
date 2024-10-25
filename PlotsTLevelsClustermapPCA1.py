import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, StringVar, filedialog, OptionMenu, messagebox, LabelFrame
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import ttest_ind
from scipy.stats import f_oneway

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

        # Add statistical analysis before plotting
        t_stat, t_p_value = None, None
        f_stat, f_p_value = None, None
       
        # Perform statistical analysis
        if treatment_to_compare == "Treatment1":
            print("Performing statistical analysis for Treatment1...")
            t_stat, t_p_value = add_statistical_analysis(melted_data, treatment_to_compare)
        else:
            print(f"Performing ANOVA analysis for {treatment_to_compare}...")
            f_stat, f_p_value = add_anova_analysis(melted_data, treatment_to_compare)

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
            #orange an blue data point on the plot, the same datapoint-information? 
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
            
        ####################################
        elif plot_type == "Heatmap":
            if treatment_to_compare not in ["Treatment1", "Treatment2"]:
                raise ValueError("Unsupported treatment specified.")

            if treatment_to_compare == "Treatment1":
                unique_treatment = melted_data['Treatment1']
            elif treatment_to_compare == "Treatment2":
                unique_treatment = melted_data['Treatment1'] + "_" + melted_data['Treatment2']
            else:
                unique_treatment = melted_data['Treatment1'] + "_" + melted_data['Treatment2'] + "_" + melted_data['Sample']

            melted_data['Unique_Treatment'] = unique_treatment

            heatmap_data = pd.pivot_table(melted_data, index="Accession", columns="Unique_Treatment", values="Value", aggfunc="mean")
            sns.heatmap(heatmap_data, cmap="YlGnBu", annot=False)
        
        elif plot_type == "Swarm Plot":
            #durch overlay_data.. wird der plot schon kreiiert mit zwei Farben, -> sns. swarmplot unnötig
            sns.swarmplot(x=treatment_to_compare, y='Value', data=melted_data)
            overlay_data_points_and_error_bars(melted_data, treatment_to_compare)
        ####################################
        
        if t_stat is not None and t_p_value is not None:
            plt.title(f't-stat: {t_stat:.4f}, p-value: {t_p_value:.4f}', 
                     ha='center')#, va='center', transform=plt.gca().transAxes, color='blue')
        if f_stat is not None and f_p_value is not None:
            plt.title(f'F-stat: {f_stat:.4f}, p-value: {f_p_value:.4f}', fontsize = 10, 
                     ha='center', va='top', x=0.47, y=1.02, color='blue')
            
        
        plt.suptitle(f'{plot_type} for {treatment_to_compare}', fontsize = 18, ha='center', x=0.5)
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
    # Standard error of the mean? What is the message of this plot? Variety of datapoints or "correctnes" of mean? 
    summary_stats['error'] = summary_stats['std'] / summary_stats['count'] ** 0.5  

    # Overlay individual data points
    sns.stripplot(x=treatment_to_compare, y='Value', data=melted_data, color='red', alpha=0.6, jitter=True)#, label='Data Points'),no valuable information cause one color 

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
        
###################################################################################################
def add_statistical_analysis(melted_data, treatment_to_compare):
    # Conduct a t-test between two treatments if applicable
    treatments = melted_data[treatment_to_compare].unique()
    if len(treatments) == 2:
        group1 = melted_data[melted_data[treatment_to_compare] == treatments[0]]['Value']
        group2 = melted_data[melted_data[treatment_to_compare] == treatments[1]]['Value']
        # Perform the t-test (independant?)
        t_stat, p_value = ttest_ind(group1, group2)
        print(f"t-statistic: {t_stat}, p-value: {p_value}")
        return t_stat, p_value
        
    else:
        print("No statistic! Current statistical analysis requires exactly two or more treatments.")
        return None, None
    
def add_anova_analysis(melted_data, treatment_to_compare):
    # Perform ANOVA between multiple treatments
    treatments = melted_data[treatment_to_compare].unique()
    if len(treatments) > 2:
        groups = [melted_data[melted_data[treatment_to_compare] == t]['Value'] for t in treatments]
        f_stat, p_value = f_oneway(*groups)
        
        print(f"ANOVA F-statistic: {f_stat}, p-value: {p_value}")
        return f_stat, p_value
    else:
        print("ANOVA requires more than two treatments.")
        return None, None
###################################################################################################

# Step 5: Set up the GUI
root = Tk()
root.title("Data Analysis Tool")
root.geometry("600x300")

file_path_var = StringVar()
plot_type_var = StringVar(value="Violin Plot")  # Default plot type
treatment_var = StringVar(value="Treatment2")  # Default treatment to compare
cluster_method_var = StringVar(value="average")  # Default clustering method
color_map_var = StringVar(value="viridis")  # Default color map

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)


# Create UI elements
label = Label(root, text="Selected file:")
#label.pack()
label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

file_path_entry = Label(root, textvariable=file_path_var, wraplength=400, bg ="ghostwhite")
#file_path_entry.pack()
file_path_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

select_file_button = Button(root, text="Select File", command=select_file)
#select_file_button.pack()
select_file_button.grid(row=1, column=2, padx=5, pady=5, sticky='e')

# Dropdown menu for plot types
plot_type_label = Label(root, text="Select Plot Type:")
#plot_type_label.pack()
plot_type_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

plot_type_menu = OptionMenu(root, plot_type_var, 
                             "Violin Plot", 
                             "Box Plot", 
                             "Bar Plot", 
                             "Scatter Plot", 
                             "Line Plot", 
                             "Strip Plot", 
                             "Histogram", 
                             #"Clustermap", # Added Clustermap option
                             "Swarm Plot", 
                             "Heatmap")  
#plot_type_menu.pack()
plot_type_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

# Dropdown menu for selecting treatment to compare
treatment_label = Label(root, text="Select Treatment to Compare:")
#treatment_label.pack()
treatment_label.grid(row=3, column=0, padx=5, pady=5, sticky='w') 

treatment_menu = OptionMenu(root, treatment_var, "Treatment1", "Treatment2")
#treatment_menu.pack()
treatment_menu.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

# Button to process data and generate plots
process_button = Button(root, text="Process Data and Generate Plots", command=process_data)
#process_button.pack()
process_button.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='ew')  

label_frame = LabelFrame(root, text = "Advanced insights:", labelanchor = "nw")
label_frame.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='ew') 
label_frame.columnconfigure(0, weight=1)  
label_frame.columnconfigure(1, weight=1)  
#label_frame.columnconfigure(2, weight=1)

# Button to plot Clustermap
clustermap_button = Button(label_frame, text="Plot Clustermap", 
                            command=lambda: plot_clustermap(data, 
                                                             cluster_method_var.get(), 
                                                             color_map_var.get(), 
                                                             10, 8, 1, 0.1, 0.5))  # Example parameters
#clustermap_button.pack()
clustermap_button.grid(row=0, column=0, #columnspan=3,
                       padx=5, pady=5, sticky='ew') 

# Button to perform PCA
pca_button = Button(label_frame, text="Perform PCA", command=perform_pca)
#pca_button.pack()
pca_button.grid(row=0, column=1, #columnspan=3, 
                padx=5, pady=5, sticky='ew') 

# Start the GUI
root.mainloop()
