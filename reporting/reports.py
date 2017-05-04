from opal.core import discoverable


class Report(discoverable.DiscoverableFeature):
    module_name = "reports"

    @property
    def description(self):
        raise NotImplementedError("please implement a description")
