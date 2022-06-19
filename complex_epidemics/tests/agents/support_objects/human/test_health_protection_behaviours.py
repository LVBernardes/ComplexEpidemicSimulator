from complex_epidemics.agents.support_objects.human.health_protection_measures import (
    ApplicationQuality,
    HandWashing,
    MaskType,
    MaskWearing,
    ProtectionMeasure,
    SocialDistancing,
)


class TestHealthProtectionBehaviours:
    def test_instantiation(self):

        new_protection = ProtectionMeasure()
        new_hand_washing = HandWashing()
        new_mask_wearing = MaskWearing()
        new_social_distance = SocialDistancing()

        assert (
            isinstance(new_protection, ProtectionMeasure)
            and isinstance(new_hand_washing, HandWashing)
            and isinstance(new_mask_wearing, MaskWearing)
            and isinstance(new_social_distance, SocialDistancing)
        )

    def test_method_get_efficacy(self):

        new_hand_washing = HandWashing()
        new_mask_wearing = MaskWearing(mask_type=MaskType.RESPIRATOR)
        new_social_distance = SocialDistancing()

        expected_hand_washing_efficacy = 0.2
        expected_mask_wearing_efficacy = 0.95
        expected_social_distance_efficacy = 0.8

        assert (
            new_hand_washing.get_efficacy() == expected_hand_washing_efficacy
            and new_mask_wearing.get_efficacy() == expected_mask_wearing_efficacy
            and new_social_distance.get_efficacy() == expected_social_distance_efficacy
        )

    def test_method_change_application_quality(self):

        new_hand_washing = HandWashing()
        new_mask_wearing = MaskWearing()
        new_social_distance = SocialDistancing()

        new_hand_washing.change_application_quality(ApplicationQuality.POOR)
        new_mask_wearing.change_application_quality(ApplicationQuality.GOOD)

        expected_hand_washing_quality = ApplicationQuality.POOR
        expected_mask_wearing_quality = ApplicationQuality.GOOD
        expected_social_distance_quality = ApplicationQuality.EXCELLENT

        assert (
            new_hand_washing.application == expected_hand_washing_quality
            and new_mask_wearing.application == expected_mask_wearing_quality
            and new_social_distance.application == expected_social_distance_quality
        )

    def test_efficacy_after_application_quality_change(self):

        new_hand_washing = HandWashing()
        new_mask_wearing = MaskWearing(mask_type=MaskType.SURGICAL)
        new_social_distance = SocialDistancing()

        new_hand_washing.change_application_quality(ApplicationQuality.POOR)
        new_mask_wearing.change_application_quality(ApplicationQuality.GOOD)

        expected_hand_washing_efficacy = round(0.2 * 0.33, 3)
        expected_mask_wearing_efficacy = round(0.7 * 0.66, 3)
        expected_social_distance_efficacy = 0.8

        real_hand_washing_efficacy = new_hand_washing.get_efficacy()
        real_mask_wearing_efficacy = new_mask_wearing.get_efficacy()
        real_social_distance_efficacy = new_social_distance.get_efficacy()

        assert (
            real_hand_washing_efficacy == expected_hand_washing_efficacy
            and real_mask_wearing_efficacy == expected_mask_wearing_efficacy
            and real_social_distance_efficacy == expected_social_distance_efficacy
        )
