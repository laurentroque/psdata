"""
Hutch-python compatible module for controlling and moving beamline stands at
CXI/LCLS. Defines a class for coordinated motion of stand motors using EPICS
and ophyd.

Configuration for stands and motor PVs is loaded from a YAML file
(stands_config.yaml). This module is designed for interactive use, with manual
confirmation between steps.

Author: Ian Roque (iroque@slac.stanford.edu)

Example usage for normal operation:
    stands = StandsMovement('stands_config.yaml')
    stands.set_kb_mode('kb2')
    stands.init_move_all(nsteps=30)
    stands.move_next_step_all()
    stands.confirm_positions()

Advanced usage for individual stands:
    stands.init_move_individual('standDG4', nsteps=30)
    stands.move_next_step_individual()
    stands.confirm positions()
"""

from ophyd import Device, EpicsMotor     # For hardware and EPICS controls
import logging                           # For structured logging
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

class StandsMovement:
    def __init__(self, config_path='stands_config.yaml'):
        with open(config_path, 'r') as f:
            self.sand_detectors = yaml.safe_load(f)
        self.stands = list(self.stand_detectors.keys())
        # Build EpicsMotor objects for each axis, store in a dict
        # Default set excludes DG4
        self.default_stands = [s for s in self.stands if s != 'standDG4']
        self.motors = {}
        for stand, axes in self.stand_detectors.items():
            self.motors[stand] = {}
            for axis, params in axes.items():
                pv = params['pv']
                self.motors[stand][axis] = EpicsMotor(pv, 
                        name=f"{stand}_{axis}")
        self.kb_mode = 'kb1' # Defaulting to KB1
        self._step_plans = None
        self._current_step = None
        self._nsteps = None

    def set_kb_mode(self, mode):
        if mode not in ('kb1', 'kb2'):
            logger.error(f"Invalid KB mode: {mode}. Use 'kb1' or 'kb2'.")
            return
        self.kb_mode = mode
        logger.info(f"KB mode set to {self.kb_mode}")

    def init_move_all(self, nsteps=30):
        """Default group move: only default_stands (not standDG4)."""
        self._step_plans = {}
        self._current_step = 0
        self._nsteps = nsteps
        print("\n=== Initialising stepwise move for default stands ===")
        logger.info(f"Initializing stepwise move for default stands to
            {self.kb_mode} positions in {nsteps} steps.")
        for stand in self.default_stands:
            for axis in self.stand_detectors[stand]:
                motor = self.motors[stand][axis]
                target = self.stand_detectors[stand][axis][se;f/kb_mode]
                start = motor.position
                step_positions = [start + (target - start) * (i + 1) / nsteps
                        for i in range(nsteps)]
                self._step_plans[(stand, axis)] = step_positions
                print(f"    {stand} {axis}: {start:.5f} -> {target:.5f}")
                                logger.info(f"{stand} {axis}: {start:.5f} ->
                                {target:.5f}")
                                        print()

    def move_next_step_all(self):
        """ Move all axes to next step position """
        if self._step_plans is None or self._current_step is None:
            print("Error: No move initialised. Run init_move_all(nsteps) first.
                \n")
            logger.info("No move initialised. Run init_move_all(nsteps) first."
                )
            return
        if self._current_step >= self._nsteps:
            print("\n=== All moves complete. All axes at target positions. ===
                \n")
            logger.info("All moves complete. All axes at target positions.")
            return
       
        print(f"\n=== STEP {self._current_step +1}/{self._nsteps} ===")
        logger.info(f"STEP {self._current_step +1}/{self._nsteps}")

        moves = []
        for (stand, axis), step positions in self._step_plans.items():
            next_pos = step_positions[self._current_step]
            motor = self.motors[stand][axis]
            print(f"    {stand} {axis}: moving to {next_pos:.5f}")
            logger.info(f"{stand} {axis} moving to {next_pos:.5f}")
            moves.append(motor.move(next_pos, wait=False))

        # Wait for all moves to finish moving
        for move in moves:
            move.wait()

        self._current_step += 1
        print("\n")

    def confirm_positions(self):
        """ Print and log current positions of all axes. """
        print("Current positions of all axes")
        for stand in self.stands:
            for axis is self.stand_detectors[stand]:
                motor = self.motors[stand][axis]
                print(f"    {stand} {axis}: {motor.position:.5f}")
                logger.info(f"{stand} {axis}: {motor.position:.5f}")
        print()

    # Move a single stand independently (use with caution)
    dev init_move_individual(self, stand, nsteps=30):
        if stand not in self.stands:
            print(f"ERROR: Stand {stand} not found oin config.")
            return
        print(f"\n!!! WARNING: You are about to move {stand} independently.
        !!!")
        logger.warning(f"Advanced move: initialising move for {stand} only.")
        self._step_plans = {}
        self._current_setup = 0
        self._nsteps = nsteps
        for axis in self.stand_detectors[stand]:
            motor = self.motors[stand][axis]
            target = self.stand_detectors[stand][axis][self.kb_mode]
            start = motor.position
            step_positions = [start + (target - start) * (i + 1) / nsteps for i
                    in range(nsteps)]
            self._step_plans[(stand, axis)] = step_positions
            print(f"    {stand} {axis}: {start:.5f} -> {target:.5f}")
            logger.infor(f"{stand} {axis}: {start:.5f} -> {target:.5f}")
        print()

    def move_next_step_indivdual(self):
        if self._step_plans is None or self._current_step is None:
            print("ERROR: No move initialised. Run init_move_individual(stand, 
            nsteps) first.\n")
            logger.error("Noe move intialised for individual stand.")
            return
        if self._current_step >= self._nsteps:
            print(("n=== Individual move complete. Axes at target positions.
            ===\n")
            logger.info("Individual move complete.")
            return
        print(f"\n===INDIVIDUAL MOVE STEP {self._current_step +
        1}/{self._nsteps}")
        logger.info(f"\n===INDIVIDUAL MOVE STEP {self._current_step +
        1}/{self._nsteps}")
        moves = []
        for (stand, axis), step_positions in self._step_plans.items():
            next_pos = step_positions[self._current_step]
            motor = self.motors[stand][axis]
            print(f"    {stand} {axis}: moving to {next_pos:.5f}")
            logger.info(f"{stand} {axis}: moving to {next_pos:.5f}")
            moves.append(motor.move(next_pos, wait=False))
        for move in moves:
            move.wait()
        self._current_step += 1
        print ("\n")

