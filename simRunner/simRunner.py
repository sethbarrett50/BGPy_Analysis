from pathlib import Path
from multiprocessing import cpu_count
from utils import timing_decorator, dirMaker

from bgpy.enums import SpecialPercentAdoptions

from bgpy.simulation_engine.policies import ASPA, ROV, OnlyToCustomers
from bgpy.simulation_framework import Simulation, ScenarioConfig, PrefixHijack, preprocess_anns_funcs


def SimSelector(configDict: dict) -> None:
    """
    Selects and runs the appropriate simulation based on the given configuration.

    This function determines the appropriate simulation runner to use based on the 'scenario' and 'asType' values from the provided configuration dictionary. It constructs the output directory path using the `dirMaker` function, and then calls the corresponding simulation runner function.

    Args:
        configDict (dict): Dictionary containing user-selected configurations for 'policy', 'scenario', and 'asType'.

    Returns:
        None
    """
    simOutputDir = dirMaker(configDict)


    # ASPA Specific
    if configDict['policy'] == ASPA:
        if configDict["scenario"] == 'ForgedOriginSubPrefix':
            if configDict["asType"] == 'NoDeploymentType':
                # For ASPA with forged-origin prefix and no deployment type
                # __ASPA_FO_NoType_SimRunner(configDict, simOutputDir) DEPRECIATED
                sc = ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ASPA,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.forged_origin_export_all_hijack
                    ),
                    BasePolicyCls=ROV
                )

            else:
                # For ASPA with forged-origin prefix and regular deployment type
                # __ASPA_FO_SimRunner(configDict, simOutputDir) DEPRECIATED
                sc = ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ASPA,
                    adoption_subcategory_attrs=(
                        configDict["asType"].value,) if configDict["asType"] else (),
                    preprocess_anns_func=(
                        preprocess_anns_funcs.forged_origin_export_all_hijack
                    ),
                    BasePolicyCls=ROV
                )
        else:
            if configDict["asType"] == 'NoDeploymentType':
                # For ASPA with non-forged origin with no deployment type
                # __ASPA_NoType_SimRunner(configDict, simOutputDir) DEPRECIATED
                sc = ScenarioConfig(
                    ScenarioCls=configDict['scenario'],
                    AdoptPolicyCls=ASPA,
                    BasePolicyCls=ROV
            )


            else:
                # For ASPA with non-forged origin with regular deployment type
                # __ASPA_SimRunner(configDict, simOutputDir) DEPRECIATED
                sc = ScenarioConfig(
                    ScenarioCls=configDict['scenario'],
                    AdoptPolicyCls=ASPA,
                    adoption_subcategory_attrs=(
                        configDict["asType"].value,) if configDict["asType"] else (),
                    BasePolicyCls=ROV
                )

    # AS-Cones Specific
    elif configDict['policy'] == "AS-Cones":
        if configDict["scenario"] == 'ForgedOriginSubPrefix':
            if configDict["asType"] == 'NoDeploymentType':
                # For AS-Cones with forged-origin prefix and no deployment type
                sc = ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ASPA,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.forged_origin_export_all_hijack
                    ),
                    BasePolicyCls=OnlyToCustomers
                )

            else:
                # For AS-Cones with forged-origin prefix and regular deployment type
                sc = ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ASPA,
                    adoption_subcategory_attrs=(
                        configDict["asType"].value,) if configDict["asType"] else (),
                    preprocess_anns_func=(
                        preprocess_anns_funcs.forged_origin_export_all_hijack
                    ),
                    BasePolicyCls=OnlyToCustomers
                )
        else:
            if configDict["asType"] == 'NoDeploymentType':
                # For AS-Cones with non-forged origin with no deployment type
                sc = ScenarioConfig(
                    ScenarioCls=configDict['scenario'],
                    AdoptPolicyCls=ASPA,
                    BasePolicyCls=OnlyToCustomers
                )


            else:
                # For AS-Cones with non-forged origin with regular deployment type
                sc = ScenarioConfig(
                    ScenarioCls=configDict['scenario'],
                    AdoptPolicyCls=ASPA,
                    adoption_subcategory_attrs=(
                        configDict["asType"].value,) if configDict["asType"] else (),
                    BasePolicyCls=OnlyToCustomers
                )

    # Non-ASPA & Non-AS-Cones Special Case
    else:
        if configDict["scenario"] == 'ForgedOriginSubPrefix':
            if configDict["asType"] == 'NoDeploymentType':
                # For forged-origin prefix with no deployment type
                # __FO_NoType_SimRunner(configDict, simOutputDir) DEPRECIATED
                sc = ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=configDict["policy"],
                    preprocess_anns_func=(
                        preprocess_anns_funcs.forged_origin_export_all_hijack
                    )
                )

            else:
                # For forged-origin prefix with regular deployment type
                # __FO_SimRunner(configDict, simOutputDir) DEPRECIATED
                sc = ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=configDict["policy"],
                    adoption_subcategory_attrs=(
                        configDict["asType"].value,) if configDict["asType"] else (),
                    preprocess_anns_func=(
                        preprocess_anns_funcs.forged_origin_export_all_hijack
                    )
                )

        else:
            if configDict["asType"] == 'NoDeploymentType':
                # For any non-special case w/ NoDeploymentType
                # __NoType_SimRunner(configDict, simOutputDir) DEPRECIATED
                sc = ScenarioConfig(
                        ScenarioCls=configDict['scenario'],
                        AdoptPolicyCls=configDict["policy"]
                    )

            else:
                # For any non-special case
                # __SimRunner(configDict, simOutputDir) DEPRECIATED
                sc = ScenarioConfig(
                        ScenarioCls=configDict['scenario'],
                        AdoptPolicyCls=configDict["policy"],
                        adoption_subcategory_attrs=(
                            configDict["asType"].value,) if configDict["asType"] else ()
                    )
    __mainSim(sc=sc, simOutputDir=simOutputDir)


@timing_decorator
def __mainSim(sc:ScenarioConfig, simOutputDir:str) -> None:
    # Main Sim
    sim = Simulation(
        percent_adoptions=(
            SpecialPercentAdoptions.ONLY_ONE,
            0.1,
            0.2,
            0.4,
            0.8,
            0.99  # Using only 1 AS not adopting causes extreme variance ->SpecialPercentAdoptions.ALL_BUT_ONE
        ),
        scenario_configs=(sc,),
        output_dir=Path(f"{simOutputDir}"),
        num_trials=1000,
        parse_cpus=cpu_count(),
    )
    sim.run()

def main():
    print("File should not be run this way")


if __name__ == '__main__':
    main()
