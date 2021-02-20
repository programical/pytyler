"""
Horizontal.py

The opposite to the Vertical layout. I like to use this on monitors with
1280x1024 (or 1920x1200) resolution, and Vertical on monitors with less
height to them (1280x720 or 1280x800).

Remember that this class inherits _cycle, help_find_next, and help_find_previous
from TileDefault.

Note that if you're creating your own tiling algorithm, you *MUST* add
    CLASS = CLASS_NAME
at the bottom of your class definition file (see the bottom of this file
for an example). This is so tiling algorithms can be dynamically loaded.
"""

from PyTyle.Tilers.TileDefault import TileDefault

class Horizontal (TileDefault):
    #
    # The core tiling algorithm. Every core tiling algorithm should start with
    # grabbing the current screen's workarea and factoring that into your
    # calculations. Feel free to follow my approach to tiling algorithms, or
    # come up with something else.
    #
    # Note: As I've been going through the source code writing these comments,
    # I've been thinking about generalizing tiling algorithms even more. So this
    # approach could change a little in the future. (Although I imagine the class
    # hierarchy will be staying the same, I like it.)
    #
    def _tile(self):
        x, y, width, height = self.screen.get_workarea()

        # set some vars...
        masters = self.storage.get_masters()
        slaves = self.storage.get_slaves()

        masterWidth = width if not masters else (width / len(masters))
        masterHeight = height if not slaves else int(height * self.state.get('height_factor'))
        masterY = y
        masterX = x

        slaveWidth = width if not slaves else (width / len(slaves))
        slaveHeight = height if not masters else height - masterHeight
        slaveY = y if not masters else (y + masterHeight)
        slaveX = x

        # resize the master windows
        for master in masters:
            self.help_resize(master, masterX, masterY, masterWidth, masterHeight, self.state.get('margin'))
            masterX += masterWidth

        # now resize the rest... keep track of heights/positioning
        for slave in slaves:
            self.help_resize(slave, slaveX, slaveY, slaveWidth, slaveHeight, self.state.get('margin'))
            slaveX += slaveWidth

    #
    # Increases the height of all master windows. Don't forget to decrease
    # the height of all slave windows. Won't do anything if there are either
    # no masters or no slaves.
    #
    def _master_increase(self, factor = 0.05):
        x, y, width, height = self.screen.get_workarea()

        slaves = self.storage.get_slaves()
        masters = self.storage.get_masters()

        # Stop if neither of either... haha
        if not slaves or not masters:
            return

        # first calculate pixels...
        pixels = int(((self.state.get('height_factor') + factor) * height) - (self.state.get('height_factor') * height))
        self.state.set('height_factor', self.state.get('height_factor') + factor)

        for slave in slaves:
            slave.resize(slave.x, slave.y + pixels, slave.width, slave.height - pixels)
        for master in masters:
            master.resize(master.x, master.y, master.width, master.height + pixels)

    #
    # Decreases the height of all master windows. Don't forget to increase
    # the height of all slave windows. Won't do anything if there are either
    # no masters or no slaves.
    #
    def _master_decrease(self, factor = 0.05):
        x, y, width, height = self.screen.get_workarea()

        slaves = self.storage.get_slaves()
        masters = self.storage.get_masters()

        # Stop if neither of either... haha
        if not slaves or not masters:
            return

        # first calculate pixels...
        pixels = int((self.state.get('height_factor') * height) - ((self.state.get('height_factor') - factor) * height))
        self.state.set('height_factor', self.state.get('height_factor') - factor)

        for slave in slaves:
            slave.resize(slave.x, slave.y - pixels, slave.width, slave.height + pixels)
        for master in masters:
            master.resize(master.x, master.y, master.width, master.height - pixels)

# You must have this line's equivalent for your tiling algorithm!
# This makes it possible to dynamically load tiling algorithms.
# (So that you may simply drop them into the Tilers directory,
# and add their name to the configuration- vini, vidi, vicci!)
CLASS = Horizontal
