import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from tkinter import Tk, Label, Button, StringVar, OptionMenu, Entry
from tkinter.filedialog import askopenfilename

# Step 1: Create a file dialog to select the input table
Tk().withdraw()  # Prevents the root window from appearing immediately
file_path = askopenfilename(title="Select the input table", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])

# Step 2: Load the data
data = pd.read_csv(file_path, sep='\t', index_col=0)

# Step 3: Preprocess the data (fill missing values with the column means)
data.fillna(data.mean(), inplace=True)

# Global variables to store PCA results and clusters
kmeans_result = None
clusters = None

# Step 4: Create a function to plot the clustermap based on the selected method, color map, size, font size, and line thickness
def plot_clustermap(method, cmap, width, height, font_size, line_thickness, dendro_line_thickness):
    plt.clf()  # Clear the current figure
    sns.set(font_scale=font_size)  # Set the font size
    g = sns.clustermap(data, method=method, metric='euclidean', cmap=cmap, cbar=True, figsize=(width, height), linewidths=line_thickness)
    
    # Adjust the line thickness of the dendrogram
    for d in g.ax_row_dendrogram.collections:
        d.set_linewidth(dendro_line_thickness)
    for d in g.ax_col_dendrogram.collections:
        d.set_linewidth(dendro_line_thickness)

    plt.title(f'Heatmap with Dendrogram (Method: {method}, Color Map: {cmap})', fontsize=font_size * 10)  # Adjust title font size
    plt.xlabel('Samples', fontsize=font_size * 8)  # Adjust x-label font size
    plt.ylabel('Features', fontsize=font_size * 8)  # Adjust y-label font size
    plt.show()  # Show the plot

# Step 5: Create a function to perform PCA and plot the results
def plot_pca(pca_font_size, pc_x, pc_y):
    pca = PCA(n_components=max(pc_x, pc_y))  # Set n_components to the max of pc_x and pc_y
    pca_result = pca.fit_transform(data.T)  # Transpose data to have samples as rows

    plt.figure(figsize=(10, 7))
    plt.scatter(pca_result[:, pc_x - 1], pca_result[:, pc_y - 1], alpha=0.7)
    plt.title(f'PCA of Samples (PC{pc_x} vs PC{pc_y})', fontsize=pca_font_size * 14)
    plt.xlabel(f'Principal Component {pc_x}', fontsize=pca_font_size * 12)
    plt.ylabel(f'Principal Component {pc_y}', fontsize=pca_font_size * 12)

    # Annotate points with sample names
    for i, sample in enumerate(data.columns):
        plt.annotate(sample, (pca_result[i, pc_x - 1], pca_result[i, pc_y - 1]), fontsize=pca_font_size * 8, alpha=0.7)

    plt.grid()
    plt.show()

# Step 6: Create a function to apply KMeans clustering and color the PCA plot accordingly
def apply_kmeans_and_plot(pca_font_size, pc_x, pc_y, num_clusters):
    global kmeans_result, clusters  # Declare global variables
    pca = PCA(n_components=max(pc_x, pc_y))  # Set n_components to the max of pc_x and pc_y
    pca_result = pca.fit_transform(data.T)  # Transpose data to have samples as rows

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(pca_result)  # Fit KMeans on PCA-reduced data
    kmeans_result = pca_result  # Store PCA results globally

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(pca_result[:, pc_x - 1], pca_result[:, pc_y - 1], c=clusters, cmap='viridis', alpha=0.7)
    plt.colorbar(scatter)  # Show color bar for clusters
    plt.title(f'PCA of Samples with KMeans Clustering (PC{pc_x} vs PC{pc_y}, {num_clusters} Clusters)', fontsize=pca_font_size * 14)
    plt.xlabel(f'Principal Component {pc_x}', fontsize=pca_font_size * 12)
    plt.ylabel(f'Principal Component {pc_y}', fontsize=pca_font_size * 12)

    # Annotate points with sample names
    for i, sample in enumerate(data.columns):
        plt.annotate(sample, (pca_result[i, pc_x - 1], pca_result[i, pc_y - 1]), fontsize=pca_font_size * 8, alpha=0.7)

    plt.grid()
    plt.show()
    
    return pca_result, clusters  # Return PCA results and clusters for further processing

# Step 7: Create a function to plot line charts for each KMeans cluster
def plot_kmeans_clusters_line_chart():
    global kmeans_result, clusters  # Declare global variables
    if kmeans_result is None or clusters is None:
        print("KMeans results are not available. Please run KMeans first.")
        return

    unique_clusters = np.unique(clusters)
    plt.figure(figsize=(10, 7))

    # Calculate the average PCA result for each cluster
    for cluster in unique_clusters:
        cluster_data = kmeans_result[clusters == cluster]  # Get data for the current cluster
        average_pca = np.mean(cluster_data, axis=0)  # Compute average
        plt.plot(average_pca, label=f'Cluster {cluster}', marker='o')

    plt.title('Average PCA Results for Each KMeans Cluster')
    plt.xlabel('Principal Components')
    plt.ylabel('Average Value')
    plt.xticks(ticks=np.arange(kmeans_result.shape[1]), labels=[f'PC {i + 1}' for i in range(kmeans_result.shape[1])])
    plt.legend()
    plt.grid()
    plt.show()

