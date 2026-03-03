import detroit as d3
from detroit.types import Scaler as D3Scaler

from .domain import Domain
from .scaler_type import ScalerType


def make_scaler(
    domains: list[Domain],
    range_vals: list[int | float],
    nice: bool = True,
) -> D3Scaler:
    """
    Returns a scaler object from `detroit`.

    Parameters
    ----------
    domains : list[Domain]
        Domains collected in marks
    range_vals : list[int | float]
        Range values collected in marks
    nice : bool
        `True` to make the scaler's domain nicer

    Returns
    -------
    D3Scaler
        [`ScaleLinear`](https://detroit.readthedocs.io/en/latest/api/scale/linear.html#detroit.scale.linear.ScaleLinear)
        or
        [`ScaleTime`](https://detroit.readthedocs.io/en/latest/api/scale/time.html#detroit.scale.time.ScaleTime)
        or
        [`ScaleBand`](https://detroit.readthedocs.io/en/latest/api/scale/band.html#detroit.scale.band.ScaleBand)
    """
    domain = Domain.reduce(domains)
    domain_vals = domain.values
    scaler_type = domain.type
    scaler = d3.scale_linear()  # default value
    match scaler_type:
        case ScalerType.CONTINUOUS:
            scaler = d3.scale_linear().set_domain(domain_vals).set_range(range_vals)
        case ScalerType.TIME:
            scaler = d3.scale_time().set_domain(domain_vals).set_range(range_vals)
        case ScalerType.BAND:
            scaler = (
                d3.scale_band()
                .set_domain(domain_vals)
                .set_range(range_vals)
                .set_padding(0.1)
            )
        case ScalerType.UNKNOWN:
            raise RuntimeError("Undefined scaler")

    if nice and scaler_type in [ScalerType.CONTINUOUS, ScalerType.TIME]:
        scaler = scaler.nice()

    return scaler
