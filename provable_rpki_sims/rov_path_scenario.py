import random
from typing import Optional

from roa_checker import ROA

from bgpy.simulation_framework import Scenario, ScenarioConfig
from bgpy.simulation_engine import BaseSimulationEngine, Announcement as Ann
from bgpy.enums import SpecialPercentAdoptions, Timestamps, Prefixes, ASGroups



class ROVPathScenario(Scenario):

    min_propagation_rounds = 2

    def __init__(
        self,
        *,
        scenario_config: ScenarioConfig,
        percent_adoption: float | SpecialPercentAdoptions = 0,
        engine: BaseSimulationEngine | None = None,
        attacker_asns: frozenset[int] | None = None,
        victim_asns: frozenset[int] | None = None,
        adopting_asns: frozenset[int] | None = None,
        rp_asns: frozenset[int] | None = None,
    ):
        """inits attrs

        Any kwarg prefixed with default is only required for the test suite/YAML
        """
        self.engine = engine
        # Config's ScenarioCls must be the same as instantiated Scenario
        assert scenario_config.ScenarioCls == self.__class__, (
            "The config's scenario class is "
            f"{scenario_config.ScenarioCls.__name__}, but the scenario used is "
            f"{self.__class__.__name__}"
        )

        self.scenario_config: ScenarioConfig = scenario_config
        self.percent_adoption: float | SpecialPercentAdoptions = percent_adoption

        self.attacker_asns: frozenset[int] = self._get_attacker_asns(
            scenario_config.override_attacker_asns,
            attacker_asns,
            engine,
        )

        self.victim_asns: frozenset[int] = self._get_victim_asns(
            scenario_config.override_victim_asns, victim_asns, engine
        )
        self.rp_asns: frozenset[int] = self._get_rp_asns(
            scenario_config.override_rp_asns, rp_asns, engine
        )
        self.adopting_asns: frozenset[int] = self._get_adopting_asns(
            scenario_config.override_adopting_asns,
            adopting_asns,
            engine,
        )

        if self.scenario_config.override_announcements is not None:
            self.announcements: tuple[Ann, ...] = (
                self.scenario_config.override_announcements
            )
        else:
            self.announcements = self._get_announcements(engine=engine)

        if self.scenario_config.override_roas is not None:
            self.roas: tuple[ROA, ...] = self.scenario_config.override_roas
        else:
            self.roas = self._get_roas(announcements=self.announcements, engine=engine)
        self._reset_and_add_roas_to_roa_checker()

        self.ordered_prefix_subprefix_dict: dict[str, list[str]] = (
            self._get_ordered_prefix_subprefix_dict()
        )

    #####################
    # Get relying party #
    #####################

    def _get_rp_asns(
        self,
        override_rp_asns: frozenset[int] | None,
        prev_rp_asns: frozenset[int] | None,
        engine: BaseSimulationEngine | None,
    ) -> frozenset[int]:
        """Returns rp ASN at random"""

        # This is coming from YAML, do not recalculate
        if override_rp_asns is not None:
            rp_asns = override_rp_asns
        # Reuse the rp from the last scenario for comparability
        elif (
            prev_rp_asns
            and len(prev_rp_asns) == self.scenario_config.num_rps
        ):
            rp_asns = prev_rp_asns
        # This is being initialized for the first time
        else:
            assert engine
            possible_rp_asns = self._get_possible_rp_asns(
                engine, self.percent_adoption
            )
            # https://stackoverflow.com/a/15837796/8903959
            rp_asns = frozenset(
                random.sample(
                    tuple(possible_rp_asns), self.scenario_config.num_rps
                )
            )

        err = "Number of rps is different from rp length"
        assert len(rp_asns) == self.scenario_config.num_rps, err

        return rp_asns

    def _get_possible_rp_asns(
        self,
        engine: BaseSimulationEngine,
        percent_adoption: float | SpecialPercentAdoptions,
    ) -> frozenset[int]:
        """Returns possible rp ASNs, defaulted from config"""

        possible_asns = engine.as_graph.asn_groups[
            self.scenario_config.rp_subcategory_attr
        ]
        err = "Make mypy happy"
        assert all(isinstance(x, int) for x in possible_asns), err
        assert isinstance(possible_asns, frozenset), err
        # Remove attackers from possible rps
        possible_asns = possible_asns.difference(self.attacker_asns)
        possible_asns = possible_asns.difference(self.victim_asns)
        return possible_asns

    #####################
    # Get Announcements #
    #####################

    def _get_announcements(
        self,
        *,
        engine: Optional["BaseSimulationEngine"] = None,
    ) -> tuple["Ann", ...]:
        """Returns a valid prefix announcement

        for subclasses of this EngineInput, you can set AnnCls equal to
        something other than Announcement
        """

        anns = list()
        for victim_asn in self.victim_asns:
            anns.append(
                self.scenario_config.AnnCls(
                    prefix=Prefixes.PREFIX.value,
                    as_path=(victim_asn,),
                    timestamp=Timestamps.VICTIM.value,
                )
            )
        return tuple(anns)
    

    def post_propagation_hook(
        self,
        engine: "BaseSimulationEngine",
        percent_adopt: float | SpecialPercentAdoptions,
        trial: int,
        propagation_round: int,
    ) -> None:
        
        if propagation_round == 0:

            # TODO: setup 3rd entity (relying party), set all ASes on path from victim (repo) to relying party as ROV adopters
            assert self.rp_asns, "You must select at least 1 relying party AS"
            adopting_asns: set[int] = set(self.adopting_asns)
            for rp_asn in self.rp_asns:
                rp_as_obj = engine.as_graph.as_dict[rp_asn]
                for prefix, ann in rp_as_obj.policy.local_rib.data.items():
                    if prefix == Prefixes.PREFIX.value:
                        for asn in ann.as_path:
                            adopting_asns.add(asn)
            self.adopting_asns = frozenset(adopting_asns)

            announcements: list[Ann] = list(self.announcements)
            assert self.attacker_asns, "You must select at least 1 attacker AS"
            for attacker_asn in self.attacker_asns:
                announcements.append(
                    self.scenario_config.AnnCls(
                        prefix=Prefixes.PREFIX.value,
                        as_path=(attacker_asn,),
                        timestamp=Timestamps.ATTACKER.value,
                    )
                )
                announcements.append(
                    self.scenario_config.AnnCls(
                        prefix=Prefixes.SUBPREFIX.value,
                        as_path=(attacker_asn,),
                        timestamp=Timestamps.ATTACKER.value,
                    )
                )
            self.announcements = tuple(announcements)
            self.setup_engine(engine)
            engine.ready_to_run_round = 1


    @property
    def untracked_asns(self) -> frozenset[int]:
        """
        We only track whether the relying party was hijacked
        """
        all_asns = self.engine.as_graph.asn_groups[
            ASGroups.ALL_WOUT_IXPS.value
        ]
        return all_asns - self.rp_asns 
    
    @property
    def _untracked_asns(self) -> frozenset[int]:
        """
        We only track whether the relying party was hijacked
        """
        return self.untracked_asns