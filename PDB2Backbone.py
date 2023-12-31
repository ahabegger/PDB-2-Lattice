# Import Outside Libraries
import pandas as pd
from Bio import PDB
import urllib.request
import os

'''
PDB2Backbone.py
This Script takes a PDB code and creates a DataFrame containing the coordinates of the protein backbone.
'''


def create_backbone(pdb_id):
    # Define the URL for the PDB file
    pdb_url = f'https://files.rcsb.org/download/{pdb_id}.pdb'

    try:
        # Download the PDB file
        pdb_file, _ = urllib.request.urlretrieve(pdb_url, f'{pdb_id}.pdb')

        # Initialize a PDB parser
        parser = PDB.PDBParser(QUIET=True)

        # Parse the PDB file
        structure = parser.get_structure(pdb_id, pdb_file)

        # Create lists to store data
        chain_id = []
        amino_acids = []
        coordinates = [[], [], []]  # X, Y, Z

        # Iterate over all models, chains, residues, and atoms
        for model in structure:
            for chain in model:
                for residue in chain:
                    residue_name = residue.get_resname()
                    for atom in residue:
                        if atom.name == "CA":
                            chain_id.append(f"{chain.id}:{residue.id[1]}")
                            amino_acids.append(residue_name)
                            coordinates[0].append(atom.get_coord()[0])  # X
                            coordinates[1].append(atom.get_coord()[1])  # Y
                            coordinates[2].append(atom.get_coord()[2])  # Z

        # Create a DataFrame
        xyz_df = pd.DataFrame({'ID': chain_id,
                               'Amino Acid': amino_acids,
                               'X': coordinates[0],
                               'Y': coordinates[1],
                               'Z': coordinates[2]})

        # Remove the PDB file
        os.remove(f'{pdb_id}.pdb')

        return xyz_df

    except Exception as e:
        return f"Error: {str(e)}"
