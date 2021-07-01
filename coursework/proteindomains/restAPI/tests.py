import json
from io import StringIO

from django.urls import reverse
from django.db.utils import IntegrityError
from django.core.management import call_command
from rest_framework.test import APITestCase, APITransactionTestCase

from .model_factories import *
from .serializers import *

# test cases for import script and resulting database
class ImportDataScriptTest(APITransactionTestCase):
    
    outMessage = ""

    def setUp(self):
        self.outMessage = StringIO()
        call_command('importdata', stdout=self.outMessage)

    # check import script completes successfully
    def test_commandOutput(self):
        self.assertIn("Data import finished with no errors.", self.outMessage.getvalue())
    
    # check correct number of records created (from given dataset only)
    def test_correctNumberOfProteinsCreated(self):
        self.assertEqual(len(Protein.objects.all()), 9988)
    
    def test_correctNumberOfOrganismsCreated(self):
        self.assertEqual(len(Organism.objects.all()), 1995)

    def test_correctNumberOfPfamsCreated(self):
        self.assertEqual(len(Pfam.objects.all()), 2453)
    
    def test_correctNumberOfProteinDomainsCreated(self):
        self.assertEqual(len(ProteinDomain.objects.all()), 10000)

# test cases for the Protein API, endpoint 1
class ProteinAPITest(APITestCase):

    protein1 = None
    good_url = ''
    bad_url = ''
    good_url_get_response = None
    good_url_get_response_json = None

    def setUp(self):
        self.protein1 = ProteinFactory.create()
        self.good_url = reverse('GET_protein_api', kwargs={"protein_id": self.protein1.protein_id})
        self.bad_url = reverse('GET_protein_api', kwargs={"protein_id": "XXXXXX"})
        self.good_url_get_response = self.client.get(self.good_url)
        self.bad_url_response = self.client.get(self.bad_url)
        self.good_url_get_response_json = json.loads(self.good_url_get_response.content)

    def tearDown(self):
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        Organism.objects.all().delete()
        OrganismFactory.reset_sequence(0)
        
    def test_ProteinDetailReturnSuccess(self):
        self.assertEqual(self.good_url_get_response.status_code, 200)

    def test_ProteinDetailProteinIdRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['protein_id'], self.protein1.protein_id)

    def test_ProteinDetailSequenceRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['sequence'], self.protein1.sequence)

    def test_ProteinDetailTaxonomyRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['taxonomy']['taxa_id'], self.protein1.taxonomy.taxa_id)
    
    def test_ProteinDetailLengthRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['length'], self.protein1.length)

    def test_ProteinDetailNumberOfPfamsRecievedCorrect(self):
        self.assertEqual(len(self.good_url_get_response_json['domains']), len(self.protein1.domains.values()))

    def test_ProteinDetailReturnFailOnBadDomainId(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_ProteinPostMethodNotAllowed(self):
        response = self.client.post(self.good_url)
        self.assertEqual(response.status_code, 405)

    def test_ProteinPutMethodNotAllowed(self):
        response = self.client.put(self.good_url)
        self.assertEqual(response.status_code, 405)
        
    def test_ProteinPatchMethodNotAllowed(self):
        response = self.client.patch(self.good_url)
        self.assertEqual(response.status_code, 405)
    
    def test_ProteinDeleteMethodNotAllowed(self):
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 405)

    def test_ProteinPostGoodProteinSuccessful(self):
        url = reverse('POST_protein_api')
        protein = ProteinFactory.build()
        organism = OrganismFactory.create()
        response = self.client.post(url, {
            "taxonomy": organism.taxa_id,
            "protein_id": protein.protein_id,
            "sequence": protein.sequence,
            "length": protein.length
        }, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_ProteinPostDuplicateProteinIdIsUnsuccessful(self):
        url = reverse('POST_protein_api')
        protein1 = ProteinFactory.create()
        protein2 = ProteinFactory.build()
        response = self.client.post(url, {
            "taxonomy": protein2.taxonomy.taxa_id,
            "protein_id": protein1.protein_id,
            "sequence": protein2.sequence,
            "length": protein2.length
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_ProteinPostGoodProteinTaxonomyCorrect(self):
        url = reverse('POST_protein_api')
        protein = ProteinFactory.build()
        organism = OrganismFactory.create()
        response = self.client.post(url, {
            "taxonomy": organism.taxa_id,
            "protein_id": protein.protein_id,
            "sequence": protein.sequence,
            "length": protein.length
        }, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response_json['taxonomy'], organism.taxa_id)
    
    def test_ProteinPostGoodProteinProteinIdCorrect(self):
        url = reverse('POST_protein_api')
        protein = ProteinFactory.build()
        organism = OrganismFactory.create()
        response = self.client.post(url, {
            "taxonomy": organism.taxa_id,
            "protein_id": protein.protein_id,
            "sequence": protein.sequence,
            "length": protein.length
        }, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response_json['protein_id'], protein.protein_id)

    def test_ProteinPostGoodProteinSequenceCorrect(self):
        url = reverse('POST_protein_api')
        protein = ProteinFactory.build()
        organism = OrganismFactory.create()
        response = self.client.post(url, {
            "taxonomy": organism.taxa_id,
            "protein_id": protein.protein_id,
            "sequence": protein.sequence,
            "length": protein.length
        }, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response_json['sequence'], protein.sequence)

    def test_ProteinPostGoodProteinSequenceCorrect(self):
        url = reverse('POST_protein_api')
        protein = ProteinFactory.build()
        organism = OrganismFactory.create()
        response = self.client.post(url, {
            "taxonomy": organism.taxa_id,
            "protein_id": protein.protein_id,
            "sequence": protein.sequence,
            "length": protein.length
        }, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response_json['length'], protein.length)

# test cases for the Pfam API, endpoint 2
class PfamAPITest(APITestCase):

    pfam1 = None
    pfam2 = None
    good_url = ''
    bad_url = ''
    good_url_get_response = None
    good_url_get_response_json = None

    def setUp(self):
        self.pfam1 = PfamFactory.create(domain_id = "CoiledCoil", domain_description = "coil prediction")
        self.pfam2 = PfamFactory.create(domain_id = "PF00014", domain_description = "Kunitz/Bovinepancreatictrypsininhibitordomain")
        self.good_url = reverse('pfam_api', kwargs={"domain_id": "PF00014"})
        self.bad_url = reverse('pfam_api', kwargs={"domain_id": "XXXXXX"})
        self.good_url_get_response = self.client.get(self.good_url)
        self.good_url_get_response_json = json.loads(self.good_url_get_response.content)

    def tearDown(self):
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)
    
    def test_PfamDetailReturnSuccess(self):
        self.assertEqual(self.good_url_get_response.status_code, 200)

    def test_PfamDetailDomainIdRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['domain_id'], "PF00014")

    def test_PfamDetailDomainDescriptionRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['domain_description'], "Kunitz/Bovinepancreatictrypsininhibitordomain")

    def test_PfamDetailReturnFailOnBadDomainId(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_PfamPostMethodNotAllowed(self):
        response = self.client.post(self.good_url)
        self.assertEqual(response.status_code, 405)

    def test_PfamPutMethodNotAllowed(self):
        response = self.client.put(self.good_url)
        self.assertEqual(response.status_code, 405)
        
    def test_PfamPatchMethodNotAllowed(self):
        response = self.client.patch(self.good_url)
        self.assertEqual(response.status_code, 405)
    
    def test_PfamDeleteMethodNotAllowed(self):
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 405)

