import fastaframes as ff
import streamlit as st

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

if fasta_file and filter_file and st.button("Apply Filter"):
    try:
        with st.spinner('Filtering sequences...'):
            fasta_df = ff.to_df(fasta_file)
            filter_ids = {line.decode().rstrip() for line in filter_file.readlines()}
            filter_ids = filter_ids - {''}
            filtered_df = fasta_df[fasta_df['unique_identifier'].isin(filter_ids)]
            filter_fasta = ff.to_fasta(filtered_df).getvalue()

            missing_ids = filter_ids - set(filtered_df['unique_identifier'])

            with st.expander("Show missing IDs"):
                st.write(missing_ids)

        num_filter_ids = len(filter_ids)

        c1, c2, c3 = st.columns(3)

        # Display the metrics using st.metrics
        c1.metric(label="Protein Sequences in FASTA File", value=len(fasta_df))
        c2.metric(label="Filter IDs in TXT File", value=num_filter_ids)
        c3.metric(label="Number of sequences retained", value=len(filtered_df))

        # Provide download button
        st.download_button(label="Download FASTA", data=filter_fasta, file_name='filtered.fasta')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')
