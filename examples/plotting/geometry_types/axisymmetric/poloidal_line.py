import logging

import numpy as np

from geometry_types.base import GeometryType

logger = logging.getLogger(__name__)


class PoloidalLine(GeometryType):
    def load(self, *, max_phi=2 * np.pi, num_phi=20, **kwargs):
        # TODO:implement
        pass

    def _plot_impl(self, plotter, part):
        # TODO:implement
        pass
