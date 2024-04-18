from pydantic.dataclasses import dataclass


@dataclass
class Params():
    fracRx: float = 0.8  # fraction of Red component in full-spectrum Red channel
    fracRy: float = 0.2  # fraction of Infrared component in full-spectrum Red channel
    fracGx: float = 1.0  # fraction of Green component in full-spectrum Green channel
    fracGy: float = 0.0  # fraction of Infrared component in full-spectrum Green channel
    fracBx: float = 0.0  # fraction of Blue component in full-spectrum Blue channel
    fracBy: float = 1.0  # fraction of Infrared component in full - spectrum Blue channel

    gammaRx: float = 0.5  # gamma correction of Red component in full - spectrum Red channel
    gammaRy: float = 1.0  # gamma correction of Infrared component in full - spectrum Red channel
    gammaGx: float = 1.0  # gamma correction of Green component in full - spectrum Green channel
    gammaGy: float = 1.0  # gamma correction of Infrared component in full - spectrum Green channel
    gammaBx: float = 0.0  # gamma correction of Blue component in full - spectrum Blue channel
    gammaBy: float = 2.0  # gamma correction of Infrared component in full - spectrum Blue channel
