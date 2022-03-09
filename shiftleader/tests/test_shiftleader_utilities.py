from decimal import Decimal

import pytest
from mixer.backend.django import mixer
from shiftleader.utilities.utilities import convert_run_registry_to_trackercertification, to_date, chunks
from unittest.mock import MagicMock
pytestmark = pytest.mark.django_db

class TestUtilities:
    def test_to_date(self):
        assert datetime.date(2010, 5, 17) == to_date(datetime.datetime(2010, 5, 17))
        assert datetime.date(2010, 5, 17) == to_date(datetime.date(2010, 5, 17))
        assert datetime.date(2010, 5, 17) == to_date("2010-05-17")

    def test_chunks(self):
        assert [range(10, 20), range(20, 29)] == list(chunks(range(10, 29), 10))

    def test_convert_run_registry_to_trackercertification(self):
        input=[{'class': 'Collisions17', 'state': 'SIGNOFF', 'short_run': 1, 'significant': True, 'stop_reason': None, 'run_number': 299327, 'name': '/ReReco/Run2017B_UL2019/DQM', 'dataset_attributes': {'dc_state': 'waiting dqm gui', 'dt_state': 'COMPLETED', 'cms_state': 'waiting dqm gui', 'csc_state': 'COMPLETED', 'hlt_state': 'COMPLETED', 'l1t_state': 'COMPLETED', 'rpc_state': 'COMPLETED', 'ecal_state': 'COMPLETED', 'hcal_state': 'COMPLETED', 'lumi_state': 'COMPLETED', 'muon_state': 'COMPLETED', 'egamma_state': 'COMPLETED', 'global_state': 'OPEN', 'jetmet_state': 'COMPLETED', 'tracker_state': 'COMPLETED'}, 'deleted': False, 'version': 4260755, 'lumisections': {'dt-dt': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-hv': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-lv': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'cms-cms': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-csc': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-mem': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-mep': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'ecal-es': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hb': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-he': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hf': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-hlt': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-tau': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-jet': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-l1t': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-feb': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-rpc': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tau-tau': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-ddus': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'ecal-ebm': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-ebp': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-eem': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-eep': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-esm': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-esp': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-tpg': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-ho0': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-muon': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-elog': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': [' http://cmsonline.cern.ch/cms-elog/998994']}, 'btag-btag': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-csctf': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'ecal-ecal': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hbls': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hcal': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hels': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hfls': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-ho12': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-bjets': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-muons': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-l1tmu': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'lumi-lumi': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'muon-muon': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-noise': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': [' https://cmswbm.web.cern.ch/cmswbm/cmsdb/servlet/RPCSummary?Run=299327&TopMenu=RPCRunSummary2&TopMenu2=ZeroPage&SubMenu=1']}, 'csc-strips': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-timing': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'dc-lowlumi': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-laser': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-noise': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-ho0ls': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-global': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-jetmet': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ctpps-ctpps': {'BAD': 82, 'EMPTY': 0, 'causes': [], 'comments': []}, 'ecal-timing': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-ho12ls': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-photons': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-e_gamma': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-hf_tech': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-l1tcalo': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-muon_dt': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-gasgains': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-segments': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'l1t-bcs_tech': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-hf_rings': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-muon_csc': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-muon_rpc': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-rpc_tech': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-software': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'castor-castor': {'EMPTY': 0, 'causes': ['UNDEF'], 'EXCLUDED': 82, 'comments': []}, 'csc-integrity': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-occupancy': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-pedestals': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-triggerpe': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'dt-dt_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-analysis': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'egamma-egamma': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-electrons': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-technical': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'jetmet-jetmet': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-bptx_tech': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-pixel': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-strip': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-track': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-efficiency': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-resolution': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'ctpps-rp45_210': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp45_220': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp45_cyl': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp56_210': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp56_220': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp56_cyl': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ecal-preshower': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-csc_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-collisions': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-es_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-hlt_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-energy_sums': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-rpc_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tau-tau_private': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'btag-btag_private': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ecal-ecal_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hcal_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'lumi-lumi_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'muon-muon_private': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'castor-castor_private': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'egamma-egamma_private': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'jetmet-jetmet_private': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-pixel_private': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-strip_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-track_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}}}]


        ret = convert_run_registry_to_trackercertification(input)

        print(ret)

        assert [{'state': 'SIGNOFF', 'short_run': 1, 'significant': True, 'stop_reason': None, 'dataset_attributes': {'dc_state': 'waiting dqm gui', 'dt_state': 'COMPLETED', 'cms_state': 'waiting dqm gui', 'csc_state': 'COMPLETED', 'hlt_state': 'COMPLETED', 'l1t_state': 'COMPLETED', 'rpc_state': 'COMPLETED', 'ecal_state': 'COMPLETED', 'hcal_state': 'COMPLETED', 'lumi_state': 'COMPLETED', 'muon_state': 'COMPLETED', 'egamma_state': 'COMPLETED', 'global_state': 'OPEN', 'jetmet_state': 'COMPLETED', 'tracker_state': 'COMPLETED'}, 'deleted': False, 'version': 4260755, 'lumisections': {'dt-dt': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-hv': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-lv': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'cms-cms': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-csc': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-mem': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-mep': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'ecal-es': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hb': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-he': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hf': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-hlt': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-tau': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-jet': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-l1t': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-feb': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-rpc': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tau-tau': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-ddus': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'ecal-ebm': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-ebp': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-eem': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-eep': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-esm': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-esp': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-tpg': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-ho0': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-muon': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-elog': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': [' http://cmsonline.cern.ch/cms-elog/998994']}, 'btag-btag': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-csctf': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'ecal-ecal': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hbls': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hcal': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hels': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hfls': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-ho12': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-bjets': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-muons': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-l1tmu': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'lumi-lumi': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'muon-muon': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-noise': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': [' https://cmswbm.web.cern.ch/cmswbm/cmsdb/servlet/RPCSummary?Run=299327&TopMenu=RPCRunSummary2&TopMenu2=ZeroPage&SubMenu=1']}, 'csc-strips': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-timing': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'dc-lowlumi': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-laser': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-noise': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-ho0ls': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-global': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-jetmet': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ctpps-ctpps': {'BAD': 82, 'EMPTY': 0, 'causes': [], 'comments': []}, 'ecal-timing': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-ho12ls': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-photons': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-e_gamma': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-hf_tech': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-l1tcalo': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-muon_dt': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-gasgains': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-segments': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'l1t-bcs_tech': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-hf_rings': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-muon_csc': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-muon_rpc': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-rpc_tech': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-software': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'castor-castor': {'EMPTY': 0, 'causes': ['UNDEF'], 'EXCLUDED': 82, 'comments': []}, 'csc-integrity': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-occupancy': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-pedestals': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-triggerpe': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'dt-dt_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-analysis': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'egamma-egamma': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-electrons': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-technical': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'jetmet-jetmet': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-bptx_tech': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-pixel': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-strip': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-track': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-efficiency': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'csc-resolution': {'EMPTY': 0, 'NOTSET': 82, 'causes': ['UNDEF'], 'comments': []}, 'ctpps-rp45_210': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp45_220': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp45_cyl': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp56_210': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp56_220': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ctpps-rp56_cyl': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ecal-preshower': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'csc-csc_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-collisions': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'ecal-es_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hlt-hlt_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'l1t-energy_sums': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'rpc-rpc_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tau-tau_private': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'btag-btag_private': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'ecal-ecal_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'hcal-hcal_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'lumi-lumi_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'muon-muon_private': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'castor-castor_private': {'EMPTY': 0, 'NOTSET': 82, 'causes': [], 'comments': []}, 'egamma-egamma_private': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'jetmet-jetmet_private': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-pixel_private': {'GOOD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-strip_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}, 'tracker-track_private': {'BAD': 82, 'EMPTY': 0, 'causes': ['UNDEF'], 'comments': []}}, 'dataset': '/ReReco/Run2017B_UL2019/DQM', 'runreconstruction__run__run_number': 299327, 'runreconstruction__run__run_type': 'collisions', 'runreconstruction__reconstruction': 'rerecoul', 'pixel': 'Good', 'strip': 'Good', 'tracking': 'Good'}] == ret


    def test_convert_run_registry_to_trackercertification_no_type(self):
        input = [{'class': 'Commissioning22', 'state': 'SIGNOFF', 'significant': True, 'stop_reason': 'CSC goes to local', 'run_number': 348409, 'name': '/Express/Commissioning2022/DQM\n', 'dataset_attributes': {'dc_state': 'waiting dqm gui', 'dt_state': 'waiting dqm gui', 'cms_state': 'waiting dqm gui', 'csc_state': 'waiting dqm gui', 'gem_state': 'waiting dqm gui', 'hlt_state': 'waiting dqm gui', 'l1t_state': 'waiting dqm gui', 'rpc_state': 'waiting dqm gui', 'tau_state': 'waiting dqm gui', 'btag_state': 'waiting dqm gui', 'ecal_state': 'waiting dqm gui', 'hcal_state': 'waiting dqm gui', 'lumi_state': 'waiting dqm gui', 'muon_state': 'waiting dqm gui', 'appeared_in': [], 'ctpps_state': 'waiting dqm gui', 'castor_state': 'waiting dqm gui', 'egamma_state': 'waiting dqm gui', 'global_state': 'waiting dqm gui', 'jetmet_state': 'waiting dqm gui', 'tracker_state': 'waiting dqm gui'}, 'datasets_in_gui': [], 'deleted': False, 'version': 45653780, 'lumisections': {'dt-dt': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'csc-tf': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'rpc-hv': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'rpc-lv': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'cms-cms': {'BAD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'csc-csc': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'ecal-es': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'gem-gem': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'hcal-hb': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hcal-he': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hcal-hf': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hlt-hlt': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'hlt-tau': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-l1t': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'rpc-feb': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'rpc-rpc': {'GOOD': 626, 'EMPTY': 0, 'causes': [], 'STANDBY': 2, 'comments': []}, 'tau-tau': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'ecal-ebm': {'EMPTY': 0, 'causes': [], 'STANDBY': 628, 'comments': []}, 'ecal-ebp': {'EMPTY': 0, 'causes': [], 'STANDBY': 628, 'comments': []}, 'ecal-eem': {'EMPTY': 0, 'causes': [], 'STANDBY': 628, 'comments': []}, 'ecal-eep': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'ecal-esm': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'ecal-esp': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'ecal-tpg': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hcal-ho0': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'rpc-elog': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'btag-btag': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'ecal-ecal': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'hcal-hcal': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'hcal-ho12': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hlt-bjets': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hlt-muons': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-l1tmu': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'lumi-lumi': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'muon-muon': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'rpc-noise': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'csc-strips': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'csc-timing': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'dc-lowlumi': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'ecal-laser': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'ecal-noise': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hcal-hb_ls': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hcal-he_ls': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hcal-hf_ls': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hlt-jetmet': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'ctpps-ctpps': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'ecal-timing': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hcal-hoO_ls': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hlt-photons': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-e_gamma': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-hf_tech': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-l1tcalo': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'l1t-muon_dt': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'csc-gasgains': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'csc-segments': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'hcal-ho12_ls': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-bcs_tech': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-hg_rings': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-muon_csc': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-muon_rpc': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-rpc_tech': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-software': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'castor-castor': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'csc-integrity': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'csc-occupancy': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'csc-pedestals': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'ecal-analysis': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'egamma-egamma': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'hlt-electrons': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hlt-technical': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'jetmet-jetmet': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'l1t-bptx_tech': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'tracker-pixel': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'tracker-strip': {'GOOD': 628, 'EMPTY': 0, 'causes': [], 'comments': []}, 'tracker-track': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'csc-efficiency': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'csc-resolution': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'csc-triggergpe': {'EMPTY': 0, 'NOTSET': 628, 'causes': [], 'comments': []}, 'ctpps-rp45_210': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'ctpps-rp45_220': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'ctpps-rp45_cyl': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'ctpps-rp56_210': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'ctpps-rp56_220': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'ctpps-rp56_cyl': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'ecal-preshower': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'hlt-hlt_global': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'ecal-collisions': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'l1t-energy_sums': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}, 'ctpps-time45_box': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'ctpps-time56_box': {'EMPTY': 0, 'causes': [], 'EXCLUDED': 628, 'comments': []}, 'cms-infrastructure': {'EMPTY': 0, 'causes': [], 'comments': [], 'NO VALUE FOUND': 628}}}]
        ret = convert_run_registry_to_trackercertification(input)
        assert 'runreconstruction__run__run_type' not in ret[0]
