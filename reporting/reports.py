from opal.core import discoverable


class Report(discoverable.DiscoverableFeature):
    module_name = "reports"

    # The description displayed in the list view
    description = None

    def to_dict(self):
        return {}
