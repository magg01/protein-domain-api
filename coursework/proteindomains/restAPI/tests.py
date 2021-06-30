import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

class PfamTest(APITestCase):

    pfam1 = None
    pfam2 = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        self.pfam1 = PfamFactory.create(domain_id = "CoiledCoil", domain_description = "coil prediction")
        self.pfam2 = PfamFactory.create(domain_id = "PF00014", domain_description = "Kunitz/Bovinepancreatictrypsininhibitordomain")
        self.good_url = reverse('pfam_api', kwargs={"domain_id": "PF00014"})
        self.bad_url = reverse('pfam_api', kwargs={"domain_id": "XXXXXX"})

    def tearDown(self):
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)

    def test_PfamDetailReturnSuccess(self):
        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, 200)

    def test_PfamDetailDomainIdRecievedCorrect(self):
        response = self.client.get(self.good_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['domain_id'], "PF00014")

    def test_PfamDetailReturnFailOnBadDomainId(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_PfamPostRequestMethodNotAllowed(self):
        response = self.client.post(self.good_url)
        self.assertEqual(response.status_code, 405)

    def test_PfamPutRequestMethodNotAllowed(self):
        response = self.client.put(self.good_url)
        self.assertEqual(response.status_code, 405)
        
    def test_PfamPatchRequestMethodNotAllowed(self):
        response = self.client.patch(self.good_url)
        self.assertEqual(response.status_code, 405)
    
    def test_PfamDeleteRequestMethodNotAllowed(self):
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 405)

class PfamSerializerTest(APITestCase):
    pfam1 = None
    pfamSerializer = None

    def setUp(self):
        self.pfam1 = PfamFactory.create()
        self.pfamSerializer = PfamSerializer(instance=self.pfam1)

    def tearDown(self):
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)

    def test_pfamSerializer(self):
        data = self.pfamSerializer.data
        self.assertEqual(set(data.keys()), set(['domain_id', 'domain_description']))

    def test_pfamSerializerDomainIdHasCorrectData(self):
        data = self.pfamSerializer.data
        self.assertEqual(data['domain_id'], self.pfam.domain_id)

    def test_pfamSerializerDomainIdHasCorrectData(self):
        data = self.pfamSerializer.data
        self.assertEqual(data['domain_description'], self.pfam1.domain_description)
        

