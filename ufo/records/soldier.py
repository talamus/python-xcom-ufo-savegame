from struct import pack, unpack
from ufo.records.baserecord import BaseRecord


class Soldier(BaseRecord):
    """
    ### Represents a single soldier from SOLDIER.DAT
    """

    FILE_NAME = "SOLDIER.DAT"
    NUMBER_OF_RECORDS = 250
    RECORD_LENGTH = 68  # bytes

    def unpack(self, data: bytes) -> None:
        (
            rank,
            base,
            craft,
            craft_before_injury,
            self.missions,
            self.kills,
            self.injury_recovery_days,
            self.importance,
            name,
            self.in_transit,
            self.initial_time_units,
            self.initial_health,
            self.initial_stamina,
            self.initial_reactions,
            self.initial_strenght,
            self.initial_firing_accuracy,
            self.initial_throwing_accuracy,
            self.initial_melee_accuracy,
            self.initial_psionic_strength,
            self.initial_psionic_skill,
            initial_bravery,
            self.time_units_improvement,
            self.health_improvement,
            self.stamina_improvement,
            self.reactions_improvement,
            self.strenght_improvement,
            self.firing_accuracy_improvement,
            self.throwing_accuracy_improvement,
            self.melee_accuracy_improvement,
            self.bravery_improvement,
            self.armor,
            self.recent_psi_training_increase,
            self.in_psi_training,
            self.recently_promoted,
            self.gender,
            self.appearance,
        ) = unpack("<HHHHhhhh25sBBBBBBBBBBBBBBBBBBBBBBBBBBB", data)

        if rank == 0xFFFF:
            self.active = False
            return
        else:
            self.active = True
            self.rank = rank

        self.base = None if base == 0xFF else base
        self.craft = None if craft == 0xFFFF else craft
        self.craft_before_injury = (
            None if craft_before_injury == 0xFFFF else craft_before_injury
        )

        name = name.decode(self.ENCODING)
        self.name = name.split("\0")[0]

        self.initial_bravery = 110 - (10 * initial_bravery)

    def pack(self) -> bytes:
        if not self.active:
            return pack("<H66s", 0xFFFF, b"")

        return pack(
            "<HHHHhhhh25sBBBBBBBBBBBBBBBBBBBBBBBBBBB",
            self.rank,
            0xFF if self.base == None else self.base,
            0xFFFF if self.craft == None else self.craft,
            0xFFFF if self.craft_before_injury == None else self.craft_before_injury,
            self.missions,
            self.kills,
            self.injury_recovery_days,
            self.importance,
            self.name.encode(self.ENCODING),
            self.in_transit,
            self.initial_time_units,
            self.initial_health,
            self.initial_stamina,
            self.initial_reactions,
            self.initial_strenght,
            self.initial_firing_accuracy,
            self.initial_throwing_accuracy,
            self.initial_melee_accuracy,
            self.initial_psionic_strength,
            self.initial_psionic_skill,
            int((110 - self.initial_bravery) / 10),
            self.time_units_improvement,
            self.health_improvement,
            self.stamina_improvement,
            self.reactions_improvement,
            self.strenght_improvement,
            self.firing_accuracy_improvement,
            self.throwing_accuracy_improvement,
            self.melee_accuracy_improvement,
            self.bravery_improvement,
            self.armor,
            self.recent_psi_training_increase,
            self.in_psi_training,
            self.recently_promoted,
            self.gender,
            self.appearance,
        )