# test cases for the proteins by organism API, endpoint 3
class OrgansimProteinAPITest(APITestCase):

    Organism = None
    protein1 = None
    protein2 = None
    good_url = ''
    bad_url = ''
    good_url_get_response = None
    good_url_get_response_json = None

    def setUp(self):
        self.organism = OrganismFactory.create()
        self.protein1 = ProteinFactory.create(protein_id="AAA", taxonomy=self.organism)
        self.protein2 = ProteinFactory.create(protein_id="BBB", taxonomy=self.organism)
        self.good_url = reverse('organism_protein_api', kwargs={"taxa_id": self.organism.taxa_id})
        self.bad_url = reverse('organism_protein_api', kwargs={"taxa_id": 99999})
        self.good_url_get_response = self.client.get(self.good_url)
        self.good_url_get_response_json = json.loads(self.good_url_get_response.content)

    def tearDown(self):
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        Organism.objects.all().delete()
        OrganismFactory.reset_sequence(0)
    
    def test_OrganismProteinDetailReturnSuccess(self):
        self.assertEqual(self.good_url_get_response.status_code, 200)

    def test_OrganismProteinDetailProteinIdsRecievedCorrect(self):
        self.assertEqual(
            set([
                self.good_url_get_response_json[0]['protein_id'],
                self.good_url_get_response_json[1]['protein_id']
            ]),
            set([
                self.protein1.protein_id,
                self.protein2.protein_id
            ])
        )

    def test_OrganismProteinDetailReturnFailOnBadDomainId(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_OrganismProteinPostMethodNotAllowed(self):
        response = self.client.post(self.good_url)
        self.assertEqual(response.status_code, 405)

    def test_OrganismProteinPutMethodNotAllowed(self):
        response = self.client.put(self.good_url)
        self.assertEqual(response.status_code, 405)
        
    def test_OrganismProteinPatchMethodNotAllowed(self):
        response = self.client.patch(self.good_url)
        self.assertEqual(response.status_code, 405)
    
    def test_OrganismProteinDeleteMethodNotAllowed(self):
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 405)


