from typing import Sequence
from django.core.management.base import BaseCommand, CommandError
import csv

#from restAPI import Organism
from restAPI.models import *

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        # create a dict of key: domain/pfam_id, value: sequence
        seq_dict = {}
        with open('input_files/assignment_data_sequences .csv', newline='') as seq_csv:
            seq_reader = csv.reader(seq_csv, delimiter=',')
            for row in seq_reader:
                seq_dict[row[0]] = row[1]

        # create a dict of key: protein_id, value: domain/pfam Family Description
        pfam_dict = {}
        with open('input_files/pfam_descriptions.csv', newline='') as pfam_csv:
            reader = csv.reader(pfam_csv, delimiter=',')
            for row in reader:
                pfam_dict[row[0]] = row[1]

        # create unique Organism and Domain objects from the data set
        with open('input_files/assignment_data_set.csv', newline='') as assignment_csv:
            reader = csv.reader(assignment_csv, delimiter=',')
            # empty lists for Organism and Domain objects
            organisms = []
            domains = []
            # empty lists to track unique values
            taxa_ids = []
            domain_ids = []

            self.stdout.write("Building organisms and domains...")
            for row in reader:
                # check the taxa_id of this row hasn't already been seen
                if not row[1] in taxa_ids:
                    # split the genus and species into separate parts
                    name = row[3].split(" ",1)
                    # create an Organism object and append it to the list
                    organisms.append(
                        Organism(
                            taxa_id=row[1],
                            clade=row[2],
                            genus=name[0],
                            species=name[1]
                        )
                    )
                    # append the taxa_id of this organism to the unique list 
                    taxa_ids.append(row[1])
                # check the pfam_id of this row hasn't already been seen
                if not row[5] in domain_ids:
                    # create a Domain object and append it to the list
                    domains.append(
                        Domain(
                            domain_id=row[5],
                            domain_description=pfam_dict[row[5]]
                        )
                    )
                    # append the domain_id of this organism to the unique list 
                    domain_ids.append(row[5])
        
        self.stdout.write("Updating the database")
        # bulk update the database with the Organisms and Domains objects
        Organism.objects.bulk_create(organisms)
        Domain.objects.bulk_create(domains)

        # create unique Protein objects from the data set
        with open('input_files/assignment_data_set.csv', newline='') as assignment_csv:
            reader = csv.reader(assignment_csv, delimiter=',')
            self.stdout.write("Building proteins...")
            # empty lists for Protein objects and protein_ids
            proteins = []
            protein_ids = []

            for row in reader:
                # check the protein_id of this row hasn't already been seen
                if not row[0] in protein_ids:
                    # create a Protein object and append it to the list
                    proteins.append(
                        Protein(
                            protein_id=row[0],
                            length=row[8],
                            sequence=seq_dict.get(row[0]),
                            taxonomy=Organism.objects.get(taxa_id=row[1])
                        )
                    )
                    # append the protein_id of this protein to the unique list 
                    protein_ids.append(row[0])

        self.stdout.write("Updating the database")
        # bulk update the database with the Protein objects
        Protein.objects.bulk_create(proteins)        

        # create ProteinDomain objects from the data set and insert the records into the database
        with open('input_files/assignment_data_set.csv') as assignment_csv:
            reader = csv.reader(assignment_csv, delimiter=",")
            self.stdout.write("Building protein_domains...")
            # empty list for ProteinDomain objects
            protein_domains = []
            for row in reader:           
                # create a ProteinDomain object and append it to the list
                protein_domains.append(
                    ProteinDomain(
                        protein_id=Protein.objects.get(protein_id=row[0]),
                        domain_id=Domain.objects.get(domain_id=row[5]),
                        start=row[6],
                        stop=row[7],
                        description=row[4]
                    )
                )
        
        self.stdout.write("Updating the database")
        # bulk update the database with the ProteinDomain objects
        ProteinDomain.objects.bulk_create(protein_domains)
    
        # print a status message to the console
        self.stdout.write("Data import finished with no errors.")