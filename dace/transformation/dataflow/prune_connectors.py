# Copyright 2019-2020 ETH Zurich and the DaCe authors. All rights reserved.

from typing import Any, Dict, Union

from dace import registry, SDFG, SDFGState
from dace.transformation import transformation as pm, helpers
from dace.sdfg import nodes, utils

@registry.autoregister_params(singlestate=True, strict=True)
class PruneConnectors(pm.Transformation):
    """ Removes unused connectors from nested SDFGs, as well as their memlets
        in the outer scope, replacing them with empty memlets if necessary.
    """

    nsdfg = pm.PatternNode(nodes.NestedSDFG)

    @staticmethod
    def expressions():
        return [utils.node_path_graph(PruneConnectors.nsdfg)]

    @staticmethod
    def can_be_applied(graph: Union[SDFG, SDFGState],
                       candidate: Dict['PatternNode', int],
                       expr_index: int,
                       sdfg: SDFG,
                       strict: bool = False) -> bool:

        nsdfg = graph.node(candidate[PruneConnectors.nsdfg])

        read_set = set()
        write_set = set()

        for state in nsdfg.sdfg.states():
            rs, ws = helpers.read_and_write_set(state)
            read_set |= rs
            write_set |= ws

        if len(nsdfg.in_connectors.keys() - read_set) > 0:
            return True

        if len(nsdfg.out_connectors.keys() - write_set) > 0:
            return True

        return False

    def apply(self, sdfg: SDFG) -> Union[Any, None]:
        raise NotImplementedError