# test cases for the OrganismProteinDomain API, endpoint 2
class OrganismProteinDomainAPITest(APITestCase):

    organism = None
    pfam1 = None
    pfam2 = None
    proteinA = None
    proteinB = None
    domainA1 = None
    domainA2 = None
    domainB1 = None
    domainB2 = None

    good_url = ''
    bad_url = ''
    good_url_get_response = None
    good_url_get_response_json = None

    def setUp(self):
        self.organism = OrganismFactory.create()
        self.pfam1 = PfamFactory.create()
        self.pfam2 = PfamFactory.create()
        self.proteinA = ProteinFactory.create(protein_id="AAA", taxonomy=self.organism)
        self.proteinB = ProteinFactory.create(protein_id="BBB", taxonomy=self.organism)
        self.domainA1 = ProteinDomainFactory.create(protein_id=self.proteinA, pfam_id=self.pfam1)
        self.domainA2 = ProteinDomainFactory.create(protein_id=self.proteinA, pfam_id=self.pfam2)
        self.domainB1 = ProteinDomainFactory.create(protein_id=self.proteinB, pfam_id=self.pfam1)
        self.domainB2 = ProteinDomainFactory.create(protein_id=self.proteinB, pfam_id=self.pfam2)
        self.good_url = reverse('organism_protein_domain_api', kwargs={"taxa_id": self.organism.taxa_id})
        self.bad_url = reverse('organism_protein_domain_api', kwargs={"taxa_id": 99999})
        self.good_url_get_response = self.client.get(self.good_url)
        self.good_url_get_response_json = json.loads(self.good_url_get_response.content)

    def tearDown(self):
        ProteinDomain.objects.all().delete()
        ProteinDomainFactory.reset_sequence(0)
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        Organism.objects.all().delete()
        OrganismFactory.reset_sequence(0)
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)
    
    def test_OrganismProteinDomainDetailReturnSuccess(self):
        self.assertEqual(self.good_url_get_response.status_code, 200)

    def test_OrganismProteinDomainDetailDomainIdsRecievedCorrect(self):
        self.assertEqual(
            set([
                self.good_url_get_response_json[0]['pfam_id']['domain_id'],
                self.good_url_get_response_json[1]['pfam_id']['domain_id'],
                self.good_url_get_response_json[2]['pfam_id']['domain_id'],
                self.good_url_get_response_json[3]['pfam_id']['domain_id']
            ]),
            set([
                self.domainA1.pfam_id.domain_id,
                self.domainA2.pfam_id.domain_id,
                self.domainB1.pfam_id.domain_id,
                self.domainB1.pfam_id.domain_id
            ])
        )
    
    def test_OrganismProteinDomainDetailDomainDescriptionsRecievedCorrect(self):
        self.assertEqual(
            set([
                self.good_url_get_response_json[0]['pfam_id']['domain_description'],
                self.good_url_get_response_json[1]['pfam_id']['domain_description'],
                self.good_url_get_response_json[2]['pfam_id']['domain_description'],
                self.good_url_get_response_json[3]['pfam_id']['domain_description']
            ]),
            set([
                self.domainA1.pfam_id.domain_description,
                self.domainA2.pfam_id.domain_description,
                self.domainB1.pfam_id.domain_description,
                self.domainB1.pfam_id.domain_description
            ])
        )

    def test_OrganismProteinDomainDetailReturnFailOnBadDomainId(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_OrganismProteinDomainPostMethodNotAllowed(self):
        response = self.client.post(self.good_url)
        self.assertEqual(response.status_code, 405)

    def test_OrganismProteinDomainPutMethodNotAllowed(self):
        response = self.client.put(self.good_url)
        self.assertEqual(response.status_code, 405)
        
    def test_OrganismProteinDomainPatchMethodNotAllowed(self):
        response = self.client.patch(self.good_url)
        self.assertEqual(response.status_code, 405)
    
    def test_OrganismProteinDomainDeleteMethodNotAllowed(self):
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 405)


