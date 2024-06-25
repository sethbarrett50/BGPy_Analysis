from pathlib import Path
from frozendict import frozendict
from bgpy.as_graphs.base import (
    ASGraphInfo,
    PeerLink,
    CustomerProviderLink as CPLink,
)
from bgpy.as_graphs.caida_as_graph.caida_as_graph_constructor import CAIDAASGraphConstructor
from bgpy.as_graphs.caida_as_graph.caida_as_graph_collector import CAIDAASGraphCollector
from bgpy.as_graphs.caida_as_graph.caida_as_graph import CAIDAASGraph

class CustomCAIDAASGraphConstructor(CAIDAASGraphConstructor):
    ASGraphCollectorCls = CAIDAASGraphCollector
    ASGraphCls = CAIDAASGraph

    def __init__(self, dl_path: Path = Path("./rels.txt")):
        self.as_graph_collector_kwargs = frozendict()
        self.as_graph_kwargs = frozendict()
        super().__init__(
            ASGraphCollectorCls=self.ASGraphCollectorCls,
            ASGraphCls=self.ASGraphCls,
            as_graph_collector_kwargs=frozendict(),
            as_graph_kwargs=frozendict(),
            tsv_path=None,
            stubs=True
        )
        self.dl_path = dl_path

    def _get_as_graph_info(self, invalid_asns: frozenset[int] = frozenset()) -> ASGraphInfo:
        input_clique_asns: set[int] = set()
        ixp_asns: set[int] = set()
        cp_links: set[CPLink] = set()
        peer_links: set[PeerLink] = set()

        with self.dl_path.open() as f:
            for line in f:
                if line.startswith("# input clique"):
                    self._extract_input_clique_asns(line, input_clique_asns, invalid_asns)
                elif line.startswith("# IXP ASes"):
                    self._extract_ixp_asns(line, ixp_asns, invalid_asns)
                elif not line.startswith("#"):
                    if "-1" in line:
                        self._extract_provider_customers(line, cp_links, invalid_asns)
                    else:
                        self._extract_peers(line, peer_links, invalid_asns)

        return ASGraphInfo(
            customer_provider_links=frozenset(cp_links),
            peer_links=frozenset(peer_links),
            ixp_asns=frozenset(ixp_asns),
            input_clique_asns=frozenset(input_clique_asns)
        )

    def analyze_as_graph(self) -> dict:
        as_graph = self.ASGraphCls(
            as_graph_info=self._get_as_graph_info()
        )
        total_ases = len(as_graph.ases)
        total_inputclique_ases = len([as_obj for as_obj in as_graph.ases if as_obj.input_clique])
        total_stub_ases = len([as_obj for as_obj in as_graph.ases if as_obj.stub])
        total_multihomed_ases = len([as_obj for as_obj in as_graph.ases if as_obj.multihomed])
        
        return {
            "total_ases": total_ases,
            "total_inputclique_ases": total_inputclique_ases,
            "total_stub_ases": total_stub_ases,
            "total_multihomed_ases": total_multihomed_ases,
        }

# This code is solely dedicated to located how many of each type of as is present in the CAIDA Serial-2 dataset
constructor = CustomCAIDAASGraphConstructor()
analysis_results = constructor.analyze_as_graph()
for k,v in analysis_results.items():
    print(f'{k}: {v}')