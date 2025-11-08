from time import time
from multiprocessing import cpu_count
from pathlib import Path
import sys
import os
from frozendict import frozendict
from datetime import date

from bgpy.simulation_engine.policies.rov import ROV
from bgpy.shared.enums import SpecialPercentAdoptions
from bgpy.simulation_framework import Simulation

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from provable_rpki_sims.rov_path_scenario_config import ROVPathScenarioConfig
from provable_rpki_sims.rov_path_scenario import ROVPathScenario


def main():
    """Run simulations :)"""

    # Simulation for the paper
    sim = Simulation(
        percent_adoptions=(
            SpecialPercentAdoptions.ONLY_ONE,
            0.1,
            0.2,
            0.4,
            0.8,
            0.99,  # SpecialPercentAdoptions.ALL_BUT_ONE,
        ),
        scenario_configs=(
            ROVPathScenarioConfig(
                ScenarioCls=ROVPathScenario, 
                AdoptPolicyCls=ROV,
            ),
        ),
        output_dir=Path("~/rpki/results").expanduser(),
        num_trials=1,
        parse_cpus=cpu_count(),
        as_graph_constructor_kwargs=frozendict(
            {
                "as_graph_collector_kwargs": frozendict({
                        "dl_time": date(2025, 9, 1),
                })
            }
        )
    )
    sim.run()


if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print(f"Total Runtime: {end - start}")