# test cases from the coverage API, endpoint 5
class ProteinCoverageTest(APITestCase):

    organism = None
    pfam1 = None
    pfam2 = None
    proteinA = None
    domainA1 = None
    domainA2 = None
    good_url = ''
    bad_url = ''
    good_url_get_response = None
    good_url_get_response_json = None

    def setUp(self):
        self.organism = OrganismFactory.create()
        self.pfam1 = PfamFactory.create()
        self.pfam2 = PfamFactory.create()
        self.proteinA = ProteinFactory.create(protein_id="AAA", taxonomy=self.organism)
        self.domainA1 = ProteinDomainFactory.create(protein_id=self.proteinA, pfam_id=self.pfam1)
        self.domainA2 = ProteinDomainFactory.create(protein_id=self.proteinA, pfam_id=self.pfam2)
        self.good_url = reverse('protein_coverage_api', kwargs={"protein_id": self.proteinA.protein_id})
        self.bad_url = reverse('protein_coverage_api', kwargs={"protein_id": "XXXXXX"})
        self.good_url_get_response = self.client.get(self.good_url)
        self.good_url_get_response_json = json.loads(self.good_url_get_response.content)

    def tearDown(self):
        ProteinDomain.objects.all().delete()
        ProteinDomainFactory.reset_sequence(0)
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        Organism.objects.all().delete()
        OrganismFactory.reset_sequence(0)
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)

    def test_CoverageDetailReturnSuccess(self):
        self.assertEqual(self.good_url_get_response.status_code, 200)
    
    def test_CoverageDetailCalculationCorrect(self):
        totalDomainLength = self.domainA1.stop - self.domainA1.start + self.domainA2.stop - self.domainA2.start
        coverage = totalDomainLength / self.proteinA.length
        self.assertEqual(self.good_url_get_response_json['coverage'], coverage)

    def test_CoverageDetailReturnFailOnBadDomainId(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_CoveragePostMethodNotAllowed(self):
        response = self.client.post(self.good_url)
        self.assertEqual(response.status_code, 405)

    def test_CoveragePutMethodNotAllowed(self):
        response = self.client.put(self.good_url)
        self.assertEqual(response.status_code, 405)
        
    def test_CoveragePatchMethodNotAllowed(self):
        response = self.client.patch(self.good_url)
        self.assertEqual(response.status_code, 405)
    
    def test_CoverageDeleteMethodNotAllowed(self):
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 405)
    

# test cases for the Pfam database constraints
class PfamTransactionTest(APITransactionTestCase):

    pfam = None
    
    def setUp(self):
        self.pfam = PfamFactory.create()
    
    def tearDown(self):
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)

    def test_PfamUniqueConstraintOnDomainId(self):
        with self.assertRaises(IntegrityError):
            PfamFactory.create(domain_id=self.pfam.domain_id)

    def test_PfamNotUniqueDomainDescriptionIsAllowed(self):
        try:
            PfamFactory.create(domain_description=self.pfam.domain_description)
        except IntegrityError:
            self.fail("an integrity error was generated on this operation, which wasn't expected")