# Step 8: Create a simple GUI for selecting parameters, principal components for PCA, and number of clusters for KMeans
def create_gui():
    root = Tk()
    root.title("Select Parameters for Clustering, PCA, and KMeans")

    # Label for clustering method
    label_method = Label(root, text="Select Clustering Method:")
    label_method.pack()

    # Variable to hold the selected method
    selected_method = StringVar(root)
    selected_method.set('ward')  # Default value

    # Dropdown menu for clustering methods
    methods = ['ward', 'single', 'complete', 'average', 'centroid', 'median', 'weighted']
    dropdown_method = OptionMenu(root, selected_method, *methods)
    dropdown_method.pack()

    # Label for color map
    label_cmap = Label(root, text="Select Color Map:")
    label_cmap.pack()

    # Variable to hold the selected color map
    selected_cmap = StringVar(root)
    selected_cmap.set('viridis')  # Default value

    # Dropdown menu for color maps
    color_maps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'coolwarm', 'Blues', 'Greens', 'Reds']
    dropdown_cmap = OptionMenu(root, selected_cmap, *color_maps)
    dropdown_cmap.pack()

    # Label for plot size
    label_size = Label(root, text="Enter Plot Size (Width x Height):")
    label_size.pack()

    # Entry fields for width and height
    width_entry = Entry(root)
    width_entry.insert(0, "12")  # Default width
    width_entry.pack()

    height_entry = Entry(root)
    height_entry.insert(0, "8")  # Default height
    height_entry.pack()

    # Label for font size
    label_font_size = Label(root, text="Enter Font Size (Default: 1):")
    label_font_size.pack()

    # Entry field for font size
    font_size_entry = Entry(root)
    font_size_entry.insert(0, "1")  # Default font size
    font_size_entry.pack()

    # Label for line thickness
    label_line_thickness = Label(root, text="Enter Line Thickness (Default: 0.5):")
    label_line_thickness.pack()

    # Entry field for line thickness
    line_thickness_entry = Entry(root)
    line_thickness_entry.insert(0, "0.5")  # Default line thickness
    line_thickness_entry.pack()

    # Label for dendrogram line thickness
    label_dendro_line_thickness = Label(root, text="Enter Dendrogram Line Thickness (Default: 1.0):")
    label_dendro_line_thickness.pack()

    # Entry field for dendrogram line thickness
    dendro_line_thickness_entry = Entry(root)
    dendro_line_thickness_entry.insert(0, "1.0")  # Default dendrogram line thickness
    dendro_line_thickness_entry.pack()

    # Label for principal component selection
    label_pc_x = Label(root, text="Select Principal Component for X-axis:")
    label_pc_x.pack()

    selected_pc_x = StringVar(root)
    selected_pc_x.set('1')  # Default value for PC1

    # Dropdown menu for PCA X-axis components
    pc_components = [str(i) for i in range(1, min(data.shape) + 1)]
    dropdown_pc_x = OptionMenu(root, selected_pc_x, *pc_components)
    dropdown_pc_x.pack()

    label_pc_y = Label(root, text="Select Principal Component for Y-axis:")
    label_pc_y.pack()

    selected_pc_y = StringVar(root)
    selected_pc_y.set('2')  # Default value for PC2

    # Dropdown menu for PCA Y-axis components
    dropdown_pc_y = OptionMenu(root, selected_pc_y, *pc_components)
    dropdown_pc_y.pack()

    # Label for the number of clusters for KMeans
    label_num_clusters = Label(root, text="Enter Number of Clusters for KMeans (Default: 3):")
    label_num_clusters.pack()

    # Entry field for the number of clusters
    num_clusters_entry = Entry(root)
    num_clusters_entry.insert(0, "3")  # Default number of clusters
    num_clusters_entry.pack()

    # Button to plot the heatmap
    button = Button(root, text="Plot Heatmap", command=lambda: plot_clustermap(
        selected_method.get(),
        selected_cmap.get(),
        float(width_entry.get()),
        float(height_entry.get()),
        float(font_size_entry.get()),
        float(line_thickness_entry.get()),
        float(dendro_line_thickness_entry.get())
    ))
    button.pack()

    # Button to plot PCA
    pca_button = Button(root, text="Plot PCA", command=lambda: plot_pca(
        float(font_size_entry.get()),
        int(selected_pc_x.get()),
        int(selected_pc_y.get())
    ))
    pca_button.pack()

    # Button to apply KMeans and re-plot PCA with clusters
    kmeans_button = Button(root, text="Apply KMeans and Plot Clusters", command=lambda: apply_kmeans_and_plot(
        float(font_size_entry.get()),
        int(selected_pc_x.get()),
        int(selected_pc_y.get()),
        int(num_clusters_entry.get())
    ))
    kmeans_button.pack()

    # Button to plot KMeans line charts for clusters
    line_chart_button = Button(root, text="Plot KMeans Line Charts", command=plot_kmeans_clusters_line_chart)
    line_chart_button.pack()

    root.mainloop()  # Start the main loop of the Tkinter GUI

# Step 9: Run the GUI
create_gui()
