import fastaframes as ff
import streamlit as st
from filterframes import from_dta_select_filter, to_dta_select_filter



st.title("🧬 Fasta Filter 🔍")

# Instructions
instructions = """
To use this app, please follow these steps:
1. Upload a FASTA file containing protein sequences.
2. Upload a TXT file with the IDs you want to filter, one per line. (Example: `P12345`)
3. Click the "Apply Filter" button to process and download the filtered FASTA file.
"""
st.write(instructions)

fasta_file = st.file_uploader("Upload FASTA file", type=['fasta'])
filter_file = st.file_uploader("Upload TXT file", type=['txt'])

debug = st.toggle('Debug')

if fasta_file and filter_file and st.button("Apply Filter"):
    try:
        with st.spinner('Filtering sequences...'):
            fasta_df = ff.to_df(fasta_file)

            # Read DTASelect-filter.txt file and create peptide and protein dataframes
            header_lines, peptide_df, protein_df, end_lines = from_dta_select_filter(filter_file)

            if debug:
                st.dataframe(fasta_df)
                st.dataframe(protein_df)

            locus_ids = protein_df['Locus'].unique()

            filtered_df = fasta_df[fasta_df['protein_id'].isin(locus_ids)]
            filter_fasta = ff.to_fasta(filtered_df).getvalue()

        # Provide download button
        st.download_button(label="Download FASTA", data=filter_fasta, file_name='filtered.fasta')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')
