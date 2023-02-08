import csv

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError, OperationalError
from factory import django

from restAPI.models import *

class Command(BaseCommand):

    integrityErrors = False
    operationalErrorMessage = "One or more tables were not found, remember to migrate before import with: \n `python manage.py migrate`."
    
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

        # create unique Organism and Pfam objects from the data set
        with open('input_files/assignment_data_set.csv', newline='') as assignment_csv:
            reader = csv.reader(assignment_csv, delimiter=',')
            # empty lists for Organism and Domain objects
            organisms = []
            pfams = []
            # empty lists to track unique values
            taxa_ids = []
            pfam_ids = []

            self.stdout.write("Building organisms and pfams...")
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
                if not row[5] in pfam_ids:
                    # create a Pfam object and append it to the list
                    pfams.append(
                        Pfam(
                            domain_id=row[5],
                            domain_description=pfam_dict[row[5]]
                        )
                    )
                    # append the domain_id of this Pfam to the unique list 
                    pfam_ids.append(row[5])
        
        # bulk update the database with the Organism and Pfam objects
        try:
            Organism.objects.bulk_create(organisms)
            self.stdout.write("Updated the database with new Organisms")
        except IntegrityError:
            self.integrityErrors = True
            print("One or more Organisms already exist in the database, none were imported")
        except OperationalError as oe:
            print(oe)
            print(self.operationalErrorMessage)
            return

        try:
            Pfam.objects.bulk_create(pfams)
            self.stdout.write("Updated the database with new Pfams")
        except IntegrityError:
            self.integrityErrors = True
            print("One or more Pfams already exist in the database, none were imported")
        except OperationalError as oe:
            print(oe)
            print(self.operationalErrorMessage)
            return

        # create unique Protein objects from the data set
        with open('input_files/assignment_data_set.csv', newline='') as assignment_csv:
            reader = csv.reader(assignment_csv, delimiter=',')
            self.stdout.write("Building proteins...")
            # empty lists for Protein objects and protein_ids
            proteins = []
            protein_ids = []

            # get a dict (key: taxa_id, value: Organism object) from the database table in bulk
            # this speeds up the operation of looking up the Organism object for the 
            # Protein.taxonomy foreign key field below as it reduces database operations to one single SELECT
            # rather than looking them up in the database individually.
            try:
                organism_dict = Organism.objects.in_bulk(taxa_ids)
            except OperationalError as oe:
                print(oe)
                print(self.operationalErrorMessage)
                return
    
            for row in reader:
                # check the protein_id of this row hasn't already been seen
                if not row[0] in protein_ids:
                    # create a Protein object and append it to the list
                    proteins.append(
                        Protein(
                            protein_id=row[0],
                            length=row[8],
                            sequence=seq_dict.get(row[0]),
                            taxonomy=organism_dict[int(row[1])]
                        )
                    )
                    # append the protein_id of this protein to the unique list 
                    protein_ids.append(row[0])

        # bulk update the database with the Protein objects
        try:
            Protein.objects.bulk_create(proteins)
            self.stdout.write("Updated the database with new Proteins")
        except IntegrityError:
            self.integrityErrors = True
            print("One or more Proteins already exist in the database, none were imported")
        except OperationalError as oe:
            print(oe)
            print(self.operationalErrorMessage)
            return

        # create ProteinDomain objects from the data set and insert the records into the database
        with open('input_files/assignment_data_set.csv') as assignment_csv:
            reader = csv.reader(assignment_csv, delimiter=",")
            self.stdout.write("Building protein_domains...")
            # empty list for ProteinDomain objects
            protein_domains = []

            # get two dicts
            # (1) (key: protein_id, value: Protein object) 
            # (2) (key: domain_id, value: Domain object)
            # from the database table in bulk
            # this speeds up the operation of looking up the Protein/Domain objects for the 
            # ProteinDomain.protein_id/ProteinDomain.domain_id foreign key fields below as 
            # it reduces database operations to one single SELECT
            # rather than looking them up in the database individually.
            try:
                protein_dict = Protein.objects.in_bulk(protein_ids,field_name='protein_id')
            except OperationalError as oe:
                print(oe)
                print(self.operationalErrorMessage)
                return
            try:
                domain_dict = Pfam.objects.in_bulk(pfam_ids,field_name='domain_id')
            except OperationalError as oe:
                print(oe)
                print(self.operationalErrorMessage)
                return

            for row in reader:           
                # create a ProteinDomain object and append it to the list
                protein_domains.append(
                    ProteinDomain(
                        protein_id=protein_dict[row[0]],
                        pfam_id=domain_dict[row[5]],
                        start=row[6],
                        stop=row[7],
                        description=row[4]
                    )
                )
        
        # bulk update the database with the ProteinDomain objects
        try:
            ProteinDomain.objects.bulk_create(protein_domains)
            self.stdout.write("Updated the database with new ProteinDomains")
        except IntegrityError:
            self.integrityErrors = True
            print("One or more ProteinDomains already exist in the database, none were imported")
        except OperationalError as oe:
            self.operationalErrors = True
            print(oe)
            print(self.operationalErrorMessage)
            return

        # print a status message to the console
        if not self.integrityErrors:
            self.stdout.write("Data import finished with no errors.")
        else:
            self.stdout.write("Import script completed with errors.\nCheck that there are no pre-existing or duplicate records in your data files.")


    