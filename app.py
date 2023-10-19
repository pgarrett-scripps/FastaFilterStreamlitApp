import fastaframes as ff
import streamlit as st

st.title("Fasta Filter")
st.write('Upload a fasta file and a txt file with the ids to filter. The ids should be one per line and '
         'correspond to the unique_identifier column in the fasta file.')

fasta_file = st.file_uploader("Upload FASTA file", type='fasta')
filter_file = st.file_uploader("Upload txt file", type='txt')

if fasta_file and filter_file and st.button("Filter"):
    fasta_df = ff.to_df(fasta_file)
    filter_ids = {line.decode().rstrip() for line in filter_file.readlines()}
    filter_ids = filter_ids - {''}
    filtered_df = fasta_df[fasta_df['unique_identifier'].isin(filter_ids)]
    filter_fasta = ff.to_fasta(filtered_df).getvalue()
    st.download_button(label="Download FASTA", data=filter_fasta, file_name='filtered.fasta')
