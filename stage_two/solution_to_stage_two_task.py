import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# =====================================================================================

# Task 1: Generate a Volcano Plot

# =====================================================================================

# Load the RNA-seq dataset from the provided URL, ensuring correct column separation

url = "https://gist.githubusercontent.com/stephenturner/806e31fce55a8b7175af/raw/1a507c4c3f9f1baaa3a69187223ff3d3050628d4/results.txt"
transcriptomics_data = pd.read_csv(url, sep=r'\s+', engine='python')

# Compute -log10(p-value) to enhance visualisation of significance in the volcano plot
transcriptomics_data['neg_log10_pvalue'] = -np.log10(transcriptomics_data['pvalue'])

# Categorise genes based on differential expression criteria (upregulated, downregulated, or not significant)
transcriptomics_data['category'] = np.where((transcriptomics_data['log2FoldChange'] > 1) & (transcriptomics_data['pvalue'] < 0.01), 'Upregulated',
                                            np.where((transcriptomics_data['log2FoldChange'] < -1) & (transcriptomics_data['pvalue'] < 0.01), 'Downregulated', 'Not significant'))

# Generate a volcano plot to visualise differentially expressed genes

plt.figure(figsize=(10, 8))
category_colors = {'Upregulated': 'red', 'Downregulated': 'blue', 'Not significant': 'gray'}
sns.scatterplot(data=transcriptomics_data, x='log2FoldChange', y='neg_log10_pvalue', hue='category', palette=category_colors, edgecolor=None, alpha=0.7)
plt.axhline(y=-np.log10(0.01), color='black', linestyle='--')
plt.axvline(x=1, color='black', linestyle='--')
plt.axvline(x=-1, color='black', linestyle='--')

# =====================================================================================

# Task 2 & 3: Determine Upregulated and Downregulated Genes

# =====================================================================================

# Identify the top 5 upregulated and downregulated genes based on log2 fold change
top_upregulated_genes = transcriptomics_data[(transcriptomics_data['log2FoldChange'] > 1) & (transcriptomics_data['pvalue'] < 0.01)].nlargest(5, 'log2FoldChange')
top_downregulated_genes = transcriptomics_data[(transcriptomics_data['log2FoldChange'] < -1) & (transcriptomics_data['pvalue'] < 0.01)].nsmallest(5, 'log2FoldChange')

# Annotate the top 5 upregulated genes on the plot
for i, gene in top_upregulated_genes.iterrows():
    plt.text(gene['log2FoldChange'], gene['neg_log10_pvalue'], gene['Gene'], fontsize=9, ha='left', color='black', verticalalignment='bottom', horizontalalignment='right')

# Annotate the top 5 downregulated genes on the plot
for i, gene in top_downregulated_genes.iterrows():
    plt.text(gene['log2FoldChange'], gene['neg_log10_pvalue'], gene['Gene'], fontsize=9, ha='right', color='black', verticalalignment='top', horizontalalignment='left')

plt.title('Volcano Plot of Differentially Expressed Genes from RNA-Seq Analysis of X Treatment on Diseased Cell Lines')
plt.xlabel('Log2 Fold Change')
plt.ylabel('-Log10 P-value')
plt.legend(title='Expression Category', loc='upper right', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()

# Output the identified upregulated and downregulated genes

print(f"Upregulated genes:\n{top_upregulated_genes[['Gene', 'log2FoldChange', 'pvalue']]}\n")
print(f"Downregulated genes:\n{top_downregulated_genes[['Gene', 'log2FoldChange', 'pvalue']]}\n")

# =====================================================================================

# Task 4: Retrieve Functional Information of Top 5 Upregulated and Downregulated Genes

# =====================================================================================

# Function to retrieve gene functions from the Ensembl database
def get_gene_function_ensembl(gene_name):
    """Fetch gene functional information from Ensembl API."""
    url = f"https://rest.ensembl.org/lookup/symbol/human/{gene_name}?content-type=application/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            gene_info = response.json()
            # Extract Gene Ontology (GO) terms if available
            go_terms = gene_info.get('go_terms', [])
            if go_terms:
                return ', '.join(go_terms)
            # If GO terms are unavailable, use the gene description if provided
            return gene_info.get('description', "No functional information available")
        else:
            return f"Failed to retrieve data (Status code: {response.status_code})"
    except Exception as e:
        return f"Error occurred: {str(e)}"


# Retrieve functional information for the top 5 upregulated and downregulated genes, while merging the output completely
merged_gene_functions = f"Top 5 Upregulated Genes' Functions:\n"
for gene in top_upregulated_genes['Gene']:
    function = get_gene_function_ensembl(gene)
    merged_gene_functions += f"{gene}: {function}\n"

merged_gene_functions += f"\nTop 5 Downregulated Genes' Functions:\n"
for gene in top_downregulated_genes['Gene']:
    function = get_gene_function_ensembl(gene)
    merged_gene_functions += f"{gene}: {function}\n"

print(merged_gene_functions)


"""
Upregulated Genes:

#   DTHD1: Involved in apoptosis, indicating potential effects on cell survival.
#   EMILIN2: Regulates extracellular matrix and cell adhesion, suggesting tissue remodeling.
#   PI16: Modulates immune responses, hinting at anti-inflammatory properties.
#   C4orf45 and FAM180B: Poorly characterised, but their expression changes may reveal novel regulatory roles.


Downregulated Genes:

#   TBX5: Relevant in development and repair, suggesting modulation of regenerative pathways.
#   IFITM1 & IFITM3: Involved in innate immunity, implying suppression of inflammatory responses.
#   TNN & COL13A1: Structural extracellular matrix proteins, indicating possible tissue remodeling effects.


These findings demonstrate that compound X could influence apoptosis, immune signaling, and extracellular matrix invovlement, and is indicative of its therapeutic potential.
"""
