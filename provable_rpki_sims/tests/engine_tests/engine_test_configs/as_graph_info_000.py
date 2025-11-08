from bgpy.as_graphs import ASGraphInfo
from bgpy.as_graphs.base.links import CustomerProviderLink as CPLink
from bgpy.as_graphs.base.links import PeerLink
from bgpy.enums import ASNs


as_graph_info_000 = ASGraphInfo(
    peer_links=frozenset(
        {
            PeerLink(56, 92),
            PeerLink(56, 666),
        }
    ),
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=66, customer_asn=555),
            CPLink(provider_asn=12, customer_asn=555),
            CPLink(provider_asn=56, customer_asn=555),
            CPLink(provider_asn=55, customer_asn=66),
            CPLink(provider_asn=44, customer_asn=55),
            CPLink(provider_asn=44, customer_asn=666),
            CPLink(provider_asn=92, customer_asn=44),
            CPLink(provider_asn=8, customer_asn=777),
            CPLink(provider_asn=9, customer_asn=8),
            CPLink(provider_asn=92, customer_asn=8),
            CPLink(provider_asn=10, customer_asn=12),
            CPLink(provider_asn=9, customer_asn=10),
        ]
    ),
)