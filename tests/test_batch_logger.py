from galileo.logger.batch import GalileoBatchLogger


def test_check_that_class_implements_abstract_methods():
    assert GalileoBatchLogger() is not None
