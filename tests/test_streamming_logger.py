from galileo.logger.streaming import GalileoStreamingLogger


def test_check_that_class_implements_abstract_methods():
    assert GalileoStreamingLogger() is not None
