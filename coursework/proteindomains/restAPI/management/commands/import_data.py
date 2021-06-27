from typing import Sequence
from django.core.management.base import BaseCommand, CommandError
import csv

#from restAPI import Organism
from restAPI.models import *

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        with open('input_files/assignment_data_set.csv', newline='') as assignment_csv:
            reader = csv.reader(assignment_csv, delimiter=',')
            organisms = []
            taxa_ids = []
            proteins = []
            
            for row in reader:
                if not row[1] in taxa_ids:
                    name = row[3].split(" ",1)
                    organisms.append(Organism(taxa_id=row[1], clade=row[2], genus=name[0], species=name[1]))
                    taxa_ids.append(row[1])

            Organism.objects.bulk_create(organisms)

        with open('input_files/assignment_data_set.csv', newline='') as assignment_csv:
            reader = csv.reader(assignment_csv, delimiter=',')
            for row in reader:
                proteins.append(Protein(protein_id=row[0], length=row[8], taxonomy=Organism.objects.get(taxa_id=row[1])))
            
            Protein.objects.bulk_create(proteins)
                    
            
            with open('input_files/assignment_data_sequences .csv', newline='') as seq_csv:
                seq_reader = csv.reader(seq_csv, delimiter=',')
                for row in seq_reader:
                    Protein.objects.filter(protein_id=row[0]).update(sequence=row[1])
                    pass
                
                
        with open('input_files/pfam_descriptions.csv', newline='') as pfam_csv:
            reader = csv.reader(pfam_csv, delimiter=',')
            pfams = []
            pfam_ids = []
            for row in reader:
                if not row[0] in pfam_ids:
                    pfams.append(Domain(domain_id=row[0], domain_description=row[1]))
        
        Domain.objects.bulk_create(pfams)


#       self.stdout.write("data imported")