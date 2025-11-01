from frozendict import frozendict

from bgpy.shared.enums import ASNs
from bgpy.simulation_engine import BGP, ROV
from bgpy.simulation_framework import ScenarioConfig, ValidPrefix
from bgpy.tests.engine_tests.utils import EngineTestConfig

from provable_rpki_sims.rov_path_scenario import ROVPathScenario
from provable_rpki_sims.rov_path_scenario_config import ROVPathScenarioConfig
from .as_graph_info_000 import as_graph_info_000


desc = ""

config_000 = EngineTestConfig(
    name="config_000",
    desc=desc,
    scenario_config=ROVPathScenarioConfig(
        ScenarioCls=ROVPathScenario,
        BasePolicyCls=BGP,
        AdoptPolicyCls=ROV,
        override_rp_asns=frozenset({777}),
        override_attacker_asns=frozenset({666}),
        override_victim_asns=frozenset({555}),
    ),
    as_graph_info=as_graph_info_000,
)