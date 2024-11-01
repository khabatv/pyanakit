# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:45:22 2024

@author: past
"""
# ====================test für einzelne elemente=========================================================
# import pytest
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
# from pca_analysis import perform_pca
# 
# # Sample data path
# data_file_path = 'C:/Users/past/Documents/DataAnalysisWorkflow/testTable.txt'
# 
# @pytest.fixture(scope="module")
# def load_data():
#     # Loading the data from the provided sample file
#     data = pd.read_csv(data_file_path, sep="\t")
#     return data
# 
# def test_data_loaded_correctly(load_data):
#     # Test that data was loaded and is not empty
#     assert load_data is not None, "Data should be loaded"
#     assert not load_data.empty, "Data should not be empty"
# 
# def test_data_selection_and_cleanup(load_data ):
#     # Ensuring data selection and cleanup works properly
#     global data
#     data = load_data.copy()
#     selected_data = data.select_dtypes(include=['number']).dropna()
#     
#     # Verifying if non-numeric columns were removed and NaNs were handled
#     assert all([pd.api.types.is_numeric_dtype(dtype) for dtype in selected_data.dtypes]), "All columns should be numeric"
#     assert selected_data.isnull().sum().sum() == 0, "No NaN values should remain after cleanup"
# 
# def test_standardization(load_data ):
#     # Test standardization of data
#     global data
#     data = load_data.copy()
#     numeric_data = data.select_dtypes(include=['number']).dropna()
#     scaler = StandardScaler()
#     standardized_data = scaler.fit_transform(numeric_data)
#     
#     # Check if standardized data has mean ~0 and std ~1
#     assert abs(standardized_data.mean()) < 1e-6, "Standardized data mean should be approximately 0"
#     assert abs(standardized_data.std() - 1) < 1e-6, "Standardized data std deviation should be approximately 1"
# 
# def test_pca_performance(load_data ):
#     # Test PCA function for returning correct component count
#     global data
#     data = load_data.copy()
#     numeric_data = data.select_dtypes(include=['number']).dropna()
#     standardized_data = StandardScaler().fit_transform(numeric_data)
#     pca = PCA(n_components=2)
#     pca_result = pca.fit_transform(standardized_data)
#     
#     # PCA should reduce dimensions to 2 components
#     assert pca_result.shape[1] == 2, "PCA should result in 2 components"
# 
# def test_plotting(load_data):
#     # Testing the plotting part
#     global data
#     data = load_data.copy()
#     numeric_data = data.select_dtypes(include=['number']).dropna()
#     standardized_data = StandardScaler().fit_transform(numeric_data)
#     pca = PCA(n_components=2)
#     pca_result = pca.fit_transform(standardized_data)
#     pca_df = pd.DataFrame(data=pca_result, columns=['Principal Component 1', 'Principal Component 2'])
#     pca_df['Accession'] = data['Accession'].values[:len(pca_df)]
#     
#     # Plotting
#     plt.figure()
#     plt.scatter(pca_df['Principal Component 1'], pca_df['Principal Component 2'])
#     plt.xlabel('Principal Component 1')
#     plt.ylabel('Principal Component 2')
#     plt.title('PCA of Dataset')
#     
#     # Check that plot was created
#     assert plt.gcf().number, "Plot should be created with a figure number"
# =============================================================================

###test für alles
import pytest
import pandas as pd
from pca_analysis import perform_pca
import matplotlib.pyplot as plt
#import os


# Sample data path
data_file_path = 'C:/Users/past/Documents/DataAnalysisWorkflow/testTable.txt'
#data_file_path = os.path.join(os.path.dirname(__file__), 'testTable.txt')


@pytest.fixture(scope="module")
def load_data():
    # Load data from the provided sample file
    return pd.read_csv(data_file_path, sep="\\t", engine="python")

def test_perform_pca_integration(load_data, monkeypatch):
    # Set the data in the pca_analysis module directly
    import pca_analysis
    monkeypatch.setattr(pca_analysis, 'data', load_data.copy())
    #global data
    #data = load_data.copy()  # Setting the global data variable to test perform_pca()

    # Define a mock messagebox to intercept any error messages
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda title, message: (title, message))

    # Run the perform_pca function
    try:
        perform_pca()
        #assert pca_df is not None, "perform_pca should return a DataFrame"
    except Exception as e:
        pytest.fail(f"perform_pca raised an exception: {e}")
    
    #überprüfen, das PCA durchgeführt und ein Plot existiert
    fig = plt.gcf()
    assert fig.number, "Ein Plot sollte nach erfolgreicher PCA-Erstellung vorhanden sein."
    
    #hole aktuelle Achse und prüfe Scatterplot
    ax = plt.gca()
    
    # Überprüfe, ob Punkte im Scatter-Plot vorhanden sind
    #scatter_points = ax.collections  
    #assert scatter_points, "Der Scatterplot enthält keine Datenpunkte."
    
    scatter_points = ax.collections[0].get_offsets()
    assert len(scatter_points) > 0, "Der Scatterplot sollte Datenpunkte enthalten."
    
    
    
    # Überprüfe, ob die Achsenlimits angepasst wurden, was auf vorhandene Datenpunkte hinweist
    #xlim = ax.get_xlim()
    #ylim = ax.get_ylim()
    #assert xlim != (0.0, 1.0), "Die X-Achsenlimits sollten nicht die Standardwerte sein."
    #assert ylim != (0.0, 1.0), "Die Y-Achsenlimits sollten nicht die Standardwerte sein."
    
    #verifikation der Achsenbeschriftungen
    assert ax.get_xlabel() == "Principal Component 1", "Die X_achse sollte PCA1 darstellen  "
    assert ax.get_ylabel() == "Principal Component 2", "Die Y-Achse solle PCA2 darstellen"
    # Check that the PCA results exist as a DataFrame with 2 components
    #numeric_data = load_data.select_dtypes(include=['number']).dropna()
    #assert 'Principal Component 1' in numeric_data.columns, "PCA component 1 should be present in the output"
    #assert 'Principal Component 2' in numeric_data.columns, "PCA component 2 should be present in the output"



