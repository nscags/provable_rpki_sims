from dataclasses import dataclass

from bgpy.simulation_framework import ScenarioConfig
from bgpy.enums import ASGroups



@dataclass(frozen=True)
class ROVPathScenarioConfig(ScenarioConfig):
    num_rps: int = 1
    override_rp_asns: frozenset[int] | None = None
    rp_subcategory_attr: str = ASGroups.STUBS_OR_MH.value
