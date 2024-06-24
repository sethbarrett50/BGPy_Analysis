from simRunner import SimSelector

from bgpy.enums import ASGroups
from bgpy.simulation_engine.policies import ROV, ASPA, PeerROV


from bgpy.simulation_framework import SubprefixHijack, PrefixHijack, AccidentalRouteLeak

# Sim config choices
__configOptions = [
    [ROV, 'ROVPP', ASPA, PeerROV, 'AS-Cones'],
    [AccidentalRouteLeak, PrefixHijack,
        SubprefixHijack, 'ForgedOriginSubPrefix'],
    [ASGroups.INPUT_CLIQUE, ASGroups.STUBS,
        ASGroups.MULTIHOMED, "NoDeploymentType"]
]


def configSetter(configOptions: list = __configOptions, test: bool = False) -> dict:
    """
    Collects user configuration choices for a simulation setup.

    This function prompts the user with a series of questions to determine the type of defensive policy, attack scenario, and defensive deployment type they want to apply. It then stores these choices in a dictionary and returns it.

    Returns:
        dict: A dictionary containing user-selected configurations for 'policy', 'scenario', and 'asType'.
    """

    # Qurstions used in config setting loop
    userQuestions = [
        'Which type of defensive policy do you want applied:\n[1] ROV\n[2] ROV++[WiP]\n[3] ASPA\n[4] PeerROV \n[5] AS-Cones',
        'Which type of attack secenario do you want applied:\n[1] Accidental Route Leak\n[2] Prefix Hijack\n[3] Subprefix Hijack\n[4] Forged-Origin Prefix Hijack',
        'Which type of defensive deployment type do you want applied:\n[1] Input Clique\n[2] Stub\n[3] Multi-Homed\n[4] No Deployment Strategy'
    ]

    # Dict to contain user choice
    configDict = {}

    # Dict keys
    setableConfigs = ["policy", "scenario", "asType"]

    # Get user input and set configChoices accordingly
    for config, question, options in zip(setableConfigs, userQuestions, configOptions):
        print(question)
        simChoice = int(input("Enter your choice: "))
        configDict[config] = options[simChoice - 1]  # Sub 1 to match index

    if test:
        print(f"Running: {configDict['policy']} + {configDict['scenario']} + {configDict['asType']}")

    return configDict


def autoRun(configOptions: list = __configOptions, test : bool = False) -> None:
    '''
    Function added to automatically run all simulation types currently working

    Still need to implement ROV++, ASPA with ROV++, ForgedOriginSubPrefix and all AS deployment types inside the simRunner function
    '''
    for policy in configOptions[0]:
        if policy == 'ROVPP':
            continue
        for scenario in configOptions[1]:
            for deploymentType in configOptions[2]:
                if test:
                    print(f"Running: {policy} + {scenario} + {deploymentType}")
                try:
                    SimSelector(
                        {'policy': policy, 'scenario': scenario, 'asType': deploymentType})
                except Exception as ex:
                    print(f"{policy} + {scenario} + {deploymentType} has already been run\n\n\n{ex}")


def main():
    # Runs user choice sim config and prints test strings
    SimSelector(configSetter(test=True))

    # Run all sims
    # autoRun()

if __name__ == '__main__':
    main()