# test cases for the Protein database constraints
class ProteinTransactionTest(APITransactionTestCase):

    protein = None
    
    def setUp(self):
        self.protein = ProteinFactory.create()
    
    def tearDown(self):
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)

    def test_ProteinUniqueConstraintOnProteinId(self):
        with self.assertRaises(IntegrityError):
            ProteinFactory.create(protein_id=self.protein.protein_id)

    def test_ProteinNotUniqueOrganismIsAllowed(self):
        try:
            ProteinFactory.create(taxonomy=self.protein.taxonomy)
        except IntegrityError:
            self.fail("an integrity error was generated on this operation, which wasn't expected")

# test cases for the Pfam serializer
class PfamSerializerTest(APITestCase):
    pfam1 = None
    pfamSerializer = None
    data = None

    def setUp(self):
        self.pfam1 = PfamFactory.create()
        self.pfamSerializer = PfamSerializer(instance=self.pfam1)
        self.data = self.pfamSerializer.data

    def tearDown(self):
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)

    def test_pfamSerializerKeySetCorrect(self):
        self.assertEqual(set(self.data.keys()), set(['domain_id', 'domain_description']))

    def test_pfamSerializerDomainIdHasCorrectData(self):
        self.assertEqual(self.data['domain_id'], self.pfam.domain_id)

    def test_pfamSerializerDomainIdHasCorrectData(self):
        self.assertEqual(self.data['domain_description'], self.pfam1.domain_description)

# test cases for the Protein serializer        
class ProteinSerializerTest(APITestCase):
    protein1 = None
    proteinSerializer = None
    data = None

    def setUp(self):
        self.protein1 = ProteinFactory.create()
        self.proteinSerializer = ProteinSerializer(instance=self.protein1)
        self.data = self.proteinSerializer.data

    def tearDown(self):
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        Organism.objects.all().delete()
        OrganismFactory.reset_sequence(0)

    def test_proteinSerializerKeySetCorrect(self):
        self.assertEqual(set(self.data.keys()), set(['id','taxonomy', 'protein_id', 'sequence', 'length', 'pfams']))

    def test_proteinSerializerTaxonomyHasCorrectData(self):
        self.assertEqual(self.data['taxonomy'], self.protein1.taxonomy.taxa_id)

    def test_proteinSerializerProteinIdHasCorrectData(self):
        self.assertEqual(self.data['protein_id'], self.protein1.protein_id)

    def test_proteinSerializerSequenceHasCorrectData(self):
        self.assertEqual(self.data['sequence'], self.protein1.sequence)

    def test_proteinSerializerLengthHasCorrectData(self):
        self.assertEqual(self.data['length'], self.protein1.length)

# test cases for the ProteinDomain serializer
class ProteinDomainSerializerTest(APITestCase):
    proteinDomain1 = None
    proteinDomainSerializer = None
    data = None

    def setUp(self):
        self.proteinDomain1 = ProteinDomainFactory.create()
        self.proteinDomainSerializer = ProteinDomainSerializer(instance=self.proteinDomain1)
        self.data = self.proteinDomainSerializer.data

    def tearDown(self):
        ProteinDomain.objects.all().delete()
        ProteinDomainFactory.reset_sequence(0)
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)

    def test_proteinDomainSerializerKeySetCorrect(self):
        self.assertEqual(set(self.data.keys()), set(['pfam_id','start', 'stop', 'description']))

    def test_proteinDomainSerializerPfamIdHasCorrectData(self):
        self.assertEqual(self.data['pfam_id']['domain_id'], self.proteinDomain1.pfam_id.domain_id)

    def test_proteinDomainSerializerStartHasCorrectData(self):
        self.assertEqual(self.data['start'], self.proteinDomain1.start)

    def test_proteinDomainSerializerStopHasCorrectData(self):
        self.assertEqual(self.data['stop'], self.proteinDomain1.stop)
    
    def test_proteinDomainSerializerDescriptionHasCorrectData(self):
        self.assertEqual(self.data['description'], self.proteinDomain1.description)
