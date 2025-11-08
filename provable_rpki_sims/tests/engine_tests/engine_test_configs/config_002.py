from bgpy.simulation_engine import BGP, ROV
from bgpy.tests.engine_tests.utils import EngineTestConfig

from provable_rpki_sims.rov_path_scenario import ROVPathScenario
from provable_rpki_sims.rov_path_scenario_config import ROVPathScenarioConfig
from .as_graph_info_001 import as_graph_info_001


desc = ""

config_002 = EngineTestConfig(
    name="config_002",
    desc=desc,
    scenario_config=ROVPathScenarioConfig(
        ScenarioCls=ROVPathScenario,
        BasePolicyCls=BGP,
        AdoptPolicyCls=ROV,
        num_rps=3,
        override_attacker_asns=frozenset({666}),
        override_victim_asns=frozenset({777}),
    ),
    as_graph_info=as_graph_info_001,
)