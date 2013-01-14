from zope import schema
from zope.interface import Interface


class ISettings(Interface):
    """ Define settings data structure """

    max_batch_size = schema.Text(title=u"Max. batch size",
                                 description=u"",
                                 required=False)


class ICollectiveSoapSearchLayer(Interface):
    """ A layer specific to this product.
        this layer is registered using browserlayer.xml in the package
        default GenericSetup profile
    """
