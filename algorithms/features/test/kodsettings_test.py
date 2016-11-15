from ..kodsettings import KODSettings, BRISKDetectorType


def KODSettings_test():
    settings = KODSettings()
    assert settings is not None
    default_settings = {'Neighbours Distance': 1.0, 'Probability': 25.0, 'Detector Type': BRISKDetectorType,
                        'Detector Settings': {'thresh': 10, 'octaves': 0, 'patternScale': 1.0}}
    test_settings = {'Neighbours Distance': 1.5, 'Probability': 10.0, 'Detector Type': BRISKDetectorType,
                        'Detector Settings': {'thresh': 8, 'octaves': 0, 'patternScale': 2.0}}
    assert settings.exportSettings() == default_settings
    settings.importSettings(test_settings)
    assert settings.exportSettings() == test_settings
    settings.dump()
